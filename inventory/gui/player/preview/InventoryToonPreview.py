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
from toontown.toon.socialpanel.SocialPanelGlobals import sp_gui
from toontown.inventory.gui.player.preview.InventoryBaseItemPreview import InventoryBaseItemPreview
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.InjectorTarget import InjectorTarget
from toontown.utils import ColorHelper
from toontown.toon.Toon import Toon
from toontown.toon.ToonDNA import ToonDNA
from direct.gui.DirectGui import *
from typing import Optional, List, Tuple, Dict, Set, TYPE_CHECKING
if TYPE_CHECKING:
    from toontown.inventory.gui.player.preview.InventoryPreviewPanel import InventoryPreviewPanel
    from toontown.utils.InjectorHelper import *


@DirectNotifyCategory()
class InventoryToonPreview(InventoryBaseItemPreview):
    """
    The toon preview for the inventory preview panel.
    """

    @InjectorTarget
    def __init__(self, parent, panel, **kw):
        """
        :type parent: NodePath
        :type panel: InventoryPreviewPanel
        """
        # GUI boilerplate.
        optiondefs = TTGui.kwargsToOptionDefs(
            toonTopPad = -0.04,
            toonBottomPad = 0.05,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, panel, **kw)

        self.toon: Optional[Toon] = None
        self.toonNode: Optional[GUINode] = None
        self.slider: Optional[DirectSlider] = None

        self.initialiseoptions(InventoryToonPreview)

    def _create(self):
        super()._create()
        self.toonNode = GUINode(parent=self.panel.getMidpoint(), pos=(0, 0, self['toonBottomPad']))
        self.toon = self.makeToon()
        self.panel.clipWithinFrame(self.toon)
        self.slider = DirectSlider(
            parent=self.panel.getMidpoint(), relief=None,
            image=sp_gui.find('**/Scrollbar_Screen'),
            image_scale=((790 / 36) * 0.09, 0.09, 0.09),
            thumb_image=sp_gui.find('**/Scroll1'),
            thumb_relief = None,
            thumb_image_scale=0.2,
            value=-180,
            range=(-360, 0),
            command=self.setToonSpin,
        )

    def place(self):
        super().place()

        # Scale the Toon to fit in the frame.
        self.toon.setScale(0.2)
        ll, rr = self.toon.getTightBounds()
        *_, za = ll
        *_, zb = rr
        toonHeight = zb - za
        panelHeight = self.panel.getTopHeight() + self['toonTopPad'] - self['toonBottomPad']
        toonScale = min(1.0, panelHeight / max(toonHeight, 0.001))
        self.toon.setScale(0.2 * toonScale)

        # Set the scale of the slider.
        self.slider.setScale(0.48 * self.panel.getBoundWidth())

    def destroy(self):
        if self.toon:
            self.toon.delete()
            self.toon = None
        self.toonNode.destroy()
        self.slider.destroy()
        super().destroy()

    def makeToon(self):
        toon = Toon()
        toon.flattenStrong()
        toon.reparentTo(self.toonNode)
        if base.localAvatar and base.localAvatar.style:
            toon.setDNAString(base.localAvatar.style.makeNetString())
        else:
            dna = ToonDNA()
            dna.newToonRandom()
            toon.setDNA(dna)
        toon.setScale(1.0)
        toon.setPosHpr(0, 0, 0, 180, 0, 0)
        toon.getGeomNode().setDepthWrite(1)
        toon.getGeomNode().setDepthTest(1)
        toon.getGeomNode().setTwoSided(True)
        toon.loop('neutral')
        return toon

    """
    Panel callbacks
    """

    def setToonSpin(self):
        h = self.slider.getValue()
        if self.toon:
            self.toon.setH(h)


if __name__ == "__main__":
    gui = InventoryToonPreview(
        parent=aspect2d,
        # any kwargs go here
    )
    GUITemplateSliders(
        gui,
        'pos', 'scale'
    )
    base.run()
