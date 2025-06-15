import time
from enum import IntEnum
from typing import List, TYPE_CHECKING, Dict, Set

from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.base.ItemID import ItemID
from toontown.inventory.enums.ItemEnums import ItemType

if TYPE_CHECKING:
    from toontown.inventory.base.Inventory import Inventory


class InventoryCache:
    """
    An interface for faster access to inventory items.
    """

    def __init__(self):
        self.__equippedItemIDs: List[ItemID] = []
        self.__items: List[InventoryItem] = []

        # Cache state
        self.__lastModified: float = time.time()
        self.__itemIDsSet: Set[ItemID] = set()
        self.__equippedItemIDsSet: Set[ItemID] = set()
        self.__equippedItems: List[InventoryItem] = []
        self.__itemID2Item: Dict[ItemID, InventoryItem] = {}
        self.__itemType2Items: Dict[ItemType, List[InventoryItem]] = {}
        self.__itemType2Subtype2Items: Dict[ItemType, Dict[IntEnum, List[InventoryItem]]] = {}

    def cleanup(self):
        del self.__equippedItemIDs
        del self.__items
        del self.__itemIDsSet
        del self.__equippedItemIDsSet
        del self.__equippedItems
        del self.__itemID2Item
        del self.__itemType2Items
        del self.__itemType2Subtype2Items

    def update(self, inventory) -> None:
        """
        Updates the inventory cache.
        :type inventory: Inventory
        """
        self.__equippedItemIDs = inventory.getEquippedItemIDs()
        self.__items = inventory.getItems()

        # Reset the cache variables.
        self.__lastModified: float = time.time()
        self.__itemIDsSet = set()
        self.__equippedItemIDsSet = set(self.__equippedItemIDs)
        self.__equippedItems = []
        self.__itemID2Item = {}
        self.__itemType2Items = {}
        self.__itemType2Subtype2Items = {}

        # Update the cache variables.
        for item in self.__items:
            # Get item attributes.
            itemID: ItemID = item.getItemID()
            itemType: ItemType = item.getItemType()
            itemSubtype: IntEnum = item.getItemSubtype()

            # Set local state.
            self.__itemIDsSet.add(itemID)

            self.__itemID2Item[itemID] = item

            self.__itemType2Items.setdefault(itemType, [])
            self.__itemType2Items[itemType].append(item)

            self.__itemType2Subtype2Items.setdefault(itemType, {})
            self.__itemType2Subtype2Items[itemType].setdefault(itemSubtype, [])
            self.__itemType2Subtype2Items[itemType][itemSubtype].append(item)

        for itemID in self.__equippedItemIDs:
            if itemID not in self.__itemID2Item:
                # we are OK empty-evaluating right now, as a cache on generation
                # may only have the itemIds but not the items
                # (like when we are sending client item partials)
                continue
            self.__equippedItems.append(self.getItemFromID(itemID))

    """
    Cache access
    """

    def getLastModified(self) -> float:
        return self.__lastModified

    def getTimeSinceModified(self) -> float:
        return time.time() - self.getLastModified()

    def hasItemID(self, itemID: ItemID) -> bool:
        return itemID in self.__itemIDsSet

    def hasItemIDEquipped(self, itemID: ItemID) -> bool:
        return itemID in self.__equippedItemIDsSet

    def getItemFromID(self, itemID: ItemID) -> InventoryItem:
        if itemID not in self.__itemID2Item:
            # If this crash ever happens...
            # ...Main will cry, a lot...
            raise KeyError(f"Inventory was missing itemID {itemID}")
        return self.__itemID2Item.get(itemID)

    def getEquippedItems(self) -> List[InventoryItem]:
        return self.__equippedItems

    def getItemsOfType(self, itemType: ItemType) -> List[InventoryItem]:
        return self.__itemType2Items.get(itemType, [])

    def getItemsOfSubtype(self, itemSubtype: IntEnum) -> List[InventoryItem]:
        itemType = ItemType.getItemType(type(itemSubtype))
        if itemType not in self.__itemType2Subtype2Items:
            return []
        if itemSubtype not in self.__itemType2Subtype2Items[itemType]:
            return []
        return self.__itemType2Subtype2Items[itemType][itemSubtype]

    def getItemCount(self, itemSubtype: IntEnum) -> int:
        return sum(
            item.getQuantity()
            for item in self.getItemsOfSubtype(itemSubtype)
        )
