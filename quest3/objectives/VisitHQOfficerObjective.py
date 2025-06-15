"""
Defining a quest where you simply have to visit an NPC for an objective.
"""
from toontown.quest3.base.QuestObjective import *
from toontown.quest3.context.NPCInteractContext import NPCInteractContext
from toontown.quest3.QuestLocalizer import HL_Visit, QuestProgress_Complete, OBJ_Visit, PFX_VISIT
from toontown.quest3.kudos import KudosConstants
from toontown.quest3.objectives.VisitObjective import VisitObjective
from toontown.toon.npc import NPCToons
from toontown.toon.npc.NPCToonConstants import NPCToonEnum
import random


class VisitHQOfficerObjective(VisitObjective):
    """
    A quest where you must visit an HQ Officer.
    """

    def __init__(self,
                 npc=2001,
                 npcZone=ToontownGlobals.ToontownCentral,
                 rewards=None,
                 nextStep=None,
                 npcReturnable: bool = True,
                 zoneUnlocks=None,
                 fromRandomKudosQuest=False,):
        super().__init__(npc=npc, rewards=rewards, nextStep=nextStep, npcReturnable=npcReturnable, zoneUnlocks=zoneUnlocks)
        self.npcZone = npcZone
        self.fromRandomKudosQuest = fromRandomKudosQuest
        self.npc = (self.getToNPCs()[0], self.getToNPCs()[0])

    def getToNPCs(self):
        return KudosConstants.getKudosNPCId(hoodId=self.npcZone)

    def getResolvableNpcIds(self) -> list:
        return self.getToNPCs()

    def calculateProgress(self, context: NPCInteractContext, questReference: QuestReference, quester: Quester) -> int:
        """
        Figures out how much progress we should accumulate,
        based on the attributes of the given QuestContext.
        :param context: Some QuestContext object.
        :return: An integer remarking progress.
        """
        if type(context) is not NPCInteractContext:
            return 0
        if context.getNpcId() in self.getToNPCs():
            return 1
        return 0

    def modifyPoster(self, questReference: QuestReference, poster):
        """
        Given a QuestPoster, update it to match what this objective should be.

        :param questReference:  The poster's quest reference.
        :param poster:          The poster GUI itself.
        :type poster:           QuestPoster
        """
        poster.visual_setNpcFrame(poster.CENTER, random.choice(self.getToNPCs()))
        poster.visual_setFrameColor(poster.CENTER, 'brown')
        poster.visual_setFrameText(poster.CENTER, PFX_VISIT + "a ToonHQ Officer")
        if self.fromRandomKudosQuest:
            poster.overrideQuestComplete(questReference)

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
        if self.npcReturnable:
            return self.getFinishToontaskStrings()
        return tuple()

    def getHeadline(self, questReference: QuestReference, objectiveSelected: int = 0) -> str:
        return HL_Visit
    
    def getObjectiveGoal(self) -> str:
        return OBJ_Visit % self.getToNpcName()
    
    def getProgressString(self, questReference: QuestReference, progress: int) -> str:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex):
            return QuestProgress_Complete
        return ''

    def getFinishToontaskStrings(self):
        """Returns a list of Toontask strings that explicitly tell you to
        go visit the toNpc.
        
        :rtype: tuple
        """
        npc = self.getToNPCs()[0]
        npcZone = NPCToons.getNPCZone(npc)
        hoodId = ZoneUtil.getCanonicalHoodId(npcZone)
        hoodName = ToontownGlobals.hoodNameMap[ZoneUtil.getCanonicalZoneId(hoodId)][-1]
        branchId = ZoneUtil.getCanonicalBranchZone(npcZone)

        from toontown.quest3.QuestLocalizer import SC_Visit, SC_VisitBuilding, SC_VisitBuildingWhere, \
            SC_VisitPlayground, SC_VisitSpecific

        # Concatenate all the strings.
        strings = [SC_Visit % " a Toon HQ Officer."]
        if ZoneUtil.isPlayground(self.getToNpcBranchId()):
            strings.append(SC_VisitPlayground % hoodName)
        else:
            toStreet = ToontownGlobals.StreetNames[branchId][0]
            streetName = ToontownGlobals.StreetNames[branchId][-1]
            strings.append(SC_VisitSpecific % {
                'to': toStreet,
                'street': streetName,
                'hood': hoodName
            })
        buildingArticle = NPCToons.getBuildingArticle(npcZone)
        buildingName = NPCToons.getBuildingTitle(npcZone)
        strings.extend([SC_VisitBuilding % (buildingArticle, buildingName),
                        SC_VisitBuildingWhere % (buildingArticle, buildingName)])

        return tuple(strings)

    def __repr__(self):
        return f'VisitHQOfficerObjective({self._getKwargStr()[:-2]})'
