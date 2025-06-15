from toontown.quest3.base.QuestObjective import *
from toontown.quest3.context.ZoneContext import ZoneContext
from toontown.quest3.QuestLocalizer import HL_Investigate, OBJ_Investigate, QuestProgress_Complete, SC_Investigate, \
    AuxillaryText_Complete, PFX_INVESTIGATE


# This will be filled with investigate objectives as they are generated
GlobalInvestigateZones = []


class InvestigateObjective(QuestObjective):
    poster_canUpdateAux = False

    def __init__(self,
                 npc = 2001,
                 rewards=None,
                 nextStep=None,
                 npcReturnable: bool = True,
                 zoneUnlocks=None,
                 zoneId: int = 2000):
        super().__init__(npc=npc, rewards=rewards, nextStep=nextStep, npcReturnable=npcReturnable, zoneUnlocks=zoneUnlocks)
        self.zoneId = zoneId
        if zoneId not in GlobalInvestigateZones:
            GlobalInvestigateZones.append(zoneId)

    def calculateProgress(self, context: ZoneContext, questReference: QuestReference, quester: Quester) -> int:
        if type(context) is not ZoneContext:
            return 0
        if context.getZoneId() == self.getZoneId():
            return 1
        return 0

    def getZoneId(self):
        return self.zoneId

    def modifyPoster(self, questReference: QuestReference, poster):
        complete = questReference.isQuestComplete(base.localAvatar, self.objectiveIndex)
        searchPoster = poster.CENTER if not (complete and self.npcReturnable) else poster.LEFT

        locName = NPCToons.getBuildingTitle(self.zoneId)
        poster.visual_setFrameColor(searchPoster, 'lightBlue')
        poster.visual_setFrameText(searchPoster, PFX_INVESTIGATE + locName)
        questIcons = loader.loadModel('phase_3.5/models/gui/quests/ttcc_quest_icons')
        glass = questIcons.find('**/magnifyingGlass')
        questIcons.removeNode()
        poster.visual_setFrameGeom(
            positionIndex=searchPoster,
            geom=glass,
            scale=0.1425
        )

        # If we're complete, bonus info
        if complete:
            if self.npcReturnable:
                poster.visual_setFrameColor(poster.RIGHT, 'lightBlue')
                poster.visual_setNpcFrame(poster.RIGHT, self.getToNpcId())
                poster.visual_setFrameText(poster.RIGHT, self.getToNpcName())
                poster.visual_setAuxText(AuxillaryText_Complete)
                poster.label_auxillaryText.show()

    def getInfoTextStrings(self, questReference: QuestReference) -> tuple:
        # If we're complete and demand NPC completion, point to NPC instead
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex) and self.npcReturnable:
            return super().getInfoTextStrings(questReference)

        # Otherwise, just list the branch/street zone
        locName = NPCToons.getBuildingTitle(self.zoneId)
        branchId = ZoneUtil.getBranchZone(self.zoneId)
        streetName = ZoneUtil.getStreetName(branchId)
        hoodId = ZoneUtil.getCanonicalHoodId(self.zoneId)
        locationName = base.cr.hoodMgr.getFullnameFromId(hoodId)
        if locName != streetName:
            return streetName, locationName
        else:
            return locationName,

    def getSpeedchatMessages(self, quester, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(quester, self.objectiveIndex):
            if self.npcReturnable:
                return self.getFinishToontaskStrings()
            return tuple()

        # Get delivery specific message
        return SC_Investigate % NPCToons.getBuildingTitle(self.zoneId),

    def getHeadline(self, questReference: QuestReference, objectiveSelected: int = 0) -> str:
        return HL_Investigate
    
    def getObjectiveGoal(self) -> str:
        return OBJ_Investigate % NPCToons.getBuildingTitle(self.zoneId)
    
    def getProgressString(self, questReference: QuestReference, progress: int) -> str:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex):
            return QuestProgress_Complete
        return ''

    def _getKwargStr(self):
        kwargstr = super()._getKwargStr()
        kwargstr += f'zoneId={self._numToLocStr(self.zoneId)}, '
        return kwargstr

    def __repr__(self):
        return f'InvestigateObjective({self._getKwargStr()[:-2]})'
