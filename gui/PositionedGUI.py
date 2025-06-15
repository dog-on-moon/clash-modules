"""
A subclass for GUI that intends on being positioned
automatically by the GUIPositionManager.
"""
import random

from direct.gui.DirectGuiBase import DirectGuiWidget
from direct.gui.DirectFrame import DirectFrame

from toontown.gui.GUIPositionGlobals import *
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory


class OnscreenPositionData:
    """
    Essentially a dataclass for onscreen positional data.
    """

    def __init__(self,
                 width=0.0, height=0.0,
                 left=0.0, right=0.0, top=0.0, down=0.0):
        """
        Defines the onscreen position for the GUI.
        :param width:  The width of this GUI.
                       When set, the GUI will expand horizontally on-screen.
        :param height: The height of this GUI.
                       When set, the GUI will expand vertically on-screen.
        :param left:   The left margin of this GUI.
        :param right:  The right margin of this GUI.
        :param top:    The top margin of this GUI.
        :param down:   The bottom margin of this GUI.
        """
        self.width = width
        self.height = height
        self.left = left
        self.right = right
        self.top = top
        self.down = down


@DirectNotifyCategory()
class PositionedGUI:
    """
    A subclass for GUI that intends on being positioned automagically on the screen.
    """

    # The corner where we belong.
    SCREEN_CORNER = ScreenCorner.TOP_RIGHT
    SCREEN_INDEX = 0

    # Positional offset
    POS_OFFSET = (0, 0, 0)

    # Default bounds
    GUI_BOUNDS = OnscreenPositionData()

    # Does this GUI extend vertically?
    EXTEND_VERTICAL = 0

    # Arguments for position management.
    ENTER_SEQ = ManagedGUIEnterSequence.instant
    ENTER_SEQ_ARGS = []
    EXIT_SEQ = ManagedGUIExitSequence.instant
    EXIT_SEQ_ARGS = []

    # Debug mode; renders a DirectFrame with our margins.
    DEBUG_MARGIN_RENDER = False
    DEBUG_MARGIN_POS = (0, 0, 0)  # set manually for testing, probably through injector

    def startPositionManagement(self, callback=None, overrideSeq=None, overrideSeqArgs=None) -> None:
        """
        Start letting this GUI's position be controlled by the GUIPositionManager.
        :param callback:        A callback to run once the enter sequence is complete.
        :param overrideSeq:     The actual way this GUI leaves when managed.
        :param overrideSeqArgs: The args for the override seq.
        :return:                None.
        """
        self.__positionManager.manageGui(
            gui=self,
            index=self.getScreenIndex(),
            corner=self.getScreenCorner(),
            sequence=overrideSeq or self.ENTER_SEQ,
            sequenceArgs=overrideSeqArgs or self.ENTER_SEQ_ARGS,
            callback=callback,
        )
        self.renderDebugMargins()

    def stopPositionManagement(self, callback=None, overrideSeq=None, overrideSeqArgs=None) -> None:
        """
        Stops letting this GUI's position be controlled by the GUIPositionManager.
        :param callback:        A callback to run once the exit sequence is complete.
        :param overrideSeq:     The actual way this GUI leaves when unmanaged.
        :param overrideSeqArgs: The args for the override seq.
        :return:                None.
        """
        self.__positionManager.unmanageGui(
            gui=self,
            sequence=overrideSeq or self.EXIT_SEQ,
            sequenceArgs=overrideSeqArgs or self.EXIT_SEQ_ARGS,
            callback=callback
        )

    """
    Various position manipulations
    """

    def moveToIndex(self, index: int) -> None:
        """
        Tells our position manager to move us to a given position.
        :param index: The index to move to.
        :return: None.
        """
        self.__positionManager.moveGuiToIndex(self, index)

    def _updatePositionManager(self):
        """
        Tells the position manager to update positions of this corner.
        :return:
        """
        messenger.send(MSG_UPDATE_POSITION_MANAGER, [self.getScreenCorner()])

    def endMovementSequence(self):
        """Tells our position manager to end our movement sequence. (ends all in the corner)"""
        self.__positionManager.finishSequencesAtCorner(self.getScreenCorner())

    """
    Debug
    """

    def getGuiElement(self):
        return self

    def renderDebugMargins(self):
        if not (self.DEBUG_MARGIN_RENDER and __debug__):
            return
        bounds = self.onscreenPositionBounds()
        left = - (bounds.width / 2) - bounds.left
        right = (bounds.width / 2) + bounds.right
        top = (bounds.height / 2) + bounds.top
        down = - (bounds.height / 2) - bounds.down
        if hasattr(self, 'DEBUG_BOUNDS'):
            self.DEBUG_BOUNDS.destroy()
        setattr(self, 'DEBUG_BOUNDS', DirectFrame(
            self.getGuiElement(), pos=self.DEBUG_MARGIN_POS, frameSize=(left, right, top, down),
            frameColor=(random.random(), random.random(), random.random(), 0.4),
        ))

    """
    Properties
    """

    @property
    def __positionManager(self):
        return base.guiPositionManager

    def getXYScale(self):
        if not self.getGuiElement():
            return 1, 1
        scale = self.getGuiElement().getScale()
        if type(scale) in (int, float):
            return scale, scale
        else:
            xscale, _, yscale = scale
            return xscale, yscale

    """
    Position getters
    """

    def getScreenIndex(self):
        return self.SCREEN_INDEX

    def extendsVertical(self):
        return self.EXTEND_VERTICAL

    def getScreenCorner(self):
        return self.SCREEN_CORNER

    def getPosOffset(self):
        return Vec3(*self.POS_OFFSET)

    def onscreenPositionActive(self) -> bool:
        """
        Determines if this GUI should be positioned onscreen currently.
        If not, then the GUIPositionManager will ignore this object.

        If this value changes, call self.updatePositionManager().
        """
        return True

    def onscreenPositionBounds(self) -> OnscreenPositionData:
        """
        Returns the bounds of this GUI's onscreen position.
        Namely, gets the width, height, and margins.

        If this value changes, call self.updatePositionManager().
        """
        return self.GUI_BOUNDS


class PaddingGUI(DirectFrame, PositionedGUI):
    """
    A subclass of PositionedGUI.

    Holds no GUI elements, but can be treated as PositionedGUI
    to add padding onto GUI elements easily.
    """

    def __init__(self, marginData: OnscreenPositionData = None,
                 corner: ScreenCorner = ScreenCorner.TOP_RIGHT,
                 vertical: bool = False, active: bool = True):
        # Initialize GUI
        optiondefs = (('relief', None, None),)
        self.defineoptions({}, optiondefs)
        DirectFrame.__init__(self, hidden)
        self.initialiseoptions(self.__class__)

        # Initialize PositionedGUI bits
        self.marginData = marginData or OnscreenPositionData()
        self.vertical = vertical
        self.active = active
        self.corner = corner
        self.startPositionManagement()

    def destroy(self):
        self.stopPositionManagement()
        self.marginData = None
        super().destroy()

    def setMarginData(self, marginData: OnscreenPositionData):
        if self.marginData != marginData:
            self.marginData = marginData
            if self.onscreenPositionActive():
                self._updatePositionManager()

    def setActive(self, mode: bool):
        if self.active != mode:
            self.active = mode
            self._updatePositionManager()

    def extendsVertical(self):
        return self.vertical

    def getScreenCorner(self):
        return self.corner

    def onscreenPositionActive(self) -> bool:
        return self.active

    def onscreenPositionBounds(self) -> OnscreenPositionData:
        return self.marginData
