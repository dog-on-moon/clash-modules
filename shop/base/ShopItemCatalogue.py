from typing import Dict, List, Optional, Union

from toontown.shop.base.ShopCategoryEnum import ShopCategoryEnum
from toontown.shop.base.ShopItem import ShopItem
from toontown.shop.base.ShopItemListing import ShopItemListing


# Make typehint for PageType.
# On built, these types will not exist, so we will
# handle the exception with a simplification.
try:
    PageType = Union[int, ShopCategoryEnum]
except NameError:
    PageType = int


class ShopItemCatalogue:
    """
    A base class to form a complete catalogue of shop items.
    Organized from ShopCategory to ItemListings.

    This class is essentially the highest-level dataclass for organization
    of ShopItems. Client GUI classes can refer to this catalogue, while various
    purchase redemption should be handled by the ShopManagerAI that uses the same catalogue.
    """

    def __init__(self, itemCatalogue: Dict[PageType, Union[ShopItemListing, list]]):
        # Remap any lists into the preferred type.
        for pageType, itemListing in itemCatalogue.items():
            if type(itemListing) is list:
                itemCatalogue[pageType] = ShopItemListing(itemListing)
        
        self.itemCatalogue = itemCatalogue

    def __repr__(self):
        return repr(self.itemCatalogue)

    ### Getters ###

    def getAllCategories(self) -> List[PageType]:
        return list(self.itemCatalogue.keys())

    def getAllItemListings(self, index: bool = True, **kwargs) -> List[ShopItemListing]:
        if index:
            self._indexAllItems(**kwargs)
        return list(self.itemCatalogue.values())

    def getAllItems(self, **kwargs) -> List[ShopItem]:
        return self._indexAllItems(**kwargs)

    def getItemListing(self, category: PageType, **kwargs):
        assert category in self.itemCatalogue, f"{self} is missing category: {category}"
        self._indexAllItems(**kwargs)
        return self.itemCatalogue.get(category)

    def hasItem(self, shopItem: ShopItem, **kwargs):
        return shopItem in self.getAllItems(**kwargs)

    ### Item Indexing ###

    def _indexAllItems(self, **kwargs) -> List[ShopItem]:
        """Indexes all items. Required for purchase validation."""
        # Generate all shop item listings.
        for shopItemListing in self.getAllItemListings(index=False):
            if shopItemListing.canGenerateItems():
                shopItemListing.generateItems(**kwargs)

        # Get all items in order.
        allItems = [shopItem
                    for shopItemListing in self.getAllItemListings(index=False)
                    for shopItem in shopItemListing.getDecompressedItems(**kwargs)]

        # Set item IDs.
        for index, shopItem in enumerate(allItems):
            shopItem.setInternalItemIndex(index)

        # Return them.
        return allItems

    def getItemFromIndex(self, index: int, **kwargs) -> Optional[ShopItem]:
        """Returns an item from an index."""
        itemListing = self._indexAllItems(**kwargs)
        if not (0 <= index < len(itemListing)):
            # SOMEHOW an invalid index was passed in.
            # This needs to be handled with care!!
            return None
        return itemListing[index]
