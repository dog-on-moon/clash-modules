from panda3d.core import LVecBase3f

from toontown.gui.Bounds import Bounds
from toontown.gui.GUIPositionGlobals import ScreenCorner
from toontown.gui.TTGui import kwargsToOptionDefs
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from direct.gui.DirectGui import *

from typing import Tuple


@DirectNotifyCategory()
class EasyManagedItem(DirectFrame, Bounds):
    """
    An item with positional management getters for the EasyScrolledFrame.
    Due to the convenience of these getters, they can be used in all kinds
    of UI utilities for very easy positional management.

    Intended to be subclassed.

    EasyManagedItems are based on the top-left of the EasyScrolledFrame.
    """

    def __init__(self, parent=aspect2d, **kw):
        optiondefs = kwargsToOptionDefs(
            pos=(0, 0, 0),
            scale=1.0,

            # The height and width of the item in the EasyScrolledFrame.
            easyHeight=[0.0, self.easyUpdate],  # Since it's built from the top left, you want this to be negative (down=negative).
            easyWidth=[0.0, self.easyUpdate],

            # Any padding on the sides of the item.
            easyPadLeft=[0.0, self.easyUpdate],
            easyPadRight=[0.0, self.easyUpdate],
            easyPadDown=[0.0, self.easyUpdate],
            easyPadUp=[0.0, self.easyUpdate],

            # The "x-max" of the item in the EasyScrolledFrame.
            # This refers to how many of this item can be put
            # into the same y-position by adding additional ESIs
            # to the right of other ESIs.
            # Turning this up is useful for creating scrolls where
            # a grid is involved.
            # easyItemCount also determines the amount of "items"
            # this item counts as in the horizontal space.
            easyXMax=[1.0, self.easyUpdate],
            easyItemCount=[1.0, self.easyUpdate],

            # The offset of the frame's position when it gets managed.
            posOffset = [(0, 0, 0), self.updateOffset],

            # Define an EasyScrolledFrame to attach to automatically.
            easyScrolledFrame=[None, self.attachFrame],
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.postInitialized = False
        self.postInitialiseFuncList.append(lambda: setattr(self, 'postInitialized', True))
        self.initialiseoptions(EasyManagedItem)

        # Sync with EasyManagedButton's init
        self.oldOffset = self.cget('posOffset')
        self._active = True

    """
    Attribute funnies
    """

    def attachFrame(self):
        easyScrolledFrame = self['easyScrolledFrame']
        if easyScrolledFrame:
            easyScrolledFrame.addItem(self)

    def updateOffset(self):
        easyScrolledFrame = self['easyScrolledFrame']
        if easyScrolledFrame:
            easyScrolledFrame.updateItemPositions()
        self.easyUpdate()

    def enableDebug(self):
        scale = self.getScale()
        if type(scale) not in (int, float):
            xscale, _, zscale = scale
        else:
            xscale, zscale = scale, scale
        left = (self.getEasyPadLeft() - (self.getEasyWidth() / 2)) / xscale
        right = (self.getEasyPadRight() + (self.getEasyWidth() / 2)) / xscale
        down = (self.getEasyPadDown() + (self.getEasyHeight() / 2)) / zscale
        up = (self.getEasyPadUp() - (self.getEasyHeight() / 2)) / zscale
        self['frameSize'] = (left, right, down, up)
        import random
        self['frameColor'] = (random.random(), random.random(), random.random(), 0.5)
        self['relief'] = DGG.FLAT

    """
    Important things to override
    """

    def bindToScroll(self, easyScrolledFrame):
        easyScrolledFrame.bindToScroll(self)

    def easyUpdate(self):
        """
        This method is called whenever any of the GUI's easy parameters get modified.
        """
        pass

    """
    Getters
    """

    def getEasyHeight(self) -> float:
        return self['easyHeight']

    def getEasyWidth(self) -> float:
        return self['easyWidth']

    def getEasyPad(self) -> list:
        return [self.getEasyPadLeft(), self.getEasyPadRight(),
                self.getEasyPadDown(), self.getEasyPadUp()]

    def getEasyPadLeft(self) -> float:
        return self['easyPadLeft']

    def getEasyPadRight(self) -> float:
        return self['easyPadRight']

    def getEasyPadDown(self) -> float:
        return self['easyPadDown']

    def getEasyPadUp(self) -> float:
        return self['easyPadUp']

    def getEasyXMax(self) -> float:
        return self['easyXMax']

    def getEasyItemCount(self) -> float:
        return self['easyItemCount']

    def getFloatScale(self) -> float:
        """Returns scale as a float, even when it's cringe."""
        scale = self.getScale()
        if isinstance(scale, LVecBase3f):
            return scale[0]
        return scale

    """
    Complex getters
    """

    def getCornerPos(self, screenCorner: ScreenCorner = None) -> Tuple[float, float]:
        return {
            ScreenCorner.TOP_LEFT:      self.getTopLeft,
            ScreenCorner.TOP_RIGHT:     self.getTopRight,
            ScreenCorner.BOTTOM_LEFT:   self.getBottomLeft,
            ScreenCorner.BOTTOM_RIGHT:  self.getBottomRight,
        }.get(screenCorner, self.getCenter)()

    def getCenter(self) -> Tuple[float, float]:
        return 0.0, 0.0

    def getTopLeft(self) -> Tuple[float, float]:
        return self.getEasyPadLeft() - (self.getEasyWidth() / 2), self.getEasyPadUp() - (self.getEasyHeight() / 2)

    def getTopRight(self) -> Tuple[float, float]:
        return self.getEasyPadRight() + (self.getEasyWidth() / 2), self.getEasyPadUp() - (self.getEasyHeight() / 2)

    def getBottomLeft(self) -> Tuple[float, float]:
        return self.getEasyPadLeft() - (self.getEasyWidth() / 2), self.getEasyPadDown() + (self.getEasyHeight() / 2)

    def getBottomRight(self) -> Tuple[float, float]:
        return self.getEasyPadRight() + (self.getEasyWidth() / 2), self.getEasyPadDown() + (self.getEasyHeight() / 2)

    """
    Active
    """

    def setActivePositioning(self, mode: bool):
        """
        Sets the active positioning mode of the EMI.
        If it is inactive, then it will be ignored when positioning.
        Other factors (such as hiding the EMI) should be handled externally.
        """
        self._active = mode

    def isActivelyPositioned(self) -> bool:
        return self._active
