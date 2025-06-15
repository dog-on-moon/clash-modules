from direct.distributed.DistributedObjectAI import DistributedObjectAI

from toontown.inventory.base.Inventory import Inventory
from toontown.inventory.base.InventoryDelta import InventoryDelta
from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.utils.AstronDict import AstronDict
from toontown.utils.RateLimiter import IdRateLimiter


class DistributedInventoryAI(DistributedObjectAI):
    """
    A non-persistent Inventory that players can interact with.
    Avatar access must be configured manually -- see setAccess below.

    In addition, Inventory contents must be requested to view from the client.
    """

    def __init__(self, air, inventory: Inventory, cleanupInventory: bool = True):
        super().__init__(air)

        self.inventory: Inventory = inventory
        self.cleanupInventory: bool = cleanupInventory

        self.avIdAccess: dict[int, tuple[bool, bool]] | AstronDict = AstronDict()
        self.inventory.addDeltaCallback(self.onInventoryUpdate)

        self._actionRatelimit = IdRateLimiter(max_hits=8, period=1)
        self._queryRatelimit = IdRateLimiter(max_hits=2, period=1)

    def delete(self):
        super().delete()
        if self.cleanupInventory:
            self.inventory.cleanup()
        else:
            self.inventory.removeDeltaCallback(self.onInventoryUpdate)
        del self.inventory
        del self.avIdAccess

    """
    Player item requests
    """

    def CL_AI_requestAddItem(self, item: list) -> None:
        """
        A client has requested to remove one of their items,
        and add it to this inventory.
        """
        avId = self.air.getAvatarIdFromSender()
        if self._actionRatelimit.userBlocked(avId):
            return
        if not self.canUse(avId):
            return

        # Verify inventories.
        item = InventoryItem.fromStruct(item)
        playerInventory: Inventory = self.air.inventoryManager.getInventory(avId)
        if not playerInventory:
            return
        if not playerInventory.canSwapItemTo(self.inventory, item):
            return

        # Do action.
        playerInventory.swapItemTo(self.inventory, item)

    def CL_AI_requestTakeItem(self, item: list) -> None:
        """
        A client has requested to remove one of our items,
        and add it to their inventory.
        """
        avId = self.air.getAvatarIdFromSender()
        if self._actionRatelimit.userBlocked(avId):
            return
        if not self.canUse(avId):
            return

        # Verify inventories.
        item = InventoryItem.fromStruct(item)
        playerInventory: Inventory = self.air.inventoryManager.getInventory(avId)
        if not playerInventory:
            return
        if not self.inventory.canSwapItemTo(playerInventory, item):
            return

        # Do action.
        self.inventory.swapItemTo(playerInventory, item)

    def CL_AI_requestDeleteItem(self, item: list) -> None:
        """
        A client has requested for an item to be deleted from this container.
        """
        avId = self.air.getAvatarIdFromSender()
        if self._actionRatelimit.userBlocked(avId):
            return
        if not self.canUse(avId):
            return

        # Verify our inventory.
        item = InventoryItem.fromStruct(item)
        if not self.inventory.canRemoveItem(item, manualDelete=True):
            return

        # Do action.
        self.inventory.removeItem(item, manualDelete=True)

    """
    Client/server synchronization
    """

    def CL_AI_requestInventory(self):
        """A client is requesting to view the inventory."""
        avId = self.air.getAvatarIdFromSender()
        if self._queryRatelimit.userBlocked(avId):
            return
        if not self.canView(avId):
            return
        self.sendUpdateToAvatarId(avId, 'AI_CL_updateInventory', [self.inventory.toStruct()])

    def onInventoryUpdate(self, inventory: Inventory, deltas: list[InventoryDelta]):
        """The inventory has new deltas to be parsed."""
        viewAvIds = self.getViewAvIds()
        if not viewAvIds:
            return

        deltas = InventoryDelta.toStructList(deltas)
        invHash = hash(inventory)

        for avId in viewAvIds:
            self.sendUpdateToAvatarId(
                avId=avId,
                fieldName='AI_CL_retrieveDeltas',
                args=[deltas, invHash]
            )

    """
    Avatar access management
    """

    def setAccess(self, avId: int, canView: bool, canUse: bool):
        """
        Sets access level for an avatar.
        - canView: The inventory is distributed to their client, and they can view its contents.
        - canUse: They are allowed to send inventory deltas to the server.
        """
        if canUse and not canView:
            raise KeyError("They can't use it if they can't SEE IT... BOZO!!!!!!")

        if avId in self.avIdAccess and self.avIdAccess[avId] == (canView, canUse):
            return

        self.avIdAccess[avId] = (canView, canUse)
        self.d_setAccess()

    def clearAccess(self, avId: int):
        """
        Clears access level for an avatar,
        preventing them from engaging with the inventory.
        """
        if avId not in self.avIdAccess:
            return

        del self.avIdAccess[avId]
        self.d_setAccess()

    def canView(self, avId: int) -> bool:
        """Determines if this avatar can view the inventory."""
        return avId in self.avIdAccess and self.avIdAccess[avId][0]

    def canUse(self, avId: int) -> bool:
        """Determines if this avatar can interact with the inventory."""
        return avId in self.avIdAccess and self.avIdAccess[avId][1]

    def getViewAvIds(self) -> list[int]:
        """Returns all avIds that can view the inventory."""
        return [avId for avId in self.avIdAccess.keys()
                if self.avIdAccess[avId][0]]

    def getUseAvIds(self) -> list[int]:
        """Returns all avIds that can use the inventory."""
        return [avId for avId in self.avIdAccess.keys()
                if self.avIdAccess[avId][0]]

    """
    Astron management
    """

    def d_setAccess(self):
        self.sendUpdate('setAccess', [self.avIdAccess.toStruct()])

    def getAccess(self) -> list:
        return self.avIdAccess.toStruct()

