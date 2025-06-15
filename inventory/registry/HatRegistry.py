"""
This module contains the item data for hats.
"""
from panda3d.core import NodePath

from toontown.inventory.base.InventoryItem import InventoryItem
from typing import Dict, Optional
from enum import IntEnum, auto

from toontown.inventory.definitions.AccessoryDefinition import AccessoryDefinition
from toontown.inventory.enums.ItemEnums import HatItemType
from toontown.inventory.enums.ItemTags import ItemTag
from toontown.toon.accessories.ToonActorAccessory import ToonActorAccessory
from toontown.toon.accessories.hats.ChainsawConsultantHat import ChainsawConsultantHat
from toontown.toon.accessories.hats.ClashBirthday import ClashBirthdayHat
from toontown.toon.accessories.hats.GhostTophat import GhostTophat
from toontown.toon.accessories.hats.HatFreezeHead import HatFreezeHead
from toontown.toon.accessories.hats.HatHideEars import HatHideEars, OttomanNumberOnePlantHat, Beret
from toontown.toon.accessories.hats.HighRollerHat import HighRollerHat
from toontown.toon.accessories.hats.StormCloudHat import StormCloudHat


class HatClassEnum(IntEnum):
    Default = auto()
    HatHideEars = auto()
    ClashBirthdayHat = auto()
    GhostTophat = auto()
    OttomanNumberOnePlantHat = auto()
    HatFreezeHead = auto()
    ChainsawConsultantHat = auto()
    Beret = auto()
    StormCloudHat = auto()
    HighRollerHat = auto()


baseTexturePath = "cosmetics/maps/"
baseModelPath = "cosmetics/models/"
textureExtension = ".png"


class HatItemDefinition(AccessoryDefinition):
    """
    The definition structure for hats.
    """

    HatClasses = {
        HatClassEnum.HatHideEars: HatHideEars,
        HatClassEnum.ClashBirthdayHat: ClashBirthdayHat,
        HatClassEnum.GhostTophat: GhostTophat,
        HatClassEnum.OttomanNumberOnePlantHat: OttomanNumberOnePlantHat,
        HatClassEnum.HatFreezeHead: HatFreezeHead,
        HatClassEnum.ChainsawConsultantHat: ChainsawConsultantHat,
        HatClassEnum.Beret: Beret,
        HatClassEnum.StormCloudHat: StormCloudHat,
        HatClassEnum.HighRollerHat: HighRollerHat,
    }

    def __init__(self,
                 modelName,
                 textureName=None,
                 accessoryClass=HatClassEnum.Default,
                 accFileType=('hat', 'hat'),  # cc_t_acc_XXX_
                 accFilePath=('hat', 'hat'),  # cosmetics/maps/XXX
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
        return 'Head'

    def getModelPath(self):
        if not self.modelName:
            return None
        return f"{self.modelPath}{self.baseModelPrefix}{self.modelName}"

    def getTexturePath(self):
        if not self.textureName:
            return None
        return f"{self.texturePath}{self.baseTexturePrefix}{self.textureName}{textureExtension}"

    def getAccessoryClass(self):
        return self.HatClasses.get(self.accessoryClass, super().getAccessoryClass())

    def getTags(self, item: 'InventoryItem') -> set[ItemTag]:
        tags = super().getTags(item)
        tags.add(ItemTag.Hat)
        return tags


# The registry dictionary for hats.
HatRegistry: Dict[IntEnum, HatItemDefinition] = {
    HatItemType.GreenBallcap: HatItemDefinition(
        name="Green Baseball Cap",
        description='Todo!',
        modelName='baseball_classic',
        textureName='baseball_classic_green',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.SafariHatBeige: HatItemDefinition(
        name="Beige Safari Hat",
        description='Todo!',
        modelName='safari_classic',
        textureName='safari_classic_beige',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.SafariHatBrown: HatItemDefinition(
        name="Brown Safari Hat",
        description='Todo!',
        modelName='safari_classic',
        textureName='safari_classic_brown',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.SafariHatGreen: HatItemDefinition(
        name="Green Safari Hat",
        description='Todo!',
        modelName='safari_classic',
        textureName='safari_classic_green',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.PinkHearts: HatItemDefinition(
        name="Pink Heart",
        description='Todo!',
        modelName='headband_heart_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.YellowHearts: HatItemDefinition(
        name="Yellow Heart",
        description='Todo!',
        modelName='headband_heart_classic',
        textureName='headband_heart_classic_yellow',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.TophatBlack: HatItemDefinition(
        name="Black Top Hat",
        description='Todo!',
        modelName='tophat_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.TophatBlue: HatItemDefinition(
        name="Blue Top Hat",
        description='Todo!',
        modelName='tophat_classic',
        textureName='tophat_classic_blue_squares',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.AnvilHat: HatItemDefinition(
        name="Anvil Hat",
        description='Right out of the forges from Ye Olde Toontowne!',
        modelName='gag_anvil_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.FlowerHat: HatItemDefinition(
        name="Flower Hat",
        description='Todo!',
        modelName='gag_flowerpot_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.SandbagHat: HatItemDefinition(
        name="Sandbag Hat",
        description='Filled on the shores of Barnacle Boatyard!',
        modelName='gag_sandbag_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.WeightHat: HatItemDefinition(
        name="Weight Hat",
        description='A gift from Franz himself!',
        modelName='gag_weight_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.FezHat: HatItemDefinition(
        name="Fez Hat",
        description='Todo!',
        modelName='fez_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.GolfHat: HatItemDefinition(
        name="Golf Hat",
        description='Todo!',
        modelName='golf_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.PartyHat: HatItemDefinition(
        name="Party Hat",
        description='Todo!',
        modelName='party_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.PartyHatToon: HatItemDefinition(
        name="Toon Party Hat",
        description='Todo!',
        modelName='party_classic',
        textureName='party_classic_anniversary10',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.FancyHat: HatItemDefinition(
        name="Fancy Hat",
        description='Todo!',
        modelName='pillbox_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.Crown: HatItemDefinition(
        name="Crown",
        description='Todo!',
        modelName='crown_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.BlueBallcap: HatItemDefinition(
        name="Blue Baseball Cap",
        description='Todo!',
        modelName='baseball_classic',
        textureName='baseball_classic_blue',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.OrangeBallcap: HatItemDefinition(
        name="Orange Baseball Cap",
        description='Todo!',
        modelName='baseball_classic',
        textureName='baseball_classic_orange',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.CowboyHat: HatItemDefinition(
        name="Cowboy Hat",
        description='Todo!',
        modelName='cowboy_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.PirateHat: HatItemDefinition(
        name="Pirate Hat",
        description='Todo!',
        modelName='pirate_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.PropellerHat: HatItemDefinition(
        name="Propeller Hat",
        description='Todo!',
        modelName='propeller_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.FishingHat: HatItemDefinition(
        name="Fishing Hat",
        description='Todo!',
        modelName='fishing_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.Sombrero: HatItemDefinition(
        name="Sombrero Hat",
        description='Todo!',
        modelName='sombrero_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.StrawHat: HatItemDefinition(
        name="Straw Hat",
        description='Todo!',
        modelName='straw_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.Antenna: HatItemDefinition(
        name="Bug Antenna",
        description='Todo!',
        modelName='antenna_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.BeehiveHair: HatItemDefinition(
        name="Beehive Hairdo",
        description='You\'ll be the buzz around town!',
        modelName='hair_beehive_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.BowlerHat: HatItemDefinition(
        name="Bowler Hat",
        description='Todo!',
        modelName='bowler_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.ChefHat: HatItemDefinition(
        name="Chef Hat",
        description='Todo!',
        modelName='chef_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.DetectiveHat: HatItemDefinition(
        name="Detective Hat",
        description='Todo!',
        modelName='detective_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.FancyFeatherHat: HatItemDefinition(
        name="Fancy Feathers Hat",
        description='Todo!',
        modelName='headband_feathers_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.Fedora: HatItemDefinition(
        name="Fedora",
        description='Todo!',
        modelName='fedora_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.BandConductorHat: HatItemDefinition(
        name="Superficial Shako Hat",
        description='Todo!',
        modelName='shako_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.Sweatband: HatItemDefinition(
        name="Sweatband",
        description='Todo!',
        modelName='headband_sweatband',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.Pompadour: HatItemDefinition(
        name="Pompadour Hairdo",
        description='Todo!',
        modelName='hair_pompador_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.ArcherHat: HatItemDefinition(
        name="Archer Hat",
        description='Todo!',
        modelName='robinhood_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.RomanHelmet: HatItemDefinition(
        name="Roman Helmet",
        description='Todo!',
        modelName='helmet_roman_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.WebbedAntenna: HatItemDefinition(
        name="Webbed Bug Antenna",
        description='Todo!',
        modelName='antenna_spider_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.Tiara: HatItemDefinition(
        name="Tiara",
        description='Todo!',
        modelName='crown_tiara_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.VikingHelmet: HatItemDefinition(
        name="Viking Helmet",
        description='Todo!',
        modelName='helmet_viking_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.WitchHat: HatItemDefinition(
        name="Witch Hat",
        description='Todo!',
        modelName='witch_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.WizardHat: HatItemDefinition(
        name="Wizard Hat",
        description='Todo!',
        modelName='wizard_enchanted',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.ConquistadorHelmet: HatItemDefinition(
        name="Conquistador Helmet",
        description='Todo!',
        modelName='helmet_conquistador_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.FirefighterHelmet: HatItemDefinition(
        name="Firefighter Helmet",
        description='Todo!',
        modelName='firefighter_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.TinFoilHat: HatItemDefinition(
        name="Anti-Cog Control Hat",
        description='Todo!',
        modelName='foil_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.MinerHat: HatItemDefinition(
        name="Miner Hat",
        description='Todo!',
        modelName='miner_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.NapoleonHat: HatItemDefinition(
        name="Napoleon Hat",
        description='Todo!',
        modelName='napoleon_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.PilotCap: HatItemDefinition(
        name="Pilot Cap",
        description='Todo!',
        modelName='pilot_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.CopHat: HatItemDefinition(
        name="Cop Hat",
        description='Todo!',
        modelName='police_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.RainbowWig: HatItemDefinition(
        name="Rainbow Wacky Wig",
        description='Todo!',
        modelName='hair_afro_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.YellowBallcap: HatItemDefinition(
        name="Yellow Baseball Cap",
        description='Todo!',
        modelName='baseball_classic',
        textureName='baseball_classic_yellow',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.RedBallcap: HatItemDefinition(
        name="Red Baseball Cap",
        description='Todo!',
        modelName='baseball_classic',
        textureName='baseball_classic_red',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.AquaBallcap: HatItemDefinition(
        name="Aqua Baseball Cap",
        description='Todo!',
        modelName='baseball_classic',
        textureName='baseball_classic_teal',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.SailorHat: HatItemDefinition(
        name="Sailor Hat",
        description='Todo!',
        modelName='paper_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.SambaHat: HatItemDefinition(
        name="Samba Hat",
        description='Todo!',
        modelName='fruits_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.BobbyHat: HatItemDefinition(
        name="Bobby Hat",
        description='Todo!',
        modelName='bobby_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.JugheadHat: HatItemDefinition(
        name="Jester Hat",
        description='Todo!',
        modelName='jughead_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.PurpleBallcap: HatItemDefinition(
        name="Purple Baseball Cap",
        description='Todo!',
        modelName='baseball_classic',
        textureName='baseball_classic_purple',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.WinterHat: HatItemDefinition(
        name="Winter Hat",
        description='Todo!',
        modelName='winter_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.ToonosaurHat: HatItemDefinition(
        name="Toonosaur Hat",
        description='Todo!',
        modelName='dinosaur_classic',
        textureName=None,
        accessoryClass=HatClassEnum.HatHideEars
    ),
    HatItemType.JamboreeHat: HatItemDefinition(
        name="Jamboree Hat",
        description='Todo!',
        modelName='band_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.BirdHat: HatItemDefinition(
        name="Bird Hat",
        description='Todo!',
        modelName='birdnest_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.PinkBow: HatItemDefinition(
        name="Pink Bow",
        description='Todo!',
        modelName='bow_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.RedBow: HatItemDefinition(
        name="Red Bow",
        description='Todo!',
        modelName='bow_classic',
        textureName='bow_classic_polka_lg_red',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.PurpleBow: HatItemDefinition(
        name="Purple Bow",
        description='Todo!',
        modelName='bow_classic',
        textureName='bow_classic_polka_sm_purple',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.SunHat: HatItemDefinition(
        name="Sun Hat",
        description='Todo!',
        modelName='sun_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.YellowBow: HatItemDefinition(
        name="Yellow Bow",
        description='Todo!',
        modelName='bow_classic',
        textureName='bow_classic_col_yellow',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.CheckerBow: HatItemDefinition(
        name="Checker Bow",
        description='Todo!',
        modelName='bow_classic',
        textureName='bow_classic_checker_blue',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.LightRedBow: HatItemDefinition(
        name="Light Red Bow",
        description='Todo!',
        modelName='bow_classic',
        textureName='bow_classic_col_red',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.RainbowBow: HatItemDefinition(
        name="Rainbow Bow",
        description='Todo!',
        modelName='bow_classic',
        textureName='bow_classic_col_rainbow',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.PrincessHat: HatItemDefinition(
        name="Princess Hat",
        description='Todo!',
        modelName='princess_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.PinkDotBow: HatItemDefinition(
        name="Pink Dots Bow",
        description='Todo!',
        modelName='bow_classic',
        textureName='bow_classic_polka_md_pink',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.GreenCheckerBow: HatItemDefinition(
        name="Green Checker Bow",
        description='Todo!',
        modelName='bow_classic',
        textureName='bow_classic_checker_yellow',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.Bandana: HatItemDefinition(
        name="Bandana",
        description='Todo!',
        modelName='bandana_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.SpaceHelm: HatItemDefinition(
        name="Moon Suit Helmet",
        description='Todo!',
        modelName='over_helmet_space',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.BatBow: HatItemDefinition(
        name="Bat Bow",
        description='Todo!',
        modelName='bow_bat',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.CauldronHat: HatItemDefinition(
        name="Cauldron Hat",
        description='Todo!',
        modelName='cauldron',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.ElectricBolts: HatItemDefinition(
        name="Electric Bolts",
        description='Todo!',
        modelName='headband_bolts',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.PumpkinBucket: HatItemDefinition(
        name="Pumpkin Bucket Hat",
        description='Todo!',
        modelName='bucket_pumpkin',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.ScarecrowHat: HatItemDefinition(
        name="Scarecrow Hat",
        description='Todo!',
        modelName='scarecrow',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.WizardBlack: HatItemDefinition(
        name="Black Wizard Hat",
        description='Todo!',
        modelName='wizard_enchanted',
        textureName='wizard_enchanted_stars_black',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.WizardPink: HatItemDefinition(
        name="Pink Wizard Hat",
        description='Todo!',
        modelName='wizard_enchanted',
        textureName='wizard_enchanted_stars_pink',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.WizardRed: HatItemDefinition(
        name="Red Wizard Hat",
        description='Todo!',
        modelName='wizard_enchanted',
        textureName='wizard_enchanted_stars_red',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.WizardGreen: HatItemDefinition(
        name="Green Wizard Hat",
        description='Todo!',
        modelName='wizard_enchanted',
        textureName='wizard_enchanted_stars_green',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.WizardBlue: HatItemDefinition(
        name="Blue Wizard Hat",
        description='Todo!',
        modelName='wizard_enchanted',
        textureName='wizard_enchanted_stars_blue',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.FrankHead: HatItemDefinition(
        name="Frankenstein Head",
        description='Todo!',
        modelName='frankenstein_classic',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.AlchemistGoggles: HatItemDefinition(
        name="Alchemist Goggles",
        description='Todo!',
        modelName='headband_alchemist',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.TiwBow: HatItemDefinition(
        name="Wonderland Bow",
        description='Todo!',
        modelName='bow_classic',
        textureName='bow_classic_col_black',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.BobbleBlue: HatItemDefinition(
        name="Blue Bobble Hat",
        description='Todo!',
        modelName='beanie_winter',
        textureName='beanie_winter_storm',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.BobbleGreen: HatItemDefinition(
        name="Green Bobble Hat",
        description='Todo!',
        modelName = 'beanie_winter',
        textureName='beanie_winter_green',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.BobbleGrey: HatItemDefinition(
        name="Gray Bobble Hat",
        description='Todo!',
        modelName = 'beanie_winter',
        textureName='beanie_winter_gray',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.BobblePink: HatItemDefinition(
        name="Pink Bobble Hat",
        description='Todo!',
        modelName = 'beanie_winter',
        textureName='beanie_winter_pink',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.BobbleRainbow: HatItemDefinition(
        name="Rainbow Bobble Hat",
        description='Todo!',
        modelName = 'beanie_winter',
        textureName='beanie_winter_rainbow',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.BobbleRed: HatItemDefinition(
        name="Red Bobble Hat",
        description='Todo!',
        modelName = 'beanie_winter',
        textureName='beanie_winter_red',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.SantaRed: HatItemDefinition(
        name="Present Delivery Hat",
        description='Todo!',
        modelName='winter_santa',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.SantaRainbow: HatItemDefinition(
        name="Rainbow Santa Hat",
        description='Todo!',
        modelName='winter_santa',
        textureName='winter_santa_col_rainbow',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.ElfGreen: HatItemDefinition(
        name="Green Elf Hat",
        description='Todo!',
        modelName='winter_santa',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.ElfRed: HatItemDefinition(
        name="Red Elf Hat",
        description='Todo!',
        modelName='winter_santa',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.StarHat: HatItemDefinition(
        name="Tree Topper",
        description='Todo!',
        modelName='star',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.TinHumble: HatItemDefinition(
        name="Humble Tin Soldier Hat",
        description='Todo!',
        modelName='soldier_humble',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.TinRegal: HatItemDefinition(
        name="Regal Tin Soldier Hat",
        description='Todo!',
        modelName='soldier_regal',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.TinTradi: HatItemDefinition(
        name="Traditional Tin Soldier Hat",
        description='Todo!',
        modelName='soldier_tradi',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.RagdollHumble: HatItemDefinition(
        name="Humble Ragdoll Hat",
        description='Todo!',
        modelName='ragdoll_humble',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.RagdollTradi: HatItemDefinition(
        name="Traditional Ragdoll Hat",
        description='Todo!',
        modelName='ragdoll_tradi',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.RagdollRegal: HatItemDefinition(
        name="Regal Ragdoll Hat",
        description='Todo!',
        modelName='ragdoll_regal',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.Antlers: HatItemDefinition(
        name="Antlers",
        description='Todo!',
        modelName='headband_antlers_small',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.DoeBeanie: HatItemDefinition(
        name="Yellow Beanie",
        description='Perfect for The Brrrgh!',
        modelName='beanie_doe',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.WebsterBookhat: HatItemDefinition(
        name="Book Stack",
        description='Books! Pete would be so proud! Maybe..?',
        modelName='books_stack',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.Umbrella: HatItemDefinition(
        name="Umbrella Hat",
        description='Todo!',
        modelName='umbrella',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.AviatorHat: HatItemDefinition(
        name="Aviator Cap",
        description='Sky Clan, here we come!',
        modelName='helmet_aviator',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.CakeHat: HatItemDefinition(
        name="The Clash Bash",
        description='Todo!',
        modelName='top_cake_ani',
        textureName=None,
        accessoryClass=HatClassEnum.ClashBirthdayHat
    ),
    HatItemType.OutbackHat: HatItemDefinition(
        name="Outback Slouch Hat",
        description='Perfect for an outback adventure!',
        modelName='slouch',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.OutbackCorkhat: HatItemDefinition(
        name="Outback Cork Hat",
        description='Quit whining about it!',
        modelName='cork',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.OutbackGeckohat: HatItemDefinition(
        name="Outback Gecko Hat",
        description='Friend included!',
        modelName='gecko',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.AlienHat: HatItemDefinition(
        name="Alien Hat",
        description='Todo!',
        modelName='alien',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.AngelHalo: HatItemDefinition(
        name="Halo",
        description='Todo!',
        modelName='top_halo',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.AngelHaloBlue: HatItemDefinition(
        name="Blue Halo",
        description='Todo!',
        modelName='top_halo',
        textureName='top_halo_blue',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.AngelHaloGreen: HatItemDefinition(
        name="Green Halo",
        description='Todo!',
        modelName='top_halo',
        textureName='top_halo_green',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.AngelHaloOrange: HatItemDefinition(
        name="Orange Halo",
        description='Todo!',
        modelName='top_halo',
        textureName='top_halo_orange',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.AngelHaloPurple: HatItemDefinition(
        name="Purple Halo",
        description='Todo!',
        modelName='top_halo',
        textureName='top_halo_purple',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.AngelHaloRed: HatItemDefinition(
        name="Red Halo",
        description='Todo!',
        modelName='top_halo',
        textureName='top_halo_red',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.DemonHorns: HatItemDefinition(
        name="Horns",
        description='Todo!',
        modelName='headband_horns',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.DemonHornsBlue: HatItemDefinition(
        name="Blue Horns",
        description='Todo!',
        modelName='headband_horns',
        textureName='headband_horns_blue',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.DemonHornsGreen: HatItemDefinition(
        name="Green Horns",
        description='Todo!',
        modelName='headband_horns',
        textureName='headband_horns_green',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.DemonHornsOrange: HatItemDefinition(
        name="Orange Horns",
        description='Todo!',
        modelName='headband_horns',
        textureName='headband_horns_orange',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.DemonHornsPurple: HatItemDefinition(
        name="Purple Horns",
        description='Todo!',
        modelName='headband_horns',
        textureName='headband_horns_purple',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.DemonHornsRed: HatItemDefinition(
        name="Red Horns",
        description='Todo!',
        modelName='headband_horns',
        textureName='headband_horns_red',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.RidinghoodHood: HatItemDefinition(
        name="Riding Hood",
        description='Todo!',
        modelName='hood_riding',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.Robophones: HatItemDefinition(
        name="Retro Robophones",
        description='Todo!',
        modelName='headphones_robo',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.NurseHat: HatItemDefinition(
        name="Nurse Hat",
        description='Laugh your way to good laff!',
        modelName='paper_classic',
        textureName='paper_classic_nurse_blue',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.SpinDoctorBand: HatItemDefinition(
        name="Doctor's Headband",
        description='Tickle feathers can cure anything!',
        modelName='headband_mirror',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.CandycornBow: HatItemDefinition(
        name="Candy Corn Bow",
        description='Todo!',
        modelName='bow_classic',
        textureName='bow_classic_candycorn',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.AngelHaloYellow: HatItemDefinition(
        name="Golden Halo",
        description='Todo!',
        modelName='top_halo',
        textureName='top_halo_yellow',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.DemonHornsYellow: HatItemDefinition(
        name="Golden Horns",
        description='Todo!',
        modelName='headband_horns',
        textureName='headband_horns_yellow',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.BowlingBall: HatItemDefinition(
        name="Bowling Ball Hat",
        description='STRIKE!',
        modelName='gag_bowlingball',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.FruitPie: HatItemDefinition(
        name="Fruit Pie Hat",
        description='Tastes good, too!',
        modelName='gag_fruitpie',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.RagdollHat: HatItemDefinition(
        name="Homemade Ragdoll Hat",
        description='Todo!',
        modelName='ragdoll_homemade',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.SkiHelmet: HatItemDefinition(
        name="Ski Helmet",
        description='Todo!',
        modelName='helmet_ski',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.SkiHelmetBlue: HatItemDefinition(
        name="Blue Ski Helmet",
        description='Todo!',
        modelName='helmet_ski',
        textureName='helmet_ski_col_blue',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.SkiHelmetGreen: HatItemDefinition(
        name="Green Ski Helmet",
        description='Todo!',
        modelName='helmet_ski',
        textureName='helmet_ski_col_green',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.SkiHelmetGray: HatItemDefinition(
        name="Gray Ski Helmet",
        description='Todo!',
        modelName='helmet_ski',
        textureName='helmet_ski_col_gray',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.SkiHelmetPink: HatItemDefinition(
        name="Pink Ski Helmet",
        description='Todo!',
        modelName='helmet_ski',
        textureName='helmet_ski_col_pink',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.SkiHelmetRainbow: HatItemDefinition(
        name="Rainbow Ski Helmet",
        description='Todo!',
        modelName='helmet_ski',
        textureName='helmet_ski_col_rainbow',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.SkiHelmetRed: HatItemDefinition(
        name="Red Ski Helmet",
        description='Todo!',
        modelName='helmet_ski',
        textureName='helmet_ski_col_red',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.SnowmanHat: HatItemDefinition(
        name="Snowman Hat",
        description='Todo!',
        modelName='snowman',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.SoldierHat: HatItemDefinition(
        name="Homemade Soldier Hat",
        description='Todo!',
        modelName='soldier_homemade',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.TvHat: HatItemDefinition(
        name="Broken TV Hat",
        description='Did you try plugging it in again..?',
        modelName='gag_tv',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.SevenFedora: HatItemDefinition(
        name="Agent Seven's Fedora",
        description='Todo!',
        modelName='fedora_classic',
        textureName='fedora_classic_agent7',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.StpatsTopLucky: HatItemDefinition(
        name="St. Pat's Lucky Tophat",
        description='Todo!',
        modelName='tophat_lucky',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.StpatsTopTart: HatItemDefinition(
        name="St. Pat's Tartan Tophat",
        description='Todo!',
        modelName='tophat_tartan',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.StpatsBand: HatItemDefinition(
        name="St. Pat's Clover Headband",
        description='Todo!',
        modelName='headband_lucky_clover',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.StpatsClip: HatItemDefinition(
        name="St. Pat's Clover Hairclip",
        description='Todo!',
        modelName='headband_lucky_clip',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.RainbowPhones: HatItemDefinition(
        name="Triple Rainbow Headphones",
        description='Triple rainbow! What does it mean?',
        modelName='headphones_rainbow',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.ClownHat: HatItemDefinition(
        name="Clown Hat",
        description='Todo!',
        modelName='bowler_clown',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.JesterHat: HatItemDefinition(
        name="Jester Hat",
        description='Popularized in Ye Olde Toontowne!',
        modelName='jester',
        textureName='jester_red',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.JesterBHat: HatItemDefinition(
        name="Black Jester Hat",
        description='Popularized in Ye Olde Toontowne!',
        modelName='jester',
        textureName='jester_black',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.EasterBeanie: HatItemDefinition(
        name="Easter 2020 Beanie",
        description='Todo!',
        modelName='beanie_easter',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.AtticusHat: HatItemDefinition(
        name="Witness Stand-In Hat",
        description='Todo!',
        modelName='skelecog',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.Diploma: HatItemDefinition(
        name="Wing Diploma Bow",
        description='Todo!',
        modelName='bow_diploma',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.Grill: HatItemDefinition(
        name="Grill Hat",
        description='Todo!',
        modelName='grill',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.LeafHat: HatItemDefinition(
        name="Leaf Hat",
        description='Todo!',
        modelName='leaf',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.CandleHat: HatItemDefinition(
        name="Toonsmas Past Candle",
        description='Todo!',
        modelName='candle_past',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.PresentBand: HatItemDefinition(
        name="Toonsmas Present Headband",
        description='Todo!',
        modelName='crown_holly',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.FutureHood: HatItemDefinition(
        name="Toonsmas Future Hood",
        description='Todo!',
        modelName='hood_xmas_future',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.PlantHat: HatItemDefinition(
        name="Plant Hat",
        description='Todo!',
        modelName='plant_fern',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.NewstoonGrayBow: HatItemDefinition(
        name="Gray Newstoon Bow",
        description='Todo!',
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.HwGibus: HatItemDefinition(
        name="Ghastly Tophat",
        description='Todo!',
        modelName='gibus',
        textureName=None,
        accessoryClass=HatClassEnum.GhostTophat
    ),
    HatItemType.HatNumber1: HatItemDefinition(
        name="#1 Hat",
        description='Todo!',
        modelName='drink_planter',
        textureName=None,
        accessoryClass=HatClassEnum.OttomanNumberOnePlantHat
    ),
    HatItemType.RibbonBlue: HatItemDefinition(
        name="Blue Ribbon",
        description='Todo!',
        modelName='bow_classic',
        textureName='bow_classic_polka_sm_blue',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.BandanaDeluxe: HatItemDefinition(
        name="Deluxe Bandana",
        description='Todo!',
        modelName='headband_bandana',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.BrovinciHair: HatItemDefinition(
        name="Bro's Hair",
        description='Todo!',
        modelName='hair_bro',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.HatIcecube: HatItemDefinition(
        name="Brain Freeze",
        description='Todo!',
        modelName='over_icecube',
        textureName=None,
        accessoryClass=HatClassEnum.HatFreezeHead
    ),
    HatItemType.HatSmartcap: HatItemDefinition(
        name="Smart Cap",
        description='Todo!',
        modelName='grad',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.HatClownbeanie: HatItemDefinition(
        name="Clownfish Beanie",
        description='Fills your head with jokes!',
        modelName='beanie_clownfish',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.HatBananahat: HatItemDefinition(
        name="Banana Peel Hat",
        description='Don\'t slip!',
        modelName='gag_banana',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.HatWingsuitHelmet: HatItemDefinition(
        name="Wingsuit Helmet",
        description='It might allow you to fly... not Loony Labs certified.',
        modelName='helmet_wingsuit',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.HatEngineerCap: HatItemDefinition(
        name="Trolley Engineer Cap",
        description='All aboard!',
        modelName='engineer_trolley',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.DonuthatPink: HatItemDefinition(
        name="Pink Donut",
        description='With sprinkles on top, please!',
        modelName='donut',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.DonuthatBlue: HatItemDefinition(
        name="Blue Donut",
        description='With sprinkles on top, please!',
        modelName='donut',
        textureName='donut_blue',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.DonuthatChocolate: HatItemDefinition(
        name="Chocolate Donut",
        description='With sprinkles on top, please!',
        modelName='donut',
        textureName='donut_chocolate',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.DonuthatLemon: HatItemDefinition(
        name="Lemon Donut",
        description='With sprinkles on top, please!',
        modelName='donut',
        textureName='donut_lemon',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.DonuthatVanilla: HatItemDefinition(
        name="Vanilla Donut",
        description='With sprinkles on top, please!',
        modelName='donut',
        textureName='donut_vanilla',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.CrullerBeret: HatItemDefinition(
        name="Cruller Beret",
        description='Hold the sprinkles, please.',
        modelName='beret_cruller',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.FlowercrownWhite: HatItemDefinition(
        name="White Flower Crown",
        description='Daffodil Gardens specialty!',
        modelName='crown_flower',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.FlowercrownBlue: HatItemDefinition(
        name="Blue Flower Crown",
        description='Daffodil Gardens specialty!',
        modelName='crown_flower',
        textureName='crown_flower_blue',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.FlowercrownCyan: HatItemDefinition(
        name="Cyan Flower Crown",
        description='Daffodil Gardens specialty!',
        modelName='crown_flower',
        textureName='crown_flower_cyan',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.FlowercrownCyanpurple: HatItemDefinition(
        name="Purple Flower Crown",
        description='Daffodil Gardens specialty!',
        modelName='crown_flower',
        textureName='crown_flower_cyanpurple',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.FlowercrownGreen: HatItemDefinition(
        name="Green Flower Crown",
        description='Daffodil Gardens specialty!',
        modelName='crown_flower',
        textureName='crown_flower_green',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.FlowercrownOrange: HatItemDefinition(
        name="Orange Flower Crown",
        description='Daffodil Gardens specialty!',
        modelName='crown_flower',
        textureName='crown_flower_orange',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.FlowercrownOrangepink: HatItemDefinition(
        name="Orangepink Flower Crown",
        description='Daffodil Gardens specialty!',
        modelName='crown_flower',
        textureName='crown_flower_orangepink',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.FlowercrownPink: HatItemDefinition(
        name="Pink Flower Crown",
        description='Daffodil Gardens specialty!',
        modelName='crown_flower',
        textureName='crown_flower_pink',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.FlowercrownPinkblue: HatItemDefinition(
        name="Pinkblue Flower Crown",
        description='Daffodil Gardens specialty!',
        modelName='crown_flower',
        textureName='crown_flower_pinkblue',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.FlowercrownPurple: HatItemDefinition(
        name="Purple Flower Crown",
        description='Daffodil Gardens specialty!',
        modelName='crown_flower',
        textureName='crown_flower_purple',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.FlowercrownRed: HatItemDefinition(
        name="Red Flower Crown",
        description='Daffodil Gardens specialty!',
        modelName='crown_flower',
        textureName='crown_flower_red',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.FlowercrownRedyellow: HatItemDefinition(
        name="Redyellow Flower Crown",
        description='Daffodil Gardens specialty!',
        modelName='crown_flower',
        textureName='crown_flower_redyellow',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.FlowercrownYellow: HatItemDefinition(
        name="Yellow Flower Crown",
        description='Daffodil Gardens specialty!',
        modelName='crown_flower',
        textureName='crown_flower_yellow',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.RosecrownWhite: HatItemDefinition(
        name="White Rose Crown",
        description='Picked right off the bouquet!',
        modelName='crown_rose',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.RosecrownBlue: HatItemDefinition(
        name="Blue Rose Crown",
        description='Picked right off the bouquet!',
        modelName='crown_rose',
        textureName='crown_rose_blue',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.RosecrownCyan: HatItemDefinition(
        name="Cyan Rose Crown",
        description='Picked right off the bouquet!',
        modelName='crown_rose',
        textureName='crown_rose_cyan',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.RosecrownGreen: HatItemDefinition(
        name="Green Rose Crown",
        description='Picked right off the bouquet!',
        modelName='crown_rose',
        textureName='crown_rose_green',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.RosecrownOrange: HatItemDefinition(
        name="Orange Rose Crown",
        description='Picked right off the bouquet!',
        modelName='crown_rose',
        textureName='crown_rose_orange',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.RosecrownPink: HatItemDefinition(
        name="Pink Rose Crown",
        description='Picked right off the bouquet!',
        modelName='crown_rose',
        textureName='crown_rose_pink',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.RosecrownPurple: HatItemDefinition(
        name="Purple Rose Crown",
        description='Picked right off the bouquet!',
        modelName='crown_rose',
        textureName='crown_rose_purple',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.RosecrownRed: HatItemDefinition(
        name="Red Rose Crown",
        description='Picked right off the bouquet!',
        modelName='crown_rose',
        textureName='crown_rose_red',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.RosecrownYellow: HatItemDefinition(
        name="Yellow Rose Crown",
        description='Picked right off the bouquet!',
        modelName='crown_rose',
        textureName='crown_rose_yellow',
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.HatChainsaw: HatItemDefinition(
        name="Chainsaw Consultant's Hat",
        description='Todo!',
        modelName='chainsaw',
        textureName=None,
        accessoryClass=HatClassEnum.ChainsawConsultantHat
    ),
    HatItemType.HatMultislacker: HatItemDefinition(
        name="Multislacker's Hat",
        description='Todo!',
        modelName='multislacker',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.HatTreekiller: HatItemDefinition(
        name="Stump Hat",
        description='Todo!',
        modelName='helmet_treestump',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.HatFeatherbedder: HatItemDefinition(
        name="Feather Unibrow",
        description='Todo!',
        modelName = 'brow_fbedder',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.HatNightcap: HatItemDefinition(
        name="Sleepwalker Nightcap",
        description='Sleep tight!',
        modelName='nightcap',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.HatBlackberet: HatItemDefinition(
        name="Beret",
        description='Un brush and un beret.',
        modelName='beret',
        textureName=None,
        accessoryClass=HatClassEnum.Beret
    ),
    HatItemType.HatGumballhat: HatItemDefinition(
        name="Gumball Machine Hat",
        description='Fits like a... gumball machine?',
        modelName='over_gumball',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.HatCardcrown: HatItemDefinition(
        name="Card Suit Crown",
        description='Raise the stakes!',
        modelName='crown_card',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.HatCardtophat: HatItemDefinition(
        name="Card Suit Hat",
        description='Raise the stakes!',
        modelName='tophat_card',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.HatButter: HatItemDefinition(
        name="Butter Hat",
        description='Hat with the \1TextTitle\1Butter.\2',
        modelName='butter',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.HatRainmakerDepression: HatItemDefinition(
        name="Storm Cloud",
        description='Todo!',
        modelName='top_cloud_rain',
        textureName=None,
        accessoryClass=HatClassEnum.StormCloudHat
    ),
    HatItemType.HatGumballHairbow: HatItemDefinition(
        name="Hairbow",
        description='Classy and classic!',
        modelName="bow_hair",
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.HatFirestarter: HatItemDefinition(
        name="Firestarter Helmet",
        description='Todo!',
        modelName='firestarter',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.PainterBeret: HatItemDefinition(
        name="Painter's Beret",
        description='Paint not included.',
        modelName='beret_painter',
        textureName=None,
        accessoryClass=HatClassEnum.Default
    ),
    HatItemType.HatGumballHairbowB: HatItemDefinition(
        name="Blue Ribbon Hairbow",
        description="Classy and classic!",
        modelName="bow_hair",
        textureName="bow_hair_blue",
    ),
    HatItemType.HatGumballHairbowBr: HatItemDefinition(
        name="Brown Ribbon Hairbow",
        description="Classy and classic!",
        modelName="bow_hair",
        textureName="bow_hair_brown",
    ),
    HatItemType.HatGumballHairbowG: HatItemDefinition(
        name="Green Ribbon Hairbow",
        description="Classy and classic!",
        modelName="bow_hair",
        textureName="bow_hair_green",
    ),
    HatItemType.HatGumballHairbowOr: HatItemDefinition(
        name="Orange Ribbon Hairbow",
        description="Classy and classic!",
        modelName="bow_hair",
        textureName="bow_hair_orange",
    ),
    HatItemType.HatGumballHairbowP: HatItemDefinition(
        name="Pink Ribbon Hairbow",
        description="Classy and classic!",
        modelName="bow_hair",
        textureName="bow_hair_pink",
    ),
    HatItemType.HatGumballHairbowPu: HatItemDefinition(
        name="Purple Ribbon Hairbow",
        description="Classy and classic!",
        modelName="bow_hair",
        textureName="bow_hair_purple",
    ),
    HatItemType.HatGumballHairbowRb: HatItemDefinition(
        name="Rainbow Ribbon Hairbow",
        description="Classy, classic, and chromatic!",
        modelName="bow_hair",
        textureName="bow_hair_rainbow",
    ),
    HatItemType.HatWitchhunter: HatItemDefinition(
        name="Caddish Chapeau",
        description="No Description",
        modelName="witchhunter",
    ),
    HatItemType.HatGoonPatrolYellow: HatItemDefinition(
        name="Yellow Goon Hardhat",
        description="No Description",
        modelName="goon_patrol_classic",
    ),
    HatItemType.HatGoonPatrolOrange: HatItemDefinition(
        name="Orange Goon Hardhat",
        description="No Description",
        modelName="goon_patrol_classic",
        textureName="goon_patrol_classic_orange",
    ),
    HatItemType.HatGoonPatrolRed: HatItemDefinition(
        name="Red Goon Hardhat",
        description="No Description",
        modelName="goon_patrol_classic",
        textureName="goon_patrol_classic_red",
    ),
    HatItemType.HatGoonPatrolPurple: HatItemDefinition(
        name="Purple Goon Hardhat",
        description="No Description",
        modelName="goon_patrol_classic",
        textureName="goon_patrol_classic_purple",
    ),
    HatItemType.HatGoonSecurity: HatItemDefinition(
        name="Security Goon Hat",
        description="No Description",
        modelName="goon_security_classic",
    ),
    HatItemType.HatForeman: HatItemDefinition(
        name="Factory Foreman Hat",
        description="No Description",
        modelName="skelecog",
        textureName="skel_purple",
    ),
    HatItemType.HatCogBucket: HatItemDefinition(
        name="Cog Bucket Hat",
        description="No Description",
        modelName="bucket_cog",
    ),
    HatItemType.HatLowBaller: HatItemDefinition(
        name="Low Baller Hat",
        description="No Description",
        modelName="lowballer",
    ),
    HatItemType.HatHighRoller: HatItemDefinition(
        name="High Roller's Hat",
        description="No Description",
        modelName="highroller",
        accessoryClass=HatClassEnum.HighRollerHat,
    ),
    HatItemType.GbHairbowBlack: HatItemDefinition(
        name="Black Hairbow",
        description="Fashionable!",
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName="bowtie_fancy_col_black",
    ),
    HatItemType.GbHairbowBlackwhite: HatItemDefinition(
        name="Zebrastripe Hairbow",
        description="Kinda tacky, but fashionable!",
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName="bowtie_fancy_striped_black_white",
    ),
    HatItemType.GbHairbowBlue: HatItemDefinition(
        name="Blue Hairbow",
        description="Boldly blue!",
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName="bowtie_fancy_col_blue",
    ),
    HatItemType.GbHairbowGray: HatItemDefinition(
        name="Gray Hairbow",
        description="Drab... still fashionable!",
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName="bowtie_fancy_col_gray",
    ),
    HatItemType.GbHairbowGreen: HatItemDefinition(
        name="Green Hairbow",
        description="Mint condition!",
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName="bowtie_fancy_col_green",
    ),
    HatItemType.GbHairbowOrange: HatItemDefinition(
        name="Orange Hairbow",
        description="Looks like sunshine! And fashion!",
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName="bowtie_fancy_col_orange",
    ),
    HatItemType.GbHairbowPink: HatItemDefinition(
        name="Pink Hairbow",
        description="It's pink!",
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName="bowtie_fancy_col_pink",
    ),
    HatItemType.GbHairbowPinkblack: HatItemDefinition(
        name="Radical Hairbow",
        description="Perfect for running!",
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName="bowtie_fancy_striped_pink_black",
    ),
    HatItemType.GbHairbowPolkadot: HatItemDefinition(
        name="Polkadot Hairbow",
        description="Unpredictably wacky!",
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName="bowtie_fancy_polka_white",
    ),
    HatItemType.GbHairbowPurple: HatItemDefinition(
        name="Grape Hairbow",
        description="Deceptively Sweet!",
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName="bowtie_fancy_col_purple",
    ),
    HatItemType.GbHairbowPurpleorange: HatItemDefinition(
        name="PBJ Hairbow",
        description="Tasty, and fashionable!",
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName="bowtie_fancy_striped_purple_orange",
    ),
    HatItemType.GbHairbowRed: HatItemDefinition(
        name="Red Hairbow",
        description="Regular red hairbow!",
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName="bowtie_fancy_col_red",
    ),
    HatItemType.GbHairbowYellow: HatItemDefinition(
        name="Yellow Hairbow",
        description="Oh so bright! And fashionable!",
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName="bowtie_fancy_col_yellow",
    ),
    HatItemType.GbHairbowYellowblack: HatItemDefinition(
        name="Stinging Hairbow",
        description="\1TextTitle\1Yeouch!\2",
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName="bowtie_fancy_striped_yellow_black",
    ),
    HatItemType.PrideHairbowAce: HatItemDefinition(
        name="Ace Pride Hairbow",
        description="No Description",
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName="bowtie_fancy_pride_ace",
    ),
    HatItemType.PrideHairbowAro: HatItemDefinition(
        name="Aromantic Pride Hairbow",
        description="No Description",
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName="bowtie_fancy_pride_aro",
    ),
    HatItemType.PrideHairbowBi: HatItemDefinition(
        name="Bi Pride Hairbow",
        description="No Description",
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName="bowtie_fancy_pride_bi",
    ),
    HatItemType.PrideHairbowGay: HatItemDefinition(
        name="Gay Pride Hairbow",
        description="No Description",
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName="bowtie_fancy_pride_gay",
    ),
    HatItemType.PrideHairbowGenderfluid: HatItemDefinition(
        name="Genderfluid Pride Hairbow",
        description="No Description",
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName="bowtie_fancy_pride_gfld",
    ),
    HatItemType.PrideHairbowLesbian: HatItemDefinition(
        name="Lesbian Pride Hairbow",
        description="No Description",
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName="bowtie_fancy_pride_lsbn",
    ),
    HatItemType.PrideHairbowLgbt: HatItemDefinition(
        name="Pride Hairbow",
        description="No Description",
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName="bowtie_fancy_pride_lgbt",
    ),
    HatItemType.PrideHairbowNb: HatItemDefinition(
        name="Non-Binary Pride Hairbow",
        description="No Description",
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName="bowtie_fancy_pride_nb",
    ),
    HatItemType.PrideHairbowPan: HatItemDefinition(
        name="Pan Pride Hairbow",
        description="No Description",
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName="bowtie_fancy_pride_pan",
    ),
    HatItemType.PrideHairbowTrans: HatItemDefinition(
        name="Trans Pride Hairbow",
        description="No Description",
        modelName='bowtie_fancy',
        accFileType=('nec', 'nec'),
        accFilePath = ('neck', 'neck'),
        textureName="bowtie_fancy_pride_trans",
    ),
    HatItemType.HatCyberpunk: HatItemDefinition(
        name="Cybertoon Visor",
        description="No Description",
        modelName="visor_cyber",
    ),
    HatItemType.MuzzleRose: HatItemDefinition(
        name="Solemn Rose",
        description='No Description',
        modelName='rose',
    ),
    HatItemType.PainterBrush: HatItemDefinition(
        name="Painter's Brush",
        description='Paint not included.',
        modelName='painter_brush',
    ),
}
