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
from toontown.toon.socialpanel.SocialPanelGlobals import sp_gui
from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.gui.player.preview.InventoryBaseItemPreview import InventoryBaseItemPreview
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.InjectorTarget import InjectorTarget
from toontown.utils import ColorHelper, text
from toontown.toon.Toon import Toon
from toontown.toon.ToonDNA import ToonDNA
from direct.gui.DirectGui import *
from typing import Optional, List, Tuple, Dict, Set, TYPE_CHECKING
if TYPE_CHECKING:
    from toontown.inventory.gui.player.preview.InventoryPreviewPanel import InventoryPreviewPanel
    from toontown.utils.InjectorHelper import *


@DirectNotifyCategory()
class InventoryGenericItemPreview(InventoryBaseItemPreview):
    """
    The generic item preview for the inventory panel.
    """

    @InjectorTarget
    def __init__(self, parent, panel, **kw):
        """
        :type parent: NodePath
        :type panel: InventoryPreviewPanel
        """
        # GUI boilerplate.
        optiondefs = TTGui.kwargsToOptionDefs(
            item = None,
            middleNode = 0.75,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, panel, **kw)

        # GUI prototypes
        self.itemNode:       Optional[GUINode] = None
        self.label_itemName: Optional[DirectLabel] = None
        self.button_equip:   Optional[EasyManagedButton] = None
        self.button_delete:  Optional[EasyManagedButton] = None

        # Initialize
        self.initialiseoptions(InventoryGenericItemPreview)

    def _create(self):
        super()._create()
        item: InventoryItem = self['item']
        itemDef = item.getItemDefinition()

        clickSndPaths = itemDef.getEquipSounds().value
        self.clickSounds = [loader.loadSfx(clickSndPaths[0]), loader.loadSfx(clickSndPaths[1])]

        # Fulfill prototypes
        self.label_itemName = DirectLabel(
            parent=self.panel.getTopAnchor(),
            relief=None,
            text=item.getItemDefinition().getName(item),
            text_fg=(0, 0, 0, 1),
            text_scale=0.5,
            text_pos=(0, -0.11),
        )
        self.itemNode = GUINode(parent=self.panel.getUpperMidpoint(), scale=2.0)
        self.button_equip = EasyManagedButton(
            parent=self.panel.getLowerMidpoint(),
            frameSize=(-0.1, 0.1, -0.05, 0.05),
            easyWidth=0.25,
            text='',
            text_scale=0.05,
            clickSound=None,
            command=self.onEquip,
        )
        self.button_delete = EasyManagedButton(
            parent=self.panel.getLowerMidpoint(),
            frameSize=(-0.1, 0.1, -0.05, 0.05),
            easyWidth=0.25,
            text='Delete',
            text_scale=0.05,
            command=self.onDelete,
        )

        # Render the item node.
        if item:
            try:
                item.getItemDefinition().getGuiItemModel(item, parent=self.itemNode)
            except Exception as e:
                print(e)
        self.updateButtonText()
        self.accept('newLocalInventory', self.updateButtonText)

    def place(self):
        super().place()

        text.fitLabelTextToBounds(
            maxWidth=self.panel.getBoundWidth() * 0.9,
            maxHeight=0.15,
            maxScale=0.11,
            maxLines=1,
            label=self.label_itemName,
            textNodeName='text0',
        )
        UiHelpers.placeElementsInHorizontalLine(
            [self.button_equip, self.button_delete],
            startPos=(0, 0, 0),
            alignCenter=True,
        )

    def destroy(self):
        self.itemNode.destroy()
        self.label_itemName.destroy()
        self.button_equip.destroy()
        self.button_delete.destroy()
        for clickSound in self.clickSounds:
            clickSound.stop()
            del clickSound
        self.clickSounds = None
        super().destroy()

    """
    Button Events
    """

    def onEquip(self):
        item = self['item']
        base.cr.inventoryManager.debug_applyLocalDelta(
            InventoryDelta(action=InventoryAction.UNEQUIP if base.localAvatar and item in base.localAvatar.getEquippedItems() else InventoryAction.EQUIP, item=item)
        )
        print(f"{str(item)} has been {'un' if base.localAvatar and item in base.localAvatar.getEquippedItems() else ''}equipped")

    def onDelete(self):
        item = self['item']
        base.cr.inventoryManager.debug_applyLocalDelta(
            InventoryDelta(action=InventoryAction.REMOVE, item=item)
        )
        print(f"{str(item)} has been deleted")

    def updateButtonText(self, inventory=None):
        item: InventoryItem = self['item']

        if not inventory:
            inventory = base.cr.inventoryManager.getInventory()

        # Logic is a little weird here? Not sure, but it has to be inverted.
        itemEquipped = item in inventory.getEquippedItems()
        self.button_equip['text'] = 'Equip' if not itemEquipped else 'Unequip'
        self.button_equip['clickSound'] = self.clickSounds[0] if not itemEquipped else self.clickSounds[1]


if __name__ == "__main__":
    gui = InventoryGenericItemPreview(
        parent=aspect2d,
        # any kwargs go here
    )
    GUITemplateSliders(
        gui,
        'pos', 'scale'
    )
    base.run()
