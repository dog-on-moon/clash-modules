"""
This module contains the item data for emotes.
"""
from panda3d.core import NodePath, TextNode

from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.base.ItemDefinition import ItemDefinition
from typing import Dict, Optional
from enum import IntEnum

from toontown.inventory.enums.ItemEnums import EmoteItemType


class EmoteDefinition(ItemDefinition):
    """
    The definition structure for emotes.
    """

    def __init__(self,
                 whisperString,
                 **kwargs):
        super().__init__(**kwargs)
        self.whisperString = whisperString

    def getWhisperString(self):
        return self.whisperString

    def getItemTypeName(self):
        return 'Emote'

    def getRewardName(self, item: Optional[InventoryItem] = None):
        return f'{self.getName()} Emote'

    def getGuiItemModel(self, item: Optional[InventoryItem] = None, *args, **kwargs) -> NodePath:
        """
        Returns a nodepath that is to be used in 2D space.
        """
        return super().getGuiItemModel(item=item, useModel=self.renderTextForGuiModel(item), *args, **kwargs)


# The registry dictionary for emotes.
EmoteRegistry: Dict[IntEnum, EmoteDefinition] = {
    EmoteItemType.Wave: EmoteDefinition(
        name='Wave',
        description='Todo!',
        whisperString='%s waves.',
    ),
    EmoteItemType.Happy: EmoteDefinition(
        name='Happy',
        description='Todo!',
        whisperString='%s is happy.',
    ),
    EmoteItemType.Sad: EmoteDefinition(
        name='Sad',
        description='Todo!',
        whisperString='%s is sad.',
    ),
    EmoteItemType.Angry: EmoteDefinition(
        name='Angry',
        description='Todo!',
        whisperString='%s is angry.',
    ),
    EmoteItemType.Sleepy: EmoteDefinition(
        name='Sleepy',
        description='Todo!',
        whisperString='%s is sleepy.',
    ),
    EmoteItemType.Shrug: EmoteDefinition(
        name='Shrug',
        description='Todo!',
        whisperString='%s shrugs.',
    ),
    EmoteItemType.Dance: EmoteDefinition(
        name='Dance',
        description='Todo!',
        whisperString='%s dances.',
    ),
    EmoteItemType.Think: EmoteDefinition(
        name='Think',
        description='Todo!',
        whisperString='%s thinks.',
    ),
    EmoteItemType.Bored: EmoteDefinition(
        name='Bored',
        description='Todo!',
        whisperString='%s is bored.',
    ),
    EmoteItemType.Applause: EmoteDefinition(
        name='Applause',
        description='Todo!',
        whisperString='%s applauds.',
    ),
    EmoteItemType.Cringe: EmoteDefinition(
        name='Cringe',
        description='Todo!',
        whisperString='%s cringes.',
    ),
    EmoteItemType.Confused: EmoteDefinition(
        name='Confused',
        description='Todo!',
        whisperString='%s is confused.',
    ),
    EmoteItemType.BellyFlop: EmoteDefinition(
        name='Belly Flop',
        description='Todo!',
        whisperString='%s does a belly flop.',
    ),
    EmoteItemType.Bow: EmoteDefinition(
        name='Bow',
        description='Todo!',
        whisperString='%s bows to you.',
    ),
    EmoteItemType.BananaPeel: EmoteDefinition(
        name='Banana Peel',
        description='Todo!',
        whisperString='%s slips and slides on a banana peel.',
    ),
    EmoteItemType.ResistanceSalute: EmoteDefinition(
        name='Resistance Salute',
        description='Todo!',
        whisperString='%s gives the resistance salute.',
    ),
    EmoteItemType.LaughUNUSED: EmoteDefinition(
        name='Laugh',
        description='You should not see this.',
        whisperString='%s laughs',
    ),
    EmoteItemType.Yes: EmoteDefinition(
        name='Agree',
        description='Todo!',
        whisperString='%s nodes their head in agreement.',
    ),
    EmoteItemType.No: EmoteDefinition(
        name='Disagree',
        description='Todo!',
        whisperString='%s shakes their head in disagreement.',
    ),
    EmoteItemType.OK: EmoteDefinition(
        name='OK',
        description='You should not see this.',
        whisperString='%s says \'OK\'.',
    ),
    EmoteItemType.Surprise: EmoteDefinition(
        name='Surprise',
        description='Todo!',
        whisperString='%s is surprised.',
    ),
    EmoteItemType.Cry: EmoteDefinition(
        name='Cry',
        description='Todo!',
        whisperString='%s is crying.',
    ),
    EmoteItemType.Delighted: EmoteDefinition(
        name='Delighted',
        description='Todo!',
        whisperString='%s is delighted.',
    ),
    EmoteItemType.Furious: EmoteDefinition(
        name='Furious',
        description='Todo!',
        whisperString='%s is furious.',
    ),
    EmoteItemType.Laugh: EmoteDefinition(
        name='Laugh',
        description='Todo!',
        whisperString='%s is laughing.',
    ),
    EmoteItemType.Taunt: EmoteDefinition(
        name='Taunt',
        description='Todo!',
        whisperString='%s taunts you.',
    ),
    EmoteItemType.Yawn: EmoteDefinition(
        name='Yawn',
        description='Todo!',
        whisperString='%s yawns.',
    ),
    EmoteItemType.Shiver: EmoteDefinition(
        name='Shiver',
        description='Todo!',
        whisperString='%s shivers.',
    ),
}

AllEmotes = set(item for item in EmoteItemType)
