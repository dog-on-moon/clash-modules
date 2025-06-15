"""
This module contains the item data for nametag fonts.
"""
from panda3d.core import NodePath

from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.base.ItemDefinition import ItemDefinition
from typing import Dict, Optional
from enum import IntEnum

from toontown.inventory.enums.ItemAttribute import ItemAttribute
from toontown.inventory.enums.ItemEnums import NametagFontItemType
from toontown.toonbase import ToontownGlobals


baseFontPath = "core/fonts/"
fontExtension = ".ttf"


class NametagFontDefinition(ItemDefinition):
    """
    The definition structure for nametag fonts.
    """

    def __init__(self,
                 fontName,
                 **kwargs):
        super().__init__(**kwargs)
        self.fontName = fontName

    def getFontPath(self):
        if not self.fontName:
            return None
        return f"{baseFontPath}{self.fontName}{fontExtension}"

    def getItemTypeName(self):
        return 'Nametag Font'

    def getRewardName(self, item: Optional[InventoryItem] = None):
        return f'{self.getName()} Nametag Font'

    def getTextRenderItemName(self, item: Optional[InventoryItem] = None):
        return self.getName()

    def getTextRenderFont(self, item: Optional[InventoryItem] = None):
        if item:
            return ToontownGlobals.getNametagFont(item.getItemSubtype())
        return ToontownGlobals.getInterfaceFont()

    def getGuiItemModel(self, item: Optional[InventoryItem] = None, *args, **kwargs) -> NodePath:
        """
        Returns a nodepath that is to be used in 2D space.
        """
        return super().getGuiItemModel(item=item, useModel=self.renderTextForGuiModel(item), *args, **kwargs)


# The registry dictionary for nametag fonts.
NametagFontRegistry: Dict[IntEnum, NametagFontDefinition] = {
    ### Default ###
    NametagFontItemType.Basic: NametagFontDefinition(
        name='Basic',
        description='The default style for your nametag.',
        fontName='ImpressBT',
    ),

    NametagFontItemType.Plain: NametagFontDefinition(
        name='Plain',
        description='TODO!',
        fontName='AnimGothic',
    ),

    NametagFontItemType.Shivering: NametagFontDefinition(
        name='Shivering',
        description='TODO!',
        fontName='Aftershock',
    ),

    NametagFontItemType.Wonky: NametagFontDefinition(
        name='Wonky',
        description='TODO!',
        fontName='JiggeryPokery',
    ),

    NametagFontItemType.Fancy: NametagFontDefinition(
        name='Fancy',
        description='TODO!',
        fontName='Ironwork',
    ),

    NametagFontItemType.Silly: NametagFontDefinition(
        name='Silly',
        description='TODO!',
        fontName='HastyPudding',
    ),

    NametagFontItemType.Zany: NametagFontDefinition(
        name='Zany',
        description='TODO!',
        fontName='Comedy',
    ),

    NametagFontItemType.Practical: NametagFontDefinition(
        name='Practical',
        description='TODO!',
        fontName='Humanist',
    ),

    NametagFontItemType.Nautical: NametagFontDefinition(
        name='Nautical',
        description='TODO!',
        fontName='Portago',
    ),

    NametagFontItemType.Whimsical: NametagFontDefinition(
        name='Whimsical',
        description='TODO!',
        fontName='Musicals',
    ),

    NametagFontItemType.Spooky: NametagFontDefinition(
        name='Spooky',
        description='TODO!',
        fontName='Scurlock',
    ),

    NametagFontItemType.Action: NametagFontDefinition(
        name='Action',
        description='TODO!',
        fontName='Danger',
    ),
    NametagFontItemType.Poetic: NametagFontDefinition(
        name='Poetic',
        description='TODO!',
        fontName='Alie',
    ),
    NametagFontItemType.Boardwalk: NametagFontDefinition(
        name='Boardwalk',
        description='TODO!',
        fontName='OysterBar',
    ),
    NametagFontItemType.Western: NametagFontDefinition(
        name='Western',
        description='TODO!',
        fontName='RedDogSaloon',
    ),
    NametagFontItemType.Abstract: NametagFontDefinition(
        name='Abstract',
        description='TODO!',
        fontName='Humanist',
    ),

    ### Kudos Fonts ###
    NametagFontItemType.IceCream: NametagFontDefinition(
        name='Ice Cream',
        description='TODO!',
        fontName='Bocah',
    ),
    NametagFontItemType.Pirate: NametagFontDefinition(
        name='Pirate',
        description='TODO!',
        fontName='Chelsea',
    ),
    NametagFontItemType.Medieval: NametagFontDefinition(
        name='Medieval',
        description='TODO!',
        fontName='Enchanted_Land',
    ),
    NametagFontItemType.Calligraphy: NametagFontDefinition(
        name='Calligraphy',
        description='TODO!',
        fontName='KaushanScript',
    ),
    NametagFontItemType.Playful: NametagFontDefinition(
        name='Playful',
        description='TODO!',
        fontName='Mabook',
    ),
    NametagFontItemType.Comical: NametagFontDefinition(
        name='Comical',
        description='TODO!',
        fontName='Qdbettercomicsans',
    ),
    NametagFontItemType.Arrogant: NametagFontDefinition(
        name='Arrogant',
        description='TODO!',
        fontName='Phattype',
    ),
    NametagFontItemType.Cinema: NametagFontDefinition(
        name='Cinema',
        description='TODO!',
        fontName='BettyNoir',
    ),
}


# Fill in ToontownGlobals with all of the fonts for these nametags
# This is for compatibility purposes with previous implementations of nametag styles
for itemEnum, itemDefinition in NametagFontRegistry.items():
    ToontownGlobals.setNametagFont(itemEnum, itemDefinition.getFontPath())
