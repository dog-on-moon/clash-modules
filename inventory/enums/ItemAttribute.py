from strenum import StrEnum


class ItemAttribute(StrEnum):
    """
    A string enum list for item attributes.
    Keep the string values short & unique.
    """
    MODEL_COLORSCALE   = 'cs'
    MODIFIER    = 'm'
    MODIFIER_3D = 'm3'
    MODIFIER_2D = 'm2'

    # Clothing / Accessories
    CLOTHES_PRIMARY_COL   = 'a'
    CLOTHES_SECONDARY_COL = 'b'

    # Boosters
    MINUTES = 'i'


# A set of attributes to be removed on items that are being added to inventories.
InventoryStripAttributes: set[ItemAttribute] = {}
