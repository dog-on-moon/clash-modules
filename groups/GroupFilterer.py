"""
A class designed to be able to run checks on a given Toon instance
to see whether or not it can join a target Group instance.

Compatible for both client and AI usage.
"""
from enum import Enum, auto

from toontown.coghq import CogDisguiseGlobals
from toontown.groups.GroupGlobals import (
    Responses, GroupType, GroupDefinition, GroupZoneIds,
    BoardingGroupInformation, entranceType2FacilityZone,
)
from toontown.groups.GroupClasses import GroupAI, GroupCreation
from toontown.toon import Experience
from enum import Enum, auto
from toontown.hood import ZoneUtil
from toontown.toonbase.ToontownGlobals import MaxCogSuitLevel, deptIndex2cogHQZoneId, cogHQZoneId2HardmodeQuestId, factoryId2factoryType
from toontown.racing.RaceGlobals import RacePriceLowest, RacePriceHighest


class IgnoreSafetyEnum(Enum):
    DontIgnore = auto()
    IgnoreAll = auto()
    IgnoreZones = auto()


class GroupFilterer:
    """
    Contains methods for testing whether a target Toon
    can join a target Group or not.
    """

    def getGroupCreationFromGroupType(self, groupType: GroupType) -> GroupCreation:
        """Gets a default GroupCreation from a GroupType variable."""
        groupDef: GroupDefinition = BoardingGroupInformation[groupType]
        groupOptions = groupDef.defaultOptions
        groupSize = groupDef.defaultMaxSize
        return GroupCreation(
            groupType=groupType, groupOptions=groupOptions, groupSize=groupSize
        )

    def runGroupTestsFromGroupType(self, toon, groupType: GroupType, force: bool = True,
                                   group: GroupAI = None, ignoreSafety=IgnoreSafetyEnum.IgnoreAll):
        return self.runGroupTests(
            toon, self.getGroupCreationFromGroupType(groupType),
            force, group, ignoreSafety
        )

    def runGroupTests(self, toon, groupCreation: GroupCreation, force: bool, group: GroupAI = None,
                      ignoreSafety=IgnoreSafetyEnum.DontIgnore) -> Responses:
        """
        Delegates several tests depending on group type.

        When "force" is set to true, we'll ignore potential warnings, while
        don't exactly prevent a user from joining a group, is
        strongly not recommended for them to join.

        ignoreSafety, 0 will run safety checks, 1 will run no safety checks, and 2 will run only basic test.
        """
        testDict = {
            GroupType.VP: self.testBoss,
            GroupType.CFO: self.testBoss,
            GroupType.CLO: self.testBoss,
            GroupType.OCLO: self.testHMBoss,
            GroupType.CEO: self.testBoss,
            GroupType.FrontFactory: self.testFacility,
            GroupType.SideFactory: self.testFacility,
            GroupType.CoinMint: self.testFacility,
            GroupType.DollarMint: self.testFacility,
            GroupType.BullionMint: self.testFacility,
            GroupType.LawficeA: self.testFacility,
            GroupType.LawficeB: self.testFacility,
            GroupType.LawficeC: self.testFacility,
            GroupType.SilverSprocket: self.testFacility,
            GroupType.GoldenGear: self.testFacility,
            GroupType.DiamondDynamo: self.testFacility,
            GroupType.Racing: self.testRacing,
            GroupType.BuildingSell: self.testBuilding,
            GroupType.BuildingCash: self.testBuilding,
            GroupType.BuildingLaw: self.testBuilding,
            GroupType.BuildingBoss: self.testBuilding,
            GroupType.BuildingBoard: self.testBuilding,
        }
        defaultTests = [
            self.testProgression,
        ]
        if ignoreSafety == IgnoreSafetyEnum.IgnoreAll:
            safeTests = []
        elif ignoreSafety == IgnoreSafetyEnum.IgnoreZones:
            safeTests = [self.testBasic, self.testSafe, self.testDynamicZones]
        else:
            safeTests = [self.testBasic, self.testSafe, self.testZones, self.testDynamicZones]

        # Run the tests lined out in the test dict.
        groupType = groupCreation.groupType
        groupDef = BoardingGroupInformation[groupType]
        groupOptions = groupCreation.groupOptions

        # Check if we need to add min laff/gag tests
        if groupDef.minLaffRec is not None:
            safeTests.append(self.testLaffRec)
        if groupDef.minGagRec is not None:
            safeTests.append(self.testGagRec)

        tests = tuple(defaultTests + safeTests + [testDict.get(groupType, None)])
        # Run the tests in the test dict.
        for test in tests:
            if test is None:
                continue
            try:
                result = test(toon, groupType, groupDef, groupOptions, force, group)
                if result is not Responses.OK:
                    return result
            except Exception as e:
                if hasattr(self, 'notify'):
                    self.notify.warning(f"Toon test {test} failed miserably with exception {e}!")
                else:
                    raise e
                return Responses.GeneralError
        return Responses.OK

    def testBasic(self, toon, groupType: GroupType,
                 groupDef: GroupDefinition, groupOptions: list, force: bool,
                  group: GroupAI = None) -> Responses:
        """
        Tests generic factors of the toon.
        """
        if not toon:
            return Responses.GeneralError
        if not hasattr(toon, 'zoneId'):
            return Responses.GeneralError
        if not self._canToonUseGroups(toon.doId):
            return Responses.PlayerGroupBanned
        # We're done.
        return Responses.OK

    def _canToonUseGroups(self, avId):
        """Determines if a toon can create a group."""
        return True

    def testDynamicZones(self, toon, groupType: GroupType,
                  groupDef: GroupDefinition, groupOptions: list, force: bool,
                  group: GroupAI = None) -> Responses:
        """
        Makes sure that the toon is not in a cringe dynamic zone
        """
        if ZoneUtil.isDynamicZone(toon.zoneId):
            return Responses.BadLocation

        return Responses.OK

    def testZones(self, toon, groupType: GroupType,
                  groupDef: GroupDefinition, groupOptions: list, force: bool,
                  group: GroupAI = None) -> Responses:
        """
        Makes sure that the toon is in a valid zone for the group.
        """
        singleZoneGood = toon.zoneId in GroupZoneIds
        fullHoodZoneGood = groupDef.allowFullHood and ZoneUtil.getHoodId(toon.zoneId) == ZoneUtil.getHoodId(
            groupDef.zoneId[0])
        if not (singleZoneGood or fullHoodZoneGood):
            return Responses.BadLocation

        return Responses.OK

    def testSafe(self, toon, groupType: GroupType,
                 groupDef: GroupDefinition, groupOptions: list, force: bool,
                  group: GroupAI = None) -> Responses:
        """
        Makes sure that the toon isn't in a battle.
        """
        if toon.getBattleId() > 0:
            return Responses.PlayerInBattle
        # We're done.
        return Responses.OK

    def testProgression(self, toon, groupType: GroupType,
                 groupDef: GroupDefinition, groupOptions: list, force: bool,
                  group: GroupAI = None) -> Responses:
        """
        Tests the taskline and playground progression of the toon.
        """
        toonQuestHistory = toon.getQuestHistory()
        # if the group requires visits, stop toon if they haven't visited a hood
        if groupDef.requireVisited:
            hasVisited = False
            toonHoods = toon.getHoodsVisited()
            for zoneId in groupDef.zoneId:
                if ZoneUtil.getHoodId(zoneId) in toonHoods:
                    hasVisited = True
                    break
            if not hasVisited:
                return Responses.AreaNotVisited
        # check the task requirement of the group
        taskReq = groupDef.taskRequired
        if taskReq is not None:
            if not toon.hasReachedQuest(taskReq.getQuestSource(),
                                        taskReq.getChainId(),
                                        taskReq.getObjectiveId()):
                return Responses.TooLowTaskProgression
        # We're done.
        return Responses.OK

    def testBoss(self, toon, groupType: GroupType,
                 groupDef: GroupDefinition, groupOptions: list, force: bool,
                  group: GroupAI = None) -> Responses:
        """
        Tests if the Toon can qualify for the boss group.
        """
        dept = groupDef.suitId
        if dept is None:
            raise Exception("testBoss called on group type without a suit requirement, groups configured wrongly?")
        # Check if they even have a suit.
        parts = toon.getCogParts()
        if not CogDisguiseGlobals.isSuitComplete(parts, dept):
            return Responses.BossNoSuit
        # Check for if they have merits.
        if not toon.readyForPromotion(dept):
            return Responses.BossNoMerits
        # We're done.
        return Responses.OK

    def testHMBoss(self, toon, groupType: GroupType,
                 groupDef: GroupDefinition, groupOptions: list, force: bool,
                  group: GroupAI = None) -> Responses:
        """
        Tests if the Toon can qualify for the boss group.
        """
        # First, they have to meet the standard boss requirements.
        result = self.testBoss(toon, groupType, groupDef, groupOptions, force)
        if result is not Responses.OK:
            return result
        dept = groupDef.suitId
        # Next, make sure they've completed the Overclocked directive.
        toonQuestHistory = toon.getQuestHistory()
        cogHQZone = deptIndex2cogHQZoneId(dept)
        if cogHQZoneId2HardmodeQuestId(cogHQZone) not in toonQuestHistory:
            return Responses.OverclockedNotUnlocked
        # If they have, make sure that they don't need to do a directive.
        if toon.cogLevels[dept] >= MaxCogSuitLevel:
            # They better not be at the COMPLETE END.
            if toon.cogTypes[dept] == 6 and toon.cogReviveLevels[dept] != 14:
                # Are they needing an directive ??
                if not toon.canIncReviveLevel(dept) and not force:
                    return Responses.WarningNeedDirective
        # We're done.
        return Responses.OK

    def testFacility(self, toon, groupType: GroupType,
                 groupDef: GroupDefinition, groupOptions: list, force: bool,
                  group: GroupAI = None) -> Responses:
        """
        Tests if the Toon can qualify for the given facility.
        """
        dept = groupDef.suitId
        if dept is None:
            raise Exception("testFacility called on group type without a suit requirement, groups configured wrongly?")
        # if their suit is incomplete, make sure that the group that
        # they are joining will give them the parts that they
        # are actually in need of getting
        parts = toon.getCogParts()
        if not CogDisguiseGlobals.isSuitComplete(parts, dept) and not force:
            entranceEnum = groupDef.entrance
            if entranceEnum is not None:
                if entranceEnum in entranceType2FacilityZone:
                    factoryZone = entranceType2FacilityZone[entranceEnum]
                    partFactoryType = factoryId2factoryType[factoryZone]
                    nextPart = None
                    for partTypeId in CogDisguiseGlobals.partTypeIds[partFactoryType]:
                        nextPart = CogDisguiseGlobals.getNextPart(toon.getCogParts(), partTypeId, dept)
                        if nextPart:
                            break
                    if not nextPart:
                        return Responses.WarningFacilityMissesPart
        # We're done.
        return Responses.OK

    def testRacing(self, toon, groupType: GroupType,
                 groupDef: GroupDefinition, groupOptions: list, force: bool,
                  group: GroupAI = None) -> Responses:
        """
        Tests if the Toon has enough jellybeans to race, lol.
        """
        if not toon.hasKart():
            return Responses.HasNoRaceKart
        if toon.getMoney() < RacePriceLowest:
            return Responses.TooBroke2RaceLol
        if RacePriceLowest <= toon.getMoney() < RacePriceHighest and not force:
            return Responses.WarningPerhapsTooPoorToRace
        # We're done.
        return Responses.OK

    def testBuilding(self, toon, groupType: GroupType,
                 groupDef: GroupDefinition, groupOptions: list, force: bool,
                  group: GroupAI = None) -> Responses:
        """
        Tests if the Toon has the location of the building discovered.
        """
        if group:
            if ZoneUtil.getHoodId(group.zoneId) not in toon.getHoodsVisited():
                return Responses.AreaNotVisited
        # We're done.
        return Responses.OK

    def testLaffRec(self, toon, groupType: GroupType,
                 groupDef: GroupDefinition, groupOptions: list, force: bool,
                  group: GroupAI = None) -> Responses:
        """
        Tests if the Toon meets the *recommended* minimum laff for this group type
        """
        if groupDef.minLaffRec is not None and toon.getMaxHp() < groupDef.minLaffRec and not force:
            return Responses.WarningBelowLaffRec
        # We're done.
        return Responses.OK

    def testGagRec(self, toon, groupType: GroupType,
                 groupDef: GroupDefinition, groupOptions: list, force: bool,
                  group: GroupAI = None) -> Responses:
        """
        Tests if the Toon meets the *recommended* minimum max gag tracks for this group type
        """
        if groupDef.minGagRec is not None and not force:
            experience = Experience.Experience(*toon.getExperience())
            numMaxed = 0
            for i, track in enumerate(toon.getTrackAccess()):
                if track and experience[i] >= Experience.MaxSkill:
                    numMaxed += 1

            if numMaxed < groupDef.minGagRec:
                return Responses.WarningBelowGagRec
        # We're done.
        return Responses.OK
