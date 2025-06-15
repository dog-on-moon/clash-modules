import time

if __name__ == "__main__":
    from tools.headless.headlessbase import HeadlessStart
    from tools.headless.headlessbase.HeadlessBase import HeadlessBase
    base = HeadlessBase(wantHotkeys=False)
    if __debug__:
        from toontown.utils.DeveloperInjector import startInjector
        startInjector()
    # base.initCR()  # defines base.cr
    # base.startHeadlessShow()

from toontown.gui.TTGui import kwargsToOptionDefs, OnscreenTextOutline, LiveLockingEntry
from toontown.gui.GUITemplateSliders import GUITemplateSliders
from toontown.gui.GUINode import GUINode
from toontown.gui import UiHelpers
from toontown.gui.EasyManagedItem import EasyManagedItem
from toontown.gui.EasyManagedButton import EasyManagedButton
from toontown.gui.EasyScrolledFrame import EasyScrolledFrame
from toontown.gui.ScaledFrame import ScaledFrame
from toontown.gui.GUIPositionGlobals import ScreenCorner
from toontown.gui.Bounds import Bounds
from toontown.gui.CornerAnchor import CornerAnchor
from toontown.toon.gui import GuiBinGlobals
from toontown.inventory.enums import RarityEnums
from toontown.inventory.gui.player.InventoryFilterWidget import InventoryFilterWidget
from toontown.inventory.gui.general.ItemFrameGrid import ItemFrameGrid
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.InjectorTarget import InjectorTarget
from toontown.inventory.base.Inventory import Inventory
from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.gui.player.preview.InventoryPreviewPanel import InventoryPreviewPanel
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from typing import Optional, List, Tuple
import random


@DirectNotifyCategory()
class InventoryViewerPanel(DirectFrame, Bounds):
    """
    A large panel used for viewing the contents of a given Inventory.

    This GUI heirarchy is a little complex, so I'll take some time to explain it.

                            InventoryViewerPanel
            | (Left Side)                           | (Right Side)
            InventoryPreviewPanel                   1) ItemFrameGrid (for listing and rendering the items)
            (Contains a subclass of                 2) Misc elements (label text, searchbar, filter button)
            InventoryBaseItemPreview,               3) InventoryFilterWidget (the actual filter GUI component)
            which renders items on
            the InventoryPreviewPanel)
    """

    ITEM_CLICK_DEBOUNCE = 0.1

    @InjectorTarget
    def __init__(self, parent=aspect2d, **kw):
        # GUI boilerplate.
        optiondefs = kwargsToOptionDefs(
            pos = (0, 0, 0),
            scale = 1.0,
            wantClipping=False,

            labelTextScale=0.08,
            frameHeight=0.1,

            gridWidth=6,
            gridHeight=4,
            gridDistance=0.055,
            gridScale=1.01,

            scrollbarXOffset=0.04,
            scrollbarWidth=0.1,

            searchbarPos = (-0.68837, 0.0, -0.06006),
            searchbarScale = 0.07795,
            searchbarWidth = 10.0,

            panelDistance = [0.13236, self.place],
            panelWidth = [0.68248, self.place],

            isLocalInventory=False,
            inventory=None,
            startVisible=False,
            # relief = None,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.postInitialized = False
        self.postInitialiseFuncList.append(lambda: setattr(self, 'postInitialized', True))
        self.initialiseoptions(InventoryViewerPanel)
        self.setBin('sorted-gui-popup', GuiBinGlobals.ItemFrameBin - 2)

        # GUI prototypes.
        self.centeredNode: Optional[GUINode] = None
        self.frame: Optional[ScaledFrame] = None
        self.frame_corner_topLeft: Optional[CornerAnchor] = None
        self.frame_corner_topRight: Optional[CornerAnchor] = None
        self.itemFrameGrid: Optional[ItemFrameGrid] = None
        self.text_category: Optional[OnscreenTextOutline] = None
        self.type_searchBar: Optional[LiveLockingEntry] = None
        self.filterButton: Optional[DirectButton] = None
        self.filterWidget: Optional[InventoryFilterWidget] = None
        self.previewPanel: Optional[InventoryPreviewPanel] = None

        # Hold state.
        self.item: Optional[InventoryItem] = None
        self.inventory: Optional[Inventory] = None
        self.searchQuery: str = ''
        self._animation: Optional[Sequence] = None
        self._itemChangedLast: float = 0.0

        # Call these two.
        self._create()
        self.place()

        # Misc things
        self.accept('mouse1-up', lambda: self.onRegularMousePress())
        if not self['startVisible']:
            self.hide()
        if self['isLocalInventory']:
            self.accept('newLocalInventory', self.setInventory)
            if base.cr and base.cr.inventoryManager and base.cr.inventoryManager.getInventory():
                self.setInventory(base.cr.inventoryManager.getInventory())
        elif self['inventory']:
            self.setInventory(self['inventory'])

    def destroy(self):
        if self._animation:
            self._animation.finish()
            self._animation = None
        if self.inventory:
            # self.inventory.cleanup()
            del self.inventory
        del self.item
        self.ignoreAll()
        super().destroy()

    def _create(self):
        # Make the frame and corners.
        self.centeredNode = GUINode(parent=self)
        self.frame = ScaledFrame(
            parent=self.centeredNode, pos=(0, 0, 0), scale=1.0,
        )
        self.frame_corner_topLeft  = CornerAnchor(parent=self.frame, corner=ScreenCorner.TOP_LEFT)
        self.frame_corner_topRight = CornerAnchor(parent=self.frame, corner=ScreenCorner.TOP_RIGHT)

        # The item frame grid.
        self.itemFrameGrid = ItemFrameGrid(
            parent=self.frame,
            gridWidth=self['gridWidth'],
            gridHeight=self['gridHeight'],
            gridDistance=self['gridDistance'],
            gridScale=self['gridScale'],
            scrollbarPosition=(self['scrollbarXOffset'], 0, 0),
            scrollbarWidth=self['scrollbarWidth'],
            callback=self.onItemSelected,
        )

        # Category text.
        midHeight = -(0.0021 * (self['labelTextScale'] * 100)) - (self['frameHeight'] / 2)
        self.text_category = OnscreenTextOutline(
            parent=self.frame_corner_topLeft,
            pos=(0.015, midHeight),
            scale=self['labelTextScale'],
            text='Hammerspace',
            align=TextNode.ALeft,
            text_dist=0.008,
            precision=12,
            outline_fg=(0.129, 0.525, 0.318, 1.0),
            fg=(1, 1, 1, 1),
        )

        # Make the searchbar.
        self.type_searchBar = LiveLockingEntry(
            parent=self.frame_corner_topRight, relief=DGG.FLAT,
            pos=self['searchbarPos'], scale=self['searchbarScale'],
            borderWidth=(0.05, 0.05),
            frameColor=(0.7, 0.7, 0.7, 1.0), state=DGG.NORMAL,
            text_align=TextNode.ALeft, text_scale=0.7, width=self['searchbarWidth'], numLines=1,
            focus=0, backgroundFocus=0, cursorKeys=1, text_fg=(0, 0, 0, 1), suppressMouse=1, autoCapitalize=0,
            initialText='Search...', clearOnFocus=True,
            callback=self.setSearchQuery,
        )

        # The filter menu.
        self.filter = InventoryFilterWidget(
            parent=self.frame_corner_topRight,
            callback=self.onFilterUpdate,
            labelPos=(-0.12934, 0.0, -0.07055),
        )
        self.filter.hide()

        def toggleFilterVisibility():
            if self.filter.isHidden():
                self.filter.show()
            else:
                self.filter.hide()

        # And the filter dropdown button.
        self.filterButton = DirectButton(
            parent=self.frame_corner_topRight,
            pos=(0, 0, 0), scale=1.0,
            frameSize=(-1, 1, -1, 1),
            command=toggleFilterVisibility,
        )
        self.filterButton.setBin('sorted-gui-popup', GuiBinGlobals.ItemFrameBin + 3)

        # Preview panel.
        self.previewPanel = InventoryPreviewPanel(
            parent=self.frame_corner_topLeft,
            frameSize=(-1, 1, -1, 1),
        )

    def place(self):
        if not self.postInitialized:
            return
        # Calculate the frame's frameSize.
        fLeft, fRight, fDown, fUp = self.itemFrameGrid['frameSize']
        fUp = fUp + self['frameHeight']
        self.frame['frameSize'] = (
            fLeft,
            fRight + self['scrollbarXOffset'] + self['scrollbarWidth'],
            fDown, fUp
        )
        self.frame_corner_topLeft.place()
        self.frame_corner_topRight.place()

        # Place the filter button.
        self.filterButton.setPos(- (self['scrollbarWidth'] / 2), 0, - (self['frameHeight'] / 2))
        self.filterButton['frameSize'] = (-self['scrollbarWidth'] / 2, self['scrollbarWidth'] / 2,
                                          -self['searchbarScale'] / 2, self['searchbarScale'] / 2)
        self.filter['frameSize'] = (-0.8, 0, -1, 0)

        # Place the preview panel.
        self.previewPanel.setPos(-self['panelDistance'], 0, 0)
        self.previewPanel['frameSize'] = (-self['panelWidth'], 0, fDown - fUp, 0)
        self.previewPanel.place()

        # Depending on the width of the preview panel, we need to "center" this GUI.
        panelWidth = self['panelWidth'] + self['panelDistance']
        self.centeredNode.setPos(panelWidth / 2, 0, 0)

    """
    Visual Sequences
    """

    def animatePopIn(self) -> None:
        if self._animation:
            self._animation.finish()
            self._animation = None

        def _setPreviewWidth(t):
            self['panelWidth'] = t

        animSpeed = 5
        self._animation = Parallel(
            # Initialize.
            Sequence(
                Func(self.show),
            ),
            # The frame scaling sequence.
            Sequence(
                LerpScaleInterval(self, 1.00 / animSpeed, scale=1.033, startScale=0.010, blendType='easeInOut'),
                LerpScaleInterval(self, 0.50 / animSpeed, scale=1.000, startScale=1.033, blendType='easeInOut'),
            ),
            # The preview panel expansion.
            Sequence(
                Func(_setPreviewWidth, 0.01),
                Wait(0.50 / animSpeed),
                LerpFunctionInterval(
                    _setPreviewWidth,
                    duration=1.25 / animSpeed,
                    fromData=0.01,
                    toData=self['panelWidth'],
                    blendType='easeOut',
                )
            ),
        )
        self._animation.start()

    def animatePopOut(self) -> None:
        if self._animation:
            self._animation.finish()
            self._animation = None

        animSpeed = 5
        self._animation = Sequence(
            Parallel(
                # The frame scaling sequence.
                LerpScaleInterval(self, 1.00 / animSpeed, scale=0.010, startScale=1.033, blendType='easeIn'),
            ),
            Sequence(
                # Cleanup
                Func(self.setScale, 1.0),
                Func(self.hide),
            )
        )
        self._animation.start()

    """
    Setters
    """

    def setInventory(self, inventory: Inventory):
        """
        Sets the inventory associated with this GUI.
        """
        self.inventory = inventory
        self.refresh()

    """
    GUI rendering
    """

    def refresh(self):
        self.itemFrameGrid.setItemList(self.getVisibleItems())

    def onFilterUpdate(self):
        self.refresh()

    def getVisibleItems(self) -> List[InventoryItem]:
        """Gets a list of all visible items."""
        if not self.inventory:
            return []

        # Update the item filter.
        self.filter.setItems(self.inventory.getItems())

        # Use these sorted items.
        items = self.filter.getSortedItems()

        # Filter items by name.
        if self.searchQuery:
            newItems = []
            for item in items:
                fieldsToQuery = [
                    # Item Name
                    item.getItemDefinition().getName(item).lower().replace(' ', ''),
                    # Item Type Name
                    item.getItemDefinition().getItemTypeName().lower().replace(' ', ''),
                    # Item Rarity
                    RarityEnums.getItemRarityName(item).lower().replace(' ', ''),
                ]
                for field in fieldsToQuery:
                    if self.searchQuery in field:
                        newItems.append(item)
                        break
            items = newItems

        # Return all sorted, filtered, and searched items.
        return items

    """
    Item clicking functionality
    """

    def onItemSelected(self, item: Optional[InventoryItem]):
        """Called when any item box is clicked."""
        # Set state.
        self.item = item
        self._itemChangedLast = time.time()

        # Change the preview panel to fit.
        self.previewPanel.setItem(item)

    def onRegularMousePress(self):
        """Called on any regular ol mouse click."""
        # Do not engage if the mouse is in a dangerous position.
        if self.previewPanel.isMouseWithinBounds():
            return

        # Debounce the call in case a regular item was selected.
        if time.time() < (self._itemChangedLast + self.ITEM_CLICK_DEBOUNCE):
            return

        # Select none.
        self.onItemSelected(None)

    """
    Search entry work
    """

    def setSearchQuery(self, text):
        self.searchQuery = text.lower().replace(' ', '')
        self.refresh()


if __name__ == "__main__":
    gui = InventoryViewerPanel(
        scale=1.0,
        startVisible=True,
        # any kwargs go here
    )

    def setNewItemList():
        from toontown.inventory.enums.ItemEnums import ChatStickersItemType, NametagFontItemType, NameplateItemType, BackgroundItemType
        crazyItemList = [
            InventoryItem.fromSubtype(subtype)
            for itemtype in [ChatStickersItemType, NametagFontItemType, NameplateItemType, BackgroundItemType]
            for subtype in itemtype
        ]
        crazyItemList = crazyItemList[0:10 + (round((len(crazyItemList) - 10) * random.random()))]
        equippedIDs = [invItem.getItemID() for invItem in random.sample(crazyItemList, len(crazyItemList) // 7)]

        from toontown.inventory.enums.ItemAttribute import ItemAttribute
        from toontown.inventory.enums.ItemModifier import ItemModifier
        for item in crazyItemList:
            if random.random() < 0.3:
                item.setAttribute(ItemAttribute.MODIFIER, ItemModifier.STICKER_FOIL)
            elif random.random() < 0.6:
                item.setAttribute(ItemAttribute.MODEL_COLORSCALE,
                                  (random.random(), random.random(),
                                   random.random(), 0.5))

        from toontown.inventory.enums.InventoryEnums import InventoryType
        gui.setInventory(
            Inventory(
                inventoryType=InventoryType.FullBehavior,
                equippedItemIDs=equippedIDs,
                items=crazyItemList,
            )
        )
    setNewItemList()
    base.accept('a', setNewItemList)
    base.accept('n', gui.animatePopIn)
    base.accept('m', gui.animatePopOut)
    # GUITemplateSliders(
    #     gui,
    #     'pos', 'scale', 'panelWidth', 'panelDistance',
    # )
    base.run()
