from toontown.quest3.base.QuestContext import QuestContext


class TreasureChestContext(QuestContext):
    """
    Context for when a Treasure Dive chest is collected.
    """

    def __init__(self, chests: int):
        self.chests = chests

    def getChestsCollected(self) -> int:
        return self.chests
