"""
A template file for creating modular sub-GUIS.
Includes all of the base code necessary to properly inherit from a GUI class.

This file should not be imported. Instead, you are welcome to copy/paste
the template file into other files as a base for designing any GUI elements.

This template now includes HeadlessStart, as seen below.
Running this file as a module will open the GUI in a headless setting
for streamlined testing and development.
"""
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
from toontown.gui.TilingScaledFrame import TilingScaledFrame
from toontown.gui.UiLerper import UILerper
from toontown.toon.gui import GuiBinGlobals
from toontown.toonbase import ToontownGlobals

from toontown.utils.InjectorTarget import InjectorTarget
from toontown.utils import ColorHelper, Nodes
from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase import PythonUtil
from panda3d.core import *


class GUITemplate(DirectFrame, Bounds):
    """

    """

    @InjectorTarget
    def __init__(self, parent, **kw):
        # GUI boilerplate.
        optiondefs = TTGui.kwargsToOptionDefs(
            pos = (0, 0, 0),
            scale = 1.0,
            # relief = None,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.postInitialized = False
        self.postInitialiseFuncList.append(lambda: setattr(self, 'postInitialized', True))
        self.initialiseoptions(self.__class__)  # <-- Update this

        # Set state here.
        # self.inventory: Inventory | None = None

        # Set GUI prototypes here.
        # self.anchor_left: CornerAnchor | None = None

        # Call these two.
        self._create()
        self.place()

    def _create(self):
        # self.anchor_left = CornerAnchor(parent=self, corner=ScreenCorner.LEFT_MIDDLE)
        pass

    def place(self):
        if not self.postInitialized:
            return
        # self.corner_topRight.place()
        # self.text_label.setPos(self['labelPos'])
        pass

    def destroy(self):
        pass
        super().destroy()


if __name__ == "__main__":
    gui = GUITemplate(
        parent=aspect2d,
        # any kwargs go here
    )
    GUITemplateSliders(
        gui,
        'pos', 'scale'
    )
    base.run()
