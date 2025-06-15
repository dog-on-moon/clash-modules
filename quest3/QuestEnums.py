"""
This module contains all enum data for quests.
"""
from enum import IntEnum, unique, auto


@unique
class QuestSource(IntEnum):
    """
    An enum class representing the sources where Quests may come from.
    Each QuestSource represents a different QuestLine class.

    Do not use Autos here as they are saved on quester DBs.
    """
    MainQuest   = 1


@unique
class QuesterType(IntEnum):
    """
    An enum class for the type of Questers we have.
    """
    Toon = auto()


@unique
class QuestItemName(IntEnum):
    """General IntEnum for quest item names"""
    Moondog                     = auto()
