import math

from toontown.quest3.base.QuestObjective import *
from toontown.quest3.context.JungleGameContext import JungleGameContext
from toontown.quest3.QuestLocalizer import (HL_Collect, JungleVines, OBJ_Collect,
                                            OnDaTrolley, PROG_Collect, QuestProgress_Complete,
                                            SC_JungleVines, PFX_SWINGFOR)


class JungleGameObjective(QuestObjective):

    def __init__(self,
                 npc = 2001,
                 rewards=None,
                 nextStep=None,
                 npcReturnable: bool = True,
                 bananaCount: int = None):
        super().__init__(npc=npc, rewards=rewards, nextStep=nextStep, npcReturnable=npcReturnable)
        self.bananaCount = bananaCount

    def calculateProgress(self, context: JungleGameContext, questReference: QuestReference, quester: Quester) -> int:
        if type(context) is not JungleGameContext:
            return 0
        return context.getBananasCollected()

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
        bananaCount = 2.0 * (difficulty ** 1.2)

        # Round off our cog count so that it is pretty.
        bananaCount = math.ceil(bananaCount)
        if bananaCount < 1:
            bananaCount = 1
        elif bananaCount < 10:
            pass
        elif bananaCount < 20:
            bananaCount = round(round(bananaCount / 2) * 2)
        elif bananaCount < 40:
            bananaCount = round(round(bananaCount / 5) * 5)
        else:
            bananaCount = round(round(bananaCount / 20) * 20)

        # Fruit time
        return cls(
            bananaCount=bananaCount,
            npcReturnable=False,
        )
    
    def getCompletionRequirement(self) -> int:
        return self.bananaCount

    def modifyPoster(self, questReference: QuestReference, poster):
        complete = questReference.isQuestComplete(base.localAvatar, self.objectiveIndex)
        searchPoster = poster.CENTER if not (complete and self.npcReturnable) else poster.LEFT

        poster.visual_setFrameColor(searchPoster, 'lightBlue')
        poster.visual_setFrameText(searchPoster, PFX_SWINGFOR + (f'{self.bananaCount} Bananas'
                                                                 if self.bananaCount > 1 else 'a Banana'))

        geom = base.localAvatar.inventory.buttonLookup(1, 0)  # Banana Peel
        poster.visual_setFrameGeom(searchPoster, geom, scale=1.0, pos=(0, 10, 0))

        # If we're complete, bonus info
        if complete:
            if self.npcReturnable:
                poster.visual_setFrameColor(poster.RIGHT, 'lightBlue')
                poster.visual_setNpcFrame(poster.RIGHT, self.getToNpcId())
                poster.visual_setFrameText(poster.RIGHT, self.getToNpcName())
                poster.label_auxillaryText.show()
        else:
            if self.bananaCount > 1:
                value, range, textFormat = self.getProgressFormat(questReference)
                poster.visual_setProgressInfo(value=value, range=range, textFormat=textFormat)

    def getProgressFormat(self, questReference):
        return questReference.getQuestProgress(self.objectiveIndex), self.bananaCount, PROG_Collect

    def getInfoTextStrings(self, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex) and self.npcReturnable:
            return super().getInfoTextStrings(questReference)

        return JungleVines, OnDaTrolley

    def getSpeedchatMessages(self, quester, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(quester, self.objectiveIndex):
            if self.npcReturnable:
                return self.getFinishToontaskStrings()
            return tuple()

        # Get book specific message
        return SC_JungleVines,

    def getHeadline(self, questReference: QuestReference, objectiveSelected: int = 0) -> str:
        return HL_Collect
    
    def getObjectiveGoal(self) -> str:
        return OBJ_Collect % "some Bananas"
    
    def getProgressString(self, questReference: QuestReference, progress: int) -> str:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex):
            return QuestProgress_Complete
        elif self.bananaCount == 1:
            return ''
        return PROG_Collect.format(value=min(progress, self.bananaCount), range=self.bananaCount)
    
    def _getKwargStr(self):
        kwargstr = super()._getKwargStr()
        if self.bananaCount is not None:
            kwargstr += f'bananaCount={self.bananaCount}, '
        return kwargstr

    def __repr__(self):
        return f'JungleGameObjective({self._getKwargStr()[:-2]})'
