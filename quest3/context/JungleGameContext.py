from toontown.quest3.base.QuestContext import QuestContext


class JungleGameContext(QuestContext):
    """
    Context for when a Toon completes the vine game.
    """
    
    def __init__(self, bananas: int) -> None:
        self.bananas = bananas
    
    def getBananasCollected(self) -> int:
        return self.bananas
