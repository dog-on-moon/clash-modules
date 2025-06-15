from toontown.hood import ZoneUtil
from toontown.quest3.base.QuestContext import QuestContext

class FishingContext(QuestContext):

    def __init__(self, rarity: int, zoneId: int) -> None:
        self.rarity = rarity
        self.zoneId = zoneId

    def getRarity(self) -> int:
        return self.rarity

    def getZoneId(self) -> int:
        return ZoneUtil.getBranchZone(self.zoneId)
