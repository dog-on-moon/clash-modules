import math

from toontown.quest3 import QuestLocalizer
from toontown.quest3.base.QuestObjective import *
from toontown.quest3.context.TreasureContext import TreasureContext
from toontown.quest3.QuestLocalizer import HL_Collect, OBJ_Collect, PROG_Collect, QuestProgress_Complete, SC_Treasure, \
    Anywhere, PFX_GRAB

TREASURE_TYPES = {
    0: {
        'location': TTLocalizer.lToontownCentral,
        'model': 'phase_4/models/props/icecream',
        'scale': 0.045,
        'pos': (0, 10, -0.065)
    },
    1: {
        'location': TTLocalizer.lDonaldsDock,
        'model': 'phase_4/models/props/bb-treasure',
        'scale': 0.045,
        'pos': (0, 10, -0.067)
    },
    2: {
        'location': TTLocalizer.lDaisyGardens,
        'model': 'phase_4/models/props/dg-treasure',
        'scale': 0.045,
        'pos': (0, 10, -0.067)
    },
    3: {
        'location': TTLocalizer.lTheBrrrgh,
        'model': 'phase_4/models/props/tb-treasure',
        'scale': 0.048,
        'pos': (0, 10, -0.07)
    },
    4: {
        'location': TTLocalizer.lMinniesMelodyland,
        'model': 'phase_4/models/props/mml-treasure',
        'scale': 0.048,
        'pos': (0, 10, -0.067)
    },
    5: {
        'location': TTLocalizer.lDonaldsDreamland,
        'model': 'phase_4/models/props/ddl-treasure',
        'scale': 0.048,
        'pos': (0, 10, -0.04)
    },
    6: {
        'location': TTLocalizer.lOutdoorZone,
        'model': 'phase_4/models/props/aa-treasure',
        'scale': 0.07,
        'pos': (0, 10, -0.07)
    },
    7: {
        'location': QuestLocalizer.AtYourHome,
        'model': 'phase_4/models/props/estate-treasure',
        'scale': 0.05,
        'pos': (0, 10, -0.07)
    },
    9: {
        'location': TTLocalizer.lOldeToontown,
        'model': 'phase_4/models/props/yott-treasure',
        'scale': 0.045,
        'pos': (0, 10, -0.067)
    },
}

ZoneId2TreasureType = {
    ToontownGlobals.ToontownCentral: 0,
    ToontownGlobals.DonaldsDock: 1,
    ToontownGlobals.OldeToontown: 9,
    ToontownGlobals.DaisyGardens: 2,
    ToontownGlobals.MinniesMelodyland: 4,
    ToontownGlobals.TheBrrrgh: 3,
    ToontownGlobals.OutdoorZone: 6,
    ToontownGlobals.DonaldsDreamland: 5,
}


class TreasureObjective(QuestObjective):

    def __init__(self,
                 npc=2001,
                 rewards=None,
                 nextStep=None,
                 npcReturnable: bool = True,
                 treasureType: int = None,
                 treasureCount: int = 1):
        super().__init__(npc=npc, rewards=rewards, nextStep=nextStep, npcReturnable=npcReturnable)
        self.treasureType = treasureType
        self.treasureCount = treasureCount

    def calculateProgress(self, context: TreasureContext, questReference: QuestReference, quester: Quester) -> int:
        if type(context) is not TreasureContext:
            return 0
        # A treasure type was specified, but it's not the one we touched.
        if self.treasureType is not None and context.getTreasureType() != self.treasureType:
            return 0
        return 1

    def getCompletionRequirement(self) -> int:
        return self.treasureCount

    @staticmethod
    def getDifficultyRange(questerType: QuesterType, questSource: QuestSource, **extraArgs):
        if questerType == QuesterType.Toon:
            return None, None
        elif questerType == QuesterType.Club:
            return None
        else:
            return None, None

    @staticmethod
    def getObjectiveWeight(questerType: QuesterType) -> int:
        """
        The likelihood for this objective to be chosen in a pool.
        The de facto amount is 100.
        """
        return 1

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
        treasureAmount = 1.5 * (difficulty ** 1.2)

        treasureType = ZoneId2TreasureType.get(extraArgs.get('zoneId'), ZoneId2TreasureType[ToontownGlobals.ToontownCentral])

        # Round off our treasure count so that it is pretty.
        treasureAmount = math.ceil(treasureAmount)
        if treasureAmount < 1:
            treasureAmount = 1
        elif treasureAmount < 10:
            pass
        elif treasureAmount < 20:
            treasureAmount = round(round(treasureAmount / 2) * 2)
        elif treasureAmount < 200:
            treasureAmount = round(round(treasureAmount / 5) * 5)
        elif treasureAmount < 500:
            treasureAmount = round(round(treasureAmount / 10) * 10)
        elif treasureAmount < 2000:
            treasureAmount = round(round(treasureAmount / 50) * 50)
        else:
            treasureAmount = round(round(treasureAmount / 100) * 100)

        # Return our objective.
        return cls(
            treasureCount=math.ceil(treasureAmount),
            npcReturnable=False,
            treasureType=treasureType,
        )

    def modifyPoster(self, questReference: QuestReference, poster):
        complete = questReference.isQuestComplete(base.localAvatar, self.objectiveIndex)
        searchPoster = poster.CENTER if not (complete and self.npcReturnable) else poster.LEFT

        poster.visual_setFrameColor(searchPoster, 'green')
        poster.visual_setFrameText(searchPoster, PFX_GRAB + (f'{self.treasureCount} Treasures'
                                                             if self.treasureCount > 1 else 'a Treasure'))

        treasureInfo = self.getTreasureInfo()
        geom = loader.loadModel(treasureInfo['model'])
        poster.visual_setFrameGeom(searchPoster, geom, scale=treasureInfo['scale'], pos=treasureInfo['pos'])
        geom.removeNode()

        # If we're complete, bonus info
        if complete:
            if self.npcReturnable:
                poster.visual_setFrameColor(poster.RIGHT, 'green')
                poster.visual_setNpcFrame(poster.RIGHT, self.getToNpcId())
                poster.visual_setFrameText(poster.RIGHT, self.getToNpcName())
                poster.label_auxillaryText.show()
        else:
            if self.treasureCount > 1:
                value, range, textFormat = self.getProgressFormat(questReference)
                poster.visual_setProgressInfo(value=value, range=range, textFormat=textFormat)

    def getProgressFormat(self, questReference):
        return questReference.getQuestProgress(self.objectiveIndex), self.treasureCount, PROG_Collect

    def getInfoTextStrings(self, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex) and self.npcReturnable:
            return super().getInfoTextStrings(questReference)
        if self.treasureType is not None:
            return self.getTreasureInfo()['location'],
        else:
            return Anywhere,

    def getSpeedchatMessages(self, quester, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(quester, self.objectiveIndex):
            if self.npcReturnable:
                return self.getFinishToontaskStrings()
            return tuple()

        # Get book specific message
        return SC_Treasure,

    def getHeadline(self, questReference: QuestReference, objectiveSelected: int = 0) -> str:
        return HL_Collect
    
    def getObjectiveGoal(self) -> str:
        return OBJ_Collect % 'some Treasure'
    
    def getProgressString(self, questReference: QuestReference, progress: int) -> str:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex):
            return QuestProgress_Complete
        elif self.treasureCount == 1:
            return ''
        return PROG_Collect.format(value=min(progress, self.treasureCount), range=self.treasureCount)

    def getTreasureInfo(self):
        return TREASURE_TYPES.get(self.treasureType, random.choice(list(TREASURE_TYPES.values())))

    def _getKwargStr(self):
        kwargstr = super()._getKwargStr()
        if self.treasureCount != 1:
            kwargstr += f'treasureCount={self.treasureCount}, '
        if self.treasureType is not None:
            kwargstr += f'treasureType={self.treasureType}, '
        return kwargstr

    def __repr__(self):
        return f'TreasureObjective({self._getKwargStr()[:-2]})'
