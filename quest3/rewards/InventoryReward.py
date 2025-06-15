"""
Inventory item reward class for quests.
"""
from enum import IntEnum

from toontown.inventory.base.Inventory import Inventory
from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.registry import ItemTypeRegistry
from toontown.quest3.QuestEnums import QuesterType
from toontown.quest3.base.QuestReward import QuestReward
from toontown.quest3.base.Quester import Quester


class InventoryReward(QuestReward):
    # TODO - give this a better name some time ...

    def __init__(self, itemSubtype: IntEnum, quantity: int = 1, attributes: dict = None):
        if attributes is None:
            attributes = {}
        self.itemSubtype = itemSubtype
        self.quantity = quantity
        self.attributes = attributes

    def handleReward(self, quester: Quester, multiplier: float = 1.0) -> None:
        if quester.questerType == QuesterType.Toon:
            hs: Inventory = quester.getHammerspace()
            if hs:
                hs.addItem(InventoryItem.fromSubtype(
                    itemSubtype=self.itemSubtype,
                    quantity=self.quantity,
                    attributes=self.attributes
                ))

    def getRewardString(self, multiplier: float = 1.0) -> list:
        dummyItem = InventoryItem.fromSubtype(
            itemSubtype=self.itemSubtype,
            quantity=self.quantity,
            attributes=self.attributes
        )
        itemDef = dummyItem.getItemDefinition()
        return [f'{itemDef.getTextIcon(dummyItem)} '
                f'{itemDef.getRewardName(dummyItem)}']

    def __repr__(self):
        return f'InventoryReward(x{self.quantity} {self.itemSubtype})'
