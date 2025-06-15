import time

from toontown.gui.toon.ToonHeadData import ToonHeadData
from toontown.hood import ZoneUtil
from toontown.hood.ZoneUtil import zoneIdToName
from toontown.utils.AstronStruct import AstronStruct
from toontown.groups.GroupGlobals import *
from typing import List

"""
Lower-level Astron structs
"""
# region GroupAvatar, GroupAvatarUDToon, GroupCreation


class GroupAvatar(AstronStruct):
    """
    Information about an avatar in a group.
    """

    def __init__(self, avId: int, name: str, status: int, reserved: bool):
        self.avId = avId
        self.name = name
        self.status = status
        self.reserved = reserved

    def getName(self):
        return self.name

    @property
    def doId(self):
        return self.avId

    def toStruct(self) -> list:
        return [self.avId, self.name, self.status, self.reserved]


class GroupAvatarUDToon(AstronStruct):
    """
    UD-facing information for a Group Avatar.
    """

    def __init__(self, avId: int, name: str, zoneId: int, districtId: int,
                 hp: int, gagLevels: list, gagPrestiges: list,
                 toonLevel: int, toonHeadData: ToonHeadData,
                 currHp: int, xp: int):
        self.avId = avId
        self.name = name
        self.zoneId = zoneId
        self.districtId = districtId
        self.hp = hp
        self.gagLevels = gagLevels
        self.gagPrestiges = gagPrestiges
        self.toonLevel = toonLevel
        self.toonHeadData = toonHeadData
        self.currHp = currHp
        self.xp = xp

    def toStruct(self) -> list:
        return [self.avId, self.name, self.zoneId, self.districtId, self.hp, self.gagLevels, self.gagPrestiges,
                self.toonLevel, self.toonHeadData.toStruct(), self.currHp, self.xp]

    @classmethod
    def fromStruct(cls, struct):
        avId, name, zoneId, districtId, hp, gagLevels, gagPrestiges, toonLevel, toonHeadData, currHp, xp = struct
        toonHeadData = ToonHeadData.fromStruct(toonHeadData)
        return cls(avId, name, zoneId, districtId, hp, gagLevels, gagPrestiges, toonLevel, toonHeadData, currHp, xp)

    def transformIntoGroupAv(self, status: int = 0, reserved: bool = False):
        return GroupAvatar(avId=self.avId, name=self.name, status=status, reserved=reserved)

    def getHp(self):
        return self.hp


class GroupCreation(AstronStruct):
    """
    Information transferred to creation a group.
    """

    def __init__(self, groupType: GroupType, groupOptions: list, groupSize: int):
        self.groupType = groupType
        self.groupOptions = groupOptions
        self.groupSize = groupSize

    def toStruct(self) -> list:
        return [self.groupType.value, self.groupOptions, self.groupSize]

    @classmethod
    def fromStruct(cls, struct: list):
        groupType, groupOptions, groupSize = struct
        groupType = GroupType(groupType)
        return cls(groupType, groupOptions, groupSize)

    def getOptionIndex(self, index: int):
        if 0 <= index < len(self.groupOptions):
            return self.groupOptions[index]
        return None

    def getGroupType(self) -> GroupType:
        return self.groupType

    def getOptions(self):
        return self.groupOptions

# endregion


"""
Group Astron Structs
"""
# region


class GroupBase(AstronStruct):
    """
    The base class representing a Group.
    """

    def __init__(self, groupId: int, groupCreation: GroupCreation, districtId: int,
                 avatarList: list, published: bool, zoneId: int, kickedAvIds: list, announcedBattle: bool = False,
                 avatarThatEncountered: int = 0):
        self.groupId = groupId
        self.groupCreation = groupCreation
        self.districtId = districtId
        self.avatarList = avatarList
        self.published = published
        self.zoneId = zoneId
        self.kickedAvIds = kickedAvIds
        self.announcedBattle = announcedBattle
        self.avatarThatEncountered = avatarThatEncountered

    def toStruct(self) -> list:
        return [self.groupId, self.groupCreation.toStruct(), self.districtId,
                AstronStruct.toStructList(self.avatarList), self.published, self.zoneId,
                self.kickedAvIds, self.announcedBattle, self.avatarThatEncountered]

    @classmethod
    def fromStruct(cls, struct: list):
        groupId, groupCreation, districtId, avatarList, published, zoneId, kickedAvIds, announcedBattle, avatarThatEncountered = struct
        groupCreation = GroupCreation.fromStruct(groupCreation)
        avatarList = GroupAvatar.fromStructList(avatarList)
        return cls(groupId, groupCreation, districtId, avatarList, published, zoneId, kickedAvIds, announcedBattle, avatarThatEncountered)

    """
    Group Data
    """

    def __eq__(self, other):
        if other is None:
            return False
        assert isinstance(other, GroupBase)
        return self.groupId == other.groupId

    def getIdsOfGroupMembers(self, includeReserved: bool = True) -> List[int]:
        """
        Returns the doId of the group members.

        :return: A list containing the doId of all the group members.
        """
        if includeReserved:
            return [x.avId for x in self.avatarList]
        else:
            return [x.avId for x in self.avatarList if not x.reserved]

    def getGroupAvatar(self, avId):
        return next(filter(lambda x: x.avId == avId, self.avatarList), None)

    def isAvIdReserved(self, avId):
        groupAvatar: GroupAvatar = self.getGroupAvatar(avId)
        if groupAvatar is None:
            return False
        return groupAvatar.reserved

    def getGroupId(self):
        return self.groupId

    def getGroupCreation(self) -> GroupCreation:
        return self.groupCreation

    def avatarKicked(self, avId):
        return avId in self.kickedAvIds

    def validateZoneId(self, zoneId):
        """Is this zoneId valid?"""
        return (zoneId in self.groupDefinition.zoneId) or (self.groupDefinition.allowFullHood and ZoneUtil.getHoodId(zoneId) == ZoneUtil.getHoodId(self.groupDefinition.zoneId[0]))

    @property
    def groupDefinition(self) -> GroupDefinition:
        return BoardingGroupInformation.get(self.groupType)

    @property
    def owner(self):
        if not self.avatarList:
            return 0
        return self.avatarList[0].avId

    @property
    def ownerName(self):
        if not self.avatarList:
            return 'Toon'
        return self.avatarList[0].name

    @property
    def avIds(self):
        return [avatarList.avId for avatarList in self.avatarList]

    @property
    def isFull(self):
        return len(self.avatarList) >= self.groupSize

    @property
    def groupType(self):
        return self.groupCreation.groupType

    @property
    def groupSize(self):
        return self.groupCreation.groupSize

    @property
    def groupOptions(self):
        return self.groupCreation.groupOptions


class GroupClient(GroupBase):
    """
    The client class for the Group.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.joinMode = 0

    def setJoinMode(self, mode):
        self.joinMode = mode

    def getJoinMode(self):
        return self.joinMode

    def getName(self) -> str:
        """Turns this GroupStruct into an extended name."""
        return groupStruct2Name(self)

    def localAvIsOwner(self) -> bool:
        if not base.localAvatar:
            return False
        return self.owner == base.localAvatar.getDoId()

    def getAgreedNonLocalAvids(self) -> set[int]:
        """Gets all non-local avIds who aren't in invite state."""
        return {
            avId for avId in self.avIds
            if not self.isAvIdReserved(avId)
            and avId != base.localAvatar.getDoId()
        }

    @property
    def alive(self):
        return bool(self.avatarList)

    @property
    def location(self):
        locationZoneId = ZoneUtil.getHoodId(self.zoneId) if self.groupDefinition.allowFullHood else self.zoneId
        if locationZoneId in TTLocalizer.GroupShortLocationNames:
            return TTLocalizer.GroupShortLocationNames[locationZoneId]
        return zoneIdToName(locationZoneId)[1]

    @property
    def shardName(self):
        avalibleShards = base.cr.listActiveShards()
        for shard in avalibleShards:
            shardId, shardName, *_ = shard
            if shardId == self.districtId:
                return shardName
        return "District Closed"

    @property
    def elevatorClass(self):
        groupDef = getGroupDef(self.groupType)
        groupElev = groupDef.getElevator()
        if groupElev is None:
            return None
        return groupElev.elevatorClass

    @property
    def hasElevator(self) -> bool:
        groupDef = getGroupDef(self.groupType)
        groupElev = groupDef.getElevator()
        if groupElev is None:
            return False
        else:
            return groupElev.warpable


class GroupAI(GroupBase):
    """
    The AI class for the Group.
    """

    @property
    def elevatorClass(self):
        groupDef = getGroupDef(self.groupType)
        groupElev = groupDef.getElevator()
        if groupElev is None:
            return None
        return groupElev.elevatorClassAI


class GroupUD(GroupBase):
    """
    The UD class for the Group.
    """

    def init_ud(self):
        self.createdAt = int(time.time())
        self.mgr = simbase.air.groupManager
        if self.groupType not in BoardingGroupInformation:
            self.mgr.notify.warning(f"Avatar {self.owner} managed to make a Group with an invalid type. Potentially dangerous!")
            self.groupCreation.groupType = GroupType(DEFAULT_GROUP)  # gag training
        self.groupDef: GroupDefinition = getGroupDef(self.groupType)

    def addAvatar(self, toon: GroupAvatarUDToon, mustReserve):
        if self.isFull:
            return

        from toontown.notifications.notificationData.GroupCallbackNotification import GroupCallbackNotification
        if toon.avId in self.avIds:
            groupAvatar = self.getGroupAvatar(toon.avId)
            if groupAvatar.reserved:
                # update their reserve status to mustReserve.
                groupAvatar.reserved = mustReserve
                self.sync()

                # Send join notif. Required to communicate content sync.
                groupOption = self.groupCreation.getOptionIndex(0)
                if groupOption is None:
                    groupOption = 0
                self.mgr.sendUpdateToAvatarId(toon.avId, "receiveNotification", [
                    GroupCallbackNotification(
                        avId=toon.avId, name=toon.name,
                        errorCode=Responses.ToonJoined, errorType=Responses.OK,
                        groupType=self.groupCreation.getGroupType(), oneGroupOption=groupOption,
                    ).toStruct()
                ])
                return
            else:
                # this avatar was not reserved, don't add them.
                return

        # Tell the folks in the group about this new avatar.
        if not mustReserve:
            for av in self.avatarList:
                av: GroupAvatar
                if av.reserved:
                    continue
                groupOption = self.groupCreation.getOptionIndex(0)
                if groupOption is None:
                    groupOption = 0
                self.mgr.sendUpdateToAvatarId(av.avId, "receiveNotification", [
                    GroupCallbackNotification(
                        avId=toon.avId, name=toon.name,
                        errorCode=Responses.ToonJoined, errorType=Responses.OK,
                        groupType=self.groupType, oneGroupOption=groupOption,
                    ).toStruct()
                ])

        # and then add them!
        self.avatarList.append(GroupAvatar(toon.avId, toon.name, False, mustReserve))

        # Send join notif. Required to communicate content sync.
        if not mustReserve:
            groupOption = self.groupCreation.getOptionIndex(0)
            if groupOption is None:
                groupOption = 0
            self.mgr.sendUpdateToAvatarId(toon.avId, "receiveNotification", [
                GroupCallbackNotification(
                    avId=toon.avId, name=toon.name,
                    errorCode=Responses.ToonJoined, errorType=Responses.OK,
                    groupType=self.groupCreation.getGroupType(), oneGroupOption=groupOption,
                ).toStruct()
            ])

        # We got back in nicely as well, so we can remove
        # ourselves from the kickedAvIds list.
        if toon.avId in self.kickedAvIds:
            self.kickedAvIds.remove(toon.avId)

        self.sync()

    def removeAvatar(self, avId, noRejoin=False):
        """Removes an avatar from this group."""
        if avId in self.avIds:
            toon: GroupAvatar = self.getGroupAvatar(avId)
            self.avatarList.remove(toon)
            self.mgr.cleanupInvites(toon.avId)

            # Tell the rest of the avatars they left.
            if not toon.reserved:
                from toontown.notifications.notificationData.GroupCallbackNotification import GroupCallbackNotification
                for av in self.avatarList:
                    av: GroupAvatar
                    if av.reserved:
                        continue
                    self.mgr.sendUpdateToAvatarId(av.avId, "receiveNotification", [
                        GroupCallbackNotification(
                            avId=toon.avId, name=toon.name,
                            errorCode=Responses.ToonLeft, errorType=Responses.OK,
                        ).toStruct()
                    ])

        # Are they allowed to rejoin?
        if noRejoin:
            self.kickedAvIds.append(avId)
        self.sync()

    def updateOptions(self, options: list):
        assert len(self.groupCreation.groupOptions) == len(options)
        self.groupCreation.groupOptions = options
        self.sync()

    def updateToons(self):
        for avatar in self.avatarList:
            avatar.status = avatar.avId in self.mgr.toons.keys()

    def sync(self):
        self.updateToons()
        struct = self.toStruct()
        detailAvatarList = [self.mgr.toons[avatar.avId].toStruct() for avatar in self.avatarList]
        for avatar in self.avatarList:
            self.mgr.sendUpdateToAvatarId(avatar.avId, "updateGroup", [struct])
            self.mgr.sendUpdateToAvatarId(avatar.avId, "receiveGroupInfo", [struct, detailAvatarList])

        if not self.avatarList:
            return self.mgr.cleanupGroup(self)
        else:
            self.mgr.air.netMessenger.send('groupUpdateUD', [self.groupId, 1, struct])

# endregion
