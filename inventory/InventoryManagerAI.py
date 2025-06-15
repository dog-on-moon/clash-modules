from typing import Dict, Optional

from direct.distributed.DistributedObjectAI import DistributedObjectAI

from toontown.inventory.base.Inventory import Inventory
from toontown.inventory.base.InventoryDelta import InventoryDelta
from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.services.InventoryDatabaseAI import InventoryDatabaseAI
from toontown.toon.DistributedToonAI import DistributedToonAI
from toontown.toonbase import RealmGlobals
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.RateLimiter import IdRateLimiter


@DirectNotifyCategory()
class InventoryManagerAI(DistributedObjectAI):
    """
    This class functions as a data wrapper for Hammerspace inventories.
    """

    ITEM_SEGMENT_LENGTH = 50

    def __init__(self, air):
        super().__init__(air)

        # Hold the local state for all Toon inventories.
        self._avId2Inventory: Dict[int, Inventory] = {}

        # Ratelimiter
        self._ratelimiter = IdRateLimiter(max_hits=2, period=1)

        # Listen to useful calls.
        self.accept('avatarEntered', self.avatarEntered)
        self.accept('avatarExited', self.avatarExited)
        self.accept('avatarLoaded', self.avatarLoaded)

        self.notify.info('Generated.')

    """
    Event Hooks
    """

    def avatarEntered(self, av: DistributedToonAI):
        """
        Called when a Toon joins the district.
        """
        avId = av.getDoId()
        self.notify.info(f'Avatar {avId} has entered, doing inventory setup.')

        # First, get the inventory for this avatar.
        # We will create one if need be.
        inventory = self.inventoryDb.queryInventory(avId=avId, create=True)
        inventory.setOwner(av)
        inventory.addDeltaCallback(lambda inv, deltas: self.sendInventoryDelta(avId, inv, deltas))

        # Store this inventory in our cache.
        self._avId2Inventory[avId] = inventory

        # Ask our database interface to begin autosave operations on the inventory.
        self.inventoryDb.startInventorySaving(avId=avId)

        # Now, send this inventory to the avatar.
        self.askInventoryUpdate(avId=avId)

    def avatarExited(self, av: DistributedToonAI):
        """
        Called when a Toon leaves the district.
        """
        avId = av.getDoId()
        self.notify.info(f'Avatar {avId} has left, bye-bye!')

        if avId not in self._avId2Inventory:
            return

        # Get the final inventory.
        inventory = self._avId2Inventory[avId]

        # Clean up autosave.
        self.inventoryDb.endInventorySaving(avId=avId, inventory=inventory)

        # Cleanup.
        del self._avId2Inventory[avId]

    def avatarLoaded(self, av: DistributedToonAI):
        """
        Called when a Toon fully loads in on their client.
        """
        avId = av.getDoId()

        # Ensure the av exists.
        if avId not in self._avId2Inventory:
            self.notify.info(f'...but {avId} does not exist.')
            return

        # Get the inventory.
        inventory = self._avId2Inventory.get(avId)

        # Update this Toon with the inventory changes.
        self._setAvEquippedItems(avId=avId, inventory=inventory)

    """
    Inventory updates
    """

    def sendInventoryDelta(self, avId: int, inventory: Inventory, deltas: list[InventoryDelta]):
        """
        Takes the latest delta changes of an inventory
        and sends them to a client.
        """
        if not deltas:
            return

        # Set equipped items.
        self._setAvEquippedItems(avId, inventory)

        # General update with inventory delta send field.
        self.sendUpdateToAvatarId(
            avId=avId,
            fieldName='sendInventoryDelta',
            args=[InventoryDelta.toStructList(deltas), hash(inventory)]
        )

    """
    Client Inventory State Management
    """

    def askInventoryUpdate(self, avId: Optional[int] = None):
        """
        Requests for their local inventory to be updated/re-evaluated.
        Can either be sent from a client or called locally.
        """
        if avId is None:
            avId = self.air.getAvatarIdFromSender()
            if self._ratelimiter.userBlocked(avId):
                return
        if avId not in self._avId2Inventory:
            return

        # Get the inventory.
        inventory = self._avId2Inventory[avId]

        # Send the client their inventory state.
        self.setAvatarInventory(avId, inventory)

    def setAvatarInventory(self, avId: int, inventory: Inventory):
        """
        Sets the inventory to some Toon's client.
        """
        self.notify.info(f'Setting equipped items & inventory for {avId}...')
        self._setAvEquippedItems(avId=avId, inventory=inventory)

        # Split up this call into segments.
        baseInventory = inventory.makeItemless().toStruct()
        itemList = inventory.getItems()
        segmentCount = (len(itemList) // self.ITEM_SEGMENT_LENGTH) + 1
        for segment in range(segmentCount):
            itemSublist = itemList[self.ITEM_SEGMENT_LENGTH * segment:self.ITEM_SEGMENT_LENGTH * (segment + 1)]
            self.sendUpdateToAvatarId(avId, 'setAvatarInventory', [
                baseInventory,
                InventoryItem.toStructList(itemSublist),
                segment + 1,
                segmentCount
            ])

    def _setAvEquippedItems(self, avId: int, inventory: Inventory):
        """
        Updates an av to match an inventory.
        """
        av = self.air.doId2do.get(avId)
        if not av:
            return
        av.b_setEquippedItems(inventory.cache.getEquippedItems())

    """
    Debug Protocols
    """

    def debug_applyLocalDelta(self, inventoryDelta: list):
        """
        The Client can force a local delta change to their inventory.
        This ONLY works on dev realms.
        """
        avId = self.air.getAvatarIdFromSender()
        if RealmGlobals.getCurrentRealm() != RealmGlobals.Realm.Development:
            self.air.writeServerEvent(
                'suspicious', avId,
                "Toon ID trying to use a *very* obviously exploit-worthy protocol. "
                "Very likely someone poking around where they don't belong."
            )
            return

        # Figure out the delta, and apply it to the av inventory.
        inventoryDelta: InventoryDelta = InventoryDelta.fromStruct(inventoryDelta)
        inventory = self.getInventory(avId)
        self.notify.info(f'APPLYING DELTA: {repr(inventoryDelta)}')
        self.notify.info(f'INVENTORY (A): {repr(inventory)}')
        inventory.applyDelta(inventoryDelta)
        self.notify.info(f'INVENTORY (B): {repr(inventory)}')

    def debug_spawnTTCchest(self):
        """Spawns a chest in TTC."""
        avId = 100000063
        from toontown.inventory.distributed.DistributedInventoryAI import DistributedInventoryAI
        from toontown.inventory.enums.InventoryEnums import InventoryType
        inv = Inventory(InventoryType.FullBehavior)
        from toontown.inventory.enums.ItemEnums import HatItemType
        inv.addItem(HatItemType.CopHat)
        inv.addItem(HatItemType.TvHat)
        chest = DistributedInventoryAI(self.air, inv)
        chest.generateWithRequired(2000)
        chest.setAccess(avId, canView=True, canUse=True)

    """
    Getters
    """

    def getInventory(self, avId: int) -> Optional[Inventory]:
        return self._avId2Inventory.get(avId)

    """
    Properties
    """

    @property
    def inventoryDb(self) -> InventoryDatabaseAI:
        return self.air.inventoryDb
