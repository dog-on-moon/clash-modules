from enum import IntEnum
from typing import Optional, Any, List, TYPE_CHECKING

from toontown.inventory.base.InventoryItemBehavior import InventoryItemBehavior
from toontown.inventory.base.ItemID import ItemID
from toontown.inventory.definitions.InventoryItemBehaviorDefinitions import getInventoryItemBehaviorDefinition
from toontown.inventory.enums.ItemAttribute import InventoryStripAttributes
from toontown.inventory.enums.ItemEnums import ItemType
from toontown.inventory.enums.RarityEnums import Rarity
from toontown.utils.AstronDict import AstronDict
from toontown.utils.AstronStruct import AstronStruct

if TYPE_CHECKING:
    from toontown.inventory.base.ItemDefinition import ItemDefinition


class InventoryItem(AstronStruct):
    """
    Represents an item inside of an inventory.
    """

    def __init__(self,
                 itemType: ItemType,
                 itemSubtype: IntEnum,
                 quantity: int = 1,
                 attributes: Optional[AstronDict] = None,
                 itemId: Optional[ItemID] = None):
        if attributes is None:
            attributes = AstronDict()
        if type(attributes) is dict:
            attributes = AstronDict.fromDict(attributes)
        if itemId is None:
            itemId = ItemID.makeUniqueId()
        self.itemType: ItemType = itemType
        self.itemSubtype: IntEnum = itemSubtype
        self.quantity: int = quantity
        self._attributes: AstronDict = attributes
        self.itemId: ItemID = itemId

    def __repr__(self):
        return f'x{self.quantity} {self.itemType.name}-{self.itemSubtype.name} ({repr(self.itemId)})'

    def __hash__(self):
        return hash(self.itemId)

    def toStruct(self):
        return [
            int(self.itemType),          # uint32
            int(self.itemSubtype),       # uint32
            self.quantity,               # uint64
            self.getAttributes().toStruct(),  # AstronDict
            self.itemId.toStruct(),      # AstronUUID
        ]

    @classmethod
    def fromStruct(cls, struct):
        itemType, itemSubtype, quantity, attributes, itemId = struct
        itemClass = cls.getItemClass(itemType)
        return itemClass(
            itemType=ItemType(itemType),
            itemSubtype=ItemType.getSubtypeClass(itemType)(itemSubtype),
            quantity=quantity,
            attributes=cls.updateAttributes(AstronDict.fromStruct(attributes)),
            itemId=ItemID.fromStruct(itemId),
        )

    def toMongo(self) -> dict:
        return {
            't': int(self.itemType),
            's': int(self.itemSubtype),
            'q': self.quantity,
            'a': self.getAttributes().toMongo(),
            'i': self.itemId.toMongo(),
        }

    @classmethod
    def fromMongo(cls, json) -> 'InventoryItem':
        itemType = ItemType(json['t'])
        subtypeCls = ItemType.getSubtypeClass(itemType)
        itemClass = cls.getItemClass(itemType)
        return itemClass(
            itemType=itemType,
            itemSubtype=subtypeCls(json['s']),
            quantity=json['q'],
            attributes=cls.updateAttributes(AstronDict.fromMongo(json['a'])),
            itemId=ItemID.fromMongo(json['i']),
        )

    @classmethod
    def fromSubtype(cls, itemSubtype: IntEnum, quantity: int = 1, attributes: Optional[dict] = None):
        if attributes is None:
            attributes = {}
        itemType = ItemType.getItemType(type(itemSubtype))
        itemClass = cls.getItemClass(itemType)
        return itemClass(
            itemType,
            itemSubtype=itemSubtype,
            quantity=quantity,
            attributes=cls.updateAttributes(AstronDict.fromDict(attributes)),
        )

    def copy(self) -> 'InventoryItem':
        return type(self)(
            itemType=self.getItemType(),
            itemSubtype=self.getItemSubtype(),
            quantity=self.getQuantity(),
            attributes=self.updateAttributes(self.getAttributes().copy()),
            itemId=self.getItemID(),
        )

    def clone(self,
              newItemType: ItemType | None = None,
              newItemSubtype: IntEnum | None = None,
              newQuantity: int | None = None,
              newAttributes: dict | None = None,
              newItemID: ItemID | None = None) -> 'InventoryItem':
        return type(self)(
            itemType=newItemType or self.getItemType(),
            itemSubtype=newItemSubtype or self.getItemSubtype(),
            quantity=newQuantity or self.getQuantity(),
            attributes=newAttributes or self.updateAttributes(self.getAttributes().copy()),
            itemId=newItemID or self.getItemID(),
        )

    def isSameItem(self, other: 'InventoryItem') -> bool:
        return self.itemId == other.itemId

    def __eq__(self, other: 'InventoryItem') -> bool:
        if not isinstance(other, InventoryItem):
            return False
        return self.itemType == other.itemType \
            and self.itemSubtype == other.itemSubtype \
            and self.getAttributes() == other.getAttributes()

    @staticmethod
    def updateAttributes(attributes: AstronDict) -> AstronDict:
        """
        Creates an attributes object in-place after it is created
        from either Mongo or from AstronStruct (used for things
        such as the GagPouchInventoryItem setting GagDict classes).

        Despite modifying in place, it should return the dict too.
        """
        return attributes

    """
    Checks
    """

    def canStack(self, other: 'InventoryItem', withoutOverflow: bool = False) -> bool:
        if self != other:
            # Items must share the same type, subtype, and
            # attributes if it wants to stack.
            return False

        # OK -- these items are stackable.
        # But will this overflow into a new item?
        stackSize = self.getInventoryItemBehavior().getStackSize()
        if withoutOverflow:
            if (self.getQuantity() + other.getQuantity()) > stackSize:
                return False

        # We also absolutely cannot stack if this item is at max quantity.
        if self.getQuantity() >= stackSize:
            return False

        # Stacking is OK.
        return True

    """
    Actions
    """

    def performStack(self, other: 'InventoryItem') -> Optional['InventoryItem']:
        self.setQuantity(self.getQuantity() + other.getQuantity())

        # If there is overflow, we will let the other item be the overflow.
        stackSize = self.getInventoryItemBehavior().getStackSize()
        if self.getQuantity() > stackSize:
            other.setQuantity(self.getQuantity() - stackSize)
            self.setQuantity(stackSize)
            return other
        else:
            other.setQuantity(0)
            return None

    def performSplit(self) -> 'InventoryItem':
        if not self.isOverflowing():
            raise Exception("performSplit called on a non-overflowing item")

        stackSize = self.getInventoryItemBehavior().getStackSize()
        overflow = self.getQuantity() - stackSize
        self.setQuantity(stackSize)

        # Give new item that is overflowing. It gets a new itemID :)
        itemClass = self.getItemClass(self.getItemType())
        return itemClass(
            itemType=self.getItemType(),
            itemSubtype=self.getItemSubtype(),
            quantity=overflow,
            attributes=self.getAttributes().copy(),
        )

    """
    Getters
    """

    def getItemType(self) -> ItemType:
        return self.itemType

    def getItemSubtype(self) -> IntEnum:
        return self.itemSubtype

    def getQuantity(self) -> int:
        return self.quantity

    def getAttributes(self) -> AstronDict:
        if type(self._attributes) is dict:
            # sanity check
            self._attributes = AstronDict.fromDict(self._attributes)
        return self._attributes

    def getItemID(self) -> ItemID:
        return self.itemId

    def getInventoryItemBehavior(self) -> InventoryItemBehavior:
        return getInventoryItemBehaviorDefinition(self.getItemType())

    def isOverflowing(self) -> bool:
        return self.getQuantity() > self.getInventoryItemBehavior().getStackSize()

    def getItemDefinition(self):
        """:rtype: ItemDefinition | Any"""
        from toontown.inventory.registry import ItemTypeRegistry
        return ItemTypeRegistry.getItemDefinition(self.getItemSubtype())

    def getRarity(self) -> Rarity:
        itemDef = self.getItemDefinition()
        return itemDef.getRarity(self)

    @classmethod
    def getItemClass(cls, itemType):
        from toontown.inventory.itemclasses.ItemClassRegistry import ItemClassRegistry
        return ItemClassRegistry.get(itemType, cls)

    """
    Attribute Manipulation
    """

    def getAttribute(self, key: str, default: Optional[Any] = None) -> Any:
        return self.getAttributes().get(key, default)

    def hasAttribute(self, key: str) -> bool:
        return key in self.getAttributes()

    def setAttribute(self, key: str, value: Any):
        self.getAttributes()[key] = value

    def setAttributes(self, attributes: dict):
        if isinstance(attributes, AstronDict):
            self._attributes = attributes.copy()
        else:
            self._attributes = AstronDict.fromDict(attributes)
        self.getAttributes()

    def stripAttributes(self):
        for attr in InventoryStripAttributes:
            if self.hasAttribute(attr):
                del self._attributes[attr]

    """
    Other useful setters
    """

    def setQuantity(self, val) -> None:
        self.quantity = val

    """
    Useful static methods
    """

    @staticmethod
    def findItemTypesFromItemList(itemType: ItemType, itemList: List['InventoryItem']) -> List['InventoryItem']:
        return [
            inventoryItem
            for inventoryItem in itemList
            if inventoryItem.getItemType() == itemType
        ]
