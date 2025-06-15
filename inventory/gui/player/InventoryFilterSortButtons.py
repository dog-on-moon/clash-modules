from toontown.inventory.enums.ItemTags import ItemFilterType, DefaultFilterType

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
from toontown.gui import UiHelpers
from toontown.gui.EasyManagedItem import EasyManagedItem
from toontown.gui.EasyManagedButton import EasyManagedButton
from toontown.gui.EasyScrolledFrame import EasyScrolledFrame
from toontown.gui.Bounds import Bounds
from toontown.gui.GUIPositionGlobals import ScreenCorner
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.InjectorTarget import InjectorTarget
from direct.gui.DirectGui import *
from enum import IntEnum, auto
from typing import Optional, List, Tuple, Dict, Set, TYPE_CHECKING
if TYPE_CHECKING:
    from toontown.utils.InjectorHelper import *


@DirectNotifyCategory()
class InventoryFilterSortButtons(DirectFrame, Bounds):
    """
    The filtering sort button types for inventory items.
    """

    @InjectorTarget
    def __init__(self, parent, **kw):
        # GUI boilerplate.
        optiondefs = TTGui.kwargsToOptionDefs(
            pos = (0, 0, 0),
            scale = 1.0,
            relief = None,

            buttonHeight = [0.17061, self.place],
            buttonPadding=[0.05, self.place],

            buttonWidths=[(0.43527, 0.71158, 0.37648), self.place],

            textPos=[(0, -0.03527), self.place],
            textScale=[0.1358, self.place],

            callback = None,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.postInitialized = False
        self.postInitialiseFuncList.append(lambda: setattr(self, 'postInitialized', True))
        self.initialiseoptions(InventoryFilterSortButtons)

        # Set state here.
        self.currentFilterType: Optional[ItemFilterType] = None
        self.orderAscending: bool = True

        # Set GUI prototypes here.
        self.filterButtons: Dict[ItemFilterType, InventoryFilterSortButton] = {}

        # Call these two.
        self._create()
        self.place()

        # Set the default filter type.
        self.onButtonPressed(DefaultFilterType, doCallback=False)

    def _create(self):
        for filterType in ItemFilterType:
            button = InventoryFilterSortButton(
                parent=self,
                filterType=filterType,
            )
            self.filterButtons[filterType] = button

    def place(self):
        if not self.postInitialized:
            return
        buttonList = list(self.filterButtons.values())
        for width, filterButton in zip(self['buttonWidths'], buttonList):
            filterType = filterButton.getFilterType()
            height = self['buttonHeight']
            padding = self['buttonPadding']
            UiHelpers.gui_update(
                filterButton,
                easyWidth=width,
                frameSize=(-width / 2, width / 2, -height / 2, height / 2),
                easyPadRight=padding,
                text=filterButton.getFilterType(),
                text_pos=self['textPos'],
                text_scale=self['textScale'],
                text_align=TextNode.ACenter,
                command=self.onButtonPressed,
                extraArgs=[filterType]
            )
        UiHelpers.placeElementsInHorizontalLine(
            guiList=buttonList,
            startPos=(0, 0, 0),
            alignCenter=True,
        )

    def destroy(self):
        del self.filterButtons
        super().destroy()

    """
    Actions
    """

    def reset(self):
        self.onButtonPressed(DefaultFilterType, setAscend=True)

    def onButtonPressed(self, filterType: ItemFilterType, setAscend: Optional[bool] = None, doCallback: bool = True):
        """
        Called whenever any of the buttons are pressed.
        """
        button = self.filterButtons.get(filterType)
        currentButton = self.filterButtons.get(self.currentFilterType)

        # Are these two buttons the same?
        if button is currentButton:
            # Flip ascending.
            self.orderAscending = not self.orderAscending
        else:
            # These two buttons are not the same.
            # Deselect the current button.
            if currentButton:
                currentButton.setFilterState(InventoryFilterSortButton.State.NOT_SELECTED)

            # Start in ascending.
            self.orderAscending = True

        # Force ascension override.
        if setAscend is not None:
            self.orderAscending = setAscend

        # Select the new button.
        button.setFilterState(
            InventoryFilterSortButton.State.ASCENDING
            if self.orderAscending else
            InventoryFilterSortButton.State.DESCENDING
        )
        self.currentFilterType = filterType

        # Perform filter update callback.
        if self['callback'] and doCallback:
            self['callback']()

    """
    Getters
    """

    def getSelectedFilterType(self) -> ItemFilterType:
        return self.currentFilterType

    def isAscending(self) -> bool:
        return self.orderAscending


@DirectNotifyCategory()
class InventoryFilterSortButton(EasyManagedButton, Bounds):
    """
    An individual button in the InventoryFilterSortButtons frame.
    """

    class State(IntEnum):
        NOT_SELECTED = auto()
        ASCENDING    = auto()
        DESCENDING   = auto()

    @InjectorTarget
    def __init__(self, parent, **kw):
        # GUI boilerplate.
        optiondefs = TTGui.kwargsToOptionDefs(
            pos = (0, 0, 0),
            scale = 1.0,
            filterType=ItemFilterType.Recent,
            # relief = None,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.initialiseoptions(InventoryFilterSortButton)
        self.setFilterState(self.State.NOT_SELECTED)

    def getFilterType(self) -> ItemFilterType:
        return self['filterType']

    def setFilterState(self, state):
        if state == self.State.NOT_SELECTED:
            self['frameColor'] = (1, 1, 1, 1)
        elif state == self.State.ASCENDING:
            self['frameColor'] = (0, 1, 0, 1)
        elif state == self.State.DESCENDING:
            self['frameColor'] = (1, 0, 0, 1)
        else:
            raise AttributeError


if __name__ == "__main__":
    gui = InventoryFilterSortButtons(
        parent=aspect2d,
        # any kwargs go here
    )
    GUITemplateSliders(
        gui,
        'textPos', 'textScale',
        'recentWidth',
        'recentAlpha',
        'recentRarty',
        'buttonHeight',
        'buttonPadding',
    )
    base.run()
