from typing import Dict, Optional, List, TYPE_CHECKING

from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI

from toontown.groups import GroupGlobals
from toontown.groups.GroupEnums import Options
from toontown.groups.GroupFilterer import GroupFilterer, IgnoreSafetyEnum
from toontown.gui.toon.ToonHeadData import ToonHeadData
from toontown.notifications.notificationData.GenericTextNotification import GenericTextNotification, GenericTextId
from toontown.notifications.notificationData.GroupInviteNotification import GroupInviteNotification
from toontown.toon.DistributedToonAI import DistributedToonAI
from toontown.groups.GroupGlobals import (
    Responses, GroupType, GroupDefinition, BoardingGroupInformation,
    DEFAULT_GROUP, AI_RATELIMITER_MAX_HITS, AI_RATELIMITER_PERIOD, AI_STRONG_RATELIMITER_MAX_HITS,
    AI_STRONG_RATELIMITER_PERIOD
)
from toontown.groups.GroupClasses import GroupAI, GroupAvatarUDToon, GroupCreation
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.RateLimiter import IdRateLimiter

if TYPE_CHECKING:
    from toontown.ai.ToontownAIRepository import ToontownAIRepository


@DirectNotifyCategory()
class DistributedGroupManagerAI(DistributedObjectGlobalAI, GroupFilterer):
    def __init__(self, air: 'ToontownAIRepository'):
        DistributedObjectGlobalAI.__init__(self, air)
        GroupFilterer.__init__(self)
        self.air = air

        # We'll want to keep track of when an avatar changes zone.
        # It's important for the UD to keep track of where we are.
        self.accept('avatarEntered', self.updateUdAvatar)
        self.accept("DOLogicalChangeZone-all", self.avatarChangedZone)

        # When we receive publishedGroups, we'll keep up with a
        # far more verbose version, using classes.
        self.groups: Dict[int, GroupAI] = {}  # group id: group struct
        self.cachedGroups = {}

        # Some mappings for avId to group.
        self.avId2Group: Dict[int, GroupAI] = {}

        # Give each avId a ratelimiter.
        # Use this to prevent user floods.
        self.rateLimiter = IdRateLimiter(max_hits=AI_RATELIMITER_MAX_HITS, period=AI_RATELIMITER_PERIOD)
        self.strongRateLimiter = IdRateLimiter(max_hits=AI_STRONG_RATELIMITER_MAX_HITS, period=AI_STRONG_RATELIMITER_PERIOD)

        # Other parts of the AI can request a group to disband.
        self.accept('GroupManager-DisbandToonGroup', self.AI_disbandToonGroup)
        self.accept('GroupManager-DisbandAllToonGroups', self.AI_disbandAllGroups)

    def announceGenerate(self):
        self.notify.info("Starting GroupManager")
        DistributedObjectGlobalAI.announceGenerate(self)
        self.accept("avatarExited", self.handleAvatarExited)

    """
    Messenger calls 
    """

    def AI_disbandToonGroup(
        self,
        avId,
        requiredGroupType: Optional[List[GroupType]] = None,
        response: int = Responses.LeaveDisbanded.value
    ) -> None:
        """
        Disbands a group that this avId is a part of.
        """
        if requiredGroupType is not None:
            # This avId must be a part of a group of a specified type.
            group: Optional[GroupAI] = self.getGroupOfAvId(avId)
            if group is None:
                # The group must exist for us to do anything.
                return
            if group.groupType not in requiredGroupType:
                # We only disband if the group's groupType is within the list.
                return
        self.sendUpdate('disbandToonGroup', [avId, 0, response])

    def AI_disbandAllGroups(self):
        for group in self.groups.values():
            self.sendUpdate('disbandToonGroup', [group.owner, 1, Responses.DistrictDraining.value])

    """
    Updates from the AI sent to the UD
    """

    def updateUdAvatar(self, av: DistributedToonAI):
        self.notify.debug(
            f"Updating UD avatar.  av: {av.getName()} ({av.getDoId()})"
        )
        toon = GroupAvatarUDToon.fromStruct([
            av.getDoId(), av.getName(), av.zoneId, self.air.districtId,
            av.getMaxHp(), av.getGagLevels(), av.getPrestigeLevels(),
            av.getToonLevel(), ToonHeadData.makeFromToonAI(av).toStruct(),
            av.getHp(), av.getToonExp(),
        ])
        self.sendUpdate("avatarChangedZoneUd", [toon.toStruct(), 0])

    def avatarChangedZone(self, newZone, oldZone, av: DistributedToonAI):
        self.notify.debug(
            f"Avatar moved. new: {newZone} old: {oldZone} av: {av.getName()} ({av.getDoId()})"
        )
        toon = GroupAvatarUDToon.fromStruct([
            av.getDoId(), av.getName(), newZone, self.air.districtId,
            av.getMaxHp(), av.getGagLevels(), av.getPrestigeLevels(),
            av.getToonLevel(), ToonHeadData.makeFromToonAI(av).toStruct(),
            av.getHp(), av.getToonExp(),
        ])
        if oldZone is None:
            oldZone = 0
        # Toon entered cog lobby, force a suit on them
        # This isn't a great place for this, but it is convenient!!
        if newZone in ToontownGlobals.CogHQLobbies:
            deptIndex = ToontownGlobals.cogHQZoneId2deptIndex(newZone)
            av.b_setCogIndex(deptIndex)
        self.sendUpdate("avatarChangedZoneUd", [toon.toStruct(), oldZone])

    def announceGroupMemberEncounteredSuit(self, avId):
        # A group member encountered a suit this group cares about, send it off to the UD
        self.sendUpdate("announceGroupMemberEncounteredSuitUd", [avId])

    """
    Updates from UD sent to the AI
    """

    def receiveAllGroups(self, groupStructList):
        """
        Receive all groups from the UD.
        """
        self.cachedGroups = self.groups.copy()
        self.groups = {struct[0]: GroupAI.fromStruct(struct) for struct in groupStructList}

        # Cache some local info of the groups.
        self.avId2Group = {}
        for groupAI in self.groups.values():
            for avId in groupAI.avIds:
                self.avId2Group[avId] = groupAI

    def groupManagerReloaded_AI(self):
        """
        The group manager crashed and reloaded.
        We clean up and tell everyone what happened.
        :return:
        """
        self.groups = {}

        # Tell the universe about this predicament
        for avId in self.air.toonTracker.getAllToons():
            # First, tell the client about the reload.
            self.sendUpdateToAvatarId(avId, 'groupManagerReloaded_CL', [])

            # Then, tell UD about all the online folks.
            av = self.air.doId2do.get(avId)
            if not av:
                # !>?@#<?!>@<#?!>@#<
                continue
            self.updateUdAvatar(av)

    def _canToonUseGroups(self, avId):
        """Determines if a toon can create a group."""
        # Todo: Check if the avId has a group ban.
        canUseGroups = True
        return canUseGroups

    """
    Requests to the AI from the client
    """

    def createGroup(self, group, published, force):
        avId = self.air.getAvatarIdFromSender()
        if self.strongRateLimiter.userBlocked(avId):
            return
        toon: DistributedToonAI = self.air.doId2do.get(avId)
        if not toon:
            return

        # Several sanity checks.
        if self.air.districtMgr.draining:
            return self.sendUpdateToAvatarId(avId, "requestGroupCallback", [Responses.DistrictDraining.value, Responses.CannotMakeGroup.value, 0])

        groupCreation = GroupCreation.fromStruct(group)
        if groupCreation.groupType not in BoardingGroupInformation:
            groupType = GroupType(DEFAULT_GROUP)
        else:
            groupType = groupCreation.groupType

        # Get the associated group definition.
        groupDef: GroupDefinition = BoardingGroupInformation[groupType]
        # Don't allow groups to be made if they aren't available (Usually due to required holiday)
        if not groupDef.isGroupAvailable:
            return self.sendUpdateToAvatarId(avId, "requestGroupCallback",
                                             [Responses.GroupNotAvailable.value, Responses.CannotMakeGroup.value, 0])

        # Validate our options.
        if any(groupDef.getOptions()):
            for i in range(len(groupCreation.groupOptions)):
                groupDefOptions = [option.value for option in groupDef.getOptions()[i].options]
                if groupCreation.groupOptions[i] not in groupDefOptions:
                    groupCreation.groupOptions[i] = groupDefOptions[i]
        else:
            groupCreation.groupOptions = []

        # Validate our max size variable.
        if groupCreation.groupSize not in groupDef.maxSize:
            groupCreation.groupSize = groupDef.maxSize[0]

        if type(groupCreation.groupSize) in (tuple, list):
            groupCreation.groupSize = groupCreation.groupSize[0]

        # Perform checks on this toon to make sure that
        # they can indeed make this group.
        testResult = self.runGroupTests(toon, groupCreation, force)
        if testResult is not Responses.OK:
            return self.sendUpdateToAvatarId(avId, "requestGroupCallback",
                                             [testResult.value, Responses.CannotMakeGroup.value, groupType.value])

        # Before the group gets send to UD, tell UD about the av's location status.
        self.updateUdAvatar(toon)

        # OK, now send the group out.
        self.sendUpdate(
            "createGroupUd",
            [toon.getDoId(), groupCreation.toStruct(), self.air.districtId, published],
        )

    def updateGroupSettings(self, groupSettings: list):
        """
        Update the group given a settings list.
        UD will make sure they're valid settings for the group type.
        """
        avId = self.air.getAvatarIdFromSender()
        if self.rateLimiter.userBlocked(avId):
            return
        toon: DistributedToonAI = self.air.doId2do.get(avId)
        if not toon:
            return

        self.sendUpdate("updateGroupSettingsUd", [avId] + groupSettings)

    def requestTeleportToGroupBattleAI(self):
        avId = self.air.getAvatarIdFromSender()
        toon: DistributedToonAI = self.air.doId2do.get(avId)
        if not toon:
            return

        group = self.getGroupOfAvId(avId)
        if not group:
            return
        if not group.announcedBattle:
            return
        if group.avatarThatEncountered == 0:
            return

        self.sendUpdate("requestTeleportToGroupBattleUD", [avId])

    def mod_forceDisband(self, otherAvId: int):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.getDo(avId)
        if not av:
            return
        if not GroupGlobals.hasForceDisbandPermission(av):
            self.air.writeServerEvent('suspicious', avId, 'Toon sent a force disband request but didnt have permission!')
            return

        self.sendUpdate('disbandToonGroup', [otherAvId, 1, Responses.ModeratorDisband])
        av.addNotification(GenericTextNotification(
            textId=GenericTextId.Mod_SuccessfullyDisbandedGroup,
            title='MOD: Group Disbanded',
            subtitle='You have successfully disbanded this group.',
        ))

    """
    Player Inviting
    """

    def invitePlayerAI_getDna(self, invitedAvIds: list):
        """
        The Client has asked the AI about avIds to invite.
        We route through the AI in order to get the inviter's
        name and DNA to be sent to the invited avIds for their panel.

        :param invitedAvIds: A list of avIds.
        """
        # Get the toon.
        inviterAvId = self.air.getAvatarIdFromSender()
        if self.rateLimiter.userBlocked(inviterAvId):
            return

        toon: DistributedToonAI = self.air.doId2do.get(inviterAvId)
        if not toon:
            return

        # Kill the invite if the player who invited's group currently has a group battle up.
        group = self.isAvidInGroup(inviterAvId)
        if group and group.announcedBattle:
            toon.addNotification(GenericTextNotification(
                textId=GenericTextId.GroupDeniedInvite,
                title=TTLocalizer.GroupDenyBattleActive,
                subtitle=TTLocalizer.GroupDenyBattleActiveInvite,
            ))
            return

        # Cap the invite length.
        if len(invitedAvIds) > 8:
            invitedAvIds = invitedAvIds[:8]

        # Pass the update up to UD.
        self.sendUpdate(
            'invitePlayerUD_getToonData',
            [inviterAvId, invitedAvIds, toon.getName(), toon.getDNAString()]
        )

    def invitePlayerAI_validateInvited(self, groupStruct: list, inviterAvId: int, invitedAvIds: list):
        """
        The UD asked us to validate each user on each invited avId.
        :param groupStruct: A target group.
        :param inviterAvId: The avId who initiated the invite.
        :param invitedAvIds: The list of avIds that are attempted to be invited.
        :return: None.
        """
        # We'll be going over each tested toon.
        groupAI = GroupAI.fromStruct(groupStruct)

        for avId in invitedAvIds:
            # No self invite.
            if avId == inviterAvId:
                continue

            # Make sure the toon we're inviting is real.
            toon: DistributedToonAI = self.air.doId2do.get(avId)
            if not toon:
                # The toon is not in this district, ignore.
                continue

            # Get some properties of the toon.
            name = toon.getName()
            dna = toon.getDNAString()

            # If they are not accepting invites, auto reject.
            if not toon.getSettings().getSetting('acceptingGroupInvites'):
                # They do not want friends lol cry about it
                args = [inviterAvId, avId, Responses.UnacceptingInvites,
                        groupAI.groupCreation.toStruct(), name, dna]
                self.tellPlayerInviteFailedAI(*args)
                self.sendUpdate('tellPlayerInviteFailedAI', args)
                return

            # Test this toon to make sure they can join our group.
            testResult = self.runGroupTests(toon, groupAI.groupCreation, True, groupAI, ignoreSafety=IgnoreSafetyEnum.IgnoreZones)
            if testResult is not Responses.OK:
                # Tell the inviter why this Toon couldn't be invited.
                args = [inviterAvId, avId, testResult.value,
                        groupAI.groupCreation.toStruct(), name, dna]
                self.tellPlayerInviteFailedAI(*args)
                self.sendUpdate('tellPlayerInviteFailedAI', args)
                continue

            # This toon is OK. Let the UD know to query this invite.
            self.sendUpdate("invitePlayerUD_finalizeInvite", [inviterAvId, avId, name, dna])

    def tellPlayerInviteFailedAI(self, inviterAvId: int, invitedAvId: int, reason: int, groupCreation: list, name: str, invitedDna):
        """
        Upon a Toon's invite failing on group tests, we notify that toon
        about why the person they tried to invite could not join the group.

        :param inviterAvId:     The inviter's avId.
        :param invitedAvId:     The invited's avId.
        :param reason:          Reason they cannot join the group.
        :param groupCreation:   Group struct data.
        :param name:            Name of the invited Toon.
        :param invitedDna:      DNA string of the invited Toon.
        :return:                None.
        """
        toon: DistributedToonAI = self.air.doId2do.get(inviterAvId)
        if not toon:
            return

        # They're real -- send them their notif.
        groupCreation = GroupCreation.fromStruct(groupCreation)
        toon.addNotification(GroupInviteNotification(
            invitedAvId, name, invitedDna,
            GroupInviteNotification.state_failed,
            groupCreation.groupType, reason, 0,
            *groupCreation.groupOptions
        ))

    def requestGroup(self, targetAvId, force, avId: int = None, respondToAv: bool = True) -> bool:
        """
        Requests to join an AvId's target group.
        This will only succeed if their group is public,
        and the target is the group owner.

        Also, we will have to pass all the sanity checks.
        These will be generally different per group, and
        is all handled on the AI front.

        This method should be fairly safe to call on the AI side,
        but do be careful that it can be desynced from the UD and
        might deny the invite on the UD side regardless.
        """
        def sendResponse(responseEnum, groupType=0):
            if respondToAv:
                self.sendUpdateToAvatarId(avId, "requestGroupCallback", [responseEnum.value, Responses.CannotJoinGroup.value, groupType])
            return False

        avId = avId or self.air.getAvatarIdFromSender()
        if self.strongRateLimiter.userBlocked(avId):
            return False
        toon: DistributedToonAI = self.air.doId2do.get(avId)
        if not toon:
            return False

        # OK, let's go grab the targetAvId's group.
        targetGroup = self.isAvidInGroup(targetAvId, cached=False, includePrivate=False)
        if not targetGroup:
            return sendResponse(Responses.TryAgain)

        # Please make sure that they are not in a group!!
        group = self.isAvidInGroup(avId)
        if group:
            return sendResponse(Responses.AlreadyInGroup)

        # Other simple checks
        if not targetGroup.published:
            return sendResponse(Responses.GroupNotPublic)
        if targetGroup.avatarKicked(avId):
            return sendResponse(Responses.KickedFromGroup)
        if targetGroup.isFull:
            return sendResponse(Responses.GroupFilledUp)

        # And now, we delegate it to several mundane tasks.
        testResult = self.runGroupTests(toon, targetGroup.groupCreation, force, targetGroup, ignoreSafety=IgnoreSafetyEnum.IgnoreZones)
        if testResult is not Responses.OK:
            return sendResponse(testResult, groupType=targetGroup.groupType.value)

        # We've passed all of the checks!!
        self.sendUpdate("requestGroupUd", [avId, targetAvId])
        return True

    """
    Client requests, which go further to UD
    """

    def handleAvatarExited(self, av):
        # self.notify.debug(f"{av.doId} exited, notifying UD!")
        self.sendUpdate("toonOffline", [av.doId])

    def requestGoUdToAi(self, group, elevatorId):
        # Lock clients here, prepare to send to the group after 3 seconds, need to check if everything is valid.
        avs = []

        elevator = self.air.getDo(elevatorId)
        if not hasattr(elevator, "sendAvatarsToDestination"):
            return self.air.writeServerEvent(
                "suspicious",
                avId=group[4][0],
                issue="Tried to requestGo a group with a doId that was not an elevator",
            )

        for avId in [av[0] for av in group[4]]:
            av = self.air.getDo(avId)
            if not av or av.isDeleted():
                continue
            avs.append(av)
            self.sendUpdateToAvatarId(avId, "requestGoClientLocks", [])

        elevator.sendAvatarsToDestination([x.doId for x in avs])
        self.sendUpdate("disbandGroupAiToUd", [group[0]])

    """Helpers"""

    def getGroupOfAvId(self, avId) -> Optional[GroupAI]:
        """
        An optimized way to check if an avId is in a group.
        Does not account for caching, and always includes private groups.
        """
        return self.avId2Group.get(avId)

    def isAvidInGroup(self, avId, cached: bool = False, includePrivate: bool = True) -> GroupAI:
        """
        Checks if an avId is in a group.
        Set the cached flag if you need to check for groups
        when they may have possibly cleaned up/disbanded very recently.
        """
        group: GroupAI
        for group in self.groups.values():
            if (not group.published) and (not includePrivate):
                continue
            if avId in group.avIds:
                return group
        if cached:
            for group in self.cachedGroups.values():
                if (not group.published) and (not includePrivate):
                    continue
                if avId in group.avIds:
                    return group
        return None

    def getGroupFromId(self, groupId) -> GroupAI:
        return self.groups.get(groupId, None)

    def doesGroupExist(self, avIds: list, groupType: GroupType,
                       groupOption: Options = None, cached: bool = True) -> bool:
        """
        Given a list of avIds, look for a group type that sufficiently matches a group option.

        :param avIds: The relevant avIds.
        :param groupType: The GroupType to be found.
        :param groupOption: Any particular option we're looking for.
        :param cached: Should we look in our group cache (in case the group has disbanded)?
        """
        for avId in avIds:
            # Find the group.
            group = self.air.groupManager.isAvidInGroup(avId=avId, cached=cached)  # type: GroupAI

            # This av must be in a group.
            if group is None:
                continue

            # The group type must match.
            if group.groupType != groupType:
                continue

            # The av must be the owner.
            if group.owner != avId:
                continue

            if groupOption is not None:
                if groupOption not in group.getGroupCreation().getOptions():
                    continue

            # This group is valid and exists.
            return True

        # No group was found, cope.
        return False
