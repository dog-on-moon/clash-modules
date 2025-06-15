import math

from toontown.quest3.base.QuestObjective import *
from toontown.quest3.context.RacingContext import RacingContext
from toontown.quest3.QuestLocalizer import HL_Race, OBJ_RacePlacement, QuestProgress_Complete, SC_RaceComplete, \
    OBJ_Complete, PROG_Complete
from toontown.racing.RaceGlobals import TrackIds
from toontown.toonbase.ToontownGlobals import ToontownCentral, DonaldsDock


class RacingObjective(QuestObjective):

    poster_canUpdateAux = False

    def __init__(self,
                 npc = 2001,
                 rewards=None,
                 nextStep=None,
                 npcReturnable: bool = True,
                 trackId: int = None,
                 totalRaces: int = 1,
                 placement: int = None,
                 minParticipants: int = None):
        super().__init__(npc=npc, rewards=rewards, nextStep=nextStep, npcReturnable=npcReturnable)
        self.trackId = trackId
        self.totalRaces = totalRaces
        self.placement = placement
        self.minParticipants = minParticipants

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

    def calculateProgress(self, context: RacingContext, questReference: QuestReference, quester: Quester) -> int:
        if type(context) is not RacingContext:
            return 0
        # A track id was specified, and it doesn't match the context.
        if self.trackId is not None and context.trackId not in (self.trackId, self.trackId + 1): 
            return 0
        # They didn't finish first.
        if self.placement is not None and context.getFinishedAvatars() > self.placement:
            return 0
        # There aren't enough participants in the race.
        if self.minParticipants is not None and self.minParticipants > context.getParticipants():
            return 0
        # They completed the race! Great.
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
        trackId = rng.choice((None, rng.choice(TrackIds[::2])))
        totalRaces = max(1, 0.2 * difficulty ** 1.3)
        totalRaces += totalRaces * (rng.random() * rng.choice((-0.2, 0.2)))

        if trackId is not None:
            # Lower the required races
            totalRaces *= 0.8

        if trackId is None and rng.random() <= 0.5:
            participants = (None, *range(4, 9))
            participantChoices = \
                max(min(int((difficulty / 3.0) * (1 + (rng.random() / 4.0))), len(participants) - 1), 1)
            minParticipants = rng.choice(participants[:participantChoices])

            # Lower the required races
            totalRaces *= 0.8
        else:
            minParticipants = None

        if rng.random() <= 0.33:
            if minParticipants is not None:
                maxParticipants = minParticipants - 1
            else:
                maxParticipants = 8

            placements = list(range(1, maxParticipants))
            placement = rng.choices(placements, [p ** -(difficulty / 10) for p in placements])[0]
            
            # Lower the required races
            totalRaces *= 0.8
        else:
            placement = None

        # Return our objective.
        return cls(
            trackId=trackId,
            totalRaces=math.ceil(totalRaces),
            npcReturnable=False,
            placement=placement,
            minParticipants=minParticipants,
        )

    def modifyPoster(self, questReference: QuestReference, poster):
        complete = questReference.isQuestComplete(base.localAvatar, self.objectiveIndex)
        searchPoster = poster.CENTER if not (complete and self.npcReturnable) else poster.LEFT

        poster.visual_setFrameColor(searchPoster, 'lightBlue')

        prefix = f"{self.totalRaces}" if self.totalRaces > 1 else "a"
        frameText = f"{prefix} {self.getRaceTrackName()} Race{'s' if self.totalRaces > 1 else ''}"

        if self.placement is not None:
            if self.placement == 1:
                ordinal = TTLocalizer.getOrdinalNum(self.placement)
                frameText = f"Place {ordinal} in {frameText}"
            else:
                frameText = f"Place Top {self.placement} in {frameText}"
        else:
            frameText = f"Complete {frameText}"

        if self.minParticipants is not None:
            frameText = f"{frameText} with {self.minParticipants}+ participants"

        poster.visual_setFrameText(searchPoster, frameText)
        poster.visual_setRaceTrophyGeom(searchPoster)

        # If we're complete, bonus info
        if not complete:
            value, range, textFormat = self.getProgressFormat(questReference)
            poster.visual_setProgressInfo(value=value, range=range, textFormat=textFormat)
        else:
            if self.npcReturnable:
                poster.visual_setFrameColor(poster.RIGHT, 'lightBlue')
                poster.visual_setNpcFrame(poster.RIGHT, self.getToNpcId())
                poster.visual_setFrameText(poster.RIGHT, self.getToNpcName())
                poster.label_auxillaryText.show()

    def getProgressFormat(self, questReference):
        return questReference.getQuestProgress(self.objectiveIndex), self.totalRaces, PROG_Complete

    def getInfoTextStrings(self, questReference: QuestReference) -> tuple:
        # If we're complete and demand NPC completion, point to NPC instead
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex) and self.npcReturnable:
            return super().getInfoTextStrings(questReference)

        return f"at {TTLocalizer.lGoofySpeedway}",

    def getSpeedchatMessages(self, quester, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(quester, self.objectiveIndex):
            return tuple()
        trackName = self.getRaceTrackName()
        retVal = SC_RaceComplete.format_map({
            "totalRaces": self.totalRaces,
            "trackName": f" {trackName.strip()}" if trackName else "",
            "s": 's' if self.totalRaces > 1 else '',
        })
        return retVal,

    def getHeadline(self, questReference: QuestReference, objectiveSelected: int = 0) -> str:
        return HL_Race

    def getCompletionRequirement(self) -> int:
        return self.totalRaces
    
    def getRaceTrackName(self) -> str:
        if self.trackId is None:
            return ''
        return f'{TTLocalizer.KartRace_TrackNames[self.trackId]}'
    
    def getObjectiveGoal(self) -> str:
        if self.placement is not None:
            return OBJ_RacePlacement % (TTLocalizer.getOrdinalNum(self.placement), self.getRaceTrackName())
        return OBJ_Complete % "Race"
    
    def getProgressString(self, questReference: QuestReference, progress: int) -> str:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex):
            return QuestProgress_Complete
        elif self.totalRaces == 1:
            return ''
        return PROG_Complete.format(value=min(progress, self.totalRaces), range=self.totalRaces)
    
    def _getKwargStr(self):
        kwargstr = super()._getKwargStr()
        if self.trackId is not None:
            kwargstr += f'trackId={self.trackId}, '
        if self.placement is not None:
            kwargstr += f'placement={self.placement}, '
        return kwargstr

    def __repr__(self):
        return f'RacingObjective({self._getKwargStr()[:-2]})'


RacingObjective() # Thanks main for this hack
