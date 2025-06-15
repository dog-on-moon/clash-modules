"""
A globals class for Boosters.
"""
from toontown.battle.attacks.base.AttackEnum import AttackEnum
from toontown.inventory.enums.ItemEnums import BoosterItemType
from typing import TYPE_CHECKING
import random

if TYPE_CHECKING:
    from toontown.booster.BoosterBase import BoosterBase
    from toontown.toon.DistributedToonAI import DistributedToonAI


MAX_BOOSTER_DURATION = 7 * 24 * 60 * 60  # one week, in seconds


suitDeptToBoosterType = {
    's': [BoosterItemType.Merit_Sellbot,  BoosterItemType.Reward_Boss_Sellbot,  BoosterItemType.Exp_Dept_Sellbot],
    'm': [BoosterItemType.Merit_Cashbot,  BoosterItemType.Reward_Boss_Cashbot,  BoosterItemType.Exp_Dept_Cashbot],
    'l': [BoosterItemType.Merit_Lawbot,   BoosterItemType.Reward_Boss_Lawbot,   BoosterItemType.Exp_Dept_Lawbot],
    'c': [BoosterItemType.Merit_Bossbot,  BoosterItemType.Reward_Boss_Bossbot,  BoosterItemType.Exp_Dept_Bossbot],
    'g': [BoosterItemType.Merit_Boardbot, BoosterItemType.Reward_Boss_Boardbot, BoosterItemType.Exp_Dept_Boardbot],
}

# Department nums, DO NOT USE WHEN NOT DEALING WITH DAILIES, THESE ARE 1 BASED, CODEBASE IS 0 BASED
BOARDBOT = 1
BOSSBOT = 2
LAWBOT = 3
CASHBOT = 4
SELLBOT = 5

actualDept2RewardDept = {
    0: BOARDBOT,
    1: BOSSBOT,
    2: LAWBOT,
    3: CASHBOT,
    4: SELLBOT
}

# Convert dept to respective rewards
dept2Reward = {
    1: BoosterItemType.Merit_Sellbot,
    2: BoosterItemType.Merit_Cashbot,
    3: BoosterItemType.Merit_Lawbot,
    4: BoosterItemType.Merit_Bossbot,
    5: BoosterItemType.Merit_Boardbot,
}

# These boosters won't get bonuses from all star boosters
allOutBoosterBannedTypes = [
    BoosterItemType.Jellybeans_Bingo,
    BoosterItemType.Gumballs_Global,
]


"""
Useful functions
"""


def getReasonableBooster(av, includeSuper: bool = False, seed: int = None) -> BoosterItemType:
    """
    Gets a list of booster enums that would be reasonable to give to an av.
    Weighted and returns a random relevant booster.

    :param av: The avatar in question.
    :param includeSuper: Add super boosters.
    :param seed: A seed to use.
    :type av: DistributedToonAI
    """
    reasonableBoosters: list[BoosterItemType] = [BoosterItemType.Jellybeans_Global]

    # Add simple ones.
    if includeSuper:
        reasonableBoosters.append(BoosterItemType.AllStar)

    # Focus on gags that need to be trained.
    needSupportExp = False
    needPowerExp = False
    experience = av.getExperience()

    # Go over alll the tracks and see where we need XP.
    for track in [AttackEnum.TOON_HEAL, AttackEnum.TOON_LURE,
                  AttackEnum.TOON_SOUND, AttackEnum.TOON_SQUIRT]:
        if not av.hasTrackAccess(track):
            continue
        if experience.isTrackMaxed(track):
            continue
        needSupportExp = True
    for track in [AttackEnum.TOON_TRAP, AttackEnum.TOON_ZAP,
                  AttackEnum.TOON_THROW, AttackEnum.TOON_DROP]:
        if not av.hasTrackAccess(track):
            continue
        if experience.isTrackMaxed(track):
            continue
        needPowerExp = True

    # Add the boosters now.
    if needSupportExp:
        reasonableBoosters.append(BoosterItemType.Exp_Gags_Support)
    if needPowerExp:
        reasonableBoosters.append(BoosterItemType.Exp_Gags_Power)

    # Add the super XP if we want.
    if (needSupportExp or needPowerExp) and includeSuper:
        reasonableBoosters.append(BoosterItemType.Exp_Gags_Global)

    # Focus on activity XP.
    from toontown.toonbase import ToontownGlobals
    needsActivityExp = False
    if not av.isActivityMaxed(ToontownGlobals.ACTIVITY_FISHING):
        reasonableBoosters.append(BoosterItemType.Exp_Activity_Fishing)
        needsActivityExp = True
    if not av.isActivityMaxed(ToontownGlobals.ACTIVITY_TROLLEY):
        reasonableBoosters.append(BoosterItemType.Exp_Activity_Trolley)
        needsActivityExp = True
    if not av.isActivityMaxed(ToontownGlobals.ACTIVITY_GOLFING):
        reasonableBoosters.append(BoosterItemType.Exp_Activity_Golf)
        needsActivityExp = True
    if av.hasKart() and not av.isActivityMaxed(ToontownGlobals.ACTIVITY_RACING):
        reasonableBoosters.append(BoosterItemType.Exp_Activity_Racing)
        needsActivityExp = True
    if needsActivityExp and includeSuper:
        reasonableBoosters.append(BoosterItemType.Exp_Activity_Global)

    # Go through the departments, add their stuff if reasonable.
    from toontown.suit import SuitDNA
    from toontown.coghq import CogDisguiseGlobals
    hasBoss = False
    needsDeptExp = False
    needsMerit = False
    for dept in SuitDNA.suitDepts:
        if dept == 'g':
            # No boardbot boosters for now -- oh god, I almost missed this for 1.3
            # Thanks Sunny
            continue

        # Is their suit complete?
        deptIndex = CogDisguiseGlobals.dept2deptIndex(dept)
        if not CogDisguiseGlobals.isSuitComplete(av.getCogParts(), dept):
            # No, ignore it.
            continue

        # Their suit is complete.
        hasBoss = True
        meritBooster, rewardBooster, deptExpBooster = suitDeptToBoosterType.get(dept)

        # The reward booster is fine, naturally.
        reasonableBoosters.append(rewardBooster)

        # Do they need department exp?
        if not av.isDepartmentMaxed(dept):
            needsDeptExp = True
            reasonableBoosters.append(deptExpBooster)

        # Do they need merits?
        if not av.readyForPromotion(deptIndex):
            needsMerit = True
            reasonableBoosters.append(meritBooster)

    # Add various universals if it makes sense to.
    if includeSuper:
        if hasBoss:
            reasonableBoosters.append(BoosterItemType.Reward_Boss_Global)

        if needsDeptExp:
            reasonableBoosters.append(BoosterItemType.Exp_Dept_Global)

        if needsMerit:
            reasonableBoosters.append(BoosterItemType.Merit_Global)

    # Pick a random booster now.
    from toontown.inventory.registry.ItemTypeRegistry import getItemDefinition
    boosterPool = {
        itemType: getItemDefinition(itemType).getRandomWeight()
        for itemType in reasonableBoosters
        if getItemDefinition(itemType).getRandomWeight()
    }
    rng = random.Random()
    if seed is not None:
        rng.seed(seed)
    return rng.choices(
        list(boosterPool.keys()),
        weights=list(boosterPool.values()),
        k=1,
    )[0]
