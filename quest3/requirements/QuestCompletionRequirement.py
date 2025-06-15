from toontown.quest3.QuestEnums import QuestSource, QuesterType
from .QuestRequirement import QuestRequirement
from ..base.Quester import Quester


class QuestCompletionRequirement(QuestRequirement):
    """
    This requirement checks that the Toon has the specified quest completed.
    """

    def __init__(self, questSource: QuestSource, chainId: int, objectiveId: int=1) -> None:
        self.questSource = questSource
        self.chainId = chainId
        self.objectiveId = objectiveId

    def check(self, quester: Quester):
        if quester.questerType == QuesterType.Toon:
            return quester.hasReachedQuest(self.questSource, self.chainId, self.objectiveId)
        return super().check(quester)
    
    def __repr__(self) -> str:
        return f"QuestCompletionRequirement(QuestSource({self.questSource}), {self.chainId})" 
