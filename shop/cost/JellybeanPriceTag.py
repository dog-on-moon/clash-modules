from toontown.shop.base.ShopPriceTag import ShopPriceTag


class JellybeanPriceTag(ShopPriceTag):
    """
    The jellybean price tag.
    """

    def __repr__(self):
        return f'{self.getCost()} jbs'

    def canAfford(self, av) -> bool:
        return av.getTotalMoney() >= self.getCost()

    def attemptPurchase(self, av) -> bool:
        return av.takeMoney(self.getCost())
