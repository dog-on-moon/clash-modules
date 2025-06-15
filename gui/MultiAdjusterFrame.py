
if __name__ == "__main__":
    from tools.headless.headlessbase import HeadlessStart
    from tools.headless.headlessbase.HeadlessBase import HeadlessBase
    base = HeadlessBase(wantHotkeys=False)
    if __debug__:
        from toontown.utils.DeveloperInjector import startInjector
        startInjector()
    # base.initCR()  # defines base.cr
    # base.startHeadlessShow()

from toontown.toon.socialpanel.SocialPanelGlobals import sp_gui
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
class MultiAdjusterFrame(ScaledFrame):
    """
    A scaled frame with support for multiple sliders.
    """

    @InjectorTarget
    def __init__(self, parent, **kw):
        # GUI boilerplate.
        optiondefs = TTGui.kwargsToOptionDefs(
            pos = (0, 0, 0),
            scale = 1.0,

            rounding=2,
            frameScale=1.0,
            data={},  # dict[str, tuple[start, default, end]]
            callback = None,
            releaseCallback = None,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.postInitialized = False
        self.postInitialiseFuncList.append(lambda: setattr(self, 'postInitialized', True))
        self.initialiseoptions(MultiAdjusterFrame)

        # Set state here.
        self.lastValue = tuple(
            round(self.getData()[key][1], self['rounding'])
            for key in self.getData().keys()
        )

        # Set GUI prototypes here.
        self.anchors: dict[str, CornerAnchor] = {}
        self.sliders: dict[str, DirectSlider] = {}
        self.lock: bool = False

        # Call these two.
        if self.__class__ is MultiAdjusterFrame:
            self._create()
            self.place()

        self.accept('MultiAdjusterFrame-new', self._onFrameOpen)

    def _create(self):
        start, end = 0.13, 0.87
        keyCount = len(self.getData())
        for i, key in enumerate(self.getData().keys()):
            flipPercent = lerp(start, end, i / (keyCount - 1))
            low, default, high = self.getData()[key]
            self.anchors[key] = CornerAnchor(parent=self, corner=ScreenCorner.TOP_MIDDLE, flipPercent=flipPercent)
            self.sliders[key] = DirectSlider(
                parent=self.anchors[key], relief=None,
                pos=(0, 0, 0), scale=1.0,
                image=sp_gui.find('**/Scrollbar_Screen'), image_scale=((790 / 36) * 0.09, 0.09, 0.09),
                thumb_image=sp_gui.find('**/Scroll1'), thumb_relief=None, thumb_image_scale=0.2,
                text=key, text_pos=(-1.12287, -0.0532), text_scale=0.05,
                value=default, range=(low, high), command=self.doCallback,
            )
            self.sliders[key].thumb.bind(DGG.B1RELEASE, self.releaseCallback)

    def place(self):
        if not self.postInitialized:
            return

        height = (0.18242 / 3.0) * self['frameScale'] * len(self.sliders)
        width = 0.6177 * self['frameScale']

        self['frameSize'] = (-width / 2, width / 2, -height / 2, height / 2)

        for anchor in self.anchors.values():
            anchor.place()
        for slider in self.sliders.values():
            sliderScale = (width / 2) * 0.93
            slider.setPos(width * 0.06, 0, 0)
            slider.setScale(sliderScale)
            slider['text_scale'] = 0.2 * (sliderScale / 0.3255)

    def destroy(self):
        del self.anchors
        del self.sliders
        super().destroy()

    def show(self):
        super().show()
        messenger.send('MultiAdjusterFrame-new', [self])

    def reset(self):
        self.lock = True
        for key, slider in self.sliders.items():
            slider.setValue(self.getData()[key][1])
        self.lock = False

    def getData(self) -> dict[str, tuple[float, float, float]]:
        return self['data']

    def doCallback(self):
        if not self['callback']:
            return
        if self.lock:
            return
        newValue = tuple(
            round(self.sliders[key].getValue(), self['rounding'])
            for key in self.getData().keys()
        )
        if self.lastValue == newValue:
            return
        self.lastValue = newValue
        self['callback'](newValue)

    def releaseCallback(self, *_):
        if not self['releaseCallback']:
            return
        if self.lock:
            return
        newValue = tuple(
            round(self.sliders[key].getValue(), self['rounding'])
            for key in self.getData().keys()
        )
        self.lastValue = newValue
        self['releaseCallback'](newValue)

    def _onFrameOpen(self, frame):
        if frame is self:
            return
        self.hide()


if __name__ == "__main__":
    gui = MultiAdjusterFrame(
        parent=aspect2d,
        # any kwargs go here
    )
    # GUITemplateSliders(
    #     gui,
    #     'frameSize'
    # )
    base.run()
