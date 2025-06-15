from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.enums.InventoryEnums import InventoryAction
from toontown.utils.AstronStruct import AstronStruct


class InventoryDelta(AstronStruct):
    """
    An InventoryDelta reflects a singular action/change (delta)
    that occurs within an inventory. This class is useful
    for communicating the action of change (for net optimizations,
    or Elastic logging, or debugging) upon an inventory.
    """

    def __init__(self, action: InventoryAction, item: InventoryItem):
        self.action = action
        self.item = item

    def __repr__(self):
        return f'{self.action} -> {self.item}'

    def toStruct(self):
        return [int(self.getAction()), self.getItem().toStruct()]

    @classmethod
    def fromStruct(cls, struct):
        action, item = struct
        return cls(
            action=InventoryAction(action),
            item=InventoryItem.fromStruct(item),
        )

    def getAction(self) -> InventoryAction:
        return self.action

    def getItem(self) -> InventoryItem:
        return self.item

    @staticmethod
    def getItemDeltaEvent(itemEnum):
        return f'inventoryDelta-{itemEnum.name}'
