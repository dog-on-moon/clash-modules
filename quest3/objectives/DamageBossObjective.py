import math
from typing import Optional

from toontown.quest3.QuestEnums import QuesterType, QuestSource
from toontown.quest3.QuestLocalizer import AuxillaryText_Against, AuxillaryText_Complete, HL_Damage, PROG_Damage, QuestProgress_Complete, SC_Damage, OBJ_Damage
from toontown.quest3.base.QuestObjective import QuestObjective
from toontown.quest3.base.QuestReference import QuestReference
from toontown.quest3.base.Quester import Quester
from toontown.quest3.context.CogBossContext import CogBossContext
from ..daily.DailyConstants import QuestTier
from toontown.quest3.objectives.CogBossObjective import CogBossObjective
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.toonbase.ToontownGlobals import ToontownCentral, DonaldsDock, OldeToontown, \
    DaisyGardens, MinniesMelodyland, TheBrrrgh


class DamageBossObjective(CogBossObjective):
    def __init__(self,
                 npc = 2001,
                 rewards=None,
                 nextStep=None,
                 npcReturnable: bool = True,
                 zoneUnlocks=None,
                 damageAmount: int = 1,
                 cogTrack: str = None,
                 cogType: str = None,
                 zoneId: int = None):
        super().__init__(
            npc=npc, rewards=rewards, nextStep=nextStep, npcReturnable=npcReturnable, zoneUnlocks=zoneUnlocks,
            cogTrack=cogTrack, cogType=cogType, zoneId=zoneId,
        )
        self.damageAmount = damageAmount

    def calculateProgress(self, context: CogBossContext, questReference: QuestReference, quester: Quester) -> int:
        if not isinstance(context, CogBossContext):
            return 0
        if self.cogTrack is not None and self.cogTrack != context.getCogTrack():
            return 0
        return context.getBossDamage()
    
    def getCompletionRequirement(self) -> int:
        return self.damageAmount

    def getObjectiveGoal(self) -> str:
        type2Name = {'g': 'the Chairman',
                     'c': 'the CEO',
                     'l': 'the CLO',
                     'm': 'the CFO',
                     's': 'the VP'}
        bossName = type2Name.get(self.cogTrack, 'a boss')
        return (OBJ_Damage % self.damageAmount) + f" against {bossName}"

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
        return 9

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
        averageBossHps = {
            "s": ToontownGlobals.SellbotBossMaxDamage * 0.65,
            "m": ToontownGlobals.CashbotBossMaxDamage[1],
            "l": ToontownGlobals.LawbotBossMaxDamage[1],
            "c": ToontownGlobals.BossbotBossMaxDamage[0],
            # todo: boardbot
        }
        zoneId = extraArgs.get("zoneId")
        if rng.random() < 0.5:
            if zoneId == DaisyGardens:
                eligibleDepts = ['s']
            elif zoneId == MinniesMelodyland:
                eligibleDepts = ['s', 'm']
            elif zoneId == TheBrrrgh:
                eligibleDepts = ['s', 'm', 'l']
            else:  # todo: boardbot
                eligibleDepts = ['s', 'm', 'l', 'c']
            cogTrack = rng.choice(eligibleDepts)
            averageBossHp = averageBossHps.get(cogTrack)
            damageAmount = lerp(averageBossHp * 0.95, averageBossHp, rng.random()) * (difficulty ** 1.3) // 40
            damageAmount = math.ceil(damageAmount * 0.75) # 25% less damage if non universal
        else:
            cogTrack = None
            averageBossHp = math.ceil(sum(list(averageBossHps.values())) / len(averageBossHps))
            damageAmount = lerp(averageBossHp * 0.95, averageBossHp, rng.random()) * (difficulty ** 1.3) // 40
            damageAmount = math.ceil(damageAmount * 1.5)  # 50% more damage if universal
        
        # Round off our cog count so that it is pretty.
        damageAmount = math.ceil(damageAmount)
        if damageAmount < 1:
            damageAmount = 1
        elif damageAmount < 10:
            pass
        elif damageAmount < 20:
            damageAmount = round(round(damageAmount / 2) * 2)
        elif damageAmount < 50:
            damageAmount = round(round(damageAmount / 5) * 5)
        elif damageAmount < 100:
            damageAmount = round(round(damageAmount / 10) * 10)
        else:
            damageAmount = round(round(damageAmount / 20) * 20)

        type2Name = {'g': 'chairman',
                     'c': 'ceo',
                     'l': 'clo',
                     'm': 'cfo',
                     's': 'vp'}
        cogType = type2Name.get(cogTrack, None)

        # Return our objective.
        return cls(
            damageAmount=math.ceil(damageAmount),
            cogType=cogType,
            cogTrack=cogTrack,
            npcReturnable=False,
        )

    def getHeadline(self, questReference: QuestReference, objectiveSelected: int = 0) -> str:
        return HL_Damage

    def getLowestToonLevel(self) -> Optional[int]:
        return {
            's': 38,
            'm': 48,
            'l': 58,
            'c': 68,
            'g': 78,
        }.get(self.cogTrack)
    
    def getProgressString(self, questReference: QuestReference, progress: int) -> str:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex):
            return QuestProgress_Complete
        elif self.damageAmount == 1:
            return ''
        return PROG_Damage.format(value=min(progress, self.damageAmount), range=self.damageAmount)
    
    def modifyPoster(self, questReference: QuestReference, poster):
        complete = questReference.isQuestComplete(base.localAvatar, self.objectiveIndex)
        cogPoster = poster.RIGHT if not (complete and self.npcReturnable) else poster.LEFT
        self.setCogFrame(cogPoster, poster)

        if not (complete and self.npcReturnable):
            statusEffectImages = base.loader.loadModel('phase_3.5/models/gui/battlegui/status_effects')
            icon = statusEffectImages.find(f'**/confusion_icon')
            poster.visual_setFrameGeom(poster.LEFT, icon, 0.2)
            poster.visual_setFrameColor(poster.LEFT, 'orange')
            poster.visual_setFrameText(poster.LEFT, f'Deal {self.damageAmount} Damage')
            statusEffectImages.removeNode()
        
        poster.visual_setAuxText(AuxillaryText_Against)
        poster.label_auxillaryText.show()

        # If we're complete, bonus info
        if complete:
            if self.npcReturnable:
                poster.visual_setFrameColor(poster.RIGHT, 'orange')
                poster.visual_setNpcFrame(poster.RIGHT, self.getToNpcId())
                poster.visual_setFrameText(poster.RIGHT, self.getToNpcName())
                poster.visual_setAuxText(AuxillaryText_Complete)
        # And if we're not, show progress
        else:
            value, range, textFormat = self.getProgressFormat(questReference)
            poster.visual_setProgressInfo(value=value, range=range, textFormat=textFormat)
    
    def getProgressFormat(self, questReference):
        return questReference.getQuestProgress(self.objectiveIndex), self.damageAmount, PROG_Damage
    
    def getSpeedchatMessages(self, quester, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(quester, self.objectiveIndex):
            if self.npcReturnable:
                return self.getFinishToontaskStrings()
            return tuple()

        # Get the message formatting.
        cogName = self.getCogNameString()
        return SC_Damage % (self.damageAmount, cogName),

    """text makin methods"""

    def _getKwargStr(self):
        kwargstr = super()._getKwargStr()
        if self.damageAmount != 1:
            kwargstr += f'damageAmount={self.damageAmount}, '
        return kwargstr


DamageBossObjective() # thanks m ai n
