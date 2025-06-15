import math

from toontown.quest3.base.QuestObjective import *
from toontown.quest3.context.GolfingContext import GolfingContext
from toontown.quest3.QuestLocalizer import HL_Golf, OBJ_GolfPlacement, OBJ_RacePlacement, QuestProgress_Complete, SC_GolfComplete, SC_RaceComplete, \
    OBJ_Complete, PROG_Complete
from toontown.toonbase.ToontownGlobals import ToontownCentral, DonaldsDock


class GolfingObjective(QuestObjective):

    poster_canUpdateAux = False

    def __init__(self,
                 npc = 2001,
                 rewards=None,
                 nextStep=None,
                 npcReturnable: bool = True,
                 courseId: int = None,
                 totalCourses: int = 1,
                 ranking: int = None,
                 minParticipants: int = None,
                 wantUnderPar: bool = False):
        super().__init__(npc=npc, rewards=rewards, nextStep=nextStep, npcReturnable=npcReturnable)
        self.courseId = courseId
        self.totalCourses = totalCourses
        self.ranking = ranking
        self.minParticipants = minParticipants
        self.wantUnderPar = wantUnderPar

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
            if zoneId in (ToontownCentral, DonaldsDock):
                return None
        if questSource == QuestSource.ClubQuest:
            return None

        return 1, 45

    @staticmethod
    def getObjectiveWeight(questerType: QuesterType) -> int:
        """
        The likelihood for this objective to be chosen in a pool.
        The de facto amount is 100.
        """
        return 8

    def calculateProgress(self, context: GolfingContext, questReference: QuestReference, quester: Quester) -> int:
        if type(context) is not GolfingContext:
            return 0
        # A track id was specified, and it doesn't match the context.
        if self.courseId is not None and context.courseId not in (self.courseId, self.courseId + 1): 
            return 0
        if self.ranking is not None:
            # They didn't attain the correct ranking.
            if context.getRanking() > self.ranking:
                return 0
            # No cheesing allowed. (cope and seethe nerd)
            elif context.getParticipants() < 2:
                return 0
        # There aren't enough participants in the course.
        if self.minParticipants is not None and self.minParticipants > context.getParticipants():
            return 0
        # They didn't score under par.
        if self.wantUnderPar and not context.getUnderPar():
            return 0
        # They completed the course! Great.
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
        # Pick a random track id, excluding all reverse tracks.
        courseId = rng.choice((None, rng.choice(list(TTLocalizer.GolfCourseNames))))
        totalCourses = max(1, 0.2 * difficulty ** 1.3)
        totalCourses += totalCourses * (rng.random() * rng.choice((-0.2, 0.2)))

        if courseId is not None:
            # Lower the required courses based on the length of
            # the course.
            totalCourses *= (0.8 ** courseId)

        wantUnderPar = False
        ranking = None
        minParticipants = None

        r = rng.random()
        if r <= 0.33:
            placements = list(range(1, 4))
            ranking = rng.choices(placements, [p ** -(difficulty / 10) for p in placements])[0]
            minParticipants = min(ranking + 1, 4)

            # Lower the required courses
            totalCourses *= 0.8
        elif r <= 0.66:
            wantUnderPar = True
            totalCourses *= 0.8
        
        if courseId is not None and rng.random() <= 0.5 and ranking is not None and ranking < 4:
            choices = list(range(minParticipants, 5))
            if len(choices) == 1:
                minParticipants = choices[0]
            else:
                minParticipants = rng.choices(choices, [p ** (difficulty / 10) for p in choices])[0]

            # Lower the required courses
            totalCourses *= 0.8

        # Return our objective.
        return cls(
            courseId=courseId,
            totalCourses=math.ceil(totalCourses),
            npcReturnable=False,
            ranking=ranking,
            minParticipants=minParticipants,
            wantUnderPar=wantUnderPar,
        )

    def modifyPoster(self, questReference: QuestReference, poster):
        complete = questReference.isQuestComplete(base.localAvatar, self.objectiveIndex)
        searchPoster = poster.CENTER if not (complete and self.npcReturnable) else poster.LEFT

        poster.visual_setFrameColor(searchPoster, 'lightBlue')

        prefix = f"{self.totalCourses}" if self.totalCourses > 1 else "a"
        frameText = f"{prefix} Course{'s' if self.totalCourses > 1 else ''}"

        if self.wantUnderPar:
            frameText += " Under Par"

        if self.ranking is not None:
            if self.ranking == 1:
                ordinal = TTLocalizer.getOrdinalNum(self.ranking)
                frameText = f"Place {ordinal} in {frameText}"
            else:
                frameText = f"Place Top {self.ranking} in {frameText}"
        else:
            frameText = f"Complete {frameText}"

        if self.minParticipants is not None:
            if self.minParticipants == 4:
                frameText = f"{frameText} with {self.minParticipants} participants"
            else:
                frameText = f"{frameText} with {self.minParticipants}+ participants"

        poster.visual_setFrameText(searchPoster, frameText, scaleOverRow=2, scaleOverRowAmount=0.8)
        poster.visual_setGolfTrophyGeom(searchPoster)

        # If we're complete, bonus info
        if not complete:
            if self.totalCourses > 1:
                value, range, textFormat = self.getProgressFormat(questReference)
                poster.visual_setProgressInfo(value=value, range=range, textFormat=textFormat)
        elif self.npcReturnable:
            poster.visual_setFrameColor(poster.RIGHT, 'lightBlue')
            poster.visual_setNpcFrame(poster.RIGHT, self.getToNpcId())
            poster.visual_setFrameText(poster.RIGHT, self.getToNpcName())
            poster.label_auxillaryText.show()

    def getProgressFormat(self, questReference):
        return questReference.getQuestProgress(self.objectiveIndex), self.totalCourses, PROG_Complete

    def getInfoTextStrings(self, questReference: QuestReference) -> tuple:
        # If we're complete and demand NPC completion, point to NPC instead
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex) and self.npcReturnable:
            return super().getInfoTextStrings(questReference)

        locName = TTLocalizer.lGolfZone
        if self.courseId is not None:
            return self.getGolfCourseName(), locName,

        return 'Any Golf Course', locName,

    def getSpeedchatMessages(self, quester, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(quester, self.objectiveIndex):
            return tuple()
        trackName = self.getGolfCourseName()
        retVal = SC_GolfComplete % (self.totalCourses, trackName)
        return retVal,

    def getHeadline(self, questReference: QuestReference, objectiveSelected: int = 0) -> str:
        return HL_Golf

    def getCompletionRequirement(self) -> int:
        return self.totalCourses
    
    def getGolfCourseName(self) -> str:
        if self.courseId is None:
            return ''
        return f' {TTLocalizer.GolfCourseNames[self.courseId]}'
    
    def getObjectiveGoal(self) -> str:
        if self.ranking is not None:
            return OBJ_GolfPlacement % (TTLocalizer.getOrdinalNum(self.ranking), self.getGolfCourseName())
        return OBJ_Complete % "Golf Course"
    
    def getProgressString(self, questReference: QuestReference, progress: int) -> str:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex):
            return QuestProgress_Complete
        elif self.totalCourses == 1:
            return ''
        return PROG_Complete.format(value=min(progress, self.totalCourses), range=self.totalCourses)
    
    def _getKwargStr(self):
        kwargstr = super()._getKwargStr()
        if self.totalCourses is not None:
            kwargstr += f'totalCourses={self.totalCourses}'
        if self.courseId is not None:
            kwargstr += f'courseId={self.courseId}, '
        if self.ranking is not None:
            kwargstr += f'ranking={self.ranking}, '
        kwargstr += f"wantUnderPar={self.wantUnderPar}"
        return kwargstr

    def __repr__(self):
        return f'GolfingObjective({self._getKwargStr()[:-2]})'


GolfingObjective() # Thanks main for this hack
