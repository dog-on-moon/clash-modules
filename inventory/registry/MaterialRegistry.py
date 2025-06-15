"""
This module contains the item data for the different currencies of Toontown.
"""
from panda3d.core import NodePath

from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.base.ItemDefinition import ItemDefinition
from toontown.inventory.enums.ItemEnums import MaterialItemType
from typing import Dict, Optional
from enum import IntEnum


class CurrencyItemDefinition(ItemDefinition):
    """
    The definition structure for currency items.
    """

    def __init__(self,
                 textIcon='package',
                 wantPlural=True,
                 **kwargs):
        super().__init__(**kwargs)
        self.currTextIcon = textIcon
        self.wantPlural = wantPlural

    def getCurrencyTextIcon(self):
        return self.currTextIcon

    def getWantPlural(self):
        return self.wantPlural

    def getItemTypeName(self):
        return 'Currency'

    def getRewardName(self, item: Optional[InventoryItem] = None) -> str:
        return f"{item.getQuantity()} {self.getName(item)}{'s' if item.getQuantity() != 1 and self.getWantPlural() else ''}"

    def getGuiItemModel(self, item: Optional[InventoryItem] = None, *args, **kwargs) -> NodePath:
        """
        Returns a nodepath that is to be used in 2D space.
        """
        return super().getGuiItemModel(item=item, useModel=self.renderTextForGuiModel(item), *args, **kwargs)

    def getTextIcon(self, item: Optional[InventoryItem] = None) -> str:
        """
        Appears on:
        - Mini icons for quest reward text
        """
        return f'\1white\1\5reward_{self.getCurrencyTextIcon()}Icon\5\2'


# The registry dictionary for currencies.
MaterialRegistry: Dict[IntEnum, CurrencyItemDefinition] = {
    MaterialItemType.Jellybeans: CurrencyItemDefinition(
        name="Jellybean",
        description='The main currency of Toontown.',
        textIcon='beanJar',
    ),
    MaterialItemType.Gumballs: CurrencyItemDefinition(
        name="Gumball",
        description='Special currency that can be used in the Gumball Machine in all Toon Headquarters.',
        textIcon='gumball'
    ),
    MaterialItemType.Batcoin: CurrencyItemDefinition(
        name="Batcoin",
        description='Crypt-o-currency. Redeem at Hexadecimal for prizes!',
        wantPlural=False,
    ),
}
