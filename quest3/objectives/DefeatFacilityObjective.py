import math

from toontown.quest3.QuestEnums import QuestSource
from toontown.quest3.base.QuestObjective import *
from toontown.quest3.context.DefeatFacilityContext import DefeatFacilityContext
from toontown.quest3.QuestLocalizer import (HL_Infiltrate, OBJ_Infiltrate, PROG_Infiltrate, QuestProgress_Complete,
                                            SC_Infiltrate,
                                            SC_InfiltrateLocation, PFX_INFILTRATE)
from ..daily.DailyConstants import QuestTier
from toontown.toonbase.ToontownGlobals import SellbotFactoryInt, CashbotMintIntA, CashbotMintIntB, CashbotMintIntC, \
    LawbotStageIntA, LawbotStageIntB, LawbotStageIntC, BossbotCountryClubIntA, BossbotCountryClubIntB, \
    BossbotCountryClubIntC, ToontownCentral, DonaldsDock, OldeToontown, DaisyGardens, MinniesMelodyland, TheBrrrgh, \
    SellbotFactorySideInt, SellbotFindForemanInt, SellbotOcFindForemanInt, SellbotOcFindFamilyInt


ExtraFacilityMatches = {
    SellbotFactorySideInt: SellbotFactoryInt,
    SellbotFindForemanInt: SellbotFactoryInt,
    SellbotOcFindForemanInt: SellbotFactoryInt,
    SellbotOcFindFamilyInt: SellbotFactoryInt,
}


class DefeatFacilityObjective(QuestObjective):
    def __init__(self,
                 npc = 2001,
                 rewards=None,
                 nextStep=None,
                 npcReturnable: bool = True,
                 facilityCount: int = 1,
                 facilityId: int = None):
        super().__init__(npc=npc, rewards=rewards, nextStep=nextStep, npcReturnable=npcReturnable)
        self.facilityCount = facilityCount
        self.facilityId = facilityId

    def calculateProgress(self, context: DefeatFacilityContext, questReference: QuestReference, quester: Quester) -> int:
        if type(context) is not DefeatFacilityContext:
            return 0
        # A facility id was specified.
        if self.facilityId is not None:
            # The context's hoodId matches the objective hoodId.
            if ZoneUtil.getHoodId(context.facilityId) == self.hoodId and self.facilityId == self.hoodId:
                return 1
            # The facilityId exists, and it matches the context, OR
            # The context fits an extra match.
            if context.facilityId == self.facilityId or ExtraFacilityMatches.get(context.facilityId) == self.facilityId:
                return 1
            return 0
        # No facility id was specified; anywhere is fine.
        return 1

    """
    Random Task Generation
    """

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
            if zoneId in (ToontownCentral, DonaldsDock, OldeToontown):
                return None
        elif questSource == QuestSource.DailyQuest:
            questTier = extraArgs.get("questTier")
            if questTier in (QuestTier.NEWBIE, QuestTier.TTC, QuestTier.BB, QuestTier.YOTT):
                return

        if questerType == QuesterType.Toon:
            return 3, None
        elif questerType == QuesterType.Club:
            return 25, None
        else:
            return 3, None

    @staticmethod
    def getObjectiveWeight(questerType: QuesterType) -> int:
        """
        The likelihood for this objective to be chosen in a pool.
        The de facto amount is 100.
        """
        return 35

    @classmethod
    def generateFromDifficulty(cls, rng, difficulty: float, questSource: QuestSource, **extraArgs):
        """
        Given an arbitrary difficulty value, generate a QuestObjective.
        For more info, seek QuestGenerator.py.

        :param rng:        A seeded Random instance. Use this for .random() or .randint() calculations.
        :param difficulty: The arbitrary difficulty of the task.
        :return:           This QuestObjective, set with values to match the arbitrary difficulty.
        """
        facilityCount = 0.135 * (difficulty ** 1.2)
        facilityIdDict = {
            SellbotFactoryInt: 0.9,
            CashbotMintIntA: 1.0,
            CashbotMintIntB: 0.8,
            CashbotMintIntC: 0.6,
            LawbotStageIntA: 0.7,
            LawbotStageIntB: 0.55,
            LawbotStageIntC: 0.4,
            BossbotCountryClubIntA: 0.8,
            BossbotCountryClubIntB: 0.55,
            BossbotCountryClubIntC: 0.3,
        }

        if questSource == QuestSource.KudosQuest:
            zoneId = extraArgs.get("zoneId")
            wantedDict = facilityIdDict.copy()

            cashFacilities = (CashbotMintIntA, CashbotMintIntB, CashbotMintIntC)
            lawFacilities = (LawbotStageIntA, LawbotStageIntB, LawbotStageIntC)
            bossFacilities = (BossbotCountryClubIntA, BossbotCountryClubIntB, BossbotCountryClubIntC)

            if zoneId == DaisyGardens:
                for key in (cashFacilities + lawFacilities + bossFacilities):
                    wantedDict.pop(key)
            elif zoneId == MinniesMelodyland:
                for key in (lawFacilities + bossFacilities):
                    wantedDict.pop(key)
            elif zoneId == TheBrrrgh:
                for key in bossFacilities:
                    wantedDict.pop(key)
        else:
            wantedDict = facilityIdDict.copy()

        # 35% chance to be "any" facility type
        if rng.random() <= 0.35:
            facilityId = None
            facilityCount *= 1.2
        else:
            facilityId = rng.choice(list(wantedDict.keys()))
            facilityCount *= facilityIdDict.get(facilityId)
        # Round off our cog count so that it is pretty.
        facilityCount = math.ceil(facilityCount)
        if facilityCount < 1:
            facilityCount = 1
        elif facilityCount < 10:
            pass
        elif facilityCount < 30:
            facilityCount = round(round(facilityCount / 2) * 2)
        else:
            facilityCount = round(round(facilityCount / 5) * 5)

        # Facility time
        return cls(
            facilityCount=facilityCount,
            facilityId=facilityId,
            npcReturnable=False,
        )

    def getLowestToonLevel(self) -> Optional[int]:
        return {
            SellbotFactoryInt: 38,
            CashbotMintIntA: 48,
            CashbotMintIntB: 48,
            CashbotMintIntC: 48,
            LawbotStageIntA: 58,
            LawbotStageIntB: 58,
            LawbotStageIntC: 58,
            BossbotCountryClubIntA: 68,
            BossbotCountryClubIntB: 68,
            BossbotCountryClubIntC: 68,
        }.get(self.facilityId, 38)

    def getCompletionRequirement(self) -> int:
        return self.facilityCount

    def modifyPoster(self, questReference: QuestReference, poster):
        complete = questReference.isQuestComplete(base.localAvatar, self.objectiveIndex)
        cogPoster = poster.CENTER if not (complete and self.npcReturnable) else poster.LEFT
        self.setCogFrame(cogPoster, poster)

        # If we're complete, bonus info
        if complete:
            if self.npcReturnable:
                poster.visual_setFrameColor(poster.RIGHT, 'blue')
                poster.visual_setNpcFrame(poster.RIGHT, self.getToNpcId())
                poster.visual_setFrameText(poster.RIGHT, self.getToNpcName())
                poster.label_auxillaryText.show()
        # And if we're not, show progress
        elif self.facilityCount > 1:
            value, range, textFormat = self.getProgressFormat(questReference)
            poster.visual_setProgressInfo(value=value, range=range, textFormat=textFormat)

    def getProgressFormat(self, questReference):
        return questReference.getQuestProgress(self.objectiveIndex), self.facilityCount, PROG_Infiltrate

    def setCogFrame(self, cogPoster, poster, declarative=False):
        poster.visual_setFrameColor(cogPoster, 'blue')
        poster.visual_setFrameText(cogPoster, PFX_INFILTRATE + self.getCogNameString(declarative=declarative))
        if self.facilityDept is None:
            # Random facility icon
            questIcons = loader.loadModel('phase_3.5/models/gui/quests/ttcc_quest_icons')
            bossGeom = questIcons.find('**/facility')
            questIcons.removeNode()
            poster.visual_setFrameGeom(
                positionIndex=cogPoster,
                geom=bossGeom,
                scale=0.13
            )
        else:
            poster.visual_setFacilityGeom(cogPoster, self.facilityDept)

    def getInfoTextStrings(self, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex) and self.npcReturnable:
            # Return the goal location
            return super().getInfoTextStrings(questReference)
        else:
            # Tell them where the cogs are
            return self.getLocationName(self.hoodId),

    def getSpeedchatMessages(self, quester, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(quester, self.objectiveIndex):
            if self.npcReturnable:
                return self.getFinishToontaskStrings()
            return tuple()

        # Get the message formatting.
        cogName = self.getCogNameString(speedchat=True)
        if self.facilityId is None:
            message = SC_Infiltrate
            return message % cogName,
        else:
            message = SC_InfiltrateLocation
            locName = self.getLocationName(zoneId=self.hoodId)
            return message % (cogName, locName),

    def getHeadline(self, questReference: QuestReference, objectiveSelected: int = 0) -> str:
        return HL_Infiltrate
    
    @property
    def hoodId(self):
        """Grab the hoodId from the facilityId, if it exists.
        """
        if self.facilityId is None:
            return
        return ZoneUtil.getHoodId(self.facilityId)
    
    @property
    def facilityDept(self):
        """Return the "department" of the facility based on its facility id,
        which is a zoneId.
        """
        if self.facilityId is None:
            return None

        for zoneIds, dept in ToontownGlobals.FacilityIdToDept.items():
            if self.facilityId in zoneIds or self.facilityId == ZoneUtil.getHoodId(zoneIds[0]):
                return dept

    """text makin methods"""

    def getCogNameString(self, forcePlural=False, declarative=False, speedchat=False):
        hoodId = self.hoodId

        if self.facilityDept is None:
            if hoodId is not None:
                if self.facilityCount == 1:
                    return TTLocalizer.getFacilityName(hoodId, index=1)
                return f"{self.facilityCount} {TTLocalizer.getFacilityName(hoodId, index=2)}"

            if self.facilityCount == 1:
                if speedchat:
                    return "a Cog Facility"
                else:
                    return "A Cog Facility"
            return f"{self.facilityCount} Cog Facilities"

        if self.facilityCount == 1:
            if speedchat:
                return TTLocalizer.getFacilityName(self.facilityId, index=1)
            else:
                text = TTLocalizer.getFacilityName(self.facilityId, index=1)
                return text[0].upper() + text[1:]
        return f"{self.facilityCount} {TTLocalizer.getFacilityName(self.facilityId, index=2)}"
    
    def getObjectiveGoal(self) -> str:
        return OBJ_Infiltrate % self.getCogNameString()

    def getProgressString(self, questReference: QuestReference, progress: int) -> str:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex):
            return QuestProgress_Complete
        elif self.facilityCount == 1:
            return ''
        return PROG_Infiltrate.format(value=min(progress, self.facilityCount), range=self.facilityCount)

    def _getKwargStr(self):
        kwargstr = super()._getKwargStr()
        if self.facilityId is not None:
            kwargstr += f'facilityId={self.facilityId}, '
        if self.facilityCount != 1:
            kwargstr += f'facilityCount={self.facilityCount}, '
        return kwargstr

    def __repr__(self):
        return f'DefeatFacilityObjective({self._getKwargStr()[:-2]})'
