from abc import ABC
from typing import Tuple

from toontown.modifiers.ModifiableDOBase import ModifiableDOBase
from toontown.modifiers.ModifierEnums import ModifierType
from toontown.modifiers.Modifier import Modifier


class ModifiableDOAI(ModifiableDOBase, ABC):
    """
    The AI representation of the ModifiableDO.
    We overwrite the basic add/remove methods to ensure raw modifiers get updated.
    """

    def cleanup(self):
        """
        Call this as the object is deleting to clear all modifiers.
        """
        self.removeAllModifiers()
        self._updateRawModifiers()

    def addModifier(self, modifier: Modifier, update: bool = True):
        modifier.onModifierPreAddAI(self)
        super().addModifier(modifier=modifier)
        modifier.onModifierPostAddAI(self)
        if update:
            self._updateRawModifiers()

    def removeModifier(self, modifier: Modifier, update: bool = True):
        modifier.onModifierPreRemoveAI(self)
        super().removeModifier(modifier=modifier)
        modifier.onModifierPostRemoveAI(self)
        if update:
            self._updateRawModifiers()

    def removeModifierOfType(self, *modifierTypes: Tuple[ModifierType], negate: bool = False, update: bool = True):
        # If you change the below code, you may want to change it in ModifiableDOBase.py as well.
        for modifier in self.getAllModifiers()[:]:
            if not negate:
                # We are filtering FOR the modifier types.
                if modifier.getModifierType() in modifierTypes:
                    self.removeModifier(modifier, update=False)
            else:
                # We are filtering AGAINST the modifier types.
                if modifier.getModifierType() not in modifierTypes:
                    self.removeModifier(modifier, update=False)
        if update:
            self._updateRawModifiers()

    """
    Astron
    """

    def _updateRawModifiers(self) -> None:
        """
        This method updates the raw modifiers to be communicated to the client.
        """
        rawModifiers = Modifier.toStructList(self.getAllModifiers())
        if rawModifiers is not None:
            self.sendUpdate(
                fieldName='setRawModifiers',
                args=[rawModifiers],
            )
