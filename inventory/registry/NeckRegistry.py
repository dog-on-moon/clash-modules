"""
This module contains the item data for neck accessories (scarves, bowties, etc.).
"""
from toontown.inventory.base.InventoryItem import InventoryItem
from typing import Dict, Optional
from enum import IntEnum

from toontown.inventory.definitions.AccessoryDefinition import AccessoryDefinition
from toontown.inventory.enums.ItemEnums import NeckItemType
from toontown.inventory.enums.ItemTags import ItemTag
from toontown.toon.accessories.ToonActorAccessory import ToonActorAccessory


class NeckClassEnum(IntEnum):
    Default = 0


baseTexturePath = "cosmetics/maps/"
baseModelPath = "cosmetics/models/"
textureExtension = ".png"


class NeckItemDefinition(AccessoryDefinition):
    """
    The definition structure for neck accessories.
    """

    NeckClasses = {

    }

    def __init__(self,
                 modelName,
                 textureName=None,
                 accessoryClass=NeckClassEnum.Default,
                 accFileType=('nec', 'nec'),  # cc_t_acc_XXX_
                 accFilePath=('neck', 'neck'),  # cosmetics/maps/XXX
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
        return 'Scarf'

    def getRewardName(self, item: Optional[InventoryItem] = None):
        return f'{self.getName()} Scarf'

    def getModelPath(self):
        if not self.modelName:
            return None
        return f"{self.modelPath}{self.baseModelPrefix}{self.modelName}"

    def getTexturePath(self):
        if not self.textureName:
            return None
        return f"{self.texturePath}{self.baseTexturePrefix}{self.textureName}{textureExtension}"

    def getAccessoryClass(self):
        return super().getAccessoryClass()

    def getToonAttachNode(self) -> str:
        return '**/def_joint_attachFlower'

    def getTags(self, item: 'InventoryItem') -> set[ItemTag]:
        tags = super().getTags(item)
        tags.add(ItemTag.NeckAcc)
        return tags


# The registry dictionary for neck accessories.
NeckRegistry: Dict[IntEnum, NeckItemDefinition] = {
    NeckItemType.Scarf2019: NeckItemDefinition(
        name="2019 Scarf",
        description='Todo!',
        modelName='scarf_nye',
        textureName='scarf_nye_19',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.DoeBandana: NeckItemDefinition(
        name="Doe's Bandana",
        description='Todo!',
        modelName='bandana_doe',
        textureName=None,
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.AviatorScarf: NeckItemDefinition(
        name="Aviator Scarf",
        description='Sky Clan, here we come!',
        modelName='scarf_aviator',
        textureName=None,
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.PinwheelBowtie: NeckItemDefinition(
        name="Pinwheel Bowtie",
        description='Todo!',
        modelName='bowtie_pinwheel',
        textureName=None,
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.BloodsuckerLollipop: NeckItemDefinition(
        name="Bloodsucker Lollipop",
        description='Todo!',
        modelName='lollipop_bloodsucker',
        textureName=None,
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.CjTie: NeckItemDefinition(
        name="Chief Justice Bowtie",
        description='Todo!',
        modelName='bowtie_cj',
        textureName=None,
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.SailorCollarWhite: NeckItemDefinition(
        name="Sailor Collar",
        description='Todo!',
        modelName='collar_sailor_tie',
        textureName=None,
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.SailorCollarBlue: NeckItemDefinition(
        name="Blue Sailor Collar",
        description='Todo!',
        modelName='collar_sailor_tie',
        textureName='collar_sailor_tie_blue',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.SailorCollarCyan: NeckItemDefinition(
        name="Cyan Sailor Collar",
        description='Todo!',
        modelName='collar_sailor_tie',
        textureName='collar_sailor_tie_cyan',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.SailorCollarGreen: NeckItemDefinition(
        name="Green Sailor Collar",
        description='Todo!',
        modelName='collar_sailor_tie',
        textureName='collar_sailor_tie_green',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.SailorCollarOrange: NeckItemDefinition(
        name="Orange Sailor Collar",
        description='Todo!',
        modelName='collar_sailor_tie',
        textureName='collar_sailor_tie_orange',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.SailorCollarPink: NeckItemDefinition(
        name="Pink Sailor Collar",
        description='Todo!',
        modelName='collar_sailor_tie',
        textureName='collar_sailor_tie_pink',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.SailorCollarPurple: NeckItemDefinition(
        name="Purple Sailor Collar",
        description='Todo!',
        modelName='collar_sailor_tie',
        textureName='collar_sailor_tie_purple',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.SailorCollarRed: NeckItemDefinition(
        name="Red Sailor Collar",
        description='Todo!',
        modelName='collar_sailor_tie',
        textureName='collar_sailor_tie_red',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.SailorCollarBlack: NeckItemDefinition(
        name="Black Sailor Collar",
        description='Todo!',
        modelName='collar_sailor_tie',
        textureName='collar_sailor_tie_black',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.SailorCollarYellow: NeckItemDefinition(
        name="Golden Sailor Collar",
        description='Todo!',
        modelName='collar_sailor_tie',
        textureName='collar_sailor_tie_yellow',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.SailorBowWhite: NeckItemDefinition(
        name="Sailor Bow",
        description='Todo!',
        modelName='collar_sailor_bow',
        textureName=None,
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.SailorBowBlue: NeckItemDefinition(
        name="Blue Sailor Bow",
        description='Todo!',
        modelName='collar_sailor_bow',
        textureName='collar_sailor_bow_blue',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.SailorBowCyan: NeckItemDefinition(
        name="Cyan Sailor Bow",
        description='Todo!',
        modelName='collar_sailor_bow',
        textureName='collar_sailor_bow_cyan',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.SailorBowGreen: NeckItemDefinition(
        name="Green Sailor Bow",
        description='Todo!',
        modelName='collar_sailor_bow',
        textureName='collar_sailor_bow_green',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.SailorBowOrange: NeckItemDefinition(
        name="Orange Sailor Bow",
        description='Todo!',
        modelName='collar_sailor_bow',
        textureName='collar_sailor_bow_orange',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.SailorBowPink: NeckItemDefinition(
        name="Pink Sailor Bow",
        description='Todo!',
        modelName='collar_sailor_bow',
        textureName='collar_sailor_bow_pink',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.SailorBowPurple: NeckItemDefinition(
        name="Purple Sailor Bow",
        description='Todo!',
        modelName='collar_sailor_bow',
        textureName='collar_sailor_bow_purple',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.SailorBowRed: NeckItemDefinition(
        name="Red Sailor Bow",
        description='Todo!',
        modelName='collar_sailor_bow',
        textureName='collar_sailor_bow_red',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.SailorBowBlack: NeckItemDefinition(
        name="Black Sailor Bow",
        description='Todo!',
        modelName='collar_sailor_bow',
        textureName='collar_sailor_bow_black',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.SailorBowYellow: NeckItemDefinition(
        name="Golden Sailor Bow",
        description='Todo!',
        modelName='collar_sailor_bow',
        textureName='collar_sailor_bow_yellow',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.RetroScarf: NeckItemDefinition(
        name="Retro Winter Scarf",
        description='Todo!',
        modelName='scarf_retro',
        textureName=None,
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.Scarf2020: NeckItemDefinition(
        name="2020 Scarf",
        description='Todo!',
        modelName='scarf_nye',
        textureName='scarf_nye_20',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.FlowerTie: NeckItemDefinition(
        name="Squirt Flower Bowtie",
        description='Todo!',
        modelName='bowtie_gag_flower',
        textureName=None,
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.ClownBowtie: NeckItemDefinition(
        name="Clown Bowtie",
        description='Todo!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_polka_pink',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.JesterCollar: NeckItemDefinition(
        name="Jester Collar",
        description='Popularized in Ye Olde Toontowne!',
        modelName='collar_jester',
        textureName=None,
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.LawBowtie: NeckItemDefinition(
        name="Lawbot Suit Bowtie",
        description='Todo!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_col_red_lawbot',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.Scarf2021: NeckItemDefinition(
        name="2021 Scarf",
        description='Todo!',
        modelName='scarf_nye',
        textureName='scarf_nye_21',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.OttomanTie: NeckItemDefinition(
        name="Plant Tie",
        description='Todo!',
        modelName='tie_clipped',
        textureName=None,
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.EyeBowtie: NeckItemDefinition(
        name="Evil Eye Bowtie",
        description='Todo!',
        modelName='bowtie_eye',
        textureName=None,
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.MysteryBowtie: NeckItemDefinition(
        name="Detective Bowtie",
        description='Todo!',
        modelName='bowtie_small',
        textureName=None,
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.NewstoonBlueBowtie: NeckItemDefinition(
        name="Newstoon's Bowtie",
        description='Todo!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_striped_blue_white',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.Scarf2022: NeckItemDefinition(
        name="2022 Scarf",
        description='Todo!',
        modelName='scarf_nye',
        textureName='scarf_nye_22',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.RibbonBowtie: NeckItemDefinition(
        name="Ribbon Bowtie",
        description='Todo!',
        modelName='bowtie_classic',
        textureName=None,
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.RibbonBowtieRedpolka: NeckItemDefinition(
        name="Red Polka-Dot Bowtie",
        description='Todo!',
        modelName='bowtie_classic',
        textureName='bow_classic_polka_lg_red',
        accFileType = ('nec', 'hat'),
        accFilePath = ('neck', 'hat'),
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.RibbonBowtiePurple: NeckItemDefinition(
        name="Purple Bowtie",
        description='Todo!',
        modelName='bowtie_classic',
        textureName = 'bow_classic_polka_sm_purple',
        accFileType = ('nec', 'hat'),
        accFilePath = ('neck', 'hat'),
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.RibbonBowtieYellow: NeckItemDefinition(
        name="Yellow Bowtie",
        description='Todo!',
        modelName='bowtie_classic',
        textureName = 'bow_classic_col_yellow',
        accFileType = ('nec', 'hat'),
        accFilePath = ('neck', 'hat'),
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.RibbonBowtieBluechecker: NeckItemDefinition(
        name="Blue Checkered Bowtie",
        description='Todo!',
        modelName='bowtie_classic',
        textureName = 'bow_classic_checker_blue',
        accFileType = ('nec', 'hat'),
        accFilePath = ('neck', 'hat'),
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.RibbonBowtieRed: NeckItemDefinition(
        name="Red Bowtie",
        description='Todo!',
        modelName='bowtie_classic',
        textureName='bow_classic_polka_lg_red',
        accFileType = ('nec', 'hat'),
        accFilePath = ('neck', 'hat'),
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.RibbonBowtieRainbow: NeckItemDefinition(
        name="Rainbow Bowtie",
        description='Todo!',
        modelName='bowtie_classic',
        textureName = 'bow_classic_col_rainbow',
        accFileType = ('nec', 'hat'),
        accFilePath = ('neck', 'hat'),
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.RibbonBowtiePinkdots: NeckItemDefinition(
        name="Pink Dotted Bowtie",
        description='Todo!',
        modelName='bowtie_classic',
        textureName='bow_classic_polka_md_pink',
        accFileType=('nec', 'hat'),
        accFilePath=('neck', 'hat'),
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.RibbonBowtieGreenchecker: NeckItemDefinition(
        name="Green Checkered Bowtie",
        description='Todo!',
        modelName='bowtie_classic',
        textureName='bow_classic_checker_yellow',
        accFileType=('nec', 'hat'),
        accFilePath=('neck', 'hat'),
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.RibbonBowtieBlue: NeckItemDefinition(
        name="Blue Bowtie",
        description='Todo!',
        modelName='bowtie_classic',
        textureName='bow_classic_polka_sm_blue',
        accFileType = ('nec', 'hat'),
        accFilePath = ('neck', 'hat'),
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.RibbonBowtieCandycorn: NeckItemDefinition(
        name="Candy Corn Bowtie",
        description='Todo!',
        modelName='bowtie_classic',
        textureName='bow_classic_candycorn',
        accFileType=('nec', 'hat'),
        accFilePath=('neck', 'hat'),
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.RibbonBowtieBlack: NeckItemDefinition(
        name="Black Bowtie",
        description='Todo!',
        modelName='bowtie_classic',
        textureName='bow_classic_col_black',
        accFileType=('nec', 'hat'),
        accFilePath=('neck', 'hat'),
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.BrovinciNecklace: NeckItemDefinition(
        name="Bro's Necklace",
        description='Todo!',
        modelName='necklace_brovinci',
        textureName=None,
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.NeckCowbell: NeckItemDefinition(
        name="Cowbell",
        description='Todo!',
        modelName='cowbell',
        textureName=None,
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.GbBowtieBlack: NeckItemDefinition(
        name="Black Bowtie",
        description='Fashionable!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_col_black',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.GbBowtieBlackwhite: NeckItemDefinition(
        name="Zebrastripe Bowtie",
        description='Kinda tacky, but fashionable!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_striped_black_white',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.GbBowtieBlue: NeckItemDefinition(
        name="Blue Bowtie",
        description='Boldly blue!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_col_blue',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.GbBowtieGray: NeckItemDefinition(
        name="Gray Bowtie",
        description='Drab... still fashionable!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_col_gray',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.GbBowtieGreen: NeckItemDefinition(
        name="Green Bowtie",
        description='Mint condition!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_col_green',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.GbBowtieOrange: NeckItemDefinition(
        name="Orange Bowtie",
        description='Looks like sunshine! And fashion!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_col_orange',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.GbBowtiePink: NeckItemDefinition(
        name="Pink Bowtie",
        description='It\'s pink!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_col_pink',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.GbBowtiePinkblack: NeckItemDefinition(
        name="Radical Bowtie",
        description='Perfect for running!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_striped_pink_black',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.GbBowtiePolkadot: NeckItemDefinition(
        name="Polkadot Bowtie",
        description='Unpredictably wacky!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_polka_white',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.GbBowtiePurple: NeckItemDefinition(
        name="Grape Bowtie",
        description='Deceptively Sweet!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_col_purple',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.GbBowtiePurpleorange: NeckItemDefinition(
        name="PBJ Bowtie",
        description='Tasty, and fashionable!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_striped_purple_orange',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.GbBowtieRed: NeckItemDefinition(
        name="Red Bowtie",
        description='Regular red bowtie!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_col_red',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.GbBowtieYellow: NeckItemDefinition(
        name="Yellow Bowtie",
        description='Oh so bright! And fashionable!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_col_yellow',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.GbBowtieYellowblack: NeckItemDefinition(
        name="Stinging Bowtie",
        description='\1TextTitle\1Yeouch!\2',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_striped_yellow_black',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.EeChefscarf: NeckItemDefinition(
        name="Chef's Scarf",
        description='Todo!',
        modelName='scarf_chef',
        textureName=None,
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.BandanaEngineer: NeckItemDefinition(
        name="Trolley Engineer Bandana",
        description='All aboard!',
        modelName='bandana_handkerchief',
        textureName='bandana_handkerchief_red',
        accessoryClass=NeckClassEnum.Default
    ),
    NeckItemType.Scarf2023: NeckItemDefinition(
        name='2023 Scarf',
        description='Todo!',
        modelName='scarf_nye',
        textureName = 'scarf_nye_23',
    ),
    NeckItemType.OutbackBandana: NeckItemDefinition(
        name="Outback Bandana",
        description='Snug as a bug on a rug!',
        modelName='bandana_handkerchief',
        textureName=None,
    ),
    NeckItemType.PrideBowtieAce: NeckItemDefinition(
        name='Ace Pride Bowtie',
        description='Todo!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_pride_ace',
    ),
    NeckItemType.PrideBowtieAro: NeckItemDefinition(
        name='Aromantic Pride Bowtie',
        description='Todo!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_pride_aro',
    ),
    NeckItemType.PrideBowtieBi: NeckItemDefinition(
        name='Bi Pride Bowtie',
        description='Todo!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_pride_bi',
    ),
    NeckItemType.PrideBowtieGay: NeckItemDefinition(
        name='Gay Pride Bowtie',
        description='Todo!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_pride_gay',
    ),
    NeckItemType.PrideBowtieFluid: NeckItemDefinition(
        name='Genderfluid Pride Bowtie',
        description='Todo!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_pride_gfld',
    ),
    NeckItemType.PrideBowtieLesbian: NeckItemDefinition(
        name='Lesbian Pride Bowtie',
        description='Todo!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_pride_lsbn',
    ),
    NeckItemType.PrideBowtieLgbt: NeckItemDefinition(
        name='Pride Bowtie',
        description='Todo!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_pride_lgbt',
    ),
    NeckItemType.PrideBowtieNb: NeckItemDefinition(
        name='Non-Binary Pride Bowtie',
        description='Todo!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_pride_nb',
    ),
    NeckItemType.PrideBowtiePan: NeckItemDefinition(
        name='Pan Pride Bowtie',
        description='Todo!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_pride_pan',
    ),
    NeckItemType.PrideBowtieTrans: NeckItemDefinition(
        name='Trans Pride Bowtie',
        description='Todo!',
        modelName='bowtie_fancy',
        textureName='bowtie_fancy_pride_trans',
    ),
}
