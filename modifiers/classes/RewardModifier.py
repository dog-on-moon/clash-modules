from typing import Any, Optional
from toontown.modifiers.Modifier import Modifier


class RewardModifier(Modifier):

    def __init__(self,
                 iousAllowed: bool = True,
                 unitesAllowed: bool = True,
                 counterfeitsAllowed: bool = True,
                 cndsAllowed: bool = True,
                 slipsAllowed: bool = True):
        super().__init__([int(iousAllowed), int(unitesAllowed), int(counterfeitsAllowed), int(cndsAllowed), int(slipsAllowed)])

    def modify(self, value: Any, do, context: Optional[int] = None) -> Any:
        # There's nothing to modify -- this modifier exists solely for setting reward flags.
        pass

    def canUseIOUs(self) -> bool:
        return bool(self.arguments[0])

    def canUseUnites(self) -> bool:
        return bool(self.arguments[1])

    def canUseCounterfeits(self) -> bool:
        return bool(self.arguments[2])

    def canUseCNDs(self) -> bool:
        return bool(self.arguments[3])

    def canUseSlips(self) -> bool:
        return bool(self.arguments[4])
