if __name__ == "__main__":
    from tools.headless.headlessbase import HeadlessStart
    from tools.headless.headlessbase.HeadlessBase import HeadlessBase
    base = HeadlessBase(wantHotkeys=False)
    if __debug__:
        from toontown.utils.DeveloperInjector import startInjector
        startInjector()
    # base.initCR()  # defines base.cr
    # base.startHeadlessShow()
    # base.initTalkAssistant()

from toontown.gui.TTGui import kwargsToOptionDefs
from toontown.gui.GUITemplateSliders import GUITemplateSliders
from toontown.gui.GUINode import GUINode
from toontown.gui import UiHelpers
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.InjectorTarget import InjectorTarget
from direct.gui.DirectGui import *


@DirectNotifyCategory()
class GenericCloseButton(DirectButton):
    """
    A generic close button.
    """

    @InjectorTarget
    def __init__(self, parent, **kw):
        # GUI boilerplate.
        buttonGui = loader.loadModel('phase_3/models/gui/ttcc_gui_generalButtons')
        optiondefs = kwargsToOptionDefs(
            pos = (0, 0, 0),
            scale = 1.0,
            relief = None,
            image=(
                buttonGui.find('**/CloseBtn_UP'),
                buttonGui.find('**/CloseBtn_DN'),
                buttonGui.find('**/CloseBtn_Rllvr'),
                buttonGui.find('**/CloseBtn_UP')
            ),
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.initialiseoptions(self.__class__)
        buttonGui.removeNode()


if __name__ == "__main__":
    gui = GenericCloseButton(
        parent=aspect2d,
        # any kwargs go here
    )
    GUITemplateSliders(
        guiAffected=gui,
        guiKeys=('pos', 'scale'),
    )
    base.run()
