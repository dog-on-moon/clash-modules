from enum import IntEnum
from typing import Any, Optional

from toontown.inventory.base.Inventory import Inventory
from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.registry import ItemTypeRegistry
from toontown.shop.base.ShopItem import ShopItem
from toontown.shop.base.ShopPriceTag import PriceTags


class InventoryShopItem(ShopItem):

    def __init__(self,
                 item: IntEnum, priceTags: PriceTags,
                 quantity: int = 1, attributes: Optional[dict] = None):
        super().__init__(priceTags=priceTags)
        if attributes is None:
            attributes = {}
        self.itemSubtype = item
        self.itemDef = ItemTypeRegistry.getItemDefinition(self.itemSubtype)
        self.quantity = quantity
        self.attributes = attributes

    def grantItem(self, av) -> Any:
        hs = av.getHammerspace()
        hs.addItem(self.makeInventoryItem())

    def getName(self) -> str:
        itemDefinition = ItemTypeRegistry.getItemDefinition(self.itemSubtype)
        return itemDefinition.getName()

    def getDescription(self) -> str:
        itemDefinition = ItemTypeRegistry.getItemDefinition(self.itemSubtype)
        return itemDefinition.getShopDescription()

    def canPurchase(self, av) -> bool:
        hs: Inventory = av.getHammerspace()
        if hs:
            return super().canPurchase(av) \
                   and hs.canAddItem(self.makeInventoryItem())
        else:
            return False

    def ownsItem(self, av) -> bool:
        hs: Inventory = av.getHammerspace()
        if hs:
            return bool(hs.findItems(self.itemSubtype))
        else:
            return False

    def makeInventoryItem(self) -> InventoryItem:
        return InventoryItem.fromSubtype(
            itemSubtype=self.itemSubtype,
            quantity=self.quantity,
            attributes=self.attributes,
        )
