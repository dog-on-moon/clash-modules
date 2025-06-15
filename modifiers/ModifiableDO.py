from abc import ABC
from typing import List

from toontown.modifiers.ModifiableDOBase import ModifiableDOBase
from toontown.modifiers.Modifier import Modifier


class ModifiableDO(ModifiableDOBase, ABC):
    """
    The client-sided representation of the ModifiableDO.
    """

    def setRawModifiers(self, rawModifiers: List[list]) -> None:
        """
        Setter for raw modifiers.
        We take in the raw modifiers that we get, and set them to our REAL modifiers accordingly.
        """
        modifiers = self.getAllModifiers()
        for modifier in modifiers[:]:
            self.removeModifier(modifier)
        for modifier in Modifier.fromStructList(rawModifiers):
            self.addModifier(modifier)

    def addModifier(self, modifier: Modifier):
        modifier.onModifierPreAdd(self)
        super().addModifier(modifier)
        modifier.onModifierPostAdd(self)

    def removeModifier(self, modifier: Modifier):
        modifier.onModifierPreRemove(self)
        super().removeModifier(modifier)
        modifier.onModifierPostRemove(self)
