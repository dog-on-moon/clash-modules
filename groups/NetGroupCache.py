from toontown.groups.GroupClasses import GroupUD
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory

from typing import TYPE_CHECKING, Dict, Set, Optional

if TYPE_CHECKING:
    from toontown.utils.BuiltinHelper import *
    from toontown.distributed.ToontownInternalRepository import ToontownInternalRepository


@DirectNotifyCategory()
class NetGroupCache:
    """
    Uses the NetMessenger to cache groups.
    """

    def __init__(self, air):
        self.air = air  # type: ToontownInternalRepository

        # Cache
        self._groups        = {}  # type: Dict[int, GroupUD]
        self._avId2Group    = {}  # type: Dict[int, GroupUD]
        self._groupId2AvIds = {}  # type: Dict[int, Set]

        # Listen to hooks.
        self.air.netMessenger.accept("groupUpdateUD", self, self.onGroupUpdate)

    def onGroupUpdate(self, groupId: int, status: int, group: GroupUD):
        """
        Receives a group container update.
        """
        # First, clean up our current references for the avs.
        if groupId in self._groupId2AvIds:
            for avId in self._groupId2AvIds[groupId]:
                if avId in self._avId2Group:
                    del self._avId2Group[avId]
            del self._groupId2AvIds[groupId]

        if status:
            # This is a fresh group update, populate cache.
            group = GroupUD.fromStruct(group)
            self._groups[groupId] = group

            # Then set new ones.
            avIds = group.avIds[:]
            for avId in avIds:
                self._avId2Group[avId] = group
            self._groupId2AvIds[groupId] = avIds

        elif groupId in self._groups:
            # The group has disbanded.
            del self._groups[groupId]

    def getGroup(self, groupId: Optional[int] = None, avId: Optional[int] = None) -> Optional[GroupUD]:
        """
        Gets a group from arguments.
        """
        if groupId:
            return self._groups.get(groupId)
        elif avId:
            return self._avId2Group.get(avId)
        else:
            return None
