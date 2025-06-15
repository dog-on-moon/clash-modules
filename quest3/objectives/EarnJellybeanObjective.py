import math

from toontown.quest3.base.QuestObjective import *
from toontown.quest3.context.EarnJellybeanContext import EarnJellybeanContext
from toontown.quest3.QuestLocalizer import (AuxillaryText_To, HL_Earn, OBJ_Earn,
                                            PROG_Earn, QuestProgress_Complete, SC_DeliverJbs, PFX_EARN, SC_EarnJbs,
                                            Anywhere)
from toontown.toon.npc.NPCToonConstants import NPCToonEnum


class EarnJellybeanObjective(QuestObjective):
    def __init__(self,
                 npc=2001,
                 rewards=None,
                 nextStep=None,
                 npcReturnable: bool = False,
                 jellybeans: int = 1):
        super().__init__(npc=npc, rewards=rewards, nextStep=nextStep, npcReturnable=npcReturnable)
        self.jellybeans = jellybeans

    def calculateProgress(self, context: EarnJellybeanContext, questReference: QuestReference, quester: Quester) -> int:
        if type(context) is not EarnJellybeanContext:
            return 0
        return context.getJellybeans()

    @staticmethod
    def getDifficultyRange(questerType: QuesterType, questSource: QuestSource, **extraArgs):
        """
        Returns the difficulty range required to use this objective in random quest generation.

        :return: Any of the following:
                 A) Two floats, for a lower and upper bound
                 B) A float and None, for a lower bound and no upper bound
                 C) None and a float, for no lower bound and an upper bound
                 D) Two nones, for no difficulty bound
                 E) One none, for "cannot be used"
        """
        return None, None

    @staticmethod
    def getObjectiveWeight(questerType: QuesterType) -> int:
        """
        The likelihood for this objective to be chosen in a pool.
        The de facto amount is 100.
        """
        return 9

    @classmethod
    def generateFromDifficulty(cls, rng, difficulty: float, questSource: QuestSource, **extraArgs):
        """
        Given an arbitrary difficulty value, generate a QuestObjective.
        For more info, seek QuestGenerator.py.

        :param rng:        A seeded Random instance. Use this for .random() or .randint() calculations.
        :param difficulty: The arbitrary difficulty of the task.
        :return:           This QuestObjective, set with values to match the arbitrary difficulty.
        """
        jellybeans = 50 * difficulty ** 1.8
        jellybeans += lerp(-jellybeans*0.1, jellybeans*0.1, rng.random())

        # Round off our jellybean count so that it is pretty.
        jellybeans = math.ceil(jellybeans)
        if jellybeans < 1:
            jellybeans = 1
        elif jellybeans < 10:
            pass
        elif jellybeans < 20:
            jellybeans = round(round(jellybeans / 2) * 2)
        elif jellybeans < 50:
            jellybeans = round(round(jellybeans / 5) * 5)
        else:
            jellybeans = round(round(jellybeans / 10) * 10)

        # It's earning time
        return cls(
            jellybeans=jellybeans,
            npcReturnable=False,
        )

    def modifyPoster(self, questReference: QuestReference, poster):
        complete = questReference.isQuestComplete(base.localAvatar, self.objectiveIndex)
        searchPoster = poster.CENTER if not (complete and self.npcReturnable) else poster.LEFT

        lIconGeom = loader.loadModel('phase_3.5/models/gui/jar_gui')
        poster.visual_setFrameGeom(searchPoster, geom=lIconGeom, scale=0.25)
        poster.visual_setFrameColor(searchPoster, 'lightGreen')
        poster.visual_setFrameText(searchPoster, PFX_EARN + f"{self.jellybeans} Jellybeans")

        if not complete:
            value, range, textFormat = self.getProgressFormat(questReference)
            poster.visual_setProgressInfo(value=value, range=range, textFormat=textFormat)
        else:
            if self.npcReturnable:
                poster.visual_setFrameColor(poster.RIGHT, 'lightGreen')
                poster.visual_setNpcFrame(poster.RIGHT, self.getToNpcId())
                poster.visual_setFrameText(poster.RIGHT, self.getToNpcName())
                poster.label_auxillaryText.show()

        lIconGeom.removeNode()

    def getProgressFormat(self, questReference):
        return questReference.getQuestProgress(self.objectiveIndex), self.jellybeans, PROG_Earn

    def getSpeedchatMessages(self, quester, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(quester, self.objectiveIndex):
            if self.npcReturnable:
                return self.getFinishToontaskStrings()
            return tuple()

        return (SC_EarnJbs,)

    def getHeadline(self, questReference: QuestReference, objectiveSelected: int = 0) -> str:
        return HL_Earn

    def getCompletionRequirement(self) -> int:
        return self.jellybeans

    def getObjectiveGoal(self) -> str:
        return OBJ_Earn % (self.jellybeans, "Jellybeans")

    def getProgressString(self, questReference: QuestReference, progress: int) -> str:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex):
            return QuestProgress_Complete
        elif self.jellybeans == 1:
            return ''
        return PROG_Earn.format(value=min(progress, self.jellybeans), range=self.jellybeans)

    def getInfoTextStrings(self, questReference: QuestReference) -> tuple:
        # If we're complete and demand NPC completion, point to NPC instead
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex) and self.npcReturnable:
            return super().getInfoTextStrings(questReference)

        return Anywhere,

    def _getKwargStr(self):
        kwargstr = super()._getKwargStr()
        if self.jellybeans != 1:
            kwargstr += f'jellybeans={self.jellybeans}, '
        return kwargstr

    def __repr__(self):
        return f'EarnJellybeanObjective({self._getKwargStr()[:-2]})'


EarnJellybeanObjective()  # Main
