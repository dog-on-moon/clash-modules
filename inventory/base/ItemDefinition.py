"""
Somehow, some way, each property of every item subtype needs to have
specific information attributed to it -- whether that's a name,
model path, or any constant data that one needs to have directly
referenced as information on the item itself.

The ItemDefinition class is designed as a dataclass that which can
hold this information for you. The base attributes of the items need
to be declared (name, description, rarity etc), but subclasses of
ItemDefinition can be made depending on the ItemType in order to
more easily define unique, registerable fields for other ItemTypes.
"""
from enum import IntEnum
from typing import Optional, Dict, List, Set, Tuple

from direct.actor.Actor import Actor
from panda3d.core import NodePath, TextNode

from toontown.cutscene.CutsceneSequenceHelpers import NodePathWithState
from toontown.estate.EstateGlobals import EstateItemType
from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.base.ItemID import ItemID
from toontown.inventory.enums.EquipSoundEnum import EquipSoundEnum
from toontown.inventory.enums.ItemAttribute import ItemAttribute
from toontown.inventory.enums import ItemModifier
from toontown.inventory.enums.ItemTags import ItemCategory, ItemTag
from toontown.inventory.enums.RarityEnums import Rarity, getItemRarityColor, getItemRarityName, getItemRarityNameWithColor
from toontown.toon.gui import GuiBinGlobals
from toontown.utils.AstronDict import AstronDict


class ItemDefinition:
    """
    A base dataclass for holding defined item values.

    This class can be inherited for creating more specific
    definitions necessary for different ItemTypes.
    """
    CACHES_3D_MODEL = False
    CACHES_2D_MODEL = False

    def __init__(self,
                 name: str = 'No Name',
                 description: str = 'No Description',
                 shopDescription: Optional[str] = None,
                 rarity: Rarity = Rarity.Common,
                 levelRequirement: int = 0,
                 statDict: dict = None,
                 equipSound: Optional[EquipSoundEnum] = None):
        if shopDescription is None:
            shopDescription = description
        self.name: str = name
        self.description: str = description
        self.shopDescription: str = shopDescription
        self.rarity: Rarity = rarity
        self.levelRequirement: int = levelRequirement
        self.statDict: dict = statDict or {}
        self.equipSounds: Optional[EquipSoundEnum] = equipSound

        # This is filled in later in ItemTypeRegistry.
        self.itemSubtype: Optional[IntEnum] = None

        # Item Definition State
        self.cached3dModels: Dict[AstronDict, NodePath] = {}
        self.cached2dModels: Dict[AstronDict, NodePath] = {}

    def getName(self, item: Optional[InventoryItem] = None) -> str:
        return self.name

    def getDescription(self) -> str:
        return self.description

    def getShopDescription(self) -> str:
        return self.shopDescription

    def getRarity(self, item: Optional[InventoryItem] = None) -> Rarity:
        return self.rarity

    def getLevelRequirement(self) -> int:
        return self.levelRequirement

    def getStatDict(self) -> dict:
        return self.statDict

    def getEquipSounds(self) -> EquipSoundEnum:
        return self.equipSounds or EquipSoundEnum.Default

    def getItemTypeName(self):
        return 'Item Type'

    def getItemSubtype(self):
        return self.itemSubtype

    def getRewardName(self, item: Optional[InventoryItem] = None):
        """
        Appears on:
        - Quest Reward Text
        """
        return self.getName()

    def getTextIcon(self, item: Optional[InventoryItem] = None) -> str:
        """
        Appears on:
        - Mini icons for quest reward text
        """
        return '\1white\1\5reward_packageIcon\5\2'

    """
    Estate Definitions
    """

    def isEstatePlaceable(self, item: InventoryItem) -> bool:
        """Is this item placeable in an estate?"""
        return False

    def getEstateItemType(self) -> EstateItemType:
        """
        Determines the AI object generated for this Item
        when placed in the estate.
        """
        return EstateItemType.GENERIC

    def getEstateModel(self, item: Optional[InventoryItem] = None, *extraArgs) -> NodePathWithState:
        return self.getItemModel(item, *extraArgs)

    def cleanupEstateModel(self, model, item):
        return self.cleanupItemModel(model, item)

    """
    Item Categorization
    """

    def getItemCategory(self) -> ItemCategory:
        """
        Gets the category of item that fulfills this definition.
        By default, items are slotted into the "misc" category.
        """
        return ItemCategory.Misc

    def getTags(self, item: 'InventoryItem') -> set[ItemTag]:
        """
        Returns a list of all tags that the items match with.
        """
        tags = set()

        # Add tags.
        if item.getRarity() == Rarity.Common:
            tags.add(ItemTag.RarityCommon)
        if item.getRarity() == Rarity.Uncommon:
            tags.add(ItemTag.RarityUncommon)
        if item.getRarity() == Rarity.Rare:
            tags.add(ItemTag.RarityRare)
        if item.getRarity() == Rarity.VeryRare:
            tags.add(ItemTag.RarityVeryRare)
        if item.getRarity() == Rarity.UltraRare:
            tags.add(ItemTag.RarityUltraRare)
        if item.getRarity() == Rarity.Legendary:
            tags.add(ItemTag.RarityLegendary)
        if item.getRarity() == Rarity.Mythic:
            tags.add(ItemTag.RarityMythic)
        if item.getRarity() == Rarity.Event:
            tags.add(ItemTag.RarityEvent)

        # Return the tags.
        return tags

    """
    Item Rendering
    """

    def makeItemModel(self, item: Optional[InventoryItem] = None, *extraArgs) -> NodePath:
        """
        Creates the item model to be used.
        """
        return NodePath()

    def modifyItemModel(self, model: NodePathWithState, item: Optional[InventoryItem] = None) -> None:
        """
        Modifies the appearance of the item model, relative to a passed-in item itself.
        """
        if not item:
            setattr(model, 'itemDefSequences', [])
            return

        itemDefSequences = []

        # Set model colorscale.
        overrideColorscale = item.getAttribute(ItemAttribute.MODEL_COLORSCALE)
        if overrideColorscale is not None:
            model.setColorScale(*overrideColorscale)

        # Get all relevant sequences.
        if item.hasAttribute(ItemAttribute.MODIFIER_3D):
            seq = ItemModifier.getVisualSequence(
                item.getAttribute(ItemAttribute.MODIFIER_3D), model
            )
            seq.loop()
            itemDefSequences.append(seq)
        elif item.hasAttribute(ItemAttribute.MODIFIER):
            seq = ItemModifier.getVisualSequence(
                item.getAttribute(ItemAttribute.MODIFIER), model
            )
            seq.loop()
            itemDefSequences.append(seq)
        setattr(model, 'itemDefSequences', itemDefSequences)

    def cleanupItemModel(self, model: NodePath, item: Optional[InventoryItem] = None) -> None:
        """
        Cleans up the item model (returned by getItemModel).
        """
        if hasattr(model, 'itemDefSequences'):
            for seq in getattr(model, 'itemDefSequences', []):
                seq.pause()
            delattr(model, 'itemDefSequences')
        if isinstance(model, Actor):
            model.cleanup()
        else:
            model.removeNode()

    def getItemModel(self, item: Optional[InventoryItem] = None, *extraArgs) -> NodePathWithState:
        """
        Returns a nodepath that represents this item.
        Accesses from a cache, preferably do not override this.
        """
        if self.CACHES_3D_MODEL and item:
            # Create a cached model if necessary.
            itemId = item.getAttributes()
            if not self.cached3dModels.get(itemId):
                self.cached3dModels[itemId] = self.makeItemModel(item=item, *extraArgs)

                # If the node is empty, we use it.
                if not self.cached3dModels[itemId]:
                    return self.cached3dModels[itemId]
                else:
                    # Otherwise, make sure it is in hidden.
                    self.cached3dModels[itemId].reparentTo(hidden)

            # Return a copy of this node.
            newModel = NodePathWithState()
            copiedModel = self.cached3dModels[itemId].copyTo(newModel)
            copiedModel = NodePathWithState(copiedModel)
            self.modifyItemModel(copiedModel, item)
            return copiedModel
        else:
            model = self.makeItemModel(item=item, *extraArgs)
            if isinstance(model, Actor):
                self.modifyItemModel(model, item)
                return model
            newModel = NodePathWithState()
            copiedModel = model.copyTo(newModel)
            copiedModel = NodePathWithState(copiedModel)
            self.modifyItemModel(copiedModel, item)
            model.removeNode()
            return copiedModel

    """
    GUI Item Models
    """

    def makeGuiItemModel(self) -> NodePath:
        """
        Creates the GUI item model to be used.
        """
        return self.makeItemModel()

    def modifyGuiItemModel(self, model: NodePathWithState, item: Optional[InventoryItem] = None) -> None:
        """
        Modifies the appearance of the item model, relative to a passed-in item itself.
        """
        model.setDepthWrite(1)
        model.setDepthTest(1)
        model.setTwoSided(True)

        if not item:
            setattr(model, 'itemDefSequences', [])
            return

        itemDefSequences = []

        # Set model colorscale.
        overrideColorscale = item.getAttribute(ItemAttribute.MODEL_COLORSCALE)
        if overrideColorscale is not None:
            model.setColorScale(*overrideColorscale)

        # Get all relevant sequences.
        if item.hasAttribute(ItemAttribute.MODIFIER_2D):
            seq = ItemModifier.getVisualSequence(
                item.getAttribute(ItemAttribute.MODIFIER_2D), model
            )
            seq.loop()
            itemDefSequences.append(seq)
        elif item.hasAttribute(ItemAttribute.MODIFIER):
            seq = ItemModifier.getVisualSequence(
                item.getAttribute(ItemAttribute.MODIFIER), model
            )
            seq.loop()
            itemDefSequences.append(seq)
        setattr(model, 'itemDefSequences', itemDefSequences)

    def cleanupGuiItemModel(self, model: NodePath, item: Optional[InventoryItem] = None) -> None:
        """
        Cleans up the GUI Item Model (returned by getGuiItemModel).
        """
        self.cleanupItemModel(model, item=item)

    def getGuiItemModel(self, item: Optional[InventoryItem] = None,
                        parent: Optional[NodePath] = None,
                        adjustScale: bool = True,
                        modelBin: Optional[int] = GuiBinGlobals.ItemFrameBin + 1,
                        useModel: Optional[NodePath] = None) -> NodePath:
        """
        Returns a nodepath that is to be used in 2D space.
        """
        if useModel:
            copiedModel = useModel
        elif self.CACHES_2D_MODEL:
            # Create a cached model if necessary.
            itemId = item.getAttributes()
            if not self.cached2dModels.get(itemId):
                self.cached2dModels[itemId] = self.makeGuiItemModel()

                # If the node is empty, we use it.
                if not self.cached2dModels[itemId]:
                    return self.cached2dModels[itemId]
                else:
                    # Otherwise, make sure it is in hidden.
                    self.cached2dModels[itemId].reparentTo(hidden)

            # Return a copy of this node.
            newModel = NodePathWithState()
            copiedModel = self.cached2dModels[itemId].copyTo(newModel)
            copiedModel = NodePathWithState(copiedModel)
            self.modifyGuiItemModel(copiedModel, item)
        else:
            model = self.makeGuiItemModel()
            if not model:
                return model
            if isinstance(model, Actor):
                copiedModel = model
                self.modifyGuiItemModel(copiedModel, item)
            else:
                newModel = NodePathWithState()
                copiedModel = model.copyTo(newModel)
                copiedModel = NodePathWithState(copiedModel)
                self.modifyGuiItemModel(copiedModel, item)
                model.removeNode()

        # Are we reparenting the copied model?
        if parent:
            copiedModel.reparentTo(parent)

        # Are we auto-rescaling the item to fit?
        if adjustScale:
            bMin, bMax = copiedModel.getTightBounds()
            center = (bMin + bMax) / 2.0
            corner = Vec3(bMax - center)
            scale = (1.0 / max(corner[0], corner[1], corner[2])) * 0.09
            pos = (-center[0] * scale, -center[1] * scale, -center[2] * scale)
            copiedModel.setPos(pos)
            copiedModel.setScale(scale)

        # Set model bin.
        if modelBin is not None:
            copiedModel.setBin('sorted-gui-popup', modelBin)

        # Return the model.
        return copiedModel

    """
    Text Rendering
    """

    def getTextRenderItemName(self, item: Optional[InventoryItem] = None):
        return f"{self.getItemTypeName()}\n{self.getName()}"

    def getTextRenderFont(self, item: Optional[InventoryItem] = None):
        from toontown.toonbase import ToontownGlobals
        return ToontownGlobals.getInterfaceFont()

    def renderTextForGuiModel(self, item: Optional[InventoryItem] = None) -> NodePath:
        # To be used mostly in placeholder development instances
        HpTextGenerator = TextNode('HpTextGenerator')
        HpTextGenerator.setFont(self.getTextRenderFont(item))
        HpTextGenerator.clearShadow()
        HpTextGenerator.setAlign(TextNode.ACenter)
        HpTextGenerator.setTextColor(0, 0, 0, 1)

        HpTextGenerator.setText(self.getTextRenderItemName(item))
        hpTextNode = HpTextGenerator.generate()
        realNode = NodePath(hpTextNode)
        realNode.setScale(1)
        del HpTextGenerator
        realNode.setDepthWrite(1)
        realNode.setDepthTest(1)
        realNode.setTwoSided(True)
        bMin, bMax = realNode.getTightBounds()
        center = (bMin + bMax) / 2.0
        realNode.setPos(-center[0], -center[1], -center[2])
        return realNode

    """
    Hover Extended Description
    """

    def getExtendedDescription(self, item: Optional[InventoryItem] = None) -> str:
        # Extended description information for use on item hovers
        if item:
            return f'\1SlightSlant\1{getItemRarityNameWithColor(item)} {self.getItemTypeName()}\2'
        return ''

    def getItemTypeDescriptionInfo(self, item: Optional[InventoryItem] = None) -> str:
        # Extended description information for specific item types, such as showing stat bonuses
        return ''
