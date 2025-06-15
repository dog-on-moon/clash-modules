from typing import Any, Optional
from math import ceil

from toontown.modifiers.Modifier import Modifier

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from toontown.toon.DistributedToonAI import DistributedToonAI


class LaffMultiplierModifier(Modifier):

    def __init__(self, multiplier: float = 1.0):
        super().__init__([int(multiplier * 100)])

    def modify(self, value: Any, do, context: Optional[int] = None) -> Any:
        # Return the laff simply multiplied by the multiplier
        return int(value * self.getMultiplier())

    def getMultiplier(self) -> float:
        return float(self.arguments[0] / 100)

    """
    Handle server-sided application
    """

    def onModifierPreAddAI(self, do) -> None:
        """
        When we apply this modifier, we match the av's HP ratio to what they'll have in the instance.
        :type do: DistributedToonAI
        """
        if do.hp <= 0:
            return

        # Calculate some values.
        hpRatio = do.hp / do.maxHp
        newMaxHp = self.modify(value=do.maxHp, do=do)

        # Set their HP to be equivalent to the old ratio of HP they had
        newHp = max(1, round(hpRatio * newMaxHp))
        do.b_setHp(newHp)

    def onModifierPreRemoveAI(self, do) -> None:
        """
        When we remove the modifier, we match their HP to what they had in the instance.
        :type do: DistributedToonAI
        """
        if do.hp <= 0:
            return

        # Calculate some values.
        hpRatio = do.getHp() / do.getMaxHp()
        trueMaxHp = do.maxHp

        # Calculate and apply the new HP.
        newHp = max(1, min(round(hpRatio * trueMaxHp), trueMaxHp))
        do.b_setHp(newHp)
