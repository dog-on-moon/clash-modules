from typing import Optional

from direct.distributed.DistributedObject import DistributedObject

from toontown.inventory.base.Inventory import Inventory
from toontown.inventory.base.InventoryDelta import InventoryDelta
from toontown.inventory.base.InventoryExceptions import InventoryActionFailure
from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.utils.AstronDict import AstronDict


class DistributedInventory(DistributedObject):
    """
    A non-persistent Inventory that players can interact with.

    Unlike typical DO pattern, the inventory must be manually requested from the client.
    The server must also manually control access to the inventory as well.
    """

    def __init__(self, cr):
        super().__init__(cr)

        self.inventory: Inventory | None = None
        self.avIdAccess: dict[str, tuple[bool, bool]] | AstronDict = AstronDict()
        self._callbacks = []

    def delete(self):
        del self.inventory
        del self.avIdAccess
        del self._callbacks
        super().delete()

    """
    Interface
    """

    def getInventory(self) -> Inventory | None:
        """
        Gets the inventory.
        Note that this does not request a server update if the inventory is not present.
        In that case, you may want to be using DistributedInventory.requestInventory instead.
        """
        if not self.canLocalView():
            return None
        return self.inventory

    def hasInventory(self) -> bool:
        """
        This checks to see if we even have the inventory.
        If this returns False, may wanna call requestInventory.
        """
        if not self.getInventory():
            return False
        return True

    def requestInventory(self, callback: Optional[callable] = None) -> bool:
        """
        Requests to get the inventory.
        Returns False if access is denied.

        If the inventory is available, calls the callback IMMEDIATELY w/ inventory.
        If not, waits for the server to update us, then does the callback DEFERRED w/ inventory.
        """
        if not self.canLocalView():
            return False

        # See if we have the inventory to give back right now.
        inventory = self.getInventory()
        if inventory:
            if callback:
                callback(inventory)
            return True

        # Request the inventory from the server.
        if callback:
            self._callbacks.append(callback)
        self.sendUpdate('CL_AI_requestInventory')
        return True

    def requestAddItem(self, item: InventoryItem) -> bool:
        """
        Requests to remove a local item and add it to the inventory.
        Returns False if any local checks pass, True if we've made it to server request.
        """
        if self.hasInventory():
            localInventory: Inventory = self.cr.inventoryManager.getInventory()
            if not localInventory:
                return False

            if not localInventory.canSwapItemTo(self.getInventory(), item):
                return False

            # The delta is acceptable.
            self.sendUpdate('CL_AI_requestAddItem', [item.toStruct()])
            return True
        else:
            return self.requestInventory(lambda _: self.requestAddItem(item))

    def requestTakeItem(self, item: InventoryItem) -> bool:
        """
        Requests to remove an item and add it to our player inventory.
        Returns False if any local checks pass, True if we've made it to server request.
        """
        if self.hasInventory():
            localInventory: Inventory = self.cr.inventoryManager.getInventory()
            if not localInventory:
                return False

            if not self.getInventory().canSwapItemTo(localInventory, item):
                return False

            # The delta is acceptable.
            self.sendUpdate('CL_AI_requestTakeItem', [item.toStruct()])
            return True
        else:
            return self.requestInventory(lambda _: self.requestTakeItem(item))

    def requestDeleteItem(self, item: InventoryItem) -> bool:
        """
        Requests for an item to be deleted from the inventory.
        Returns False if any local checks pass, True if we've made it to server request.
        """
        if self.hasInventory():
            if not self.getInventory().canRemoveItem(item, manualDelete=True):
                return False

            # The delta is acceptable.
            self.sendUpdate('CL_AI_requestDeleteItem', [item.toStruct()])
            return True
        else:
            return self.requestInventory(lambda _: self.requestDeleteItem(item))

    def getInventoryUpdateName(self):
        return self.uniqueName('update')

    """
    Client/server synchronization
    """

    def AI_CL_updateInventory(self, inventory: list):
        """The server has sent us a new inventory."""
        self.inventory = Inventory.fromStruct(inventory)
        for callback in self._callbacks:
            callback(self.inventory)
        self._callbacks = []
        self._sendInventoryUpdate()

    def AI_CL_retrieveDeltas(self, deltas: list, invHash: int):
        """Gets inventory deltas from the server."""
        if not self.canLocalView():
            return

        # Ignore this request if we don't have an inventory.
        inventory = self.getInventory()
        if not inventory:
            return

        # Attempt applying all deltas.
        deltas: list[InventoryDelta] = InventoryDelta.fromStructList(deltas)
        for delta in deltas:
            try:
                inventory.applyDelta(delta)
            except InventoryActionFailure:
                # This delta failed to apply, so ask for a new inventory.
                self._resetInventory()
                self.requestInventory()
                return

        # Do a hash check.
        if hash(inventory) != invHash:
            # Hash is invalid, deltas updated wrong?
            self._resetInventory()
            self.requestInventory()
        else:
            # Successful inventory update.
            self._sendInventoryUpdate()

    """
    Internal inventory management
    """

    def _resetInventory(self):
        """Resets the inventory, requiring a new server request."""
        self.inventory = None

    def _sendInventoryUpdate(self):
        messenger.send(self.getInventoryUpdateName(), [self.getInventory()])

    """
    Avatar access management
    """

    def canLocalView(self) -> bool:
        """Determines if the local avatar can view the inventory."""
        return self.canView(base.localAvatar.doId)

    def canLocalUse(self) -> bool:
        """Determines if the local avatar can interact with the inventory."""
        return self.canUse(base.localAvatar.doId)

    def canView(self, avId: int) -> bool:
        """Determines if this avatar can view the inventory."""
        return str(avId) in self.getAccess() and self.getAccess()[str(avId)][0]

    def canUse(self, avId: int) -> bool:
        """Determines if this avatar can interact with the inventory."""
        return str(avId) in self.getAccess() and self.getAccess()[str(avId)][1]

    def getViewAvIds(self) -> list[int]:
        """Returns all avIds that can view the inventory."""
        return [int(avId) for avId in self.getAccess().keys()
                if self.getAccess()[avId][0]]

    def getUseAvIds(self) -> list[int]:
        """Returns all avIds that can use the inventory."""
        return [int(avId) for avId in self.getAccess().keys()
                if self.getAccess()[avId][0]]

    def setAccess(self, access: list):
        oldAccess = self.getAccess().get(str(base.localAvatar.doId))
        self.avIdAccess = AstronDict.fromStruct(access)
        newAccess = self.getAccess().get(str(base.localAvatar.doId))
        if oldAccess != newAccess:
            self._callbacks = []
            self._sendInventoryUpdate()

    def getAccess(self) -> dict[str, tuple[bool, bool]]:
        return self.avIdAccess
