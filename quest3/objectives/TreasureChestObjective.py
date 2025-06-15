import math

from toontown.quest3.base.QuestObjective import *
from toontown.quest3.context.TreasureChestContext import TreasureChestContext
from toontown.quest3.QuestLocalizer import (HL_Collect, OBJ_Collect, OnDaTrolley,
                                            PROG_Collect, QuestProgress_Complete, SC_TreasureChest, TreasureDive,
                                            PFX_DIVEFOR)


class TreasureChestObjective(QuestObjective):

    def __init__(self,
                 npc = 2001,
                 rewards=None,
                 nextStep=None,
                 npcReturnable: bool = True,
                 chestCount: int = 1):
        super().__init__(npc=npc, rewards=rewards, nextStep=nextStep, npcReturnable=npcReturnable)
        self.chestCount = chestCount

    def calculateProgress(self, context: TreasureChestContext, questReference: QuestReference, quester: Quester) -> int:
        if type(context) is not TreasureChestContext:
            return 0
        return context.getChestsCollected()

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
        if questSource == QuestSource.KudosQuest:
            zoneId = extraArgs.get("zoneId")
            if zoneId not in (ToontownGlobals.ToontownCentral, ToontownGlobals.DonaldsDock, ToontownGlobals.OldeToontown):
                return None
            return None, None

        return None  # die

    @staticmethod
    def getObjectiveWeight(questerType: QuesterType) -> int:
        """
        The likelihood for this objective to be chosen in a pool.
        The de facto amount is 100.
        """
        return 4

    @classmethod
    def generateFromDifficulty(cls, rng, difficulty: float, questSource: QuestSource, **extraArgs):
        """
        Given an arbitrary difficulty value, generate a QuestObjective.
        For more info, seek QuestGenerator.py.

        :param rng:        A seeded Random instance. Use this for .random() or .randint() calculations.
        :param difficulty: The arbitrary difficulty of the task.
        :return:           This QuestObjective, set with values to match the arbitrary difficulty.
        """
        chestCount = 0.8 * (difficulty**1.2)

        # Round off our cog count so that it is pretty.
        chestCount = round(chestCount)
        if chestCount < 1:
            chestCount = 1

        # Chest time
        return cls(
            chestCount=int(chestCount),
            npcReturnable=False,
        )

    def getCompletionRequirement(self) -> int:
        return self.chestCount

    def modifyPoster(self, questReference: QuestReference, poster):
        complete = questReference.isQuestComplete(base.localAvatar, self.objectiveIndex)
        searchPoster = poster.CENTER if not (complete and self.npcReturnable) else poster.LEFT

        poster.visual_setFrameColor(searchPoster, 'lightBlue')
        poster.visual_setFrameText(searchPoster, PFX_DIVEFOR + (f'{self.chestCount} Treasure Chests'
                                                                if self.chestCount > 1 else 'a Treasure Chest'))

        bookModel = loader.loadModel('phase_3.5/models/gui/material_icons')
        geom = bookModel.find('**/material_treasure')
        poster.visual_setFrameGeom(searchPoster, geom, scale=1.0, pos=(0, 10, 0))
        bookModel.removeNode()

        # If we're complete, bonus info
        if complete:
            if self.npcReturnable:
                poster.visual_setFrameColor(poster.RIGHT, 'lightBlue')
                poster.visual_setNpcFrame(poster.RIGHT, self.getToNpcId())
                poster.visual_setFrameText(poster.RIGHT, self.getToNpcName())
                poster.label_auxillaryText.show()
        else:
            if self.chestCount > 1:
                value, range, textFormat = self.getProgressFormat(questReference)
                poster.visual_setProgressInfo(value=value, range=range, textFormat=textFormat)

    def getProgressFormat(self, questReference):
        return questReference.getQuestProgress(self.objectiveIndex), self.chestCount, PROG_Collect

    def getInfoTextStrings(self, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex) and self.npcReturnable:
            return super().getInfoTextStrings(questReference)

        return TreasureDive, OnDaTrolley

    def getSpeedchatMessages(self, quester, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(quester, self.objectiveIndex):
            if self.npcReturnable:
                return self.getFinishToontaskStrings()
            return tuple()

        # Get book specific message
        return SC_TreasureChest,

    def getHeadline(self, questReference: QuestReference, objectiveSelected: int = 0) -> str:
        return HL_Collect
    
    def getObjectiveGoal(self) -> str:
        return OBJ_Collect % "some Treasure Chests"
    
    def getProgressString(self, questReference: QuestReference, progress: int) -> str:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex):
            return QuestProgress_Complete
        elif self.chestCount == 1:
            return ''
        return PROG_Collect.format(value=min(progress, self.chestCount), range=self.chestCount)

    def _getKwargStr(self):
        kwargstr = super()._getKwargStr()
        if self.chestCount != 1:
            kwargstr += f'chestCount={self.chestCount}, '
        return kwargstr

    def __repr__(self):
        return f'TreasureChestObjective({self._getKwargStr()[:-2]})'
