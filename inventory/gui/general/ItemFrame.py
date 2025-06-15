from toontown.inventory.enums.RarityEnums import getItemRarityColor
from toontown.toonbase import RealmGlobals

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
from toontown.gui.TTGui import kwargsToOptionDefs
from toontown.gui.GUITemplateSliders import GUITemplateSliders
from toontown.gui.GUINode import GUINode
from toontown.gui import UiHelpers
from toontown.gui.EasyManagedItem import EasyManagedItem
from toontown.gui.EasyManagedButton import EasyManagedButton
from toontown.gui.EasyScrolledFrame import EasyScrolledFrame
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.InjectorTarget import InjectorTarget
from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.base.ItemDefinition import ItemDefinition
from toontown.toon.gui import GuiBinGlobals
from direct.gui.DirectGui import *
from panda3d.core import NodePath
from typing import Union, Any


@DirectNotifyCategory()
class ItemFrame(EasyManagedButton):
    """
    This GUI frame can be used to render an InventoryItem.
    """

    @InjectorTarget
    def __init__(self, parent, **kw):
        # GUI boilerplate.
        optiondefs = kwargsToOptionDefs(
            pos = (0, 0, 0),
            scale = 1.0,
            easyWidth  = 0.2,
            easyHeight = -0.2,
            callback = None,
            # relief = None,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.initialiseoptions(ItemFrame)
        self.setBin('sorted-gui-popup', GuiBinGlobals.ItemFrameBin)

        self.item: Optional[InventoryItem] = None
        self.itemModelNode: Optional[NodePath] = None
        self.itemModel: Optional[NodePath] = None

        self.text_quantity: DirectLabel | None = None
        self.text_equipped: Optional[DirectLabel] = None

        if self['callback']:
            self.bind(DGG.B1PRESS, lambda _=None: self['callback'](self.item))

        self._create()
        self.place()

    def destroy(self):
        self._setItemRender(None)
        self.unbind(DGG.B1PRESS)
        super().destroy()

    def _create(self):
        self.text_quantity = DirectLabel(
            parent=self, relief=None,
            text='x1',
            text_pos=(0.08818, -0.10),
            text_scale=0.06,
        )
        self.text_quantity.setBin('sorted-gui-popup', GuiBinGlobals.ItemFrameBin + 5)
        self.text_equipped = DirectLabel(parent=self, pos=(.09, 0, .09), text='E', text_scale=0.05)

    def place(self):
        if base.localAvatar and self.item in base.localAvatar.getEquippedItems():
            self.text_equipped.show()
        else:
            self.text_equipped.hide()

    def bindToScroll(self, easyScrolledFrame):
        easyScrolledFrame.bindToScroll(self)

    def setItem(self, item: Optional[InventoryItem] = None):
        """Sets the item within the ItemFrame."""
        if RealmGlobals.getCurrentRealm().isDevRealm():
            try:
                self._setItemRender(item)
            except Exception as e:
                # We're catching exceptions ATM since we're still in development.
                print(str(e))
        else:
            # Blindly set the render.
            self._setItemRender(item)
        self.item = item

        if self['callback']:
            self.unbind(DGG.B1PRESS)
            self.bind(DGG.B1PRESS, lambda _=None: self['callback'](self.item))

    """
    Item Rendering
    """

    def _setItemRender(self, item: Optional[InventoryItem]):
        if item is None:
            # Cleanup item render.
            if not self.item:
                return
            if self.itemModel:
                itemDef = self.item.getItemDefinition()
                itemDef.cleanupGuiItemModel(self.itemModel, self.item)
            if self.itemModelNode:
                self.itemModelNode.removeNode()
            self.itemModel = None
            self.itemModelNode = None
            self['frameColor'] = (1, 1, 1, 1)
            self.text_quantity['text'] = ''
        else:
            # Sets this item to render.
            if self.itemModel or self.itemModelNode:
                # Cleanup if need be.
                self._setItemRender(None)

            # Make item render visible.
            itemDef = item.getItemDefinition()
            self.itemModelNode = self.attachNewNode('modelNode')
            self.itemModel = itemDef.getGuiItemModel(item, parent=self.itemModelNode)
            self['frameColor'] = getItemRarityColor(item)

            quantity = item.getQuantity()
            if quantity > 1:
                quantityText = f'x{quantity}'
            else:
                quantityText = ''
            if self.text_quantity['text'] != quantityText:
                self.text_quantity['text'] = quantityText


if __name__ == "__main__":
    from toontown.inventory.enums.ItemEnums import BackgroundItemType
    from toontown.inventory.enums.ItemEnums import ChatStickersItemType
    from toontown.inventory.enums.ItemEnums import FishingRodItemType
    from toontown.inventory.enums.ItemEnums import ProfilePoseItemType
    for i, invItem in enumerate([
        InventoryItem.fromSubtype(BackgroundItemType.Event_Winter2018_A),
        InventoryItem.fromSubtype(ChatStickersItemType.GreenedCat),
        InventoryItem.fromSubtype(ProfilePoseItemType.Wave)
            ]):
        gui = ItemFrame(
            parent=aspect2d,
            scale=2.0,
            pos=(-1.1 + (i * 1.1), 0, 0),
        )
        gui.setItem(invItem)

    GUITemplateSliders(
        gui.text_quantity,
        'text_pos', 'text_scale'
    )
    base.run()
