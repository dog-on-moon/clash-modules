"""
Module for NPC interaction contexts
"""
from toontown.quest3.QuestEnums import QuestItemName
from toontown.quest3.base.QuestContext import QuestContext


class QuestFishContext(QuestContext):

    def __init__(self, fish: QuestItemName):
        self.fish = fish

    def getQuestFish(self) -> QuestItemName:
        """Returns the epic catch."""
        return self.fish
