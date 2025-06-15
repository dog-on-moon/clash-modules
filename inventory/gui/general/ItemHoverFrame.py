if __name__ == "__main__":
    from tools.headless.headlessbase import HeadlessStart
    from tools.headless.headlessbase.HeadlessBase import HeadlessBase
    base = HeadlessBase(wantHotkeys=False)
    if __debug__:
        from toontown.utils.DeveloperInjector import startInjector
        startInjector()
    # base.initCR()  # defines base.cr
    # base.startHeadlessShow()

from typing import Optional
from toontown.toonbase import RealmGlobals
from toontown.inventory.enums.RarityEnums import getItemRarityColor
from toontown.gui.TTGui import kwargsToOptionDefs
from toontown.gui.GUITemplateSliders import GUITemplateSliders
from toontown.gui.GUINode import GUINode
from toontown.gui import UiHelpers
from toontown.gui.ScaledFrame import ScaledFrame
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.InjectorTarget import InjectorTarget
from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.base.ItemDefinition import ItemDefinition
from toontown.toon.gui import GuiBinGlobals
from panda3d.core import *
from direct.gui.DirectGui import *
from typing import Union, Any


@DirectNotifyCategory()
class ItemHoverFrame(ScaledFrame):
    """
    This GUI frame can be used to render detailed information about an item when its frame is hovered over.
    """

    @InjectorTarget
    def __init__(self, parent, **kw):
        self.item: InventoryItem | None = None
        # GUI boilerplate.
        optiondefs = kwargsToOptionDefs(
            pos=(0, 0, 0),
            scale=1.0,
            frameSize=(-0.475, 0.475, -0.4, 0.0),
            scaledTexture='phase_3/maps/gui/ttcc_gui_scaledFrame_shadow.png',
            borderScale=0.04,
            # relief = None,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.initialiseoptions(ItemHoverFrame)
        self.setBin('sorted-gui-popup', GuiBinGlobals.ItemHoverFrameBin)
        # Double up on shadow so that the texture is more opaque and thus easier to read text on
        self['shadowStrength'] = 0.001

        self.text_title: DirectLabel | None = None
        self.text_description: DirectLabel | None = None

        self._create()
        self.place()

    def destroy(self):
        self.setItem(None)
        super().destroy()

    def _create(self):
        self.text_title = DirectLabel(parent=self, pos=(0.0, 0, -0.06), text='Title', text_scale=0.065, relief=None,
                                      text_align=TextNode.ACenter, text_fg=(1, 1, 1, 1))
        self.text_description = DirectLabel(parent=self, pos=(-0.45, 0, -0.09), text='Description', text_scale=0.05,
                                            relief=None, text_align=TextNode.ALeft, text_wordwrap=18,
                                            text_fg=(1, 1, 1, 1))

    def place(self):
        if self.item is None:
            return

        isEquipped = base.localAvatar and self.item in base.localAvatar.getEquippedItems()
        title = self.item.getItemDefinition().getName()
        quantity = self.item.getQuantity()
        if quantity > 1:
            quantityText = f' (x{quantity})'
        else:
            quantityText = ''
        title += quantityText
        if isEquipped:
            # TODO: This equip indicator is temporary, we need an icon
            title += ' \1deepYellow\1(E)\2'
        desc = '\1item_hover_underline\1____________________________________\2\n\n'

        itemDesc = self.item.getItemDefinition().getItemTypeDescriptionInfo(self.item)
        if itemDesc:
            desc += itemDesc
            desc += '\n\1item_hover_underline\1____________________________________\2\n\n'

        standardDesc = self.item.getItemDefinition().getDescription()
        if standardDesc:
            desc += standardDesc
            desc += '\1TextShrink\1\n\n\2'
        desc += self.item.getItemDefinition().getExtendedDescription(self.item)

        self.text_title['text'] = title
        self.text_description['text'] = desc

        # Scale frame size downwards dependent on the sizing of the description text.
        # Longer description = frame size goes further down
        self['frameSize'] = (-0.475, 0.475, self.text_description.component('text0').getTightBounds()[0][2] - 0.11, 0.0)

    def setItem(self, item: Optional[InventoryItem] = None):
        """Sets the item within the ItemFrame."""
        self.item = item
        self.place()


if __name__ == "__main__":
    from toontown.inventory.enums.ItemEnums import BackgroundItemType
    from toontown.inventory.enums.ItemEnums import ChatStickersItemType
    from toontown.inventory.enums.ItemEnums import FishingRodItemType
    from toontown.inventory.enums.ItemEnums import ProfilePoseItemType
    for i, invItem in enumerate([
        InventoryItem.fromSubtype(BackgroundItemType.Event_Winter2018_A),
        InventoryItem.fromSubtype(ChatStickersItemType.GreenedCat),
        InventoryItem.fromSubtype(FishingRodItemType.Platinum)
            ]):
        gui = ItemHoverFrame(
            parent=aspect2d,
            scale=1.0,
            pos=(-1.1 + (i * 1.1), 0, 0),
        )
        gui.setItem(invItem)

    base.setBackgroundColor(0.5, 0.5, 1)

    # GUITemplateSliders(
    #     gui.text_quantity,
    #     'text_pos', 'text_scale'
    # )
    base.run()
