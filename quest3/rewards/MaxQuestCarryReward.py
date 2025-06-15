"""
Max quest carry size reward class for quests.
"""
from toontown.quest3.QuestEnums import QuesterType
from toontown.quest3.base.QuestReward import QuestReward
from toontown.quest3.base.Quester import Quester


class MaxQuestCarryReward(QuestReward):

    def __init__(self, newCarryLimit: int):
        self.newCarryLimit = newCarryLimit

    def handleReward(self, quester: Quester, multiplier: float = 1.0) -> None:
        if quester.questerType == QuesterType.Toon:
            quester.b_setQuestCarryLimit(limit=self.newCarryLimit)

    def getRewardString(self, multiplier: float = 1.0) -> list:
        return []

    def __repr__(self):
        return f'MaxQuestCarryReward({self.newCarryLimit})'
