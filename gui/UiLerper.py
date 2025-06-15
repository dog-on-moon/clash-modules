from typing import Any

from direct.gui.DirectGuiBase import DirectGuiWidget
from direct.interval.IntervalGlobal import *

from toontown.utils import ColorHelper
from enum import Enum, auto


class UILerper:
    """
    A helper singleton designed to provide simple means
    for lerping different GUI properties.
    """

    class LerpMode(Enum):
        COLOR = auto()

    """
    Interface
    """

    @staticmethod
    def lerpOption(
        gui: DirectGuiWidget,
        option: str,
        end: Any,
        start: Any | None = None,
        duration: float = 1.0,
        blendType: str = 'easeOut',
        instant: bool = False,
        lerpMode: LerpMode | None = None,
    ):
        """
        Lerps an option on a UI element.
        :param gui:       The target element.
        :param option:    The option to configure.
        :param end:       The end value.
        :param start:     An optional starting value.
        :param duration:  The length of the lerp.
        :param blendType: The blend type of the lerp.
        :param instant:   Run it instantly?
        :param lerpMode:  Influences the way the value is lerped.
        """
        # Do nothing if GUI is rotten.
        if not gui:
            return

        # Is this goal already active? If so, don't lerp.
        if UILerper.isLerpActive(gui, option, end):
            return

        # Is this GUI already at the target? If so, also don't lerp
        if gui[option] == end:
            return

        # If we are at this point, clean up any existing seqs
        UILerper.cleanupLerp(gui, option)

        # If instant, just do it lol
        if instant:
            gui[option] = end
            return

        # Create the sequence here, and play it
        if start is None:
            start = gui[option]
        seq = Sequence(
            Func(UILerper._startLerp, gui, option, end),
            LerpFunctionInterval(
                UILerper._lerp, duration=duration, blendType=blendType,
                extraArgs=[(gui, option, end, start, lerpMode)],
            ),
            Func(UILerper._endLerp, gui, option, end),
        )
        seq.start()

        # Stash it for good luck
        UILerper.storeLerp(seq, gui, option, end)

    """
    Internal state
    """

    ACTIVE_IVALS: dict[DirectGuiWidget, set[tuple[Sequence, str, Any]]] = {}

    @staticmethod
    def isLerpActive(
        gui: DirectGuiWidget, option: str, end: Any,
    ) -> bool:
        # Initial barriers.
        if not gui:
            return False
        if gui not in UILerper.ACTIVE_IVALS:
            return False

        # OK, pull stored information.
        infoSet: set[tuple[Sequence, str, Any]] = UILerper.ACTIVE_IVALS.get(gui)
        for infoTuple in infoSet:
            activeSeq, activeOption, activeEnd = infoTuple
            if activeOption == option and activeEnd == end:
                # This lerp is ongoing and active.
                return True

        # Could not find active sequence.
        return False

    @staticmethod
    def cleanupLerp(
        gui: DirectGuiWidget, option: str,
    ) -> bool:
        # Initial barriers.
        if not gui:
            return False
        if gui not in UILerper.ACTIVE_IVALS:
            return False

        # OK, pull stored information.
        infoSet: set[tuple[Sequence, str, Any]] = UILerper.ACTIVE_IVALS.get(gui)
        for infoTuple in infoSet.copy():
            activeSeq, activeOption, activeEnd = infoTuple
            if activeOption == option:
                # Yeah, this is the lerp for us to kill.
                activeSeq.pause()
                UILerper.ACTIVE_IVALS[gui].remove(infoTuple)
                if not UILerper.ACTIVE_IVALS[gui]:
                    del UILerper.ACTIVE_IVALS[gui]
                return True

        # Could not find active sequence.
        return False

    @staticmethod
    def storeLerp(
        seq: Sequence, gui: DirectGuiWidget, option: str, end: Any,
    ) -> None:
        UILerper.ACTIVE_IVALS.setdefault(gui, set())
        UILerper.ACTIVE_IVALS[gui].add((seq, option, end))

    """
    Lerp Logic
    """

    @staticmethod
    def _lerp(t: float, args: tuple):
        # Unpack args.
        gui, option, end, start, lerpMode = args

        # Cleanup if need be.
        if not gui:
            UILerper.cleanupLerp(gui, option)
            return

        # Any lerp mode overrides?
        if lerpMode == UILerper.LerpMode.COLOR:
            gui[option] = ColorHelper.lerpPColSmart(start, end, t)

        # Otherwise, lerp based on type.
        elif isinstance(end, (int, float)):
            gui[option] = lerp(start, end, t)
        elif isinstance(end, (tuple, list)):
            gui[option] = ColorHelper.lerpColor(start, end, t)
        else:
            raise KeyError

    @staticmethod
    def _startLerp(gui: DirectGuiWidget, option: str, end: Any):
        pass

    @staticmethod
    def _endLerp(gui: DirectGuiWidget, option: str, end: Any):
        UILerper.cleanupLerp(gui, option)
