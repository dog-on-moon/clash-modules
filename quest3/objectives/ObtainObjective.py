from toontown.quest3.base.QuestObjective import *
from toontown.quest3.objectives import DeliverObjective
from toontown.quest3.QuestLocalizer import (AuxillaryText_From, HL_Obtain, OBJ_Obtain,
                                            SC_Obtain, getQuestItemText, PFX_OBTAIN)


class ObtainObjective(DeliverObjective):
    """
    A quest where you must obtain an item from an NPC.
    """

    def modifyPoster(self, questReference: QuestReference, poster):
        super().modifyPoster(questReference, poster)
        itemName = getQuestItemText(self.recoverItem, capitalizeFirstInSingular=True)
        poster.visual_setFrameText(poster.LEFT, PFX_OBTAIN + itemName)
        poster.visual_setAuxText(AuxillaryText_From)

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

        # Get delivery specific message
        msg = SC_Obtain % getQuestItemText(self.recoverItem)

        # Format messages
        msgs = [msg] + list(self.getFinishToontaskStrings())
        return tuple(msgs)

    def getHeadline(self, questReference: QuestReference, objectiveSelected: int = 0) -> str:
        return HL_Obtain
    
    def getObjectiveGoal(self) -> str:
        return OBJ_Obtain % getQuestItemText(self.recoverItem)

    def __repr__(self):
        return f'ObtainObjective({self._getKwargStr()[:-2]})'
