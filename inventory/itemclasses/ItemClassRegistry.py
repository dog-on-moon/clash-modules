from typing import Dict, Type

from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.enums.ItemEnums import ItemType


ItemClassRegistry: Dict[ItemType, Type[InventoryItem]] = {}
