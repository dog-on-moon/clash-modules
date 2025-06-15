"""
This module contains the item data for glasses.
"""
from panda3d.core import NodePath

from toontown.inventory.base.InventoryItem import InventoryItem
from typing import Dict, Optional
from enum import IntEnum, auto

from toontown.inventory.definitions.AccessoryDefinition import AccessoryDefinition
from toontown.inventory.enums.ItemEnums import GlassesItemType
from toontown.inventory.enums.ItemTags import ItemTag
from toontown.toon.accessories.ToonActorAccessory import ToonActorAccessory
from toontown.toon.accessories.glasses.AnimatedHypno import AnimatedHypno
from toontown.toon.accessories.glasses.GlassesHideEyes import GlassesHideEyes
from toontown.toon.accessories.glasses.GlassesHideLashes import GlassesHideLashes
from toontown.toon.accessories.glasses.ScifiGlasses import ScifiGlasses


class GlassesClassEnum(IntEnum):
    Default = auto()
    GlassesHideEyes = auto()
    GlassesHideLashes = auto()
    AnimatedHypno = auto()
    ScifiGlasses = auto()


baseTexturePath = "cosmetics/maps/"
baseModelPath = "cosmetics/models/"
textureExtension = ".png"


class GlassesItemDefinition(AccessoryDefinition):
    """
    The definition structure for glasses.
    """

    GlassesClasses = {
        GlassesClassEnum.GlassesHideEyes: GlassesHideEyes,
        GlassesClassEnum.GlassesHideLashes: GlassesHideLashes,
        GlassesClassEnum.AnimatedHypno: AnimatedHypno,
        GlassesClassEnum.ScifiGlasses: ScifiGlasses,
    }

    def __init__(self,
                 modelName,
                 textureName=None,
                 accessoryClass=GlassesClassEnum.Default,
                 accFileType=('face', 'face'),  # cc_t_acc_XXX_
                 accFilePath=('face', 'face'),  # cosmetics/maps/XXX
                 **kwargs):
        super().__init__(**kwargs)
        self.modelName = modelName
        self.textureName = textureName
        self.accessoryClass = accessoryClass

        modelType = "a" if issubclass(self.getAccessoryClass(), ToonActorAccessory) else "m"

        mdlFileType, texFileType = accFileType
        mdlFilePath, texFilePath = accFilePath

        self.baseModelPrefix = f"cc_{modelType}_acc_{mdlFileType}_"
        self.baseTexturePrefix = f"cc_t_acc_{texFileType}_"
        self.texturePath = f"{baseTexturePath}{texFilePath}/"
        self.modelPath = f"{baseModelPath}{mdlFilePath}/"

    def getItemTypeName(self):
        return 'Glasses'

    def getRewardName(self, item: Optional[InventoryItem] = None):
        return f'{self.getName()} Glasses'

    def getModelPath(self):
        if not self.modelName:
            return None
        return f"{self.modelPath}{self.baseModelPrefix}{self.modelName}"

    def getTexturePath(self):
        if not self.textureName:
            return None
        return f"{self.texturePath}{self.baseTexturePrefix}{self.textureName}{textureExtension}"

    def getAccessoryClass(self):
        return self.GlassesClasses.get(self.accessoryClass, super().getAccessoryClass())

    def getTags(self, item: 'InventoryItem') -> set[ItemTag]:
        tags = super().getTags(item)
        tags.add(ItemTag.Glasses)
        return tags


# The registry dictionary for glasses.
GlassesRegistry: Dict[IntEnum, GlassesItemDefinition] = {
    GlassesItemType.RoundGlasses: GlassesItemDefinition(
        name="Round Glasses",
        description='Todo!',
        modelName='gl_round_classic',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.WhiteMiniBlinds: GlassesItemDefinition(
        name="White Mini Blinds",
        description='Todo!',
        modelName='gl_miniblinds_classic',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.HollywoodShades: GlassesItemDefinition(
        name="Hollywood Shades",
        description='Even the Cogs admit, this one looks good.',
        modelName='gl_narrow_classic',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.StarGlasses: GlassesItemDefinition(
        name="Yellow Star Glasses",
        description='Todo!',
        modelName='gl_star_classic',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.MovieGlasses: GlassesItemDefinition(
        name="Movie Glasses",
        description='Todo!',
        modelName='gl_3d_classic',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.AviatorGlasses: GlassesItemDefinition(
        name="Aviator",
        description='Sky Clan, here we come!',
        modelName='gl_aviator_classic',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.CelebShades: GlassesItemDefinition(
        name="Celebrity Shades",
        description='Todo!',
        modelName='gl_jackieo_classic',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.ScubaMask: GlassesItemDefinition(
        name="Scuba Mask",
        description='Todo!',
        modelName='gl_goggles_scuba_classic',
        textureName=None,
        accessoryClass=GlassesClassEnum.GlassesHideEyes
    ),
    GlassesItemType.Goggles: GlassesItemDefinition(
        name="Goggles",
        description='Todo!',
        modelName='gl_goggles_classic',
        textureName=None,
        accessoryClass=GlassesClassEnum.GlassesHideLashes
    ),
    GlassesItemType.GrouchoGlasses: GlassesItemDefinition(
        name="Groucho Glasses",
        description='Todo!',
        modelName='gl_groucho_classic',
        textureName=None,
        accessoryClass=GlassesClassEnum.GlassesHideLashes
    ),
    GlassesItemType.HeartGlasses: GlassesItemDefinition(
        name="Heart Glasses",
        description='Todo!',
        modelName='gl_heart_classic',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.BugeyeGlasses: GlassesItemDefinition(
        name="Bug Eye Glasses",
        description='Todo!',
        modelName='gl_insect_classic',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.STMaskBlack: GlassesItemDefinition(
        name="Black Super Toon Mask",
        description='Todo!',
        modelName='msk_ident_classic',
        textureName='msk_ident_classic_black',
        accessoryClass=GlassesClassEnum.GlassesHideLashes
    ),
    GlassesItemType.STMaskBlue: GlassesItemDefinition(
        name="Blue Super Toon Mask",
        description='Todo!',
        modelName='msk_ident_classic',
        textureName='msk_ident_classic_blue',
        accessoryClass=GlassesClassEnum.GlassesHideLashes
    ),
    GlassesItemType.CarnivaleMaskBlue: GlassesItemDefinition(
        name="Blue Carnivale Mask",
        description='Todo!',
        modelName='msk_carnival_classic',
        textureName='msk_carnival_classic_blue',
        accessoryClass=GlassesClassEnum.GlassesHideLashes
    ),
    GlassesItemType.CarnivaleMaskPurple: GlassesItemDefinition(
        name="Purple Carnivale Mask",
        description='Todo!',
        modelName='msk_carnival_classic',
        textureName='msk_carnival_classic_purple',
        accessoryClass=GlassesClassEnum.GlassesHideLashes
    ),
    GlassesItemType.CarnivaleMaskAqua: GlassesItemDefinition(
        name="Aqua Carnivale Mask",
        description='Todo!',
        modelName='msk_carnival_classic',
        textureName='msk_carnival_classic_green',
        accessoryClass=GlassesClassEnum.GlassesHideLashes
    ),
    GlassesItemType.Monocle: GlassesItemDefinition(
        name="Monocle",
        description='Todo!',
        modelName='gl_monocle_classic',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.SmoochGlasses: GlassesItemDefinition(
        name="Smooch Glasses",
        description='Todo!',
        modelName='gl_mouth_classic',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.SquareFrames: GlassesItemDefinition(
        name="Square Frame Glasses",
        description='Todo!',
        modelName='gl_square_classic',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.CateyeGlasses: GlassesItemDefinition(
        name="Cateye Glasses",
        description='Todo!',
        modelName='gl_cateye_classic',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.NerdGlasses: GlassesItemDefinition(
        name="Nerd Glasses",
        description='Todo!',
        modelName='gl_dork_classic',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.AlienEyes: GlassesItemDefinition(
        name="Alien Eyes",
        description='Todo!',
        modelName='gl_alien_classic',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.EyepatchSkull: GlassesItemDefinition(
        name="Skull Eyepatch",
        description='Todo!',
        modelName='gl_eyepatch_classic',
        textureName='gl_eyepatch_classic_skull',
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.EyepatchGem: GlassesItemDefinition(
        name="Gem Eyepatch",
        description='Todo!',
        modelName='gl_eyepatch_classic',
        textureName='gl_eyepatch_classic_gem',
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.EyepatchLimey: GlassesItemDefinition(
        name="Limey's Eyepatch",
        description='Todo!',
        modelName='gl_eyepatch_classic',
        textureName='gl_eyepatch_classic_gem',
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.SpiderGlasses: GlassesItemDefinition(
        name="Spider Glasses",
        description='Todo!',
        modelName='msk_spider',
        textureName=None,
        accessoryClass=GlassesClassEnum.GlassesHideLashes
    ),
    GlassesItemType.Hypno: GlassesItemDefinition(
        name="Hypno Glasses 2018",
        description='Todo!',
        modelName='gl_hypno',
        textureName='gl_hypno_zany',
        accessoryClass=GlassesClassEnum.AnimatedHypno
    ),
    GlassesItemType.SnowGogglesBlue: GlassesItemDefinition(
        name="Blue Snow Goggles",
        description='Todo!',
        modelName='gl_goggles_ski',
        textureName='gl_goggles_ski_blue',
        accessoryClass=GlassesClassEnum.GlassesHideEyes
    ),
    GlassesItemType.SnowGogglesGreen: GlassesItemDefinition(
        name="Green Snow Goggles",
        description='Todo!',
        modelName='gl_goggles_ski',
        textureName='gl_goggles_ski_green',
        accessoryClass=GlassesClassEnum.GlassesHideEyes
    ),
    GlassesItemType.SnowGogglesGrey: GlassesItemDefinition(
        name="Grey Snow Goggles",
        description='Todo!',
        modelName='gl_goggles_ski',
        textureName='gl_goggles_ski_gray',
        accessoryClass=GlassesClassEnum.GlassesHideEyes
    ),
    GlassesItemType.SnowGogglesPink: GlassesItemDefinition(
        name="Pink Snow Goggles",
        description='Todo!',
        modelName='gl_goggles_ski',
        textureName='gl_goggles_ski_pink',
        accessoryClass=GlassesClassEnum.GlassesHideEyes
    ),
    GlassesItemType.SnowGogglesRainbow: GlassesItemDefinition(
        name="Rainbow Snow Goggles",
        description='Todo!',
        modelName='gl_goggles_ski',
        textureName='gl_goggles_ski_rainbow',
        accessoryClass=GlassesClassEnum.GlassesHideEyes
    ),
    GlassesItemType.SnowGogglesRed: GlassesItemDefinition(
        name="Red Snow Goggles",
        description='Todo!',
        modelName='gl_goggles_ski',
        textureName='gl_goggles_ski_red',
        accessoryClass=GlassesClassEnum.GlassesHideEyes
    ),
    GlassesItemType.SnowGogglesVintage: GlassesItemDefinition(
        name="Vintage Snow Goggles",
        description='Todo!',
        modelName='gl_goggles_ski',
        textureName='gl_goggles_ski_vintage',
        accessoryClass=GlassesClassEnum.GlassesHideEyes
    ),
    GlassesItemType.Glasses2019: GlassesItemDefinition(
        name="2019 Glasses",
        description='Todo!',
        modelName='gl_nye_2019',
        textureName=None,
        accessoryClass=GlassesClassEnum.GlassesHideLashes
    ),
    GlassesItemType.FlunkyGlasses: GlassesItemDefinition(
        name="Flunky Glasses",
        description='Smells like morning cogfee.',
        modelName='gl_flunky',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.EyeSpring: GlassesItemDefinition(
        name="Eye Spring Glasses",
        description='Perfect prescription.',
        modelName='gl_eyespring',
        textureName=None,
        accessoryClass=GlassesClassEnum.GlassesHideLashes
    ),
    GlassesItemType.FlightGoggles: GlassesItemDefinition(
        name="Flight Goggles",
        description='Sky Clan, here we come!',
        modelName='gl_goggles_flight',
        textureName=None,
        accessoryClass=GlassesClassEnum.GlassesHideLashes
    ),
    GlassesItemType.OutbackSunnyglasses: GlassesItemDefinition(
        name="Outback Sunnyglasses",
        description='Let that sun shine!',
        modelName='gl_sunny',
        textureName=None,
        accessoryClass=GlassesClassEnum.GlassesHideLashes
    ),
    GlassesItemType.Hypno2019: GlassesItemDefinition(
        name="Hypno Glasses 2019",
        description='oOoOoOoOh... You want to buy these glasses...',
        modelName='gl_hypno',
        textureName='gl_hypno_green',
        accessoryClass=GlassesClassEnum.AnimatedHypno
    ),
    GlassesItemType.XGlassesB: GlassesItemDefinition(
        name="Black Sad Glasses",
        description='You might be sad, but at least you\'re stylish!',
        modelName='gl_x',
        textureName='gl_x_black',
        accessoryClass=GlassesClassEnum.GlassesHideLashes
    ),
    GlassesItemType.XGlassesGo: GlassesItemDefinition(
        name="Gold Sad Glasses",
        description='You might be sad, but at least you\'re stylish!',
        modelName='gl_x',
        textureName='gl_x_gold',
        accessoryClass=GlassesClassEnum.GlassesHideLashes
    ),
    GlassesItemType.XGlassesGr: GlassesItemDefinition(
        name="Green Sad Glasses",
        description='You might be sad, but at least you\'re stylish!',
        modelName='gl_x',
        textureName='gl_x_green',
        accessoryClass=GlassesClassEnum.GlassesHideLashes
    ),
    GlassesItemType.XGlassesRa: GlassesItemDefinition(
        name="Rainbow Sad Glasses",
        description='You might be sad, but at least you\'re stylish!',
        modelName='gl_x',
        textureName='gl_x_rainbow',
        accessoryClass=GlassesClassEnum.GlassesHideLashes
    ),
    GlassesItemType.XGlassesRed: GlassesItemDefinition(
        name="Red Sad Glasses",
        description='You might be sad, but at least you\'re stylish!',
        modelName='gl_x',
        textureName='gl_x_red',
        accessoryClass=GlassesClassEnum.GlassesHideLashes
    ),
    GlassesItemType.GiftGlasses: GlassesItemDefinition(
        name="Gift Glasses",
        description='Todo!',
        modelName='gl_gift',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.GiftGlassesBlue: GlassesItemDefinition(
        name="Blue Gift Glasses",
        description='Todo!',
        modelName='gl_gift',
        textureName='gl_gift_blue',
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.GiftGlassesCyan: GlassesItemDefinition(
        name="Cyan Gift Glasses",
        description='Todo!',
        modelName='gl_gift',
        textureName='gl_gift_cyan',
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.GiftGlassesGreen: GlassesItemDefinition(
        name="Green Gift Glasses",
        description='Todo!',
        modelName='gl_gift',
        textureName='gl_gift_green',
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.GiftGlassesOrange: GlassesItemDefinition(
        name="Orange Gift Glasses",
        description='Todo!',
        modelName='gl_gift',
        textureName='gl_gift_orange',
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.GiftGlassesPink: GlassesItemDefinition(
        name="Pink Gift Glasses",
        description='Todo!',
        modelName='gl_gift',
        textureName='gl_gift_pink',
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.GiftGlassesPurple: GlassesItemDefinition(
        name="Purple Gift Glasses",
        description='Todo!',
        modelName='gl_gift',
        textureName='gl_gift_purple',
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.GiftGlassesRed: GlassesItemDefinition(
        name="Red Gift Glasses",
        description='Todo!',
        modelName='gl_gift',
        textureName='gl_gift_red',
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.GiftGlassesYellow: GlassesItemDefinition(
        name="Yellow Gift Glasses",
        description='Todo!',
        modelName='gl_gift',
        textureName='gl_gift_yellow',
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.Glasses2020: GlassesItemDefinition(
        name="2020 New Year's Glasses",
        description='Todo!',
        modelName='gl_nye_2020',
        textureName=None,
        accessoryClass=GlassesClassEnum.GlassesHideLashes
    ),
    GlassesItemType.SevenGlasses: GlassesItemDefinition(
        name="Red Hypno Glasses",
        description='oOoOoOoOh... You want to buy these glasses...',
        modelName='gl_hypno',
        textureName='gl_hypno_red_7',
        accessoryClass=GlassesClassEnum.AnimatedHypno
    ),
    GlassesItemType.VinnyStache: GlassesItemDefinition(
        name="Vinny's Facial Hair",
        description='Todo!',
        modelName='mustache_vinny',
        textureName=None,
        accessoryClass=GlassesClassEnum.GlassesHideEyes
    ),
    GlassesItemType.ChairGlasses: GlassesItemDefinition(
        name="Chairman Glasses",
        description='Todo!',
        modelName='gl_chairman',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.HypnoBlue: GlassesItemDefinition(
        name="Blue Hypno",
        description='oOoOoOoOh... You want to buy these glasses...',
        modelName='gl_hypno',
        textureName='gl_hypno_blue',
        accessoryClass=GlassesClassEnum.AnimatedHypno
    ),
    GlassesItemType.HypnoLightblue: GlassesItemDefinition(
        name="Light-Blue Hypno",
        description='oOoOoOoOh... You want to buy these glasses...',
        modelName='gl_hypno',
        textureName='gl_hypno_cyan',
        accessoryClass=GlassesClassEnum.AnimatedHypno
    ),
    GlassesItemType.HypnoOrange: GlassesItemDefinition(
        name="Orange Hypno",
        description='oOoOoOoOh... You want to buy these glasses...',
        modelName='gl_hypno',
        textureName='gl_hypno_orange',
        accessoryClass=GlassesClassEnum.AnimatedHypno
    ),
    GlassesItemType.HypnoPink: GlassesItemDefinition(
        name="Pink Hypno",
        description='oOoOoOoOh... You want to buy these glasses...',
        modelName='gl_hypno',
        textureName='gl_hypno_pink',
        accessoryClass=GlassesClassEnum.AnimatedHypno
    ),
    GlassesItemType.HypnoYellow: GlassesItemDefinition(
        name="Yellow Hypno",
        description='oOoOoOoOh... You want to buy these glasses...',
        modelName='gl_hypno',
        textureName='gl_hypno_yellow',
        accessoryClass=GlassesClassEnum.AnimatedHypno
    ),
    GlassesItemType.HypnoPurple: GlassesItemDefinition(
        name="Purple Hypno",
        description='oOoOoOoOh... You want to buy these glasses...',
        modelName='gl_hypno',
        textureName='gl_hypno_pink',
        accessoryClass=GlassesClassEnum.AnimatedHypno
    ),
    GlassesItemType.HypnoDarkpurple: GlassesItemDefinition(
        name="Dark-Purple Hypno",
        description='oOoOoOoOh... You want to buy these glasses...',
        modelName='gl_hypno',
        textureName='gl_hypno_purple',
        accessoryClass=GlassesClassEnum.AnimatedHypno
    ),
    GlassesItemType.HypnoRainbow: GlassesItemDefinition(
        name="Rainbow Hypno",
        description='oOoOoOoOh... You want to buy these glasses...',
        modelName='gl_hypno',
        textureName='gl_hypno_rainbow',
        accessoryClass=GlassesClassEnum.AnimatedHypno
    ),
    GlassesItemType.OrnGlassesBlack: GlassesItemDefinition(
        name="Black Ornament",
        description='Todo!',
        modelName='gl_ornament',
        textureName='gl_orn_black',
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.OrnGlassesBlue: GlassesItemDefinition(
        name="Blue Ornament",
        description='Todo!',
        modelName='gl_ornament',
        textureName='gl_orn_blue',
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.OrnGlassesCyan: GlassesItemDefinition(
        name="Cyan Ornament",
        description='Todo!',
        modelName='gl_ornament',
        textureName='gl_orn_cyan',
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.OrnGlassesGreen: GlassesItemDefinition(
        name="Green Ornament",
        description='Todo!',
        modelName='gl_ornament',
        textureName='gl_orn_green',
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.OrnGlassesOrange: GlassesItemDefinition(
        name="Orange Ornament",
        description='Todo!',
        modelName='gl_ornament',
        textureName='gl_orn_orange',
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.OrnGlassesPink: GlassesItemDefinition(
        name="Pink Ornament",
        description='Todo!',
        modelName='gl_ornament',
        textureName='gl_orn_pink',
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.OrnGlassesPurple: GlassesItemDefinition(
        name="Purple Ornament",
        description='Todo!',
        modelName='gl_ornament',
        textureName='gl_orn_purple',
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.OrnGlassesRainbow: GlassesItemDefinition(
        name="Rainbow Ornament",
        description='Todo!',
        modelName='gl_ornament',
        textureName='gl_orn_rainbow',
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.OrnGlassesRed: GlassesItemDefinition(
        name="Red Ornament",
        description='Todo!',
        modelName='gl_ornament',
        textureName='gl_orn_red',
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.OrnGlassesWhite: GlassesItemDefinition(
        name="White Ornament",
        description='Todo!',
        modelName='gl_ornament',
        textureName='gl_orn_white',
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.OrnGlassesYellow: GlassesItemDefinition(
        name="Yellow Ornament",
        description='Todo!',
        modelName='gl_ornament',
        textureName='gl_orn_yellow',
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.HwtownMask: GlassesItemDefinition(
        name="Hallowopolis Mask",
        description='Todo!',
        modelName='msk_hwtown',
        textureName=None,
        accessoryClass=GlassesClassEnum.GlassesHideLashes
    ),
    GlassesItemType.CountMask: GlassesItemDefinition(
        name="Count Mask",
        description='Todo!',
        modelName='msk_count',
        textureName=None,
        accessoryClass=GlassesClassEnum.GlassesHideLashes
    ),
    GlassesItemType.Glasses2022: GlassesItemDefinition(
        name="2022 Glasses",
        description='Todo!',
        modelName='gl_nye_2020',
        textureName=None,
        accessoryClass=GlassesClassEnum.GlassesHideLashes
    ),
    GlassesItemType.ScifiVisor: GlassesItemDefinition(
        name="Space-Age Visor",
        description='Todo!',
        modelName='gl_visor_scifi',
        textureName=None,
        accessoryClass=GlassesClassEnum.ScifiGlasses
    ),
    GlassesItemType.BrovinciGlasses: GlassesItemDefinition(
        name="Bro's Glasses",
        description='Todo!',
        modelName='gl_bro',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.GlassesMouthpiece: GlassesItemDefinition(
        name="Mouthpiece's Glasses",
        description='Todo!',
        modelName='gl_mouthpiece',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.GlassesFunky: GlassesItemDefinition(
        name="Retro Glasses",
        description='Friday night fever!',
        modelName='gl_funky',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.DdlSleepingmask: GlassesItemDefinition(
        name="Sleepwalker Mask",
        description='Sleep tight!',
        modelName='msk_sleepy',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.GlassesPacesetter: GlassesItemDefinition(
        name="Pacesetter's Glasses",
        description='Todo!',
        modelName='gl_pacesetter',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.GlassesCardblack: GlassesItemDefinition(
        name="Card Suit Glasses",
        description="Don't tap on the glass.",
        modelName='gl_card_black',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.GlassesCardred: GlassesItemDefinition(
        name="Card Suit Glasses",
        description="Don't tap on the glass.",
        modelName='gl_card_red',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.CookieGlasses: GlassesItemDefinition(
        name="Cookie Glasses",
        description='Don\'t get all dough-eyed on me!',
        modelName='gl_cookie',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.LowBallerGlasses: GlassesItemDefinition(
        name="Low Baller Glasses",
        description='Todo!',
        modelName='gl_lowball',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
    GlassesItemType.CyberpunkGlasses: GlassesItemDefinition(
        name="Cyberpunk Glasses",
        description='Todo!',
        modelName='gl_visor_cyber',
        textureName=None,
        accessoryClass=GlassesClassEnum.Default
    ),
}
