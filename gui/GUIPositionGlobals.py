"""
Globals file (enums, etc) for how to position GUI.
"""
from direct.interval.IntervalGlobal import *
from enum import IntEnum, auto

MSG_UPDATE_POSITION_MANAGER = 'msg-update-position-manager'


class ScreenCorner(IntEnum):
    TOP_LEFT = auto()
    TOP_RIGHT = auto()
    BOTTOM_LEFT = auto()
    BOTTOM_RIGHT = auto()

    # Only used in certain contexts
    TOP_MIDDLE = auto()
    BOTTOM_MIDDLE = auto()
    LEFT_MIDDLE = auto()
    RIGHT_MIDDLE = auto()

    def getOppositeCorner(self) -> 'ScreenCorner':
        return {
            self.TOP_LEFT:      self.BOTTOM_RIGHT,
            self.TOP_RIGHT:     self.BOTTOM_LEFT,
            self.BOTTOM_LEFT:   self.TOP_RIGHT,
            self.BOTTOM_RIGHT:  self.TOP_LEFT,
            self.TOP_MIDDLE:    self.BOTTOM_MIDDLE,
            self.BOTTOM_MIDDLE: self.TOP_MIDDLE,
            self.LEFT_MIDDLE:   self.RIGHT_MIDDLE,
            self.RIGHT_MIDDLE:  self.LEFT_MIDDLE,
        }.get(self)


class ManagedGUIEnterSequence:
    """
    A collection of callables for GUI enter sequences.
    """

    @classmethod
    def instant(cls, gui, args: list = None):
        return Sequence(
            Func(gui.getGuiElement().setPos, gui.getPosOffset()),
        )

    @classmethod
    def enterRight(cls, gui, args: list = None):
        duration, dist = args
        return Sequence(
            LerpPosInterval(gui, duration, gui.getPosOffset(),
                            startPos=Vec3(dist, 0, 0) + gui.getPosOffset(), blendType='easeIn'),
        )


class ManagedGUIExitSequence:
    """
    A collection of callables for GUI exit sequences.
    """

    @classmethod
    def instant(cls, gui, args: list = None):
        return Sequence()

    @classmethod
    def leaveRight(cls, gui, args: list = None):
        duration, dist = args
        return Sequence(
            LerpPosInterval(gui, duration, (dist, 0, 0), blendType='easeIn'),
        )

    @classmethod
    def instantDelayed(cls, gui, args: list = None):
        time, *_ = args
        return Sequence(Wait(time))
