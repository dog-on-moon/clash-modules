import random

from toontown.quest3.QuestEnums import QuesterType, QuestSource
from toontown.quest3.base.QuestObjective import QuestObjective
from toontown.quest3.base.QuestReference import QuestReference
from toontown.quest3.base.Quester import Quester
from toontown.quest3.context.CogBossContext import CogBossContext
from ..daily.DailyConstants import QuestTier
from toontown.toonbase import TTLocalizer
from toontown.toonbase.ToontownGlobals import ToontownCentral, DonaldsDock, OldeToontown


class CogBossObjective(QuestObjective):

    def __init__(self,
                 npc = 2001,
                 rewards=None,
                 nextStep=None,
                 npcReturnable: bool = True,
                 zoneUnlocks=None,
                 cogTrack: str = None,
                 cogType: str = None,
                 zoneId: int = None):
        super().__init__(
            npc=npc, rewards=rewards, nextStep=nextStep, npcReturnable=npcReturnable, zoneUnlocks=zoneUnlocks
        )
        self.cogTrack = cogTrack
        self.cogType = cogType
        self.zoneId = zoneId

    def calculateProgress(self, context: CogBossContext, questReference: QuestReference, quester: Quester) -> int:
        return type(context) is CogBossContext

    @staticmethod
    def getDifficultyRange(questerType: QuesterType, questSource: QuestSource, **extraArgs):
        return None

    @staticmethod
    def getObjectiveWeight(questerType: QuesterType) -> int:
        """
        The likelihood for this objective to be chosen in a pool.
        The de facto amount is 100.
        """
        return 10
    
    def getInfoTextStrings(self, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex) and self.npcReturnable:
            # Return the goal location
            return super().getInfoTextStrings(questReference)

        locations = TTLocalizer.AvatarDetailPanelDynamicZoneLocations
        track2Location = {
            "s": locations[4],
            "m": locations[5],
            "l": locations[6],
            "c": locations[7],
            # todo: boardbot
        }
        if self.cogTrack is None:
            return self.getLocationName(),

        return track2Location[self.cogTrack],

    def setCogFrame(self, cogPoster, poster, declarative=False):
        poster.visual_setFrameColor(cogPoster, 'orange')
        poster.visual_setFrameText(cogPoster, self.getCogNameString())
        if self.cogTrack is None:
            # Random boss cog icon
            questIcons = loader.loadModel('phase_3.5/models/gui/quests/ttcc_quest_icons')
            bossGeom = questIcons.find('**/boss_cog')
            questIcons.removeNode()
            poster.visual_setFrameGeom(
                positionIndex=cogPoster,
                geom=bossGeom,
                scale=0.1425
            )
        else:
            # Make a boss head
            poster.visual_setBossHead(cogPoster, self.cogTrack)

    """text makin methods"""

    def getCogNameString(self, forcePlural=False, declarative=True, speedchat=False, count=0):
        nameSingle, _ = TTLocalizer.BossNames[self.cogTrack]
        return nameSingle

    def _getKwargStr(self):
        kwargstr = super()._getKwargStr()
        if self.zoneId:
            kwargstr += f'cogLocation={self._numToLocStr(self.zoneId)}, '
        if self.cogType:
            kwargstr += f"cogType='{self.cogType}', "
        if self.cogTrack:
            kwargstr += f"cogTrack='{self.cogTrack}', "
        return kwargstr
