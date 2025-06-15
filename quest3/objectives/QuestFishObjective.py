from toontown.quest3.base.QuestObjective import *
from toontown.quest3.context.QuestFishContext import QuestFishContext
from toontown.quest3.QuestEnums import QuestItemName
from toontown.quest3.QuestLocalizer import (AuxillaryText_For, HL_Fish, OBJ_Recover,
                                            PROG_Recover, QuestItemNames, QuestProgress_Complete,
                                            SC_GoFishing, TheFish, PFX_FISH)


class QuestFishObjective(QuestObjective):

    def __init__(self,
                 npc = 2001,
                 rewards=None,
                 nextStep=None,
                 npcReturnable: bool = True,
                 fishType: QuestItemName = QuestItemName.GlassJar,
                 fishCount: int = 1,
                 fishChance: float = 0.8,
                 fishLocation: int = None, ):
        super().__init__(npc=npc, rewards=rewards, nextStep=nextStep, npcReturnable=npcReturnable)
        self.fishType = fishType
        self.fishCount = fishCount
        self.fishChance = fishChance
        self.fishLocation = fishLocation

    def calculateProgress(self, context: QuestFishContext, questReference: QuestReference, quester: Quester) -> int:
        if type(context) is not QuestFishContext:
            return 0
        return context.getQuestFish() == self.fishType
    
    def getCompletionRequirement(self) -> int:
        return self.fishCount

    def modifyPoster(self, questReference: QuestReference, poster):
        complete = questReference.isQuestComplete(base.localAvatar, self.objectiveIndex)
        itemPoster = poster.CENTER if not (complete and self.npcReturnable) else poster.LEFT
        poster.visual_setFrameColor(itemPoster, 'green')
        poster.visual_setFramePackageGeom(itemPoster)

        # Set fish name
        fishTextTuple = QuestItemNames.get(self.fishType, QuestItemNames['default'])
        if self.fishCount == 1:
            wordPrefix: str = fishTextTuple[2]
            fishText = wordPrefix.lower() + fishTextTuple[0]
        else:
            fishText = f'{self.fishCount} {fishTextTuple[1]}'
        poster.visual_setFrameText(itemPoster, PFX_FISH + fishText)

        # If we're complete, bonus info
        if complete and self.npcReturnable:
            poster.visual_setFrameColor(poster.RIGHT, 'green')
            poster.visual_setNpcFrame(poster.RIGHT, self.getToNpcId())
            poster.visual_setFrameText(poster.RIGHT, self.getToNpcName())
            poster.label_auxillaryText.show()
        else:
            poster.visual_setAuxText(AuxillaryText_For)
            poster.visual_setAuxTextPosition((-0.18, 0, 0.09))
            poster.label_auxillaryText.show()
            if not complete and self.fishCount > 1:
                # show progress bar
                value, range, textFormat = self.getProgressFormat(questReference)
                poster.visual_setProgressInfo(value=value, range=range, textFormat=textFormat)

    def getProgressFormat(self, questReference):
        return questReference.getQuestProgress(self.objectiveIndex), self.fishCount, PROG_Recover

    def getInfoTextStrings(self, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex) and self.npcReturnable:
            # Return the goal location
            return super().getInfoTextStrings(questReference)
        else:
            # Tell them where The Fish are
            return self.getLocationName(zoneId=self.fishLocation),

    def getSpeedchatMessages(self, quester, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(quester, self.objectiveIndex):
            if self.npcReturnable:
                return self.getFinishToontaskStrings()
            return tuple()

        # Fish time
        return SC_GoFishing % (self.getFishText(), self.getLocationName(zoneId=self.fishLocation, lowercaseAnywhere=True, raw=True)),
    
    def getFishText(self) -> str:
        fishTextTuple = QuestItemNames.get(self.fishType, QuestItemNames['default'])
        if self.fishCount == 1:
            fishText = fishTextTuple[2] + fishTextTuple[0]
        else:
            fishText = fishTextTuple[1]
        return fishText

    def getHeadline(self, questReference: QuestReference, objectiveSelected: int = 0) -> str:
        return HL_Fish
    
    def getObjectiveGoal(self) -> str:
        return OBJ_Recover % (self.getFishText(), TheFish)
    
    def getProgressString(self, questReference: QuestReference, progress: int) -> str:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex):
            return QuestProgress_Complete
        elif self.fishCount == 1:
            return ''
        return PROG_Recover.format(value=min(progress, self.fishCount), range=self.fishCount)

    """
    Accessor methods
    """

    def rollForFish(self, zoneId: int) -> bool:
        """Rolls for fish."""
        if self.fishLocation is not None:
            # Match by Hood
            if ZoneUtil.getHoodId(self.fishLocation) == self.fishLocation:
                if ZoneUtil.getHoodId(self.fishLocation) != ZoneUtil.getHoodId(zoneId):
                    # This fish is caught in the wrong hood.
                    return False

            # Match by Branch
            elif ZoneUtil.getBranchZone(self.fishLocation) == self.fishLocation:
                if ZoneUtil.getBranchZone(self.fishLocation) != ZoneUtil.getBranchZone(zoneId):
                    # This fish is caught in the wrong branch.
                    return False

        # Now do RNG chance.
        return random.random() <= self.fishChance

    def getFishType(self):
        return self.fishType

    def _getKwargStr(self):
        kwargstr = super()._getKwargStr()
        kwargstr += f'fishType=QuestItemName.{QuestItemName(self.fishType).name}, '
        if self.fishCount != 1:
            kwargstr += f'fishCount={self.fishCount}, '
        kwargstr += f'fishChance={self.fishChance}, '
        if self.fishLocation is not None:
            kwargstr += f'fishLocation={self._numToLocStr(self.fishLocation)}, '
        return kwargstr

    # fishType: QuestItemName = QuestItemName.GlassJar,
    #                  fishCount: int = 3,
    #                  fishChance: float = 0.8,
    #                  fishLocation: int = None, ):

    def __repr__(self):
        return f'RecoverFromCogObjective({self._getKwargStr()[:-2]})'
