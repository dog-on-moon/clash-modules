"""
Defining a quest where you simply have to visit an NPC for an objective.
"""
from toontown.quest3.base.QuestObjective import *
from toontown.quest3.context.NPCInteractContext import NPCInteractContext
from toontown.quest3.QuestLocalizer import HL_Visit, QuestProgress_Complete, OBJ_Visit, PFX_VISIT


class VisitObjective(QuestObjective):
    """
    A quest where you must visit an NPC.
    """

    def __init__(self,
                 npc=2001,
                 rewards=None,
                 nextStep=None,
                 npcReturnable: bool = True,
                 zoneUnlocks=None):
        super().__init__(npc=npc, rewards=rewards, nextStep=nextStep, npcReturnable=npcReturnable, zoneUnlocks=zoneUnlocks)

    def calculateProgress(self, context: NPCInteractContext, questReference: QuestReference, quester: Quester) -> int:
        """
        Figures out how much progress we should accumulate,
        based on the attributes of the given QuestContext.
        :param context: Some QuestContext object.
        :return: An integer remarking progress.
        """
        if type(context) is not NPCInteractContext:
            return 0
        if context.getNpcId() == self.getToNpcId():
            return 1
        return 0

    def modifyPoster(self, questReference: QuestReference, poster):
        """
        Given a QuestPoster, update it to match what this objective should be.

        :param questReference:  The poster's quest reference.
        :param poster:          The poster GUI itself.
        :type poster:           QuestPoster
        """
        poster.visual_setNpcFrame(poster.CENTER, self.getToNpcId())
        poster.visual_setFrameColor(poster.CENTER, 'brown')
        poster.visual_setFrameText(poster.CENTER, PFX_VISIT + self.getToNpcName())

    def getSpeedchatMessages(self, quester, questReference: QuestReference) -> tuple:
        """
        Given a QuestReference, return Speedchat messages to be expressed.

        If you need the text to change when the poster is green/completed,
        you can determine that by checking questReference.isQuestComplete(self.objectiveIndex).

        :param questReference: The quest reference to use.
        :return: Speedchat messages, formatted and wrapped in a tuple.
        """
        if questReference.isQuestComplete(quester, self.objectiveIndex):
            return tuple()
        if self.npcReturnable:
            return self.getFinishToontaskStrings()
        return tuple()

    def getHeadline(self, questReference: QuestReference, objectiveSelected: int = 0) -> str:
        return HL_Visit
    
    def getObjectiveGoal(self) -> str:
        return OBJ_Visit % self.getToNpcName()
    
    def getProgressString(self, questReference: QuestReference, progress: int) -> str:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex):
            return QuestProgress_Complete
        return ''

    def __repr__(self):
        return f'VisitObjective({self._getKwargStr()[:-2]})'
