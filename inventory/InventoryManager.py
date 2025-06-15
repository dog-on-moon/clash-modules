import time
from typing import Optional, List

from direct.distributed.DistributedObject import DistributedObject

from toontown.inventory.base.Inventory import Inventory
from toontown.inventory.base.InventoryDelta import InventoryDelta
from toontown.inventory.base.InventoryExceptions import InventoryActionFailure
from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.enums import ItemEnums
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory


@DirectNotifyCategory()
class InventoryManager(DistributedObject):
    """
    The client-side view of the InventoryManager.

    This class receives the local Toon's current inventory.
    """
    neverDisable = 1

    def __init__(self, cr):
        super().__init__(cr)

        # Initialize local state.
        self.inventory: Optional[Inventory] = None
        self.tempInventory: Optional[Inventory] = None

    def announceGenerate(self):
        super().announceGenerate()
        if self.cr.inventoryManager:
            self.cr.inventoryManager.delete()
        self.cr.inventoryManager = self
        self.notify.info(f'Generated.')

    def delete(self):
        super().delete()
        self.cr.inventoryManager = None

    """
    Client Inventory State Management
    """

    def sendInventoryDelta(self, deltas: list, inventoryHash: int):
        """
        Receives inventory deltas from the server.
        """
        # self.notify.info(f'Receiving deltas: {deltas}')
        deltas: List[InventoryDelta] = InventoryDelta.fromStructList(deltas)
        for delta in deltas:
            try:
                self.inventory.applyDelta(delta)
            except InventoryActionFailure:
                # This delta failed to apply -- just ask for a new inventory
                self.notify.warning(f'Received inventory has invalid delta -- just ask for new inventory')
                self.askInventoryUpdate()
                return
            else:
                messenger.send('inventoryDelta', [delta])
                messenger.send(InventoryDelta.getItemDeltaEvent(delta.item.getItemType()), [delta])

        # Do a hash check.
        if hash(self.inventory) != inventoryHash:
            # Hash is invalid, deltas updated wrong?
            self.notify.warning(f'Inventory hash out of date ({round(time.time() % 1000, 3)})! Asking for update...')
            self.askInventoryUpdate()
        else:
            # Hash is fine, treat it as valid
            messenger.send('newLocalInventory', [self.inventory])

    def askInventoryUpdate(self):
        """Asks the server for an inventory update."""
        self.sendUpdate('askInventoryUpdate')

    def setAvatarInventory(self, inventory, items, segment, segmentCount):
        """
        Receives inventory data from the server.
        """
        # Initial segment, build inventory.
        if segment == 1:
            self.tempInventory = Inventory.fromStruct(inventory)

        # Populate items.
        self.tempInventory.getItems().extend(InventoryItem.fromStructList(items))

        # Final segment, complete call
        if segment == segmentCount:
            self.inventory = self.tempInventory
            self.inventory.setOwner(base.localAvatar)
            self.inventory.updateCache()
            self.tempInventory = None
            self.notify.info(f'Received local inventory: {inventory}')
            messenger.send('LocalInventorySet')
            messenger.send('newLocalInventory', [self.inventory])
            for value in [enum for enum in ItemEnums.ItemType]:
                messenger.send(InventoryDelta.getItemDeltaEvent(value), [None])

    """
    Debug Protocols
    """

    def debug_applyLocalDelta(self, inventoryDelta: InventoryDelta):
        """
        Sends a local delta out to the server, to force apply to our
        own inventory. Only works on dev, ofc.
        """
        self.sendUpdate('debug_applyLocalDelta', [inventoryDelta.toStruct()])

    """
    Getters
    """

    def getInventory(self) -> Optional[Inventory]:
        return self.inventory
