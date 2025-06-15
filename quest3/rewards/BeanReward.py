"""
Jellybean reward class for quests.
"""
from toontown.quest3.QuestEnums import QuesterType
from toontown.quest3.QuestLocalizer import RWD_Jellybeans
from toontown.quest3.base.QuestReward import QuestReward
from toontown.quest3.base.Quester import Quester


class BeanReward(QuestReward):
    def __init__(self, money: int):
        self.money = money

    def handleReward(self, quester: Quester, multiplier: float = 1.0) -> None:
        if quester.questerType == QuesterType.Toon:
            quester.addMoney(
                deltaMoney=self.getMoney(multiplier=multiplier),
                doAnim=True,
            )

    def getRewardString(self, multiplier: float = 1.0) -> list:
        return [RWD_Jellybeans % self.getMoney(multiplier=multiplier)]

    def attemptCombine(self, other, selfMultiplier: float = 1.0, otherMultiplier: float = 1.0):
        return BeanReward(
            money=self.getMoney(multiplier=selfMultiplier) + other.getMoney(multiplier=otherMultiplier)
        )

    def getMoney(self, multiplier: float = 1.0) -> int:
        return round(self.money * multiplier)

    def __repr__(self):
        return f'BeanReward({self.money})'
