"""
This module contains the item data for chat stickers.
"""
from panda3d.core import NodePath

from toontown.chat.services.ChatAssetCache import ChatAssetCache
from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.base.ItemDefinition import ItemDefinition
from typing import Dict, Type, Union, Optional, Set
from enum import IntEnum
import random

from toontown.inventory.enums.ItemAttribute import ItemAttribute
from toontown.inventory.enums.ItemEnums import ChatStickersItemType
from toontown.inventory.enums.ItemModifier import ItemModifier
from toontown.inventory.enums.ItemTags import ItemTag, ItemCategory
from toontown.inventory.enums.RarityEnums import Rarity, getRaritySteps
from toontown.stickers.sequences.StickerSequenceBase import StickerSequenceBase
from toontown.stickers.sequences.DiceStickerSequence import DiceStickerSequence
from toontown.toonbase import ToontownGlobals
from toontown.stickers.sequences.DefaultStickerSequence import DefaultStickerSequence


DefaultSequence = DefaultStickerSequence

AssetCache = ChatAssetCache()

StickerNameToEnum = {}


class ChatStickerDefinition(ItemDefinition):
    """
    The definition structure for chat stickers.
    """
    def __init__(self,
                 modelPath: str,
                 stickerSound: str = "phase_3.5/audio/sfx/Sticker_Pop.ogg",
                 customSequence: Union[None, Type[StickerSequenceBase]] = None,
                 isDefault: bool = False,
                 isSuit: bool = False,
                 stickerMenuAlphabeticalName: Union[None, str] = None,
                 stickerScale3d: Union[float, tuple] = 1.0,
                 stickerScale2d: Union[float, tuple] = 1.0,
                 **kwargs):
        super().__init__(**kwargs)
        self.modelPath = modelPath
        self.stickerSound = stickerSound
        self.customSequence = customSequence
        self.isDefault = isDefault
        self.isSuit = isSuit
        self.stickerMenuAlphabeticalName = stickerMenuAlphabeticalName
        self.stickerScale3d = stickerScale3d
        self.stickerScale2d = stickerScale2d

    def getModelPath(self, modifier: Optional[int] = None):
        return self.modelPath

    def getStickerSound(self):
        return AssetCache.getSfx(self.stickerSound, forceLoad=True)

    def getBaseName(self, item, modifier: Optional[int] = None):
        return super().getName()

    def getName(self, item: Optional[InventoryItem] = None, modifier: Optional[int] = None) -> str:
        name = self.getBaseName(item, modifier=modifier)
        if self.isFoil(item):
            return f'Foil {name}'
        return name

    def getItemTypeName(self):
        return 'Sticker'

    def getRewardName(self, item: Optional[InventoryItem] = None):
        return f'{self.getName()} Sticker'

    def getRarity(self, item: Optional[InventoryItem] = None) -> Rarity:
        rarity = super().getRarity(item)
        if self.isFoil(item):
            return getRaritySteps(rarity, 2)
        return rarity

    def makeItemModel(self, item: Optional[InventoryItem] = None, *extraArgs) -> NodePath:
        """
        Returns a nodepath that represents this item.
        """
        modifier = extraArgs[0] if len(extraArgs) else None
        stickerNode = AssetCache.getNodePath("phase_3.5/models/gui/stickers", self.getModelPath(modifier=modifier))

        return stickerNode

    def getSequence(self) -> Type[StickerSequenceBase]:
        if self.customSequence:
            return self.customSequence
        return DefaultStickerSequence

    def getItemCategory(self) -> ItemCategory:
        return ItemCategory.Cosmetic

    def getTags(self, item: 'InventoryItem') -> Set[ItemTag]:
        tags = super().getTags(item)
        if self.isFoil(item):
            tags.add(ItemTag.StickersFoil)
        if self.isDefault:
            tags.add(ItemTag.DefaultSticker)
        if self.isSuit:
            tags.add(ItemTag.SuitSticker)
        return tags

    def getStickerMenuAlphabeticalName(self):
        if self.stickerMenuAlphabeticalName:
            return self.stickerMenuAlphabeticalName
        return self.name

    def getStickerScale3D(self):
        if type(self.stickerScale3d) in (tuple, list):
            return (1.6*self.stickerScale3d[0], 1.6*self.stickerScale3d[1], 1.6*self.stickerScale3d[2])

        return 1.6 * self.stickerScale3d

    def getStickerScale2D(self):
        return self.stickerScale2d

    """
    Item-Related Getters
    """

    @staticmethod
    def isFoil(item: Optional[InventoryItem]) -> bool:
        return item and item.getAttribute(ItemAttribute.MODIFIER) == ItemModifier.STICKER_FOIL


class DiceRollStickerItemDefinition(ChatStickerDefinition):
    """
    The definition specifically for the dice roll sticker type
    """
    def getBaseName(self, item: Optional[InventoryItem] = None, modifier: Optional[int] = None) -> str:
        if modifier is None:
            # Return default name for the dice sticker.
            return super().getBaseName(item=item, modifier=modifier)
        else:
            # Pick one determined by seed
            rng = random.Random(modifier)
            pip = rng.randint(1, 6)
            return f"Rolled a {pip}"

    def getModelPath(self, modifier: Optional[int] = None):
        if modifier is None:
            # Return default image for the dice sticker.
            return super().getModelPath(modifier=modifier)
        else:
            # Pick one determined by seed
            rng = random.Random(modifier)
            pip = rng.randint(1, 6)
            return f"**/dice_{pip}"


# The registry dictionary for chat stickers.
ChatStickerRegistry: Dict[IntEnum, ChatStickerDefinition] = {
    ### Default ###
    ChatStickersItemType.DisgustGator: ChatStickerDefinition(
        name='Disgust Gator',
        description='Todo!',
        modelPath="**/disgust_gator",
        isDefault=True,
    ),
    ChatStickersItemType.ConcernedDog: ChatStickerDefinition(
        name='Concerned Dog',
        description='Todo!',
        modelPath="**/concerned_dog",
        isDefault=True,
    ),
    ChatStickersItemType.ConfusedKangaroo: ChatStickerDefinition(
        name='Confused Kangaroo',
        description='Todo!',
        modelPath="**/confused_kangaroo",
        isDefault=True,
    ),
    ChatStickersItemType.CryCat: ChatStickerDefinition(
        name='Cry Cat',
        description='Todo!',
        modelPath="**/cry_cat",
        isDefault=True,
    ),
    ChatStickersItemType.GriefKiwi: ChatStickerDefinition(
        name='Grief Kiwi',
        description='Todo!',
        modelPath="**/grief_kiwi",
        isDefault=True,
    ),
    ChatStickersItemType.BlushBat: ChatStickerDefinition(
        name='Blush Bat',
        description='Todo!',
        modelPath="**/blush_bat",
        isDefault=True,
    ),
    ChatStickersItemType.GrinDuck: ChatStickerDefinition(
        name='Grin Duck',
        description='Todo!',
        modelPath="**/grin_duck",
        isDefault=True,
    ),
    ChatStickersItemType.HeartRabbit: ChatStickerDefinition(
        name='Heart Rabbit',
        description='Todo!',
        modelPath="**/heart_rabbit",
        isDefault=True,
    ),
    ChatStickersItemType.GreenedCat: ChatStickerDefinition(
        name='Greened Cat',
        description='Todo!',
        modelPath="**/greened_cat",
        isDefault=True,
    ),
    ChatStickersItemType.PensiveFox: ChatStickerDefinition(
        name='Pensive Fox',
        description='Todo!',
        modelPath="**/pensive_fox",
        isDefault=True,
    ),
    ChatStickersItemType.PleadingDog: ChatStickerDefinition(
        name='Pleading Dog',
        description='Todo!',
        modelPath="**/pleading_dog",
        isDefault=True,
    ),
    ChatStickersItemType.SadBat: ChatStickerDefinition(
        name='Sad Bat',
        description='Todo!',
        modelPath="**/sad_bat",
        isDefault=True,
    ),
    ChatStickersItemType.SurprisedArmadillo: ChatStickerDefinition(
        name='Surprised Armadillo',
        description='Todo!',
        modelPath="**/surprised_armadillo",
        isDefault=True,
    ),
    ChatStickersItemType.SurprisedRaccoon: ChatStickerDefinition(
        name='Surprised Raccoon',
        description='Todo!',
        modelPath="**/surprised_raccoon",
        isDefault=True,
    ),
    ChatStickersItemType.SusBeaver: ChatStickerDefinition(
        name='Suspicious Beaver',
        description='Todo!',
        modelPath="**/sus_beaver",
        isDefault=True,
    ),
    ChatStickersItemType.WinkDeer: ChatStickerDefinition(
        name='Wink Deer',
        description='Todo!',
        modelPath="**/wink_deer",
        isDefault=True,
    ),

    ### Regional Managers ###
    ChatStickersItemType.Bellringer: ChatStickerDefinition(
        name='Bellringer',
        rarity=Rarity.Rare,
        description='Todo!',
        modelPath="**/bellringer",
        isSuit=True,
    ),
    ChatStickersItemType.ChainsawConsultant: ChatStickerDefinition(
        name='Chainsaw Consultant',
        rarity=Rarity.Rare,
        description='Todo!',
        modelPath="**/chainsaw_consultant",
        isSuit=True,
    ),
    ChatStickersItemType.DeepDiver: ChatStickerDefinition(
        name='Deep Diver',
        rarity=Rarity.Rare,
        description='Todo!',
        modelPath="**/deep_diver",
        isSuit=True,
    ),
    ChatStickersItemType.DuckShuffler: ChatStickerDefinition(
        name='Duck Shuffler',
        rarity=Rarity.Rare,
        description='Todo!',
        modelPath="**/duck_shuffler",
        isSuit=True,
    ),
    ChatStickersItemType.Featherbedder: ChatStickerDefinition(
        name='Featherbedder',
        rarity=Rarity.Rare,
        description='Todo!',
        modelPath="**/featherbedder",
        isSuit=True,
    ),
    ChatStickersItemType.Firestarter: ChatStickerDefinition(
        name='Firestarter',
        rarity=Rarity.Rare,
        description='Todo!',
        modelPath="**/firestarter",
        isSuit=True,
    ),
    ChatStickersItemType.Gatekeeper: ChatStickerDefinition(
        name='Gatekeeper',
        rarity=Rarity.Rare,
        description='Todo!',
        modelPath="**/gatekeeper",
        isSuit=True,
    ),
    ChatStickersItemType.MajorPlayer: ChatStickerDefinition(
        name='Major Player',
        rarity=Rarity.Rare,
        description='Todo!',
        modelPath="**/major_player",
        isSuit=True,
    ),
    ChatStickersItemType.Mouthpiece: ChatStickerDefinition(
        name='Mouthpiece',
        rarity=Rarity.Rare,
        description='Todo!',
        modelPath="**/mouthpiece",
        isSuit=True,
    ),
    ChatStickersItemType.Multislacker: ChatStickerDefinition(
        name='Multislacker',
        rarity=Rarity.Rare,
        description='Todo!',
        modelPath="**/multislacker",
        isSuit=True,
    ),
    ChatStickersItemType.Pacesetter: ChatStickerDefinition(
        name='Pacesetter',
        rarity=Rarity.Rare,
        description='Todo!',
        modelPath="**/pacesetter",
        isSuit=True,
    ),
    ChatStickersItemType.Plutocrat: ChatStickerDefinition(
        name='Plutocrat',
        rarity=Rarity.Rare,
        description='Todo!',
        modelPath="**/plutocrat",
        isSuit=True,
    ),
    ChatStickersItemType.Prethinker: ChatStickerDefinition(
        name='Prethinker',
        rarity=Rarity.Rare,
        description='Todo!',
        modelPath="**/prethinker",
        isSuit=True,
    ),
    ChatStickersItemType.Rainmaker: ChatStickerDefinition(
        name='Rainmaker',
        rarity=Rarity.Rare,
        description='Todo!',
        modelPath="**/rainmaker",
        isSuit=True,
    ),
    ChatStickersItemType.Treekiller: ChatStickerDefinition(
        name='Treekiller',
        rarity=Rarity.Rare,
        description='Todo!',
        modelPath="**/treekiller",
        isSuit=True,
    ),
    ChatStickersItemType.WitchHunter: ChatStickerDefinition(
        name='Witch Hunter',
        rarity=Rarity.Rare,
        description='Todo!',
        modelPath="**/witch_hunter",
        isSuit=True,
    ),

    # April Toons 2023 Stickers
    ChatStickersItemType.SellbotEmblem: ChatStickerDefinition(
        name='Sellbot Emblem',
        description='Todo!',
        modelPath="**/insignia_sellbot",
        isSuit=True,
        stickerMenuAlphabeticalName='Cog Emblem A',
        stickerScale3d=0.90625,
    ),
    ChatStickersItemType.CashbotEmblem: ChatStickerDefinition(
        name='Cashbot Emblem',
        description='Todo!',
        modelPath="**/insignia_cashbot",
        isSuit=True,
        stickerMenuAlphabeticalName='Cog Emblem B',
        stickerScale3d=0.90625,
    ),
    ChatStickersItemType.LawbotEmblem: ChatStickerDefinition(
        name='Lawbot Emblem',
        description='Todo!',
        modelPath="**/insignia_lawbot",
        isSuit=True,
        stickerMenuAlphabeticalName='Cog Emblem C',
        stickerScale3d=0.90625,
    ),
    ChatStickersItemType.BossbotEmblem: ChatStickerDefinition(
        name='Bossbot Emblem',
        description='Todo!',
        modelPath="**/insignia_bossbot",
        isSuit=True,
        stickerMenuAlphabeticalName='Cog Emblem D',
        stickerScale3d=0.90625,
    ),
    ChatStickersItemType.BoardbotEmblem: ChatStickerDefinition(
        name='Boardbot Emblem',
        description='Todo!',
        modelPath="**/insignia_boardbot",
        isSuit=True,
        stickerMenuAlphabeticalName='Cog Emblem E',
        stickerScale3d=0.90625,
    ),

    ChatStickersItemType.DiceRoll: DiceRollStickerItemDefinition(
        name='Dice Roll',
        description='Todo!',
        rarity=Rarity.Rare,
        modelPath="**/dice_base",
        stickerSound="phase_3.5/audio/sfx/tt_s_sfx_sticker_dice.ogg",
        customSequence=DiceStickerSequence,
        stickerScale3d=0.9375,
        stickerScale2d=0.88,
    ),

    ChatStickersItemType.HighRoller: ChatStickerDefinition(
        name='High Roller',
        description='Todo!',
        rarity=Rarity.Rare,
        modelPath="**/high_roller",
        isSuit=True,
    ),
    ChatStickersItemType.FrustratedForeman: ChatStickerDefinition(
        name='Frustrated Foreman',
        description='Todo!',
        rarity=Rarity.Rare,
        modelPath="**/frustrated_foreman",
        isSuit=True,
    ),

    ChatStickersItemType.Litigator: ChatStickerDefinition(
        name='Litigator',
        description='Todo!',
        rarity=Rarity.Rare,
        modelPath="**/litigator",
        isSuit=True,
    ),
    ChatStickersItemType.Stenographer: ChatStickerDefinition(
        name='Case Manager',
        description='Todo!',
        rarity=Rarity.Rare,
        modelPath="**/stenographer",
        isSuit=True,
    ),
    ChatStickersItemType.CaseManager: ChatStickerDefinition(
        name='Case Manager',
        description='Todo!',
        rarity=Rarity.Rare,
        modelPath="**/case_manager",
        isSuit=True,
        stickerScale3d=(1.0, 1.0, (406/676)),
        stickerScale2d=(1.0, 1.0, (406/676)),
    ),
    ChatStickersItemType.Scapegoat: ChatStickerDefinition(
        name='Scapegoat',
        description='Todo!',
        rarity=Rarity.Rare,
        modelPath="**/scapegoat",
        isSuit=True,
    ),
}
