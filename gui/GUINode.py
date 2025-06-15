from direct.gui.DirectGuiBase import DirectGuiWidget

from toontown.gui.Bounds import Bounds
from toontown.gui.GUIPositionGlobals import ScreenCorner
from toontown.gui.TTGui import kwargsToOptionDefs
from toontown.utils.InjectorTarget import InjectorTarget

from typing import Union, Optional, Any


class GUINode(DirectGuiWidget, Bounds):
    """
    A simple GUI node to parent various GUI elements onto.
    Has injector access if given a name.
    """

    @InjectorTarget
    def __init__(self, parent, name: str = None, **kw):
        # GUI boilerplate.
        optiondefs = kwargsToOptionDefs(
            relief=None,
            pos=(0, 0, 0),
            hpr=(0, 0, 0),
            scale=1.0,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.initialiseoptions(GUINode)

        # Set injector target.
        if name is not None and __debug__:
            setattr(base, name, self)

    @classmethod
    def makeOnCorner(cls, gui: Union[DirectGuiWidget, Any], corner: ScreenCorner) -> 'GUINode':
        """
        Creates a GUINode located at the corner of a GUI element's frame.
        The GUI must have a well-defined frameSize.
        """
        if isinstance(gui, Bounds):
            return cls(
                parent=gui, name='cornerAnchor',
                pos=gui.getCornerPosition(corner),
            )
        else:
            left, right, down, up = gui['frameSize']
            hcenter = (left + right) / 2
            vcenter = (down + up) / 2
            xpos = {
                ScreenCorner.TOP_LEFT:      left,
                ScreenCorner.TOP_RIGHT:     right,
                ScreenCorner.BOTTOM_LEFT:   left,
                ScreenCorner.BOTTOM_RIGHT:  right,
                ScreenCorner.TOP_MIDDLE:    hcenter,
                ScreenCorner.BOTTOM_MIDDLE: hcenter,
                ScreenCorner.LEFT_MIDDLE:   left,
                ScreenCorner.RIGHT_MIDDLE:  right,
            }.get(corner)
            zpos = {
                ScreenCorner.TOP_LEFT:      up,
                ScreenCorner.TOP_RIGHT:     up,
                ScreenCorner.BOTTOM_LEFT:   down,
                ScreenCorner.BOTTOM_RIGHT:  down,
                ScreenCorner.TOP_MIDDLE:    up,
                ScreenCorner.BOTTOM_MIDDLE: down,
                ScreenCorner.LEFT_MIDDLE:   vcenter,
                ScreenCorner.RIGHT_MIDDLE:  vcenter,
            }.get(corner)
            return cls(
                parent=gui, name='cornerAnchor',
                pos=(xpos, 0, zpos),
            )
