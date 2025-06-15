from abc import ABC, abstractmethod
from typing import Tuple, List, Any, Optional

from toontown.modifiers.ModifierEnums import ModifierType
from toontown.modifiers.Modifier import Modifier


class ModifiableDOBase(ABC):
    """
    A ModifiableDO is a way to implement a "modifier" system over a DistributedObject.
    Modifiers are distributable, so that the client and server can recognize it.

    Modifiers can be used to wrap the "getter" of a method of a class, to make changes
    to the intended output. Modifiers can stack with modifiers of the same type.

    Modifiers are similar to Boosters, but are designed to be managed much more frequently,
    with no expiry date nor should they be databased on a Toon in any capacity.

    Ensure that the dclass for this object also inherits the protocols of ModifiableDO in toon.dc.
    """

    def applyModifiers(self, *modifierTypes: ModifierType, value: Any = None, context: Optional[int] = None) -> Any:
        """
        Modifies a value by using different modifiers.

        :param modifierTypes: The types of modifier that should transform the value.
        :param value:         The value to be transformed.
        :param context:       The context for the modifiers to respond to.
        """
        # Modify the value.
        for modifier in self.getModifiersOfType(*modifierTypes, negate=False):
            value = modifier.modify(value=value, do=self, context=context)

        # Return the modified value.
        return value

    """
    Abstract Methods
    """

    @abstractmethod
    def getAllModifiers(self) -> List[Modifier]:
        """
        Gets a list of all modifiers of the ModifiableDO.
        This list must be mutable.
        """
        raise NotImplementedError

    """
    Setters
    """

    def addModifier(self, modifier: Modifier):
        """
        Adds a modifier to the ModifiableDO.

        :param modifier: The modifier to add.
        """
        self.getAllModifiers().append(modifier)
        self._sendUpdateMessage(modifier)

    def removeModifier(self, modifier: Modifier):
        """
        Removes a modifier to the ModifiableDO.

        :param modifier: The modifier to remove.
        """
        modifiers = self.getAllModifiers()
        if modifier in modifiers:
            modifiers.remove(modifier)
            self._sendUpdateMessage(modifier)

    def removeModifierOfType(self, *modifierTypes: Tuple[ModifierType], negate: bool = False):
        """
        Removes a modifier to the ModifiableDO.

        :param modifierTypes: All modifier types to look out for.
        :param negate:        Whether to return everything BUT the specified modifiers.
        """
        # If you change the below code, you may want to change it in ModifiableDOAI.py as well.
        for modifier in self.getAllModifiers()[:]:
            if not negate:
                # We are filtering FOR the modifier types.
                if modifier.getModifierType() in modifierTypes:
                    self.removeModifier(modifier)
            else:
                # We are filtering AGAINST the modifier types.
                if modifier.getModifierType() not in modifierTypes:
                    self.removeModifier(modifier)

    def removeAllModifiers(self):
        """
        Removes all modifiers.
        """
        for modifier in self.getAllModifiers()[:]:
            self.removeModifier(modifier)

    """
    Getters
    """

    def getModifiersOfType(self, *modifierTypes: ModifierType, negate: bool = False) -> List[Modifier]:
        """
        Returns a list of all modifiers of a given type.

        :param modifierTypes: All modifier types to look out for.
        :param negate:        Whether to return everything BUT the specified modifiers.
        """
        if not negate:
            return [modifier for modifier in self.getAllModifiers() if modifier.getModifierType() in modifierTypes]
        else:
            return [modifier for modifier in self.getAllModifiers() if modifier.getModifierType() not in modifierTypes]

    def hasModifier(self, *modifierTypes: ModifierType) -> bool:
        """Simple getter for code clarity"""
        return bool(self.getModifiersOfType(*modifierTypes, negate=False))

    def getRawModifiers(self):
        """Required for Astron to be happy with me."""
        return []

    """
    Messaging
    """

    def hookCallbackToModifier(self, *modifierTypes: ModifierType, method: callable = None, extraArgs: list = None):
        """
        Hooks up a callback to a modifier type (or list of them).
        When a modifier gets added or removed from the object, the callbacks will be called.

        :param modifierTypes: All modifier types to hook up to a callback.
        :param method:        The method to be called upon modifier addition/removal.
        :param extraArgs:     Any arguments for the method.
        """
        if extraArgs is None:
            extraArgs = []
        assert method is not None, "A method must be specified in kwargs for this method."
        for modifierType in modifierTypes:
            message = self.getModifierMessage(modifierType)
            self.accept(message, method, extraArgs)

    def clearCallbackToModifier(self, *modifierTypes: ModifierType):
        """
        Clears all callbacks for listed modifiers.

        :param modifierTypes: All modifier types to hook off of a callback.
        """
        for modifierType in modifierTypes:
            message = self.getModifierMessage(modifierType)
            self.ignore(message)

    def _sendUpdateMessage(self, modifier: Modifier) -> None:
        """
        Sends a messenger message for updating this modifier.
        """
        messageName = self.getModifierMessage(modifierType=modifier.getModifierType())
        messenger.send(messageName)

    def getModifierMessage(self, modifierType: ModifierType) -> str:
        """
        Returns the update message for when a modifier of a type is added/removed from this ModifiableDO.
        """
        return f'{self.getDoId()}-update-{modifierType.name}'
