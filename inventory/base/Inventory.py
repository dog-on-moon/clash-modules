from datetime import timedelta
from enum import IntEnum
from typing import Optional, List, Union, Any

from toontown.inventory.base.InventoryBehavior import InventoryBehavior
from toontown.inventory.base.InventoryCache import InventoryCache
from toontown.inventory.base.InventoryDelta import InventoryDelta
from toontown.inventory.base.InventoryExceptions import InventoryActionFailure
from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.base.InventoryItemBehavior import EquipAction
from toontown.inventory.base.ItemID import ItemID
from toontown.inventory.definitions.InventoryBehaviorDefinitions import getInventoryBehaviorDefinition
from toontown.inventory.enums.InventoryEnums import InventoryType, InventoryAction
from toontown.inventory.enums.ItemAttribute import ItemAttribute
from toontown.inventory.enums.ItemEnums import ItemType
from toontown.utils.AstronDict import AstronDict
from toontown.utils.AstronStruct import AstronStruct


class Inventory(AstronStruct):
    """
    Provides a basic interface for an inventory.
    """

    def __init__(self,
                 inventoryType: InventoryType,
                 equippedItemIDs: List[ItemID] = None,
                 items: Optional[List[InventoryItem]] = None,
                 attributes: Optional[AstronDict] = None):
        if equippedItemIDs is None:
            equippedItemIDs = []
        if items is None:
            items = []
        if attributes is None:
            attributes = AstronDict()

        # Inventory attributes
        self.inventoryType = inventoryType
        self.equippedItemIDs = equippedItemIDs
        self.items = items
        self.attributes = attributes

        # Local inventory state
        self.cache: InventoryCache = InventoryCache()
        self.cache.update(self)

        self.owner: Any | None = None

        # Delta management
        self._deltaCallbacks = []
        self._latestDeltas = []

    def __repr__(self):
        return f'{self.inventoryType} inv: {self.items} (Equipped: {self.equippedItemIDs})'

    def cleanup(self):
        del self.inventoryType
        del self.equippedItemIDs
        del self.items
        del self.attributes
        self.cache.cleanup()
        del self.cache
        del self.owner
        del self._deltaCallbacks
        del self._latestDeltas

    def toStruct(self) -> list:
        return [
            int(self.inventoryType),                    # uint16
            ItemID.toStructList(self.equippedItemIDs),  # AstronUUID[]
            InventoryItem.toStructList(self.items),     # InventoryItem[]
            self.attributes.toStruct(),                 # AstronDict
        ]

    @classmethod
    def fromStruct(cls, struct) -> 'Inventory':
        inventoryType, equippedItemIDs, items, attributes = struct
        return cls(
            inventoryType=InventoryType(inventoryType),
            equippedItemIDs=ItemID.fromStructList(equippedItemIDs),
            items=InventoryItem.fromStructList(items),
            attributes=AstronDict.fromStruct(attributes),
        )

    def toMongo(self) -> dict:
        return {
            't': int(self.inventoryType),
            'e': [ItemID.toMongo(equippedItemID) for equippedItemID in self.equippedItemIDs],
            'i': [InventoryItem.toMongo(item) for item in self.items],
            'a': self.attributes.toMongo(),
        }

    @classmethod
    def fromMongo(cls, json) -> 'Inventory':
        return cls(
            inventoryType=InventoryType(json['t']),
            equippedItemIDs=[ItemID.fromMongo(equippedItemID) for equippedItemID in json['e']],
            items=[InventoryItem.fromMongo(item) for item in json['i']],
            attributes=AstronDict.fromMongo(json['a']),
        )

    def makeItemless(self) -> 'Inventory':
        """
        Makes an itemless copy of this inventory.
        """
        return type(self)(
            inventoryType=self.getInventoryType(),
            equippedItemIDs=self.getEquippedItemIDs(),
            items=[],
            attributes=self.getAttributes(),
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, Inventory):
            return False
        return self.inventoryType == other.inventoryType \
            and self.equippedItemIDs == other.equippedItemIDs \
            and self.items == other.items \
            and self.attributes == other.attributes

    def __hash__(self) -> int:
        maxVal = 2 ** 64
        currHash = 0
        for item in self.items:
            currHash = (currHash + hash(item)) % maxVal
        return currHash

    """
    Setup
    """

    def setOwner(self, owner: Any):
        self.owner = owner

    """
    Delta Management
    """

    def addDeltaCallback(self, callback: callable):
        """
        Adds a callback for when this inventory updates.
        It will be called back with two arguments:
            A) the inventory
            A) a list of the latest deltas
        """
        self._deltaCallbacks.append(callback)

    def removeDeltaCallback(self, callback: callable):
        assert callback in self._deltaCallbacks, "Callback not found"
        self._deltaCallbacks.remove(callback)

    def _onInventoryUpdate(self):
        """Called locally when the inventory updates."""
        self.cache.update(self)

        # Do delta callbacks.
        if self._deltaCallbacks:
            deltas = self._latestDeltas[:]
            self._latestDeltas = []
            for callback in self._deltaCallbacks:
                callback(self, deltas)

    def _addDelta(self, action: InventoryAction, item: InventoryItem) -> None:
        """Adds this delta as a marked change."""
        if not self._deltaCallbacks:
            return

        self._latestDeltas.append(
            InventoryDelta(
                action=action,
                item=item,
            )
        )

    """
    Inventory Checks
    """

    def canAddItem(self, item: InventoryItem) -> bool:
        """Determines if an item can be added into the Inventory."""
        # Get the behavior logic.
        inventoryBehavior = self.getInventoryBehavior()
        itemBehavior = item.getInventoryItemBehavior()

        # Don't re-add this item if it is already in the inventory.
        if self.cache.hasItemID(item.getItemID()):
            return False

        # Check if this item can stack.
        canStack = False
        for otherItem in self.findItems(item.getItemSubtype()):
            if otherItem.canStack(item):
                # We can indeed stack into an item without overflow --
                # therefore, this check is safe and the item can be added.
                canStack = True
                break

        # Do inventory behavior checks.
        if not inventoryBehavior.canAddItems():
            return False
        if self.getTotalStackCount() >= inventoryBehavior.getMaxSize() and not canStack:
            return False
        if inventoryBehavior.getTypeFilter():
            if item.getItemType() not in inventoryBehavior.getTypeFilter():
                return False

        # Do item behavior checks.
        if itemBehavior.getMaxSubtypeQuantity() is not None:
            if len(self.findItems(item.getItemSubtype())) >= itemBehavior.getMaxSubtypeQuantity() and not canStack:
                return False
        if itemBehavior.getMaxTypeQuantity() is not None:
            if len(self.findItemsOfType(item.getItemType())) >= itemBehavior.getMaxTypeQuantity() and not canStack:
                return False

        # Seems like this item can be added.
        return True

    def canRemoveItem(self, item: InventoryItem, manualDelete: bool, mustHaveEnough: bool = True) -> bool:
        """Determines if an item can be removed from the Inventory."""
        # Get the behavior logic.
        inventoryBehavior = self.getInventoryBehavior()
        itemBehavior = item.getInventoryItemBehavior()

        # Is this a manual delete?
        if manualDelete and not inventoryBehavior.canDeleteItems():
            return False

        # Can the item be deleted?
        if not itemBehavior.canDelete() and itemBehavior.getEquipAction() != EquipAction.BOOSTER:
            return False

        if mustHaveEnough:
            # We need to make sure there are enough items to delete.
            removeQuantity = item.getQuantity()
            for invItem in self.cache.getItemsOfSubtype(item.getItemSubtype()):
                removeQuantity -= invItem.getQuantity()
            if removeQuantity > 0:
                # Not enough items to remove.
                return False

        # Seems like this item can be removed.
        return True

    def canEquipItem(self, item: InventoryItem) -> bool:
        # Get the behavior logic.
        inventoryBehavior = self.getInventoryBehavior()
        itemBehavior = item.getInventoryItemBehavior()

        # Can this inventory even equip items?
        if not inventoryBehavior.canEquipItems():
            return False

        # Can this item be equipped?
        if not itemBehavior.canEquip():
            return False

        # Is this item already equipped?
        if self.cache.hasItemIDEquipped(item.getItemID()):
            return False

        # This item is owned?
        if not self.cache.hasItemID(item.getItemID()):
            return False

        # Are there too many items equipped?
        if not itemBehavior.canForceUnequip():
            if len(self.getEquippedItems(item.getItemType())) >= itemBehavior.getMaxEquipped():
                return False

        # For boosters, will be able to remove it after?
        if itemBehavior.getEquipAction() == EquipAction.BOOSTER:
            singleItem = item.clone(newQuantity=1)
            if not self.canRemoveItem(singleItem, manualDelete=False):
                return False

        # We can equip it!! Yippee
        return True

    def canUnequipItem(self, item: InventoryItem) -> bool:
        # Get the behavior logic.
        inventoryBehavior = self.getInventoryBehavior()
        itemBehavior = item.getInventoryItemBehavior()

        # Can this inventory even equip items?
        if not inventoryBehavior.canEquipItems():
            return False

        # Can this item be equipped?
        if not itemBehavior.canEquip():
            return False

        # Is this item even equipped?
        if not self.cache.hasItemIDEquipped(item.getItemID()):
            return False

        # Would this make there be too little items equipped?
        if itemBehavior.getMinEquipped() is not None:
            if len(self.getEquippedItems(item.getItemType())) <= itemBehavior.getMinEquipped():
                return False

        # We can unequip it!! Yippee
        return True

    def canUpdateItem(self, item: InventoryItem) -> bool:
        itemInInventory = self.cache.getItemFromID(item.getItemID())
        if not itemInInventory:
            return False
        return True

    def canSwapItemTo(self, other: 'Inventory', item: InventoryItem) -> bool:
        if not self.canRemoveItem(item, manualDelete=False):
            return False
        if not other.canAddItem(item):
            return False

        selfInventoryBehavior = self.getInventoryBehavior()
        if not selfInventoryBehavior.canSwapItemsOut():
            return False
        otherInventoryBehavior = other.getInventoryBehavior()
        if not otherInventoryBehavior.canSwapItemsIn():
            return False
        if self.getInventoryType() == other.getInventoryType():
            if not selfInventoryBehavior.canSwapBetweenSameType():
                return False

        # The swap should be OK.
        return True

    """
    Inventory Actions
    """

    def addItem(self, item: Union[InventoryItem, IntEnum], quantity: int = 1) -> bool:
        """
        Adds an item to the inventory.
        NOTE -- THIS CAN MODIFY (ITEM) BY STRIPPING ITS ATTRIBUTES !!
        """
        if isinstance(item, IntEnum):
            item = InventoryItem.fromSubtype(item, quantity=quantity)
        if self.canAddItem(item):
            self._addDelta(InventoryAction.ADD, item=item.copy())
            overflow = self._performAddItem(item)
            while overflow:
                if self.canAddItem(overflow):
                    overflow = self._performAddItem(overflow)
                else:
                    break
            return True
        return False

    def removeItem(self, item: InventoryItem, manualDelete: bool = False) -> bool:
        if self.canRemoveItem(item, manualDelete):
            self._addDelta(InventoryAction.REMOVE, item=item.copy())
            self._performRemoveItem(item)
            return True
        return False

    def equipItem(self, item: InventoryItem) -> bool:
        if self.canEquipItem(item):
            self._addDelta(InventoryAction.EQUIP, item=item.copy())
            self._performEquipItem(item)
            return True
        return False

    def unequipItem(self, item: InventoryItem) -> bool:
        if self.canUnequipItem(item):
            self._addDelta(InventoryAction.UNEQUIP, item=item.copy())
            self._performUnequipItem(item)
            return True
        return False

    def updateItem(self, item: InventoryItem) -> bool:
        if self.canUpdateItem(item):
            itemInInventory = self.cache.getItemFromID(item.getItemID())
            if not itemInInventory:
                return False
            itemInInventory.setAttributes(item.getAttributes())
            itemInInventory.setQuantity(item.getQuantity())
            self._addDelta(InventoryAction.UPDATE, itemInInventory.copy())
            self._onInventoryUpdate()
            return True
        return True

    def swapItemTo(self, other: 'Inventory', item: InventoryItem) -> bool:
        """Removes item from self, adds to other"""
        if self is other:
            raise InventoryActionFailure
        if self.canSwapItemTo(other, item):
            self._performSwapItemTo(other, item)
            return True
        return False

    def applyDelta(self, delta: InventoryDelta):
        """Applies an InventoryDelta."""
        action: InventoryAction = delta.getAction()
        item: InventoryItem = delta.getItem()

        # Perform delta callback.
        callback = {
            InventoryAction.ADD:     self.addItem,
            InventoryAction.REMOVE:  self.removeItem,
            InventoryAction.EQUIP:   self.equipItem,
            InventoryAction.UNEQUIP: self.unequipItem,
            InventoryAction.UPDATE:  self.updateItem,
        }.get(action)
        callback(item=item)

    def testDelta(self, delta: InventoryDelta) -> bool:
        """Tests to see if a delta can be applied."""
        action: InventoryAction = delta.getAction()
        item: InventoryItem = delta.getItem()

        # Perform delta callback.
        callback = {
            InventoryAction.ADD:     self.canAddItem,
            InventoryAction.REMOVE:  self.canRemoveItem,
            InventoryAction.EQUIP:   self.canEquipItem,
            InventoryAction.UNEQUIP: self.canUnequipItem,
            InventoryAction.UPDATE:  self.canUpdateItem,
        }.get(action)
        return callback(item=item)

    """
    Inventory Performance
    """

    def _performAddItem(self, item: InventoryItem) -> Optional[InventoryItem]:
        # Strip inventory attributes.
        item.stripAttributes()

        # Attempt to stack the item with an existing item.
        for otherItem in self.findItems(item.getItemSubtype()):
            if otherItem.canStack(item):
                # We will stack into this item!
                overflow = otherItem.performStack(item)

                # If we have overflow, we will have to add it separately.
                # Yes, this call will happen recursively lol.
                if overflow and self.canAddItem(overflow):
                    return overflow

                # We are done here.
                self._onInventoryUpdate()
                return None

        # STRONGLY AVOID adding this item if it shares an ID with an existing one
        if self.cache.hasItemID(item.getItemID()):
            raise InventoryActionFailure

        # If this item is too big, we need to split it.
        if item.isOverflowing():
            overflow = item.performSplit()
            self.items.append(item)
            return overflow

        # We can simply add this item as a separate item.
        self.items.append(item)
        self._onInventoryUpdate()

        # In addition, request an equip if need be.
        if item.getInventoryItemBehavior().getForceEquipOnAdd():
            self.equipItem(item)
        return None

    def _performRemoveItem(self, item: InventoryItem) -> None:
        # Go through all existing items of the same subtype,
        # and go ahead and make "zero-quantity" items.
        zeroQuantityItems = []
        for otherItem in self.findItems(item.getItemSubtype()):
            # If these items are the same, we can remove it.
            if item == otherItem:
                # Are we going to have to remove additional items?
                if otherItem.getQuantity() < item.getQuantity():
                    # Indeed we will have to remove extra.
                    item.setQuantity(item.getQuantity() - otherItem.getQuantity())
                    otherItem.setQuantity(0)
                    zeroQuantityItems.append(otherItem)
                else:
                    # Nope, just detract from this one.
                    otherItem.setQuantity(otherItem.getQuantity() - item.getQuantity())

                    # Is this item a ZQ now?
                    if otherItem.getQuantity() == 0:
                        zeroQuantityItems.append(otherItem)

                    # This item is exhausted for removal now.
                    break

        # Remove all zero-quantity items.
        for zqItem in zeroQuantityItems:
            self.items.remove(zqItem)
            if zqItem.getItemID() in self.equippedItemIDs:
                self.equippedItemIDs.remove(zqItem.getItemID())
        self._onInventoryUpdate()

    def _performEquipItem(self, item: InventoryItem) -> None:
        # We may need to force-unequip an item.
        itemBehavior = item.getInventoryItemBehavior()
        if itemBehavior.getEquipAction() == EquipAction.DEFAULT:
            equippedItems = self.getEquippedItems(item.getItemType())
            if len(equippedItems) >= itemBehavior.getMaxEquipped():
                # Hmm.. We need to force unequip an item here.
                self.equippedItemIDs.remove(equippedItems[0].getItemID())

            # Equip the new item.
            self.equippedItemIDs.append(item.getItemID())
            self._onInventoryUpdate()
        elif itemBehavior.getEquipAction() == EquipAction.BOOSTER:
            # Set the booster if we're AI.
            from toontown.toonbase import ProcessGlobals
            if not (ProcessGlobals.getCurrentProcess() == ProcessGlobals.Process.AI and self.owner):
                return
            from toontown.booster.BoosterHandler import BoosterHandler
            if not isinstance(self.owner, BoosterHandler):
                return

            # Add the booster.
            from toontown.inventory.enums.ItemEnums import BoosterItemType
            from toontown.booster.BoosterGlobals import getReasonableBooster
            boosterType = item.getItemSubtype()
            if boosterType == BoosterItemType.Random:
                boosterType = getReasonableBooster(self.owner, includeSuper=True)
            self.owner.addNewBooster(
                boosterType=boosterType,
                timeDelta=timedelta(minutes=item.getAttribute(ItemAttribute.MINUTES, 120))
            )

            # Destroy the booster.
            self.removeItem(item.clone(newQuantity=1), manualDelete=False)
        else:
            raise KeyError

    def _performUnequipItem(self, item: InventoryItem) -> None:
        self.equippedItemIDs.remove(item.getItemID())
        self._onInventoryUpdate()

    def _performSwapItemTo(self, other: 'Inventory', item: InventoryItem) -> None:
        self.removeItem(item.copy())
        other.addItem(item.copy())

    """
    Simple Getters
    """

    def getInventoryType(self) -> InventoryType:
        return self.inventoryType

    def getEquippedItemIDs(self) -> List[ItemID]:
        return self.equippedItemIDs

    def getItems(self) -> List[InventoryItem]:
        return self.items

    def getAttributes(self) -> AstronDict:
        return self.attributes

    def getInventoryBehavior(self) -> InventoryBehavior:
        return getInventoryBehaviorDefinition(self.getInventoryType())

    def getOwner(self) -> Any:
        return self.owner

    """
    Inventory Getters
    """

    def getCache(self) -> InventoryCache:
        return self.cache

    def updateCache(self):
        self.cache.update(self)

    def getTotalStackCount(self) -> int:
        """
        Get the total number of item stacks in the inventory.
        """
        return len(self.getItems())

    def getStackSpace(self) -> int:
        """
        Gets the amount of stack space left in the inventory.
        """
        return self.getInventoryBehavior().getMaxSize() - self.getTotalStackCount()

    def getEquippedItems(self, *itemTypes: ItemType) -> List[InventoryItem]:
        """
        Given specified item types, returns a list of equipped items
        that are supported by the filter.

        If no filter is specified, it will return all equipped items.
        """
        if itemTypes:
            return [
                item for item in self.cache.getEquippedItems()
                if item.getItemType() in itemTypes
            ]
        else:
            return self.cache.getEquippedItems()

    def findItems(self, *itemSubtypes: IntEnum) -> List[InventoryItem]:
        """
        Finds items matching various item subtypes.
        """
        # Hunt for the items now.
        retList = []

        # Extend by each matching subtype.
        for itemSubtype in itemSubtypes:
            retList.extend(self.cache.getItemsOfSubtype(itemSubtype))

        # Return list.
        return retList

    def findItemsOfType(self, *itemTypes: ItemType) -> List[InventoryItem]:
        # Hunt for the items now.
        retList = []

        # Extend by each matching subtype.
        for itemType in itemTypes:
            retList.extend(self.cache.getItemsOfType(itemType))

        # Return list.
        return retList
