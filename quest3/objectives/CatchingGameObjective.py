import math

from toontown.quest3.base.QuestObjective import *
from toontown.quest3.context.CatchingGameContext import CatchingGameContext
from toontown.quest3.QuestLocalizer import (HL_Collect, OBJ_Catch, OnTheTrolley,
                                            PROG_Collect, QuestProgress_Complete, SC_CatchingGame, PFX_CATCH)

FRUIT_TYPES = {
    # TTC
    2000: {
        'fruit': 'apple',
        'scale': 0.04,
        'pos': (0, 10, -0.01),
        'path': 'phase_4/models/minigames/apple',
        'name': TTLocalizer.CatchGameApples
    },

    # BB
    1000: {
        'fruit': 'orange',
        'scale': .06,
        'pos': (0, 10, -0.01),
        'path': 'phase_4/models/minigames/orange',
        'name': TTLocalizer.CatchGameOranges
    },

    # YOTT
    7000: {
        'fruit': 'cherry',
        'scale': .06,
        'pos': (0, 10, -0.05),
        'hpr': (90, 0, 0),
        'path': 'phase_4/models/minigames/cherry',
        'name': TTLocalizer.CatchGameCherries
    },

    # DG
    5000: {
        'fruit': 'pear',
        'scale': .035,
        'pos': (0, 9.5, -0.05),
        'hpr': (-45, 0, 0),
        'path': 'phase_4/models/minigames/pear',
        'name': TTLocalizer.CatchGamePears
    },

    # MM
    4000: {
        'fruit': 'coconut',
        'scale': .035,
        'pos': (0, 10, -0.01),
        'path': 'phase_4/models/minigames/coconut',
        'specialCase': True,
        'name': TTLocalizer.CatchGameCoconuts
    },

    # TB
    3000: {
        'fruit': 'watermelon',
        'scale': .04,
        'pos': (0.0, 10, -0.006),
        'hpr': (-90, 0, 0),
        'path': 'phase_4/models/minigames/watermelon',
        'specialCase': True,
        'name': TTLocalizer.CatchGameWatermelons
    },

    # AA
    6000: {
        'fruit': 'acorn',
        'scale': .04,
        'pos': (-0.01, 10, -0.01),
        'hpr': (0, -90, 0),
        'path': 'phase_4/models/minigames/acorn',  # todo: switch this out with acorn treasure phase_4/props
        'specialCase': True,
        'name': TTLocalizer.CatchGameAcorns
    },

    # DD
    9000: {
        'fruit': 'pineapple',
        'scale': .025,
        'pos': (0, 10, -0.1),
        'path': 'phase_4/models/minigames/pineapple',
        'name': TTLocalizer.CatchGamePineapples
    },
}


class CatchingGameObjective(QuestObjective):

    def __init__(self,
                 npc = 2001,
                 rewards=None,
                 nextStep=None,
                 npcReturnable: bool = True,
                 fruitCount: int = None,
                 zoneId: int = None):
        super().__init__(npc=npc, rewards=rewards, nextStep=nextStep, npcReturnable=npcReturnable)
        self.fruitCount = fruitCount
        self.zoneId = zoneId

    def calculateProgress(self, context: CatchingGameContext, questReference: QuestReference,  quester: Quester) -> int:
        if type(context) is not CatchingGameContext:
            return 0
        # A zone was defined, but it doesn't match the context.
        if self.zoneId is not None and context.getZoneId() != self.zoneId:
            return 0
        return context.getFruitsCollected()

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
            if zoneId not in (ToontownGlobals.ToontownCentral, ToontownGlobals.DonaldsDock, ToontownGlobals.OldeToontown):
                return None
            return None, None

        return None  # die

    @staticmethod
    def getObjectiveWeight(questerType: QuesterType) -> int:
        """
        The likelihood for this objective to be chosen in a pool.
        The de facto amount is 100.
        """
        return 4

    @classmethod
    def generateFromDifficulty(cls, rng, difficulty: float, questSource: QuestSource, **extraArgs):
        """
        Given an arbitrary difficulty value, generate a QuestObjective.
        For more info, seek QuestGenerator.py.

        :param rng:        A seeded Random instance. Use this for .random() or .randint() calculations.
        :param difficulty: The arbitrary difficulty of the task.
        :return:           This QuestObjective, set with values to match the arbitrary difficulty.
        """
        fruitCount = 7.0 * (difficulty ** 1.2)
        zoneIdDict = {
            2000: 0.86,
            1000: 0.88,
            7000: 0.90,
            5000: 0.92,
            4000: 0.94,
            3000: 0.96,
            6000: 0.98,
            9000: 1.0,
        }
        zoneId = extraArgs.get("zoneId")
        if not zoneId:
            zoneId = rng.choice(list(zoneIdDict.keys()))
        fruitCount *= zoneIdDict.get(zoneId)

        # Round off our cog count so that it is pretty.
        fruitCount = math.ceil(fruitCount)
        if fruitCount < 1:
            fruitCount = 1
        elif fruitCount < 10:
            pass
        elif fruitCount < 20:
            fruitCount = round(round(fruitCount / 2) * 2)
        elif fruitCount < 40:
            fruitCount = round(round(fruitCount / 5) * 5)
        else:
            fruitCount = round(round(fruitCount / 20) * 20)
        
        # Fruit time
        return cls(
            fruitCount=fruitCount,
            zoneId=zoneId,
            npcReturnable=False,
        )
    
    def getCompletionRequirement(self) -> int:
        return self.fruitCount

    def modifyPoster(self, questReference: QuestReference, poster):
        complete = questReference.isQuestComplete(base.localAvatar, self.objectiveIndex)
        searchPoster = poster.CENTER if not (complete and self.npcReturnable) else poster.LEFT

        poster.visual_setFrameColor(searchPoster, 'lightBlue')
        
        fruitInfo = FRUIT_TYPES[self.zoneId]

        model = loader.loadModel(fruitInfo["path"])
        if fruitInfo.get("specialCase", False):
            geom = model.find(f"**/{fruitInfo['fruit']}")
        else:
            geom = model

        poster.visual_setFrameGeom(
            searchPoster, 
            geom, 
            scale=fruitInfo['scale'], 
            pos=fruitInfo['pos'], 
            hpr=fruitInfo.get('hpr')
        )

        model.removeNode()

        fruitName = fruitInfo['name'].capitalize()

        poster.visual_setFrameText(searchPoster, PFX_CATCH + (f'{self.fruitCount} {fruitName}'
                                                              if self.fruitCount > 1 else f'a {fruitName}'))

        # If we're complete, bonus info
        if complete:
            if self.npcReturnable:
                poster.visual_setFrameColor(poster.RIGHT, 'lightBlue')
                poster.visual_setNpcFrame(poster.RIGHT, self.getToNpcId())
                poster.visual_setFrameText(poster.RIGHT, self.getToNpcName())
                poster.label_auxillaryText.show()
        else:
            if self.fruitCount > 1:
                value, range, textFormat = self.getProgressFormat(questReference)
                poster.visual_setProgressInfo(value=value, range=range, textFormat=textFormat)

    def getProgressFormat(self, questReference):
        return questReference.getQuestProgress(self.objectiveIndex), self.fruitCount, PROG_Collect

    def getInfoTextStrings(self, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex) and self.npcReturnable:
            return super().getInfoTextStrings(questReference)

        return OnTheTrolley, self.getLocationName(self.zoneId)

    def getSpeedchatMessages(self, quester, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(quester, self.objectiveIndex):
            if self.npcReturnable:
                return self.getFinishToontaskStrings()
            return tuple()

        # Get book specific message
        fruitInfo = FRUIT_TYPES[self.zoneId]
        return SC_CatchingGame % f"{fruitInfo['fruit']}s",

    def getHeadline(self, questReference: QuestReference, objectiveSelected: int = 0) -> str:
        return HL_Collect
    
    def getObjectiveGoal(self) -> str:
        return OBJ_Catch % FRUIT_TYPES[self.zoneId]['fruit'].capitalize()
    
    def getProgressString(self, questReference: QuestReference, progress: int) -> str:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex):
            return QuestProgress_Complete
        elif self.fruitCount == 1:
            return ''
        return PROG_Collect.format(value=min(progress, self.fruitCount), range=self.fruitCount)

    def _getKwargStr(self):
        kwargstr = super()._getKwargStr()
        if self.fruitCount is not None:
            kwargstr += f'fruitCount={self.fruitCount}, '
        if self.zoneId is not None:
            kwargstr += f'zoneId={self.zoneId}, '
        return kwargstr

    def __repr__(self):
        return f'CatchingGameObjective({self._getKwargStr()[:-2]})'
