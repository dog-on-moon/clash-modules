"""
Module for av entering a new zone
"""
from toontown.quest3.base.QuestContext import QuestContext


class ZoneContext(QuestContext):

    def __init__(self, zoneId: int):
        self.zoneId = zoneId

    def getZoneId(self) -> int:
        return self.zoneId
