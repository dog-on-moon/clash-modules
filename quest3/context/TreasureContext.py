from toontown.quest3.base.QuestContext import QuestContext


class TreasureContext(QuestContext):
    """
    Context for when a Toon picks up a treasure.
    """
    
    def __init__(self, treasureType: int) -> None:
        self.treasureType = treasureType
    
    def getTreasureType(self) -> int:
        return self.treasureType
