"""
Laff point reward class for quests.
"""
from toontown.quest3.QuestEnums import QuesterType
from toontown.quest3.QuestLocalizer import RWD_Laff
from toontown.quest3.base.QuestReward import QuestReward
from toontown.quest3.base.Quester import Quester
from toontown.toonbase import ToontownGlobals


class LaffReward(QuestReward):

    def __init__(self, boost: int):
        self.boost = boost

    def handleReward(self, quester: Quester, multiplier: float = 1.0) -> None:
        if quester.questerType == QuesterType.Toon:
            maxHp = quester.getTrueMaxHp()
            maxHp = min(ToontownGlobals.MaxHpLimit, maxHp + self.boost)
            quester.b_setMaxHp(maxHp)
            quester.toonUp(maxHp)

    def getRewardString(self, multiplier: float = 1.0) -> list:
        return [RWD_Laff % self.boost]

    def __repr__(self):
        return f'LaffReward({self.boost})'
