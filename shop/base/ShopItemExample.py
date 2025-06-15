"""
This module shows an example of a ShopItem subclass, with all the required fields populated.
"""
from typing import Tuple, Any

from toontown.shop.base.ShopItem import ShopItem
from toontown.shop.base.ShopPriceTag import ShopPriceTag
from toontown.shop.cost.JellybeanPriceTag import JellybeanPriceTag


class ShopItemExample(ShopItem):
    def __init__(self, itemId: int, name: str, desc: str, cost: int):
        super().__init__(priceTags=JellybeanPriceTag(cost))
        self.itemId = itemId
        self.name = name
        self.desc = desc

    def __eq__(self, other):
        return type(self) is type(other) and self.itemId == other.itemId

    def grantItem(self, av) -> Any:
        # This is where you grant the item
        return

    def getName(self) -> str:
        return self.name

    def getDescription(self) -> str:
        return self.desc
