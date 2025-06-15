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
from toontown.gui.CornerAnchor import CornerAnchor
from toontown.gui import UiHelpers
from toontown.gui.EasyManagedItem import EasyManagedItem
from toontown.gui.EasyManagedButton import EasyManagedButton
from toontown.gui.EasyScrolledFrame import EasyScrolledFrame
from toontown.gui.Bounds import Bounds
from toontown.gui.GUIPositionGlobals import ScreenCorner
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.InjectorTarget import InjectorTarget
from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.enums.ItemTags import ItemTag, ConflictingTags
from direct.gui.DirectGui import *
from typing import Optional, List, Tuple, Dict, Set, TYPE_CHECKING
if TYPE_CHECKING:
    from toontown.utils.InjectorHelper import *


@DirectNotifyCategory()
class ItemTagSelectorFrame(EasyScrolledFrame, Bounds):
    """
    A scrollable frame that contains a list of all matching item tags.
    """

    @InjectorTarget
    def __init__(self, parent, **kw):
        # GUI boilerplate.
        optiondefs = TTGui.kwargsToOptionDefs(
            pos = (0, 0, 0),
            scale = 1.0,
            hideScroll=True,

            callback=None,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.initialiseoptions(ItemTagSelectorFrame)

        # GUI State
        self.itemTags: Dict[ItemTag, ItemTagButton] = dict()
        self.selectedTags: Set[ItemTag] = set()

    def destroy(self):
        super().destroy()
        del self.itemTags

    def setItems(self, items: List[InventoryItem]):
        """
        Sets the visible item tags within the scroll frame.
        The tags used are grabbed from the selected items.
        """
        itemTags = set()

        # Iterate over each item, get their tags.
        for item in items:
            itemTags.update(item.getItemDefinition().getTags(item))

        # Set the tags now.
        self.setItemTags(itemTags)

    def setItemTags(self, itemTags: Set[ItemTag]):
        """
        Sets the visible item tags within the scroll frame.
        """
        self.removeAllItems()
        self.itemTags = {}

        # First, get an ordered list of the itemtags.
        orderedTags = []
        for it in ItemTag:
            if it in itemTags:
                orderedTags.append(it)

        # Add a component per tag.
        for itemTag in orderedTags:
            button = ItemTagButton(
                parent=self,
                itemTag=itemTag,
                easyScrolledFrame=self,
                command=self.onTagSelected,
                extraArgs=[itemTag],
            )
            self.itemTags[itemTag] = button

        # Clean out old unused selectedTags.
        for selectedTag in tuple(self.selectedTags):
            if selectedTag not in self.itemTags:
                self.selectedTags.discard(selectedTag)

        # Place them.
        self.updateItemPositions()

    def onTagSelected(self, itemTag: ItemTag):
        """
        Called to add or remove a tag.
        """
        if itemTag not in self.selectedTags:
            # We need to add this tag.
            # But first, look for any potential overlapping tags,
            # and deselect those.
            for conflictingTagSet in ConflictingTags:
                # Skip this tag set if we are not a part of it.
                if itemTag not in conflictingTagSet:
                    continue

                # Remove all selected tags in this set.
                for exclusionTag in conflictingTagSet:
                    self.selectedTags.discard(exclusionTag)

            # Now select this new tag.
            self.selectedTags.add(itemTag)
        else:
            # We need to remove this tag.
            self.selectedTags.discard(itemTag)

        # Figure out where our overlapping tags are.
        conflictingTags = set()
        for conflictingTagSet in ConflictingTags:
            # For each conflicting tag set, we'll check all
            # of our selected tags.
            for selectedTag in self.selectedTags:
                # Do we have a selected tag in this conflicting set?
                if selectedTag in conflictingTagSet:
                    # Update the conflicting set to include all these tags,
                    # and then move onto the next conflicting tag set.
                    conflictingTags.update(conflictingTagSet)
                    break

        # Update the GUI elements.
        for itemTag, button in self.itemTags.items():
            button.setSelected(
                mode=itemTag in self.selectedTags,
                overlaps=itemTag in conflictingTags,
            )

        if self['callback']:
            self['callback']()

    def getSelectedTags(self) -> Set[ItemTag]:
        return self.selectedTags


@DirectNotifyCategory()
class ItemTagButton(EasyManagedButton, Bounds):
    """
    A single item tag button row.
    """

    @InjectorTarget
    def __init__(self, parent, **kw):
        # GUI boilerplate.
        optiondefs = TTGui.kwargsToOptionDefs(
            pos = (0, 0, 0),
            scale = 1.0,
            text = '',
            text_align=TextNode.ALeft,
            text_pos=(0.00588, -0.05585),
            text_scale=0.05938,

            itemTag=ItemTag.RarityCommon,
            height=0.08,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.initialiseoptions(ItemTagButton)

        UiHelpers.gui_update(
            self,
            text=self['itemTag'],
            frameSize=(0, 1, -self['height'], 0),
            easyHeight=-self['height'],
        )

    def setSelected(self, mode: bool, overlaps: bool):
        if mode:
            self['frameColor'] = (0, 1, 0, 1)
        elif overlaps:
            self['frameColor'] = (0.58, 0.58, 0.58, 1.0)
        else:
            self['frameColor'] = (1, 1, 1, 1)


if __name__ == "__main__":
    gui = ItemTagSelectorFrame(
        parent=aspect2d,
        # any kwargs go here
    )
    gui.setItemTags(
        {
            ItemTag.RarityEvent,
            ItemTag.RarityEvent,
            ItemTag.RarityCommon,
            ItemTag.StickersFoil,
        }
    )
    GUITemplateSliders(
        gui.canvasItems[0],
        'text_pos', 'text_scale'
    )
    base.run()
