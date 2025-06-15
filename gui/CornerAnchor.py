from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectGuiBase import DirectGuiWidget

from toontown.gui.Bounds import Bounds
from toontown.gui.GUIPositionGlobals import ScreenCorner
from toontown.gui.TTGui import kwargsToOptionDefs
from toontown.utils.InjectorTarget import InjectorTarget

from typing import Union, Optional, Tuple, Any


class CornerAnchor(DirectGuiWidget):
    """
    A GUI node that is anchored on the corner of another GUI.
    """

    def __init__(self, parent, corner: ScreenCorner, **kw):
        # GUI boilerplate.
        optiondefs = kwargsToOptionDefs(
            # Base GUI args of the anchor
            relief=None,
            pos=(0, 0, 0),
            hpr=(0, 0, 0),
            scale=1.0,

            render=False,  # debug

            # The target and corner parameters.
            # The target is the Bounds class
            target=[parent, self.place],
            corner=[corner, self.place],

            # The flip percent is a value from 0 to 1 which
            # flips the value to the opposite corner.
            flipPercent=[0.0, self.place],

            # And absolute offset too for funsies
            xOffset=[0.0, self.place],
            zOffset=[0.0, self.place],
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.postInitialized = False
        self.postInitialiseFuncList.append(lambda: setattr(self, 'postInitialized', True))
        self.initialiseoptions(CornerAnchor)

        if self['render']:
            self.renderNode = DirectFrame(
                parent=self,
                frameSize=(-1, 1, -1, 1),
                scale=0.015,
                frameColor=(1, 0, 1, 1),
            )

    def place(self):
        if not self.postInitialized:
            return
        self.setPos(self.getFitPosition())

    def getFitPosition(self) -> Tuple[float, float, float]:
        """
        Gets the fit position for the GUI.
        """
        gui = self['target']
        corner = self['corner']
        if isinstance(gui, Bounds):
            x, y, z = gui.getOffsetCornerPosition(corner, flipPercent=self['flipPercent'])
            return x + self['xOffset'], y, z + self['zOffset']
        else:
            raise AttributeError('CornerAnchor target must inherit and define Bounds')
