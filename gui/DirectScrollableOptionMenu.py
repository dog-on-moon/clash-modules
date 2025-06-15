if __name__ == "__main__":
    from tools.headless.headlessbase import HeadlessStart
    from tools.headless.headlessbase.HeadlessBase import HeadlessBase
    base = HeadlessBase(wantHotkeys=False)
    if __debug__:
        from toontown.utils.DeveloperInjector import startInjector
        startInjector()
    # base.initCR()  # defines base.cr
    # base.startHeadlessShow()

from toontown.gui.TTGui import kwargsToOptionDefs
from toontown.gui.GUITemplateSliders import GUITemplateSliders
from toontown.gui.GUINode import GUINode
from toontown.gui import UiHelpers
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.InjectorTarget import InjectorTarget
from direct.gui.DirectGui import *


@DirectNotifyCategory()
class DirectScrollableOptionMenu(DirectOptionMenu):
    """
    A DirectOptionMenu with scroll support.
    """

    @InjectorTarget
    def __init__(self, parent, **kw):
        # GUI boilerplate.
        optiondefs = kwargsToOptionDefs(
            pos = (0, 0, 0),
            scale = 1.0,
            scrollDist = 1.3333,
            bin=10000,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.initialiseoptions(DirectScrollableOptionMenu)
        self.setBin('sorted-gui-popup', self['bin'])

    def setItems(self):
        super().setItems()
        for itemIndex in range(len(self['items'])):
            skipUp = (itemIndex == 0)
            skipDown = (itemIndex == (len(self['items']) - 1))
            self.bindToScroll(self.component(f'item{itemIndex}'),
                              skipUp=skipUp, skipDown=skipDown)
        self.popupMenu.setBin('sorted-gui-popup', self['bin'] + 1)

    def bindToScroll(self, gui, skipUp: bool = False, skipDown: bool = False):
        if not skipUp:
            gui.bind(DGG.WHEELUP, lambda _: self._scrollItems(-1))
        if not skipDown:
            gui.bind(DGG.WHEELDOWN, lambda _: self._scrollItems(1))

    def _scrollItems(self, direction: int):
        scrollDist = self['scrollDist']
        for itemIndex in range(len(self['items'])):
            item = self.component(f'item{itemIndex}')
            x, y, z = item.getPos()
            item.setPos(x, y, z + (direction * scrollDist))


if __name__ == "__main__":
    gui = DirectScrollableOptionMenu(
        parent=aspect2d,
        items=[
            'milk',
            'chocolate',
            'cookies',
            'candy',
        ],
        initialitem=0,
        scale=0.1,
    )
    GUITemplateSliders(
        gui,
        'pos', 'scale'
    )
    base.run()
