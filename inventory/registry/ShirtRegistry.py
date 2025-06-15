"""
This module contains the item data for shirts.
"""
from panda3d.core import NodePath, Texture, LVecBase4f

from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.base.ItemDefinition import ItemDefinition
from typing import Dict, Optional
from enum import IntEnum

from toontown.inventory.enums.ItemAttribute import ItemAttribute
from toontown.inventory.enums.ItemEnums import ShirtItemType

from toontown.toon import ToonGlobals
from toontown.toonbase import ProcessGlobals


class ShirtItemDefinition(ItemDefinition):
    """
    The definition structure for shirts.
    """
    # Need to pre-load the model, or hammerspace item previews get very laggy
    if ProcessGlobals.getCurrentProcess() == ProcessGlobals.Process.Client:
        ShirtModel = NodePath('ShirtRegistry-ShirtModel')
        tempTorso = loader.loadModel(f"phase_3/{ToonGlobals.TorsoDict['ms']}1000")
        tempTorso.find('**/torso-top').copyTo(ShirtModel)
        tempTorso.find('**/sleeves').copyTo(ShirtModel)
        tempTorso.removeNode()
        del tempTorso

    def __init__(self,
                 texturePath: str,
                 sleeveTexturePath: str,
                 dyeable: bool = False,
                 **kwargs):
        super().__init__(**kwargs)
        self.texturePath = texturePath
        self.sleeveTexturePath = sleeveTexturePath
        self.dyeable = dyeable

    def getItemTypeName(self):
        return 'Shirt'

    def getRewardName(self, item: Optional[InventoryItem] = None):
        return f'{self.getName()} Shirt'

    def getTexture(self) -> Texture:
        tex = loader.loadTexture(self.texturePath)
        tex.setMinfilter(Texture.FTLinearMipmapLinear)
        tex.setMagfilter(Texture.FTLinear)
        return tex

    def getSleeveTexture(self):
        tex = loader.loadTexture(self.sleeveTexturePath)
        tex.setMinfilter(Texture.FTLinearMipmapLinear)
        tex.setMagfilter(Texture.FTLinear)
        return tex

    def getColor(self, item: Optional[InventoryItem] = None):
        if item is None or not self.dyeable:
            return LVecBase4f(1, 1, 1, 1)
        r, g, b, *_ = item.getAttribute(ItemAttribute.CLOTHES_PRIMARY_COL, (1, 1, 1))
        return LVecBase4f(r, g, b, 1)

    def getSleeveColor(self, item: Optional[InventoryItem] = None):
        if item is None or not self.dyeable:
            return LVecBase4f(1, 1, 1, 1)
        r, g, b, *_ = item.getAttribute(ItemAttribute.CLOTHES_SECONDARY_COL,
                                        item.getAttribute(ItemAttribute.CLOTHES_PRIMARY_COL, (1, 1, 1)))
        return LVecBase4f(r, g, b, 1)

    def isDyeable(self) -> bool:
        return self.dyeable

    def makeItemModel(self, item: Optional[InventoryItem] = None, *extraArgs) -> NodePath:
        newNode = self.ShirtModel.copyTo(NodePath())

        newNode.find('**/torso-top').setTexture(self.getTexture(), 1)
        newNode.find('**/torso-top').setColor(self.getColor(item=item))
        newNode.find('**/sleeves').setTexture(self.getSleeveTexture(), 1)
        newNode.find('**/sleeves').setColor(self.getSleeveColor(item=item))

        return newNode

    def makeGuiItemModel(self) -> NodePath:
        """
        Creates the GUI item model to be used.
        """
        model = self.makeItemModel()
        for node in model.findAllMatches('*'):
            node.setH(180)
        model.flattenStrong()
        return model


# The registry dictionary for shirts.
ShirtRegistry: Dict[IntEnum, ShirtItemDefinition] = {
    ShirtItemType.Plain: ShirtItemDefinition(
        name="Plain",
        description="No Description",
        texturePath="phase_3/maps/desat_shirt_1.png",
        sleeveTexturePath="phase_3/maps/desat_sleeve_1.png",
        dyeable=True,
    ),
    ShirtItemType.BottomStripe: ShirtItemDefinition(
        name="Bottom Stripe",
        description="No Description",
        texturePath="phase_3/maps/desat_shirt_2.png",
        sleeveTexturePath="phase_3/maps/desat_sleeve_2.png",
        dyeable=True,
    ),
    ShirtItemType.ButtonUpA: ShirtItemDefinition(
        name="Button-Up",
        description="No Description",
        texturePath="phase_3/maps/desat_shirt_3.png",
        sleeveTexturePath="phase_3/maps/desat_sleeve_3.png",
        dyeable=True,
    ),
    ShirtItemType.DoubleStriped: ShirtItemDefinition(
        name="Double Striped",
        description="No Description",
        texturePath="phase_3/maps/desat_shirt_4.png",
        sleeveTexturePath="phase_3/maps/desat_sleeve_4.png",
        dyeable=True,
    ),
    ShirtItemType.Striped: ShirtItemDefinition(
        name="Striped",
        description="No Description",
        texturePath="phase_3/maps/desat_shirt_5.png",
        sleeveTexturePath="phase_3/maps/desat_sleeve_5.png",
        dyeable=True,
    ),
    ShirtItemType.PocketPolo: ShirtItemDefinition(
        name="Pocket Polo",
        description="No Description",
        texturePath="phase_3/maps/desat_shirt_6.png",
        sleeveTexturePath="phase_3/maps/desat_sleeve_6.png",
        dyeable=True,
    ),
    ShirtItemType.Feather: ShirtItemDefinition(
        name="Feather",
        description="No Description",
        texturePath="phase_3/maps/desat_shirt_9.png",
        sleeveTexturePath="phase_3/maps/desat_sleeve_9.png",
        dyeable=True,
    ),
    ShirtItemType.Dress: ShirtItemDefinition(
        name="Dress",
        description="No Description",
        texturePath="phase_3/maps/desat_shirt_10.png",
        sleeveTexturePath="phase_3/maps/desat_sleeve_10.png",
        dyeable=True,
    ),
    ShirtItemType.TwoToneButtonUp: ShirtItemDefinition(
        name="Two-Tone Button-Up",
        description="No Description",
        texturePath="phase_3/maps/desat_shirt_11.png",
        sleeveTexturePath="phase_3/maps/desat_sleeve_1.png",
        dyeable=True,
    ),
    ShirtItemType.Vest: ShirtItemDefinition(
        name="Vest",
        description="No Description",
        texturePath="phase_3/maps/desat_shirt_12.png",
        sleeveTexturePath="phase_3/maps/desat_sleeve_1.png",
        dyeable=True,
    ),
    ShirtItemType.ButtonUpB: ShirtItemDefinition(
        name="Button-Up",
        description="No Description",
        texturePath="phase_3/maps/desat_shirt_15.png",
        sleeveTexturePath="phase_3/maps/desat_sleeve_15.png",
        dyeable=True,
    ),
    ShirtItemType.Soccer: ShirtItemDefinition(
        name="Soccer",
        description="No Description",
        texturePath="phase_3/maps/desat_shirt_17.png",
        sleeveTexturePath="phase_3/maps/desat_sleeve_1.png",
        dyeable=True,
    ),
    ShirtItemType.LightningBolt: ShirtItemDefinition(
        name="Lightning Bolt",
        description="No Description",
        texturePath="phase_3/maps/desat_shirt_18.png",
        sleeveTexturePath="phase_3/maps/desat_sleeve_1.png",
        dyeable=True,
    ),
    ShirtItemType.No19: ShirtItemDefinition(
        name="#19",
        description="No Description",
        texturePath="phase_3/maps/desat_shirt_19.png",
        sleeveTexturePath="phase_3/maps/desat_sleeve_19.png",
        dyeable=True,
    ),
    ShirtItemType.Guayabera: ShirtItemDefinition(
        name="Guayabera",
        description="No Description",
        texturePath="phase_3/maps/desat_shirt_20.png",
        sleeveTexturePath="phase_3/maps/desat_sleeve_20.png",
        dyeable=True,
    ),
    ShirtItemType.Flower: ShirtItemDefinition(
        name="Flower",
        description="No Description",
        texturePath="phase_3/maps/desat_shirt_7.png",
        sleeveTexturePath="phase_3/maps/desat_sleeve_7.png",
        dyeable=True,
    ),
    ShirtItemType.FlowerStripe: ShirtItemDefinition(
        name="Flower Stripe",
        description="No Description",
        texturePath="phase_3/maps/desat_shirt_8.png",
        sleeveTexturePath="phase_3/maps/desat_sleeve_8.png",
        dyeable=True,
    ),
    ShirtItemType.DenimVest: ShirtItemDefinition(
        name="Denim Vest",
        description="No Description",
        texturePath="phase_3/maps/desat_shirt_13.png",
        sleeveTexturePath="phase_3/maps/desat_sleeve_1.png",
    ),
    ShirtItemType.CuffedBlouse: ShirtItemDefinition(
        name="Cuffed Blouse",
        description="No Description",
        texturePath="phase_3/maps/desat_shirt_14.png",
        sleeveTexturePath="phase_3/maps/desat_sleeve_16.png",
        dyeable=True,
    ),
    ShirtItemType.Peplum: ShirtItemDefinition(
        name="Peplum",
        description="No Description",
        texturePath="phase_3/maps/desat_shirt_16.png",
        sleeveTexturePath="phase_3/maps/desat_sleeve_16.png",
        dyeable=True,
    ),
    ShirtItemType.Hearts: ShirtItemDefinition(
        name="Hearts",
        description="No Description",
        texturePath="phase_3/maps/desat_shirt_21.png",
        sleeveTexturePath="phase_3/maps/desat_sleeve_1.png",
        dyeable=True,
    ),
    ShirtItemType.Stars: ShirtItemDefinition(
        name="Stars",
        description="No Description",
        texturePath="phase_3/maps/desat_shirt_22.png",
        sleeveTexturePath="phase_3/maps/desat_sleeve_1.png",
        dyeable=True,
    ),
    ShirtItemType.SingleFlower: ShirtItemDefinition(
        name="Single Flower",
        description="No Description",
        texturePath="phase_3/maps/desat_shirt_23.png",
        sleeveTexturePath="phase_3/maps/desat_sleeve_1.png",
        dyeable=True,
    ),
    ShirtItemType.ZipUpHoodie: ShirtItemDefinition(
        name="Zip-Up Hoodie",
        description="No Description",
        texturePath="phase_4/maps/female_shirt3.png",
        sleeveTexturePath="phase_4/maps/female_sleeve3.png",
    ),
    ShirtItemType.Island: ShirtItemDefinition(
        name="Island",
        description="No Description",
        texturePath="phase_4/maps/male_shirt2_palm.png",
        sleeveTexturePath="phase_4/maps/male_sleeve2_palm.png",
    ),
    ShirtItemType.PurpleStars: ShirtItemDefinition(
        name="Purple Stars",
        description="No Description",
        texturePath="phase_4/maps/shirt6New.png",
        sleeveTexturePath="phase_4/maps/sleeve6New.png",
    ),
    ShirtItemType.WinterStripes: ShirtItemDefinition(
        name="Winter Stripes",
        description="No Description",
        texturePath="phase_4/maps/male_shirt1.png",
        sleeveTexturePath="phase_4/maps/male_sleeve1.png",
    ),
    ShirtItemType.No1: ShirtItemDefinition(
        name="#1",
        description="No Description",
        texturePath="phase_4/maps/male_shirt3c.png",
        sleeveTexturePath="phase_4/maps/male_sleeve3c.png",
    ),
    ShirtItemType.GreenStripe: ShirtItemDefinition(
        name="Green Stripe",
        description="No Description",
        texturePath="phase_4/maps/shirtMale4B.png",
        sleeveTexturePath="phase_4/maps/male_sleeve4New.png",
    ),
    ShirtItemType.RedCheckerboardKimono: ShirtItemDefinition(
        name="Red Checkerboard Kimono",
        description="No Description",
        texturePath="phase_4/maps/shirtMaleNew7.png",
        sleeveTexturePath="phase_4/maps/SleeveMaleNew7.png",
    ),
    ShirtItemType.GoldenStripes: ShirtItemDefinition(
        name="Golden Stripes",
        description="No Description",
        texturePath="phase_4/maps/female_shirt1b.png",
        sleeveTexturePath="phase_4/maps/female_sleeve1b.png",
    ),
    ShirtItemType.PinkBow: ShirtItemDefinition(
        name="Pink Bow",
        description="No Description",
        texturePath="phase_4/maps/female_shirt2.png",
        sleeveTexturePath="phase_4/maps/female_sleeve2.png",
    ),
    ShirtItemType.TiedDress: ShirtItemDefinition(
        name="Tied Dress",
        description="No Description",
        texturePath="phase_4/maps/female_shirt5New.png",
        sleeveTexturePath="phase_4/maps/female_sleeve5New.png",
    ),
    ShirtItemType.WinterStripe: ShirtItemDefinition(
        name="Winter Stripe",
        description="No Description",
        texturePath="phase_4/maps/femaleShirtNew6.png",
        sleeveTexturePath="phase_4/maps/female_sleeveNew6.png",
    ),
    ShirtItemType.TieDye: ShirtItemDefinition(
        name="Tie-Dye",
        description="No Description",
        texturePath="phase_4/maps/shirtTieDyeNew.png",
        sleeveTexturePath="phase_4/maps/sleeveTieDye.png",
    ),
    ShirtItemType.Sheriff: ShirtItemDefinition(
        name="Sheriff",
        description="No Description",
        texturePath="phase_4/maps/CowboyShirt1.png",
        sleeveTexturePath="phase_4/maps/CowboySleeve1.png",
    ),
    ShirtItemType.CheckeredCowboy: ShirtItemDefinition(
        name="Checkered Cowboy",
        description="No Description",
        texturePath="phase_4/maps/CowboyShirt2.png",
        sleeveTexturePath="phase_4/maps/CowboySleeve2.png",
    ),
    ShirtItemType.CactusCowboy: ShirtItemDefinition(
        name="Cactus Cowboy",
        description="No Description",
        texturePath="phase_4/maps/CowboyShirt3.png",
        sleeveTexturePath="phase_4/maps/CowboySleeve3.png",
    ),
    ShirtItemType.CowboyVest: ShirtItemDefinition(
        name="Cowboy Vest",
        description="No Description",
        texturePath="phase_4/maps/CowboyShirt4.png",
        sleeveTexturePath="phase_4/maps/CowboySleeve4.png",
    ),
    ShirtItemType.GreenDrawstring: ShirtItemDefinition(
        name="Green Drawstring",
        description="No Description",
        texturePath="phase_4/maps/CowboyShirt5.png",
        sleeveTexturePath="phase_4/maps/CowboySleeve5.png",
    ),
    ShirtItemType.BlueDrawstring: ShirtItemDefinition(
        name="Blue Drawstring",
        description="No Description",
        texturePath="phase_4/maps/CowboyShirt6.png",
        sleeveTexturePath="phase_4/maps/CowboySleeve6.png",
    ),
    ShirtItemType.Ghost: ShirtItemDefinition(
        name="Ghost",
        description="No Description",
        texturePath="phase_4/maps/halloween/ghost_shirt/shirt_ghost.png",
        sleeveTexturePath="phase_4/maps/halloween/ghost_shirt/shirt_Sleeve_ghost.png",
    ),
    ShirtItemType.Pumpkin: ShirtItemDefinition(
        name="Pumpkin",
        description="No Description",
        texturePath="phase_4/maps/halloween/pumkin_shirt/shirt_pumkin.png",
        sleeveTexturePath="phase_4/maps/halloween/pumkin_shirt/shirt_Sleeve_pumkin.png",
    ),
    ShirtItemType.VampireA: ShirtItemDefinition(
        name="Vampire",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_halloween5.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween5.png",
    ),
    ShirtItemType.Turtle: ShirtItemDefinition(
        name="Turtle",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_halloweenTurtle.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_halloweenTurtle.png",
    ),
    ShirtItemType.VampireB: ShirtItemDefinition(
        name="Vampire",
        description="No Description",
        texturePath="phase_4/maps/halloween/dracula_outfit/tt_t_chr_avt_shirt_vampire.png",
        sleeveTexturePath="phase_4/maps/halloween/dracula_outfit/tt_t_chr_avt_shirtSleeve_vampire.png",
    ),
    ShirtItemType.Toonosaur: ShirtItemDefinition(
        name="Toonosaur",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_dinosaur.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_dinosaur.png",
    ),
    ShirtItemType.FishingBubble: ShirtItemDefinition(
        name="Fishing Bubble",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_fishing04.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing04.png",
    ),
    ShirtItemType.FORE: ShirtItemDefinition(
        name="FORE!",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_golf03.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_golf03.png",
    ),
    ShirtItemType.GearBusting: ShirtItemDefinition(
        name="Gear Busting",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_mostCogsDefeated02.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_mostCogsDefeated02.png",
    ),
    ShirtItemType.Snowman: ShirtItemDefinition(
        name="Snowman",
        description="No Description",
        texturePath="phase_4/maps/holiday_shirt1.png",
        sleeveTexturePath="phase_4/maps/holidaySleeve1.png",
    ),
    ShirtItemType.Snowflakes: ShirtItemDefinition(
        name="Snowflakes",
        description="No Description",
        texturePath="phase_4/maps/holiday_shirt2b.png",
        sleeveTexturePath="phase_4/maps/holidaySleeve1.png",
    ),
    ShirtItemType.CandyCaneHearts: ShirtItemDefinition(
        name="Candy Cane Hearts",
        description="No Description",
        texturePath="phase_4/maps/holidayShirt3b.png",
        sleeveTexturePath="phase_4/maps/holidaySleeve3.png",
    ),
    ShirtItemType.WinterScarf: ShirtItemDefinition(
        name="Winter Scarf",
        description="No Description",
        texturePath="phase_4/maps/holidayShirt4.png",
        sleeveTexturePath="phase_4/maps/holidaySleeve3.png",
    ),
    ShirtItemType.PinkHeart: ShirtItemDefinition(
        name="Pink Heart",
        description="No Description",
        texturePath="phase_4/maps/Vday1Shirt5.png",
        sleeveTexturePath="phase_4/maps/Vday5Sleeve.png",
    ),
    ShirtItemType.RedHeart: ShirtItemDefinition(
        name="Red Heart",
        description="No Description",
        texturePath="phase_4/maps/Vday1Shirt6SHD.png",
        sleeveTexturePath="phase_4/maps/Vda6Sleeve.png",
    ),
    ShirtItemType.WingedHeart: ShirtItemDefinition(
        name="Winged Heart",
        description="No Description",
        texturePath="phase_4/maps/Vday1Shirt4.png",
        sleeveTexturePath="phase_4/maps/Vday_shirt4sleeve.png",
    ),
    ShirtItemType.FieryHeart: ShirtItemDefinition(
        name="Fiery Heart",
        description="No Description",
        texturePath="phase_4/maps/Vday_shirt2c.png",
        sleeveTexturePath="phase_4/maps/Vday2cSleeve.png",
    ),
    ShirtItemType.Cupid: ShirtItemDefinition(
        name="Cupid",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_valentine1.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_valentine1.png",
    ),
    ShirtItemType.DottedHearts: ShirtItemDefinition(
        name="Dotted Hearts",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_valentine2.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_valentine2.png",
    ),
    ShirtItemType.RedBow: ShirtItemDefinition(
        name="Red Bow",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_valentine3.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_valentine3.png",
    ),
    ShirtItemType.LuckyClover: ShirtItemDefinition(
        name="Lucky Clover",
        description="No Description",
        texturePath="phase_4/maps/StPats_shirt1.png",
        sleeveTexturePath="phase_4/maps/StPats_sleeve.png",
    ),
    ShirtItemType.PotOGold: ShirtItemDefinition(
        name="Pot O' Gold",
        description="No Description",
        texturePath="phase_4/maps/StPats_shirt2.png",
        sleeveTexturePath="phase_4/maps/StPats_sleeve2.png",
    ),
    ShirtItemType.IdesofMarch: ShirtItemDefinition(
        name="Ides of March",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_greentoon1.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_greentoon1.png",
    ),
    ShirtItemType.Fisherman: ShirtItemDefinition(
        name="Fisherman",
        description="No Description",
        texturePath="phase_4/maps/ContestfishingVestShirt2.png",
        sleeveTexturePath="phase_4/maps/ContestfishingVestSleeve1.png",
    ),
    ShirtItemType.Goldfish: ShirtItemDefinition(
        name="Goldfish",
        description="No Description",
        texturePath="phase_4/maps/ContestFishtankShirt1.png",
        sleeveTexturePath="phase_4/maps/ContestFishtankSleeve1.png",
    ),
    ShirtItemType.Pawprint: ShirtItemDefinition(
        name="Pawprint",
        description="No Description",
        texturePath="phase_4/maps/ContestPawShirt1.png",
        sleeveTexturePath="phase_4/maps/ContestPawSleeve1.png",
    ),
    ShirtItemType.BackpackAndShades: ShirtItemDefinition(
        name="Backpack & Shades",
        description="No Description",
        texturePath="phase_4/maps/contest_backpack3.png",
        sleeveTexturePath="phase_4/maps/contest_backpack_sleeve.png",
    ),
    ShirtItemType.Lederhosen: ShirtItemDefinition(
        name="Lederhosen",
        description="No Description",
        texturePath="phase_4/maps/contest_leder.png",
        sleeveTexturePath="phase_4/maps/Contest_leder_sleeve.png",
    ),
    ShirtItemType.Watermelon: ShirtItemDefinition(
        name="Watermelon",
        description="No Description",
        texturePath="phase_4/maps/contest_mellon2.png",
        sleeveTexturePath="phase_4/maps/contest_mellon_sleeve2.png",
    ),
    ShirtItemType.RacingFlag: ShirtItemDefinition(
        name="Racing Flag",
        description="No Description",
        texturePath="phase_4/maps/contest_race2.png",
        sleeveTexturePath="phase_4/maps/contest_race_sleeve.png",
    ),
    ShirtItemType.AmericanFlag: ShirtItemDefinition(
        name="American Flag",
        description="No Description",
        texturePath="phase_4/maps/4thJulyShirt1.png",
        sleeveTexturePath="phase_4/maps/4thJulySleeve1.png",
    ),
    ShirtItemType.Fireworks: ShirtItemDefinition(
        name="Fireworks",
        description="No Description",
        texturePath="phase_4/maps/4thJulyShirt2.png",
        sleeveTexturePath="phase_4/maps/4thJulySleeve2.png",
    ),
    ShirtItemType.GreenButtonUp: ShirtItemDefinition(
        name="Green Button-Up",
        description="No Description",
        texturePath="phase_4/maps/shirt_Cat7_01.png",
        sleeveTexturePath="phase_4/maps/shirt_sleeveCat7_01.png",
    ),
    ShirtItemType.Daisy: ShirtItemDefinition(
        name="Daisy",
        description="No Description",
        texturePath="phase_4/maps/shirt_Cat7_02.png",
        sleeveTexturePath="phase_4/maps/shirt_sleeveCat7_02.png",
    ),
    ShirtItemType.BananaPeel: ShirtItemDefinition(
        name="Banana Peel",
        description="No Description",
        texturePath="phase_4/maps/PJBlueBanana2.png",
        sleeveTexturePath="phase_4/maps/PJSleeveBlue.png",
    ),
    ShirtItemType.BikeHorn: ShirtItemDefinition(
        name="Bike Horn",
        description="No Description",
        texturePath="phase_4/maps/PJRedHorn2.png",
        sleeveTexturePath="phase_4/maps/PJSleeveRed.png",
    ),
    ShirtItemType.HypnoGoggles: ShirtItemDefinition(
        name="Hypno Goggles",
        description="No Description",
        texturePath="phase_4/maps/PJGlasses2.png",
        sleeveTexturePath="phase_4/maps/PJSleevePurple.png",
    ),
    ShirtItemType.ClownFish: ShirtItemDefinition(
        name="Clown Fish",
        description="Better get your jokebook at the ready!",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_fishing1.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing1.png",
    ),
    ShirtItemType.OldBootA: ShirtItemDefinition(
        name="Old Boot",
        description="Pulled right out of the pond!",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_fishing2.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing2.png",
    ),
    ShirtItemType.Mole: ShirtItemDefinition(
        name="Mole",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_gardening1.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_gardening1.png",
    ),
    ShirtItemType.Gardening: ShirtItemDefinition(
        name="Gardening",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_gardening2.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_gardening2.png",
    ),
    ShirtItemType.Cupcake: ShirtItemDefinition(
        name="Cupcake",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_party1.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_party1.png",
    ),
    ShirtItemType.PartyHat: ShirtItemDefinition(
        name="Party Hat",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_party2.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_party2.png",
    ),
    ShirtItemType.RoadsterRaceway: ShirtItemDefinition(
        name="Roadster Raceway",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_racing1.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_racing1.png",
    ),
    ShirtItemType.Roadster: ShirtItemDefinition(
        name="Roadster",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_racing2.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_racing2.png",
    ),
    ShirtItemType.CoolSun: ShirtItemDefinition(
        name="Cool Sun",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_summer1.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_summer1.png",
    ),
    ShirtItemType.Beachball: ShirtItemDefinition(
        name="Beachball",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_summer2.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_summer2.png",
    ),
    ShirtItemType.DiamondPolo: ShirtItemDefinition(
        name="Diamond Polo",
        description="Perfect for when you're batting on the diamond-- Wait, this isn't baseball.",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_golf1.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_golf1.png",
    ),
    ShirtItemType.DottedPolo: ShirtItemDefinition(
        name="Dotted Polo",
        description="Dots, which are circles, which are like golf balls! It makes sense.",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_golf2.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_golf2.png",
    ),
    ShirtItemType.GoldMedal: ShirtItemDefinition(
        name="Gold Medal",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_marathon1.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_marathon1.png",
    ),
    ShirtItemType.SaveTheBuildings: ShirtItemDefinition(
        name="Save The Buildings",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_saveBuilding1.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_saveBuilding1.png",
    ),
    ShirtItemType.SaveTheBuildingsNo2: ShirtItemDefinition(
        name="Save The Buildings #2",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_saveBuilding2.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_saveBuilding2.png",
    ),
    ShirtItemType.ToontaskCompleter: ShirtItemDefinition(
        name="Toontask Completer",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_toonTask1.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_toonTask1.png",
    ),
    ShirtItemType.ToontaskCompleterNo2: ShirtItemDefinition(
        name="Toontask Completer #2",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_toonTask2.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_toonTask2.png",
    ),
    ShirtItemType.Trolley: ShirtItemDefinition(
        name="Trolley",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_trolley1.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_trolley1.png",
    ),
    ShirtItemType.TrolleyNo2: ShirtItemDefinition(
        name="Trolley #2",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_trolley2.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_trolley2.png",
    ),
    ShirtItemType.WinterGift: ShirtItemDefinition(
        name="Winter Gift",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_winter1.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_winter1.png",
    ),
    ShirtItemType.Skeletoon: ShirtItemDefinition(
        name="Skeletoon",
        description="No Description",
        texturePath="phase_4/maps/halloween/skeleton_outfit/tt_t_chr_avt_shirt_halloween3.png",
        sleeveTexturePath="phase_4/maps/halloween/skeleton_outfit/tt_t_chr_avt_shirtSleeve_halloween3.png",
    ),
    ShirtItemType.Cobweb: ShirtItemDefinition(
        name="Cobweb",
        description="No Description",
        texturePath="phase_4/maps/halloween/spider_outfit/tt_t_chr_avt_shirt_halloween4.png",
        sleeveTexturePath="phase_4/maps/halloween/spider_outfit/tt_t_chr_avt_shirtSleeve_halloween4.png",
    ),
    ShirtItemType.MostCogsDefeatedA: ShirtItemDefinition(
        name="Most Cogs Defeated",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_mostCogsDefeated01.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_mostCogsDefeated01.png",
    ),
    ShirtItemType.MostVPsDefeated: ShirtItemDefinition(
        name="Most VP's Defeated",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_sellbotVPIcon.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_sellbotVPIcon.png",
    ),
    ShirtItemType.SellbotSmasher: ShirtItemDefinition(
        name="Sellbot Smasher",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_sellbotCrusher.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_sellbotCrusher.png",
    ),
    ShirtItemType.Pirate: ShirtItemDefinition(
        name="Pirate",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_pirate.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_pirate.png",
    ),
    ShirtItemType.Supertoon: ShirtItemDefinition(
        name="Supertoon",
        description="No Description",
        texturePath="phase_4/maps/halloween/supertoon_outfit/tt_t_chr_avt_shirt_supertoon.png",
        sleeveTexturePath="phase_4/maps/halloween/supertoon_outfit/tt_t_chr_avt_shirtSleeve_supertoon.png",
    ),
    ShirtItemType.RacerJumpsuit: ShirtItemDefinition(
        name="Racer Jumpsuit",
        description="Guaranteed to be fireproof, bananaproof, and pieproof!",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_racingGrandPrix.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_racingGrandPrix.png",
    ),
    ShirtItemType.NoTimeforCogBuildings: ShirtItemDefinition(
        name="No Time for Cog Buildings",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_saveBuilding3.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_saveBuilding3.png",
    ),
    ShirtItemType.TrolleyGang: ShirtItemDefinition(
        name="Trolley Gang",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_trolley03.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_trolley03.png",
    ),
    ShirtItemType.OldBootB: ShirtItemDefinition(
        name="Old Boot",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_fishing05.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing05.png",
    ),
    ShirtItemType.WitchPolo: ShirtItemDefinition(
        name="Witch Polo",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_halloween06.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_halloween06.png",
    ),
    ShirtItemType.Sledding: ShirtItemDefinition(
        name="Sledding",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_winter03.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_winter03.png",
    ),
    ShirtItemType.Bat: ShirtItemDefinition(
        name="Bat",
        description="No Description",
        texturePath="phase_4/maps/halloween/bat_shirt/tt_t_chr_avt_shirt_halloween07.png",
        sleeveTexturePath="phase_4/maps/halloween/bat_shirt/tt_t_chr_avt_shirtSleeve_halloween07.png",
    ),
    ShirtItemType.Mittens: ShirtItemDefinition(
        name="Mittens",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_winter02.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_winter02.png",
    ),
    ShirtItemType.PoolShark: ShirtItemDefinition(
        name="Pool Shark",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_fishing06.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing06.png",
    ),
    ShirtItemType.PianoTuna: ShirtItemDefinition(
        name="Piano Tuna",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_fishing07.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_fishing07.png",
    ),
    ShirtItemType.GolfStripes: ShirtItemDefinition(
        name="Golf Stripes",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_golf05.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_golf05.png",
    ),
    ShirtItemType.DummyCogPolo: ShirtItemDefinition(
        name="Dummy Cog Polo",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_mostCogsDefeated03.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_mostCogsDefeated03.png",
    ),
    ShirtItemType.MostCogsDefeatedforAnts: ShirtItemDefinition(
        name="Most Cogs Defeated for Ants",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_mostCogsDefeated04.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_mostCogsDefeated04.png",
    ),
    ShirtItemType.TrolleyForAnts: ShirtItemDefinition(
        name="Trolley For Ants",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_trolley04.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_trolley04.png",
    ),
    ShirtItemType.TrolleySideways: ShirtItemDefinition(
        name="Trolley Sideways",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_trolley05.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_trolley03.png",
    ),
    ShirtItemType.MostBuildingsDefeated: ShirtItemDefinition(
        name="Most Buildings Defeated",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_saveBuilding4.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_trolley05.png",
    ),
    ShirtItemType.MostCogsDefeatedB: ShirtItemDefinition(
        name="Most Cogs Defeated",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_saveBuilding05.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_saveBuilding05.png",
    ),
    ShirtItemType.BirthdayCake: ShirtItemDefinition(
        name="Birthday Cake",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_anniversary.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_anniversary.png",
    ),
    ShirtItemType.LoonyLabsScientistA: ShirtItemDefinition(
        name="Loony Labs Scientist A",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_shirt_scientistC.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_shirtSleeve_scientist.png",
    ),
    ShirtItemType.LoonyLabsScientistB: ShirtItemDefinition(
        name="Loony Labs Scientist B",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_shirt_scientistA.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_shirtSleeve_scientist.png",
    ),
    ShirtItemType.LoonyLabsScientistC: ShirtItemDefinition(
        name="Loony Labs Scientist C",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_shirt_scientistB.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_shirtSleeve_scientist.png",
    ),
    ShirtItemType.SillyMailbox: ShirtItemDefinition(
        name="Silly Mailbox",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_mailbox.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_mailbox.png",
    ),
    ShirtItemType.SillyTrashCan: ShirtItemDefinition(
        name="Silly Trash Can",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_trashcan.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_trashcan.png",
    ),
    ShirtItemType.LoonyLabsLogo: ShirtItemDefinition(
        name="Loony Labs Logo",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_loonyLabs.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_loonyLabs.png",
    ),
    ShirtItemType.SillyHydrant: ShirtItemDefinition(
        name="Silly Hydrant",
        description="A hilariously humorous hydrant!",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_hydrant.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_hydrant.png",
    ),
    ShirtItemType.SillyMeterWhistle: ShirtItemDefinition(
        name="Silly Meter Whistle",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_whistle.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_whistle.png",
    ),
    ShirtItemType.CogCrusherShirt: ShirtItemDefinition(
        name="Cog-Crusher Shirt",
        description="The suit for the most masterful of Gag-wielding! If you don't mind looking like a banana.",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_cogbuster.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_cogbuster.png",
    ),
    ShirtItemType.NoMoreCheese: ShirtItemDefinition(
        name="No More Cheese!",
        description="Whether you are lactose intolerant, or just don't like Cogs, this is the shirt for you.",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_victoryParty01.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_victoryParty01.png",
    ),
    ShirtItemType.FlunkyFlannel: ShirtItemDefinition(
        name="Flunky Flannel",
        description="Real spunky.",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_victoryParty02.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_victoryParty02.png",
    ),
    ShirtItemType.DefeatedSellbots: ShirtItemDefinition(
        name="Defeated Sellbots",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_sellbotIcon.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_sellbotIcon.png",
    ),
    ShirtItemType.JellybeanJar: ShirtItemDefinition(
        name="Jellybean Jar",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_jellyBeans.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_jellyBeans.png",
    ),
    ShirtItemType.Doodle: ShirtItemDefinition(
        name="Doodle",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_doodle.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_doodle.png",
    ),
    ShirtItemType.GetConnected: ShirtItemDefinition(
        name="Get Connected",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_getConnectedMoverShaker.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_getConnectedMoverShaker.png",
    ),
    ShirtItemType.Bee: ShirtItemDefinition(
        name="Bee",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_bee.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_bee.png",
    ),
    ShirtItemType.Meatballs: ShirtItemDefinition(
        name="Meatballs",
        description="You can't actually eat this. Well you COULD, but...",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_meatballs.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_meatballs.png",
    ),
    ShirtItemType.TrashcatsRags: ShirtItemDefinition(
        name="Trashcat's Rags",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_trashcat.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_trashcat.png",
    ),
    ShirtItemType.DrowsyDreamland: ShirtItemDefinition(
        name="Drowsy Dreamland",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_ZZZ.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_sleeve_ZZZ.png",
    ),
    ShirtItemType.BetaToon: ShirtItemDefinition(
        name="Beta Toon",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_beta.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirt_sleeve_beta.png",
    ),
    ShirtItemType.YOTTKnight: ShirtItemDefinition(
        name="YOTT Knight",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_yott.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirt_sleeve_yott.png",
    ),
    ShirtItemType.BBSailor: ShirtItemDefinition(
        name="BB Sailor",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_sail.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirt_sleeve_sail.png",
    ),
    ShirtItemType.DGGardening: ShirtItemDefinition(
        name="DG Gardening",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_garden.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_garden.png",
    ),
    ShirtItemType.TTCFirefighter: ShirtItemDefinition(
        name="TTC Firefighter",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_fire.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_fire.png",
    ),
    ShirtItemType.MMLBand: ShirtItemDefinition(
        name="MML Band",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_band.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_band.png",
    ),
    ShirtItemType.TeamBarnyard: ShirtItemDefinition(
        name="Team Barnyard",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_barnyard.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_barnyard.png",
    ),
    ShirtItemType.TeamOutback: ShirtItemDefinition(
        name="Team Outback",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_outback.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_shirtSleeve_outback.png",
    ),
    ShirtItemType.BarnyardVacation: ShirtItemDefinition(
        name="Barnyard Vacation",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_barnyard_victory.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_sleeve_barnyard_victory.png",
    ),
    ShirtItemType.OutbackVacation: ShirtItemDefinition(
        name="Outback Vacation",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_outback_victory.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_sleeve_outback_victory.png",
    ),
    ShirtItemType.AAParkRanger: ShirtItemDefinition(
        name="AA Park Ranger",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_park_ranger.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_sleeve_park_ranger.png",
    ),
    ShirtItemType.BrrrghSnowflakes: ShirtItemDefinition(
        name="Brrrgh Snowflakes",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_brrrgh.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_sleeve_brrrgh.png",
    ),
    ShirtItemType.Alchemist: ShirtItemDefinition(
        name="Alchemist",
        description="No Description",
        texturePath="phase_4/maps/halloween/alchemist_outfit/tt_t_chr_avt_shirt_alchemist_male.png",
        sleeveTexturePath="phase_4/maps/halloween/alchemist_outfit/tt_t_chr_avt_sleeve_alchemist.png",
    ),
    ShirtItemType.AlchemistOveralls: ShirtItemDefinition(
        name="Alchemist Overalls",
        description="No Description",
        texturePath="phase_4/maps/halloween/alchemist_outfit/tt_t_chr_avt_shirt_alchemist_female.png",
        sleeveTexturePath="phase_4/maps/halloween/alchemist_outfit/tt_t_chr_avt_sleeve_alchemist.png",
    ),
    ShirtItemType.Frankentoon: ShirtItemDefinition(
        name="Frankentoon",
        description="No Description",
        texturePath="phase_4/maps/halloween/frankenstein_outfit/tt_t_chr_avt_shirt_frankenstien.png",
        sleeveTexturePath="phase_4/maps/halloween/frankenstein_outfit/tt_t_chr_avt_sleeve_frankenstien.png",
    ),
    ShirtItemType.Spacetoon: ShirtItemDefinition(
        name="Spacetoon",
        description="No Description",
        texturePath="phase_4/maps/halloween/moonsuit_outfit/tt_t_chr_avt_shirt_moonsuit.png",
        sleeveTexturePath="phase_4/maps/halloween/moonsuit_outfit/tt_t_chr_avt_sleeve_moonsuit.png",
    ),
    ShirtItemType.MadScientist: ShirtItemDefinition(
        name="Mad Scientist",
        description="No Description",
        texturePath="phase_4/maps/halloween/scientistD_outfit/tt_t_chr_avt_shirt_scientistd.png",
        sleeveTexturePath="phase_4/maps/halloween/scientistD_outfit/tt_t_chr_avt_sleeve_scientistd.png",
    ),
    ShirtItemType.Clown: ShirtItemDefinition(
        name="Clown",
        description="No Description",
        texturePath="phase_4/maps/halloween/clown_outfit/tt_t_chr_avt_shirt_clown.png",
        sleeveTexturePath="phase_4/maps/halloween/clown_outfit/tt_t_chr_avt_sleeve_clown.png",
    ),
    ShirtItemType.Wonderland: ShirtItemDefinition(
        name="Wonderland",
        description="No Description",
        texturePath="phase_4/maps/halloween/toons_in_wonderland_outfit/tt_t_chr_avt_shirt_tiw.png",
        sleeveTexturePath="phase_4/maps/halloween/toons_in_wonderland_outfit/tt_t_chr_avt_sleeve_tiw.png",
    ),
    ShirtItemType.Reaper: ShirtItemDefinition(
        name="Reaper",
        description="No Description",
        texturePath="phase_4/maps/halloween/reaper_outfit/tt_t_chr_avt_shirt_reaper.png",
        sleeveTexturePath="phase_4/maps/halloween/reaper_outfit/tt_t_chr_avt_sleeve_reaper.png",
    ),
    ShirtItemType.Scarecrow: ShirtItemDefinition(
        name="Scarecrow",
        description="No Description",
        texturePath="phase_4/maps/halloween/scarecrow_outfit/tt_t_chr_avt_shirt_scarecrow_male.png",
        sleeveTexturePath="phase_4/maps/halloween/scarecrow_outfit/tt_t_chr_avt_sleeve_scarecrow.png",
    ),
    ShirtItemType.ScarecrowOveralls: ShirtItemDefinition(
        name="Scarecrow Overalls",
        description="No Description",
        texturePath="phase_4/maps/halloween/scarecrow_outfit/tt_t_chr_avt_shirt_scarecrow_female.png",
        sleeveTexturePath="phase_4/maps/halloween/scarecrow_outfit/tt_t_chr_avt_sleeve_scarecrow.png",
    ),
    ShirtItemType.Wizard: ShirtItemDefinition(
        name="Wizard",
        description="No Description",
        texturePath="phase_4/maps/halloween/witch_outfit/tt_t_chr_avt_shirt_witch.png",
        sleeveTexturePath="phase_4/maps/halloween/witch_outfit/tt_t_chr_avt_sleeve_witch.png",
    ),
    ShirtItemType.GreenElfShirt: ShirtItemDefinition(
        name="Green Elf Shirt",
        description="No Description",
        texturePath="phase_4/maps/winter/elf_green_outfit/tt_t_chr_avt_shirt_elf_green.png",
        sleeveTexturePath="phase_4/maps/winter/elf_green_outfit/tt_t_chr_avt_sleeve_elf_green.png",
    ),
    ShirtItemType.RedElfShirt: ShirtItemDefinition(
        name="Red Elf Shirt",
        description="No Description",
        texturePath="phase_4/maps/winter/elf_red_outfit/tt_t_chr_avt_shirt_elf_red.png",
        sleeveTexturePath="phase_4/maps/winter/elf_red_outfit/tt_t_chr_avt_sleeve_elf_red.png",
    ),
    ShirtItemType.GingerbreadA: ShirtItemDefinition(
        name="Gingerbread",
        description="No Description",
        texturePath="phase_4/maps/winter/gingerbread_outfit/tt_t_chr_avt_shirt_gingerbread_male.png",
        sleeveTexturePath="phase_4/maps/winter/gingerbread_outfit/tt_t_chr_avt_sleeve_gingerbread.png",
    ),
    ShirtItemType.GingerbreadB: ShirtItemDefinition(
        name="Gingerbread",
        description="No Description",
        texturePath="phase_4/maps/winter/gingerbread_outfit/tt_t_chr_avt_shirt_gingerbread_female.png",
        sleeveTexturePath="phase_4/maps/winter/gingerbread_outfit/tt_t_chr_avt_sleeve_gingerbread.png",
    ),
    ShirtItemType.PresentUniform: ShirtItemDefinition(
        name="Present Uniform",
        description="No Description",
        texturePath="phase_4/maps/winter/present_delivery_uniform_outfit/tt_t_chr_avt_shirt_pdu.png",
        sleeveTexturePath="phase_4/maps/winter/present_delivery_uniform_outfit/tt_t_chr_avt_sleeve_pdu.png",
    ),
    ShirtItemType.RagdollHumble: ShirtItemDefinition(
        name="Ragdoll Humble",
        description="No Description",
        texturePath="phase_4/maps/winter/ragdoll_outfits/humble/tt_t_chr_avt_shirt_ragdoll_humble.png",
        sleeveTexturePath="phase_4/maps/winter/ragdoll_outfits/humble/tt_t_chr_avt_sleeve_ragdoll_humble.png",
    ),
    ShirtItemType.RagdollRegal: ShirtItemDefinition(
        name="Ragdoll Regal",
        description="No Description",
        texturePath="phase_4/maps/winter/ragdoll_outfits/regal/tt_t_chr_avt_shirt_ragdoll_regal.png",
        sleeveTexturePath="phase_4/maps/winter/ragdoll_outfits/regal/tt_t_chr_avt_sleeve_ragdoll_regal.png",
    ),
    ShirtItemType.RagdollTraditional: ShirtItemDefinition(
        name="Ragdoll Traditional",
        description="No Description",
        texturePath="phase_4/maps/winter/ragdoll_outfits/traditional/tt_t_chr_avt_shirt_ragdoll_traditional.png",
        sleeveTexturePath="phase_4/maps/winter/ragdoll_outfits/traditional/tt_t_chr_avt_sleeve_ragdoll_traditional.png",
    ),
    ShirtItemType.Reindeer: ShirtItemDefinition(
        name="Reindeer",
        description="No Description",
        texturePath="phase_4/maps/winter/reindeer_outfit/tt_t_chr_avt_shirt_reindeer.png",
        sleeveTexturePath="phase_4/maps/winter/reindeer_outfit/tt_t_chr_avt_sleeve_reindeer.png",
    ),
    ShirtItemType.TinSoldierHumble: ShirtItemDefinition(
        name="Tin Soldier Humble",
        description="No Description",
        texturePath="phase_4/maps/winter/tin_soldier_outfits/humble/tt_t_chr_avt_shirt_tin_soldier_humble.png",
        sleeveTexturePath="phase_4/maps/winter/tin_soldier_outfits/humble/tt_t_chr_avt_sleeve_tin_soldier_humble.png",
    ),
    ShirtItemType.TinSoldierRegal: ShirtItemDefinition(
        name="Tin Soldier Regal",
        description="No Description",
        texturePath="phase_4/maps/winter/tin_soldier_outfits/regal/tt_t_chr_avt_shirt_tin_soldier_regal.png",
        sleeveTexturePath="phase_4/maps/winter/tin_soldier_outfits/regal/tt_t_chr_avt_sleeve_tin_soldier_regal.png",
    ),
    ShirtItemType.TinSoldierTraditional: ShirtItemDefinition(
        name="Tin Soldier Traditional",
        description="No Description",
        texturePath="phase_4/maps/winter/tin_soldier_outfits/traditional/tt_t_chr_avt_shirt_tin_soldier_traditional.png",
        sleeveTexturePath="phase_4/maps/winter/tin_soldier_outfits/traditional/tt_t_chr_avt_sleeve_tin_soldier_traditional.png",
    ),
    ShirtItemType.UglySweater: ShirtItemDefinition(
        name="Ugly Sweater",
        description="No Description",
        texturePath="phase_4/maps/winter/ugly_sweater_shirt/tt_t_chr_avt_shirt_ugly_sweater.png",
        sleeveTexturePath="phase_4/maps/winter/ugly_sweater_shirt/tt_t_chr_avt_sleeve_ugly_sweater.png",
    ),
    ShirtItemType.VintageSnowShirt: ShirtItemDefinition(
        name="Vintage Snow Shirt",
        description="No Description",
        texturePath="phase_4/maps/winter/vintage_snow_outfit/tt_t_chr_avt_shirt_vintage_snow.png",
        sleeveTexturePath="phase_4/maps/winter/vintage_snow_outfit/tt_t_chr_avt_sleeve_vintage_snow.png",
    ),
    ShirtItemType.NY2019Suit: ShirtItemDefinition(
        name="2019 Suit",
        description="No Description",
        texturePath="phase_4/maps/winter/2019_outfit/tt_t_chr_avt_shirt_2019_suit.png",
        sleeveTexturePath="phase_4/maps/winter/2019_outfit/tt_t_chr_avt_sleeve_2019_suit.png",
    ),
    ShirtItemType.NY2019Dress: ShirtItemDefinition(
        name="2019 Dress",
        description="No Description",
        texturePath="phase_4/maps/winter/2019_outfit/tt_t_chr_avt_shirt_2019_dress.png",
        sleeveTexturePath="phase_4/maps/winter/2019_outfit/tt_t_chr_avt_sleeve_2019_dress.png",
    ),
    ShirtItemType.CupidOutfit: ShirtItemDefinition(
        name="Cupid Outfit",
        description="No Description",
        texturePath="phase_4/maps/valentoon/tt_t_chr_avt_shirt_cupid.png",
        sleeveTexturePath="phase_4/maps/valentoon/tt_t_chr_avt_sleeve_cupid.png",
    ),
    ShirtItemType.DoesShirt: ShirtItemDefinition(
        name="Doe's Shirt",
        description="No Description",
        texturePath="phase_4/maps/social/doe/tt_t_chr_avt_shirt_doe.png",
        sleeveTexturePath="phase_4/maps/social/doe/tt_t_chr_avt_sleeve_doe.png",
    ),
    ShirtItemType.WebstersShirt: ShirtItemDefinition(
        name="Webster's Shirt",
        description="No Description",
        texturePath="phase_4/maps/social/webster/tt_t_chr_avt_shirt_webster.png",
        sleeveTexturePath="phase_4/maps/social/webster/tt_t_chr_avt_sleeve_webster.png",
    ),
    ShirtItemType.AngelWings: ShirtItemDefinition(
        name="Angel Wings",
        description="No Description",
        texturePath="phase_4/maps/apriltoons/wing_motif_shirt/tt_t_chr_avt_shirt_angel_wings.png",
        sleeveTexturePath="phase_4/maps/apriltoons/wing_motif_shirt/tt_t_chr_avt_sleeve_angel_wings.png",
    ),
    ShirtItemType.AviatorShirt: ShirtItemDefinition(
        name="Aviator Shirt",
        description="Sky Clan, here we come!",
        texturePath="phase_4/maps/apriltoons/aviator_outfit/tt_t_chr_avt_shirt_aviator_top.png",
        sleeveTexturePath="phase_4/maps/apriltoons/aviator_outfit/tt_t_chr_avt_sleeve_aviator_sleeve.png",
    ),
    ShirtItemType.WingsuitShirt: ShirtItemDefinition(
        name="Wingsuit Shirt",
        description="It might allow you to fly... not Loony Labs certified.",
        texturePath="phase_4/maps/apriltoons/wingsuit_outfit/tt_t_chr_avt_shirt_wingsuit.png",
        sleeveTexturePath="phase_4/maps/apriltoons/wingsuit_outfit/tt_t_chr_avt_sleeve_wingsuit.png",
    ),
    ShirtItemType.DragonWings: ShirtItemDefinition(
        name="Dragon Wings",
        description="No Description",
        texturePath="phase_4/maps/apriltoons/wing_motif_shirt/tt_t_chr_avt_shirt_dragon_wings.png",
        sleeveTexturePath="phase_4/maps/apriltoons/wing_motif_shirt/tt_t_chr_avt_sleeve_dragon_wings.png",
    ),
    ShirtItemType.ChibiWings: ShirtItemDefinition(
        name="Chibi Wings",
        description="No Description",
        texturePath="phase_4/maps/apriltoons/wing_motif_shirt/tt_t_chr_avt_shirt_chibi_wings.png",
        sleeveTexturePath="phase_4/maps/apriltoons/wing_motif_shirt/tt_t_chr_avt_sleeve_chibi_wings.png",
    ),
    ShirtItemType.BurgerShirt: ShirtItemDefinition(
        name="Burger Shirt",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_shirt_burger.png",
        sleeveTexturePath="phase_4/maps/tt_t_chr_avt_sleeve_burger.png",
    ),
    ShirtItemType.SellbotSeeker: ShirtItemDefinition(
        name="Sellbot Seeker",
        description="No Description",
        texturePath="phase_4/maps/dept_uniforms/sellbotuniform_top.png",
        sleeveTexturePath="phase_4/maps/dept_uniforms/sellbotuniform_sleeve.png",
    ),
    ShirtItemType.CashbotCatcher: ShirtItemDefinition(
        name="Cashbot Catcher",
        description="No Description",
        texturePath="phase_4/maps/dept_uniforms/cashbotuniform_top.png",
        sleeveTexturePath="phase_4/maps/dept_uniforms/cashbotuniform_sleeve.png",
    ),
    ShirtItemType.LawbotLiberator: ShirtItemDefinition(
        name="Lawbot Liberator",
        description="No Description",
        texturePath="phase_4/maps/dept_uniforms/lawbotuniform_top.png",
        sleeveTexturePath="phase_4/maps/dept_uniforms/lawbotuniform_sleeve.png",
    ),
    ShirtItemType.BossbotBasher: ShirtItemDefinition(
        name="Bossbot Basher ",
        description="No Description",
        texturePath="phase_4/maps/dept_uniforms/bossbotuniform_top.png",
        sleeveTexturePath="phase_4/maps/dept_uniforms/bossbotuniform_sleeve.png",
    ),
    ShirtItemType.OutbackUniform: ShirtItemDefinition(
        name="Outback Uniform",
        description="No Description",
        texturePath="phase_4/maps/outback/tt_t_chr_avt_shirt_outback_uniform.png",
        sleeveTexturePath="phase_4/maps/outback/tt_t_chr_avt_sleeve_outback_uniform.png",
    ),
    ShirtItemType.OutbackDenim: ShirtItemDefinition(
        name="Outback Denim",
        description="No Description",
        texturePath="phase_4/maps/outback/tt_t_chr_avt_shirt_outback_shirt.png",
        sleeveTexturePath="phase_4/maps/outback/tt_t_chr_avt_sleeve_outback_shirt.png",
    ),
    ShirtItemType.AlienShirt: ShirtItemDefinition(
        name="Alien Shirt",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/alien_top.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/alien_sleeve.png",
    ),
    ShirtItemType.CandyCornShirt: ShirtItemDefinition(
        name="Candy Corn Shirt",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/candycorn_top.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/candycorn_sleeves.png",
    ),
    ShirtItemType.Busted: ShirtItemDefinition(
        name="Busted!",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/jail_top.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/jail_sleeve.png",
    ),
    ShirtItemType.LawbotResistance: ShirtItemDefinition(
        name="Lawbot Resistance",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/l_resist_top.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/l_resist_sleeve.png",
    ),
    ShirtItemType.RetroRobotShirt: ShirtItemDefinition(
        name="Retro Robot Shirt",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/retrobot_top.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/retrobot_sleeve.png",
    ),
    ShirtItemType.RidingHoodShirt: ShirtItemDefinition(
        name="Riding Hood Shirt",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/ridinghood_top.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/ridinghood_sleeve.png",
    ),
    ShirtItemType.NurseShirt: ShirtItemDefinition(
        name="Nurse Shirt",
        description="Laugh your way to good laff!",
        texturePath="phase_13/maps/events/btl/clothing/nurse_top.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/nurse_sleeve.png",
    ),
    ShirtItemType.LazyBonesShirt: ShirtItemDefinition(
        name="Lazy Bones Shirt",
        description="No Description",
        texturePath="phase_4/maps/halloween/lazy_bones_outfit/lazy_bones_top.png",
        sleeveTexturePath="phase_4/maps/halloween/lazy_bones_outfit/lazy_bones_sleeve.png",
    ),
    ShirtItemType.SailorShirtA: ShirtItemDefinition(
        name="Sailor Shirt A",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_top_white.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/sailor/sailor_sleeve_white.png",
    ),
    ShirtItemType.SailorShirtB: ShirtItemDefinition(
        name="Sailor Shirt B",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_top_button_white.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/sailor/sailor_sleeve_white.png",
    ),
    ShirtItemType.BlueSailorShirtA: ShirtItemDefinition(
        name="Blue Sailor Shirt A",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_top_blue.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/sailor/sailor_sleeve_blue.png",
    ),
    ShirtItemType.BlueSailorShirtB: ShirtItemDefinition(
        name="Blue Sailor Shirt B",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_top_button_blue.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/sailor/sailor_sleeve_blue.png",
    ),
    ShirtItemType.CyanSailorShirtA: ShirtItemDefinition(
        name="Cyan Sailor Shirt A",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_top_cyan.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/sailor/sailor_sleeve_cyan.png",
    ),
    ShirtItemType.CyanSailorShirtB: ShirtItemDefinition(
        name="Cyan Sailor Shirt B",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_top_button_cyan.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/sailor/sailor_sleeve_cyan.png",
    ),
    ShirtItemType.GreenSailorShirtA: ShirtItemDefinition(
        name="Green Sailor Shirt A",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_top_green.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/sailor/sailor_sleeve_green.png",
    ),
    ShirtItemType.GreenSailorShirtB: ShirtItemDefinition(
        name="Green Sailor Shirt B",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_top_button_green.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/sailor/sailor_sleeve_green.png",
    ),
    ShirtItemType.OrangeSailorShirtA: ShirtItemDefinition(
        name="Orange Sailor Shirt A",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_top_orange.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/sailor/sailor_sleeve_orange.png",
    ),
    ShirtItemType.OrangeSailorShirtB: ShirtItemDefinition(
        name="Orange Sailor Shirt B",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_top_button_orange.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/sailor/sailor_sleeve_orange.png",
    ),
    ShirtItemType.PinkSailorShirtA: ShirtItemDefinition(
        name="Pink Sailor Shirt A",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_top_pink.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/sailor/sailor_sleeve_pink.png",
    ),
    ShirtItemType.PinkSailorShirtB: ShirtItemDefinition(
        name="Pink Sailor Shirt B",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_top_button_pink.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/sailor/sailor_sleeve_pink.png",
    ),
    ShirtItemType.PurpleSailorShirtA: ShirtItemDefinition(
        name="Purple Sailor Shirt A",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_top_purple.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/sailor/sailor_sleeve_purple.png",
    ),
    ShirtItemType.PurpleSailorShirtB: ShirtItemDefinition(
        name="Purple Sailor Shirt B",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_top_button_purple.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/sailor/sailor_sleeve_purple.png",
    ),
    ShirtItemType.RedSailorShirtA: ShirtItemDefinition(
        name="Red Sailor Shirt A",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_top_red.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/sailor/sailor_sleeve_red.png",
    ),
    ShirtItemType.RedSailorShirtB: ShirtItemDefinition(
        name="Red Sailor Shirt B",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_top_button_red.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/sailor/sailor_sleeve_red.png",
    ),
    ShirtItemType.BlackSailorShirtA: ShirtItemDefinition(
        name="Black Sailor Shirt A",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_top_black.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/sailor/sailor_sleeve_black.png",
    ),
    ShirtItemType.BlackSailorShirtB: ShirtItemDefinition(
        name="Black Sailor Shirt B",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_top_button_black.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/sailor/sailor_sleeve_black.png",
    ),
    ShirtItemType.GoldenSailorShirtA: ShirtItemDefinition(
        name="Golden Sailor Shirt A",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_top_yellow.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/sailor/sailor_sleeve_yellow.png",
    ),
    ShirtItemType.GoldenSailorShirtB: ShirtItemDefinition(
        name="Golden Sailor Shirt B",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/sailor/sailor_top_button_yellow.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/sailor/sailor_sleeve_yellow.png",
    ),
    ShirtItemType.TeamTreesShirt: ShirtItemDefinition(
        name="Team Trees Shirt",
        description="No Description",
        texturePath="phase_13/maps/events/trees/tree_shirt.png",
        sleeveTexturePath="phase_13/maps/events/trees/tree_shirt_sleeves.png",
    ),
    ShirtItemType.HomemadeRagdoll: ShirtItemDefinition(
        name="Homemade Ragdoll",
        description="No Description",
        texturePath="phase_4/maps/winter/homemade_ragdoll/ragdoll_homemade_top.png",
        sleeveTexturePath="phase_4/maps/winter/homemade_ragdoll/ragdoll_homemade_sleeve.png",
    ),
    ShirtItemType.HomemadeSoldier: ShirtItemDefinition(
        name="Homemade Soldier",
        description="No Description",
        texturePath="phase_4/maps/winter/homemade_tin_soldier/soldier_homemade_top.png",
        sleeveTexturePath="phase_4/maps/winter/homemade_tin_soldier/soldier_homemade_sleeve.png",
    ),
    ShirtItemType.RetroWinterSuit: ShirtItemDefinition(
        name="Retro Winter Suit",
        description="No Description",
        texturePath="phase_4/maps/winter/retro_winterwear/wintersuit_top.png",
        sleeveTexturePath="phase_4/maps/winter/retro_winterwear/wintersuit_sleeve.png",
    ),
    ShirtItemType.RetroWinterDress: ShirtItemDefinition(
        name="Retro Winter Dress",
        description="No Description",
        texturePath="phase_4/maps/winter/retro_winterwear/winterdress_top.png",
        sleeveTexturePath="phase_4/maps/winter/retro_winterwear/wintersuit_sleeve.png",
    ),
    ShirtItemType.SnowmanShirt: ShirtItemDefinition(
        name="Snowman Shirt",
        description="No Description",
        texturePath="phase_4/maps/winter/snowman_outfit/snowman_top.png",
        sleeveTexturePath="phase_4/maps/winter/snowman_outfit/snowman_sleeve.png",
    ),
    ShirtItemType.NewYears2020: ShirtItemDefinition(
        name="New Year's 2020",
        description="No Description",
        texturePath="phase_4/maps/winter/2020_outfit/2020suit_top.png",
        sleeveTexturePath="phase_4/maps/winter/2020_outfit/2020suit_sleeve.png",
    ),
    ShirtItemType.ValentoonsShirt: ShirtItemDefinition(
        name="Valentoon's Shirt",
        description="No Description",
        texturePath="phase_4/maps/valentoon/val_shirt.png",
        sleeveTexturePath="phase_4/maps/valentoon/val_sleeve.png",
    ),
    ShirtItemType.AgentSevensShirt: ShirtItemDefinition(
        name="Agent Seven's Shirt",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/seven_shirt.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/seven_sleeve.png",
    ),
    ShirtItemType.StPats2020: ShirtItemDefinition(
        name="St. Pat's 2020",
        description="No Description",
        texturePath="phase_13/maps/events/stpats/lucky_top.png",
        sleeveTexturePath="phase_13/maps/events/stpats/lucky_sleeve.png",
    ),
    ShirtItemType.ClownShirt: ShirtItemDefinition(
        name="Clown Shirt",
        description="Who thought Toons could get any sillier?",
        texturePath="phase_13/maps/events/apriltoons/clothing/clown_top.png",
        sleeveTexturePath="phase_13/maps/events/apriltoons/clothing/clown_sleeve.png",
    ),
    ShirtItemType.SevenStriped: ShirtItemDefinition(
        name="Seven Striped",
        description="Jackpot!",
        texturePath="phase_13/maps/events/apriltoons/clothing/sevenjersey_top.png",
        sleeveTexturePath="phase_13/maps/events/apriltoons/clothing/sevenjersey_sleeve.png",
    ),
    ShirtItemType.TripleRainbow: ShirtItemDefinition(
        name="Triple Rainbow",
        description="Triple rainbow! What does it mean?",
        texturePath="phase_13/maps/events/apriltoons/clothing/triplerainbow_top.png",
        sleeveTexturePath="phase_13/maps/events/apriltoons/clothing/triplerainbow_sleeve.png",
    ),
    ShirtItemType.BoardbotShirt: ShirtItemDefinition(
        name="Boardbot Shirt",
        description="No Description",
        texturePath="phase_4/maps/social/discord/cc_t_clth_shirt_promo_chairman.png",
        sleeveTexturePath="phase_4/maps/social/discord/cc_t_clth_shirt_promo_chairman_sleeve.png",
    ),
    ShirtItemType.BoredbotShirt: ShirtItemDefinition(
        name="Boredbot Shirt",
        description="No Description",
        texturePath="phase_13/maps/events/apriltoons/clothing/bored_top.png",
        sleeveTexturePath="phase_13/maps/events/apriltoons/clothing/bored_sleeve.png",
    ),
    ShirtItemType.JesterShirt: ShirtItemDefinition(
        name="Jester Shirt",
        description="Popularized in Ye Olde Toontowne!",
        texturePath="phase_13/maps/events/apriltoons/clothing/jester_top.png",
        sleeveTexturePath="phase_13/maps/events/apriltoons/clothing/jester_sleeve.png",
    ),
    ShirtItemType.BlackJesterShirt: ShirtItemDefinition(
        name="Black Jester Shirt",
        description="Popularized in Ye Olde Toontowne!",
        texturePath="phase_13/maps/events/apriltoons/clothing/jesterblack_top.png",
        sleeveTexturePath="phase_13/maps/events/apriltoons/clothing/jesterblack_sleeve.png",
    ),
    ShirtItemType.Easter2020: ShirtItemDefinition(
        name="Easter 2020",
        description="No Description",
        texturePath="phase_13/maps/events/easter2020/easter_2020_shirt.png",
        sleeveTexturePath="phase_13/maps/events/easter2020/easter_2020_sleeves.png",
    ),
    ShirtItemType.ExecutiveBoardbot: ShirtItemDefinition(
        name="Executive Boardbot",
        description="No Description",
        texturePath="phase_4/maps/social/discord/cc_t_clth_shirt_promo_chairman_exec.png",
        sleeveTexturePath="phase_4/maps/social/discord/cc_t_clth_shirt_promo_chairman_exec_sleeve.png",
    ),
    ShirtItemType.LawbotSuitTop: ShirtItemDefinition(
        name="Lawbot Suit Top",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/lawsuit_top.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/lawsuit_sleeve.png",
    ),
    ShirtItemType.CooktheCogsShirt: ShirtItemDefinition(
        name="Cook the Cogs Shirt",
        description="No Description",
        texturePath="phase_13/maps/events/july4/clothing/cook_top.png",
        sleeveTexturePath="phase_13/maps/events/july4/clothing/cook_sleeve.png",
    ),
    ShirtItemType.VacationFroge: ShirtItemDefinition(
        name="Vacation Froge",
        description="No Description",
        texturePath="phase_4/maps/frog_top.png",
        sleeveTexturePath="phase_4/maps/frog_sleeve.png",
    ),
    ShirtItemType.PhantoonShirt: ShirtItemDefinition(
        name="Phantoon Shirt",
        description="No Description",
        texturePath="phase_13/maps/events/halloween/phantoon_top.png",
        sleeveTexturePath="phase_13/maps/events/halloween/phantoon_sleeve.png",
    ),
    ShirtItemType.VolunteerRanger: ShirtItemDefinition(
        name="Volunteer Ranger",
        description="No Description",
        texturePath="phase_13/maps/events/btl/clothing/v_resist_shirt.png",
        sleeveTexturePath="phase_13/maps/events/btl/clothing/v_resist_sleeve.png",
    ),
    ShirtItemType.ToonsmasPast: ShirtItemDefinition(
        name="Toonsmas Past",
        description="No Description",
        texturePath="phase_4/maps/winter/past_outfit/past_top.png",
        sleeveTexturePath="phase_4/maps/winter/past_outfit/past_sleeve.png",
    ),
    ShirtItemType.ToonsmasPresent: ShirtItemDefinition(
        name="Toonsmas Present",
        description="No Description",
        texturePath="phase_4/maps/winter/present_outfit/present_top.png",
        sleeveTexturePath="phase_4/maps/winter/present_outfit/present_sleeve.png",
    ),
    ShirtItemType.ToonsmasFuture: ShirtItemDefinition(
        name="Toonsmas Future",
        description="No Description",
        texturePath="phase_4/maps/winter/future_outfit/future_top.png",
        sleeveTexturePath="phase_4/maps/winter/future_outfit/future_sleeve.png",
    ),
    ShirtItemType.NewYears2021: ShirtItemDefinition(
        name="New Year's 2021",
        description="No Description",
        texturePath="phase_4/maps/winter/2021_outfit/fireworks_top.png",
        sleeveTexturePath="phase_4/maps/winter/2021_outfit/fireworks_sleeve.png",
    ),
    ShirtItemType.TumblesShirt: ShirtItemDefinition(
        name="Tumbles' Shirt",
        description="No Description",
        texturePath="phase_4/maps/tumbles/tumbles_shirt.png",
        sleeveTexturePath="phase_4/maps/tumbles/tumbles_sleeve.png",
    ),
    ShirtItemType.Valentoons2021: ShirtItemDefinition(
        name="Valentoon's 2021",
        description="No Description",
        texturePath="phase_4/maps/valentoon/strawberry_top.png",
        sleeveTexturePath="phase_4/maps/valentoon/strawberry_sleeve.png",
    ),
    ShirtItemType.HallowopolisShirt: ShirtItemDefinition(
        name="Hallowopolis Shirt",
        description="No Description",
        texturePath="phase_4/maps/halloween/halloweentown_outfit/hwtown_top.png",
        sleeveTexturePath="phase_4/maps/halloween/halloweentown_outfit/hwtown_sleeve.png",
    ),
    ShirtItemType.Detective: ShirtItemDefinition(
        name="Detective",
        description="No Description",
        texturePath="phase_4/maps/halloween/detective_outfit/mystery_top.png",
        sleeveTexturePath="phase_4/maps/halloween/detective_outfit/mystery_sleeve.png",
    ),
    ShirtItemType.TwoPocketCargo: ShirtItemDefinition(
        name="Two-Pocket Cargo",
        description="No Description",
        texturePath="phase_4/maps/halloween/misc_outfit/cargo_top.png",
        sleeveTexturePath="phase_4/maps/halloween/misc_outfit/cargo_sleeve.png",
    ),
    ShirtItemType.JacketAndFlannel: ShirtItemDefinition(
        name="Jacket + Flannel",
        description="No Description",
        texturePath="phase_4/maps/halloween/misc_outfit/flannel_top.png",
        sleeveTexturePath="phase_4/maps/halloween/misc_outfit/flannel_sleeve.png",
    ),
    ShirtItemType.BlueNewstoon: ShirtItemDefinition(
        name="Blue Newstoon",
        description="No Description",
        texturePath="phase_4/maps/social/newstoon_blue/newstoon-blue_top.png",
        sleeveTexturePath="phase_4/maps/social/newstoon_blue/newstoon-blue_sleeve.png",
    ),
    ShirtItemType.GrayNewstoon: ShirtItemDefinition(
        name="Gray Newstoon",
        description="No Description",
        texturePath="phase_4/maps/social/newstoon_gray/newstoon-gray_top.png",
        sleeveTexturePath="phase_4/maps/social/newstoon_gray/newstoon-gray_sleeve.png",
    ),
    ShirtItemType.ChupShirt: ShirtItemDefinition(
        name="Chup Shirt",
        description="No Description",
        texturePath="phase_4/maps/halloween/chup_outfit/tt_t_chr_shirt_chup.png",
        sleeveTexturePath="phase_4/maps/halloween/chup_outfit/tt_t_chr_sleeve_chup.png",
    ),
    ShirtItemType.NewYears2022: ShirtItemDefinition(
        name="New Year's 2022",
        description="No Description",
        texturePath="phase_4/maps/winter/2022_outfit/2022_top.png",
        sleeveTexturePath="phase_4/maps/winter/2022_outfit/2022_sleeve.png",
    ),
    ShirtItemType.Valentoons2022: ShirtItemDefinition(
        name="Valentoon's 2022",
        description="No Description",
        texturePath="phase_4/maps/valentoon/val2022_top.png",
        sleeveTexturePath="phase_4/maps/valentoon/val2022_sleeve.png",
    ),
    ShirtItemType.DoctorToonShirt: ShirtItemDefinition(
        name="Doctor Toon Shirt",
        description="No Description",
        texturePath="phase_4/maps/social/doctor_toon/tt_t_chr_avt_shirt_doctortoon.png",
        sleeveTexturePath="phase_4/maps/social/doctor_toon/tt_t_chr_avt_sleeve_doctortoon.png",
    ),
    ShirtItemType.TrolleyEngineerShirt: ShirtItemDefinition(
        name="Trolley Engineer Shirt",
        description="All aboard!",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shirt_engineer.png",
        sleeveTexturePath="phase_4/maps/social/gumball/tt_t_chr_avt_sleeve_engineer.png",
    ),
    ShirtItemType.ArtisticShirt: ShirtItemDefinition(
        name="Artistic Shirt",
        description="Show off your true artistic passion!",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shirt_artistic.png",
        sleeveTexturePath="phase_4/maps/social/gumball/tt_t_chr_avt_sleeve_artistic.png",
    ),
    ShirtItemType.StarstruckShirt: ShirtItemDefinition(
        name="Starstruck Shirt",
        description="You'll outshine the moon with this one!",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shirt_moon.png",
        sleeveTexturePath="phase_4/maps/social/gumball/tt_t_chr_avt_sleeve_moon.png",
    ),
    ShirtItemType.RetroShirt: ShirtItemDefinition(
        name="Retro Shirt",
        description="Friday night fever!",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shirt_funky.png",
        sleeveTexturePath="phase_4/maps/social/gumball/tt_t_chr_avt_sleeve_funky.png",
    ),
    ShirtItemType.BattleJacket: ShirtItemDefinition(
        name="Battle Jacket",
        description="Seek and destroy the cogs!",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shirt_battlejacket.png",
        sleeveTexturePath="phase_4/maps/social/gumball/tt_t_chr_avt_sleeve_battlejacket.png",
    ),
    ShirtItemType.GumballMachineShirt: ShirtItemDefinition(
        name="Gumball Machine Shirt",
        description="Full of flavor!",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shirt_gumball.png",
        sleeveTexturePath="phase_4/maps/social/gumball/tt_t_chr_avt_sleeve_gumball.png",
    ),
    ShirtItemType.CardSuitShirtA: ShirtItemDefinition(
        name="Card Suit Shirt",
        description="Got a card up your sleeve?",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shirt_cards.png",
        sleeveTexturePath="phase_4/maps/social/gumball/tt_t_chr_avt_sleeve_cards.png",
    ),
    ShirtItemType.CardSuitShirtB: ShirtItemDefinition(
        name="Card Suit Shirt",
        description="Got a card up your sleeve?",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shirt_cardsF.png",
        sleeveTexturePath="phase_4/maps/social/gumball/tt_t_chr_avt_sleeve_cardsF.png",
    ),
    ShirtItemType.SchoolhouseFlannel: ShirtItemDefinition(
        name="Schoolhouse Flannel",
        description="Show your school spirit!",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shirt_flannel.png",
        sleeveTexturePath="phase_4/maps/social/gumball/tt_t_chr_avt_sleeve_flannel.png",
    ),
    ShirtItemType.SleepwalkerShirt: ShirtItemDefinition(
        name="Sleepwalker Shirt",
        description="Sleep tight!",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shirt_sleepwalker.png",
        sleeveTexturePath="phase_4/maps/social/gumball/tt_t_chr_avt_sleeve_sleepwalker.png",
    ),
    ShirtItemType.FruitPieShirt: ShirtItemDefinition(
        name="Fruit Pie Shirt",
        description="Tastes good, too!",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shirt_fruitpie.png",
        sleeveTexturePath="phase_4/maps/social/gumball/tt_t_chr_avt_sleeve_fruitpie.png",
    ),
    ShirtItemType.PinkDonutShirt: ShirtItemDefinition(
        name="Pink Donut Shirt",
        description="Frosted to perfection!",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shirt_donutpink.png",
        sleeveTexturePath="phase_4/maps/social/gumball/tt_t_chr_avt_sleeve_donutpink.png",
    ),
    ShirtItemType.BlueDonutShirt: ShirtItemDefinition(
        name="Blue Donut Shirt",
        description="Frosted to perfection!",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shirt_donutblue.png",
        sleeveTexturePath="phase_4/maps/social/gumball/tt_t_chr_avt_sleeve_donutblue.png",
    ),
    ShirtItemType.ChocolateDonutShirt: ShirtItemDefinition(
        name="Chocolate Donut Shirt",
        description="Frosted to perfection!",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shirt_donutchocolate.png",
        sleeveTexturePath="phase_4/maps/social/gumball/tt_t_chr_avt_sleeve_donutchocolate.png",
    ),
    ShirtItemType.LemonDonutShirt: ShirtItemDefinition(
        name="Lemon Donut Shirt",
        description="Frosted to perfection!",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shirt_donutlemon.png",
        sleeveTexturePath="phase_4/maps/social/gumball/tt_t_chr_avt_sleeve_donutlemon.png",
    ),
    ShirtItemType.VanillaDonutShirt: ShirtItemDefinition(
        name="Vanilla Donut Shirt",
        description="Frosted to perfection!",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shirt_donutvanilla.png",
        sleeveTexturePath="phase_4/maps/social/gumball/tt_t_chr_avt_sleeve_donutvanilla.png",
    ),
    ShirtItemType.BluePainter: ShirtItemDefinition(
        name="Blue Painter",
        description="Paint not included.",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shirt_painter_blue.png",
        sleeveTexturePath="phase_4/maps/social/gumball/tt_t_chr_avt_sleeve_painter_blue.png",
    ),
    ShirtItemType.RedPainter: ShirtItemDefinition(
        name="Red Painter",
        description="Paint not included.",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shirt_painter_red.png",
        sleeveTexturePath="phase_4/maps/social/gumball/tt_t_chr_avt_sleeve_painter_red.png",
    ),
    ShirtItemType.GreenPainter: ShirtItemDefinition(
        name="Green Painter",
        description="Paint not included.",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shirt_painter_green.png",
        sleeveTexturePath="phase_4/maps/social/gumball/tt_t_chr_avt_sleeve_painter_green.png",
    ),
    ShirtItemType.YellowPainter: ShirtItemDefinition(
        name="Yellow Painter",
        description="Paint not included.",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shirt_painter_yellow.png",
        sleeveTexturePath="phase_4/maps/social/gumball/tt_t_chr_avt_sleeve_painter_yellow.png",
    ),
    ShirtItemType.ChefCoat: ShirtItemDefinition(
        name="Chef Coat",
        description="No Description",
        texturePath="phase_4/maps/social/gumball/tt_t_chr_avt_shirt_chef.png",
        sleeveTexturePath="phase_4/maps/social/gumball/tt_t_chr_avt_sleeve_chef.png",
    ),
    ShirtItemType.NewYears2023: ShirtItemDefinition(
        name="New Year's 2023",
        description="No Description",
        texturePath="phase_4/maps/winter/2023_outfit/2023_top.png",
        sleeveTexturePath="phase_4/maps/winter/2023_outfit/2023_sleeve.png",
    ),
    ShirtItemType.ArmoredChestplate: ShirtItemDefinition(
        name="Armored Chestplate",
        description="No Description",
        texturePath="phase_4/maps/bosses/tt_t_chr_avt_shirt_armor.png",
        sleeveTexturePath="phase_4/maps/bosses/tt_t_chr_avt_sleeve_armor.png",
    ),
    ShirtItemType.RejectedSweater: ShirtItemDefinition(
        name="Rejected Sweater",
        description="No Description",
        texturePath="phase_4/maps/apriltoons/ottoman_sweater/cc_t_clth_shirt_ottoman_sweater.png",
        sleeveTexturePath="phase_4/maps/apriltoons/ottoman_sweater/cc_t_clth_sleeve_ottoman_sleeve.png",
    ),
    ShirtItemType.HighRollersSuit: ShirtItemDefinition(
        name="High Roller's Suit",
        description="No Description",
        texturePath="phase_4/maps/apriltoons/high_roller_outfit/cc_t_clth_shirt_high_roller.png",
        sleeveTexturePath="phase_4/maps/apriltoons/high_roller_outfit/cc_t_clth_sleeve_high_roller.png",
    ),
    ShirtItemType.HighRollersProdigalSuit: ShirtItemDefinition(
        name="High Roller's Prodigal Suit",
        description="No Description",
        texturePath="phase_4/maps/apriltoons/high_roller_outfit/cc_t_clth_shirt_high_roller_black.png",
        sleeveTexturePath="phase_4/maps/apriltoons/high_roller_outfit/cc_t_clth_sleeve_high_roller_black.png",
    ),
    ShirtItemType.CybertoonShirt: ShirtItemDefinition(
        name="Cybertoon Shirt",
        description="No Description",
        texturePath="phase_4/maps/social/cyberpunk/cc_t_clth_shirt_cyberpunk.png",
        sleeveTexturePath="phase_4/maps/social/cyberpunk/cc_t_clth_sleeve_cyberpunk.png",
    ),
    ShirtItemType.BroVinci: ShirtItemDefinition(
        name="Bro Vinci's Shirt",
        description="No Description",
        texturePath="phase_4/maps/social/bro/tt_t_chr_avt_shirt_bro.png",
        sleeveTexturePath="phase_4/maps/social/bro/tt_t_chr_avt_sleeve_bro.png",
    ),
}
