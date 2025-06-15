from toontown.quest3.base.QuestObjective import *
from toontown.quest3.objectives import VisitObjective
from toontown.quest3.QuestEnums import QuestItemName
from toontown.quest3.QuestLocalizer import (AuxillaryText_To, HL_Deliver, OBJ_DeliverTo, QuestProgress_Complete,
                                            SC_Deliver, getQuestItemText, PFX_DELIVER)


class DeliverObjective(VisitObjective):
    """
    A quest where you must deliver an item to an NPC.
    """

    poster_canUpdateAux = False

    def __init__(self,
                 npc = 2001,
                 rewards=None,
                 nextStep=None,
                 npcReturnable: bool = True,
                 recoverItem: QuestItemName = QuestItemName.GlassJar):
        super().__init__(npc=npc, rewards=rewards, nextStep=nextStep, npcReturnable=npcReturnable)
        self.recoverItem = recoverItem

    def modifyPoster(self, questReference: QuestReference, poster):
        """
        Given a QuestPoster, update it to match what this objective should be.

        :param questReference:  The poster's quest reference.
        :param poster:          The poster GUI itself.
        :type poster:           QuestPoster
        """
        poster.visual_setFramePackageGeom(poster.LEFT)
        itemName = getQuestItemText(self.recoverItem, capitalizeFirstInSingular=True)
        poster.visual_setFrameColor(poster.LEFT, 'lightGreen')
        poster.visual_setFrameText(poster.LEFT, PFX_DELIVER + itemName)

        poster.visual_setNpcFrame(poster.RIGHT, self.getToNpcId())
        poster.visual_setFrameColor(poster.RIGHT, 'lightGreen')
        poster.visual_setFrameText(poster.RIGHT, self.getToNpcName())

        poster.visual_setAuxText(AuxillaryText_To)
        poster.label_auxillaryText.show()

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
        msg = SC_Deliver.format(getQuestItemText(self.recoverItem))

        # Format messages
        msgs = [msg] + list(self.getFinishToontaskStrings())
        return tuple(msgs)

    def getHeadline(self, questReference: QuestReference, objectiveSelected: int = 0) -> str:
        return HL_Deliver
    
    def getObjectiveGoal(self) -> str:
        return OBJ_DeliverTo % (getQuestItemText(self.recoverItem), self.getToNpcName())
    
    def getProgressString(self, questReference: QuestReference, progress: int) -> str:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex):
            return QuestProgress_Complete
        return ''

    def _getKwargStr(self):
        kwargstr = super()._getKwargStr()
        kwargstr += f'recoverItem=QuestItemName.{QuestItemName(self.recoverItem).name}, '
        return kwargstr

    def __repr__(self):
        return f'DeliverObjective({self._getKwargStr()[:-2]})'
