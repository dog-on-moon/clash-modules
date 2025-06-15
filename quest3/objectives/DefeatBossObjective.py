import math
import random
from typing import Optional

from toontown.quest3.QuestEnums import QuesterType, QuestSource
from ..daily.DailyConstants import QuestTier
from toontown.quest3.QuestLocalizer import PFX_DEFEAT
from toontown.quest3.objectives.DefeatCogObjective import DefeatCogObjective
from toontown.toonbase import TTLocalizer
from toontown.toonbase.ToontownGlobals import ToontownCentral, DonaldsDock, OldeToontown, DaisyGardens, MinniesMelodyland, TheBrrrgh


class DefeatBossObjective(DefeatCogObjective):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, boss=True)

    @staticmethod
    def getDifficultyRange(questerType: QuesterType, questSource: QuestSource, **extraArgs):
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
        return 24

    @classmethod
    def generateFromDifficulty(cls, rng, difficulty: float, questSource: QuestSource, **extraArgs):
        """
        Given an arbitrary difficulty value, generate a QuestObjective.
        For more info, seek QuestGenerator.py.

        :param rng:        A seeded Random instance. Use this for .random() or .randint() calculations.
        :param difficulty: The arbitrary difficulty of the task.
        :return:           This QuestObjective, set with values to match the arbitrary difficulty.
        """
        # Set initial parameters.
        cogCount = 0.025 * (difficulty ** 1.7)
        zoneId = extraArgs.get("zoneId")
        if rng.random() < 0.5:
            if zoneId == DaisyGardens:
                eligibleDepts = ['s']
            elif zoneId == MinniesMelodyland:
                eligibleDepts = ['s', 'm']
            elif zoneId == TheBrrrgh:
                eligibleDepts = ['s', 'm', 'l']
            else: # todo: boardbot
                eligibleDepts = ['s', 'm', 'l', 'c']
            cogTrack = rng.choice(eligibleDepts)
        else:
            cogTrack = None
            cogCount = math.ceil(cogCount * 1.5)  # 50% more bosses if universal

        type2Name = {'g': 'chairman',
                     'c': 'ceo',
                     'l': 'clo',
                     'm': 'cfo',
                     's': 'vp'}
        cogType = type2Name.get(cogTrack, None)

        # Return our objective.
        return cls(
            cogCount=math.ceil(cogCount),
            cogType=cogType,
            cogTrack=cogTrack,
            npcReturnable=False,
        )

    def getLowestToonLevel(self) -> Optional[int]:
        return {
            'g': 78,
            'c': 68,
            'l': 58,
            'm': 48,
            's': 38,
        }.get(self.cogTrack, None)

    def setCogFrame(self, cogPoster, poster, complete=False, declarative=False):
        poster.visual_setFrameColor(cogPoster, 'orange')
        poster.visual_setFrameText(cogPoster, PFX_DEFEAT + self.getCogNameString())

        # This block obscures managers if the local player has not encountered them
        # This also acts as a spoiler protection from people with completed tasks
        if not complete:
            lavGal = base.localAvatar.getGalleryStatus()
            track2Name = {'g': 'chairman',
                         'c': 'ceo',
                         'l': 'clo',
                         'm': 'cfo',
                         's': 'vp',
                         None: 'vp'}
            type = track2Name.get(self.cogTrack)
            if lavGal.get(type, 0) <= 0:  # Only want to obscure manager cogs
                silhouette = True
            else:
                silhouette = False
        else:
            silhouette = False
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
            poster.visual_setBossHead(cogPoster, self.cogTrack, silhouette=silhouette)

    def getReturnPosterColor(self):
        return 'orange'

    """text makin methods"""

    def getCogNameString(self, forcePlural=False, declarative=True, speedchat=False, count=0):
        if self.cogType is not None and self.cogType in TTLocalizer.BossNames:
            nameSingle, namePlural = TTLocalizer.BossNames[self.cogType]
        else:
            nameSingle, namePlural = TTLocalizer.BossNames[self.cogTrack]
        if self.cogCount == 1:
            return nameSingle[0].upper() + nameSingle[1:]
        return f"{self.cogCount} {namePlural}"

    def __repr__(self):
        return f'DefeatBossObjective({self._getKwargStr()[:-2]})'
