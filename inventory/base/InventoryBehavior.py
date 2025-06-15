from typing import List

from toontown.inventory.enums.ItemEnums import ItemType


class InventoryBehavior:
    """
    This class provides an interface into the basic actions
    that are permitted for an inventory.
    """

    def __init__(self,
                 maxSize:                int  = 100,
                 typeFilter:             List[ItemType] = None,
                 canAddItems:            bool = True,
                 canDeleteItems:         bool = True,
                 canEquipItems:          bool = True,
                 canSwapItemsIn:         bool = True,
                 canSwapItemsOut:        bool = True,
                 canSwapBetweenSameType: bool = True):
        if typeFilter is None:
            typeFilter = []
        self._maxSize = maxSize
        self._typeFilter = typeFilter
        self._canAddItems = canAddItems
        self._canDeleteItems = canDeleteItems
        self._canEquipItems = canEquipItems
        self._canSwapItemsIn = canSwapItemsIn
        self._canSwapItemsOut = canSwapItemsOut
        self._canSwapBetweenSameType = canSwapBetweenSameType

    """
    Getters
    """

    def getMaxSize(self) -> int:
        return self._maxSize

    def getTypeFilter(self) -> List[ItemType]:
        return self._typeFilter

    def canAddItems(self) -> bool:
        return self._canAddItems

    def canDeleteItems(self) -> bool:
        return self._canDeleteItems

    def canEquipItems(self) -> bool:
        return self._canEquipItems

    def canSwapItemsIn(self) -> bool:
        return self._canSwapItemsIn

    def canSwapItemsOut(self) -> bool:
        return self._canSwapItemsOut

    def canSwapBetweenSameType(self) -> bool:
        return self._canSwapBetweenSameType
