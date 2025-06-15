"""
This module defines the behavior for each inventory type.
"""
from toontown.inventory.base.InventoryBehavior import InventoryBehavior
from toontown.inventory.enums.InventoryEnums import InventoryType
from toontown.toonbase import RealmGlobals

__InventoryBehaviorDefinitions = {
    InventoryType.FullBehavior: InventoryBehavior(
        maxSize=999,
    ),
    InventoryType.Test: InventoryBehavior(
        maxSize=5,
    ),

    InventoryType.Player: InventoryBehavior(
        maxSize=5000,
        canSwapBetweenSameType=False,
    ),
    InventoryType.Chest: InventoryBehavior(
        maxSize=20,
        canAddItems=False,
        canDeleteItems=False,
        canSwapItemsIn=False,
        canEquipItems=False,
    ),
    InventoryType.Cache: InventoryBehavior(
        canAddItems=False,
        canDeleteItems=False,
        canEquipItems=False,
        canSwapItemsIn=False,
        canSwapBetweenSameType=False,
    ),
}

if RealmGlobals.getCurrentRealm().isDevRealm():
    __InventoryBehaviorDefinitions[InventoryType.Player] = InventoryBehavior(
        maxSize=99999,
        canSwapBetweenSameType=False,
    )


def getInventoryBehaviorDefinition(inventoryType: InventoryType) -> InventoryBehavior:
    assert inventoryType in __InventoryBehaviorDefinitions, \
           f"Undefined inventory behavior for {inventoryType}."
    return __InventoryBehaviorDefinitions.get(inventoryType)
