"""
The module containin the base QuestType.
"""
import random

from toontown.hood import ZoneUtil
from toontown.quest3.QuestEnums import QuesterType, QuestSource
from toontown.quest3.SpecialQuestZones import SpecialQuestZones
from toontown.quest3.base.QuestContext import QuestContext
from toontown.quest3.base.QuestReference import QuestReference
from toontown.quest3.base.QuestReward import QuestReward

from typing import TYPE_CHECKING, Optional
from toontown.quest3.base.Quester import Quester

# "Ending" objective sentinel value for definitions.
from toontown.quest3.context.NPCInteractContext import NPCInteractContext
from toontown.toon.npc import NPCToons, NPCToonConstants
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory

if TYPE_CHECKING:
    from toontown.quest3.gui.Quest3Poster import QuestPoster

END = 'END'


@DirectNotifyCategory()
class QuestObjective:
    """
    A base QuestObjective. Defines the fine details of a given QuestStep.
    """

    __slots__ = 'npc', 'dialogueId', 'rewards', 'nextStep', 'objectiveIndex', 'npcReturnable', 'zoneUnlocks'

    # Visual properties for poster manipulation
    poster_canUpdateAux = True  # can poster set aux text to 'Return To:'?

    # A reference to all QuestObjectives classes.
    objectiveClasses = []

    # Some nice variables for other uses.
    lowestToonLevel = None  # A reference for the lowest recommended toon level for the task.

    def __init__(self,
                 npc=2001,
                 rewards=None,
                 nextStep=None,
                 npcReturnable: bool=False,
                 zoneUnlocks=None):
        """
        Defines a QuestObjective object.

        :param npc:           The NPC assigning the quest. Can be defined as either:
                              - An Int (implying fromNpc and toNpc).
                              - A tuple of two ints to define fromNpc and toNpc separately.
        :param rewards:       Any QuestRewards to be given upon completion of the QuestStep.
        :param nextStep:      The next step of the QuestObjective. Can be defined as either:
                              - None (Implies that the next one is next.)
                              - END (Ends the QuestChain upon completion.)
                              - An int, referring to another step in the step dictionary.
                              - A tuple of ints. One will be picked at random.
        :param npcReturnable: Does this objective require TRUE 'completion' by talking to the toNpc?
        :param zoneUnlocks: Specific zones which are gated behind this quest objective.
        :type zoneUnlocks: list
        """
        # Process the args.
        if type(npc) in (int, NPCToonConstants.NPCToonID):
            npc = (npc, npc)
        if isinstance(rewards, QuestReward):
            rewards = [rewards]
        elif rewards is None:
            rewards = []

        # Set the args.
        self.npc = npc
        self.rewards = rewards
        self.nextStep = nextStep
        self.npcReturnable = npcReturnable
        self.zoneUnlocks = zoneUnlocks or []

        # Assigned externally.
        self.objectiveIndex = None

        # Add objective class.
        if self.__class__ not in self.objectiveClasses:
            # DO NOT USE A SET FOR THIS! SETS ARE UNSORTED AND THIS LIST IS TAKEN FROM RANDOMLY
            self.objectiveClasses.append(self.__class__)

    """
    Processing methods (on initialization)    
    """

    def assignNextStep(self, nextStep) -> None:
        """
        Called when processing from QuestLine.
        Assigns a proper nextStep variable to this object.

        :param nextStep: Union[int, Tuple[int], str]
        """
        self.nextStep = nextStep

    def assignObjectiveIndex(self, objectiveIndex: int) -> None:
        """
        Called when processing from QuestLine.
        Sets the objectiveIndex of the quest objective.
        """
        self.objectiveIndex = objectiveIndex

    """
    Reward accumulation
    """

    def calculateProgress(self, context: QuestContext, questReference: QuestReference, quester: Quester) -> int:
        """
        Figures out how much progress we should accumulate,
        based on the attributes of the given QuestContext.
        :param context: Some QuestContext object.
        :return: An integer remarking progress.
        """
        raise NotImplementedError

    """
    Random Task Generation
    """

    @staticmethod
    def canQuesterGetRandomTask(questerType: QuesterType) -> bool:
        """
        Determines if a Quester can get a random task.
        """
        return True

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
        return None

    @staticmethod
    def getObjectiveWeight(questerType: QuesterType) -> int:
        """
        The likelihood for this objective to be chosen in a pool.
        The de facto amount is 100.
        """
        return 100

    @classmethod
    def generateFromDifficulty(cls, rng, difficulty: float, questSource: QuestSource, **extraArgs):
        """
        Given an arbitrary difficulty value, generate a QuestObjective.
        For more info, seek QuestGenerator.py.

        :param rng:        A seeded Random instance. Use this for .random() or .randint() calculations.
        :param difficulty: The arbitrary difficulty of the task.
        :return:           This QuestObjective, set with values to match the arbitrary difficulty.
        """
        return cls(
            npcReturnable=False,
        )

    def getLowestToonLevel(self) -> Optional[int]:
        """Returns the lowest recommend toon level for the quest.
        stars at 0 probably i guess"""
        return self.lowestToonLevel

    """
    Getters
    """

    def getCompletionRequirement(self) -> int:
        """Returns the amount of progress needed to make on this objective before
        it can be completed.
        """
        return 1

    def isComplete(self, questReference: QuestReference, objectiveIndex: int, quester: Quester) -> bool:
        """
        Given a QuestReference, determines if the quest is complete or not.
        :param questReference: The quest reference to use.
        :param objectiveIndex: The objective index to use.
        """
        return questReference.getProgress()[objectiveIndex] >= self.getCompletionRequirement()

    def getTrueNextStep(self):
        """Returns the true nextStep variable (no tuple processing or dict weights).
        
        :rtype: Union[int, Tuple[int], str, None]
        """
        return self.nextStep

    def getNextStep(self):
        """Returns the next step. Does processing for randomization."""
        if type(self.nextStep) is tuple:
            return random.choice(self.nextStep)
        return self.nextStep

    def getQuestRewards(self):
        """Returns all QuestRewards.
        
        :rtype: Tuple[QuestReward]
        """
        return self.rewards

    """
    NPC accessors
    """

    def getFromNpcId(self) -> int:
        """Gets the 'from' NPC."""
        return self.npc[0]

    def getFromNpcName(self):
        return NPCToons.getNPCName(self.getFromNpcId())

    def getFromNpcZone(self):
        if self.getFromNpcId() == 2007:
            # Lowden hack
            return 2520
        return NPCToons.getNPCZone(self.getFromNpcId())

    def getFromNpcHoodId(self):
        return ZoneUtil.getCanonicalHoodId(self.getFromNpcZone())

    def getFromNpcLocationName(self):
        return base.cr.hoodMgr.getFullnameFromId(self.getFromNpcHoodId())

    def getFromNpcBuildingName(self):
        return NPCToons.getBuildingTitle(self.getFromNpcZone())

    def getFromNpcBranchId(self):
        return ZoneUtil.getBranchZone(self.getFromNpcZone())

    def getFromNpcStreetName(self):
        return ZoneUtil.getStreetName(self.getFromNpcBranchId())

    def getToNpcId(self) -> int:
        """Gets the 'to' NPC."""
        return self.npc[1]

    def getResolvableNpcIds(self) -> list:
        """Gets a list of all NPCs that can complete the objective."""
        return [self.npc[1]]

    def getToNpcName(self):
        return NPCToons.getNPCName(self.getToNpcId())

    def getToNpcZone(self):
        if self.getToNpcId() in (2007, 2009):
            # Lowden/Bumpy hack
            return 2520
        return NPCToons.getNPCZone(self.getToNpcId())

    def getToNpcHoodId(self):
        return ZoneUtil.getCanonicalHoodId(self.getToNpcZone())

    def getToNpcLocationName(self):
        return base.cr.hoodMgr.getFullnameFromId(self.getToNpcHoodId())

    def getToNpcBuildingName(self):
        return NPCToons.getBuildingTitle(self.getToNpcZone())

    def getToNpcBranchId(self):
        return ZoneUtil.getBranchZone(self.getToNpcZone())

    def getToNpcStreetName(self):
        return ZoneUtil.getStreetName(self.getToNpcBranchId())

    """
    Gameplay and client modification
    """

    def modifyPoster(self, questReference: QuestReference, poster):
        """
        Given a QuestPoster, update it to match what this objective should be.

        :param questReference:  The poster's quest reference.
        :param poster:          The poster GUI itself.
        :type poster:           QuestPoster
        """
        raise NotImplementedError

    def getInfoTextStrings(self, questReference: QuestReference):
        """
        Given a QuestReference, return info strings relevant to this objective.
        These are the three lines that show up on the QuestPoster.

        If you need the text to change when the poster is green/completed,
        you can determine that by checking questReference.isQuestComplete(self.objectiveIndex).

        :param questReference: The quest reference to use.
        :return: Info strings wrapped in a tuple, match the formatting in QuestLocalizer.
                 Custom formats can be specified per QuestObjective class in QuestLocalizer
        :rtype: tuple
        """
        buildingName, streetName, locationName = self.getToNpcBuildingName(), self.getToNpcStreetName(), self.getToNpcLocationName()
        if buildingName == locationName:
            return buildingName, streetName
        return buildingName, streetName, locationName

    def getSpeedchatMessages(self, quester, questReference: QuestReference):
        """
        Given a QuestReference, return Speedchat messages to be expressed.

        If you need the text to change when the poster is green/completed,
        you can determine that by checking questReference.isQuestComplete(self.objectiveIndex).

        :param questReference: The quest reference to use.
        :return: Speedchat messages, formatted and wrapped in a tuple.
        :rtype: tuple
        """
        raise NotImplementedError

    def getHeadline(self, questReference: QuestReference, objectiveSelected: int = 0) -> str:
        """Returns the all-caps task headline, directing the goal of the task."""
        raise NotImplementedError
    
    def getObjectiveGoal(self) -> str:
        """Returns the goal of the current objective, used for the RewardPanel."""
        raise NotImplementedError
    
    def getProgressString(self, questReference: QuestReference, progress: int) -> str:
        """Returns a string similar to the one seen on QuestPoster progress bars."""
        raise NotImplementedError

    def getProgressFormat(self, questReference):
        """Returns a string to mark progress for tasks."""
        raise NotImplementedError

    """
    Handy generics for building speedchat messages
    """

    def getFinishToontaskStrings(self):
        """Returns a list of Toontask strings that explicitly tell you to
        go visit the toNpc.
        
        :rtype: tuple
        """
        npcZone = self.getToNpcZone()
        hoodId = self.getToNpcHoodId()
        hoodName = ToontownGlobals.hoodNameMap[ZoneUtil.getCanonicalZoneId(hoodId)][-1]
        branchId = ZoneUtil.getCanonicalBranchZone(npcZone)

        from toontown.quest3.QuestLocalizer import SC_Visit, SC_VisitBuilding, SC_VisitBuildingWhere, \
            SC_VisitPlayground, SC_VisitSpecific

        # Concatenate all the strings.
        strings = [SC_Visit % self.getToNpcName()]
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

    @staticmethod
    def getLocationName(zoneId: int = None, lowercaseAnywhere: bool = False, raw: bool = False):
        if zoneId is None:
            locName = 'Anywhere' if not lowercaseAnywhere else 'anywhere'
        elif zoneId in ToontownGlobals.hoodNameMap:
            if not raw:
                locName = TTLocalizer.QuestInLocationString % {'inPhrase': ToontownGlobals.hoodNameMap[zoneId][1],
                 'location': ToontownGlobals.hoodNameMap[zoneId][-1] + TTLocalizer.QuestsLocationArticle}
            else:
                locName = ToontownGlobals.hoodNameMap[zoneId][-1]
        elif zoneId in ToontownGlobals.StreetBranchZones:
            if not raw:
                locName = TTLocalizer.QuestInLocationString % {'inPhrase': ToontownGlobals.StreetNames[zoneId][1],
                 'location': ToontownGlobals.StreetNames[zoneId][-1] + TTLocalizer.QuestsLocationArticle}
            else:
                locName = ToontownGlobals.StreetNames[zoneId][-1]
        elif zoneId in list(TTLocalizer.zone2TitleDict.keys()):
            locName = TTLocalizer.zone2TitleDict.get(zoneId)[0]
            branchZone = ZoneUtil.getCanonicalBranchZone(zoneId)
            hoodId = ZoneUtil.getHoodId(zoneId)
            if branchZone in ToontownGlobals.StreetBranchZones:
                locName += '\n' + ToontownGlobals.StreetNames[branchZone][2]
            if hoodId in ToontownGlobals.hoodNameMap:
                locName += '\n' + ToontownGlobals.hoodNameMap[hoodId][2]
        elif zoneId in SpecialQuestZones:
            from toontown.quest3.QuestLocalizer import SpecialQuestZone2Name
            zoneStrTuple = SpecialQuestZone2Name.get(zoneId, ('UNDEFINED', 'UNDEFINED', 'UNDEFINED'))
            locName = TTLocalizer.QuestInLocationString % {'inPhrase': zoneStrTuple[1],
             'location': zoneStrTuple[-1] + TTLocalizer.QuestsLocationArticle}
        else:
            locName = 'QuestObjective.getLocationName()'  # Please fix this apparently this is bad according to tubby
        return locName

    """
    Repr methods
    """

    def _getKwargStr(self):
        kwargstr = ''
        if self.npc:
            if type(self.npc) is tuple and self.npc[0] == self.npc[1]:
                kwargstr += f'npc={self.npc[0]}, '
            else:
                kwargstr += f'npc={self.npc}, '
        if self.rewards:
            kwargstr += f'rewards={self.rewards}, '
        if self.nextStep:
            kwargstr += f'nextStep={self.nextStep}, '
        return kwargstr

    def _numToLocStr(self, num):
        # sory
        nameStr = {
            1000: 'DonaldsDock',
            2000: 'ToontownCentral',
            3000: 'TheBrrrgh',
            4000: 'MinniesMelodyland',
            5000: 'DaisyGardens',
            6000: 'OutdoorZone',
            7000: 'OldeToontown',
            8000: 'GoofySpeedway',
            9000: 'DonaldsDreamland',
            17000: 'GolfZone',
            18000: 'ToonselTown',
            19000: 'SkyClan',
            15000: 'Tutorial',
            1100: 'BuccaneerBoulevard',
            1200: 'SeaweedStreet',
            1300: 'LighthouseLane',
            1400: 'AnchorAvenue',
            2100: 'SillyStreet',
            2200: 'LoopyLane',
            2300: 'PunchlinePlace',
            2400: 'WackyWay',
            3100: 'WalrusWay',
            3200: 'SleetStreet',
            3300: 'PolarPlace',
            3400: 'ArcticAvenue',
            4100: 'AltoAvenue',
            4200: 'BaritoneBoulevard',
            4300: 'TenorTerrace',
            4400: 'SopranoStreet',
            5100: 'PetuniaPlace',
            5200: 'DaisyDrive',
            5300: 'TulipTerrace',
            5400: 'SunflowerStreet',
            6100: 'AlmondAvenue',
            6200: 'PeanutPlace',
            6300: 'WalnutWay',
            6400: 'LegumeLane',
            7100: 'KnightKnoll',
            7200: 'NobleNook',
            7300: 'WizardWay',
            9100: 'LullabyLane',
            9200: 'PajamaPlace',
            9300: 'TwilightTerrace',
            2513: 'ToonHall',
            2921: 'Gagsoline',
            7507: 'OldeToontownDungeon',
            4507: 'RandomTunes',
            3607: 'BlizzardWizard',
            1903: 'TellTaleCarp',
        }.get(num, None)
        if nameStr:
            return f'ToontownGlobals.{nameStr}'
        return num

    def __repr__(self):
        return f'QuestObjective({self._getKwargStr()[:-2]})'


class MultiObjective:
    """
    A container for multi-objective tasks.
    Holds logic on how the quest should declare itself to be completed.
    """

    __slots__ = 'questObjectives', 'wantAll'

    def __init__(self, *questObjectives, wantAll: bool = True):
        """
        Declares a group of objectives, associated with one task step.

        :param questObjectives:  The quest objective list.
        :param wantAll:          Do we need all objectives to be complete to finish the objective?
        """
        self.questObjectives = tuple(questObjectives)
        self.wantAll = wantAll

    def isComplete(self, questReference: QuestReference, context: QuestContext, quester: Quester) -> bool:
        """
        Given a QuestReference, determines if the quest container is complete or not.
        Subclasses of MultiObjective can override this for unique functionality.
        """
        # First, determine if this objective line requires NPC completion.
        npcsRequired = []
        for questObjective in self.getQuestObjectives():
            if questObjective.npcReturnable:
                npcsRequired.extend(questObjective.getResolvableNpcIds())

        # Do our quest objectives need to be NPC completed?
        if npcsRequired:
            # We see if the NPC IDs line up with context.
            if type(context) is not NPCInteractContext:
                return False

            # Does this context check out?
            context: NPCInteractContext
            if context.getNpcId() not in npcsRequired:
                return False

        # We then do standard logic to ask if all objectives are complete.
        if self.wantAll:
            # All objectives must be considered complete.
            return all(questObjective.isComplete(questReference=questReference,
                                                 objectiveIndex=index, quester=quester)
                       for index, questObjective in enumerate(self.getQuestObjectives()))

        # Any of the objectives have to be considered complete.
        return any(questObjective.isComplete(questReference=questReference,
                                             objectiveIndex=index, quester=quester)
                   for index, questObjective in enumerate(self.getQuestObjectives()))

    """
    Handy getters
    """

    def getInitialObjective(self) -> QuestObjective:
        """
        Gets the initial objective from the MultiObjective.
        """
        return self.getObjectiveIndex(0)

    def getObjectiveIndex(self, objectiveIndex: int) -> QuestObjective:
        """Returns an objective index."""
        return self.getQuestObjectives()[objectiveIndex]

    def getQuestObjectives(self):
        """Returns the list of quest objective.
        
        :rtype: tuple
        """
        return self.questObjectives

    def getObjectiveCount(self) -> int:
        """Gets a count of the quest objectives."""
        return len(self.questObjectives)

    def __repr__(self):
        retString = ''
        for objective in self.questObjectives:
            retString += f'\n\t{repr(objective)}'
        return retString
