"""
Teleport reward class for quests.
"""
from toontown.hood.ZoneUtil import zoneIdToName
from toontown.quest3.QuestEnums import QuesterType
from toontown.quest3.QuestLocalizer import RWD_TPAccess
from toontown.quest3.base.QuestReward import QuestReward
from toontown.quest3.base.Quester import Quester


class TeleportReward(QuestReward):
    def __init__(self, zoneId: int):
        self.zoneId = zoneId

    def handleReward(self, quester: Quester, multiplier: float = 1.0) -> None:
        if quester.questerType == QuesterType.Toon:
            quester.addTeleportAccess(self.zoneId)

    def getRewardString(self, multiplier: float = 1.0) -> list:
        return [RWD_TPAccess % zoneIdToName(self.zoneId)[0]]

    def __repr__(self):
        return f'TeleportReward({self.zoneId})'
