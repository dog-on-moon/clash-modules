if __name__ == "__main__":
    from tools.headless.headlessbase import HeadlessStart
    from tools.headless.headlessbase.HeadlessBase import HeadlessBase
    base = HeadlessBase(wantHotkeys=False)
    if __debug__:
        from toontown.utils.DeveloperInjector import startInjector
        startInjector()
    # base.initCR()  # defines base.cr
    # base.startHeadlessShow()

from toontown.inventory.enums import RarityEnums
from toontown.gui.TTGui import kwargsToOptionDefs, OnscreenTextOutline, LiveLockingEntry
from toontown.gui.GUITemplateSliders import GUITemplateSliders
from toontown.gui.GUINode import GUINode
from toontown.gui.CornerAnchor import CornerAnchor
from toontown.gui import UiHelpers
from toontown.gui.EasyManagedItem import EasyManagedItem
from toontown.gui.EasyManagedButton import EasyManagedButton
from toontown.gui.EasyScrolledFrame import EasyScrolledFrame
from toontown.gui.ScaledFrame import ScaledFrame
from toontown.gui.GUIPositionGlobals import ScreenCorner
from toontown.gui.Bounds import Bounds
from toontown.gui.DirectScrollableOptionMenu import DirectScrollableOptionMenu
from toontown.toon.gui import GuiBinGlobals
from toontown.inventory.enums.ItemTags import ItemCategory, DefaultItemCategory, GlobalItemCategory, ItemTag, ItemFilterType
from toontown.inventory.gui.player.InventoryFilterSortButtons import InventoryFilterSortButtons
from toontown.inventory.gui.general.ItemFrameGrid import ItemFrameGrid
from toontown.inventory.gui.player.ItemTagSelectorFrame import ItemTagSelectorFrame
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.InjectorTarget import InjectorTarget
from toontown.inventory.base.Inventory import Inventory
from toontown.inventory.base.InventoryItem import InventoryItem
from direct.gui.DirectGui import *
from typing import Optional, List, Set
import random


@DirectNotifyCategory()
class InventoryFilterWidget(ScaledFrame, Bounds):
    """
    A GUI widget that allows filter settings to be specified on items.
    """

    @InjectorTarget
    def __init__(self, parent, **kw):
        # GUI boilerplate.
        optiondefs = kwargsToOptionDefs(
            pos = (0, 0, 0),
            scale = 1.0,
            frameSize=(-0.4, 0.4, -0.6, 0.6),
            bin=GuiBinGlobals.ItemFrameBin + 2,
            labelPos=[(-0.02352, 0.0, -0.07055), self.place],
            labelScale=[0.0877, self.place],
            categoryPos=[(0.01764, 0.0, -0.06467), self.place],
            categoryScale=[0.07114, self.place],
            sortButtonsPos=[(0, 0, -0.13325), self.place],
            sortButtonsScale=[0.47286, self.place],
            tagsPadding=[0.0, self.place],
            tagsHeadroom=[0.1823, self.place],

            callback=None,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.initialiseoptions(InventoryFilterWidget)
        self.setBin('sorted-gui-popup', self['bin'])

        self.items: List[InventoryItem] = []

        self.corner_topRight: Optional[CornerAnchor] = None
        self.corner_topLeft: Optional[CornerAnchor] = None
        self.corner_topCenter: Optional[CornerAnchor] = None
        self.text_label: Optional[DirectLabel] = None
        self.dropdown_category: Optional[DirectScrollableOptionMenu] = None
        self.sortButtons: Optional[InventoryFilterSortButtons] = None
        self.itemTagFrame: Optional[ItemTagSelectorFrame] = None

        self._create()
        self.place()

    def _create(self):
        self.corner_topRight  = CornerAnchor(self, ScreenCorner.TOP_RIGHT)
        self.corner_topLeft   = CornerAnchor(self, ScreenCorner.TOP_LEFT)
        self.corner_topCenter = CornerAnchor(self, ScreenCorner.TOP_MIDDLE)
        self.text_label = DirectLabel(
            parent=self.corner_topRight, relief=None,
            text='Filter', text_align=TextNode.ARight,
            pos=(0, 0, 0), scale=1.0,
        )
        self.dropdown_category = DirectScrollableOptionMenu(
            parent=self.corner_topLeft,
            items=list(ItemCategory),
            initialitem=DefaultItemCategory,
            command=self.onCategoryChange,
            pos=(0, 0, 0), scale=1.0,
        )
        self.sortButtons = InventoryFilterSortButtons(
            parent=self.corner_topCenter,
            callback=self['callback'],
            pos=(0, 0, 0), scale=1.0,
        )
        self.itemTagFrame = ItemTagSelectorFrame(
            parent=self.corner_topLeft,
            callback=self['callback'],
            pos=(0, 0, 0), scale=1.0,
        )

    def place(self):
        if not hasattr(self, 'text_label'):
            return
        self.corner_topRight.place()
        self.corner_topLeft.place()
        self.corner_topCenter.place()
        self.text_label.setPos(self['labelPos'])
        self.text_label.setScale(self['labelScale'])
        self.dropdown_category.setPos(self['categoryPos'])
        self.dropdown_category.setScale(self['categoryScale'])
        self.sortButtons.setPos(self['sortButtonsPos'])
        self.sortButtons.setScale(self['sortButtonsScale'])
        UiHelpers.gui_update(
            self.itemTagFrame,
            frameSize=(
                0,
                self.getBoundWidth(),
                -self.getBoundHeight(),
                -self['tagsHeadroom']),
        )

    def destroy(self):
        del self.items
        super().destroy()

    def setFrameSize(self, fClearFrame = 0):
        super().setFrameSize(fClearFrame)
        self.place()

    def update(self):
        self.itemTagFrame.setItems(self.getItemsInCurrentCategory())

    def onCategoryChange(self, _=None):
        self.update()
        self.callback()

    def callback(self):
        if self['callback']:
            self['callback']()

    """
    Actions
    """

    def setItems(self, items: List[InventoryItem]):
        if (len(items) != len(self.items)) or (items != self.items):
            self.items = items
            self.update()

    def getItemsInCurrentCategory(self) -> List[InventoryItem]:
        """
        Gets the items in the current category.
        """
        category = self.dropdown_category.get()
        if category == GlobalItemCategory:
            # All items are fine.
            return self.items
        else:
            # Filter based on items that match the category.
            return [
                item for item in self.items
                if item.getItemDefinition().getItemCategory() == category
            ]

    def getFilteredItems(self) -> List[InventoryItem]:
        """
        Gets all items that have been completely filtered.
        """
        items = self.getItemsInCurrentCategory()
        tags: Set[ItemTag] = self.itemTagFrame.getSelectedTags()

        # If no tags selected, passthrough.
        if not tags:
            return items

        # Filter through all items.
        return [
            item for item in items
            if all(
                tag in item.getItemDefinition().getTags(item)
                for tag in tags
            )
        ]

    def getSortedItems(self) -> List[InventoryItem]:
        """
        Gets all filtered items that are sorted appropriately.
        """
        items = self.getFilteredItems()
        filterType = self.sortButtons.getSelectedFilterType()
        ascending = self.sortButtons.isAscending()

        if filterType == ItemFilterType.Recent:
            if not ascending:
                return items
            else:
                return list(reversed(items))
        elif filterType == ItemFilterType.Alphabetical:
            return sorted(
                items,
                key=lambda item: item.getItemDefinition().getName(item),
                reverse=not ascending,
            )
        elif filterType == ItemFilterType.Rarity:
            return sorted(
                items,
                key=lambda item: item.getItemDefinition().getRarity(item),
                reverse=ascending,
            )

        raise AttributeError(f'No filterType: {filterType}')


if __name__ == "__main__":
    gui = InventoryFilterWidget(
        parent=aspect2d,
        scale=1.0,
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
        gui.setItems(crazyItemList)
    setNewItemList()
    base.accept('a', setNewItemList)

    GUITemplateSliders(
        gui,
        'pos',
        'scale',
        'frameSize',
        'labelPos',
        'labelScale',
        'categoryPos',
        'categoryScale',
        'sortButtonsPos',
        'sortButtonsScale',
        'tagsPadding',
        'tagsHeadroom',
        scale=0.12,
    )
    base.run()
