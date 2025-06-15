from toontown.hood import ZoneUtil
from toontown.quest3.QuestEnums import QuesterType, QuestSource
from toontown.quest3.QuestLocalizer import PROG_Collect, OnTheTrolley, SC_CatchingGame, SC_Fishing, HL_Fish, OBJ_Catch, \
    QuestProgress_Complete, PFX_CATCH
from toontown.quest3.base.QuestObjective import QuestObjective
from toontown.quest3.base.QuestReference import QuestReference
from toontown.quest3.base.Quester import Quester
from toontown.quest3.context.FishingContext import FishingContext
from toontown.toonbase import TTLocalizer
from toontown.toonbase.ToontownGlobals import HoodHierarchy, OldeToontown, OutdoorZone


class FishingObjective(QuestObjective):

    def __init__(self, npc=2001, rewards=None, nextStep=None, npcReturnable: bool = False, zoneUnlocks=None, zoneId: int = 2000, rarity: int = 0, fishReq: int = 1):
        super().__init__(npc, rewards, nextStep, npcReturnable, zoneUnlocks)

        self.zoneId = zoneId
        self.rarity = rarity
        self.fishReq = fishReq

    def calculateProgress(self, context: FishingContext, questReference: QuestReference,  quester: Quester) -> int:
        if type(context) is not FishingContext:
            return 0

        if self.zoneId is not None and ZoneUtil.getHoodId(context.getZoneId()) == self.zoneId:
            # Special case, Playground should match all branch zones
            pass
        elif self.zoneId is not None and context.getZoneId() != self.zoneId:
            # A zone was defined, but it doesn't match the context.
            return 0
        if context.getRarity() < self.rarity:
            return 0
        return 1

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
        if questerType == QuesterType.Club:
            return None, None
        return 1, 45

    @staticmethod
    def getObjectiveWeight(questerType: QuesterType) -> int:
        """
        The likelihood for this objective to be chosen in a pool.
        The de facto amount is 100.
        """
        return 8

    @classmethod
    def generateFromDifficulty(cls, rng, difficulty: float, questSource: QuestSource, **extraArgs):
        """
        Given an arbitrary difficulty value, generate a QuestObjective.
        For more info, seek QuestGenerator.py.

        :param rng:        A seeded Random instance. Use this for .random() or .randint() calculations.
        :param difficulty: The arbitrary difficulty of the task.
        :return:           This QuestObjective, set with values to match the arbitrary difficulty.
        """

        questZone = extraArgs.get("zoneId")
        rarity = min(int(difficulty * 0.35) + 1, 5)
        fishReq = int((8 * difficulty) / (rarity ** 1.3))
        varianceAmount = max(int(lerp(6, 2, rarity/8)), 1)
        fishReq += rng.randint(-varianceAmount, varianceAmount)
        if questZone:
            if questZone == OldeToontown or questZone == OutdoorZone:
                zoneChoices = [questZone]
            else:
                zoneChoices = [questZone] + list(zone for zone in HoodHierarchy.get(questZone, []))
            zoneId = rng.choice(zoneChoices)
        else:
            zoneId = None

        # Fish time
        return cls(
            zoneId=zoneId,
            rarity=rarity,
            fishReq=fishReq,
            npcReturnable=False,
        )

    def getCompletionRequirement(self) -> int:
        return self.fishReq

    def modifyPoster(self, questReference: QuestReference, poster):
        complete = questReference.isQuestComplete(base.localAvatar, self.objectiveIndex)
        searchPoster = poster.CENTER if not (complete and self.npcReturnable) else poster.LEFT

        poster.visual_setFrameColor(searchPoster, 'lightBlue')

        model = loader.loadModel('phase_3.5/models/gui/sos_textures')
        geom = model.find('**/fish')


        poster.visual_setFrameGeom(
            searchPoster,
            geom,
            scale=0.12,
        )

        model.removeNode()

        if self.rarity == 1:
            poster.visual_setFrameText(searchPoster, PFX_CATCH + (f'{self.fishReq} Fish'
                                                                  if self.fishReq > 1 else f'a Fish'))
        else:
            rarityName = TTLocalizer.RarityToString.get(self.rarity)
            if self.rarity < 8:
                rarityName += '+"'
            else:
                rarityName += '"'
            poster.visual_setFrameText(searchPoster, PFX_CATCH + (f'{self.fishReq} "{rarityName} Fish'
                                                                  if self.fishReq > 1 else f'a "{rarityName}" Fish'))

        # If we're complete, bonus info
        if complete:
            if self.npcReturnable:
                poster.visual_setFrameColor(poster.RIGHT, 'lightBlue')
                poster.visual_setNpcFrame(poster.RIGHT, self.getToNpcId())
                poster.visual_setFrameText(poster.RIGHT, self.getToNpcName())
                poster.label_auxillaryText.show()
        else:
            if self.fishReq > 1:
                value, range, textFormat = self.getProgressFormat(questReference)
                poster.visual_setProgressInfo(value=value, range=range, textFormat=textFormat)

    def getProgressFormat(self, questReference):
        return questReference.getQuestProgress(self.objectiveIndex), self.fishReq, PROG_Collect

    def getInfoTextStrings(self, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex) and self.npcReturnable:
            # Return the goal location
            return super().getInfoTextStrings(questReference)
        else:
            # Tell them where the cogs are
            return self.getLocationName(self.zoneId),

    def getSpeedchatMessages(self, quester, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(quester, self.objectiveIndex):
            if self.npcReturnable:
                return self.getFinishToontaskStrings()
            return tuple()

        # Get book specific message
        rarityName = TTLocalizer.RarityToString.get(self.rarity)
        return SC_Fishing % (self.fishReq, rarityName),

    def getHeadline(self, questReference: QuestReference, objectiveSelected: int = 0) -> str:
        return HL_Fish

    def getObjectiveGoal(self) -> str:
        rarityName = TTLocalizer.RarityToString.get(self.rarity)
        return OBJ_Catch % rarityName + ' fish'

    def getProgressString(self, questReference: QuestReference, progress: int) -> str:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex):
            return QuestProgress_Complete
        elif self.fishReq == 1:
            return ''
        return PROG_Collect.format(value=min(progress, self.fishReq), range=self.fishReq)

    def _getKwargStr(self):
        kwargstr = super()._getKwargStr()
        if self.rarity is not None:
            kwargstr += f'rarity={self.rarity}, '
        if self.zoneId is not None:
            kwargstr += f'zoneId={self.zoneId}, '
        return kwargstr

    def __repr__(self):
        return f'FishingObjective({self._getKwargStr()[:-2]})'


FishingObjective()  # hack thanks to main

