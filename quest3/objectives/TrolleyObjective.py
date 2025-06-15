from toontown.quest3.base.QuestObjective import *
from toontown.quest3.context.TrolleyContext import TrolleyContext
from toontown.quest3.QuestLocalizer import (HL_Trolley, InThePlayground, QuestProgress_Complete,
                                            RideTheTrolley, SC_Trolley)


class TrolleyObjective(QuestObjective):

    def __init__(self,
                 npc = 2001,
                 rewards=None,
                 nextStep=None,
                 npcReturnable: bool=True):
        # override to set npcReturnable default to True
        super().__init__(npc=npc, rewards=rewards, nextStep=nextStep, npcReturnable=npcReturnable)

    def calculateProgress(self, context: TrolleyContext, questReference: QuestReference, quester: Quester) -> int:
        return type(context) is TrolleyContext

    def modifyPoster(self, questReference: QuestReference, poster):
        # Complete flag
        complete = questReference.isQuestComplete(base.localAvatar, self.objectiveIndex)

        # Set poster constants
        searchPoster = poster.CENTER if not (complete and self.npcReturnable) else poster.LEFT
        poster.visual_setFrameColor(searchPoster, 'lightBlue')
        poster.visual_setTrolleyGeom(searchPoster)
        poster.visual_setFrameText(searchPoster, RideTheTrolley)

        # If we're complete, bonus info
        if complete:
            if self.npcReturnable:
                poster.visual_setFrameColor(poster.RIGHT, 'lightBlue')
                poster.visual_setNpcFrame(poster.RIGHT, self.getToNpcId())
                poster.visual_setFrameText(poster.RIGHT, self.getToNpcName())
                poster.label_auxillaryText.show()
        else:
            # Misc stuff to show when incomplete
            pass

    def getInfoTextStrings(self, questReference: QuestReference) -> tuple:
        # If we're complete and demand NPC completion, point to NPC instead
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex) and self.npcReturnable:
            return super().getInfoTextStrings(questReference)

        return InThePlayground,

    def getSpeedchatMessages(self, quester, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(quester, self.objectiveIndex):
            if self.npcReturnable:
                return self.getFinishToontaskStrings()
            return tuple()
        return SC_Trolley,

    def getHeadline(self, questReference: QuestReference, objectiveSelected: int = 0) -> str:
        return HL_Trolley
    
    def getObjectiveGoal(self) -> str:
        return RideTheTrolley
    
    def getProgressString(self, questReference: QuestReference, progress: int) -> str:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex):
            return QuestProgress_Complete
        return ''

    def __repr__(self):
        return f'TrolleyObjective({self._getKwargStr()[:-2]})'
