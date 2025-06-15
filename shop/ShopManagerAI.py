from toontown.shop.base.ShopItem import ShopItem
from toontown.shop.base.ShopItemCatalogue import ShopItemCatalogue


from typing import TYPE_CHECKING, Optional

from toontown.toon.DistributedToonAI import DistributedToonAI

if TYPE_CHECKING:
    from toontown.ai.ToontownAIRepository import ToontownAIRepository


class ShopManagerAI:
    """
    An AI-sided class used to provide a helpful interface for
    purchasing various kinds of ShopItems.
    """

    def __init__(self, air, itemCatalogue: ShopItemCatalogue):
        self.air = air  # type: ToontownAIRepository
        self.itemCatalogue = itemCatalogue

    def requestItemPurchase(self, shopItemStruct: int):
        """
        Sent from an avatar.
        Requests an item to be purchased.
        """
        # Validate the av.
        avId = self.air.getAvatarIdFromSender()
        av: Optional[DistributedToonAI] = self.air.doId2do.get(avId, None)
        if av is None:
            return

        # Get the shop item.
        accessKwargs = self.getItemAccessKwargs(av)
        shopItem = ShopItem.fromStruct(shopItemStruct, self.itemCatalogue, **accessKwargs)

        # Is this shop item in the item catalogue?
        if shopItem is None or not self.itemCatalogue.hasItem(shopItem, **accessKwargs):
            # The item catalogue is missing this item.
            self.callbackItemMissing(shopItem=shopItem, av=av)
            return False

        # Any subclasses add special purchase checks?
        if not self.performAdditionalPurchaseChecks(shopItem=shopItem, av=av):
            # Additional purchase checks have failed.
            self.callbackAdditionalChecksFailed(shopItem=shopItem, av=av)
            return False

        # Can the avatar afford the item?
        if not shopItem.canAfford(av):
            # The avatar cannot afford this item.
            self.callbackAvatarCannotAfford(shopItem=shopItem, av=av)
            return False

        # Are there any other purchase checks preventing?
        if not shopItem.canPurchase(av):
            # The avatar cannot purchase the item.
            self.callbackAvatarCannotPurchase(shopItem=shopItem, av=av)
            return False

        # Attempt to grant the item.
        if shopItem.attemptPurchase(av):
            # The item was purchased successfully. Grant the item.
            returnValue = shopItem.grantItem(av)
            self.callbackPurchaseSuccessful(shopItem=shopItem, av=av, returnValue=returnValue)
            return True
        else:
            # The item could not be purchased, even still.
            self.callbackPurchaseAttemptFailed(shopItem=shopItem, av=av)
            return False

    def getItemAccessKwargs(self, av) -> dict:
        """Gets the item access kwargs."""
        return {}

    def performAdditionalPurchaseChecks(self, shopItem: ShopItem, av: DistributedToonAI) -> bool:
        """
        Subclasses can add additional purchase checks to perform here.
        :return: True if successful, False otherwise.
        """
        return True

    ### Callbacks ###

    def sendPurchaseNotification(self, av: DistributedToonAI):
        self.sendUpdateToAvatarId(av.doId, 'onItemPurchase', [])

    def callbackPurchaseSuccessful(self, shopItem: ShopItem, av: DistributedToonAI, returnValue=None):
        """Callback when purchasing an item was successful!"""
        self.sendPurchaseNotification(av)

    def callbackItemMissing(self, shopItem: Optional[ShopItem], av: DistributedToonAI):
        """Callback sent when the item is missing from our item catalogue"""
        self.sendPurchaseNotification(av)

    def callbackAvatarCannotAfford(self, shopItem: ShopItem, av: DistributedToonAI):
        """Callback sent when the avatar is too poor"""
        self.sendPurchaseNotification(av)

    def callbackAvatarCannotPurchase(self, shopItem: ShopItem, av: DistributedToonAI):
        """Callback sent when the avatar cannot purchase for some reason"""
        self.sendPurchaseNotification(av)

    def callbackAdditionalChecksFailed(self, shopItem: ShopItem, av: DistributedToonAI):
        """Callback sent when the shop manager purchase checks fail"""
        self.sendPurchaseNotification(av)

    def callbackPurchaseAttemptFailed(self, shopItem: ShopItem, av: DistributedToonAI):
        """Callback sent when, despite everything, the act of purchasing fails"""
        self.sendPurchaseNotification(av)
