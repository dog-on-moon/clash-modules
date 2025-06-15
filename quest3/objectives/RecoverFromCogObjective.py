import math

from toontown.quest3.base.QuestObjective import *
from toontown.quest3.context.DefeatCogContext import DefeatCogContext
from toontown.quest3.objectives import DefeatCogObjective
from toontown.quest3.QuestEnums import QuestItemName
from toontown.quest3.QuestLocalizer import (AuxillaryText_Complete,
                                            AuxillaryText_From, HL_Recover, OBJ_Recover,
                                            PROG_Recover, QuestItemNames,
                                            SC_RecoverCogs, itemTuple2Word,
                                            QuestProgress_Complete, PFX_RECOVER)


class RecoverFromCogObjective(DefeatCogObjective):
    """Same as DefeatCogObjective, but with a 'recover' tag."""

    def __init__(self,
                 npc = 2001,
                 rewards=None,
                 nextStep=None,
                 npcReturnable: bool = True,
                 zoneUnlocks=None,
                 cogLocation: int = None,
                 cogType: str = None,
                 cogLevelMin: int = None,
                 cogTrack: str = None,
                 skelecog: bool = False,
                 virtual: bool = False,
                 revives: bool = False,
                 executive: bool = False,
                 recoverItem: QuestItemName = QuestItemName.ExerciseSupplies,
                 recoverChance: float = 0.8,
                 recoverRequired: int = 1,
                 *args, **kwargs):
        super().__init__(npc=npc, rewards=rewards, nextStep=nextStep, npcReturnable=npcReturnable, zoneUnlocks=zoneUnlocks,
                         cogLocation=cogLocation, cogType=cogType, cogLevelMin=cogLevelMin, cogTrack=cogTrack,
                         skelecog=skelecog, virtual=virtual, revives=revives, executive=executive, *args, **kwargs)
        self.recoverItem = recoverItem
        self.recoverChance = recoverChance
        self.recoverRequired = recoverRequired

    def calculateProgress(self, context: DefeatCogContext, questReference: QuestReference, quester: Quester) -> int:
        # Get our suits defeated.
        suitsDefeated = super().calculateProgress(context, questReference, quester, cappedProgress=False)

        # Roll a chance completed per suit.
        # Do a "fake randomization"; we average out the chance over cogs killed,
        # and the fraction of what is left over we just do a random call on it.
        totalRecovered = suitsDefeated * self.recoverChance
        itemsRecovered = math.floor(totalRecovered)
        fractionRecovered = totalRecovered - itemsRecovered
        if random.random() <= fractionRecovered:
            itemsRecovered += 1

        # Return our result.
        return min(itemsRecovered, self.recoverRequired - questReference.getQuestProgress(self.objectiveIndex))

    @staticmethod
    def getDifficultyRange(questerType: QuesterType, questSource: QuestSource, **extraArgs):
        return None
    
    def getCompletionRequirement(self) -> int:
        return self.recoverRequired

    def modifyPoster(self, questReference: QuestReference, poster):
        complete = questReference.isQuestComplete(base.localAvatar, self.objectiveIndex)

        # Set cog poster attributes
        self.setCogFrame(poster.RIGHT, poster, complete, declarative=True)

        # Set item posted attributes
        itemPoster = poster.LEFT
        poster.visual_setFramePackageGeom(itemPoster)
        poster.visual_setFrameText(itemPoster, text=(PFX_RECOVER if not complete else '') + itemTuple2Word(
            QuestItemNames.get(self.recoverItem), self.recoverRequired,
            capitalizeFirstInSingular=True), maxRows=1 if complete and self.npcReturnable else 2)

        # Other poster changes
        color = 'green' if not self.taskManagerBoss else 'red'
        poster.visual_setFrameColor(poster.LEFT, color)
        poster.visual_setFrameColor(poster.RIGHT, color)
        poster.visual_setAuxText(AuxillaryText_From)
        poster.label_auxillaryText.show()

        # If we're complete, bonus info
        if complete:
            if self.npcReturnable:
                poster.visual_setNpcFrame(poster.RIGHT, self.getToNpcId())
                poster.visual_setFrameText(poster.RIGHT, self.getToNpcName())
                poster.visual_setAuxText(AuxillaryText_Complete)

        # And if we're not, show progress
        else:
            if self.recoverRequired > 1:
                value, range, textFormat = self.getProgressFormat(questReference)
                poster.visual_setProgressInfo(value=value, range=range, textFormat=textFormat)

    def getProgressFormat(self, questReference):
        return questReference.getQuestProgress(self.objectiveIndex), self.recoverRequired, PROG_Recover

    def getInfoTextStrings(self, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex) and self.npcReturnable:
            # Return the goal location
            return super().getInfoTextStrings(questReference)
        else:
            # Tell them where the cogs are
            return self.getLocationName(self.cogLocation),

    def getSpeedchatMessages(self, quester, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(quester, self.objectiveIndex):
            if self.npcReturnable:
                return self.getFinishToontaskStrings()
            return tuple()

        # Get the message formatting.
        message = SC_RecoverCogs
        cogName = self.getCogNameString(speedchat=True, count=self.recoverRequired)
        itemName = itemTuple2Word(QuestItemNames.get(self.recoverItem), self.recoverRequired)
        location = ''

        # Figure out location name
        if self.cogLocation is not None:
            location = self.getLocationName(zoneId=self.cogLocation)

        # Return message
        return message % (itemName, cogName, location),

    def getHeadline(self, questReference: QuestReference, objectiveSelected: int = 0) -> str:
        return HL_Recover
    
    def getObjectiveGoal(self) -> str:
        itemName = itemTuple2Word(QuestItemNames.get(self.recoverItem), self.recoverRequired, capitalizeFirstInSingular=True)
        return OBJ_Recover % (itemName, self.getCogNameString(count=self.recoverRequired))
    
    def getProgressString(self, questReference: QuestReference, progress: int) -> str:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex):
            return QuestProgress_Complete
        elif self.recoverRequired == 1:
            return ''
        return PROG_Recover.format(value=min(progress, self.recoverRequired), range=self.recoverRequired)

    def _getKwargStr(self):
        kwargstr = super()._getKwargStr()
        kwargstr += f'recoverItem=QuestItemName.{QuestItemName(self.recoverItem).name}, '
        kwargstr += f'recoverChance={self.recoverChance}, '
        if self.recoverRequired != 1:
            kwargstr += f'recoverRequired={self.recoverRequired}, '
        return kwargstr

    def __repr__(self):
        return f'RecoverFromCogObjective({self._getKwargStr()[:-2]})'
