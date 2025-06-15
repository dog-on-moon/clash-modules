from panda3d.core import ConfigVariableString

from toontown.quest3.rewards import *
from toontown.quest3.QuestEnums import QuestSource
from toontown.quest3.base.QuestChain import QuestChain
from toontown.quest3.base.QuestHistory import QuestHistory
from toontown.quest3.base.QuestLine import QuestLine
from toontown.quest3.base.QuestObjective import MultiObjective, QuestObjective
from toontown.quest3.base.QuestReference import QuestId, QuestReference
from toontown.quest3.questlines.MainQuestLine import MainQuestLine
from toontown.quest3.questlines.SideQuestLine import SideQuestLine
from toontown.quest3.questlines.DirectiveQuestLine import DirectiveQuestLine
from toontown.quest3.questlines.KudosQuestLine import KudosQuestLine
from toontown.quest3.questlines.DailyQuestLine import DailyQuestLine
from toontown.quest3.base.Quester import Quester
from toontown.toonbase import ToontownGlobals


def getSidequests(quester: Quester):
    """
    :rtype: List[Tuple[int, QuestChain]]
    """
    return SideQuestLine.getValidQuestChains(quester)


def getDirectives(quester: Quester):
    """
    :rtype: List[Tuple[int, QuestChain]]
    """
    return DirectiveQuestLine.getValidQuestChains(quester)


def getSidequestsByNpcId(quester: Quester, npcId: int):
    """Generates a list of available sidequests and directives based on
    the given quester and the quests which the given npc toon can provide.

    :param quester: Quester object.
    :param npcId: ID of the NPCToon.
    :return: A list of quests.
    :rtype: List[QuestId]
    """
    # Get all of the sidequests that are accessible to this quester.
    sidequests = getSidequests(quester)
    directives = getDirectives(quester)

    validSidequests = []
    for quests, questSource in zip((sidequests, directives), (QuestSource.SideQuest, QuestSource.Directive)):
        for chainId, chain in quests:
            chain: QuestChain

            # Get the first objective of the quest chain.
            firstObjective = chain.getInitialObjective()

            # Get the npcId from this objective.
            fromNpc = firstObjective.getFromNpcId()

            # The npcId matches the npcId of the first npc of the chain.
            if npcId == fromNpc:
                # The chainId does not exist in the quester's quest history.
                if not quester.hasCompletedQuest(questSource, chainId):
                    questId = QuestId(questSource, chainId, chain.getStartObjectiveId())
                    # The questId does not exist in any of their quest references.
                    if not quester.hasQuest(questId):
                        validSidequests.append(questId)

    return validSidequests


def getAvailableSidequests(quester: Quester, branchZone: int=0):
    """Get all of the sidequests that are accessible to the indicated quester.

    :rtype: List[QuestId]
    """
    validSidequests = []
    for chainId, chain in getSidequests(quester):
        chain: QuestChain

        # Get the first objective of the quest chain.
        firstObjective = chain.getInitialObjective()

        # Get the npc's branch zone from this objective.
        npcBranchId = firstObjective.getFromNpcBranchId()

        if not branchZone or npcBranchId == branchZone:
            # The chainId does not exist in the quester's quest history.
            if not quester.hasCompletedQuest(QuestSource.SideQuest, chainId):
                questId = QuestId(QuestSource.SideQuest, chainId, chain.getStartObjectiveId())
                # The questId does not exist in any of their quest references.
                if not quester.hasQuest(questId):
                    validSidequests.append(questId)

    return validSidequests


def isInTutorial(quester: Quester) -> bool:
    """Check if the given quester has the tutorial quest chain by checking
    if it isn't in their quest history.
    """
    if quester is None:
        return False
    return not quester.hasCompletedQuest(QuestSource.MainQuest, 1)


# Whenever a quester logs in, ensure that they have the rewards
# specified here.
SANITY_REWARDS = (
    TeleportReward
)

# What doors are locked?
LOCKED_DOORS = {
    100: ToontownGlobals.Gagsoline,
    101: ToontownGlobals.BlizzardWizard,
}

# The quest history required to be considered "complete" with a Playground.
QuestHistoryForPlaygroundCompletion = {
    ToontownGlobals.ToontownCentral:    QuestHistory(questSource=QuestSource.MainQuest, chainId=11),
    ToontownGlobals.DonaldsDock:        QuestHistory(questSource=QuestSource.MainQuest, chainId=21),
    ToontownGlobals.OldeToontown:       QuestHistory(questSource=QuestSource.MainQuest, chainId=31),
    ToontownGlobals.DaisyGardens:       QuestHistory(questSource=QuestSource.MainQuest, chainId=41),
    ToontownGlobals.MinniesMelodyland:  QuestHistory(questSource=QuestSource.MainQuest, chainId=48),
    ToontownGlobals.TheBrrrgh:          QuestHistory(questSource=QuestSource.MainQuest, chainId=56),
    ToontownGlobals.OutdoorZone:        QuestHistory(questSource=QuestSource.MainQuest, chainId=66),
    ToontownGlobals.DonaldsDreamland:   QuestHistory(questSource=QuestSource.MainQuest, chainId=74),
}


def canEnterQuestBuilding(zoneId: int, quester: Quester) -> bool:
    """Determine if the quester can access the given zoneId based on
    if they have completed an objective which unlocks the zoneId for them.
    """
    # Always True if we aren't attempting to enter a quest area.
    if zoneId not in LOCKED_DOORS.values():
        return True

    # First, check their quest history.
    for questHistory in quester.getQuestHistory():
        questHistory: QuestHistory
        chain: QuestChain = QuestLine.getQuestChainFromId(questHistory.questSource, questHistory.chainId, quester=quester)

        # Iterate this chain's multiobjectives.
        for multiObjective in chain.steps.values():
            multiObjective: MultiObjective

            # Iterate the objectives of the multiobjective.
            for objective in multiObjective.getQuestObjectives():
                objective: QuestObjective
                # If the given zoneId is in the objectives "zoneUnlocks",
                # they are granted access.
                if zoneId in objective.zoneUnlocks:
                    return True
    
    # Next, check their quest references.
    for questReference in quester.getQuestReferences():
        questReference: QuestReference
        chain: QuestChain = QuestLine.getQuestChainFromQuestId(questReference.getQuestId(), quester=quester)

        # We assume we are completed until we get to the relevant objective.
        completedTo = True

        # Iterate this chain's multiobjectives.
        for step, multiObjective in chain.steps.items():
            multiObjective: MultiObjective

            # Iterate the objectives of the multiobjective.
            for i, objective in enumerate(multiObjective.getQuestObjectives()):
                objective: QuestObjective

                # If we are at this task, we must check if we have completed it.
                if questReference.getObjectiveId() == step:
                    objectiveCompleted = objective.isComplete(questReference, i, quester)

                # Otherwise, it is just if we have completed all the tasks up to this point.
                else:
                    objectiveCompleted = completedTo

                # If the given zoneId is in the objective's "zoneUnlocks",
                # and the objective has been completed, they are granted access.
                if zoneId in objective.zoneUnlocks and objectiveCompleted:
                    return True

            # At this point, we have completed no more after this.
            if questReference.getObjectiveId() == step:
                completedTo = False

    # They are not allowed here.
    return False


# The types of quest sources that do not hold weight in quest refs.
# (i.e. are not shown on regular task panels)
HiddenQuestSources = [
    QuestSource.DailyQuest,
]


SUIT_NPC_IDS = {
    12101: "judy",
}


"""
Zone protection code
"""

protectedBuildings = [
    2606, 2602, 2605, 2708, 2705, 2704, 2701, 2803, 2804, 2809, 2805, 5607, 1707, 5609, 3605, 3703, 7706, 4908, 1903, 9835
]

# Temporary protection for count replacement building, it's a bit buggy.
protectedBuildings += [3833]

# Temporary protection for Flora's Flowers because the building is bugged atm.
protectedBuildings += [5911]

# trickOrTreatBuildings = [2717, 1718, 7805, 5909, 4904, 3829, 6835, 9814]  # TODO: TWEAK AND UNCOMMENT FOR HALLOWEEN
# protectedBuildings += trickOrTreatBuildings

# carolingBuildings = [2665, 1913, 7803, 5835, 4828, 3611, 6904, 9737]  # TODO: RE-COMMENT AFTER CHRISTMAS
# protectedBuildings += carolingBuildings

# Dynamically append TrickOrTreatZones or CarolZones to protectedBuildings if we're in the middle of halloween or christmas
# Note: since I'm both not sure when this file first gets called, and since this gets called both on AI and client,
# we'll check with ConfigVaribleString instead
season = ConfigVariableString('current-seasonal-holiday', 'None').getValue()
if season == 'halloween':
    protectedBuildings.extend(ToontownGlobals.TrickOrTreatZones)

if season == 'christmas':
    protectedBuildings.extend(ToontownGlobals.carolNames.keys())

potentialBuildings = {}

# Iterate the main/side quest lines.
for questLine in (MainQuestLine, SideQuestLine):
    # Iterate its chains.
    for chain in questLine.questLine.values():
        # Iterate the chain's multiobjectives.
        for multiObjective in chain.steps.values():
            # Iterate the objectives of the multiobjective.
            for questObjective in multiObjective.getQuestObjectives():
                # Get the zoneId which the NPC resides in.
                zoneId = questObjective.getToNpcZone()
                if not zoneId:
                    continue # Sanity
                
                # All TTC/BB zoneIds are protected.
                if 1000 <= zoneId <= 2999:
                    protectedBuildings.append(zoneId)
                    continue
                
                # Add the zoneId to the potentialBuildings dict.
                if zoneId in potentialBuildings:
                    potentialBuildings[zoneId] += 1
                    # If the zoneId has 3 hits, protect it.
                    if potentialBuildings[zoneId] == 3:
                        protectedBuildings.append(zoneId)
                else:
                    potentialBuildings[zoneId] = 1

protectedBuildings = set(protectedBuildings)
del potentialBuildings


def isZoneProtected(zoneId: int) -> bool:
    """Is the zoneId protected?"""
    return zoneId in protectedBuildings
