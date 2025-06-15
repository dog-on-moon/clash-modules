from toontown.quest3.base.QuestContext import QuestContext


class IceGameContext(QuestContext):
    """
    Context for when a Toon completes the ice game.
    """
    
    def __init__(self, treasures: int, zoneId: int) -> None:
        self.treasures = treasures
        self.zoneId = zoneId
    
    def getTreasuresCollected(self) -> int:
        return self.treasures
    
    def getZoneId(self) -> int:
        return self.zoneId
