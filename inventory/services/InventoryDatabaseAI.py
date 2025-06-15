from direct.showbase.DirectObject import DirectObject

from toontown.inventory.base import DefaultInventory
from toontown.inventory.base.Inventory import Inventory

from typing import TYPE_CHECKING, Optional
from pymongo.collection import Collection

from toontown.toonbase import RealmGlobals

if TYPE_CHECKING:
    from toontown.ai.ToontownAIRepository import ToontownAIRepository


class InventoryDatabaseAI(DirectObject):
    """
    Provides an interface for direct query & interfaces for Toon inventories.
    Uses a cache local to the district for inventories, though
    subclasses may implement their own DB interface.
    """

    AUTOSAVE_DURATION = 30

    def __init__(self, air):
        """:type air: ToontownAIRepository"""
        self.air = air  # type: ToontownAIRepository
        self.inventoryCache = {}

    """
    Inventory Saving
    """

    def startInventorySaving(self, avId: int):
        """
        Starts a task to save inventory changes to DB.
        """
        self.doMethodLater(
            delayTime=self.AUTOSAVE_DURATION,
            funcOrTask=self.__inventorySaveTask,
            name=self.inventorySaveTaskName(avId),
            extraArgs=[avId],
        )

    def endInventorySaving(self, avId: int, inventory: Inventory):
        """
        Ends inventory auto-saving.
        """
        self.__doInventorySave(avId, inventory)
        self.removeTask(self.inventorySaveTaskName(avId))

    def __inventorySaveTask(self, avId: int):
        # Get the av.
        av = self.air.doId2do.get(avId, None)
        if av is None:
            # The av is gone -- end the task.
            return

        # Find the av's inventory.
        inventory = self.air.inventoryManager.getInventory(avId)
        if not inventory:
            return

        # Has the av hammerspace updated recently?
        if inventory.cache.getTimeSinceModified() < self.AUTOSAVE_DURATION:
            self.__doInventorySave(avId, inventory)

        # Re-do the task.
        self.startInventorySaving(avId)

    def __doInventorySave(self, avId: int, inventory: Inventory):
        self.saveInventory(avId, inventory)

    @staticmethod
    def inventorySaveTaskName(avId: int):
        return f'InventoryDatabaseAI-Autosave-{avId}'

    """
    Inventory Interface
    """

    def queryInventory(self, avId: int, create: bool = False) -> Optional[Inventory]:
        """
        Queries for an avatar's inventory.
        """
        if avId not in self.inventoryCache:
            if create:
                return self.makeInventory(avId, force=True)
            else:
                return None
        return self.inventoryCache.get(avId)

    def saveInventory(self, avId: int, inventory: Inventory) -> None:
        """
        Saves an avatar's inventory.
        """
        self.inventoryCache[avId] = inventory

    def makeInventory(self, avId: int, force: bool = False) -> Inventory:
        """
        Creates an avatar's default inventory.
        """
        if not force and avId in self.inventoryCache:
            raise AttributeError

        # Make default inventory.
        inventory = DefaultInventory.getDefaultInventory()
        self.inventoryCache[avId] = inventory
        return inventory


class InventoryMongoDatabaseAI(InventoryDatabaseAI):
    """
    Provides an interface for direct query & interfaces for Toon inventories.
    Interfaces with MongoDB.
    """
    DEV_RESET_ON_LOGIN = False

    def __init__(self, air):
        """:type air: ToontownAIRepository"""
        super().__init__(air)
        self.collection: Collection = self.air.mongodb.inventory

    def queryInventory(self, avId: int, create: bool = False) -> Optional[Inventory]:
        """
        Queries for an avatar's inventory.
        """
        if RealmGlobals.getCurrentRealm() == RealmGlobals.Realm.Development and self.DEV_RESET_ON_LOGIN:
            return self.makeInventory(avId, force=True)

        inventoryJson = self.collection.find_one({'_id': avId})
        if not inventoryJson:
            # No document found ... what do we do?
            if create:
                # Force create an inventory.
                return self.makeInventory(avId, force=True)
            else:
                # Nope, return nothin'.
                return None

        # Return our inventory dict
        return Inventory.fromMongo(inventoryJson)

    def saveInventory(self, avId: int, inventory: Inventory) -> None:
        """
        Saves an avatar's inventory.
        """
        self.collection.update_one({'_id': avId}, {"$set": inventory.toMongo()})

    def makeInventory(self, avId: int, force: bool = False) -> Inventory:
        """
        Creates an avatar's default inventory.
        """
        inventoryJson = self.collection.find_one({'_id': avId})
        if inventoryJson:
            if not force:
                raise AttributeError("avId already has an inventory!")
            else:
                self.collection.delete_one({'_id': avId})

        # Make default inventory.
        inventory = DefaultInventory.getDefaultInventory()

        # Save it in DB.
        inventoryJson = inventory.toMongo()
        inventoryJson.update({'_id': avId})
        self.collection.insert_one(inventoryJson)

        # Return the inventory.
        return inventory
