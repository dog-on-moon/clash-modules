from typing import Any, Optional
from math import ceil

from toontown.modifiers.Modifier import Modifier

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from toontown.toon.DistributedToonAI import DistributedToonAI


class LaffAdaptiveModifier(Modifier):
    """
    This class sets toons' laff to a strict, forced amount over the course of a fight.
    Used in High Roller battle to update laff.
    """

    def __init__(self, laffCap: int = 15):
        super().__init__([laffCap])

    def modify(self, value: Any, do, context: Optional[int] = None) -> Any:
        # All we really want to do is make sure whatever the laff cap is gets adjusted this round.
        return self.getLaffCap()

    def getLaffCap(self) -> int:
        return self.arguments[0]

    """
    Handle server-sided application
    """

    def onModifierPreAddAI(self, do) -> None:
        """
        When we apply this modifier, we just kinda max the toon's current HP to make things easy on them.
        :type do: DistributedToonAI
        """
        if do.hp <= 0:
            return

        newMaxHp = self.modify(value=do.maxHp, do=do)
        do.b_setHp(newMaxHp)

    def onModifierPreRemoveAI(self, do) -> None:
        """
        When we remove the modifier, we just kinda max the current toon's HP to make things easy on them.
        :type do: DistributedToonAI
        """
        if do.hp <= 0:
            return

        do.b_setHp(do.maxHp)

    def updateLaffCap(self, do, newLaffCap) -> None:
        """
        Let's add onto the player's max health and current health.
        """

        # Let's determine how much laff we added on this turn.
        laffDiff = newLaffCap - self.getLaffCap()

        # Set the toon's laff to the new cap.
        self.arguments[0] = newLaffCap
        do._sendUpdateMessage(self)
        do._updateRawModifiers()

        # Let's add the same amount onto their current laff.
        newCurrentHp = do.hp + laffDiff
        do.b_setHp(newCurrentHp)


