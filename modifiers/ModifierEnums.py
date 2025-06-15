from enum import IntEnum, auto


class ModifierType(IntEnum):
    """
    Designates the type of modifier that is being applied.
    """
    LaffContentSync   = auto()
    GagsContentSync   = auto()
    RewardModifier    = auto()
    RewardContentSync = auto()
    LaffMultiplier    = auto()
    LaffAdaptive      = auto()


"""
Modifier Presets
"""

HP_MODIFIERS = {ModifierType.LaffContentSync, ModifierType.LaffMultiplier, ModifierType.LaffAdaptive}
REWARD_MODIFIERS = {ModifierType.RewardModifier, ModifierType.RewardContentSync}
