import time
from enum import IntEnum
from direct.interval.IntervalGlobal import *
from typing import Union

from toontown.cutscene.CutsceneSequenceHelpers import NodePathWithState
from toontown.utils import ColorHelper


class ItemModifier(IntEnum):
    """
    An enum list for the types of item sequences
    """
    STICKER_FOIL = 1


def getVisualSequence(itemVisualSequence: ItemModifier, model: NodePathWithState) -> Union[Sequence, Parallel]:
    """
    Returns a visual sequence to be applied onto item models.
    """
    if itemVisualSequence == ItemModifier.STICKER_FOIL:
        return Sequence()
