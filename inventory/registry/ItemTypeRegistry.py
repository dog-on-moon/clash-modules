"""
This module contains the registry for ItemTypes to the
local registries for different item subtypes.
"""
from toontown.inventory.base.ItemDefinition import ItemDefinition
from toontown.inventory.enums.ItemEnums import ItemType
from enum import IntEnum
from typing import Dict, Union, Any

from toontown.inventory.registry.BoosterRegistry import BoosterRegistry
from toontown.inventory.registry.ProfileBackgroundRegistry import ProfileBackgroundRegistry
from toontown.inventory.registry.ProfileNameplateRegistry import ProfileNameplateRegistry
from toontown.inventory.registry.ProfilePoseRegistry import ProfilePoseRegistry
from toontown.inventory.registry.HatRegistry import HatRegistry
from toontown.inventory.registry.GlassesRegistry import GlassesRegistry
from toontown.inventory.registry.BackpackRegistry import BackpackRegistry
from toontown.inventory.registry.NeckRegistry import NeckRegistry
from toontown.inventory.registry.ShirtRegistry import ShirtRegistry
from toontown.inventory.registry.ShoeRegistry import ShoeRegistry
from toontown.inventory.registry.ShortsRegistry import ShortsRegistry
from toontown.inventory.registry.ChatStickerRegistry import ChatStickerRegistry
from toontown.inventory.registry.CustomSpeedchatRegistry import CustomSpeedchatRegistry
from toontown.inventory.registry.NametagFontRegistry import NametagFontRegistry
from toontown.inventory.registry.CheesyEffectRegistry import CheesyEffectRegistry
from toontown.inventory.registry.EmoteRegistry import EmoteRegistry
from toontown.inventory.registry.FishingRodRegistry import FishingRodRegistry
from toontown.inventory.registry.MaterialRegistry import MaterialRegistry


ItemTypeRegistry: Dict[ItemType, Dict[IntEnum, ItemDefinition]] = {
    ItemType.Profile_Background: ProfileBackgroundRegistry,
    ItemType.Profile_Nameplate: ProfileNameplateRegistry,
    ItemType.Profile_Pose: ProfilePoseRegistry,
    ItemType.Cosmetic_Shirt: ShirtRegistry,
    ItemType.Cosmetic_Shorts: ShortsRegistry,
    ItemType.Cosmetic_Hat: HatRegistry,
    ItemType.Cosmetic_Glasses: GlassesRegistry,
    ItemType.Cosmetic_Backpack: BackpackRegistry,
    ItemType.Cosmetic_Shoes: ShoeRegistry,
    ItemType.Cosmetic_Neck: NeckRegistry,
    ItemType.Social_ChatStickers: ChatStickerRegistry,
    ItemType.Social_CustomSpeedchat: CustomSpeedchatRegistry,
    ItemType.Social_NametagFont: NametagFontRegistry,
    ItemType.Social_CheesyEffect: CheesyEffectRegistry,
    ItemType.Social_Emote: EmoteRegistry,
    ItemType.Fishing_Rod: FishingRodRegistry,
    ItemType.Consumable_Boosters: BoosterRegistry,
    ItemType.Material: MaterialRegistry,
}


def getItemDefinition(itemSubtype: IntEnum) -> Union[ItemDefinition, Any]:
    """
    Retrieves the item definition for a given item subtype.
    """
    itemType: ItemType = ItemType.getItemType(type(itemSubtype))
    if itemType not in ItemTypeRegistry:
        raise KeyError(f"Missing registry information for itemType {itemType}!")
    elif itemSubtype not in ItemTypeRegistry[itemType]:
        raise KeyError(f"Missing registry information for item subtype {itemSubtype} for {itemType}!")
    else:
        return ItemTypeRegistry[itemType][itemSubtype]


# Populate every definition with a reference to its own itemSubtype.
for registry in ItemTypeRegistry.values():
    for itemEnum, itemDef in registry.items():
        itemDef.itemSubtype = itemEnum
