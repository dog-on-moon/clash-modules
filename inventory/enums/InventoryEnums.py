"""
A module file containing the different types of inventories that may exist.
"""
from enum import IntEnum


class InventoryType(IntEnum):
    """
    The different types of inventory that may exist.
    """
    FullBehavior = 0
    Test   = 1

    Player = 10
    Chest  = 11
    Cache  = 12


class InventoryAction(IntEnum):
    """
    The different base 'actions' that can occur
    in a given inventory.
    """
    ADD     = 1
    REMOVE  = 2
    EQUIP   = 3
    UNEQUIP = 4
    UPDATE  = 5


