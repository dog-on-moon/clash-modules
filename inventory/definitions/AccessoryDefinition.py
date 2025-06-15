from enum import IntEnum
from typing import Optional

from panda3d.core import NodePath, Texture

from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.base.ItemDefinition import ItemDefinition
from toontown.inventory.enums.ItemEnums import ItemType
from toontown.inventory.enums.ItemTags import ItemTag
from toontown.toon.accessories.ToonAccessory import ToonAccessory
from toontown.toon.accessories.placements.HatPlacements import HatPlacements
from toontown.toon.accessories.placements.GlassesPlacements import GlassesPlacements
from toontown.toon.accessories.placements.BackpackPlacements import BackpackPlacements
from toontown.toon.accessories.placements.NeckPlacements import NeckPlacements


class AccessoryDefinition(ItemDefinition):
    """
    A special item definition class for accessories.
    """

    PLACEMENT_DICT: dict[ItemType, dict[IntEnum, dict[str, tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]]]]] = {
        ItemType.Cosmetic_Hat: HatPlacements,
        ItemType.Cosmetic_Glasses: GlassesPlacements,
        ItemType.Cosmetic_Backpack: BackpackPlacements,
        ItemType.Cosmetic_Neck: NeckPlacements,
    }

    def getAccessoryPlacement(self, item: InventoryItem) -> dict[str, tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]]]:
        """
        Returns the placement of this accessory.
        """
        assert item.getItemType() in self.PLACEMENT_DICT
        return self.PLACEMENT_DICT[item.getItemType()].get(item.getItemSubtype(), {})

    def getToonAttachNode(self) -> str:
        """
        Returns the node to attach the accessories to.
        """
        return '**/__Actor_head'

    def getModelPath(self) -> str:
        return ''

    def getTexturePath(self) -> str | None:
        return None

    def getAccessoryClass(self):
        return ToonAccessory

    def getTags(self, item: 'InventoryItem') -> set[ItemTag]:
        tags = super().getTags(item)
        tags.add(ItemTag.Accessory)
        return tags

    def makeItemModel(self, item: Optional[InventoryItem] = None, *extraArgs) -> NodePath:
        # Load model.
        modelPath = self.getModelPath()
        if not modelPath:
            return NodePath()
        model = loader.loadModel(modelPath)

        # Apply texture if need be.
        texturePath = self.getTexturePath()
        if texturePath:
            texture = loader.loadTexture(texturePath)
            texture.setMinfilter(Texture.FTLinearMipmapLinear)
            texture.setMagfilter(Texture.FTLinear)
            model.setTexture(texture, 1)

        # Return model.
        return model

    def makeGuiItemModel(self) -> NodePath:
        """
        Creates the GUI item model to be used.
        """
        model = self.makeItemModel()
        if model:
            self.getAccessoryClass().modifyPreview(model)
            model.flattenLight()
        # TODO - adjust model H dynamically
        return model
