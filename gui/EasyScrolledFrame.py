from toontown.gui import UiHelpers
from toontown.utils.InjectorTarget import InjectorTarget

if __name__ == "__main__":
    from tools.headless.headlessbase import HeadlessStart
    from tools.headless.headlessbase.HeadlessBase import HeadlessBase
    base = HeadlessBase(wantHotkeys=False)
    if __debug__:
        from toontown.utils.DeveloperInjector import startInjector
        startInjector()

from toontown.gui.TTGui import kwargsToOptionDefs
from toontown.gui.DirectScrolledFrameNoHorizontal import DirectScrolledFrameNoHorizontal
from toontown.gui.GUITemplateSliders import GUITemplateSliders
from toontown.gui.EasyManagedItem import EasyManagedItem
from toontown.gui.UiHelpers import gui_update
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from direct.gui.DirectGui import *

from typing import List


@DirectNotifyCategory()
class EasyScrolledFrame(DirectScrolledFrameNoHorizontal):
    """
    Are you endlessly tired of managing your scrollbar?
    Then this is the class for you!

    EasyScrolledFrames are designed to easily manage vertically
    scrolled lists, along with keeping track of the items inside the frame.

    All you have to do is create an EasyScrolledFrame, and then
    insert EasyScrolledItems (designed to be subclassed).
    The canvas size will be managed automatically.

    This class is not designed with a horizontal scroll.
    """

    @InjectorTarget
    def __init__(self, parent, **kw):
        # GUI boilerplate.
        optiondefs = kwargsToOptionDefs(
            # Some default overrides over the DirectScrolledFrame.
            # It is best to not touch these unless you know what you're doing.
            # P.S. You probably don't
            autoHideScrollBars=False,
            manageScrollBars=False,

            # A debug mode, overriding item's reliefs/framesizes/framecolors and making them visible.
            debug=False,

            # Arguments to modify scroll bar functionality.
            thumbChangesSize=False,                   # Should the scroll thumb size dynamically with the frame?
                                                      # If this is True, the thumbHeight is used as a coefficient
                                                      # for the amount the thumb should change size by.
            thumbHeight=[0.18, self.setThumbHeight],  # If not, set the thumb height explicitly.
            scrollBarWidth=0.08,                      # Set the width of the scroll bar.
            hasIncButton=False,                       # Do we have an inc button?
            hasDecButton=False,                       # Do we have a dec button?
            scrollBarPosOffset=[(0, 0, 0), self.manageScrollBars],  # Positional offset for the scrollbar.
            scrollBarScale=[1.0, self.manageScrollBars],            # Scale of the scrollbar.

            # Things to hide if there's not enough items to warrant scrolling.
            hideScroll=False,  # Does the whole scrollbar get hidden? (Includes thumb/inc/dec)
            hideThumb=False,   # Does the thumb get hidden?
            hideInc=False,     # Does the inc button get hidden?
            hideDec=False,     # Does the dec button get hidden?

            # Enable the clipping plane, clipping the entire frame.
            # If this is disabled, clipping must be done manually.
            clipFrame=True,
            clipScroll=True,

            # Things that manage item placements.
            itemStartPosition=[None, self.updateItemPositions],
            itemScale=[1.0, self.updateItemPositions],  # Sets the scales of the internal item frame
            horizontalCentering=False,  # Items get horizontally centered from the start position

            # Things that manage the canvas size.
            forcedHeight=[None, self.updateItemPositions],  # Does the canvas size have a currently-enforced height?
                                                            # Note that it will still be bounded by the screen height.

            # Scroll wheel arguments.
            enableScrollWheel=True,
            scrollDistance=0.1,
            scrollCondition=True,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)

        # Get references to parts of the scroll bar.
        self.thumb = self.verticalScroll.thumb
        self.incButton = self.verticalScroll.incButton
        self.decButton = self.verticalScroll.decButton

        # Keep up with some things.
        self.canvasItems = []
        self.clipPlanes = []

        # Do some great initialization.
        self._initScrollBar()
        self._initClipPlanes()
        self._initScroll()

        # Let canvas size match frame size.
        self.manageCanvasSize(newHeight=0.0)

        # Initialize the options.
        self.initialiseoptions(EasyScrolledFrame)

    def destroy(self):
        # Clean up references.
        self.thumb = None
        self.incButton = None
        self.decButton = None
        self.canvasItems = []

        # Clean up clipping planes.
        for planeNode in self.clipPlanes:
            planeNode.removeNode()
        self.clipPlanes = []

        # Now fully clean up. This cleans up canvasItems too.
        super().destroy()

    """
    Methods during initialization
    """

    def _initScrollBar(self):
        """
        Do some initialization steps specifically on the scroll bar.
        """
        if not self['manageScrollBars']:
            # Disable the ScrollBar's default positioning management.
            self.verticalScroll['manageButtons'] = 0
            self.verticalScroll['resizeThumb'] = 0

        # Attempt to nuke the inc/dec buttons.
        if not self['hasIncButton']:
            self.incButton.destroy()
            self.incButton = None

        if not self['hasDecButton']:
            self.decButton.destroy()
            self.decButton = None

    def _initClipPlanes(self):
        """
        Makes a list of clip planes.

        :return: Returns Left, Right, Down, and Up planes.
        """
        for i, plane in enumerate([
                (1, 0, 0),
                (-1, 0, 0),
                (0, 0, 1),
                (0, 0, -1),
            ]):
            clippingPlane = PlaneNode(f'{self.uniqueName("clippingPlane")}-{i}')
            clippingPlane.setPlane(Plane(Vec3(*plane), Point3(0, 0, 0)))
            clipNP = self.attachNewNode(clippingPlane)
            # clipNP.show()
            self.clipPlanes.append(clipNP)

        # Clip ourselves if we so desire.
        if self['clipFrame']:
            self.setToClip(self)
        if self['clipScroll']:
            self.setToClip(self.verticalScroll)

    def _initScroll(self):
        # Binds several elements to scroll.
        self['state'] = DGG.NORMAL
        self.bindToScroll(self)
        self.bindToScroll(self.verticalScroll)
        self.bindToScroll(self.thumb)
        if self.incButton:
            self.bindToScroll(self.incButton)
        if self.decButton:
            self.bindToScroll(self.decButton)

    """
    Position management
    """

    def manageAll(self):
        self.manageScrollBars()
        self.manageClippingPlanes()

    def manageCanvasSize(self, newHeight: float):
        """Updates the canvas size to match a new height."""
        if self['forcedHeight'] is not None:
            newHeight = self['forcedHeight']
        frameLeft, frameRight, frameDown, frameUp = self['frameSize']
        scrollBarWidth = self['scrollBarWidth']
        self['canvasSize'] = (frameLeft, frameRight - scrollBarWidth, min(frameDown, frameUp + newHeight), frameUp)

    def manageScrollBars(self):
        """
        This method moves all of the scroll bars into place.
        We do this manually to avoid mysterious issues with the automatic placer.
        """
        frameLeft, frameRight, frameDown, frameUp = self['frameSize']
        thumbHeight = self['thumbHeight']
        scrollBarWidth = self['scrollBarWidth']

        frameHeight = self.getFrameHeight()
        canvasHeight = self.getCanvasHeight()

        # Figure out if we need to dynamically address thumb size.
        if self['thumbChangesSize'] and canvasHeight and (canvasHeight > frameHeight):
            # We multiply:
            #  - The actual region that the thumb can be inside.
            #  - The % size of the visible region in the frame.
            #  - The current thumbHeight, used as a coefficient.
            # to get the new thumbHeight.
            thumbHeight = (frameHeight - scrollBarWidth * 2) \
                        * (frameHeight / canvasHeight) \
                        * thumbHeight

        # Make all the scrollbar elements visible.
        self.verticalScroll.show()
        self.thumb.show()
        if self.incButton:
            self.incButton.show()
        if self.decButton:
            self.decButton.show()

        # Hide specific scrollbar elements if we're being demanded to.
        if frameHeight >= canvasHeight:
            # The frame height is greater than/equal to the canvas height.
            # Therefore, there is no reason to show certain scroll elements.
            attrToItem = {
                'hideScroll': self.verticalScroll,
                'hideThumb': self.thumb,
                'hideInc': self.incButton,
                'hideDec': self.decButton,
            }
            for attr, item in attrToItem.items():
                # If the item is destroyed, don't bother.
                if not item:
                    continue
                # If we want the item hidden, hide it.
                if self[attr]:
                    item.hide()

        # Now, we update the positions of the GUI.
        x, y, z = self['scrollBarPosOffset']
        gui_update(
            self.verticalScroll,
            pos=(frameRight - (scrollBarWidth / 2) + x, y, z),
            frameSize=(-scrollBarWidth / 2, scrollBarWidth / 2, frameDown, frameUp),
            scale=self['scrollBarScale'],
        )
        gui_update(
            self.thumb,
            frameSize=(-scrollBarWidth / 2, scrollBarWidth / 2,
                       -thumbHeight / 2, thumbHeight,)
        )
        if self.decButton:
            gui_update(
                self.decButton,
                pos=(0, 0, frameUp - (scrollBarWidth / 2)),
                frameSize=(-(scrollBarWidth / 2), scrollBarWidth / 2,
                           -(scrollBarWidth / 2), scrollBarWidth / 2)
            )
        if self.incButton:
            gui_update(
                self.incButton,
                pos=(0, 0, frameDown + (scrollBarWidth / 2)),
                frameSize=(-(scrollBarWidth / 2), scrollBarWidth / 2,
                           -(scrollBarWidth / 2), scrollBarWidth / 2)
            )

    def manageClippingPlanes(self):
        # Update the positions of the clipping planes.
        if not self.clipPlanes:
            return
        frameLeft, frameRight, frameDown, frameUp = self['frameSize']
        planeLeft, planeRight, planeDown, planeUp = self.clipPlanes
        planeLeft.setPos(frameLeft, 0, 0)
        planeRight.setPos(frameRight, 0, 0)
        planeDown.setPos(0, 0, frameDown)
        planeUp.setPos(0, 0, frameUp)

    """
    Item Adding
    """

    def addItem(self, item: EasyManagedItem, index: int = None):
        """
        Adds an item into the EasyScrolledFrame.

        After all items are added, call self.updateItemPositions().
        We don't call it in this method because that can be very slow.

        :param item: The item to add into the frame.
        :param index: The index to add the EMI to. Can pass in a callable.
        """
        item.reparentTo(self.getCanvas())
        if index is None:
            self.canvasItems.append(item)
        else:
            if callable(index):
                index = index()
            self.canvasItems.insert(index, item)
        item.bindToScroll(self)

    def removeItem(self, item: EasyManagedItem):
        """
        Removes an item from the EasyScrolledFrame.
        """
        if item in self.canvasItems:
            self.canvasItems.remove(item)

    def removeAllItems(self):
        """Removes all items."""
        for item in self.canvasItems:
            item.destroy()
        self.canvasItems = []

    """
    Item Positioning
    """

    def updateItemPositions(self):
        """
        Updates all canvas items (EasyScrolledItems).
        Currently, this only works for the top left of the canvas, unless overriden.
        """
        if self['itemStartPosition'] is None:
            xstart, zstart = self.getTopLeftOfCanvas()
        else:
            xstart, _, zstart = self['itemStartPosition']
        xoffset, zoffset = 0.0, 0.0
        maxzoffset = []
        rowWidth = 0.0
        itemsInRow = []
        scale = self['itemScale']
        debugMode = self['debug']

        # Start positioning items.
        canvasItems = self.getCanvasItems()
        for item in canvasItems:
            # Skip this item if it is inactive.
            if not item.isActivelyPositioned():
                continue

            # Add this item to the row.
            itemsInRow.append(item)

            # Calculate the new xpos for this item.
            xoffset += item.getEasyPadLeft() * scale

            # Apply the up padding if this is the first item in the row.
            if rowWidth == 0:
                zoffset += item.getEasyPadUp() * scale

            # Place this item.
            itemxoffset, itemyoffset, itemzoffset = item.cget('posOffset')
            item.setPos(xstart + xoffset + itemxoffset,
                        itemyoffset,
                        zstart + zoffset + itemzoffset)

            # Set frame size on the item in debug mode.
            if debugMode:
                item.enableDebug()

            # Apply the width and right padding, increment the items in row
            xoffset += item.getEasyWidth() * scale
            xoffset += item.getEasyPadRight() * scale
            rowWidth += item.getEasyItemCount()

            # We will move down by the "tallest" item present in this entire row.
            maxzoffset.append((item.getEasyHeight() + item.getEasyPadDown()) * scale)

            # If we are at the end of the row, apply new positions.
            # This also occurs if this is the last item.
            if rowWidth >= item.getEasyXMax() or item is canvasItems[-1]:
                # Center align if we are asked to.
                if self['horizontalCentering'] and itemsInRow:
                    UiHelpers.placeElementsInHorizontalLine(
                        guiList=itemsInRow,
                        startPos=itemsInRow[0].getPos(),
                        alignCenter=True,
                    )

                # OK, we've reached the end of the row;
                # We burn over into the next row now.
                zoffset += min(maxzoffset)
                xoffset = 0.0
                maxzoffset = []
                itemsInRow = []
                rowWidth = 0.0

        # We note that the zoffset is now the total height of the canvas,
        # so we're going to go ahead and update the canvas size.
        self.manageCanvasSize(zoffset)

        # After item positions are updated, we ask the canvas size to update.
        self.manageAll()

    """
    Attribute setters
    """

    def setFrameSize(self, fClearFrame = 0):
        # Changing the frame size requires us to update the scroll bar.
        super().setFrameSize(fClearFrame=fClearFrame)
        self.manageAll()

    def setCanvasSize(self):
        # Changing the canvas size requires us to update the scroll bar.
        super().setCanvasSize()
        self.manageAll()

    def setThumbHeight(self):
        # Changing the thumb height requires us to update the scroll bar.
        self.manageAll()

    def setScrollBarWidth(self):
        # Changing the scrollbar width requires us to update the scroll bar.
        super().setScrollBarWidth()
        self.manageAll()

    """
    Scroll functionality
    """

    def scroll(self, direction):
        if not self['enableScrollWheel']:
            return
        if self['scrollCondition'] is True or (callable(self['scrollCondition']) and self['scrollCondition']() is True):
            scrollPercent = self['scrollDistance'] / abs(self['canvasSize'][2] - self['canvasSize'][3])
            self['verticalScroll_value'] = self['verticalScroll_value'] + scrollPercent * direction

    """
    Object setters
    """

    def setToClip(self, gui):
        for clipNP in self.clipPlanes:
            gui.setClipPlane(clipNP)

    def bindToScroll(self, gui):
        gui.bind(DGG.WHEELUP, lambda _: self.scroll(-1))
        gui.bind(DGG.WHEELDOWN, lambda _: self.scroll(1))

    """
    Useful frame getters
    """

    def getCanvasItems(self):
        """:rtype: List[EasyManagedItem]"""
        return self.canvasItems

    def getTopLeftOfCanvas(self) -> tuple:
        """Returns the top left of the canvas (X/Z)."""
        left, right, down, up = self['canvasSize']
        return left, up

    def getFrameHeight(self, makeAbsolute=True):
        """Returns the height of the frame."""
        left, right, down, up = self['frameSize']
        return abs(up - down) if makeAbsolute else (up - down)

    def getCanvasHeight(self, makeAbsolute=True):
        """Returns the height of the canvas."""
        left, right, down, up = self['canvasSize']
        return abs(up - down) if makeAbsolute else (up - down)


if __name__ == "__main__":
    gui = EasyScrolledFrame(
        parent=aspect2d,
        # any kwargs go here
    )
    import random
    for _ in range(60):
        EasyManagedItem(
            frameSize=(0, 0.2, -0.2, 0),
            frameColor=(random.random(), random.random(), random.random(), 1),
            easyWidth=0.2,
            easyHeight=-0.2,
            easyPadLeft=0.05,
            easyPadRight=-0.05,
            easyPadDown=0.05,
            easyPadUp=-0.05,
            easyScrolledFrame=gui,
            easyXMax=4.0,
        )
    gui.updateItemPositions()
    base.run()
