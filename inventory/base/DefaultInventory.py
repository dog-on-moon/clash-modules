"""
This module is responsible for creating the default inventory for Toons.
"""
from toontown.inventory.base.Inventory import Inventory
from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.enums import ItemEnums
from toontown.inventory.enums.InventoryEnums import InventoryType


DefaultItems = [
    ItemEnums.ChatStickersItemType.DisgustGator,
    ItemEnums.ChatStickersItemType.ConcernedDog,
    ItemEnums.ChatStickersItemType.ConfusedKangaroo,
    ItemEnums.ChatStickersItemType.CryCat,
    ItemEnums.ChatStickersItemType.GriefKiwi,
    ItemEnums.ChatStickersItemType.BlushBat,
    ItemEnums.ChatStickersItemType.GrinDuck,
    ItemEnums.ChatStickersItemType.HeartRabbit,
    ItemEnums.ChatStickersItemType.GreenedCat,
    ItemEnums.ChatStickersItemType.PensiveFox,
    ItemEnums.ChatStickersItemType.PleadingDog,
    ItemEnums.ChatStickersItemType.SadBat,
    ItemEnums.ChatStickersItemType.SurprisedArmadillo,
    ItemEnums.ChatStickersItemType.SurprisedRaccoon,
    ItemEnums.ChatStickersItemType.SusBeaver,
    ItemEnums.ChatStickersItemType.WinkDeer,

    ItemEnums.EmoteItemType.Wave,
    ItemEnums.EmoteItemType.Happy,
    ItemEnums.EmoteItemType.Sad,
    ItemEnums.EmoteItemType.Angry,
    ItemEnums.EmoteItemType.Sleepy,
    ItemEnums.EmoteItemType.Yes,
    ItemEnums.EmoteItemType.No,

    ItemEnums.NametagFontItemType.Basic,

    ItemEnums.FishingRodItemType.Cardboard,
]

DefaultEquips = [
    ItemEnums.BackgroundItemType.Default,
    ItemEnums.ProfilePoseItemType.Neutral,
    ItemEnums.NameplateItemType.DefaultBlue,
]


def getDefaultInventory() -> Inventory:
    """
    Creates the player's default inventory.
    """
    # Start with player inventory.
    inventory = Inventory(inventoryType=InventoryType.Player)

    # Add and equip everything.
    for subitemType in DefaultItems:
        invItem = InventoryItem.fromSubtype(subitemType)
        inventory.addItem(invItem)
    for subitemType in DefaultEquips:
        invItem = InventoryItem.fromSubtype(subitemType)
        inventory.addItem(invItem)
        inventory.equipItem(invItem)

    # And just like that -- we're done!!
    return inventory
