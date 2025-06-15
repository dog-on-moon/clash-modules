from typing import Any, Optional
from math import ceil

from toontown.modifiers.Modifier import Modifier

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from toontown.toon.DistributedToonAI import DistributedToonAI


class LaffContentSyncModifier(Modifier):

    def __init__(self, laffCap: int = 30, softness: float = 1.0, forceLaff: bool = False):
        super().__init__([laffCap, int(softness * 100), int(forceLaff)])

    def modify(self, value: Any, do, context: Optional[int] = None) -> Any:
        # Get the values.
        laffCap = self.getLaffCap()
        softness = self.getSoftness()

        # Is the laff cap being forced to a certain amount?
        if self.getForceLaff():
            return laffCap

        # If we're below the laff cap, do not transform the value.
        elif value <= laffCap:
            return value

        # Otherwise, we need to reduce it.
        else:
            # Take our health over the cap, and soften it.
            overheal = ceil((value - laffCap) ** softness)

            # Return our new laff with this overheal.
            return laffCap + overheal

    def getLaffCap(self) -> int:
        return self.arguments[0]

    def getSoftness(self) -> float:
        return self.arguments[1] / 100

    def getForceLaff(self) -> bool:
        return bool(self.arguments[2])

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

        # Calculate and apply the new HP.
        if not self.getForceLaff():
            newHp = max(1, round(hpRatio * newMaxHp))
            do.b_setHp(newHp)
        else:
            # The laff is being forced to this amount.
            # Just play it safe and make sure they have the laff.
            do.b_setHp(newMaxHp)

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
