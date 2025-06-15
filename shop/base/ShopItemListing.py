"""
A container class for listing several shop items.
"""
from typing import List, Union

from toontown.shop.base.ShopItem import ShopItem


class ShopItemListing:

    def __init__(self, shopItems: List[Union[ShopItem, List[ShopItem]]]):
        self.shopItems: List[Union[ShopItem, List[ShopItem]]] = shopItems

    def __repr__(self):
        return repr(self.shopItems)

    def getItems(self, *args, **kwargs) -> List[Union[ShopItem, List[ShopItem]]]:
        """Gets items, leaving shopItem lists intact."""
        return self.shopItems

    def getItemCount(self, *args, **kwargs) -> int:
        """Gets items, leaving shopItem lists intact."""
        return len(self.getItems(*args, **kwargs))

    def getDecompressedItems(self, *args, **kwargs) -> List[ShopItem]:
        """Gets the decompressed list of items, including subitems in lists."""
        returnItems = []
        for shopItem in self.getItems(*args, **kwargs):
            if isinstance(shopItem, list):
                returnItems.extend(shopItem)
            else:
                returnItems.append(shopItem)
        return returnItems

    def getDecompressedItemCount(self, *args, **kwargs) -> int:
        """Gets the decompressed amount of items, including subitems in lists."""
        return len(self.getDecompressedItems(*args, **kwargs))

    """
    Item Generation
    """

    def canGenerateItems(self, **kwargs) -> bool:
        """
        Determines if this item listing can dynamically generate items.
        :return: True if so, False if not.
        """
        return False

    def generateItems(self, **kwargs) -> None:
        """
        Generates the items to be used (set self.shopItems).
        :return:
        """
        pass
