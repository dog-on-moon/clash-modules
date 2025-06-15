from typing import TYPE_CHECKING

from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal

from toontown.chat.constants import ChatEvents, ChatGlobals
from toontown.chat.enums.ChatChannel import ChatChannel
from toontown.chat.enums.ChatContentType import ChatContentType
from toontown.chat.enums.ChatNpcPreset import ChatNpcPreset
from toontown.groups import GroupGlobals
from toontown.groups.GroupClasses import GroupClient, GroupCreation, GroupAvatarUDToon
from toontown.groups.GroupEnums import GroupType
from toontown.groups.GroupGlobals import Responses
from toontown.gui.game.condition import ConditionGlobals
from toontown.notifications.NotificationEnums import NotificationType
from toontown.notifications.notificationData.GenericTextNotification import GenericTextNotification, GenericTextId
from toontown.notifications.notificationData.GroupCallbackNotification import GroupCallbackNotification
from toontown.notifications.notificationData.GroupInviteNotification import GroupInviteNotification
from toontown.notifications.notificationData.NotificationData import NotificationData
from toontown.toonbase import TTLocalizer
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory

if TYPE_CHECKING:
    from toontown.utils.BuiltinHelper import *


@DirectNotifyCategory()
class DistributedGroupManager(DistributedObjectGlobal):
    neverDisable = 1

    """
    Global Object Methods
    """

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)
        self.group = None
        self.joinableGroups = ()
        self.inviteePanel = None
        self.queuedAvIdInvites = []
        self.detailAvatarList: list[GroupAvatarUDToon] = []
        self.accept('groups-refresh', self.requestJoinableGroups)
        self.accept('respondToGroupInvite', self.respondToGroupInvite)
        self.accept('clientLogout', self.cleanupGroupState)

    def delete(self):
        DistributedObjectGlobal.delete(self)
        self.cr.groupManager = None

    def disable(self):
        self.notify.debug("Disabling GroupManager.")
        DistributedObjectGlobal.disable(self)

    def generate(self):
        self.notify.debug("Generated")
        DistributedObjectGlobal.generate(self)

    def cleanupGroupState(self):
        self.group = None

    """
    Requests to the AI from the client
    """

    def createGroup(self, groupCreation: GroupCreation, invitedAvIds: list, published: bool, force: bool = True):
        """
        Creates a group, given several parameters.
        """
        # Make sure we're not doing something illegal.
        if self.group:
            return

        # Queue avIds, send our group creation request.
        self.queuedAvIdInvites = invitedAvIds
        self.sendUpdate("createGroup", [groupCreation.toStruct(), published, force])

    def updateGroupSettings(self, groupSettings: list):
        """
        Update the group given a settings list.
        AI will do the sanity checking.
        """
        self.sendUpdate("updateGroupSettings", groupSettings)

    def disbandGroup(self):
        self.sendUpdate("disbandGroup", [])

    def leaveGroup(self):
        self.sendUpdate("leaveGroup", [])

    def kickPlayer(self, avId):
        self.sendUpdate("kickPlayer", [avId])

    def invitePlayer(self, invitedAvIds: list):
        if self.group and self.group.announcedBattle:
            base.localAvatar.addNotification(GenericTextNotification(
                textId=GenericTextId.GroupDeniedInvite,
                title=TTLocalizer.GroupDenyBattleActive,
                subtitle=TTLocalizer.GroupDenyBattleActiveInvite,
            ))
            return
        self.sendUpdate("invitePlayerAI_getDna", [invitedAvIds])

    def publishGroup(self, mode: bool):
        if self.group and self.group.announcedBattle:
            base.localAvatar.addNotification(GenericTextNotification(
                textId=GenericTextId.GroupDeniedPrivacyChange,
                title=TTLocalizer.GroupDenyBattleActive,
                subtitle=TTLocalizer.GroupDenyBattleActivePrivacy,
            ))
            return
        self.sendUpdate("publishGroup", [mode])

    def requestGo(self):
        if not self.group:
            return False

        # todo - use more specific filtering based on
        #  group type, group options, etc
        elevator = next(
            filter(
                lambda x: x.__class__ == self.group.elevatorClass,
                base.cr.doId2do.values(),
            )
        )

        if not elevator:
            # make sure that we have a proper destination.
            return False

        for avId in self.group.avIds:
            # make sure all avatars are in the area.
            av = self.cr.getDo(avId)
            if not av or av.isDisabled():
                return False

        if any([self.group.isAvIdReserved(checkAvId) for checkAvId in self.group.avIds]):
            # make sure that no avatar is "reserved".
            return False

        self.sendUpdate("requestGo", [elevator.doId])
        return True

    def respondToGroupInvite(self, avId, status):
        self.sendUpdate("invitePlayerQueryResponse", [avId, status])

    def receiveGroupRejection(self, inviteeAvId):
        base.localAvatar.addNotification(
            GroupInviteNotification(
                avId=inviteeAvId, state=GroupInviteNotification.state_denied,
            )
        )

    def requestGroup(self, targetAvId, force=False):
        """
        Requests to join an AvId's target group.
        This will only succeed if their group is public,
        and the target is the group owner.

        Also, we will have to pass all the sanity checks.
        These will be generally different per group, and
        is all handled on the AI front.
        """
        self.sendUpdate("requestGroup", [targetAvId, force])

    def askForGroupInfo(self, group: GroupClient):
        """
        Asks the AI for info about a group.
        """
        self.sendUpdate('askForGroupInfo', [group.groupId])

    def mod_forceDisband(self, group: GroupClient):
        """
        Allows a moderator to send over to the AI a request to force disband a group.
        """
        if GroupGlobals.hasForceDisbandPermission(base.localAvatar):
            self.sendUpdate('mod_forceDisband', [group.avatarList[0].avId])

    """
    Updates from the AI sent to the client
    """

    def invitePlayerQuery(self, fromAvId, toAvId, name, dna, group):
        groupCreation = GroupCreation.fromStruct(group)
        if toAvId == -1 and fromAvId == -1:
            # Both being -1 is key for 'the person we invited is in a group already'.
            base.localAvatar.addNotification(
                GroupInviteNotification(
                    toAvId, name, dna,
                    GroupInviteNotification.state_failed,
                    groupCreation.groupType, Responses.AlreadyInGroup, 0,
                    *groupCreation.groupOptions
                )
            )
            return
        elif fromAvId == base.localAvatar.getDoId():
            # We sent an invite, acknowledge by server.
            base.localAvatar.addNotification(
                GroupInviteNotification(
                    toAvId, name, dna,
                    GroupInviteNotification.state_sent,
                    groupCreation.groupType, Responses.AlreadyInGroup, 0,
                    *groupCreation.groupOptions
                )
            )
        elif toAvId == base.localAvatar.getDoId():
            base.localAvatar.addNotification(
                GroupInviteNotification(
                    toAvId, name, dna,
                    GroupInviteNotification.state_received,
                    groupCreation.groupType, Responses.AlreadyInGroup, 0,
                    *groupCreation.groupOptions
                )
            )

    def cancelInvite(self, invitedAvId: int):
        self.sendUpdate('invitePlayerCancel', [invitedAvId])

    def requestGoClientLocks(self):
        pass  # TODO: lock clients in place.

    def requestTeleportToGroupBattle(self):
        if base.localAvatar.doId == self.group.avatarThatEncountered:
            # Can't teleport to ourselves
            return False
        place = base.localAvatar.getPlace()
        if not place:
            return False

        if base.localAvatar.isTeleportAllowed() and place.getState() in ('Walk', 'StickerBook'):
            self.sendUpdate('requestTeleportToGroupBattleAI')

    def postClientTeleportToGroupBattle(self, avId, zoneId, shardId):
        place = base.localAvatar.getPlace()
        if not place:
            return
        if place.getState() not in ('walk', 'stickerBook'):
            return
        if not self.group:
            return

        if base.localAvatar.isTeleportAllowed():
            messenger.send('gotoAvatar', [self.group.avatarThatEncountered,
                                          self.group.getGroupAvatar(self.group.avatarThatEncountered).getName(),
                                          f'foo123placeholderFake-{self.group.avatarThatEncountered}'])

    def receiveJoinableGroups(self, joinableGroups):
        """
        This Client receives all of the possible groups that it may join.
        """
        self.joinableGroups = GroupClient.fromStructList(joinableGroups)
        messenger.send('group-manager-update')

    def getJoinableGroups(self):
        # validate all of the districts are still available
        existingGroups = []
        existingDistrictIds = [x[0] for x in base.cr.listActiveShards()]
        for group in self.joinableGroups:
            if group.districtId in existingDistrictIds:
                existingGroups.append(group)
        return existingGroups

    def requestJoinableGroups(self):
        self.sendUpdate('getUpdateToonQuery')

    def requestGroupCallback(self, errorCode: int, errorType: int, groupType: int):
        """
        Receives an error code.
        """
        # If we tried to make a group and got that we couldn't,
        # we will unqueue all of the avIds we tried to invite.
        errorType = Responses(errorType)
        errorCode = Responses(errorCode)

        kwargs = {'errorCode': errorCode, 'errorType': errorType}
        if groupType != 0:
            kwargs['groupType'] = GroupType(groupType)

        if errorType == Responses.CannotMakeGroup:
            self.queuedAvIdInvites = []
            if errorCode in TTLocalizer.GroupCreateFailure:
                base.localAvatar.addNotification(GroupCallbackNotification(**kwargs))
        if errorType == Responses.CannotJoinGroup:
            if errorCode in TTLocalizer.GroupJoinFailure:
                base.localAvatar.addNotification(GroupCallbackNotification(**kwargs))
        messenger.send('groupCallbackFailure', [errorCode, errorType])

    def receiveGroupInfo(self, group: list, detailAvatarList: list):
        """
        Extended information about a group.
        """
        self.detailAvatarList = GroupAvatarUDToon.fromStructList(detailAvatarList)
        messenger.send(ConditionGlobals.RefreshMsg)
        messenger.send('receiveGroupInfo', [GroupClient.fromStruct(group), self.detailAvatarList[:]])

    def receiveNotification(self, notificationData: NotificationData):
        base.localAvatar.addNotification(NotificationData.fromStruct(notificationData))

    def getDetailAvatarList(self) -> list[GroupAvatarUDToon]:
        return self.detailAvatarList

    """
    Updates from the UD sent to the client
    """

    def groupManagerReloaded_CL(self):
        """The group manager has reloaded, force cleanup on group if necessary."""
        # Clear any of our group-related notifs.
        base.localAvatar.removeNotificationsOfType(
            [NotificationType.GroupInvite, NotificationType.GroupCallback]
        )

        # Force leave our group.
        if self.group:
            self.groupLeaveUdResponse(GroupGlobals.Responses.ManagerRestart)
            messenger.send('groupSystemCrashed')

    def groupLeaveUdResponse(self, response, flag: bool = False):
        if not hasattr(base, 'localAvatar'):
            # Yes, this can get called before localAvatar exists...
            # Classic networking bugs
            return
        if not self.group:
            # On quick disconnects-come backs, UD might like to tell us
            # we've disbanded from a group that we don't even know yet!
            return
        response = GroupGlobals.Responses(response)
        owner = self.group.owner
        self.group = None

        messenger.send(ChatEvents.Groups_LocalToon_Left)
        messenger.send("groupLeaveResponse", [response])
        messenger.send("forceTAPGroupRefresh")
        messenger.send(ConditionGlobals.RefreshMsg)
        if response == GroupGlobals.Responses.LeaveDisbanded:
            if flag:
                base.localAvatar.addNotification(
                    GroupCallbackNotification(
                        errorCode=Responses.GroupDisbanded, errorType=Responses.OK,
                    )
                )
        elif response == GroupGlobals.Responses.LeaveKicked:
            base.localAvatar.addNotification(
                GroupCallbackNotification(
                    errorCode=Responses.LeaveKicked, errorType=Responses.OK,
                )
            )
        elif response == GroupGlobals.Responses.ManagerRestart:
            base.localAvatar.addNotification(
                GroupCallbackNotification(
                    errorCode=Responses.ManagerRestart, errorType=Responses.OK,
                )
            )
        elif response == GroupGlobals.Responses.DistrictDraining:
            base.localAvatar.addNotification(
                GroupCallbackNotification(
                    errorCode=Responses.DistrictDraining, errorType=Responses.OK,
                )
            )
        elif response == GroupGlobals.Responses.DistrictFullPizzeria:
            base.localAvatar.addNotification(
                GroupCallbackNotification(
                    errorCode=Responses.DistrictFullPizzeria, errorType=Responses.DistrictFullPizzeria,
                )
            )
        elif response == GroupGlobals.Responses.ModeratorDisband:
            base.localAvatar.addNotification(
                GroupCallbackNotification(
                    errorCode=Responses.ModeratorDisband, errorType=Responses.OK,
                )
            )

    def updateGroup(self, groupStruct):
        """
        Receives a group update after it has synced.
        """
        group = GroupClient.fromStruct(groupStruct)

        # If we are in the group, but reserved, don't show us!
        if base.localAvatar.doId in group.avIds:
            if group.isAvIdReserved(base.localAvatar.doId):
                # we're only RESERVED in this group, not actually in it,
                # so we don't wanna think that we are in it.
                return

        # Invite every avId we've queued to this group.
        if self.group is None and self.queuedAvIdInvites:
            self.invitePlayer(self.queuedAvIdInvites)
            self.queuedAvIdInvites = []

        # Set our group status.
        newGroup = self.group is None
        self.group = group
        if newGroup:
            messenger.send(ChatEvents.Groups_LocalToon_Joined)
            messenger.send('joinedNewGroup', [group])
        messenger.send('groupUpdate', [group])
        messenger.send("forceTAPGroupRefresh")
        messenger.send(ConditionGlobals.RefreshMsg)

        # Do debug.
        self.notify.debug(group)

    def postGroupMemberEncounteredSuit(self, avId):
        # UD has decided to tell us locally that a group member encountered a cog we care about.
        # We're given the avId of the member who encountered them so that we can display it to the client.
        if self.group is None:
            return
        if not self.group.groupDefinition.suitName:
            return
        if avId not in [toon.avId for toon in self.group.avatarList]:
            return
        toonThatEncountered = None
        for toon in self.group.avatarList:
            if toon.avId == avId:
                toonThatEncountered = toon
                break
        if not toonThatEncountered:
            return

        messageText = f'{toonThatEncountered.name} has encountered {TTLocalizer.suitName(self.group.groupDefinition.suitName)}! You may now teleport to the battle from the Actions menu.'
        self.cr.chatManager.receiveChatMessage(channelId=ChatChannel.Groups, modifier=ChatNpcPreset.Toon,
                                               contentTypeId=ChatContentType.Text, content=messageText,
                                               senderId=ChatGlobals.Sender_NoId, senderName='')

    @property
    def isLocalOwner(self):
        return self.group.owner == base.localAvatar.getDoId()
