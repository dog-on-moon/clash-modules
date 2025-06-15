"""
Module class for QuestHistory.
"""
from toontown.quest3.QuestEnums import QuestSource
from toontown.quest3.base.QuestReference import QuestId
from toontown.utils.AstronStruct import AstronStruct


class QuestHistory(AstronStruct):
    """
    Data class for storing if a Quest was completed.
    """

    def __init__(self, questSource: QuestSource, chainId: int):
        self.questSource = questSource
        self.chainId = chainId
    
    def __repr__(self) -> str:
        return f"QuestHistory(questSource={self.questSource}, chainId={self.chainId})"
    
    def __eq__(self, __o) -> bool:
        """
        :type __o: QuestHistory
        """
        if isinstance(__o, QuestHistory):
            return (self.questSource == __o.questSource) and (self.chainId == __o.chainId)
        return False

    def __repr__(self):
        return f'{QuestSource(self.questSource).name} : Chain #{self.chainId}'

    def toStruct(self) -> list:
        return [self.questSource, self.chainId]

    @classmethod
    def fromQuestId(cls, questId: QuestId):
        """Creates a QuestHistory object by quest id reference."""
        return cls(
            questSource=questId.getQuestSource(),
            chainId=questId.getChainId()
        )

    def getQuestSource(self) -> QuestSource:
        return self.questSource

    def getChainId(self):
        return self.chainId
