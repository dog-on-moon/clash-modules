from typing import Union, Tuple
from toontown.shop.ShopEnums import ShopPriceTagType

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from toontown.toon.DistributedToonAI import DistributedToonAI


class ShopPriceTag:
    """
    A dataclass containing information about the cost of a shop item.
    """

    priceTagType = None  # type: ShopPriceTagType

    def __init__(self, cost: Union[int, float]):
        self.cost = cost

    def __repr__(self):
        return f"{self.cost} {self.priceTagType}"

    ### Getters ###

    def getCost(self) -> Union[int, float]:
        return self.cost

    def getPriceTagType(self) -> ShopPriceTagType:
        return self.priceTagType

    ### Checkers ###

    def canAfford(self, av) -> bool:
        """
        Determines if an avatar can afford this cost.
        :type av: DistributedToonAI
        """
        raise NotImplementedError

    def attemptPurchase(self, av) -> bool:
        """
        'Purchases' using the cost, removing the money from the avatar.
        :type av: DistributedToonAI
        """
        raise NotImplementedError


# Make typehint for ShopPriceTag.
# On built, these types will not exist, so we will
# handle the exception with a simplification.
try:
    PriceTags = Union[ShopPriceTag, Tuple[ShopPriceTag]]
except NameError:
    PriceTags = ShopPriceTag
