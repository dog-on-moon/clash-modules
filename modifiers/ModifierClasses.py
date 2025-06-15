"""
This module defines all of the classes per modifier type.
"""
from toontown.modifiers.ModifierEnums import ModifierType
from toontown.modifiers.classes.LaffAdaptiveModifier import LaffAdaptiveModifier
from toontown.modifiers.classes.LaffMultiplierModifier import LaffMultiplierModifier
from toontown.modifiers.classes.LaffContentSyncModifier import LaffContentSyncModifier
from toontown.modifiers.classes.GagsContentSyncModifier import GagsContentSyncModifier
from toontown.modifiers.classes.RewardModifier import RewardModifier
from toontown.modifiers.classes.RewardContentSyncModifier import RewardContentSyncModifier

# A mapping of all modifier types to modifier classes.
ModifierClasses = {
    ModifierType.LaffMultiplier:    LaffMultiplierModifier,
    ModifierType.LaffAdaptive:      LaffAdaptiveModifier,
    ModifierType.LaffContentSync:   LaffContentSyncModifier,
    ModifierType.GagsContentSync:   GagsContentSyncModifier,
    ModifierType.RewardModifier:    RewardModifier,
    ModifierType.RewardContentSync: RewardContentSyncModifier,
}

# All "content sync" modifiers.
ContentSyncModifiers = {
    ModifierType.LaffContentSync,
    ModifierType.GagsContentSync,
    ModifierType.RewardContentSync,
}
