"""
This module contains the item data for cheesy effects.
"""
from panda3d.core import NodePath

from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.base.ItemDefinition import ItemDefinition
from typing import Dict, Optional
from enum import IntEnum

from toontown.inventory.enums.ItemEnums import CheesyEffectItemType


class CheesyEffectDefinition(ItemDefinition):
    """
    The definition structure for cheesy effects.
    """
    def __init__(self,
                 **kwargs):
        super().__init__(**kwargs)

    def getItemTypeName(self):
        return 'Cheesy Effect'

    def getRewardName(self, item: Optional[InventoryItem] = None):
        return f'{self.getName()} Cheesy Effect'


# The registry dictionary for cheesy effects.
CheesyEffectRegistry: Dict[IntEnum, CheesyEffectDefinition] = {
    ### Default ###
    CheesyEffectItemType.BigHead: CheesyEffectDefinition(
        name='Big Head',
        description='Todo!',
    ),
    CheesyEffectItemType.SmallHead: CheesyEffectDefinition(
        name='Small Head',
        description='Todo!',
    ),
    CheesyEffectItemType.BigLegs: CheesyEffectDefinition(
        name='Big Legs',
        description='Todo!',
    ),
    CheesyEffectItemType.SmallLegs: CheesyEffectDefinition(
        name='Small Legs',
        description='Todo!',
    ),
    CheesyEffectItemType.BigToon: CheesyEffectDefinition(
        name='Big Toon',
        description='Todo!',
    ),
    CheesyEffectItemType.SmallToon: CheesyEffectDefinition(
        name='Small Toon',
        description='Todo!',
    ),
    CheesyEffectItemType.FlatPortrait: CheesyEffectDefinition(
        name='Flat Portrait',
        description='Todo!',
    ),
    CheesyEffectItemType.FlatProfile: CheesyEffectDefinition(
        name='Flat Profile',
        description='Todo!',
    ),
    CheesyEffectItemType.Transparent: CheesyEffectDefinition(
        name='Transparent',
        description='Todo!',
    ),
    CheesyEffectItemType.NoColor: CheesyEffectDefinition(
        name='NoColor',
        description='Todo!',
    ),
    CheesyEffectItemType.Invisible: CheesyEffectDefinition(
        name='Invisible',
        description='Todo!',
    ),
    CheesyEffectItemType.Pumpkin: CheesyEffectDefinition(
        name='Pumpkin',
        description='Todo!',
    ),
    CheesyEffectItemType.BigWhite: CheesyEffectDefinition(
        name='Polar',
        description='Todo!',
    ),
    CheesyEffectItemType.SnowMan: CheesyEffectDefinition(
        name='Snowman',
        description='Todo!',
    ),
    CheesyEffectItemType.GreenToon: CheesyEffectDefinition(
        name='Green Toon',
        description='Todo!',
    ),
    CheesyEffectItemType.PumpkinPale: CheesyEffectDefinition(
        name='Pumpkin Head: 2018',
        description='Todo!',
    ),
    CheesyEffectItemType.PumpkinPurple: CheesyEffectDefinition(
        name='Pumpkin Head: Pumpkin Behind the Carving',
        description='Todo!',
    ),
    CheesyEffectItemType.PumpkinFlare: CheesyEffectDefinition(
        name='Pumpkin Head: \'Flared Up Hollows\' by Tally',
        description='Todo!',
    ),
    CheesyEffectItemType.PumpkinScapegoat: CheesyEffectDefinition(
        name='Pumpkin Head: Scapegourd',
        description='Todo!',
    ),
    CheesyEffectItemType.Spirit: CheesyEffectDefinition(
        name='Spirit',
        description='Todo!',
    ),
    CheesyEffectItemType.Stomped: CheesyEffectDefinition(
        name='Stomped',
        description='Todo!',
    ),
    CheesyEffectItemType.Wireframe: CheesyEffectDefinition(
        name='Wireframe',
        description='Todo!',
    ),
    CheesyEffectItemType.Backwards: CheesyEffectDefinition(
        name='Backwards',
        description='Todo!',
    ),
    CheesyEffectItemType.Amogus: CheesyEffectDefinition(
        name='No Arms',
        description='Todo!',
    ),
    CheesyEffectItemType.Fired: CheesyEffectDefinition(
        name='No Arms',
        description='Todo!',
    ),
}

