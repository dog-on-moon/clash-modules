"""
A template file for creating modular sub-GUIS.
Includes all of the base code necessary to properly inherit from a GUI class.

This file should not be imported. Instead, you are welcome to copy/paste
the template file into other files as a base for designing any GUI elements.

This template now includes HeadlessStart, as seen below.
Running this file as a module will open the GUI in a headless setting
for streamlined testing and development.
"""
from direct.directtools.DirectUtil import CLAMP

if __name__ == "__main__":
    from tools.headless.headlessbase import HeadlessStart
    from tools.headless.headlessbase.HeadlessBase import HeadlessBase
    base = HeadlessBase(wantHotkeys=False)
    if __debug__:
        from toontown.utils.DeveloperInjector import startInjector
        startInjector()
    # base.initCR()  # defines base.cr
    # base.startHeadlessShow()

from toontown.gui import TTGui
from toontown.gui.GUITemplateSliders import GUITemplateSliders
from toontown.gui.GUINode import GUINode
from toontown.gui.CornerAnchor import CornerAnchor
from toontown.gui import UiHelpers
from toontown.gui.EasyManagedItem import EasyManagedItem
from toontown.gui.EasyManagedButton import EasyManagedButton
from toontown.gui.EasyScrolledFrame import EasyScrolledFrame
from toontown.gui.Bounds import Bounds
from toontown.gui.GUIPositionGlobals import ScreenCorner
from toontown.gui.ScaledFrame import ScaledFrame
from toontown.toon.gui import GuiBinGlobals
from toontown.toonbase import ToontownGlobals

from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.InjectorTarget import InjectorTarget
from toontown.utils import ColorHelper
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase import PythonUtil
from typing import Optional, List, Tuple, Dict, Set, TYPE_CHECKING

from panda3d.core import *

if TYPE_CHECKING:
    from toontown.utils.InjectorHelper import *


@DirectNotifyCategory()
class WorldGUI(DirectFrame, Bounds):
    """
    A GUI element that is fixed on a target NodePath,
    yet still renders in 2D.
    """

    @InjectorTarget
    def __init__(self, parent, **kw):
        # GUI boilerplate.
        optiondefs = TTGui.kwargsToOptionDefs(
            pos = (0, 0, 0),
            scale = 1.0,

            target = None,
            screenOffset = (0, 0, 0),
            worldOffset = (0, 0, 0),
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.postInitialized = False
        self.postInitialiseFuncList.append(lambda: setattr(self, 'postInitialized', True))
        self.initialiseoptions(WorldGUI)

        self._centeringActive: bool = True
        self.__startCenterTask()

    def destroy(self):
        self.__endCenterTask()
        super().destroy()

    """
    Interface
    """

    def setWorldTransform(self, mode: bool):
        self._centeringActive = mode

    def setTarget(self, target: NodePath | None):
        self['target'] = target
        if target:
            self.__recenterButtonFrameTask()

    """
    Position mapping
    """

    def __startCenterTask(self):
        taskMgr.add(self.__recenterButtonFrameTask, 'recenterButtonFrameTask', 10)

    def __endCenterTask(self):
        taskMgr.remove('recenterButtonFrameTask')

    def __recenterButtonFrameTask(self, task=None):
        if not self.target:
            self.onNoTarget()
        elif self._centeringActive:
            self.setPos(self.getSelectedObjectScreenXY())
        if task:
            return task.cont

    def onNoTarget(self):
        pass

    def getSelectedObjectScreenXY(self):
        tNodePath = self.target.attachNewNode('temp')
        if hasattr(self.target, 'center'):
            tNodePath.setPos(self.target.center)
        else:
            tNodePath.setPos(0, 0, 0)

        x, y, z = self['worldOffset']
        xx, yy, zz = tNodePath.getPos()
        tNodePath.setPos(x + xx, y + yy, z + zz)

        # Where does the node path's projection fall on the near plane
        nearVec = self.getNearProjectionPoint(tNodePath)
        # Where does this fall on focal plane
        nearVec *= base.camLens.getFocalLength() / base.camLens.getNear()

        # Convert to aspect2d coords (clamping to visible screen
        render2dX = CLAMP(nearVec[0] / (base.camLens.getFilmSize()[0] / 2.0), -.9, 0.9)
        aspect2dX = render2dX * base.getAspectRatio()
        aspect2dZ = CLAMP(nearVec[2] / (base.camLens.getFilmSize()[1] / 2.0), -.8, 0.9)
        tNodePath.removeNode()

        # Return the resulting value
        x, y, z = self['screenOffset']
        return Vec3(aspect2dX + x, y, aspect2dZ + z)

    def getNearProjectionPoint(self, nodePath):
        # Find the position of the projection of the specified node path on the near plane
        origin = nodePath.getPos(camera)
        # project this onto near plane
        if origin[1] != 0.0:
            return origin * (base.camLens.getNear() / origin[1])
        else:
            # Object is coplanar with camera, just return something reasonable
            return Point3(0, base.camLens.getNear(), 0)

    @property
    def target(self):
        return self['target']


if __name__ == "__main__":
    gui = WorldGUI(
        parent=aspect2d,
        # any kwargs go here
    )

    GUITemplateSliders(
        gui,
        'pos', 'scale'
    )
    base.run()
