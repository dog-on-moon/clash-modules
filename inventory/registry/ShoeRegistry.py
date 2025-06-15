"""
This module contains the item data for shoes.
"""
from panda3d.core import NodePath, Texture

from toontown.inventory.base.InventoryItem import InventoryItem
from typing import Dict, Optional
from strenum import StrEnum

from toontown.inventory.definitions.AccessoryDefinition import AccessoryDefinition
from toontown.inventory.enums.ItemEnums import ShoeItemType
from toontown.inventory.enums.ItemTags import ItemTag
from toontown.toonbase import ProcessGlobals


class ShoeType(StrEnum):
    Shoes       = 'shoes'
    BootsShort  = 'boots_short'
    BootsLong   = 'boots_long'


class ShoeItemDefinition(AccessoryDefinition):
    """
    The definition structure for eating a shoe.
    """
    # preload leg model for optimization purposes
    if ProcessGlobals.getCurrentProcess() == ProcessGlobals.Process.Client:
        legModel = loader.loadModel('phase_3/models/char/toons/legs/tt_a_chr_dgm_shorts_legs_1000')

    def __init__(self,
                 texturePath,
                 shoeType: ShoeType,
                 bsTexturePath: str | None = None,
                 blTexturePath: str | None = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.shoeType = shoeType
        self.texturePath = texturePath

        # Specific texpath overrides for BootsShort and BootsLong
        self.bsTexturePath = bsTexturePath
        self.blTexturePath = blTexturePath

    def getItemTypeName(self):
        return 'Shoes'

    def getShoeType(self) -> ShoeType:
        return self.shoeType

    def getTexturePath(self):
        if self.getShoeType() == ShoeType.BootsShort and self.bsTexturePath:
            return self.bsTexturePath
        if self.getShoeType() == ShoeType.BootsLong and self.blTexturePath:
            return self.blTexturePath
        return self.texturePath

    def getTags(self, item: 'InventoryItem') -> set[ItemTag]:
        tags = super().getTags(item)
        tags.add(ItemTag.Shoes)
        return tags

    def makeItemModel(self, item: Optional[InventoryItem] = None, *extraArgs) -> NodePath:
        # Load model.
        model = NodePath('feet')
        model = self.legModel.find('**/' + str(self.getShoeType())).copyTo(model)

        # Apply texture if need be.
        texturePath = self.getTexturePath()
        if texturePath:
            texture = loader.loadTexture(texturePath)
            texture.setMinfilter(Texture.FTLinearMipmapLinear)
            texture.setMagfilter(Texture.FTLinear)
            model.setTexture(texture, 1)

        # Return model.
        return model


# The registry dictionary for shoes.
ShoeRegistry: Dict[ShoeItemType, ShoeItemDefinition] = {
    ShoeItemType.GreenAthleticShoes: ShoeItemDefinition(
        name="Green Athletic Shoes",
        description="No Description",
        texturePath="phase_3/maps/tt_t_chr_avt_acc_sho_athleticGreen.png",
        shoeType=ShoeType.Shoes,
    ),
    ShoeItemType.RedAthleticShoes: ShoeItemDefinition(
        name="Red Athletic Shoes",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_athleticRed.png",
        shoeType=ShoeType.Shoes,
    ),
    ShoeItemType.GreenToonBoots: ShoeItemDefinition(
        name="Green Toon Boots",
        description="No Description",
        texturePath="phase_3/maps/tt_t_chr_avt_acc_sho_docMartinBootsGreen.png",
        blTexturePath="phase_3/maps/tt_t_chr_avt_acc_sho_docMartinBootsGreenLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.GreenSneakers: ShoeItemDefinition(
        name="Green Sneakers",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_converseStyleGreen.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.BoatShoes: ShoeItemDefinition(
        name="Boat Shoes",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_deckShoes.png",
        shoeType=ShoeType.Shoes,
    ),
    ShoeItemType.YellowAthleticShoes: ShoeItemDefinition(
        name="Yellow Athletic Shoes",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_athleticYellow.png",
        shoeType=ShoeType.Shoes,
    ),
    ShoeItemType.BlackSneakers: ShoeItemDefinition(
        name="Black Sneakers",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_converseStyleBlack.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.WhiteSneakers: ShoeItemDefinition(
        name="White Sneakers",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_converseStyleWhite.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.PinkSneakers: ShoeItemDefinition(
        name="Pink Sneakers",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_converseStylePink.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.CowboyBoots: ShoeItemDefinition(
        name="Cowboy Boots",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_cowboyBoots.png",
        blTexturePath="phase_4/maps/tt_t_chr_avt_acc_sho_cowboyBootsLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.GreenHiTops: ShoeItemDefinition(
        name="Green Hi-Tops",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_hiTopSneakers.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.RedSuperToonBoots: ShoeItemDefinition(
        name="Red Super Toon Boots",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_superToonRedBoots.png",
        blTexturePath="phase_4/maps/tt_t_chr_avt_acc_sho_superToonRedBootsLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.GreenTennisShoes: ShoeItemDefinition(
        name="Green Tennis Shoes",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_tennisShoesGreen.png",
        shoeType=ShoeType.Shoes,
    ),
    ShoeItemType.PinkTennisShoes: ShoeItemDefinition(
        name="Pink Tennis Shoes",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_tennisShoesPink.png",
        shoeType=ShoeType.Shoes,
    ),
    ShoeItemType.RedSneakers: ShoeItemDefinition(
        name="Red Sneakers",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_converseStyleRed.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.AquaToonBoots: ShoeItemDefinition(
        name="Aqua Toon Boots",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_docMartinBootsAqua.png",
        blTexturePath="phase_4/maps/tt_t_chr_avt_acc_sho_docMartinBootsAquaLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.BrownToonBoots: ShoeItemDefinition(
        name="Brown Toon Boots",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_docMartinBootsBrown.png",
        blTexturePath="phase_4/maps/tt_t_chr_avt_acc_sho_docMartinBootsBrownLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.YellowToonBoots: ShoeItemDefinition(
        name="Yellow Toon Boots",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_docMartinBootsYellow.png",
        blTexturePath="phase_4/maps/tt_t_chr_avt_acc_sho_docMartinBootsYellowLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.Loafers: ShoeItemDefinition(
        name="Loafers",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_loafers.png",
        shoeType=ShoeType.Shoes,
    ),
    ShoeItemType.MotorcycleBoots: ShoeItemDefinition(
        name="Motorcycle Boots",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_motorcycleBoots.png",
        blTexturePath="phase_4/maps/tt_t_chr_avt_acc_sho_motorcycleBootsLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.Oxfords: ShoeItemDefinition(
        name="Oxfords",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_oxfords.png",
        shoeType=ShoeType.Shoes,
    ),
    ShoeItemType.PinkRainBoots: ShoeItemDefinition(
        name="Pink Rain Boots",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_rainBootsPink.png",
        blTexturePath="phase_4/maps/tt_t_chr_avt_acc_sho_rainBootsPinkLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.JollyBoots: ShoeItemDefinition(
        name="Jolly Boots",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_santaBoots.png",
        blTexturePath="phase_4/maps/tt_t_chr_avt_acc_sho_santaBootsLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.BeigeWinterBoots: ShoeItemDefinition(
        name="Beige Winter Boots",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_winterBootsBeige.png",
        blTexturePath="phase_4/maps/tt_t_chr_avt_acc_sho_winterBootsBeigeLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.PinkWinterBoots: ShoeItemDefinition(
        name="Pink Winter Boots",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_winterBootsPink.png",
        blTexturePath="phase_4/maps/tt_t_chr_avt_acc_sho_winterBootsPinkLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.WorkBoots: ShoeItemDefinition(
        name="Work Boots",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_workBoots.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.YellowSneakers: ShoeItemDefinition(
        name="Yellow Sneakers",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_converseStyleYellow.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.PinkToonBoots: ShoeItemDefinition(
        name="Pink Toon Boots",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_docMartinBootsPink.png",
        blTexturePath="phase_4/maps/tt_t_chr_avt_acc_sho_docMartinBootsPinkLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.PinkHiTops: ShoeItemDefinition(
        name="Pink Hi-Tops",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_hiTopSneakersPink.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.RedDotsRainBoots: ShoeItemDefinition(
        name="Red Dots Rain Boots",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_rainBootsRedDots.png",
        blTexturePath="phase_4/maps/tt_t_chr_avt_acc_sho_rainBootsRedDotsLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.PurpleTennisShoes: ShoeItemDefinition(
        name="Purple Tennis Shoes",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_tennisShoesPurple.png",
        shoeType=ShoeType.Shoes,
    ),
    ShoeItemType.VioletTennisShoes: ShoeItemDefinition(
        name="Violet Tennis Shoes",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_tennisShoesViolet.png",
        shoeType=ShoeType.Shoes,
    ),
    ShoeItemType.YellowTennisShoes: ShoeItemDefinition(
        name="Yellow Tennis Shoes",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_tennisShoesYellow.png",
        shoeType=ShoeType.Shoes,
    ),
    ShoeItemType.BlueRainBoots: ShoeItemDefinition(
        name="Blue Rain Boots",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_rainBootsBlue.png",
        blTexturePath="phase_4/maps/tt_t_chr_avt_acc_sho_rainBootsBlueLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.YellowRainBoots: ShoeItemDefinition(
        name="Yellow Rain Boots",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_rainBootsYellow.png",
        blTexturePath="phase_4/maps/tt_t_chr_avt_acc_sho_rainBootsYellowLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.BlackAthleticShoes: ShoeItemDefinition(
        name="Black Athletic Shoes",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_athleticBlack.png",
        shoeType=ShoeType.Shoes,
    ),
    ShoeItemType.PirateShoes: ShoeItemDefinition(
        name="Pirate Shoes",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_pirate.png",
        blTexturePath="phase_4/maps/tt_t_chr_avt_acc_sho_pirateLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.ToonosaurFeet: ShoeItemDefinition(
        name="Toonosaur Feet",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_dinosaur.png",
        blTexturePath="phase_4/maps/tt_t_chr_avt_acc_sho_dinosaurLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.Wingtips: ShoeItemDefinition(
        name="Wingtips",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_wingtips.png",
        shoeType=ShoeType.Shoes,
    ),
    ShoeItemType.BlackFancyShoes: ShoeItemDefinition(
        name="Black Fancy Shoes",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_maryJaneShoes.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.PurpleBoots: ShoeItemDefinition(
        name="Purple Boots",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsPurple.png",
        blTexturePath="phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsPurpleLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.BrownFancyShoes: ShoeItemDefinition(
        name="Brown Fancy Shoes",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_maryJaneShoesBrown.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.RedFancyShoes: ShoeItemDefinition(
        name="Red Fancy Shoes",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_maryJaneShoesRed.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.BlueSquareBoots: ShoeItemDefinition(
        name="Blue Square Boots",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsBlueSquares.png",
        blTexturePath="phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsBlueSquaresLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.GreenHeartsBoots: ShoeItemDefinition(
        name="Green Hearts Boots",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsGreenHearts.png",
        blTexturePath="phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsGreenHeartsLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.GreyDotsBoots: ShoeItemDefinition(
        name="Grey Dots Boots",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsGreyDots.png",
        blTexturePath="phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsGreyDotsLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.OrangeStarsBoots: ShoeItemDefinition(
        name="Orange Stars Boots",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsOrangeStars.png",
        blTexturePath="phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsOrangeStarsLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.PinkStarsBoots: ShoeItemDefinition(
        name="Pink Stars Boots",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsPinkStars.png",
        blTexturePath="phase_4/maps/tt_t_chr_avt_acc_sho_fashionBootsPinkStarsLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.PurpleFancyShoes: ShoeItemDefinition(
        name="Purple Fancy Shoes",
        description="No Description",
        texturePath="phase_4/maps/tt_t_chr_avt_acc_sho_maryJaneShoesPurple.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.SpaceBoots: ShoeItemDefinition(
        name="Space Boots",
        description="No Description",
        texturePath="phase_4/maps/halloween/accessories_textures/tt_t_chr_avt_acc_sho_space_boots.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.WitchShoes: ShoeItemDefinition(
        name="Witch Shoes",
        description="No Description",
        texturePath="phase_4/maps/halloween/accessories_textures/tt_t_chr_avt_acc_sho_witch.png",
        blTexturePath="phase_4/maps/halloween/accessories_textures/tt_t_chr_avt_acc_sho_witchLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.SkeletonShoes: ShoeItemDefinition(
        name="Skeleton Shoes",
        description="No Description",
        texturePath="phase_4/maps/halloween/accessories_textures/tt_t_chr_avt_acc_sho_skeleton.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.AlchemistShoes: ShoeItemDefinition(
        name="Alchemist Shoes",
        description="No Description",
        texturePath="phase_4/maps/halloween/accessories_textures/tt_t_chr_avt_acc_sho_alchemist.png",
        blTexturePath="phase_4/maps/halloween/accessories_textures/tt_t_chr_avt_acc_sho_alchemistLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.HumbleRagdoll: ShoeItemDefinition(
        name="Humble Ragdoll",
        description="No Description",
        texturePath="phase_4/maps/winter/accessories_textures/humble-ragdoll-shoes.png",
        blTexturePath="phase_4/maps/winter/accessories_textures/humble-ragdoll-shoesLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.RegalRagdoll: ShoeItemDefinition(
        name="Regal Ragdoll",
        description="No Description",
        texturePath="phase_4/maps/winter/accessories_textures/regal-ragdoll-shoes.png",
        blTexturePath="phase_4/maps/winter/accessories_textures/regal-ragdoll-shoesLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.TraditionalRagdoll: ShoeItemDefinition(
        name="Traditional Ragdoll",
        description="No Description",
        texturePath="phase_4/maps/winter/accessories_textures/tradi-ragdoll-shoes.png",
        blTexturePath="phase_4/maps/winter/accessories_textures/tradi-ragdoll-shoesLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.HumbleTin: ShoeItemDefinition(
        name="Humble Tin",
        description="No Description",
        texturePath="phase_4/maps/winter/accessories_textures/humble-tinsoldier-shoes.png",
        blTexturePath="phase_4/maps/winter/accessories_textures/humble-tinsoldier-shoesLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.RegalTin: ShoeItemDefinition(
        name="Regal Tin",
        description="No Description",
        texturePath="phase_4/maps/winter/accessories_textures/regal-tinsoldier-shoes.png",
        blTexturePath="phase_4/maps/winter/accessories_textures/regal-tinsoldier-shoesLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.TraditionalTin: ShoeItemDefinition(
        name="Traditional Tin",
        description="No Description",
        texturePath="phase_4/maps/winter/accessories_textures/tradi-tinsoldier-shoes.png",
        blTexturePath="phase_4/maps/winter/accessories_textures/tradi-tinsoldier-shoesLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.VintageSnow: ShoeItemDefinition(
        name="Vintage Snow",
        description="No Description",
        texturePath="phase_4/maps/winter/vintage_snow_outfit/tt_t_chr_avt_acc_sho_vintage_snow.png",
        blTexturePath="phase_4/maps/winter/vintage_snow_outfit/tt_t_chr_avt_acc_sho_vintage_snowLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.AviatorBoots: ShoeItemDefinition(
        name="Aviator Boots",
        description="Sky Clan, here we come!",
        texturePath="phase_4/maps/apriltoons/aviator_outfit/aviator_boots.png",
        blTexturePath="phase_4/maps/apriltoons/aviator_outfit/aviator_bootsLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.WingsuitBoots: ShoeItemDefinition(
        name="Wingsuit Boots",
        description="It might allow you to fly... not Loony Labs certified.",
        texturePath="phase_4/maps/apriltoons/wingsuit_outfit/wingsuit_boots.png",
        blTexturePath="phase_4/maps/apriltoons/wingsuit_outfit/wingsuit_bootsLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.OutbackShoes: ShoeItemDefinition(
        name="Outback Shoes",
        description="Perfect for an outback adventure!",
        texturePath="phase_4/maps/outback/outback_shoes.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.PumpkinShoes: ShoeItemDefinition(
        name="Pumpkin Shoes",
        description="No Description",
        texturePath="phase_13/maps/events/btl/accessories/pumpkin_shoes.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.LazyBonesSlippers: ShoeItemDefinition(
        name="Lazy Bones Slippers",
        description="No Description",
        texturePath="phase_4/maps/halloween/lazy_bones_outfit/lazy_bones_shoes.png",
        shoeType=ShoeType.Shoes,
    ),
    ShoeItemType.HomemadeRagdoll: ShoeItemDefinition(
        name="Homemade Ragdoll",
        description="No Description",
        texturePath="phase_4/maps/winter/homemade_ragdoll/ragdoll_homemade_boots.png",
        blTexturePath="phase_4/maps/winter/homemade_ragdoll/ragdoll_homemade_bootsLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.HomemadeTin: ShoeItemDefinition(
        name="Homemade Tin",
        description="No Description",
        texturePath="phase_4/maps/winter/homemade_tin_soldier/soldier_homemade_boots.png",
        blTexturePath="phase_4/maps/winter/homemade_tin_soldier/soldier_homemade_bootsLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.RetroWinterSuit: ShoeItemDefinition(
        name="Retro Winter Suit",
        description="No Description",
        texturePath="phase_4/maps/winter/retro_winterwear/wintersuit_shoes.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.RetroWinterDress: ShoeItemDefinition(
        name="Retro Winter Dress",
        description="No Description",
        texturePath="phase_4/maps/winter/retro_winterwear/winterdress_shoes.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.BreaktheLawShoes: ShoeItemDefinition(
        name="Break the Law Shoes",
        description="No Description",
        texturePath="phase_13/maps/events/apriltoons/accessories/btl_lbhq_shoes.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.TripleRainbowShoes: ShoeItemDefinition(
        name="Triple Rainbow Shoes",
        description="Triple rainbow! What does it mean?",
        texturePath="phase_13/maps/events/apriltoons/accessories/triplerainbow_shoes.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.ChairmanShoes: ShoeItemDefinition(
        name="Chairman Shoes",
        description="No Description",
        texturePath="phase_4/maps/social/discord/cc_t_acc_sho_promo_chairman.png",
        shoeType=ShoeType.Shoes,
    ),
    ShoeItemType.PhantoonShoes: ShoeItemDefinition(
        name="Phantoon Shoes",
        description="No Description",
        texturePath="phase_13/maps/events/halloween/phantoon_boots.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.TumblesShoes: ShoeItemDefinition(
        name="Tumbles' Shoes",
        description="No Description",
        texturePath="phase_4/maps/tumbles/tumbles_shoes.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.HallowopolisBoots: ShoeItemDefinition(
        name="Hallowopolis Boots",
        description="No Description",
        texturePath="phase_4/maps/halloween/halloweentown_outfit/hwtown_boots.png",
        blTexturePath="phase_4/maps/halloween/halloweentown_outfit/hwtown_bootsLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.DiverBoots: ShoeItemDefinition(
        name="Diver Boots",
        description="No Description",
        texturePath="phase_4/maps/bosses/shoes_diver.png",
        blTexturePath="phase_4/maps/bosses/shoes_diverLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.TrolleyEngineerBoots: ShoeItemDefinition(
        name="Trolley Engineer Boots",
        description="All aboard!",
        texturePath="phase_4/maps/social/gumball/ttcc_acc_engineer_shoes.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.FruitPieShoes: ShoeItemDefinition(
        name="Fruit Pie Shoes",
        description="Tastes good, too!",
        texturePath="phase_4/maps/social/gumball/ttcc_acc_fruitpieshoes.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.CardSuitShoesRed: ShoeItemDefinition(
        name="Red Card Suit Shoes",
        description="Not to be shuffled, but used to shuffle.",
        texturePath="phase_4/maps/social/gumball/ttcc_acc_cardBoots_red.png",
        blTexturePath="phase_4/maps/social/gumball/ttcc_acc_cardBoots_redLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.CardSuitShoesBlack: ShoeItemDefinition(
        name="Black Card Suit Shoes",
        description="Not to be shuffled, but used to shuffle.",
        texturePath="phase_4/maps/social/gumball/ttcc_acc_cardBoots_black.png",
        blTexturePath="phase_4/maps/social/gumball/ttcc_acc_cardBoots_blackLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.GatorSlippers: ShoeItemDefinition(
        name="Gator Slippers",
        description="They aren't crocodiles!",
        texturePath="phase_4/maps/social/gumball/ttcc_acc_gator_shoes.png",
        blTexturePath="phase_4/maps/social/gumball/ttcc_acc_gator_shoesLL.png",
        shoeType=ShoeType.BootsLong,
    ),
    ShoeItemType.PaintersMocasins: ShoeItemDefinition(
        name="Painter's Mocasins",
        description="Paint not included.",
        texturePath="phase_4/maps/social/gumball/ttcc_acc_painter_shoes.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.ArmoredGreaves: ShoeItemDefinition(
        name="Armored Greaves",
        description="No Description",
        texturePath="phase_4/maps/bosses/ttcc_acc_armored_boots.png",
        shoeType=ShoeType.BootsShort,
    ),
    ShoeItemType.CybertoonShoes: ShoeItemDefinition(
        name="Cybertoon Shoes",
        description="No Description",
        texturePath="phase_4/maps/social/cyberpunk/cc_t_acc_shoes_cyberpunk.png",
        shoeType=ShoeType.BootsShort,
    ),
}
