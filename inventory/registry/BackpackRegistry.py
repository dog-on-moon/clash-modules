"""
This module contains the item data for backpacks.
"""
from panda3d.core import NodePath

from toontown.inventory.base.InventoryItem import InventoryItem
from typing import Dict, Optional
from enum import IntEnum, auto

from toontown.inventory.definitions.AccessoryDefinition import AccessoryDefinition
from toontown.inventory.enums.ItemEnums import BackpackItemType
from toontown.inventory.enums.ItemTags import ItemTag
from toontown.toon.accessories.ToonActorAccessory import ToonActorAccessory
from toontown.toon.accessories.backpacks.BackpackMagnet import BackpackMagnet
from toontown.toon.accessories.backpacks.BackpackPotionsBag import BackpackPotionsBag
from toontown.toon.accessories.backpacks.FactoryGearBackpack import FactoryGearBackpack


class BackpackClassEnum(IntEnum):
    Default = auto()
    BackpackMagnet = auto()
    BackpackPotionsBag = auto()
    FactoryGearBackpack = auto()


baseTexturePath = "cosmetics/maps/"
baseModelPath = "cosmetics/models/"
textureExtension = ".png"


class BackpackItemDefinition(AccessoryDefinition):
    """
    The definition structure for backpacks.
    """

    BackpackClasses = {
        BackpackClassEnum.BackpackMagnet: BackpackMagnet,
        BackpackClassEnum.BackpackPotionsBag: BackpackPotionsBag,
        BackpackClassEnum.FactoryGearBackpack: FactoryGearBackpack,
    }

    def __init__(self,
                 modelName,
                 textureName=None,
                 accessoryClass=BackpackClassEnum.Default,
                 accFileType=('bp', 'bp'),  # cc_t_acc_XXX_
                 accFilePath=('backpack', 'backpack'),  # cosmetics/maps/XXX
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
        return 'Backpack'

    def getRewardName(self, item: Optional[InventoryItem] = None):
        return f'{self.getName()} Backpack'

    def getModelPath(self):
        if not self.modelName:
            return None
        return f"{self.modelPath}{self.baseModelPrefix}{self.modelName}"

    def getTexturePath(self):
        if not self.textureName:
            return None
        return f"{self.texturePath}{self.baseTexturePrefix}{self.textureName}{textureExtension}"


    def getAccessoryClass(self):
        return self.BackpackClasses.get(self.accessoryClass, super().getAccessoryClass())

    def getToonAttachNode(self) -> str:
        return '**/def_joint_attachFlower'

    def getTags(self, item: 'InventoryItem') -> set[ItemTag]:
        tags = super().getTags(item)
        tags.add(ItemTag.Backpack)
        return tags


# The registry dictionary for backpacks.
BackpackRegistry: Dict[IntEnum, BackpackItemDefinition] = {
    BackpackItemType.BlueBackpack: BackpackItemDefinition(
        name="Blue Backpack",
        description='Todo!',
        modelName='backpack_classic',
        textureName='backpack_classic_blue',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.OrangeBackpack: BackpackItemDefinition(
        name="Orange Backpack",
        description='Todo!',
        modelName='backpack_classic',
        textureName='backpack_classic_splat_orange',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.PurpleBackpack: BackpackItemDefinition(
        name="Purple Backpack",
        description='Todo!',
        modelName='backpack_classic',
        textureName='backpack_classic_splat_purple',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.RedDotBackpack: BackpackItemDefinition(
        name="Red Dot Backpack",
        description='Todo!',
        modelName='backpack_classic',
        textureName='backpack_classic_polka_red',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.YellowDotBackpack: BackpackItemDefinition(
        name="Yellow Dot Backpack",
        description='Todo!',
        modelName='backpack_classic',
        textureName='backpack_classic_polka_yellow',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.BatWings: BackpackItemDefinition(
        name="Bat Wings",
        description='Todo!',
        modelName='wings_bat_classic',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.BeeWings: BackpackItemDefinition(
        name="Bee Wings",
        description='Todo!',
        modelName='wings_bee_classic',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.DragonflyWings: BackpackItemDefinition(
        name="Dragonfly Wings",
        description='Todo!',
        modelName='wings_dragonfly_classic',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.ScubaTank: BackpackItemDefinition(
        name="Scuba Tank",
        description='Todo!',
        modelName='tank_scuba_classic',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.SharkFin: BackpackItemDefinition(
        name="Shark Fin",
        description='Todo!',
        modelName='shark_classic',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.AngelWingsClassic: BackpackItemDefinition(
        name="White Angel Wings",
        description='Todo!',
        modelName='wings_angel_classic',
        textureName='wings_angel_classic_col_white',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.AngelWingsClassicRainbow: BackpackItemDefinition(
        name="Rainbow Angel Wings",
        description='Todo!',
        modelName='wings_angel_classic',
        textureName='wings_angel_classic_col_rainbow',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.ToyBackpack: BackpackItemDefinition(
        name="Toys Backpack",
        description='Todo!',
        modelName='toys_classic',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.ButterflyWings: BackpackItemDefinition(
        name="Butterfly Wings",
        description='Todo!',
        modelName='wings_butterfly_classic',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.PixieWings: BackpackItemDefinition(
        name="Pixie Wings",
        description='Todo!',
        modelName='wings_butterfly_classic',
        textureName='wings_butterfly_classic_2',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.DragonWings: BackpackItemDefinition(
        name="Dragon Wings",
        description='Todo!',
        modelName='wings_dragonfly_classic',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.Jetpack: BackpackItemDefinition(
        name="Jet Pack",
        description='Todo!',
        modelName='jetpack_classic',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.BugBackpack: BackpackItemDefinition(
        name="Bug Backpack",
        description='Todo!',
        modelName='legs_spider_classic',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.PlushBearPack: BackpackItemDefinition(
        name="Plush Bear Pack",
        description='Todo!',
        modelName='stuffed_bear_classic',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.BirdWings: BackpackItemDefinition(
        name="Bird Wings",
        description='Todo!',
        modelName='wings_bird_classic',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.PlushCatPack: BackpackItemDefinition(
        name="Plush Cat Pack",
        description='Todo!',
        modelName='stuffed_cat_classic',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.PlushDogPack: BackpackItemDefinition(
        name="Plush Dog Pack",
        description='Todo!',
        modelName='stuffed_dog_classic',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.PlaneWings: BackpackItemDefinition(
        name="Airplane Wings",
        description='Todo!',
        modelName='wings_airplane_classic',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.PirateSword: BackpackItemDefinition(
        name="Pirate Sword",
        description='Todo!',
        modelName='sword_classic',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.SuperToonCape: BackpackItemDefinition(
        name="Super Toon Cape",
        description='Todo!',
        modelName='cape_classic',
        textureName='cape_classic_col_red',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.VampireCape: BackpackItemDefinition(
        name="Vampire Cape",
        description='Todo!',
        modelName='cape_classic',
        textureName='cape_classic_col_black',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.ToonosaurTail: BackpackItemDefinition(
        name="Toonosaur Tail",
        description='Todo!',
        modelName='tail_dinosaur_classic',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.JamboreePack: BackpackItemDefinition(
        name="Jamboree Pack",
        description='Todo!',
        modelName='band_classic',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.GagAttackPack: BackpackItemDefinition(
        name="Gag Attack Pack",
        description='Todo!',
        modelName='gags_classic',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.CogPack: BackpackItemDefinition(
        name="Cog Pack",
        description='Todo!',
        modelName='plushie_flunky_classic',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.SpaceBack: BackpackItemDefinition(
        name="Moon Suit Backpack",
        description='Todo!',
        modelName='tank_space',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.WitchBroom: BackpackItemDefinition(
        name="Witches Broom",
        description='Todo!',
        modelName='broom_witch',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.ReaperCape: BackpackItemDefinition(
        name="Reaper Cape",
        description='Todo!',
        modelName='cape_reaper',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.DraculaCape: BackpackItemDefinition(
        name="Dracula Cape",
        description='Todo!',
        modelName='cape_dracula',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.TrickortreatBack: BackpackItemDefinition(
        name="Trick or Treat Backpack",
        description='Todo!',
        modelName='bag_trickortreat',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.PotionBack: BackpackItemDefinition(
        name="Potions Bag",
        description='Todo!',
        modelName='bag_potions',
        textureName=None,
        accessoryClass=BackpackClassEnum.BackpackPotionsBag
    ),
    BackpackItemType.TinTradi: BackpackItemDefinition(
        name="Traditional Tin Soldier",
        description='Todo!',
        modelName='key_windup',
        textureName='key_windup_gold',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.TinHumble: BackpackItemDefinition(
        name="Humble Tin Soldier",
        description='Todo!',
        modelName='key_windup',
        textureName='key_windup_silver',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.TinRegal: BackpackItemDefinition(
        name="Regal Tin Soldier",
        description='Todo!',
        modelName='key_windup',
        textureName='key_windup_bronze',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.RagdollHumble: BackpackItemDefinition(
        name="Humble Ragdoll",
        description='Todo!',
        modelName='bow_ragdoll',
        textureName='bow_ragdoll_col_white',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.RagdollRegal: BackpackItemDefinition(
        name="Regal Ragdoll",
        description='Todo!',
        modelName='bow_ragdoll',
        textureName='bow_ragdoll_col_red',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.RagdollTradi: BackpackItemDefinition(
        name="Traditional Ragdoll",
        description='Todo!',
        modelName='bow_ragdoll',
        textureName='bow_ragdoll_col_yellow',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.PresentsSack: BackpackItemDefinition(
        name="Presents Sack",
        description='Todo!',
        modelName='bag_presents',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.Snowboard: BackpackItemDefinition(
        name="Snowboard Backpack",
        description='Todo!',
        modelName='snowboard',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.CandyCane: BackpackItemDefinition(
        name="Candy Cane Backpack",
        description='Todo!',
        modelName='candycane',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.CupidBow: BackpackItemDefinition(
        name="Cupid's Bow",
        description='Todo!',
        modelName='bow_cupid_quiver',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.CupidBowQuiver: BackpackItemDefinition(
        name="Cupid's Bow + Quiver",
        description='Todo!',
        modelName='bow_cupid_quiver',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.PropPack: BackpackItemDefinition(
        name="Propeller Pack",
        description='Todo!',
        modelName='propeller',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.Kite: BackpackItemDefinition(
        name="Kite Backpack",
        description='Todo!',
        modelName='kite',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.Hangglider: BackpackItemDefinition(
        name="Hang Glider Backpack",
        description='Todo!',
        modelName='wings_hangglider',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.Telescope: BackpackItemDefinition(
        name="Telescope Backpack",
        description='Todo!',
        modelName='telescope',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.OutbackBackpack: BackpackItemDefinition(
        name="Outback Backpack",
        description='Perfect for an outback adventure!',
        modelName='camper_outback',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.OutbackBoomerang: BackpackItemDefinition(
        name="Outback Boomerang",
        description='Comes right back!',
        modelName='boomerang_outback',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.OutbackDidgeridoo: BackpackItemDefinition(
        name="Outback Didgeridoo",
        description='Sounds like home.',
        modelName='didgeridoo',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.AlienBackpack: BackpackItemDefinition(
        name="Alien Backpack",
        description='Todo!',
        modelName='alien',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.AngelWings: BackpackItemDefinition(
        name="Angel Wings",
        description='Todo!',
        modelName='wings_angel_divine',
        textureName='wings_angel_divine_col_white',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.AngelWingsBlue: BackpackItemDefinition(
        name="Blue Angel Wings",
        description='Todo!',
        modelName='wings_angel_divine',
        textureName='wings_angel_divine_col_blue',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.AngelWingsGreen: BackpackItemDefinition(
        name="Green Angel Wings",
        description='Todo!',
        modelName='wings_angel_divine',
        textureName='wings_angel_divine_col_green',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.AngelWingsOrange: BackpackItemDefinition(
        name="Orange Angel Wings",
        description='Todo!',
        modelName='wings_angel_divine',
        textureName='wings_angel_divine_col_orange',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.AngelWingsPurple: BackpackItemDefinition(
        name="Purple Angel Wings",
        description='Todo!',
        modelName='wings_angel_divine',
        textureName='wings_angel_divine_col_purple',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.AngelWingsRed: BackpackItemDefinition(
        name="Red Angel Wings",
        description='Todo!',
        modelName='wings_angel_divine',
        textureName='wings_angel_divine_col_red',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.DemonWings: BackpackItemDefinition(
        name="Evil Wings",
        description='Todo!',
        modelName='wings_demon',
        textureName='wings_demon_black',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.DemonWingsBlue: BackpackItemDefinition(
        name="Blue Evil Wings",
        description='Todo!',
        modelName='wings_demon',
        textureName='wings_demon_blue',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.DemonWingsGreen: BackpackItemDefinition(
        name="Green Evil Wings",
        description='Todo!',
        modelName='wings_demon',
        textureName='wings_demon_green',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.DemonWingsOrange: BackpackItemDefinition(
        name="Orange Evil Wings",
        description='Todo!',
        modelName='wings_demon',
        textureName='wings_demon_orange',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.DemonWingsPurple: BackpackItemDefinition(
        name="Purple Evil Wings",
        description='Todo!',
        modelName='wings_demon',
        textureName='wings_demon_purple',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.DemonWingsRed: BackpackItemDefinition(
        name="Red Evil Wings",
        description='Todo!',
        modelName='wings_demon',
        textureName='wings_demon_red',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.RidinghoodCloak: BackpackItemDefinition(
        name="Riding Hood Cloak",
        description='Todo!',
        modelName='cloak_riding',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.AngelWingsYellow: BackpackItemDefinition(
        name="Golden Angel Wings",
        description='Todo!',
        modelName='wings_angel_divine',
        textureName='wings_angel_divine_col_yellow',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.DemonWingsYellow: BackpackItemDefinition(
        name="Golden Evil Wings",
        description='Todo!',
        modelName='wings_demon',
        textureName='wings_demon_yellow',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.StabPack: BackpackItemDefinition(
        name="The Backstab",
        description='Todo!',
        modelName='backstab',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.GavelPack: BackpackItemDefinition(
        name="Gavel Backpack",
        description='Todo!',
        modelName='gavel',
        textureName = None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.CjPack: BackpackItemDefinition(
        name="The Book of Law",
        description='Todo!',
        modelName='book',
        textureName='book_clo',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.StonePack: BackpackItemDefinition(
        name="Lawbots Tombstone",
        description='Todo!',
        modelName='gravestone',
        textureName='gravestone_lawbots',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.TntPack: BackpackItemDefinition(
        name="TNT Backpack",
        description='You\'ll have a blast!',
        modelName='gag_tnt',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.RagdollHomemadeBow: BackpackItemDefinition(
        name="Homemade Ragdoll Bow",
        description='Todo!',
        modelName = 'bow_ragdoll',
        textureName = 'bow_ragdoll_col_orange',
        accessoryClass = BackpackClassEnum.Default
    ),
    BackpackItemType.SoldierHomemadeKey: BackpackItemDefinition(
        name="Homemade Tin Soldier Key",
        description='Todo!',
        modelName='key_windup',
        textureName='key_windup_wood',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.SeltzerPack: BackpackItemDefinition(
        name="Seltzer Backpack",
        description='Would you like a glass?',
        modelName='gag_seltzer',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.MiniMag: BackpackItemDefinition(
        name="Small Magnet Backpack",
        description='Function and fashion!',
        modelName='gag_magnet',
        textureName='gag_magnet_red',
        accessoryClass=BackpackClassEnum.BackpackMagnet
    ),
    BackpackItemType.Taser: BackpackItemDefinition(
        name="Button Backpack",
        description='Todo!',
        modelName='gag_joybuzzer',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.FusionPack: BackpackItemDefinition(
        name="Fusion Gags Pack",
        description='Keeps you SAFE.',
        modelName='gags_fusion',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.ChairPack: BackpackItemDefinition(
        name="Plush Chairman Backpack",
        description='Todo!',
        modelName='plushie_chairman',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.BunnyBackpack: BackpackItemDefinition(
        name="Easter 2020 Bunnypack",
        description='Todo!',
        modelName='stuffed_bunny',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.Spatula: BackpackItemDefinition(
        name="Spatula Backpack",
        description='Todo!',
        modelName='spatula',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.Firework: BackpackItemDefinition(
        name="Firework Backpack",
        description='Todo!',
        modelName='firecracker',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.Spellbook: BackpackItemDefinition(
        name="Spellbook Backpack",
        description='Todo!',
        modelName='book',
        textureName='book_spells',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.Tombstone: BackpackItemDefinition(
        name="Tombstone Backpack",
        description='Todo!',
        modelName='gravestone',
        textureName='gravestone_smile',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.CandyPumpkin: BackpackItemDefinition(
        name="Candy-Filled Pumpkin",
        description='Todo!',
        modelName='pumpkin_candy',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.PlatePack: BackpackItemDefinition(
        name="Giving Thanks Platepack",
        description='Todo!',
        modelName='plate',
        textureName='plate_thanks',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.Extinguisher: BackpackItemDefinition(
        name="Toonsmas Past Extinguisher",
        description='Todo!',
        modelName='extinguisher',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.PresentCorn: BackpackItemDefinition(
        name="Toonsmas Present Cornucopia",
        description='Todo!',
        modelName='cornucopia',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.FutureWing: BackpackItemDefinition(
        name="Toonsmas Future Wings",
        description='Todo!',
        modelName='cloak_future_wings',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.FutureCloak: BackpackItemDefinition(
        name="Toonsmas Future Cloak",
        description='Todo!',
        modelName='cloak_future_cape',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.FutureWingCloak: BackpackItemDefinition(
        name="Toonsmas Future Wingcloak",
        description='Todo!',
        modelName='cloak_future_combo',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.HwtownCape: BackpackItemDefinition(
        name="Hallowopolis Wingcape",
        description='Todo!',
        modelName='cape_hwtown',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.SadsPack: BackpackItemDefinition(
        name="Sads Plushpack",
        description='Todo!',
        modelName='plushie_sads',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.NewstoonSuitcase: BackpackItemDefinition(
        name="Newstoon's Suitcase",
        description='Todo!',
        modelName='briefcase',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.NewstoonCamera: BackpackItemDefinition(
        name="Newstoon's Camera",
        description='Todo!',
        modelName='camera_news',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.PrideCapeLgbt: BackpackItemDefinition(
        name="Pride Cape",
        description='Todo!',
        modelName='cape_classic',
        textureName="cape_classic_pride_lgbt",
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.PrideCapeTrans: BackpackItemDefinition(
        name="Trans Pride Cape",
        description='Todo!',
        modelName='cape_classic',
        textureName='cape_classic_pride_trans',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.PrideCapeLesbian: BackpackItemDefinition(
        name="Lesbian Pride Cape",
        description='Todo!',
        modelName='cape_classic',
        textureName='cape_classic_pride_lsbn',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.PrideCapePan: BackpackItemDefinition(
        name="Pan Pride Cape",
        description='Todo!',
        modelName='cape_classic',
        textureName='cape_classic_pride_pan',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.PrideCapeBi: BackpackItemDefinition(
        name="Bi Pride Cape",
        description='Todo!',
        modelName='cape_classic',
        textureName='cape_classic_pride_bi',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.PrideCapeNb: BackpackItemDefinition(
        name="Non-Binary Pride Cape",
        description='Todo!',
        modelName='cape_classic',
        textureName='cape_classic_pride_nb',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.PrideCapeAce: BackpackItemDefinition(
        name="Ace Pride Cape",
        description='Todo!',
        modelName='cape_classic',
        textureName='cape_classic_pride_ace',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.PrideCapeFluid: BackpackItemDefinition(
        name="Genderfluid Pride Cape",
        description='Todo!',
        modelName='cape_classic',
        textureName='cape_classic_pride_gfld',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.PrideCapeAro: BackpackItemDefinition(
        name="Aromantic Pride Cape",
        description='Todo!',
        modelName='cape_classic',
        textureName='cape_classic_pride_aro',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.PrideCape: BackpackItemDefinition(
        name="Gay Pride Cape",
        description='Todo!',
        modelName='cape_classic',
        textureName='cape_classic_pride_gay',
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.DoodlePack: BackpackItemDefinition(
        name="Doodle Pack",
        description='Todo!',
        modelName='stuffed_doodle',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.BackpackMoneybag: BackpackItemDefinition(
        name="Money Bag",
        description='Todo!',
        modelName='bag_money',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.BackpackPitchfork: BackpackItemDefinition(
        name="Pitchfork",
        description='Todo!',
        modelName='pitchfork',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.BackpackWingsuitWings: BackpackItemDefinition(
        name="Wingsuit Wings",
        description='It might allow you to fly... not Loony Labs certified.',
        modelName='wings_wingsuit',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.BackpackPillow: BackpackItemDefinition(
        name="Sleepwalker Pillow",
        description='Sleep tight!',
        modelName='pillow',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.BackpackMajorplayer: BackpackItemDefinition(
        name="Saxophone",
        description='Todo!',
        modelName='saxophone',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.BackpackFirestarter: BackpackItemDefinition(
        name="Firestoker",
        description='Todo!',
        modelName='firestoker',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.BackpackGatekeeper: BackpackItemDefinition(
        name="Shield",
        description='Todo!',
        modelName='shield',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.BackpackFruitbasket: BackpackItemDefinition(
        name="Fruit Basket",
        description='Tastes good, too!',
        modelName='basket_berries',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.BackpackRetrobag: BackpackItemDefinition(
        name="Retro Backpack",
        description='Friday night fever!',
        modelName='retrobag',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.EeBreadbag: BackpackItemDefinition(
        name="Breadbag",
        description='Todo!',
        modelName='bag_bread',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.EePaddle: BackpackItemDefinition(
        name="Pizza Paddle",
        description='Todo!',
        modelName='paddle',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.PainterPalette: BackpackItemDefinition(
        name="Painter's Palette",
        description='...Some paint included.',
        modelName='painter_palette',
        textureName=None,
        accessoryClass=BackpackClassEnum.Default
    ),
    BackpackItemType.DaShredderOmg: BackpackItemDefinition(
        name='The Shredder',
        description='Todo!',
        modelName='guitar_1',
    ),
    BackpackItemType.FactoryGear: BackpackItemDefinition(
        name='Factory Gear Backpack',
        description='Todo!',
        modelName='gear',
        accessoryClass=BackpackClassEnum.FactoryGearBackpack,
    ),
    BackpackItemType.CyberpunkBackpack: BackpackItemDefinition(
        name='Cybertoon Backpack',
        description='Todo!',
        modelName='cybertoon',
    ),
}
