from typing import Tuple

from direct.task import Task

from toontown.gui.GUIPositionGlobals import ScreenCorner
from toontown.utils import ColorHelper

from panda3d.core import LVecBase3f


class Bounds:
    """
    A GUI class with a defined 'bounds' getter.
    Useful for getting flex info on a GUI element.
    """

    def getDefinedBounds(self) -> Tuple[float, float, float, float]:
        return self['frameSize']

    def getRenderPos(self) -> Tuple[float, float, float]:
        return self.getPos(aspect2d)

    def getRenderBounds(self) -> tuple:
        """Returns the bounds of the GUI relative to aspect2d."""
        x, _, z = self.getRenderPos()
        left, right, down, up = self.getDefinedBounds()
        return x + left, x + right, z + down, z + up

    def getBoundWidth(self) -> float:
        left, right, down, up = self.getDefinedBounds()
        return right - left

    def getBoundHeight(self) -> float:
        left, right, down, up = self.getDefinedBounds()
        return up - down

    def isMouseWithinBounds(self, padding: float = 0.0) -> bool:
        """Returns True if the mouse is within the bounds."""
        mwn = base.mouseWatcherNode
        if not mwn.hasMouse():
            return False

        # Get the screen mouse position. Adjust for aspect ratio.
        ar = base.getAspectRatio()
        xpos = mwn.getMouse()[0] * max(ar, 1)
        zpos = mwn.getMouse()[1] * min(ar, 1)

        # Get render bounds.
        left, right, down, up = self.getRenderBounds()
        left -= padding
        right += padding
        down -= padding
        up += padding
        if not (left <= xpos <= right):
            return False
        if not (down <= zpos <= up):
            return False

        # The mouse is within bounds.
        return True

    def makeHoverTask(self, callback: callable, taskName: str, padding: float = 0.0):
        """
        Creates a task to listen for this element being hovered.
        Performs callback(bool)
        """
        taskMgr.add(self.__hoverTask, taskName, extraArgs=[callback, padding])

    def __hoverTask(self, callback, padding: float):
        callback(self.isMouseWithinBounds(padding))
        Task.delayTime = 0.05
        return Task.again

    def removeHoverTask(self, taskName: str):
        taskMgr.remove(taskName)

    def getCornerPosition(self, corner: ScreenCorner) -> Tuple[float, float, float]:
        """
        Gets the locations of the corners of the GUI element.
        """
        left, right, down, up = self.getDefinedBounds()
        hcenter = (left + right) / 2
        vcenter = (down + up) / 2
        xpos = {
            ScreenCorner.TOP_LEFT: left,
            ScreenCorner.TOP_RIGHT: right,
            ScreenCorner.BOTTOM_LEFT: left,
            ScreenCorner.BOTTOM_RIGHT: right,
            ScreenCorner.TOP_MIDDLE: hcenter,
            ScreenCorner.BOTTOM_MIDDLE: hcenter,
            ScreenCorner.LEFT_MIDDLE: left,
            ScreenCorner.RIGHT_MIDDLE: right,
        }.get(corner)
        zpos = {
            ScreenCorner.TOP_LEFT: up,
            ScreenCorner.TOP_RIGHT: up,
            ScreenCorner.BOTTOM_LEFT: down,
            ScreenCorner.BOTTOM_RIGHT: down,
            ScreenCorner.TOP_MIDDLE: up,
            ScreenCorner.BOTTOM_MIDDLE: down,
            ScreenCorner.LEFT_MIDDLE: vcenter,
            ScreenCorner.RIGHT_MIDDLE: vcenter,
        }.get(corner)
        return xpos, 0.0, zpos

    def getOffsetCornerPosition(self, corner: ScreenCorner, flipPercent: float = 0.0):
        if not flipPercent:
            return self.getCornerPosition(corner)
        else:
            startPos = self.getCornerPosition(corner)
            endPos = self.getCornerPosition(corner.getOppositeCorner())
            return ColorHelper.lerpColor(startPos, endPos, flipPercent)
