from toontown.inventory.base.InventoryDelta import InventoryDelta
from toontown.inventory.enums.InventoryEnums import InventoryAction

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
from toontown.gui.UiHelpers import GridType
from toontown.toon.gui import GuiBinGlobals
from toontown.gui.EasyManagedItem import EasyManagedItem
from toontown.gui.EasyManagedButton import EasyManagedButton
from toontown.gui.EasyScrolledFrame import EasyScrolledFrame
from toontown.gui.TTGui import getMousePositionWithAspect2d
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.InjectorTarget import InjectorTarget
from toontown.utils.DGGEventIgnorer import ignore_event
from toontown.inventory.gui.general.ItemFrame import ItemFrame
from toontown.inventory.gui.general.ItemHoverFrame import ItemHoverFrame
from toontown.inventory.base.InventoryItem import InventoryItem
from panda3d.core import *
from direct.gui.DirectGui import *
from typing import List, Union, Optional
import math


@DirectNotifyCategory()
class ItemFrameGrid(DirectFrame):
    """
    Holds a grid collection of Item Frames.
    Contains several useful parameters to make it trivial
    to position and organize the item frames.
    """

    @InjectorTarget
    def __init__(self, parent, **kw):
        # GUI boilerplate.
        optiondefs = kwargsToOptionDefs(
            pos = (0, 0, 0),
            scale = 1.0,

            # Some default visuals for the back.
            relief = DGG.FLAT,
            frameColor = (0.7, 0.7, 0.7, 0.7),

            # Grid Parameters
            gridWidth = 3,
            gridHeight = 3,
            gridDistance = 0.1,
            gridScale = 1.0,

            # Scrollbar Parameters
            scrollEnabled = True,
            scrollbarPosition=(0.0, 0, 0),
            scrollbarOrientation=DGG.VERTICAL,
            scrollbarWidth=0.1,
            scrollbarLengthMult=1.0,
            scrollbarWidthMult=1.0,
            scrollbarThumbResize=False,
            scrollbarKwargs={},

            hoverFrameScale=0.7,

            # Callbacks
            callback=None,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.initialiseoptions(self.__class__)
        self.setBin('sorted-gui-popup', GuiBinGlobals.ItemFrameBin - 1)
        self.itemNameLabel = DirectLabel(
            parent=parent,
            relief=None,
            pos=(0, 0, -0.6),
            text='',
            textMayChange=1,
            text_scale=0.08
        )

        # Create our item hover element
        self.itemHover = ItemHoverFrame(
            parent=aspect2d, pos=(0, 0, 0)
        )
        self.itemHover.hide()
        self.itemHover.setScale(self['hoverFrameScale'])
        self.__itemHoverTaskName = f'ItemFrameGrid-HoverPlacement-{id(self)}'
        self.__hoveredFrame: ItemFrame | None = None
        self.__hoveredFrameOffset = None

        # Create our grids and place them.
        self.itemFrames = [ItemFrame(
            parent=self,
            pos=(0, 0, 0), scale=self['gridScale'],
            easyPadRight=self['gridDistance'],
            easyPadDown=-self['gridDistance'],
            callback=self['callback'],
        ) for _ in range(self['gridWidth'] * self['gridHeight'])]
        if self['scrollbarOrientation'] == DGG.VERTICAL:
            hcount = self['gridWidth']
            vcount = self['gridHeight']
        else:
            hcount = self['gridHeight']
            vcount = self['gridWidth']
        UiHelpers.fillGridWithElements(
            initialGuiList=self.itemFrames,
            horizontalCount=hcount,
            verticalCount=vcount,
            scale=self['gridScale'],
            centering=True,
            centeringOtherAxis=True,
            expandMode=GridType.HorizontalFirst if self['scrollbarOrientation'] == DGG.VERTICAL else GridType.VerticalFirst
        )
        baseItemSpacing = (0.2 + self['gridDistance']) * self['gridScale'] * 0.5
        xdist = baseItemSpacing * self['gridWidth']
        ydist = baseItemSpacing * self['gridHeight']
        self['frameSize'] = (-xdist, xdist, -ydist, ydist)

        # Create the scrollbar.
        self.scrollbar = None
        if self['scrollEnabled']:
            halfBarWidth = self['scrollbarWidth'] / 2
            lengthMult = self['scrollbarLengthMult']
            widthMult = self['scrollbarWidthMult']
            if self['scrollbarOrientation'] == DGG.HORIZONTAL:
                # Horizontal scrollbar - it is on the bottom
                posOffset = Vec3(0, 0, -ydist - (halfBarWidth * widthMult))
                frameSize = (-xdist * lengthMult, xdist * lengthMult,
                             -halfBarWidth * widthMult, halfBarWidth * widthMult)
            else:
                # Vertical scrollbar - it is on the right
                posOffset = Vec3(xdist + (halfBarWidth * widthMult), 0, 0)
                frameSize = (-halfBarWidth * widthMult, halfBarWidth * widthMult,
                             -ydist * lengthMult, ydist * lengthMult)
            self.scrollbar = DirectScrollBar(
                parent=self,
                pos=Vec3(*self['scrollbarPosition']) + posOffset, scale=1.0,
                frameSize = frameSize,
                orientation=self['scrollbarOrientation'],
                scrollSize=1,
                pageSize=1,
                resizeThumb=self['scrollbarThumbResize'],
                command=self._onScroll,
                **self['scrollbarKwargs'],
            )

        # Some quick GUI binding
        self['state'] = DGG.NORMAL
        self.bindToScroll(self)
        self.bindToScroll(self.scrollbar)
        self.bindToScroll(self.scrollbar.thumb)
        self.bindToScroll(self.scrollbar.incButton)
        self.bindToScroll(self.scrollbar.decButton)
        for frame in self.itemFrames:
            frame.bindToScroll(self)
            frame.bind(DGG.ENTER, self.__hoverItemFrame, extraArgs=[frame, True])
            frame.bind(DGG.EXIT, self.__hoverItemFrame, extraArgs=[frame, False])

        # Various state
        self.itemList: List[InventoryItem] = []
        self.currentPage: float = 0.0
        self._previousPageIndex: Optional[int] = None

    def destroy(self):
        self.removeAllTasks()
        self.itemHover.destroy()
        self.itemHover = None
        del self.itemList
        del self.currentPage
        del self._previousPageIndex
        super().destroy()

    def bindToScroll(self, gui):
        gui.bind(DGG.WHEELUP, lambda _: self.scroll(-1))
        gui.bind(DGG.WHEELDOWN, lambda _: self.scroll(1))

    """
    Setters
    """

    def setItemList(self, items: List[InventoryItem]):
        """
        Sets the list of items to be present in the item frame grid.
        """
        self.itemList = items
        self.refresh(force=True)

    def _onScroll(self):
        self.currentPage = self.scrollbar['value']
        self.refresh()

    def refresh(self, force: bool = False):
        """
        Refreshes the visible items within the item frame grid.
        """
        if self._previousPageIndex == self.currentPageIndex and not force:
            # Don't over refresh.
            return

        # Set scroll range.
        if self.scrollbar:
            self.scrollbar['range'] = (0, self.maxPages or 0.001)

        # Set the items in the item box.
        self._previousPageIndex = self.currentPageIndex
        for frame, item in zip(self.itemFrames, self.visibleItems):
            if item:
                frame.setItem(item)
                frame.show()
            else:
                frame.hide()

    """
    Page Management
    """

    def scroll(self, moveIndex):
        self.scrollbar['value'] += moveIndex
        self._onScroll()

    @ignore_event
    def __hoverItemFrame(self, frame: ItemFrame, hovered: bool) -> None:
        self.removeTask(self.__itemHoverTaskName)
        self.itemHover.hide()
        if hovered or (self.__hoveredFrame is not None and frame != self.__hoveredFrame):
            self.__hoveredFrame = frame
            self.itemHover.setItem(frame.item)
            bounds = self.itemHover['frameSize']
            self.__hoveredFrameOffset = [-0.8 * (abs(bounds[0]) + abs(bounds[1]))/2, 0, 0]
            self.addTask(self.__hoverTask, name=self.__itemHoverTaskName)
        else:
            self.__hoveredFrame = None

    def __hoverTask(self, task):
        if not self.__hoveredFrame:
            return task.cont
        if not base.mouseWatcherNode.hasMouse():
            return task.cont

        newPos = getMousePositionWithAspect2d(zmin=-1.0 - (self.itemHover['frameSize'][2]*self['hoverFrameScale'] - 0.05))
        newPos = Point3(newPos[0] + self.__hoveredFrameOffset[0], 0, newPos[2] + self.__hoveredFrameOffset[2])
        self.itemHover.setPos(newPos)
        if self.itemHover.isHidden():
            self.itemHover.show()

        return task.cont

    """
    Various GUI properties
    """

    @property
    def visibleItemCount(self) -> int:
        return self['gridWidth'] * self['gridHeight']

    @property
    def itemCount(self) -> int:
        return len(self.filteredItems)

    @property
    def currentPageIndex(self) -> int:
        """Takes the current page index (based off of the page float)."""
        maxPages = self.maxPages
        if maxPages == 0:
            return 0
        currentPageIndex = math.floor(self.currentPage * ((maxPages + 1) / maxPages))
        if currentPageIndex >= maxPages:
            return maxPages
        return currentPageIndex

    @property
    def filteredItems(self) -> List[InventoryItem]:
        """
        Returns a list of all items to use from the item list.
        """
        return self.itemList

    @property
    def visibleItems(self) -> List[Union[InventoryItem, None]]:
        """
        Returns the number of visible items.
        These are what is rendered within the inventory GUI.
        """
        pageDistance = self['gridHeight' if self['scrollbarOrientation'] == DGG.HORIZONTAL else 'gridWidth']
        itemsScrolled = pageDistance * self.currentPageIndex
        items: List[Union[InventoryItem, None]] = self.filteredItems[itemsScrolled : itemsScrolled + self.visibleItemCount]
        items.extend([None] * (self.visibleItemCount - len(items)))
        return items

    @property
    def maxPages(self) -> int:
        """
        Returns the number of max "pages" in the grid,
        i.e. the number of rows/columns offscreen.
        """
        # How many offscreen items are there?
        offscreenItems = max(0, self.itemCount - self.visibleItemCount)
        if offscreenItems == 0:
            # No items are offscreen, only one page exists.
            return 0

        # Figure out how many offscreen rows/columns there are.
        if self['scrollbarOrientation'] == DGG.HORIZONTAL:
            return 1 + ((offscreenItems - 1) // self['gridHeight'])
        else:
            return 1 + ((offscreenItems - 1) // self['gridWidth'])


if __name__ == "__main__":
    from toontown.inventory.enums.ItemEnums import ChatStickersItemType
    gui = ItemFrameGrid(
        parent=aspect2d,
        gridWidth=8,
        gridHeight=5,
        gridDistance=0.04,
        gridScale=1.1,
        # scrollbarOrientation=DGG.HORIZONTAL,
        scrollbarWidth=0.12,
    )
    gui.setItemList(
        [
            InventoryItem.fromSubtype(subtype)
            for subtype in ChatStickersItemType
        ] * 3
    )
    base.run()
