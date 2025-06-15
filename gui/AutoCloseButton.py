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
if TYPE_CHECKING:
    from toontown.utils.InjectorHelper import *


@DirectNotifyCategory()
class AutoCloseButton(EasyManagedButton):
    """
    A close button that automatically latches on to its parent.
    """

    @InjectorTarget
    def __init__(self, parent, **kw):
        # GUI boilerplate.
        self._parent = parent
        gui = loader.loadModel('phase_3/models/gui/ttcc_gui_generalButtons')
        optiondefs = TTGui.kwargsToOptionDefs(
            pos = (0, 0, 0), relief = None,
            scale = 2.0,

            image=(
                gui.find('**/CloseBtn_UP'),
                gui.find('**/CloseBtn_DN'),
                gui.find('**/CloseBtn_Rllvr'),
                gui.find('**/CloseBtn_UP')
            ),
            text=('', '', 'Close'),
            text_scale=0.04,
            text_pos=(0.0, 0.05346),
            text_fg=VBase4(1, 1, 1, 1),

            posOffset = [(0.1, 0, 0.1), self.place],
            corner = [ScreenCorner.TOP_RIGHT, self.place],
            cornerDist = [0.0, self.place],
        )
        gui.removeNode()
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.postInitialized = False
        self.postInitialiseFuncList.append(lambda: setattr(self, 'postInitialized', True))
        self.initialiseoptions(AutoCloseButton)

        self.place()

    def destroy(self):
        self._parent = None
        super().destroy()

    def place(self):
        if not self.postInitialized:
            return
        x, y, z = self._parent.getOffsetCornerPosition(self['corner'], -self['cornerDist'])
        a, b, c = self['posOffset']
        self.setPos(x + a, y + b, z + c)


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
