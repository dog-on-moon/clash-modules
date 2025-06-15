from typing import Optional
from enum import IntEnum, auto


class EquipAction(IntEnum):
    DEFAULT = auto()
    BOOSTER = auto()


class InventoryItemBehavior:
    """
    This is the base class that determines how InventoryItems behave
    in regards to behaving nicely in the Inventory overall.
    """

    def __init__(self,
                 stackSize: int = 999_999_999,
                 maxSubtypeQuantity: Optional[int] = 99_999_999,
                 maxTypeQuantity: Optional[int] = None,
                 canEquip: bool = False,
                 maxEquipped: int = 1,
                 minEquipped: Optional[int] = None,
                 canForceUnequip: bool = True,
                 forceEquipOnAdd: bool = False,
                 canDelete: bool = False,
                 equipAction: EquipAction = EquipAction.DEFAULT):
        self._stackSize = stackSize
        self._maxSubtypeQuantity = maxSubtypeQuantity
        self._maxTypeQuantity = maxTypeQuantity
        self._canEquip = canEquip
        self._maxEquipped = maxEquipped
        self._minEquipped = minEquipped
        self._canForceUnequip = canForceUnequip
        self._forceEquipOnAdd = forceEquipOnAdd
        self._canDelete = canDelete
        self._equipAction = equipAction

    """
    Getters
    """

    def getStackSize(self) -> int:
        return self._stackSize

    def getMaxSubtypeQuantity(self) -> Optional[int]:
        return self._maxSubtypeQuantity

    def getMaxTypeQuantity(self) -> Optional[int]:
        return self._maxTypeQuantity

    def canEquip(self) -> bool:
        return self._canEquip

    def getMaxEquipped(self) -> int:
        return self._maxEquipped

    def getMinEquipped(self) -> Optional[int]:
        return self._minEquipped

    def canForceUnequip(self) -> bool:
        return self._canForceUnequip

    def getForceEquipOnAdd(self) -> bool:
        return self._forceEquipOnAdd

    def canDelete(self) -> bool:
        return self._canDelete

    def getEquipAction(self) -> EquipAction:
        return self._equipAction
