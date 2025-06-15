from toontown.quest3.base.QuestContext import QuestContext


class EarnJellybeanContext(QuestContext):
    """
    Context for when a Toon earns some jellybeans.
    """
    def __init__(self, jellybeans: int) -> None:
        self.jellybeans = jellybeans

    def getJellybeans(self) -> int:
        return self.jellybeans
