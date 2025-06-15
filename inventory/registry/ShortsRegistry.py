"""
This module contains the item data for shorts.
"""
from panda3d.core import NodePath, Texture, LVecBase4f

from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.base.ItemDefinition import ItemDefinition
from typing import Dict, Optional
from enum import IntEnum

from toontown.inventory.enums.ItemAttribute import ItemAttribute
from toontown.inventory.enums.ItemEnums import ShortItemType

from toontown.toon import ToonGlobals
from toontown.toonbase import ProcessGlobals


class ShortsItemDefinition(ItemDefinition):
    """
    The definition structure for shorts.
    """
    # Need to pre-load the model, or hammerspace item previews get very laggy
    if ProcessGlobals.getCurrentProcess() == ProcessGlobals.Process.Client:
        ShortsModel = NodePath('ShortsRegistry-ShortsModel')
        tempTorso = loader.loadModel(f"phase_3/{ToonGlobals.TorsoDict['ms']}1000")
        tempTorso.find('**/torso-bot').copyTo(ShortsModel)
        tempTorso.removeNode()

        SkirtModel = NodePath('ShortsRegistry-SkirtModel')
        tempTorso = loader.loadModel(f"phase_3/{ToonGlobals.TorsoDict['md']}1000")
        tempTorso.find('**/torso-bot').copyTo(SkirtModel)
        tempTorso.removeNode()

        del tempTorso

    def __init__(self,
                 texturePath: str,
                 skirt: bool = False,
                 dyeable: bool = False,
                 **kwargs):
        super().__init__(**kwargs)
        self.texturePath = texturePath
        self.skirt = skirt
        self.dyeable = dyeable

    def getItemTypeName(self):
        return 'Shorts'

    def getRewardName(self, item: Optional[InventoryItem] = None):
        return f'{self.getName()} Shorts'

    def getTexture(self) -> Texture:
        tex = loader.loadTexture(self.texturePath)
        tex.setMinfilter(Texture.FTLinearMipmapLinear)
        tex.setMagfilter(Texture.FTLinear)
        return tex

    def getColor(self, item: Optional[InventoryItem] = None):
        if item is None or not self.dyeable:
            return LVecBase4f(1, 1, 1, 1)
        r, g, b, *_ = item.getAttribute(ItemAttribute.CLOTHES_PRIMARY_COL, (1, 1, 1))
        return LVecBase4f(r, g, b, 1)

    def makeItemModel(self, item: Optional[InventoryItem] = None, *extraArgs) -> NodePath:
        if self.isShorts():
            newNode = self.ShortsModel.copyTo(NodePath())
        else:
            newNode = self.SkirtModel.copyTo(NodePath())

        newNode.setTexture(self.getTexture(), 1)
        newNode.setColor(self.getColor(item=item))

        return newNode

    def isSkirt(self) -> bool:
        return self.skirt

    def isShorts(self) -> bool:
        return not self.skirt

    def makeGuiItemModel(self) -> NodePath:
        """
        Creates the GUI item model to be used.
        """
        model = self.makeItemModel()
        for node in model.findAllMatches('*'):
            node.setH(180)
        model.flattenStrong()
        return model


# The registry dictionary for shorts.
ShortsRegistry: Dict[IntEnum, ShortsItemDefinition] = {
    ShortItemType.ShortswithBelt: ShortsItemDefinition(
        name="Shorts with Belt",
        description="No Description",
        texturePath="phase_3/maps/desat_shorts_2.png",
        dyeable=True,
    ),
    ShortItemType.BigPocketsShorts: ShortsItemDefinition(
        name="Big Pockets",
        description="No Description",
        texturePath="phase_3/maps/desat_shorts_4.png",
        dyeable=True,
    ),
    ShortItemType.FeatherShorts: ShortsItemDefinition(
        name="Feather",
        description="No Description",
        texturePath="phase_3/maps/desat_shorts_6.png",
        dyeable=True,
    ),
    ShortItemType.SidestripedShorts: ShortsItemDefinition(
        name="Side-striped",
        description="No Description",
        texturePath="phase_3/maps/desat_shorts_7.png",
        dyeable=True,
    ),
    ShortItemType.AthleticShortsA: ShortsItemDefinition(
        name="Athletic",
        description="No Description",
        texturePath="phase_3/maps/desat_shorts_8.png",
        dyeable=True,
    ),
    ShortItemType.FieryShorts: ShortsItemDefinition(
        name="Fiery",
        description="No Description",
        texturePath="phase_3/maps/desat_shorts_9.png",
        dyeable=True,
    ),
    ShortItemType.JeanShorts: ShortsItemDefinition(
        name="Jean",
        description="No Description",
        texturePath="phase_3/maps/desat_shorts_10.png",
        dyeable=True,
    ),
    ShortItemType.ValentoonsPinkShorts: ShortsItemDefinition(
        name="Valentoon's Pink",
        description="No Description",
        texturePath="phase_4/maps/VdayShorts2.png",
    ),
    ShortItemType.ValentoonsGreenShorts: ShortsItemDefinition(
        name="Valentoon's Green",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_valentine1.png",
    ),
    ShortItemType.JeanHeartShorts: ShortsItemDefinition(
        name="Jean Heart Shorts",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_valentine2.png",
    ),
    ShortItemType.AthleticShortsB: ShortsItemDefinition(
        name="Athletic",
        description="No Description",
        texturePath="phase_4/maps/shorts4.png",
    ),
    ShortItemType.TealAndYellowShorts: ShortsItemDefinition(
        name="Teal & Yellow",
        description="No Description",
        texturePath="phase_4/maps/shorts1.png",
    ),
    ShortItemType.GreenAndYellowShorts: ShortsItemDefinition(
        name="Green & Yellow",
        description="No Description",
        texturePath="phase_4/maps/shortsCat7_01.png",
    ),
    ShortItemType.IdesofMarchShorts: ShortsItemDefinition(
        name="Ides of March",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_greentoon1.png",
    ),
    ShortItemType.SnowmanShortsA: ShortsItemDefinition(
        name="Snowman",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_winter1.png",
    ),
    ShortItemType.SnowflakeShorts: ShortsItemDefinition(
        name="Snowflake",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_winter2.png",
    ),
    ShortItemType.PeppermintShorts: ShortsItemDefinition(
        name="Peppermint",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_winter3.png",
    ),
    ShortItemType.FestiveWinterShorts: ShortsItemDefinition(
        name="Festive Winter",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_winter4.png",
    ),
    ShortItemType.SupertoonShorts: ShortsItemDefinition(
        name="Supertoon",
        description="No Description",
        texturePath="phase_4/maps/halloween/supertoon_outfit/tt_t_chr_avt_shorts_supertoon.png",
    ),
    ShortItemType.GolfingShorts: ShortsItemDefinition(
        name="Golfing",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_golf03.png",
    ),
    ShortItemType.PleatedSkirt: ShortsItemDefinition(
        name="Pleated",
        description="No Description",
        texturePath="phase_3/maps/desat_skirt_1.png",
        skirt=True,
        dyeable=True,
    ),
    ShortItemType.PolkaDotSkirt: ShortsItemDefinition(
        name="Polka Dot",
        description="No Description",
        texturePath="phase_3/maps/desat_skirt_2.png",
        skirt=True,
        dyeable=True,
    ),
    ShortItemType.StripedSkirt: ShortsItemDefinition(
        name="Striped",
        description="No Description",
        texturePath="phase_3/maps/desat_skirt_3.png",
        skirt=True,
        dyeable=True,
    ),
    ShortItemType.BottomStripeSkirt: ShortsItemDefinition(
        name="Bottom Stripe",
        description="No Description",
        texturePath="phase_3/maps/desat_skirt_4.png",
        skirt=True,
        dyeable=True,
    ),
    ShortItemType.FlowersSkirt: ShortsItemDefinition(
        name="Flowers",
        description="No Description",
        texturePath="phase_3/maps/desat_skirt_5.png",
        skirt=True,
        dyeable=True,
    ),
    ShortItemType.JeanPocketsSkirt: ShortsItemDefinition(
        name="Jean Pockets",
        description="No Description",
        texturePath="phase_3/maps/desat_skirt_6.png",
        skirt=True,
        dyeable=True,
    ),
    ShortItemType.DenimSkirt: ShortsItemDefinition(
        name="Denim",
        description="No Description",
        texturePath="phase_3/maps/desat_skirt_7.png",
        skirt=True,
        dyeable=True,
    ),
    ShortItemType.HighPocketsShorts: ShortsItemDefinition(
        name="High Pockets",
        description="No Description",
        texturePath="phase_3/maps/desat_shorts_1.png",
        dyeable=True,
    ),
    ShortItemType.FlowerShorts: ShortsItemDefinition(
        name="Flower",
        description="No Description",
        texturePath="phase_3/maps/desat_shorts_5.png",
        dyeable=True,
    ),
    ShortItemType.BlueAndGoldSkirt: ShortsItemDefinition(
        name="Blue & Gold",
        description="No Description",
        texturePath="phase_4/maps/female_skirt1.png",
        skirt=True,
    ),
    ShortItemType.PinkBowSkirt: ShortsItemDefinition(
        name="Pink Bow",
        description="No Description",
        texturePath="phase_4/maps/female_skirt2.png",
        skirt=True,
    ),
    ShortItemType.BlueGreenStarSkirt: ShortsItemDefinition(
        name="Blue-Green Star",
        description="No Description",
        texturePath="phase_4/maps/female_skirt3.png",
        skirt=True,
    ),
    ShortItemType.RedAndWhiteHeartsSkirt: ShortsItemDefinition(
        name="Red & White Hearts",
        description="No Description",
        texturePath="phase_4/maps/VdaySkirt1.png",
        skirt=True,
    ),
    ShortItemType.ValentoonsHeartsSkirt: ShortsItemDefinition(
        name="Valentoon's Hearts",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_valentine1.png",
        skirt=True,
    ),
    ShortItemType.JeanHeartSkirt: ShortsItemDefinition(
        name="Jean Heart Skirt",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_valentine2.png",
        skirt=True,
    ),
    ShortItemType.RainbowSkirt: ShortsItemDefinition(
        name="Rainbow",
        description="No Description",
        texturePath="phase_4/maps/skirtNew5.png",
        skirt=True,
    ),
    ShortItemType.LuckyCloverShorts: ShortsItemDefinition(
        name="Lucky Clover",
        description="No Description",
        texturePath="phase_4/maps/shorts5.png",
    ),
    ShortItemType.IdesofMarchSkirt: ShortsItemDefinition(
        name="Ides of March",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_greentoon1.png",
        skirt=True,
    ),
    ShortItemType.WesternSkirt: ShortsItemDefinition(
        name="Western",
        description="No Description",
        texturePath="phase_4/maps/CowboySkirt1.png",
        skirt=True,
    ),
    ShortItemType.ZestyWesternSkirt: ShortsItemDefinition(
        name="Zesty Western",
        description="No Description",
        texturePath="phase_4/maps/CowboySkirt2.png",
        skirt=True,
    ),
    ShortItemType.GoldBuckleShorts: ShortsItemDefinition(
        name="Gold Buckle",
        description="No Description",
        texturePath="phase_4/maps/CowboyShorts1.png",
    ),
    ShortItemType.SilverBuckleShorts: ShortsItemDefinition(
        name="Silver Buckle",
        description="No Description",
        texturePath="phase_4/maps/CowboyShorts2.png",
    ),
    ShortItemType.July4thShorts: ShortsItemDefinition(
        name="July 4th",
        description="No Description",
        texturePath="phase_4/maps/4thJulyShorts1.png",
    ),
    ShortItemType.July4thSkirt: ShortsItemDefinition(
        name="July 4th",
        description="No Description",
        texturePath="phase_4/maps/4thJulySkirt1.png",
        skirt=True,
    ),
    ShortItemType.DaisySkirt: ShortsItemDefinition(
        name="Daisy",
        description="No Description",
        texturePath="phase_4/maps/skirtCat7_01.png",
        skirt=True,
    ),
    ShortItemType.BananaPeelShorts: ShortsItemDefinition(
        name="Banana Peel",
        description="No Description",
        texturePath="phase_4/maps/Blue_shorts_1.png",
    ),
    ShortItemType.BikeHornShorts: ShortsItemDefinition(
        name="Bike Horn",
        description="No Description",
        texturePath="phase_4/maps/Red_shorts_1.png",
    ),
    ShortItemType.HypnoGogglesShorts: ShortsItemDefinition(
        name="Hypno Goggles",
        description="No Description",
        texturePath="phase_4/maps/Purple_shorts_1.png",
    ),
    ShortItemType.SnowmanSkirt: ShortsItemDefinition(
        name="Snowman",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_winter1.png",
        skirt=True,
    ),
    ShortItemType.SnowflakesSkirt: ShortsItemDefinition(
        name="Snowflakes",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_winter2.png",
        skirt=True,
    ),
    ShortItemType.PeppermintSkirt: ShortsItemDefinition(
        name="Peppermint",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_winter3.png",
        skirt=True,
    ),
    ShortItemType.FestiveWinterSkirt: ShortsItemDefinition(
        name="Festive Winter",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_winter4.png",
        skirt=True,
    ),
    ShortItemType.FishingShorts: ShortsItemDefinition(
        name="Fishing",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_fishing1.png",
    ),
    ShortItemType.GardeningShorts: ShortsItemDefinition(
        name="Gardening",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_gardening1.png",
    ),
    ShortItemType.PartyShorts: ShortsItemDefinition(
        name="Party",
        description="You'll be the life of the party!",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_party1.png",
    ),
    ShortItemType.CheckeredRacingShorts: ShortsItemDefinition(
        name="Checkered Racing",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_racing1.png",
    ),
    ShortItemType.GoldfishShorts: ShortsItemDefinition(
        name="Goldfish",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_summer1.png",
    ),
    ShortItemType.GreenPlaidGolfingShorts: ShortsItemDefinition(
        name="Green Plaid Golfing",
        description="Great for camouflage!",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_golf1.png",
    ),
    ShortItemType.BeeShorts: ShortsItemDefinition(
        name="Bee",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_bee.png",
    ),
    ShortItemType.SaveTheBuildingsShorts: ShortsItemDefinition(
        name="Save The Buildings",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_saveBuilding1.png",
    ),
    ShortItemType.TrolleyShorts: ShortsItemDefinition(
        name="Trolley",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_trolley1.png",
    ),
    ShortItemType.SpiderShorts: ShortsItemDefinition(
        name="Spider",
        description="No Description",
        texturePath="phase_4/maps/halloween/spider_outfit/tt_t_chr_avt_shorts_halloween4.png",
    ),
    ShortItemType.SkeletoonShorts: ShortsItemDefinition(
        name="Skeletoon",
        description="No Description",
        texturePath="phase_4/maps/halloween/skeleton_outfit/tt_t_chr_avt_shorts_halloween3.png",
    ),
    ShortItemType.BlueRacingShorts: ShortsItemDefinition(
        name="Blue Racing",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_racingGrandPrix.png",
    ),
    ShortItemType.IndigoRacingShorts: ShortsItemDefinition(
        name="Indigo Racing",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_racing03.png",
    ),
    ShortItemType.TanGolfingShorts: ShortsItemDefinition(
        name="Tan Golfing",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_golf04.png",
    ),
    ShortItemType.CheckeredGolfShorts: ShortsItemDefinition(
        name="Checkered Golf",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_golf05.png",
    ),
    ShortItemType.DarkBlueRacingShorts: ShortsItemDefinition(
        name="Dark Blue Racing",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_racing04.png",
    ),
    ShortItemType.RacingStripeShorts: ShortsItemDefinition(
        name="Racing w/ Stripe",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_racing05.png",
    ),
    ShortItemType.FishingSkirt: ShortsItemDefinition(
        name="Fishing",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_fishing1.png",
        skirt=True,
    ),
    ShortItemType.GardeningSkirt: ShortsItemDefinition(
        name="Gardening",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_gardening1.png",
        skirt=True,
    ),
    ShortItemType.PartySkirt: ShortsItemDefinition(
        name="Party",
        description="For when you want that extra swish when you dance!",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_party1.png",
        skirt=True,
    ),
    ShortItemType.RedCheckeredSkirt: ShortsItemDefinition(
        name="Red Checkered",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_racing1.png",
        skirt=True,
    ),
    ShortItemType.GrassSkirt: ShortsItemDefinition(
        name="Grass",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_summer1.png",
        skirt=True,
    ),
    ShortItemType.PinkPlaidGolfSkirt: ShortsItemDefinition(
        name="Pink Plaid Golf",
        description="Not great for camouflage!",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_golf1.png",
        skirt=True,
    ),
    ShortItemType.BeeSkirt: ShortsItemDefinition(
        name="Bee",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_halloween1.png",
        skirt=True,
    ),
    ShortItemType.SupertoonSkirt: ShortsItemDefinition(
        name="Supertoon",
        description="No Description",
        texturePath="phase_4/maps/halloween/supertoon_outfit/tt_t_chr_avt_skirt_halloween2.png",
        skirt=True,
    ),
    ShortItemType.SaveTheBuildingsSkirt: ShortsItemDefinition(
        name="Save The Buildings",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_saveBuilding1.png",
        skirt=True,
    ),
    ShortItemType.TrolleySkirt: ShortsItemDefinition(
        name="Trolley",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_trolley1.png",
        skirt=True,
    ),
    ShortItemType.SkeletoonSkirt: ShortsItemDefinition(
        name="Skeletoon",
        description="No Description",
        texturePath="phase_4/maps/halloween/skeleton_outfit/tt_t_chr_avt_skirt_halloween3.png",
        skirt=True,
    ),
    ShortItemType.SpiderSkirt: ShortsItemDefinition(
        name="Spider",
        description="No Description",
        texturePath="phase_4/maps/halloween/spider_outfit/tt_t_chr_avt_skirt_halloween4.png",
        skirt=True,
    ),
    ShortItemType.CogCrusherShorts: ShortsItemDefinition(
        name="Cog-Crusher Shorts",
        description="The suit for the most masterful of Gag-wielding! If you don't mind looking like a banana.",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_cogbuster.png",
    ),
    ShortItemType.SellbotCrusherShorts: ShortsItemDefinition(
        name="Sellbot Crusher",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_sellbotCrusher.png",
    ),
    ShortItemType.BlueCheckeredRacingSkirt: ShortsItemDefinition(
        name="Blue Checkered Racing",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_racingGrandPrix.png",
        skirt=True,
    ),
    ShortItemType.StarryGolfingSkirt: ShortsItemDefinition(
        name="Starry Golfing",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_golf02.png",
        skirt=True,
    ),
    ShortItemType.IndigoRacingSkirt: ShortsItemDefinition(
        name="Indigo Racing",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_racing03.png",
        skirt=True,
    ),
    ShortItemType.RainbowGolfingSkirt: ShortsItemDefinition(
        name="Rainbow Golfing",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_golf03.png",
        skirt=True,
    ),
    ShortItemType.BluePlaidGolfingSkirt: ShortsItemDefinition(
        name="Blue Plaid Golfing",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_golf04.png",
        skirt=True,
    ),
    ShortItemType.DarkBlueRacingSkirt: ShortsItemDefinition(
        name="Dark Blue Racing",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_racing04.png",
        skirt=True,
    ),
    ShortItemType.RacingStripeSkirt: ShortsItemDefinition(
        name="Racing w/ Stripe",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_racing05.png",
        skirt=True,
    ),
    ShortItemType.ScientistAShorts: ShortsItemDefinition(
        name="Scientist A",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_shorts_scientistA.png",
    ),
    ShortItemType.ScientistBShorts: ShortsItemDefinition(
        name="Scientist B",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_shorts_scientistB.png",
    ),
    ShortItemType.ScientistCShorts: ShortsItemDefinition(
        name="Scientist C",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_shorts_scientistC.png",
    ),
    ShortItemType.OvercoatVampireShorts: ShortsItemDefinition(
        name="Overcoat Vampire",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_halloween5.png",
    ),
    ShortItemType.TurtleShorts: ShortsItemDefinition(
        name="Turtle",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_halloweenTurtle.png",
    ),
    ShortItemType.PirateShorts: ShortsItemDefinition(
        name="Pirate",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_pirate.png",
    ),
    ShortItemType.PirateSkirt: ShortsItemDefinition(
        name="Pirate",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_pirate.png",
        skirt=True,
    ),
    ShortItemType.VampireShorts: ShortsItemDefinition(
        name="Vampire",
        description="No Description",
        texturePath="phase_4/maps/halloween/dracula_outfit/tt_t_chr_avt_shorts_vampire.png",
    ),
    ShortItemType.ToonosaurShorts: ShortsItemDefinition(
        name="Toonosaur",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_dinosaur.png",
    ),
    ShortItemType.MeatballsShorts: ShortsItemDefinition(
        name="Meatballs",
        description="No really, don't eat it. It's fabric.",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_meatballs.png",
    ),
    ShortItemType.TrashcatsRagsShorts: ShortsItemDefinition(
        name="Trashcat's Rags",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_trashcat.png",
    ),
    ShortItemType.DrowsyDreamlandShorts: ShortsItemDefinition(
        name="Drowsy Dreamland",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_ZZZ.png",
    ),
    ShortItemType.BetaToonShorts: ShortsItemDefinition(
        name="Beta Toon",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_beta.png",
    ),
    ShortItemType.BetaToonSkirt: ShortsItemDefinition(
        name="Beta Toon",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_beta.png",
        skirt=True,
    ),
    ShortItemType.YOTTKnightShorts: ShortsItemDefinition(
        name="YOTT Knight",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_yott.png",
    ),
    ShortItemType.YOTTKnightSkirt: ShortsItemDefinition(
        name="YOTT Knight",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_yott.png",
        skirt=True,
    ),
    ShortItemType.BBSailorShorts: ShortsItemDefinition(
        name="BB Sailor",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_sail.png",
    ),
    ShortItemType.BBSailorSkirt: ShortsItemDefinition(
        name="BB Sailor",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_sail.png",
        skirt=True,
    ),
    ShortItemType.DGGardeningShorts: ShortsItemDefinition(
        name="DG Gardening",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_garden.png",
    ),
    ShortItemType.DGGardeningSkirt: ShortsItemDefinition(
        name="DG Gardening",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_garden.png",
        skirt=True,
    ),
    ShortItemType.TTCFirefighterShorts: ShortsItemDefinition(
        name="TTC Firefighter",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_fire.png",
    ),
    ShortItemType.TTCFirefighterSkirt: ShortsItemDefinition(
        name="TTC Firefighter",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_fire.png",
        skirt=True,
    ),
    ShortItemType.MMLBandShorts: ShortsItemDefinition(
        name="MML Band",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_band.png",
    ),
    ShortItemType.TeamBarnyardShorts: ShortsItemDefinition(
        name="Team Barnyard",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_barnyard.png",
    ),
    ShortItemType.TeamBarnyardSkirt: ShortsItemDefinition(
        name="Team Barnyard",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_barnyard.png",
        skirt=True,
    ),
    ShortItemType.TeamOutbackShorts: ShortsItemDefinition(
        name="Team Outback",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_outback.png",
    ),
    ShortItemType.TeamOutbackSkirt: ShortsItemDefinition(
        name="Team Outback",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_outback.png",
        skirt=True,
    ),
    ShortItemType.AAParkRangerShorts: ShortsItemDefinition(
        name="AA Park Ranger",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_park_ranger.png",
    ),
    ShortItemType.TBSnowflakeShorts: ShortsItemDefinition(
        name="TB Snowflake",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shorts_brrrgh.png",
    ),
    ShortItemType.TBSnowflakeSkirt: ShortsItemDefinition(
        name="TB Snowflake",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_skirt_brrrgh.png",
        skirt=True,
    ),
    ShortItemType.AlchemistShorts: ShortsItemDefinition(
        name="Alchemist",
        description="No Description",
        texturePath="phase_4/maps/halloween/alchemist_outfit/tt_t_chr_avt_shorts_alchemist.png",
    ),
    ShortItemType.AlchemistSkirt: ShortsItemDefinition(
        name="Alchemist",
        description="No Description",
        texturePath="phase_4/maps/halloween/alchemist_outfit/tt_t_chr_avt_skirt_alchemist.png",
        skirt=True,
    ),
    ShortItemType.FrankentoonShorts: ShortsItemDefinition(
        name="Frankentoon",
        description="No Description",
        texturePath="phase_4/maps/halloween/frankenstein_outfit/tt_t_chr_avt_shorts_frankenstien.png",
    ),
    ShortItemType.SpacetoonShorts: ShortsItemDefinition(
        name="Spacetoon",
        description="No Description",
        texturePath="phase_4/maps/halloween/moonsuit_outfit/tt_t_chr_avt_shorts_moonsuit.png",
    ),
    ShortItemType.MadScientistShorts: ShortsItemDefinition(
        name="Mad Scientist",
        description="No Description",
        texturePath="phase_4/maps/halloween/scientistD_outfit/tt_t_chr_avt_shorts_scientistd.png",
    ),
    ShortItemType.ClownShortsA: ShortsItemDefinition(
        name="Clown",
        description="No Description",
        texturePath="phase_4/maps/halloween/clown_outfit/tt_t_chr_avt_shorts_clown.png",
    ),
    ShortItemType.ClownSkirtA: ShortsItemDefinition(
        name="Clown",
        description="No Description",
        texturePath="phase_4/maps/halloween/clown_outfit/tt_t_chr_avt_skirt_clown.png",
        skirt=True,
    ),
    ShortItemType.WonderlandShorts: ShortsItemDefinition(
        name="Wonderland",
        description="No Description",
        texturePath="phase_4/maps/halloween/toons_in_wonderland_outfit/tt_t_chr_avt_shorts_tiw.png",
    ),
    ShortItemType.WonderlandSkirt: ShortsItemDefinition(
        name="Wonderland",
        description="No Description",
        texturePath="phase_4/maps/halloween/toons_in_wonderland_outfit/tt_t_chr_avt_skirt_tiw.png",
        skirt=True,
    ),
    ShortItemType.ReaperShorts: ShortsItemDefinition(
        name="Reaper",
        description="No Description",
        texturePath="phase_4/maps/halloween/reaper_outfit/tt_t_chr_avt_shorts_reaper.png",
    ),
    ShortItemType.ReaperSkirt: ShortsItemDefinition(
        name="Reaper",
        description="No Description",
        texturePath="phase_4/maps/halloween/reaper_outfit/tt_t_chr_avt_skirt_reaper.png",
        skirt=True,
    ),
    ShortItemType.ScarecrowShorts: ShortsItemDefinition(
        name="Scarecrow Shorts",
        description="No Description",
        texturePath="phase_4/maps/halloween/scarecrow_outfit/tt_t_chr_avt_shorts_scarecrow.png",
    ),
    ShortItemType.ScarecrowSkirt: ShortsItemDefinition(
        name="Scarecrow Skirt",
        description="No Description",
        texturePath="phase_4/maps/halloween/scarecrow_outfit/tt_t_chr_avt_skirt_scarecrow.png",
        skirt=True,
    ),
    ShortItemType.WitchShorts: ShortsItemDefinition(
        name="Witch",
        description="No Description",
        texturePath="phase_4/maps/halloween/witch_outfit/tt_t_chr_avt_shorts_witch.png",
    ),
    ShortItemType.WitchSkirt: ShortsItemDefinition(
        name="Witch",
        description="No Description",
        texturePath="phase_4/maps/halloween/witch_outfit/tt_t_chr_avt_skirt_witch.png",
        skirt=True,
    ),
    ShortItemType.GreenElfShorts: ShortsItemDefinition(
        name="Green Elf",
        description="No Description",
        texturePath="phase_4/maps/winter/elf_green_outfit/tt_t_chr_avt_shorts_elf_green.png",
    ),
    ShortItemType.RedElfShorts: ShortsItemDefinition(
        name="Red Elf",
        description="No Description",
        texturePath="phase_4/maps/winter/elf_red_outfit/tt_t_chr_avt_shorts_elf_red.png",
    ),
    ShortItemType.GingerbreadShorts: ShortsItemDefinition(
        name="Gingerbread",
        description="No Description",
        texturePath="phase_4/maps/winter/gingerbread_outfit/tt_t_chr_avt_shorts_gingerbread.png",
    ),
    ShortItemType.GingerbreadSkirt: ShortsItemDefinition(
        name="Gingerbread Skirt",
        description="No Description",
        texturePath="phase_4/maps/winter/gingerbread_outfit/tt_t_chr_avt_skirt_gingerbread.png",
        skirt=True,
    ),
    ShortItemType.PresentUniformShorts: ShortsItemDefinition(
        name="Present Uniform",
        description="No Description",
        texturePath="phase_4/maps/winter/present_delivery_uniform_outfit/tt_t_chr_avt_shorts_pdu.png",
    ),
    ShortItemType.PresentUniformSkirt: ShortsItemDefinition(
        name="Present Uniform",
        description="No Description",
        texturePath="phase_4/maps/winter/present_delivery_uniform_outfit/tt_t_chr_avt_skirt_pdu.png",
        skirt=True,
    ),
    ShortItemType.RagdollHumbleSkirt: ShortsItemDefinition(
        name="Ragdoll Humble",
        description="No Description",
        texturePath="phase_4/maps/winter/ragdoll_outfits/humble/tt_t_chr_avt_shorts_ragdoll_humble.png",
        skirt=True,
    ),
    ShortItemType.RagdollRegalSkirt: ShortsItemDefinition(
        name="Ragdoll Regal",
        description="No Description",
        texturePath="phase_4/maps/winter/ragdoll_outfits/regal/tt_t_chr_avt_shorts_ragdoll_regal.png",
        skirt=True,
    ),
    ShortItemType.RagdollTraditionalSkirt: ShortsItemDefinition(
        name="Ragdoll Traditional",
        description="No Description",
        texturePath="phase_4/maps/winter/ragdoll_outfits/traditional/tt_t_chr_avt_shorts_ragdoll_traditional.png",
        skirt=True,
    ),
    ShortItemType.ReindeerSkirt: ShortsItemDefinition(
        name="Reindeer",
        description="No Description",
        texturePath="phase_4/maps/winter/reindeer_outfit/tt_t_chr_avt_skirt_reindeer.png",
        skirt=True,
    ),
    ShortItemType.ReindeerShorts: ShortsItemDefinition(
        name="Reindeer",
        description="No Description",
        texturePath="phase_4/maps/winter/reindeer_outfit/tt_t_chr_avt_shorts_reindeer.png",
    ),
    ShortItemType.VintageSnowShorts: ShortsItemDefinition(
        name="Vintage Snow",
        description="No Description",
        texturePath="phase_4/maps/winter/vintage_snow_outfit/tt_t_chr_avt_shorts_vintage_snow.png",
    ),
    ShortItemType.RagdollHumbleShorts: ShortsItemDefinition(
        name="Ragdoll Humble",
        description="No Description",
        texturePath="phase_4/maps/winter/ragdoll_outfits/male_shorts/humble-ragdoll-bot.png",
    ),
    ShortItemType.RagdollRegalShorts: ShortsItemDefinition(
        name="Ragdoll Regal",
        description="No Description",
        texturePath="phase_4/maps/winter/ragdoll_outfits/male_shorts/regal-ragdoll-bot.png",
    ),
    ShortItemType.RagdollTraditionalShorts: ShortsItemDefinition(
        name="Ragdoll Traditional",
        description="No Description",
        texturePath="phase_4/maps/winter/ragdoll_outfits/male_shorts/tradi-ragdoll-bot.png",
    ),
    ShortItemType.TinHumbleShorts: ShortsItemDefinition(
        name="Tin Humble",
        description="No Description",
        texturePath="phase_4/maps/winter/tin_soldier_outfits/humble/tt_t_chr_avt_shorts_tin_soldier_humble.png",
    ),
    ShortItemType.TinRegalShorts: ShortsItemDefinition(
        name="Tin Regal",
        description="No Description",
        texturePath="phase_4/maps/winter/tin_soldier_outfits/regal/tt_t_chr_avt_shorts_tin_soldier_regal.png",
    ),
    ShortItemType.TinTraditionalShorts: ShortsItemDefinition(
        name="Tin Traditional",
        description="No Description",
        texturePath="phase_4/maps/winter/tin_soldier_outfits/traditional/tt_t_chr_avt_shorts_tin_soldier_traditional.png",
    ),
    ShortItemType.NY2019SuitShorts: ShortsItemDefinition(
        name="2019 Suit",
        description="No Description",
        texturePath="phase_4/maps/winter/2019_outfit/tt_t_chr_avt_shorts_2019_suit.png",
    ),
    ShortItemType.NY2019DressSkirt: ShortsItemDefinition(
        name="2019 Dress",
        description="No Description",
        texturePath="phase_4/maps/winter/2019_outfit/tt_t_chr_avt_skirt_2019_dress.png",
        skirt=True,
    ),
    ShortItemType.CupidShorts: ShortsItemDefinition(
        name="Cupid Shorts",
        description="No Description",
        texturePath="phase_4/maps/valentoon/tt_t_chr_avt_shorts_cupid.png",
    ),
    ShortItemType.CupidSkirt: ShortsItemDefinition(
        name="Cupid Skirt",
        description="No Description",
        texturePath="phase_4/maps/valentoon/tt_t_chr_avt_skirt_cupid.png",
        skirt=True,
    ),
    ShortItemType.WebstersShorts: ShortsItemDefinition(
        name="Webster's Shorts",
        description="No Description",
        texturePath="phase_4/maps/social/webster/tt_t_chr_avt_shorts_webster.png",
    ),
    ShortItemType.DoesSkirt: ShortsItemDefinition(
        name="Doe's Skirt",
        description="No Description",
        texturePath="phase_4/maps/social/doe/tt_t_chr_avt_skirt_doe.png",
        skirt=True,
    ),
    ShortItemType.AviatorShorts: ShortsItemDefinition(
        name="Aviator Shorts",
        description="Sky Clan, here we come!",
        texturePath="phase_4/maps/apriltoons/aviator_outfit/tt_t_chr_avt_shorts_aviator_bot.png",
    ),
    ShortItemType.WingsuitShorts: ShortsItemDefinition(
        name="Wingsuit Shorts",
        description="It might allow you to fly... not Loony Labs certified.",
        texturePath="phase_4/maps/apriltoons/wingsuit_outfit/tt_t_chr_avt_shorts_wingsuit.png",
    ),
    ShortItemType.SellbotSeekerSkirt: ShortsItemDefinition(
        name="Sellbot Seeker",
        description="No Description",
        texturePath="phase_4/maps/dept_uniforms/sellbotuniform_skirt.png",
        skirt=True,
    ),
    ShortItemType.SellbotSeekerShorts: ShortsItemDefinition(
        name="Sellbot Seeker",
        description="No Description",
        texturePath="phase_4/maps/dept_uniforms/sellbotuniform_bot.png",
    ),
    ShortItemType.CashbotCatcherSkirt: ShortsItemDefinition(
        name="Cashbot Catcher",
        description="No Description",
        texturePath="phase_4/maps/dept_uniforms/cashbotuniform_skirt.png",
        skirt=True,
    ),
    ShortItemType.CashbotCatcherShorts: ShortsItemDefinition(
        name="Cashbot Catcher",
        description="No Description",
        texturePath="phase_4/maps/dept_uniforms/cashbotuniform_bot.png",
    ),
    ShortItemType.LawbotLiberatorSkirt: ShortsItemDefinition(
        name="Lawbot Liberator",
        description="No Description",
        texturePath="phase_4/maps/dept_uniforms/lawbotuniform_skirt.png",
        skirt=True,
    ),
    ShortItemType.LawbotLiberatorShorts: ShortsItemDefinition(
        name="Lawbot Liberator",
        description="No Description",
        texturePath="phase_4/maps/dept_uniforms/lawbotuniform_bot.png",
    ),
    ShortItemType.BossbotBasherSkirt: ShortsItemDefinition(
        name="Bossbot Basher",
        description="No Description",
        texturePath="phase_4/maps/dept_uniforms/bossbotuniform_skirt.png",
        skirt=True,
    ),
    ShortItemType.BossbotBasherShorts: ShortsItemDefinition(
        name="Bossbot Basher",
        description="No Description",
        texturePath="phase_4/maps/dept_uniforms/bossbotuniform_bot.png",
    ),
    ShortItemType.OutbackUniformShorts: ShortsItemDefinition(
        name="Outback Uniform",
        description="No Description",
        texturePath="phase_4/maps/outback/tt_t_chr_avt_shorts_outback_uniform.png",
    ),
    ShortItemType.OutbackUniformSkirt: ShortsItemDefinition(
        name="Outback Uniform",
        description="No Description",
        texturePath="phase_4/maps/outback/tt_t_chr_avt_skirt_outback_uniform.png",
        skirt=True,
    ),
    ShortItemType.AlienShorts: ShortsItemDefinition(
        name="Alien Shorts",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/alien_bot.png",
    ),
    ShortItemType.CandyCornShorts: ShortsItemDefinition(
        name="Candy Corn Shorts",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/candycorn_bot.png",
    ),
    ShortItemType.LawbotResistanceShorts: ShortsItemDefinition(
        name="Lawbot Resistance",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/l_resist_bot.png",
    ),
    ShortItemType.LawbotResistanceSkirt: ShortsItemDefinition(
        name="Lawbot Resistance",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/l_resist_skirt.png",
        skirt=True,
    ),
    ShortItemType.RetroRobotShorts: ShortsItemDefinition(
        name="Retro Robot Shorts",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/retrobot_bot.png",
    ),
    ShortItemType.RidingHoodShorts: ShortsItemDefinition(
        name="Riding Hood",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/ridinghood_bot.png",
    ),
    ShortItemType.RidingHoodSkirt: ShortsItemDefinition(
        name="Riding Hood",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/ridinghood_skirt.png",
        skirt=True,
    ),
    ShortItemType.NurseShorts: ShortsItemDefinition(
        name="Nurse Shorts",
        description="Laugh your way to good laff!",
        texturePath="phase_13/maps/events/btl/clothing/nurse_bot.png",
    ),
    ShortItemType.NurseSkirt: ShortsItemDefinition(
        name="Nurse Skirt",
        description="Laugh your way to good laff!",
        texturePath="phase_13/maps/events/btl/clothing/nurse_skirt.png",
        skirt=True,
    ),
    ShortItemType.LazyBonesShorts: ShortsItemDefinition(
        name="Lazy Bones",
        description="No Description",
        texturePath="phase_4/maps/halloween/lazy_bones_outfit/lazy_bones_bot.png",
    ),
    ShortItemType.SailorShorts: ShortsItemDefinition(
        name="Sailor Shorts",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_bot_white.png",
    ),
    ShortItemType.SailorSkirt: ShortsItemDefinition(
        name="Sailor Skirt",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_skirt_white.png",
        skirt=True,
    ),
    ShortItemType.BlueSailorShorts: ShortsItemDefinition(
        name="Blue Sailor Shorts",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_bot_blue.png",
    ),
    ShortItemType.BlueSailorSkirt: ShortsItemDefinition(
        name="Blue Sailor Skirt",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_skirt_blue.png",
        skirt=True,
    ),
    ShortItemType.CyanSailorShorts: ShortsItemDefinition(
        name="Cyan Sailor Shorts",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_bot_cyan.png",
    ),
    ShortItemType.CyanSailorSkirt: ShortsItemDefinition(
        name="Cyan Sailor Skirt",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_skirt_cyan.png",
        skirt=True,
    ),
    ShortItemType.GreenSailorShorts: ShortsItemDefinition(
        name="Green Sailor Shorts",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_bot_green.png",
    ),
    ShortItemType.GreenSailorSkirt: ShortsItemDefinition(
        name="Green Sailor Skirt",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_skirt_green.png",
        skirt=True,
    ),
    ShortItemType.OrangeSailorShorts: ShortsItemDefinition(
        name="Orange Sailor Shorts",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_bot_orange.png",
    ),
    ShortItemType.OrangeSailorSkirt: ShortsItemDefinition(
        name="Orange Sailor Skirt",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_skirt_orange.png",
        skirt=True,
    ),
    ShortItemType.PinkSailorShorts: ShortsItemDefinition(
        name="Pink Sailor Shorts",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_bot_pink.png",
    ),
    ShortItemType.PinkSailorSkirt: ShortsItemDefinition(
        name="Pink Sailor Skirt",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_skirt_pink.png",
        skirt=True,
    ),
    ShortItemType.PurpleSailorShorts: ShortsItemDefinition(
        name="Purple Sailor Shorts",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_bot_purple.png",
    ),
    ShortItemType.PurpleSailorSkirt: ShortsItemDefinition(
        name="Purple Sailor Skirt",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_skirt_purple.png",
        skirt=True,
    ),
    ShortItemType.RedSailorShorts: ShortsItemDefinition(
        name="Red Sailor Shorts",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_bot_red.png",
    ),
    ShortItemType.RedSailorSkirt: ShortsItemDefinition(
        name="Red Sailor Skirt",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_skirt_red.png",
        skirt=True,
    ),
    ShortItemType.BlackSailorShorts: ShortsItemDefinition(
        name="Black Sailor Shorts",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_bot_black.png",
    ),
    ShortItemType.BlackSailorSkirt: ShortsItemDefinition(
        name="Black Sailor Skirt",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_skirt_black.png",
        skirt=True,
    ),
    ShortItemType.GoldenSailorShorts: ShortsItemDefinition(
        name="Golden Sailor Shorts",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_bot_yellow.png",
    ),
    ShortItemType.GoldenSailorSkirt: ShortsItemDefinition(
        name="Golden Sailor Skirt",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_skirt_yellow.png",
        skirt=True,
    ),
    ShortItemType.TeamTreesShorts: ShortsItemDefinition(
        name="Team Trees",
        description="No Description",
        texturePath="phase_13/maps/events/trees/tree_shorts.png",
    ),
    ShortItemType.HomemadeRagdollShorts: ShortsItemDefinition(
        name="Homemade Ragdoll",
        description="No Description",
        texturePath="phase_4/maps/winter/homemade_ragdoll/ragdoll_homemade_bot.png",
    ),
    ShortItemType.HomemadeRagdollSkirt: ShortsItemDefinition(
        name="Homemade Ragdoll",
        description="No Description",
        texturePath="phase_4/maps/winter/homemade_ragdoll/ragdoll_homemade_skirt.png",
        skirt=True,
    ),
    ShortItemType.HomemadeSoldierShorts: ShortsItemDefinition(
        name="Homemade Soldier",
        description="No Description",
        texturePath="phase_4/maps/winter/homemade_tin_soldier/soldier_homemade_bot.png",
    ),
    ShortItemType.RetroWinterShorts: ShortsItemDefinition(
        name="Retro Winter",
        description="No Description",
        texturePath="phase_4/maps/winter/retro_winterwear/wintersuit_bot.png",
    ),
    ShortItemType.RetroWinterSkirt: ShortsItemDefinition(
        name="Retro Winter",
        description="No Description",
        texturePath="phase_4/maps/winter/retro_winterwear/winterdress_skirt.png",
        skirt=True,
    ),
    ShortItemType.SnowmanShortsB: ShortsItemDefinition(
        name="Snowman",
        description="No Description",
        texturePath="phase_4/maps/winter/snowman_outfit/snowman_bot.png",
    ),
    ShortItemType.NewYears2020Shorts: ShortsItemDefinition(
        name="New Year's 2020",
        description="No Description",
        texturePath="phase_4/maps/winter/2020_outfit/2020suit_bot.png",
    ),
    ShortItemType.NewYears2020Skirt: ShortsItemDefinition(
        name="New Year's 2020",
        description="No Description",
        texturePath="phase_4/maps/winter/2020_outfit/2020suit_skirt.png",
        skirt=True,
    ),
    ShortItemType.AgentSevenSkirt: ShortsItemDefinition(
        name="Agent Seven",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/seven_skirt.png",
        skirt=True,
    ),
    ShortItemType.StPattys2020Skirt: ShortsItemDefinition(
        name="St. Patty's 2020",
        description="No Description",
        texturePath="phase_13/maps/events/stpats/lucky_skirt.png",
        skirt=True,
    ),
    ShortItemType.StPattys2020Shorts: ShortsItemDefinition(
        name="St. Patty's 2020",
        description="No Description",
        texturePath="phase_13/maps/events/stpats/lucky_bot.png",
    ),
    ShortItemType.ClownSkirtB: ShortsItemDefinition(
        name="Clown",
        description="Who thought Toons could get any sillier?",
        texturePath="phase_13/maps/events/apriltoons/clothing/clown_skirt.png",
        skirt=True,
    ),
    ShortItemType.ClownShortsB: ShortsItemDefinition(
        name="Clown",
        description="Who thought Toons could get any sillier?",
        texturePath="phase_13/maps/events/apriltoons/clothing/clown_bot.png",
    ),
    ShortItemType.SevenStripedSkirt: ShortsItemDefinition(
        name="Seven Striped",
        description="Jackpot!",
        texturePath="phase_13/maps/events/apriltoons/clothing/sevenjersey_skirt.png",
        skirt=True,
    ),
    ShortItemType.SevenStripedShorts: ShortsItemDefinition(
        name="Seven Striped",
        description="Jackpot!",
        texturePath="phase_13/maps/events/apriltoons/clothing/sevenjersey_bot.png",
    ),
    ShortItemType.TripleRainbowSkirt: ShortsItemDefinition(
        name="Triple Rainbow",
        description="Triple rainbow! What does it mean?",
        texturePath="phase_13/maps/events/apriltoons/clothing/triplerainbow_skirt.png",
        skirt=True,
    ),
    ShortItemType.TripleRainbowShorts: ShortsItemDefinition(
        name="Triple Rainbow",
        description="Triple rainbow! What does it mean?",
        texturePath="phase_13/maps/events/apriltoons/clothing/triplerainbow_bot.png",
    ),
    ShortItemType.BoardbotShorts: ShortsItemDefinition(
        name="Boardbot",
        description="No Description",
        texturePath="phase_4/maps/social/discord/cc_t_clth_shorts_promo_chairman.png",
    ),
    ShortItemType.JesterSkirt: ShortsItemDefinition(
        name="Jester",
        description="Popularized in Ye Olde Toontowne!",
        texturePath="phase_13/maps/events/apriltoons/clothing/jester_skirt.png",
        skirt=True,
    ),
    ShortItemType.JesterShorts: ShortsItemDefinition(
        name="Jester",
        description="Popularized in Ye Olde Toontowne!",
        texturePath="phase_13/maps/events/apriltoons/clothing/jester_bot.png",
    ),
    ShortItemType.BlackJesterSkirt: ShortsItemDefinition(
        name="Black Jester Skirt",
        description="Popularized in Ye Olde Toontowne!",
        texturePath="phase_13/maps/events/apriltoons/clothing/jesterblack_skirt.png",
        skirt=True,
    ),
    ShortItemType.BlackJesterShorts: ShortsItemDefinition(
        name="Black Jester Shorts",
        description="Popularized in Ye Olde Toontowne!",
        texturePath="phase_13/maps/events/apriltoons/clothing/jesterblack_bot.png",
    ),
    ShortItemType.Easter2020Shorts: ShortsItemDefinition(
        name="Easter 2020",
        description="No Description",
        texturePath="phase_13/maps/events/easter2020/easter_2020_shorts.png",
    ),
    ShortItemType.Easter2020Skirt: ShortsItemDefinition(
        name="Easter 2020",
        description="No Description",
        texturePath="phase_13/maps/events/easter2020/easter_2020_skirt.png",
        skirt=True,
    ),
    ShortItemType.LawbotSuitPants: ShortsItemDefinition(
        name="Lawbot Suit Pants",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/lawsuit_bot.png",
    ),
    ShortItemType.CooktheCogsShorts: ShortsItemDefinition(
        name="Cook the Cogs",
        description="No Description",
        texturePath="phase_13/maps/events/july4/clothing/cook_shorts.png",
    ),
    ShortItemType.CooktheCogsSkirt: ShortsItemDefinition(
        name="Cook the Cogs",
        description="No Description",
        texturePath="phase_13/maps/events/july4/clothing/cook_skirt.png",
        skirt=True,
    ),
    ShortItemType.ExecutiveBoardbotShorts: ShortsItemDefinition(
        name="Executive Boardbot",
        description="No Description",
        texturePath="phase_4/maps/social/discord/cc_t_clth_shorts_promo_chairman_exec.png",
    ),
    ShortItemType.PhantoonShorts: ShortsItemDefinition(
        name="Phantoon",
        description="No Description",
        texturePath="phase_13/maps/events/halloween/phantoon_bot.png",
    ),
    ShortItemType.ToonsmasPastSkirt: ShortsItemDefinition(
        name="Toonsmas Past",
        description="No Description",
        texturePath="phase_4/maps/winter/past_outfit/past_skirt.png",
        skirt=True,
    ),
    ShortItemType.ToonsmasPastShorts: ShortsItemDefinition(
        name="Toonsmas Past",
        description="No Description",
        texturePath="phase_4/maps/winter/past_outfit/past_bot.png",
    ),
    ShortItemType.ToonsmasPresentSkirt: ShortsItemDefinition(
        name="Toonsmas Present",
        description="No Description",
        texturePath="phase_4/maps/winter/present_outfit/present_skirt.png",
        skirt=True,
    ),
    ShortItemType.ToonsmasPresentShorts: ShortsItemDefinition(
        name="Toonsmas Present",
        description="No Description",
        texturePath="phase_4/maps/winter/present_outfit/present_bot.png",
    ),
    ShortItemType.ToonsmasFutureSkirt: ShortsItemDefinition(
        name="Toonsmas Future",
        description="No Description",
        texturePath="phase_4/maps/winter/future_outfit/future_skirt.png",
        skirt=True,
    ),
    ShortItemType.ToonsmasFutureShorts: ShortsItemDefinition(
        name="Toonsmas Future",
        description="No Description",
        texturePath="phase_4/maps/winter/future_outfit/future_bot.png",
    ),
    ShortItemType.NewYears2021Skirt: ShortsItemDefinition(
        name="New Year's 2021",
        description="No Description",
        texturePath="phase_4/maps/winter/2021_outfit/fireworks_skirt.png",
        skirt=True,
    ),
    ShortItemType.NewYears2021Shorts: ShortsItemDefinition(
        name="New Year's 2021",
        description="No Description",
        texturePath="phase_4/maps/winter/2021_outfit/fireworks_bot.png",
    ),
    ShortItemType.TumblesShorts: ShortsItemDefinition(
        name="Tumbles' Shorts",
        description="No Description",
        texturePath="phase_4/maps/tumbles/tumbles_shorts.png",
    ),
    ShortItemType.HallowopolisShorts: ShortsItemDefinition(
        name="Hallowopolis Shorts",
        description="No Description",
        texturePath="phase_4/maps/halloween/halloweentown_outfit/hwtown_bot.png",
    ),
    ShortItemType.DetectiveShorts: ShortsItemDefinition(
        name="Detective",
        description="No Description",
        texturePath="phase_4/maps/halloween/detective_outfit/mystery_bot.png",
    ),
    ShortItemType.FloralShorts: ShortsItemDefinition(
        name="Floral Shorts",
        description="No Description",
        texturePath="phase_4/maps/halloween/misc_outfit/floral_bot.png",
    ),
    ShortItemType.BlueNewstoonShorts: ShortsItemDefinition(
        name="Blue Newstoon Shorts",
        description="No Description",
        texturePath="phase_4/maps/social/newstoon_blue/newstoon-blue_bot.png",
    ),
    ShortItemType.BlueNewstoonSkirt: ShortsItemDefinition(
        name="Blue Newstoon Skirt",
        description="No Description",
        texturePath="phase_4/maps/social/newstoon_blue/newstoon-blue_skirt.png",
        skirt=True,
    ),
    ShortItemType.GrayNewstoonShorts: ShortsItemDefinition(
        name="Gray Newstoon Shorts",
        description="No Description",
        texturePath="phase_4/maps/social/newstoon_gray/newstoon-gray_bot.png",
    ),
    ShortItemType.GrayNewstoonSkirt: ShortsItemDefinition(
        name="Gray Newstoon Skirt",
        description="No Description",
        texturePath="phase_4/maps/social/newstoon_gray/newstoon-gray_skirt.png",
        skirt=True,
    ),
    ShortItemType.ChupShorts: ShortsItemDefinition(
        name="Chup Shorts",
        description="No Description",
        texturePath="phase_4/maps/halloween/chup_outfit/tt_t_chr_shorts_chup.png",
    ),
    ShortItemType.ChupSkirt: ShortsItemDefinition(
        name="Chup Skirt",
        description="No Description",
        texturePath="phase_4/maps/halloween/chup_outfit/tt_t_chr_skirt_chup.png",
        skirt=True,
    ),
    ShortItemType.NewYears2022Shorts: ShortsItemDefinition(
        name="New Year's 2022",
        description="No Description",
        texturePath="phase_4/maps/winter/2022_outfit/2022_bot.png",
    ),
    ShortItemType.NewYears2022Skirt: ShortsItemDefinition(
        name="New Year's 2022",
        description="No Description",
        texturePath="phase_4/maps/winter/2022_outfit/2022_skirt.png",
        skirt=True,
    ),
    ShortItemType.DoctorToonShorts: ShortsItemDefinition(
        name="Doctor Toon Shorts",
        description="No Description",
        texturePath="phase_4/maps/social/doctor_toon/tt_t_chr_avt_shorts_doctortoon.png",
    ),
    ShortItemType.DoctorToonSkirt: ShortsItemDefinition(
        name="Doctor Toon Skirt",
        description="No Description",
        texturePath="phase_4/maps/social/doctor_toon/tt_t_chr_avt_skirt_doctortoon.png",
        skirt=True,
    ),
    ShortItemType.TrolleyEngineerShorts: ShortsItemDefinition(
        name="Trolley Engineer Shorts",
        description="All aboard!",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shorts_engineer.png",
    ),
    ShortItemType.TrolleyEngineerSkirt: ShortsItemDefinition(
        name="Trolley Engineer Skirt",
        description="All aboard!",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_skirt_engineer.png",
        skirt=True,
    ),
    ShortItemType.StarstruckSkirt: ShortsItemDefinition(
        name="Starstruck Skirt",
        description="You'll outshine the moon with this one!",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_skirt_moon.png",
        skirt=True,
    ),
    ShortItemType.RetroShorts: ShortsItemDefinition(
        name="Retro Shorts",
        description="Friday night fever!",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shorts_funky.png",
    ),
    ShortItemType.StarstruckShorts: ShortsItemDefinition(
        name="Starstruck Shorts",
        description="You'll outshine the moon with this one!",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shorts_moon.png",
    ),
    ShortItemType.SleepwalkerShorts: ShortsItemDefinition(
        name="Sleepwalker Shorts",
        description="Sleep tight!",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shorts_sleepwalker.png",
    ),
    ShortItemType.FruitPieShorts: ShortsItemDefinition(
        name="Fruit Pie Shorts",
        description="Tastes good, too!",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shorts_fruitpie.png",
    ),
    ShortItemType.FruitPieSkirt: ShortsItemDefinition(
        name="Fruit Pie Skirt",
        description="Tastes good, too!",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_skirt_fruitpie.png",
        skirt=True,
    ),
    ShortItemType.GumballMachineShorts: ShortsItemDefinition(
        name="Gumball Machine Shorts",
        description="Full of flavor!",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shorts_gumball.png",
    ),
    ShortItemType.GumballMachineSkirt: ShortsItemDefinition(
        name="Gumball Machine Skirt",
        description="Full of flavor!",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_skirt_gumball.png",
        skirt=True,
    ),
    ShortItemType.CardSuitShorts: ShortsItemDefinition(
        name="Card Suit Shorts",
        description="You've got to know when to hold 'em and when to fold 'em.",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shorts_cards.png",
    ),
    ShortItemType.CardSuitSkirt: ShortsItemDefinition(
        name="Card Suit Skirt",
        description="You've got to know when to hold 'em and when to fold 'em.",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_skirt_cards.png",
        skirt=True,
    ),
    ShortItemType.PainterShorts: ShortsItemDefinition(
        name="Painter Shorts",
        description="Paint not included.",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shorts_painter.png",
    ),
    ShortItemType.PainterSkirt: ShortsItemDefinition(
        name="Painter Skirt",
        description="Paint not included.",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_skirt_painter.png",
        skirt=True,
    ),
    ShortItemType.ChefShorts: ShortsItemDefinition(
        name="Chef Shorts",
        description="No Description",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shorts_chef.png",
    ),
    ShortItemType.ChefSkirt: ShortsItemDefinition(
        name="Chef Skirt",
        description="No Description",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_skirt_chef.png",
        skirt=True,
    ),
    ShortItemType.NewYears2023Shorts: ShortsItemDefinition(
        name="New Year's 2023",
        description="No Description",
        texturePath="phase_4/maps/winter/2023_outfit/2023_bot.png",
    ),
    ShortItemType.NewYears2023Skirt: ShortsItemDefinition(
        name="New Year's 2023",
        description="No Description",
        texturePath="phase_4/maps/winter/2023_outfit/2023_skirt.png",
        skirt=True,
    ),
    ShortItemType.ArmoredPants: ShortsItemDefinition(
        name="Armored Pants",
        description="No Description",
        texturePath="phase_4/maps/bosses/tt_t_chr_avt_shorts_armor.png",
    ),
    ShortItemType.ArmoredSkirt: ShortsItemDefinition(
        name="Armored Skirt",
        description="No Description",
        texturePath="phase_4/maps/bosses/tt_t_chr_avt_skirt_armor.png",
        skirt=True,
    ),
    ShortItemType.HighRollersSuitShorts: ShortsItemDefinition(
        name="High Roller's Suit",
        description="No Description",
        texturePath="phase_4/maps/apriltoons/high_roller_outfit/cc_t_clth_shorts_high_roller.png",
    ),
    ShortItemType.HighRollersProdigalSuitShorts: ShortsItemDefinition(
        name="High Roller's Prodigal Suit",
        description="No Description",
        texturePath="phase_4/maps/apriltoons/high_roller_outfit/cc_t_clth_shorts_high_roller_black.png",
    ),
    ShortItemType.CybertoonShorts: ShortsItemDefinition(
        name="Cybertoon Shorts",
        description="No Description",
        texturePath="phase_4/maps/social/cyberpunk/cc_t_clth_shorts_cyberpunk.png",
    ),
    ShortItemType.CybertoonSkirt: ShortsItemDefinition(
        name="Cybertoon Skirt",
        description="No Description",
        texturePath="phase_4/maps/social/cyberpunk/cc_t_clth_skirt_cyberpunk.png",
        skirt=True,
    ),
    ShortItemType.BroVinci: ShortsItemDefinition(
        name="Bro Vinci",
        description="No Description",
        texturePath="phase_4/maps/social/bro/tt_t_chr_avt_shorts_bro.png",
    ),
}
