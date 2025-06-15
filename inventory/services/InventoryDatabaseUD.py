from direct.showbase.DirectObject import DirectObject

from toontown.inventory.base import DefaultInventory
from toontown.inventory.base.Inventory import Inventory

from typing import TYPE_CHECKING, Optional
from pymongo.collection import Collection

if TYPE_CHECKING:
    from toontown.uberdog.ToontownUberRepository import ToontownUberRepository


class InventoryDatabaseUD(DirectObject):
    """
    A stripped down version of the AI inventory database for UD,
    which manages only inventory queries.
    """

    def __init__(self, udr):
        """:type udr: ToontownUberRepository"""
        self.udr = udr  # type: ToontownUberRepository
        self.collection: Collection = self.udr.mongodb.inventory
        self.defaultInventory = DefaultInventory.getDefaultInventory()

    def queryInventory(self, avId: int) -> Inventory:
        """
        Queries for an avatar's inventory.
        """
        inventoryJson = self.collection.find_one({'_id': avId})
        if not inventoryJson:
            # No document found, assume default.
            return self.defaultInventory

        # Return our inventory dict
        return Inventory.fromMongo(inventoryJson)
