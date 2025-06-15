"""
Example of the Crazy Geometric Shapes !!!
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

from toontown.gui.TTGui import kwargsToOptionDefs
from toontown.gui.GUITemplateSliders import GUITemplateSliders
from toontown.gui.GUINode import GUINode
from toontown.gui.ScaledFrame import ScaledFrame
from toontown.gui import UiHelpers
from toontown.utils import Nodes
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.InjectorTarget import InjectorTarget
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *


@DirectNotifyCategory()
class CrazyGeometricShapesExample(ScaledFrame):
    """
    Demonstrates the crazy geometric shapes.
    """

    @InjectorTarget
    def __init__(self, parent, **kw):
        # GUI boilerplate.
        optiondefs = kwargsToOptionDefs(
            pos = (0, 0, 0),
            parent=base.aspect2d,
            frameSize=(-0.5, 0.4, -0.5, 0.6),
            scaledTexture='phase_4/maps/normalDistrict.png',
            text='YOUR SOUL\nIS MINE',
            text_scale=0.07,
            text_fg=(0, 0, 0, 1),
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.initialiseoptions(self.__class__)

        # Make our cute little clipplane node.
        self.cgsNp = self.attachNewNode(Nodes.CrazyGeometricShapes(radius=1.0, segments=64).node())
        self.cgsNp.setScale(0.015)
        Parallel(
            LerpPosInterval(
                nodePath=self.cgsNp,
                duration=3.0,
                pos=(-1, 0, -1),
                startPos=(1, 0, 1),
            ),
            LerpHprInterval(
                nodePath=self.cgsNp,
                duration=3.0,
                hpr=(360, 360, 360),
                startHpr=(0, 0, 0),
            ),
        ).loop()

    def destroy(self):
        pass
        super().destroy()


if __name__ == "__main__":
    gui = CrazyGeometricShapesExample(
        parent=aspect2d,
        # any kwargs go here
    )
    base.run()
