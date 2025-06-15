from enum import IntEnum, auto

from toontown.utils import ColorHelper
from panda3d.core import TextPropertiesManager, TextProperties


class Rarity(IntEnum):
    """
    An enum class for indicating how rare something is.
    """

    Common    = 0
    Uncommon  = 1
    Rare      = 2
    VeryRare  = 3
    UltraRare = 4
    Legendary = 5
    Mythic    = 6

    Event   = 7


RarityColors = {
    Rarity.Common:    ColorHelper.hexToPCol('ffffff'),
    Rarity.Uncommon:  ColorHelper.hexToPCol('7BFF8D'),
    Rarity.Rare:      ColorHelper.hexToPCol('93F0FF'),
    Rarity.VeryRare:  ColorHelper.hexToPCol('EDB8FF'),
    Rarity.UltraRare: ColorHelper.hexToPCol('FF97A1'),
    Rarity.Legendary: ColorHelper.hexToPCol('FFF4AF'),
    Rarity.Mythic:    ColorHelper.hexToPCol('7C81FF'),
    Rarity.Event:     ColorHelper.hexToPCol('FFADF5'),
}


def getItemRarityColor(item) -> tuple:
    return RarityColors.get(item.getRarity())


RarityNames = {
    Rarity.Common:    'Common',
    Rarity.Uncommon:  'Uncommon',
    Rarity.Rare:      'Rare',
    Rarity.VeryRare:  'Very Rare',
    Rarity.UltraRare: 'Ultra Rare',
    Rarity.Legendary: 'Legendary',
    Rarity.Mythic:    'Mythic',
    Rarity.Event:     'Event',
}


def getItemRarityName(item) -> str:
    return RarityNames.get(item.getRarity())


"""
Rarity Functions
"""


def getRaritySteps(rarity: Rarity, x: int) -> Rarity:
    """Pushes the rarity up by X steps."""
    if Rarity.Common <= rarity <= Rarity.Mythic:
        if (rarity + x) < Rarity.Common:
            return Rarity.Common
        elif (rarity + x) > Rarity.Mythic:
            return Rarity.Mythic
        else:
            return Rarity(rarity + x)
    else:
        return rarity


"""
Text Properties
"""

tpm = TextPropertiesManager.getGlobalPtr()

for rarity in Rarity:
    rarityProperty = TextProperties()
    rarityProperty.setShadow(0.05, 0.05)
    rarityProperty.setTextColor(RarityColors[rarity])
    tpm.setProperties(f'ItemRarity_{rarity}', rarityProperty)


def getItemRarityNameWithColor(item) -> str:
    return f'\1ItemRarity_{item.getRarity()}\1{getItemRarityName(item)}\2'
