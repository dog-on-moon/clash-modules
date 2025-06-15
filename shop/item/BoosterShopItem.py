import datetime
from toontown.booster import BoosterGlobals
from toontown.inventory.enums.ItemEnums import BoosterItemType
from toontown.inventory.registry.ItemTypeRegistry import getItemDefinition
from toontown.shop.base.ShopItem import ShopItem
from toontown.shop.base.ShopPriceTag import PriceTags
from toontown.toonbase import TTLocalizer

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from toontown.toon.DistributedToonAI import DistributedToonAI


class BoosterShopItem(ShopItem):

    def __init__(self, boosterType: BoosterItemType, hours: int,
                 desc: str, priceTags: PriceTags, includeSuper: bool = True):
        super().__init__(priceTags)
        self.boosterType = boosterType
        self.hours = hours
        self.includeSuper = includeSuper
        try:
            self.desc = desc % hours
        except TypeError:
            raise TypeError("Description for BoosterShopItem must have a %s for hour formatting.")

    def grantItem(self, av):
        boosterType = self.getBoosterType()
        isRandomBooster = boosterType == BoosterItemType.randomBooster
        if isRandomBooster:
            boosterType = BoosterGlobals.getReasonableBooster(av=av, includeSuper=self.includeSuper)
        av.addNewBooster(
            boosterType=boosterType,
            timeDelta=self.getTimeDelta(),
        )

        if isRandomBooster:
            return boosterType

    def getName(self) -> str:
        return getItemDefinition(self.getBoosterType()).getName()

    def getDescription(self) -> str:
        return self.desc

    def getBoosterType(self) -> BoosterItemType:
        return self.boosterType

    def getTimeDelta(self) -> datetime.timedelta:
        return datetime.timedelta(hours=self.hours)

    def hasTooLongBooster(self, av) -> bool:
        """:type av: DistributedToonAI"""
        avatarBooster = av.getBoosterOfType(self.getBoosterType())
        if avatarBooster is None:
            return False
        return avatarBooster.durationExtendsPastMax()

    def canPurchase(self, av) -> bool:
        return super().canPurchase(av) \
               and not self.hasTooLongBooster(av)
