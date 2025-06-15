"""
Toon Experience reward class for quests.
"""
from toontown.quest3.QuestEnums import QuesterType
from toontown.quest3.QuestLocalizer import RWD_ToonExp
from toontown.quest3.base.QuestReward import QuestReward
from toontown.quest3.base.Quester import Quester


class ExpReward(QuestReward):

    def __init__(self, toonExp: int):
        self.toonExp = toonExp

    def handleReward(self, quester: Quester, multiplier: float = 1.0) -> None:
        if quester.questerType == QuesterType.Toon:
            quester.addToonExp(self.getToonExp(multiplier=multiplier))

    def getRewardString(self, multiplier: float = 1.0) -> list:
        return [RWD_ToonExp % self.getToonExp(multiplier=multiplier)]

    def attemptCombine(self, other, selfMultiplier: float = 1.0, otherMultiplier: float = 1.0):
        return ExpReward(
            toonExp=self.getToonExp(multiplier=selfMultiplier) + other.getToonExp(multiplier=otherMultiplier)
        )

    def getToonExp(self, multiplier: float = 1.0) -> int:
        return round(self.toonExp * multiplier)

    def __repr__(self):
        return f'ExpReward({self.toonExp})'
