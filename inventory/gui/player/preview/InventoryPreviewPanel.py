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
from toontown.gui.ScaledFrame import ScaledFrame
from toontown.gui.GUIPositionGlobals import ScreenCorner
from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.InjectorTarget import InjectorTarget
from toontown.utils import ColorHelper
from toontown.inventory.gui.player.preview.InventoryBaseItemPreview import InventoryBaseItemPreview
from toontown.inventory.gui.player.preview.InventoryToonPreview import InventoryToonPreview
from toontown.inventory.gui.player.preview.InventoryGenericItemPreview import InventoryGenericItemPreview
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from typing import Optional, List, Tuple, Dict, Set, TYPE_CHECKING
if TYPE_CHECKING:
    from toontown.utils.InjectorHelper import *


@DirectNotifyCategory()
class InventoryPreviewPanel(ScaledFrame, Bounds):
    """
    The base widget panel widget for the InventoryViewerPanel
    that shows item & action previews for an item.
    """

    RENDER_MIDPOINTS = False  # Debug flag to render midpoints

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
        self.postInitialiseFuncList.append(self._create)
        self.postInitialiseFuncList.append(self.place)

        # Set state here.
        self._item:      Optional[InventoryItem] = None
        self.previewGUI: Optional[InventoryBaseItemPreview] = None

        # Set GUI prototypes here.
        self.corner_topRight:    Optional[CornerAnchor] = None
        self.corner_topLeft:     Optional[CornerAnchor] = None
        self.corner_bottomRight: Optional[CornerAnchor] = None
        self.corner_bottomLeft:  Optional[CornerAnchor] = None
        self.midpoint:           Optional[CornerAnchor] = None
        self.upper_midpoint:     Optional[CornerAnchor] = None
        self.lower_midpoint:     Optional[CornerAnchor] = None
        self.corner_top:         Optional[CornerAnchor] = None
        self.corner_bottom:      Optional[CornerAnchor] = None

        # Initialize options.
        self.initialiseoptions(InventoryPreviewPanel)

        # Start with toon panel.
        self.setItem(None, force=True)

    def _create(self):
        self.corner_topRight    = CornerAnchor(parent=self, corner=ScreenCorner.TOP_RIGHT)
        self.corner_topLeft     = CornerAnchor(parent=self, corner=ScreenCorner.TOP_LEFT)
        self.corner_bottomRight = CornerAnchor(parent=self, corner=ScreenCorner.BOTTOM_RIGHT)
        self.corner_bottomLeft  = CornerAnchor(parent=self, corner=ScreenCorner.BOTTOM_LEFT)
        self.midpoint           = CornerAnchor(parent=self, corner=ScreenCorner.TOP_MIDDLE)
        self.upper_midpoint     = CornerAnchor(parent=self, corner=ScreenCorner.TOP_MIDDLE)
        self.lower_midpoint     = CornerAnchor(parent=self, corner=ScreenCorner.TOP_MIDDLE)
        self.corner_top         = CornerAnchor(parent=self, corner=ScreenCorner.TOP_MIDDLE)
        self.corner_bottom      = CornerAnchor(parent=self, corner=ScreenCorner.BOTTOM_MIDDLE)

        if self.RENDER_MIDPOINTS:
            for thing in (self.midpoint, self.upper_midpoint, self.lower_midpoint):
                thing['frameSize'] = (-0.05, 0.05, -0.05, 0.05)
                thing['relief'] = DGG.FLAT
                thing['frameColor'] = (1, 0, 1, 1)

    def place(self):
        if not self.postInitialized:
            return

        # Place anchors.
        self.corner_topRight.place()
        self.corner_topLeft.place()
        self.corner_bottomRight.place()
        self.corner_bottomLeft.place()
        self.midpoint.place()
        self.upper_midpoint.place()
        self.lower_midpoint.place()
        self.corner_top.place()
        self.corner_bottom.place()

        # Place the preview GUI.
        if self.previewGUI:
            self.previewGUI.place()

    def destroy(self):
        del self.previewGUI
        del self.corner_topRight
        del self.corner_topLeft
        del self.corner_bottomRight
        del self.corner_bottomLeft
        del self.midpoint
        del self.upper_midpoint
        del self.lower_midpoint
        del self.corner_top
        del self.corner_bottom
        del self._item
        super().destroy()

    def setFrameSize(self, fClearFrame = 0):
        super().setFrameSize(fClearFrame)
        self.place()

    """
    Setters
    """

    def setItem(self, item: Optional[InventoryItem], force: bool = False):
        """Sets the item of the preview panel."""
        # Don't reset to the same item.
        if item == self._item and not force:
            return
        self._item = item

        # Cleanup preview GUI.
        if self.previewGUI:
            self.previewGUI.destroy()
            self.previewGUI = None

        # Create new GUI.
        if item is None:
            self.previewGUI = InventoryToonPreview(parent=self, panel=self)
        else:
            # Get the relevant preview GUI for this item and display it.
            self.previewGUI = InventoryGenericItemPreview(parent=self, panel=self, item=item)

    """
    GUI Access for preview components
    """

    def setMidpoint(self, percent: float = 0.50):
        """Sets the midpoint for the preview panel."""
        self.midpoint['flipPercent'] = percent
        self.upper_midpoint['flipPercent'] = percent / 2
        self.lower_midpoint['flipPercent'] = (1.0 + percent) / 2

    """
    GUI Getters
    """

    def getTopRight(self) -> CornerAnchor:
        return self.corner_topRight

    def getTopLeft(self) -> CornerAnchor:
        return self.corner_topLeft

    def getBottomRight(self) -> CornerAnchor:
        return self.corner_bottomRight

    def getBottomLeft(self) -> CornerAnchor:
        return self.corner_bottomLeft

    def getMidpoint(self) -> CornerAnchor:
        return self.midpoint

    def getUpperMidpoint(self) -> CornerAnchor:
        return self.upper_midpoint

    def getLowerMidpoint(self) -> CornerAnchor:
        return self.lower_midpoint

    def getTopAnchor(self) -> CornerAnchor:
        return self.corner_top

    def getBottomAnchor(self) -> CornerAnchor:
        return self.corner_bottom

    def getTopHeight(self) -> float:
        return self.getBoundHeight() * self.midpoint['flipPercent']

    def getBottomHeight(self) -> float:
        return self.getBoundHeight() * (1 - self.midpoint['flipPercent'])


if __name__ == "__main__":
    gui = InventoryPreviewPanel(
        parent=aspect2d,
        frameSize=(-0.4, 0.4, -0.5151, 0.6151)
        # any kwargs go here
    )
    GUITemplateSliders(
        gui.previewGUI,
        'middleNode',
    )
    base.run()
