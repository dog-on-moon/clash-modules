from typing import Optional, TYPE_CHECKING

from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.task import Task
from panda3d.core import UniqueIdAllocator

from toontown.groups.GroupClasses import GroupUD, GroupAvatarUDToon, GroupCreation
from toontown.groups.GroupEnums import GroupType
from toontown.groups.GroupGlobals import (
    Responses, BoardingGroupInformation, PUBLISHED_GROUP_REFRESH_TIME,
    UD_RATELIMITER_MAX_HITS, UD_RATELIMITER_PERIOD
)
from toontown.hood.ZoneUtil import getHoodId
from toontown.notifications.notificationData.GroupCallbackNotification import GroupCallbackNotification
from toontown.notifications.notificationData.GroupInviteNotification import GroupInviteNotification
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.RateLimiter import RateLimiter

if TYPE_CHECKING:
    from toontown.utils.BuiltinHelper import *
    from toontown.uberdog.ToontownUberRepository import ToontownUberRepository


@DirectNotifyCategory()
class DistributedGroupManagerUD(DistributedObjectGlobalUD):
    def __init__(self, air):
        super().__init__(air)
        self.air: 'ToontownUberRepository' = air
        self.toons = {}
        self.groups = {}
        self.groupIdAllocator = UniqueIdAllocator(1, 60000)
        self.avIdRateLimiter = {}

        # A DNAString cache.
        self.avId2DNANetstring = {}

        # A toon name cache.
        self.avId2avName = {}

        # We cache inviter -> invited for invite validation.
        self.avIdInvites = {}

        # Accept hooks
        self.air.netMessenger.accept('toonOffline', self, self.toonOffline)

    def announceGenerate(self):
        self.notify.info("Starting GroupManager")
        DistributedObjectGlobalUD.announceGenerate(self)

        # Tell connected avIds that we have restarted.
        self.sendUpdate('groupManagerReloaded_AI')

        # Refresh published group state.
        self.refreshPublishedGroups()

    def getGroup(self, groupId: int) -> Optional[GroupUD]:
        """
        Returns the group with a matching id.

        :param groupId: The id of the group to get.
        :return: The group object if one is found under the specified id.
        """
        return self.groups.get(groupId)

    def cleanupGroup(self, group):
        """Cleans up a group."""
        self.air.netMessenger.send('groupUpdateUD', [group.groupId, 0, 0])
        self.groupIdAllocator.free(group.groupId)
        del self.groups[group.groupId]

    """Tasks"""

    def handleToonOffline(self, avId):
        if avId not in self.toons.keys():
            return
        del self.toons[avId]

        group = self.isAvidInGroup(avId)
        if group:
            if group.owner == avId:
                self._doDisband(avId, notify=1)
            else:
                group.removeAvatar(avId)

        if avId in self.avId2DNANetstring:
            del self.avId2DNANetstring[avId]

        if avId in self.avId2avName:
            del self.avId2avName[avId]

        self.cleanupInvites(avId)

        return Task.done

    def refreshPublishedGroups(self):
        """Sends all published groups out to the AIs."""
        self.sendUpdate("receiveAllGroups", [self.allGroupStructs])

        # Call the method again later.
        taskMgr.doMethodLater(
            PUBLISHED_GROUP_REFRESH_TIME,
            self.refreshPublishedGroups,
            self.uniqueName(f"refreshPublishedGroups"),
            extraArgs=[],
        )

    """Local events from other managers"""

    def toonOffline(self, avId):
        """Called when an avatar is going offline from the Friends Manager"""
        if avId not in self.toons.keys():
            return

        taskMgr.doMethodLater(
            30,
            self.handleToonOffline,
            self.uniqueName(f"toonOffline-{avId}"),
            extraArgs=[avId],
        )

    """Client to UD requests"""

    def disbandGroup(self):
        avId = self.air.getAvatarIdFromSender()
        self._doDisband(avId, notify=1)

    def _doDisband(self, avId, notify=0, response=Responses.LeaveDisbanded.value):
        group = self.isAvidInGroup(avId)
        if group and group.owner == avId:
            for avatar in group.avatarList:
                notifyKick = notify
                if avatar.avId == group.owner:
                    notifyKick = 1
                self.sendUpdateToAvatarId(
                    avatar.avId, "groupLeaveUdResponse", [response, notifyKick]
                )
                self.cleanupInvites(avatar.avId)

            return self.cleanupGroup(group)
        self.notify.warning(
            f"Avatar {avId} tried to disband a group that didn't exist or they weren't the owner of."
        )

    def kickPlayer(self, targetAvId):
        avId = self.air.getAvatarIdFromSender()
        group = self.isAvidInGroup(avId)
        if group and group.owner == avId and targetAvId in group.avIds:
            group.removeAvatar(targetAvId, noRejoin=True)
            self.sendUpdateToAvatarId(
                targetAvId, "groupLeaveUdResponse", [Responses.LeaveKicked.value, 0]
            )
            return group.sync()

        self.notify.warning(
            f"Avatar {avId} tried to kick a group that didn't exist or they weren't the owner of or "
            f"the user was already kicked."
        )

    def leaveGroup(self):
        avId = self.air.getAvatarIdFromSender()
        group = self.isAvidInGroup(avId)
        if group and avId in group.avIds:
            group.removeAvatar(avId)
            self.sendUpdateToAvatarId(
                avId, "groupLeaveUdResponse", [Responses.ToonLeft.value, 0]
            )
            return group.sync()

        self.notify.warning(f"Avatar {avId} tried to leave a group that didn't exist.")

    def requestGo(self, elevatorId):
        avId = self.air.getAvatarIdFromSender()
        group = self.isAvidInGroup(avId)
        if group and group.owner == avId:
            self.sendUpdate("requestGoUdToAi", [group.toStruct(), elevatorId])
            return
        self.notify.warning(
            f"Avatar {avId} tried to requestGo a group that didn't exist or they weren't the owner of."
        )

    def publishGroup(self, mode: bool):
        """
        Requests to publish a client's group (set public or private).
        """
        avId = self.air.getAvatarIdFromSender()
        group = self.isAvidInGroup(avId)
        # Kill the privacy toggle if the group has announced a group battle
        if group and group.announcedBattle:
            return
        if group and group.owner == avId:
            group.published = mode
            return group.sync()

        self.notify.warning(
            f"Avatar {avId} tried to publish a group they weren't owner of, or wasn't in."
        )

    def getUpdateToonQuery(self):
        """
        The Client has asked for its toon to be updated directly.
        """
        avId = self.air.getAvatarIdFromSender()
        if self.rateLimited(avId):
            return
        self.sendUpdateToAvatarId(avId, "receiveJoinableGroups", [self.publishedGroupStructs])

    def askForGroupInfo(self, groupId):
        """
        A client asks for detailed information about a group.
        """
        avId = self.air.getAvatarIdFromSender()
        if self.rateLimited(avId):
            return

        # Get the group.
        if groupId not in self.groups:
            return
        group = self.groups[groupId]  # type: GroupUD

        # Get their group avatars.
        avatarList = group.avatarList

        # Get a large GroupStruct to send to the client.
        detailAvatarList = [self.toons[avatar.avId].toStruct() for avatar in avatarList]

        # Send this back to the client..
        self.sendUpdateToAvatarId(avId, 'receiveGroupInfo', [group.toStruct(), detailAvatarList])

    """Invite Handling"""

    def invitePlayerUD_getToonData(self, inviterAvId, invitedAvIds, avName, dnaString):
        """
        A player has sent a list of avIds they would like to invite to their group.
        :param inviterAvId:     The fellow responsible for the invite.
        :param invitedAvIds:    A list of avIds.
        :param avName:          The avatar's name.
        :param dnaString:       The inviter's dnaString.
        :return: None.
        """
        if self.rateLimited(inviterAvId):
            return

        # Cache the inviter's name and DNA.
        self.avId2avName[inviterAvId] = avName
        self.avId2DNANetstring[inviterAvId] = dnaString

        # Make sure that they're in a group.
        group = self.isAvidInGroup(inviterAvId)
        if not group:
            return

        # We'll ask all of the AIs if they can check that the list of invited avIds can join the group.
        self.sendUpdate('invitePlayerAI_validateInvited', [group.toStruct(), inviterAvId, invitedAvIds])

    def invitePlayerUD_finalizeInvite(self, inviterAvId: int, invitedAvId: int, invitedName: str, invitedDna):
        """
        The AI has validated that an invited avId can be invited to this group.

        Note that we cannot batch invitedAvId into a list, since this call may be
        happening from several different AI districts.

        :param inviterAvId: The initiator of the invite.
        :param invitedAvId: The target to invite.
        :param invitedName: The target's name.
        :param invitedDna:  The target's DNA string.
        """
        if inviterAvId not in self.avId2DNANetstring or inviterAvId not in self.avId2avName:
            self.notify.warning(
                f"Avatar {inviterAvId}... invited a player way out of order!?"
            )
            return

        group = self.isAvidInGroup(inviterAvId)
        if not group:
            return
        groupCreation = group.groupCreation

        # If the invited avId is in a group, trol them hard
        if self.isAvidInGroup(invitedAvId) or invitedAvId not in self.toons:
            self.sendUpdateToAvatarId(inviterAvId, "receiveNotification", [
                GroupInviteNotification(
                    avId=invitedAvId, name=invitedName, dna=invitedDna,
                    state=GroupInviteNotification.state_failed,
                    response=Responses.AlreadyInGroup,
                ).toStruct()
            ])
            return

        # If the inviter's group is full, troll them hard
        if group.isFull:
            self.sendUpdateToAvatarId(inviterAvId, "receiveNotification", [
                GroupInviteNotification(
                    avId=invitedAvId, name=invitedName, dna=invitedDna,
                    state=GroupInviteNotification.state_failed,
                    response=Responses.GroupFilledUp,
                ).toStruct()
            ])
            return

        inviterDna = self.avId2DNANetstring.get(inviterAvId, '')
        inviterName = self.avId2avName.get(inviterAvId, '')

        # Send the folks notifications.
        self.sendUpdateToAvatarId(invitedAvId, "receiveNotification", [
            GroupInviteNotification(
                inviterAvId, inviterName, inviterDna,
                GroupInviteNotification.state_received,
                groupCreation.groupType, 0, group.zoneId,
                *groupCreation.groupOptions
            ).toStruct()
        ])
        self.sendUpdateToAvatarId(inviterAvId, "receiveNotification", [
            GroupInviteNotification(
                avId=invitedAvId, name=invitedName, dna=invitedDna,
                state=GroupInviteNotification.state_sent,
            ).toStruct()
        ])

        # Cache this invite.
        if inviterAvId not in self.avIdInvites:
            self.avIdInvites[inviterAvId] = set()
        self.avIdInvites[inviterAvId].add(invitedAvId)

        # Attempt to force invite them if we're the owner.
        inviterGroup = self.isAvidInGroup(inviterAvId)
        if inviterAvId == inviterGroup.owner:
            self.addPlayerToGroup(inviterAvId, invitedAvId, True)

    def invitePlayerQueryResponse(self, inviterAvId, response):
        # Make sure this response is valid.
        invitedAvId = self.air.getAvatarIdFromSender()
        if not self.invitePlayerCancel(inviterAvId=inviterAvId) and response:
            # The invite no longer exists.
            self.sendUpdateToAvatarId(invitedAvId, "receiveNotification", [
                GroupCallbackNotification(
                    errorType=Responses.CannotJoinGroup, errorCode=Responses.InviteExpired,
                ).toStruct()
            ])
            self.unreservePlayer(invitedAvId, mustHaveAvId=inviterAvId)
            return

        # OK, now handle the response
        if not response:
            # they said no. cry about it
            self.sendUpdateToAvatarId(inviterAvId, 'receiveGroupRejection', [invitedAvId])
            self.unreservePlayer(invitedAvId, mustHaveAvId=inviterAvId)
        else:
            self.addPlayerToGroup(inviterAvId, invitedAvId, False)

    def invitePlayerCancel(self, invitedAvId=None, inviterAvId=None):
        """
        Cancels a Group invite between two Toons.
        :param invitedAvId: The invited avId (sent in from a sendUpdate or locally)
        :param inviterAvId: The inviter's avId.
        """
        if invitedAvId is None:
            invitedAvId = self.air.getAvatarIdFromSender()
        if inviterAvId is None:
            inviterAvId = self.air.getAvatarIdFromSender()
        if invitedAvId not in self.avIdInvites.get(inviterAvId, []):
            return False
        self.avIdInvites[inviterAvId].remove(invitedAvId)
        self.cleanupInvites(inviterAvId, requireEmpty=True)
        self.unreservePlayer(invitedAvId, mustHaveAvId=inviterAvId)
        return True

    def cleanupInvites(self, inviterAvId, requireEmpty=False):
        """Cleans up any outbound invites regarding an avId."""
        if inviterAvId in self.avIdInvites:
            if requireEmpty and self.avIdInvites[inviterAvId]:
                return
            del self.avIdInvites[inviterAvId]

    """AI to UD Updates"""

    def avatarChangedZoneUd(self, toon, oldZoneId):
        # if we got this message, they're obviously still online, clear out these tasks.
        avId, *_ = toon
        toon = GroupAvatarUDToon.fromStruct(toon)
        taskMgr.remove(self.uniqueName(f"toonOffline-{avId}"))
        self.toons[avId] = toon

        # If this Toon is in a group and they are the owner,
        # we will need to validate their zone ID.
        group = self.isAvidInGroup(avId)
        if group and group.owner == avId:
            # OK, they're the owner. Is the zone ID ok?
            zoneId = toon.zoneId

            # Zone ID 1 is a default ID when toons are loading in
            # Their proper zone ID will be filled in soon after.
            fullHoodOkay = group.groupDef.allowFullHood and (zoneId == 1 or getHoodId(zoneId) == group.groupDef.zoneId[0])
            # If they spanned a full hood, disband.
            if getHoodId(zoneId) != getHoodId(oldZoneId) and not fullHoodOkay:
                return self._doDisband(avId)

            if not group.groupDef.forceZoneConstant:
                # The allowed zones can span the definition's zoneId list.
                if zoneId in group.groupDef.zoneId or fullHoodOkay:
                    # The zone ID is okay. Poggers.
                    pass
                else:
                    # The zone ID is not okay. Force disband the group.
                    self._doDisband(avId)
            else:
                # The allowed zone MUST be the group's initial creation zone.
                if zoneId != group.groupDef.zoneId:
                    # The zone ID is not okay. Force disband the group.
                    self._doDisband(avId)

    def createGroupUd(self, avId, group, districtId, published):
        groupCreation = GroupCreation.fromStruct(group)
        group = self.isAvidInGroup(avId)
        if group:
            # Only return if we are not invited.
            if not group.getGroupAvatar(avId).reserved:
                return

        groupLeader: GroupAvatarUDToon = self.toons.get(avId)

        # these can be None if UD gets reset
        if not groupLeader:
            return
        if groupLeader.name is None:
            return
        if groupLeader.zoneId is None:
            return

        # Clear any reservations we have.
        self.unreservePlayer(avId)

        group = GroupUD(
            groupId=self.groupIdAllocator.allocate(),
            groupCreation=groupCreation,
            districtId=districtId,
            avatarList=[groupLeader.transformIntoGroupAv(status=0, reserved=False)],
            published=published,
            zoneId=groupLeader.zoneId,
            kickedAvIds=[],
        )
        group.init_ud()
        self.groups[group.groupId] = group

        group.sync()

        # Send join notif. Required to communicate content sync.
        groupOption = groupCreation.getOptionIndex(0)
        if groupOption is None:
            groupOption = 0
        self.sendUpdateToAvatarId(avId, "receiveNotification", [
            GroupCallbackNotification(
                avId=avId, name='',
                errorCode=Responses.ToonJoined, errorType=Responses.OK,
                groupType=groupCreation.getGroupType(), oneGroupOption=groupOption,
            ).toStruct()
        ])

    def updateGroupSettingsUd(self, avId, groupOptions: list):
        """
        Update the group given a settings list.
        """
        group = self.isAvidInGroup(avId)
        if not group:
            return

        # Must only be updated by group owner.
        if avId != group.owner:
            return

        # First, let's go through the group's defined settings.
        groupType = group.groupType

        # It has to be an actual defined group, for one.
        if groupType not in BoardingGroupInformation:
            return

        # OK, we passed all the checks, and can update this group.
        group.updateOptions(groupOptions)

    def disbandGroupAiToUd(self, groupId):
        group = self.groups.get(groupId)
        if group:
            for avId in group.avIds:
                self.sendUpdateToAvatarId(
                    avId, "groupLeaveUdResponse", [Responses.LeaveDisbanded.value, 0]
                )
            return self.cleanupGroup(group)
        self.notify.warning(
            f"AI operated on Group {groupId}: tried to disband a group that didn't exist."
        )

    def addPlayerToGroup(self, fromAvId, targetAvId, mustReserve):
        group = self.isAvidInGroup(fromAvId)
        if not group:
            return
        if targetAvId in group.avIds:
            groupAvatar = group.getGroupAvatar(targetAvId)
            if not groupAvatar.reserved:
                return  # they are legitimately in a group already
            elif mustReserve:
                return  # they're already reserved for another group, don't reserve them for this one.

        if targetAvId in self.toons:
            group.addAvatar(self.toons[targetAvId], mustReserve)

    def unreservePlayer(self, targetAvId, mustHaveAvId=None):
        """The AI asked us to unreserve a player."""
        group: GroupUD = self.isAvidInGroup(targetAvId)
        if mustHaveAvId:
            group_b = self.isAvidInGroup(mustHaveAvId)
            if group is not group_b:
                return
        if group:
            groupAvatar = group.getGroupAvatar(targetAvId)
            if groupAvatar.reserved:
                group.removeAvatar(targetAvId)

    def requestGroupUd(self, avId, targetAvId):
        """
        At this point, this avId has passed all checks
        to be able to join this group on the AI.
        """
        def sendResponse(responseEnum, groupType=0):
            return self.sendUpdateToAvatarId(avId, "requestGroupCallback", [responseEnum.value, Responses.CannotJoinGroup.value, groupType])

        # DEFINITELY make sure they aren't in a group at this point.
        group = self.isAvidInGroup(avId)
        if group:
            return sendResponse(Responses.AlreadyInGroup)

        # Make sure the owner's group exists.
        targetGroup: GroupUD = self.isAvidInGroup(targetAvId)
        if not targetGroup:
            return sendResponse(Responses.GroupNonexistent)

        # Make sure the group is published. (Hopefully it is..)
        if not targetGroup.published:
            return sendResponse(Responses.GroupNotPublic)

        # Make sure the avatar wasn't already kicked.
        if targetGroup.avatarKicked(avId):
            return sendResponse(Responses.KickedFromGroup)

        # Make sure there is room in the group.
        if targetGroup.isFull:
            return sendResponse(Responses.GroupFilledUp)

        # Hey, we do have data on this toon, right?
        if avId not in self.toons:
            return

        # OK, we can definitely join the group now!
        targetGroup.addAvatar(self.toons[avId], False)

    def announceGroupMemberEncounteredSuitUd(self, avId):
        # Group member encountered cog they care about, need to let the rest of the group know.
        toonGroup = self.isAvidInGroup(avId)
        if toonGroup and not toonGroup.announcedBattle:
            toonGroup.announcedBattle = True
            toonGroup.avatarThatEncountered = avId
            # Mark it as private so that new people can't join after the cog is encountered
            toonGroup.published = False
            toonGroup.sync()

            # Tell all client avatars in group, except the person who triggered it, that this happened.
            for groupMemberId in [toon.avId for toon in toonGroup.avatarList if toon.avId != avId]:
                self.sendUpdateToAvatarId(groupMemberId, "postGroupMemberEncounteredSuit", [avId])
            # Now clear out all invited players for all group members
            for groupMemberId in [toon.avId for toon in toonGroup.avatarList]:
                groupAvatar = toonGroup.getGroupAvatar(groupMemberId)
                if groupAvatar.reserved:
                    toonGroup.removeAvatar(groupMemberId)
                else:
                    self.cleanupInvites(groupMemberId)

    def requestTeleportToGroupBattleUD(self, avId):
        toonGroup = self.isAvidInGroup(avId)
        if not toonGroup:
            return
        if not toonGroup.announcedBattle:
            return
        if toonGroup.avatarThatEncountered in (0, avId):
            # Don't want to teleport to ourselves, or a nonexistant avatar
            return
        if toonGroup.avatarThatEncountered not in [toon.avId for toon in toonGroup.avatarList]:
            return

        requestedAvatar: GroupAvatarUDToon = self.toons.get(toonGroup.avatarThatEncountered)
        if not requestedAvatar:
            return
        if not requestedAvatar.zoneId:
            return
        if not requestedAvatar.districtId:
            return

        # At this point, everything seems good and we can go ahead and send this back to the client
        requestedToonId = requestedAvatar.avId
        zoneId = requestedAvatar.zoneId
        shardId = requestedAvatar.districtId
        self.sendUpdateToAvatarId(avId, 'postClientTeleportToGroupBattle', [requestedToonId, zoneId, shardId])

    """AI to UD requests"""

    def disbandToonGroup(self, avId: int, notify=0, response=Responses.LeaveDisbanded.value):
        """
        Disbands a group that this toon is in.
        This is sent exclusively from the AI.
        """
        # We need to find the owner of this group.
        group = self.isAvidInGroup(avId)
        if group:
            self._doDisband(group.owner, notify, response)

    """Helpers"""

    def isAvidInGroup(self, avId: int) -> Optional[GroupUD]:
        group: GroupUD
        for group in self.groups.values():
            if avId in group.avIds:
                return group
        return None

    """Rate Limiting"""

    def rateLimited(self, avId):
        if avId not in self.avIdRateLimiter:
            self.avIdRateLimiter[avId] = RateLimiter(max_hits=UD_RATELIMITER_MAX_HITS, period=UD_RATELIMITER_PERIOD)
        rateLimiter = self.avIdRateLimiter[avId]
        return rateLimiter.tryRequest()

    @property
    def allGroupStructs(self):
        return [group.toStruct() for group in self.groups.values()]

    @property
    def publishedGroupStructs(self):
        return [group.toStruct() for group in self.groups.values() if group.published]
