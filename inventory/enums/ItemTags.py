"""
A module containing enum information for items.
"""
from strenum import StrEnum
from typing import List, Set


class ItemCategory(StrEnum):
    """
    The main headline categories for items.
    Returned by ItemDefinition.
    """
    All       = 'All'
    Materials = 'Materials'
    Battle    = 'Battle'
    Cosmetic  = 'Cosmetic'
    Games     = 'Games'
    Misc      = 'Misc'


# Default item category in the filterer.
DefaultItemCategory: ItemCategory = ItemCategory.All

# A constant referring to the item category which contains everything.
GlobalItemCategory: ItemCategory = ItemCategory.All


class ItemTag(StrEnum):
    """
    A 'tag' for items.
    ItemDefinition builds and returns a big list of these.
    """
    DefaultSticker = 'Basic Sticker'
    SuitSticker    = 'Suit Sticker'
    StickersFoil   = 'Foil Sticker'

    RarityCommon    = 'Common'
    RarityUncommon  = 'Uncommon'
    RarityRare      = 'Rare'
    RarityVeryRare  = 'Very Rare'
    RarityUltraRare = 'Ultra Rare'
    RarityLegendary = 'Legendary'
    RarityMythic    = 'Mythic'
    RarityEvent     = 'Event Item'

    Accessory = 'Accessory'
    Hat = 'Head Accessory'
    Glasses = 'Glasses'
    Backpack = 'Backpack'
    Shoes = 'Shoes'
    NeckAcc = 'Neck Accessory'

    FishingRod = 'Fishing Rod'


# A list containing all sets of conflicting tags.
# These tags have no overlap between them.
ConflictingTags: List[Set[ItemTag]] = [
    # Item Rarity Tags
    {ItemTag.RarityCommon,   ItemTag.RarityUncommon,  ItemTag.RarityRare,
     ItemTag.RarityVeryRare, ItemTag.RarityUltraRare, ItemTag.RarityLegendary,
     ItemTag.RarityMythic,   ItemTag.RarityEvent},
    # Accessory Subtypes
    {ItemTag.Hat, ItemTag.Glasses, ItemTag.Backpack,
     ItemTag.Shoes, ItemTag.NeckAcc,
     ItemTag.FishingRod, ItemTag.DefaultSticker, ItemTag.SuitSticker},
    # Item Types
    {ItemTag.Accessory, ItemTag.FishingRod,
     ItemTag.DefaultSticker, ItemTag.SuitSticker}
]


class ItemFilterType(StrEnum):
    """
    The different high-level filtering options for items.
    """
    Recent       = 'Recent'
    Alphabetical = 'Alphabetical'
    Rarity       = 'Rarity'


# The default filter type.
DefaultFilterType: ItemFilterType = ItemFilterType.Recent
