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
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.InjectorTarget import InjectorTarget
from toontown.utils import ColorHelper
from direct.gui.DirectGui import *
from typing import Optional, List, Tuple, Dict, Set, TYPE_CHECKING
if TYPE_CHECKING:
    from toontown.inventory.gui.player.preview.InventoryPreviewPanel import InventoryPreviewPanel
    from toontown.utils.InjectorHelper import *


@DirectNotifyCategory()
class InventoryBaseItemPreview(DirectFrame, Bounds):
    """
    The base class for inventory item previews.
    """

    @InjectorTarget
    def __init__(self, parent, panel, **kw):
        """
        :type parent: NodePath
        :type panel: InventoryPreviewPanel
        """
        # GUI boilerplate.
        optiondefs = TTGui.kwargsToOptionDefs(
            pos = (0, 0, 0),
            scale = 1.0,
            relief = None,

            # The placement of the "middle" node (vertically aligned).
            middleNode = [0.60, self._testPlace],
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.postInitialized = False
        self.postInitialiseFuncList.append(lambda: setattr(self, 'postInitialized', True))
        self.postInitialiseFuncList.append(self._create)
        self.postInitialiseFuncList.append(self._testPlace)

        # Set state here.
        self.panel = panel  # type: InventoryPreviewPanel
        self.panel.clipWithinFrame(self)

        # Initialize options.
        self.initialiseoptions(InventoryBaseItemPreview)

    def _create(self):
        # self.corner_topRight = CornerAnchor(parent=self, corner=ScreenCorner.TOP_MIDDLE)
        pass

    def _testPlace(self):
        if self.postInitialized:
            self.place()

    def place(self):
        self.panel.setMidpoint(self['middleNode'])

    def destroy(self):
        del self.panel
        super().destroy()


if __name__ == "__main__":
    gui = InventoryBaseItemPreview(
        parent=aspect2d,
        # any kwargs go here
    )
    GUITemplateSliders(
        gui,
        'pos', 'scale'
    )
    base.run()
