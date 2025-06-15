from toontown.toonbase import ProcessGlobals
from toontown.toonbase.ToontownGlobals import *
from toontown.instances.mercs.InstanceMercGlobals import *
from toontown.groups.GroupEnums import *
from toontown.hood import ZoneUtil
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from toontown.utils.BuiltinHelper import *

"""
Network enums
"""

PUBLISHED_GROUP_REFRESH_TIME = 3
AI_UPDATE_PLAYERS_REFRESH_TIME = 60
AI_RATELIMITER_MAX_HITS = 10
AI_RATELIMITER_PERIOD = 5
AI_STRONG_RATELIMITER_MAX_HITS = 1
AI_STRONG_RATELIMITER_PERIOD = 2
UD_RATELIMITER_MAX_HITS = 10
UD_RATELIMITER_PERIOD = 5

"""
General group constants
"""

DEFAULT_GROUP = 1  # the enum in group type, which is gag training

"""
Container classes for groups
"""


class GroupDefinition:
    """
    Small container class, hosting all of the
    definitions which makes up a group.
    """
    def __init__(self, maxSize, options=None, zoneId=None,
                 entrance=None, elevatorClasses=None, requireVisited=False,
                 taskRequired=None, suitId=None, forceZoneConstant=False, allowFullHood=False,
                 suitName=None, minLaffRec=None, minGagRec=None, holidayList=None):
        if zoneId is None:
            zoneId = []
        self.options = options                      # The options associated with this group.
        self.maxSize = maxSize                      # The maximum capacity of this group.
        self.zoneId = zoneId                        # The zone ids assoacited with this group.
        self.elevatorClasses = elevatorClasses      # Any existing elevator objects to teleport Toons to.
        self.entrance = entrance                    # What is the entrance associated with this? (Used to differentiate between elevators.)
        self.requireVisited = requireVisited        # Should the Toon have visited the hoodId to join the group?
        self.taskRequired = taskRequired            # What tasks must the Toon have to join the group?
        self.suitId = suitId                        # What is the suitId associated with this group?
        self.forceZoneConstant = forceZoneConstant  # Upon owner changing zone, disband if they leave the zone they created the group in?
        self.allowFullHood = allowFullHood          # If a playground zone Id, allows the group to stay afloat across the entire hood
        self.groupType = None                       # Reference to groupType
        self.suitName = suitName                    # If the group hinges on a certain suit type in battle being present
        self.minLaffRec = minLaffRec                # The number of *recommended* minimum max laff for this group
        self.minGagRec = minGagRec                  # The number of *recommended* minimum max gag tracks for this group
        self.holidayList = holidayList or []        # Optional, sets required holidays for group type to be available

        # Make sure maxSize is in list format.
        if type(self.maxSize) is not list and type(self.maxSize) is not tuple:
            self.maxSize = (self.maxSize,)

    def getOptions(self):
        if type(self.options) in (tuple, list):
            return self.options
        return self.options,

    def getElevator(self):
        return self.elevatorClasses

    @property
    def defaultMaxSize(self) -> int:
        return self.maxSize[-1]

    @property
    def defaultOptions(self) -> list:
        opts = self.getOptions()
        if opts is None or None in opts:
            return []
        return [opt.default for opt in opts]

    @property
    def isGroupAvailable(self) -> bool:
        if not self.holidayList:
            # Return true if no required holiday is defined
            return True

        if ProcessGlobals.getCurrentProcess() == ProcessGlobals.Process.Client:
            # Client. We need to check news manager for existing holidays
            if not base.cr.newsManager:
                # We require a holiday, but have no news manager. return False.
                return False
            return any([base.cr.newsManager.isHolidayRunning(holiday) for holiday in self.holidayList])
        else:
            # Server. We need to check holiday manager for existing holidays
            return any([simbase.air.holidayManager.isHolidayRunning(holiday) for holiday in self.holidayList])


class GroupOptions:
    """
    Small container class used for holding the
    specific options for a boarding group.
    """
    def __init__(self, label, *options):
        self.label = label
        self.options = options

    @property
    def default(self):
        """Returns the default options for this group."""
        return self.options[-1]

    @property
    def optionCount(self):
        return len(self.options)


class GroupElevator:
    """
    Small container class holding the information
    about the elevator classes of a given group.
    """
    def __init__(self, warpable, elevatorClass, elevatorClassAI):
        self.warpable = warpable
        self.elevatorClass = elevatorClass
        self.elevatorClassAI = elevatorClassAI


"""
Zone IDs for groups
"""

pgs = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 9000]
StreetFishZones = [
    1129, 1236, 1330, 1410,
    2156, 2236, 2341, 2418,
    3136, 3236, 3329, 3427,
    4148, 4240, 4345, 4411,
    5139, 5245, 5318, 5415,
    9153, 9255, 9339,
]
AllFishZones = StreetFishZones + pgs

"""
Building definitions
"""

BuildingZones = []
for aRange in [range(x + 100, x + 499) for x in pgs]:
    BuildingZones.extend(aRange)


def makeBuildingGroupDef(floors: list, forceType: GroupType = None):
    """Creates a building group definition"""
    groupDef = GroupDefinition(
        maxSize=4,
        options=[
            GroupOptions(
                'Playing', Options.REGULAR, Options.LENGTH_TRAINING
            ),
            GroupOptions(
                'Floors', *floors
            ),
        ],
        zoneId=BuildingZones,
        requireVisited=True,
        elevatorClasses=GroupElevator(  # without this key, warping is implied to not be a thing for this group type
            False,  # you cannot warp to this elevator,
            'DistributedElevatorExt',     # string name for client elevator class,
            'DistributedElevatorExtAI',     # string name for AI elevator class
        )
    )
    if forceType:
        groupDef.groupType = forceType
    return groupDef


def getBuildingGroupDef():
    return makeBuildingGroupDef(
        floors=[Options.ONE, Options.TWO, Options.THREE, Options.FOUR, Options.FIVE, Options.SIX])


"""
All Boarding Group Information
"""

BoardingGroupInformation = {
    # region General
    GroupType.BuildingSell: getBuildingGroupDef(),
    GroupType.BuildingCash: getBuildingGroupDef(),
    GroupType.BuildingLaw: getBuildingGroupDef(),
    GroupType.BuildingBoss: getBuildingGroupDef(),
    GroupType.BuildingBoard: getBuildingGroupDef(),
    # endregion
    # region Activities
    GroupType.Fishing: GroupDefinition(
        maxSize=4,
        requireVisited=True,
        zoneId=AllFishZones,
        forceZoneConstant=True,
    ),
    GroupType.Golfing: GroupDefinition(
        options=GroupOptions(
            'Difficulty',
            Options.EASY, Options.MEDIUM, Options.HARD,
        ),
        maxSize=4,
        elevatorClasses=GroupElevator(
            False,
            'DistributedGolfKart',
            'DistributedGolfKartAI',
        ),
        zoneId=[GolfZone],
    ),
    GroupType.Checkers: GroupDefinition(
        options=GroupOptions(
            'Difficulty',
            Options.CASUAL, Options.COMPETITIVE,
        ),
        maxSize=6,
        elevatorClasses=GroupElevator(
            False,
            'DistributedPicnicGameTable',
            'DistributedPicnicGameTableAI',
        ),
        zoneId=[GolfZone],
    ),
    GroupType.Chess: GroupDefinition(
        options=GroupOptions(
            'Difficulty',
            Options.CASUAL, Options.COMPETITIVE,
        ),
        maxSize=6,
        elevatorClasses=GroupElevator(
            False,
            'DistributedPicnicGameTable',
            'DistributedPicnicGameTableAI',
        ),
        zoneId=[GolfZone],
    ),
    GroupType.TOONO: GroupDefinition(
        options=GroupOptions(
            'Difficulty',
            Options.CASUAL, Options.COMPETITIVE,
        ),
        maxSize=[2, 4, 6],
        elevatorClasses=GroupElevator(
            False,
            'DistributedPicnicGameTable',
            'DistributedPicnicGameTableAI',
        ),
        zoneId=[GolfZone],
    ),
    GroupType.Trolley: GroupDefinition(
        options=GroupOptions(
            'Game Mode',
            Options.CASUAL,  # Options.TRACKS,
        ),
        maxSize=4,
        elevatorClasses=GroupElevator(
            False,
            'DistributedTrolley',
            'DistributedTrolleyAI',
        ),
        zoneId=pgs,
    ),
    GroupType.Racing: GroupDefinition(
        options=GroupOptions(
            'Difficulty',
            Options.CASUAL, Options.COMPETITIVE,
        ),
        maxSize=(4, 6, 8),
        elevatorClasses=GroupElevator(
            False,
            'DistributedStartingBlock',
            'DistributedStartingBlockAI',
        ),
        zoneId=[GoofySpeedway],
    ),
    # endregion
    # region Bosses
    GroupType.VP: GroupDefinition(
        maxSize=(2, 4, 6, 8),
        suitId=4,
        elevatorClasses=GroupElevator(
            True,
            'DistributedVPElevator',
            'DistributedVPElevatorAI',
        ),
        zoneId=[SellbotHQ, SellbotLobby],
    ),
    GroupType.CFO: GroupDefinition(
        maxSize=(2, 4, 6, 8),
        suitId=3,
        elevatorClasses=GroupElevator(
            True,
            'DistributedCFOElevator',
            'DistributedCFOElevatorAI',
        ),
        zoneId=[CashbotHQ, CashbotLobby],
    ),
    GroupType.CLO: GroupDefinition(
        maxSize=(2, 4, 6, 8),
        suitId=2,
        elevatorClasses=GroupElevator(
            True,
            'DistributedCLOElevator',
            'DistributedCLOElevatorAI',
        ),
        zoneId=[LawbotHQ, LawbotLobby],
    ),
    GroupType.OCLO: GroupDefinition(
        maxSize=(4, 8),
        suitId=2,
        elevatorClasses=GroupElevator(
            True,
            'DistributedHardmodeCLOElevator',
            'DistributedHardmodeCLOElevatorAI',
        ),
        zoneId=[LawbotHQ, LawbotLobby, LawbotLounge],
    ),
    GroupType.CEO: GroupDefinition(
        maxSize=(2, 4, 6, 8),
        suitId=1,
        elevatorClasses=GroupElevator(
            True,
            'DistributedCEOElevator',
            'DistributedCEOElevatorAI',
        ),
        zoneId=[BossbotHQ, BossbotLobby],
    ),
    # todo note: boardbot will have suit requirement of 0
    # endregion
    # region Facilities
    GroupType.FrontFactory: GroupDefinition(
        options=GroupOptions(
            'Length',
            Options.REGULAR, Options.LENGTH_SHORT, Options.LENGTH_LONG, Options.LENGTH_TRAINING,
        ),
        entrance=Entrances.FrontFactory,
        maxSize=4,
        requireVisited=True,
        elevatorClasses=GroupElevator(
            True,
            'DistributedFactoryElevatorExt',
            'DistributedFactoryElevatorExtAI',
        ),
        suitId=4,
        zoneId=[SellbotHQ, SellbotFactoryExt],
    ),
    GroupType.SideFactory: GroupDefinition(
        options=GroupOptions(
            'Length',
            Options.REGULAR, Options.LENGTH_SHORT, Options.LENGTH_LONG, Options.LENGTH_TRAINING,
        ),
        entrance=Entrances.SideFactory,
        maxSize=4,
        requireVisited=True,
        elevatorClasses=GroupElevator(
            True,
            'DistributedFactoryElevatorExt',
            'DistributedFactoryElevatorExtAI',
        ),
        suitId=4,
        zoneId=[SellbotHQ, SellbotFactoryExt],
    ),
    GroupType.CoinMint: GroupDefinition(
        options=GroupOptions(
            'Length',
            Options.REGULAR, Options.LENGTH_MINIMAL, Options.LENGTH_FULL, Options.LENGTH_TRAINING,
        ),
        entrance=Entrances.CoinMint,
        maxSize=4,
        requireVisited=True,
        elevatorClasses=GroupElevator(
            True,
            'DistributedMintElevatorExt',
            'DistributedMintElevatorExtAI',
        ),
        suitId=3,
        zoneId=[CashbotHQ],
    ),
    GroupType.DollarMint: GroupDefinition(
        options=GroupOptions(
            'Length',
            Options.REGULAR, Options.LENGTH_MINIMAL, Options.LENGTH_FULL, Options.LENGTH_TRAINING,
        ),
        entrance=Entrances.DollarMint,
        maxSize=4,
        requireVisited=True,
        elevatorClasses=GroupElevator(
            True,
            'DistributedMintElevatorExt',
            'DistributedMintElevatorExtAI',
        ),
        suitId=3,
        zoneId=[CashbotHQ],
    ),
    GroupType.BullionMint: GroupDefinition(
        options=GroupOptions(
            'Length',
            Options.REGULAR, Options.LENGTH_MINIMAL, Options.LENGTH_FULL, Options.LENGTH_TRAINING,
        ),
        entrance=Entrances.BullionMint,
        maxSize=4,
        requireVisited=True,
        elevatorClasses=GroupElevator(
            True,
            'DistributedMintElevatorExt',
            'DistributedMintElevatorExtAI',
        ),
        suitId=3,
        zoneId=[CashbotHQ],
    ),
    GroupType.LawficeA: GroupDefinition(
        options=GroupOptions(
            'Length',
            Options.REGULAR, Options.LENGTH_MINIMAL, Options.LENGTH_FULL, Options.LENGTH_TRAINING,
        ),
        entrance=Entrances.LawficeA,
        maxSize=4,
        requireVisited=True,
        elevatorClasses=GroupElevator(
            True,
            'DistributedLawOfficeElevatorExt',
            'DistributedLawOfficeElevatorExtAI',
        ),
        suitId=2,
        zoneId=[LawbotHQ, LawbotOfficeExt],
    ),
    GroupType.LawficeB: GroupDefinition(
        options=GroupOptions(
            'Length',
            Options.REGULAR, Options.LENGTH_MINIMAL, Options.LENGTH_FULL, Options.LENGTH_TRAINING,
        ),
        entrance=Entrances.LawficeB,
        maxSize=4,
        requireVisited=True,
        elevatorClasses=GroupElevator(
            True,
            'DistributedLawOfficeElevatorExt',
            'DistributedLawOfficeElevatorExtAI',
        ),
        suitId=2,
        zoneId=[LawbotHQ, LawbotOfficeExt],
    ),
    GroupType.LawficeC: GroupDefinition(
        options=GroupOptions(
            'Length',
            Options.REGULAR, Options.LENGTH_MINIMAL, Options.LENGTH_FULL, Options.LENGTH_TRAINING,
        ),
        entrance=Entrances.LawficeC,
        maxSize=4,
        requireVisited=True,
        elevatorClasses=GroupElevator(
            True,
            'DistributedLawOfficeElevatorExt',
            'DistributedLawOfficeElevatorExtAI',
        ),
        suitId=2,
        zoneId=[LawbotHQ, LawbotOfficeExt],
    ),
    GroupType.SilverSprocket: GroupDefinition(
        options=GroupOptions(
            'Length',
            Options.REGULAR, Options.LENGTH_MINIMAL, Options.LENGTH_FULL, Options.LENGTH_TRAINING,
        ),
        entrance=Entrances.FrontThree,
        maxSize=4,
        requireVisited=True,
        elevatorClasses=GroupElevator(
            True,
            'DistributedCogKart',
            'DistributedCogKartAI',
        ),
        suitId=1,
        zoneId=[BossbotHQ],
    ),
    GroupType.GoldenGear: GroupDefinition(
        options=GroupOptions(
            'Length',
            Options.REGULAR, Options.LENGTH_MINIMAL, Options.LENGTH_FULL, Options.LENGTH_TRAINING,
        ),
        entrance=Entrances.MiddleSix,
        maxSize=4,
        requireVisited=True,
        elevatorClasses=GroupElevator(
            True,
            'DistributedCogKart',
            'DistributedCogKartAI',
        ),
        suitId=1,
        zoneId=[BossbotHQ],
    ),
    GroupType.DiamondDynamo: GroupDefinition(
        options=GroupOptions(
            'Length',
            Options.REGULAR, Options.LENGTH_MINIMAL, Options.LENGTH_FULL, Options.LENGTH_TRAINING,
        ),
        entrance=Entrances.BackNine,
        maxSize=4,
        requireVisited=True,
        elevatorClasses=GroupElevator(
            True,
            'DistributedCogKart',
            'DistributedCogKartAI',
        ),
        suitId=1,
        zoneId=[BossbotHQ],
    ),
    # endregion
    # region Minibosses
    GroupType.DM: GroupDefinition(
        taskRequired=QuestId(QuestSource.MainQuest, 11, 7),
        maxSize=4,
        elevatorClasses=GroupElevator(
            False,
            'DistributedDerrickManElevator',
            'DistributedDerrickManElevatorAI',
        ),
        zoneId=[DerrickManLobby],
    ),
    GroupType.DOLA: GroupDefinition(
        taskRequired=QuestId(QuestSource.MainQuest, 21, 14),
        maxSize=4,
        elevatorClasses=GroupElevator(
            False,
            'DistributedLandAcquisitionElevator',
            'DistributedLandAcquisitionElevatorAI',
        ),
        zoneId=[DOLAExtZone],
    ),
    GroupType.DOPR: GroupDefinition(
        taskRequired=QuestId(QuestSource.MainQuest, 30, 9),
        maxSize=4,
        elevatorClasses=GroupElevator(
            False,
            'DistributedDungeonSigilvator',
            'DistributedDungeonSigilvatorAI',
        ),
        zoneId=[OldeToontownDungeon],
    ),
    GroupType.DOPA: GroupDefinition(
        taskRequired=QuestId(QuestSource.MainQuest, 74, 9),
        maxSize=4,
        elevatorClasses=GroupElevator(
            False,
            'DistributedDirectorsElevator',
            'DistributedDirectorsElevatorAI',
        ),
        zoneId=[BossbotHQ, BossbotLobby],
    ),
    # endregion
    # region Street Mercs
    GroupType.DuckShuffler: GroupDefinition(
        maxSize=4,
        requireVisited=True,
        allowFullHood=True,
        zoneId=[ToontownCentral],
        suitName='duckshfl',
    ),
    GroupType.DeepDiver: GroupDefinition(
        maxSize=4,
        requireVisited=True,
        allowFullHood=True,
        zoneId=[DonaldsDock],
        suitName='ddiver',
    ),
    GroupType.Gatekeeper: GroupDefinition(
        maxSize=4,
        requireVisited=True,
        allowFullHood=True,
        zoneId=[OldeToontown],
        suitName='gatekeep',
    ),
    GroupType.Bellringer: GroupDefinition(
        maxSize=4,
        requireVisited=True,
        allowFullHood=True,
        zoneId=[DaisyGardens],
        suitName='bellring',
    ),
    GroupType.Mouthpiece: GroupDefinition(
        maxSize=4,
        requireVisited=True,
        allowFullHood=True,
        zoneId=[MinniesMelodyland],
        suitName='mouthp',
    ),
    GroupType.Firestarter: GroupDefinition(
        maxSize=4,
        requireVisited=True,
        allowFullHood=True,
        zoneId=[TheBrrrgh],
        suitName='fires',
    ),
    GroupType.Treekiller: GroupDefinition(
        maxSize=4,
        requireVisited=True,
        allowFullHood=True,
        zoneId=[OutdoorZone],
        suitName='treek',
    ),
    GroupType.Featherbedder: GroupDefinition(
        maxSize=4,
        requireVisited=True,
        allowFullHood=True,
        zoneId=[DonaldsDreamland],
        suitName='fbed',
    ),
    # endregion
    # region Instance Mercs
    GroupType.Prethinker: GroupDefinition(
        taskRequired=MercDefinitions[MERC_PRETHINKER].requiredTaskID,
        maxSize=4,
        elevatorClasses=GroupElevator(
            False,
            'DistributedPrethinkerSigilvator',
            'DistributedPrethinkerSigilvatorAI',
        ),
        zoneId=[MercDefinitions[MERC_PRETHINKER].zoneId],
    ),
    GroupType.Rainmaker: GroupDefinition(
        taskRequired=MercDefinitions[MERC_RAINMAKER].requiredTaskID,
        maxSize=4,
        elevatorClasses=GroupElevator(
            False,
            'DistributedRainmakerSigilvator',
            'DistributedRainmakerSigilvatorAI',
        ),
        # This specific zone is stupid and is the one that Toons exit the lighthouse from
        zoneId=[MercDefinitions[MERC_RAINMAKER].zoneId, 1316],
    ),
    GroupType.Witchhunter: GroupDefinition(
        taskRequired=MercDefinitions[MERC_WITCHHUNTER].requiredTaskID,
        maxSize=4,
        elevatorClasses=GroupElevator(
            False,
            'DistributedWitchHunterSigilvator',
            'DistributedWitchHunterSigilvatorAI',
        ),
        zoneId=[MercDefinitions[MERC_WITCHHUNTER].zoneId],
    ),
    GroupType.Multislacker: GroupDefinition(
        taskRequired=MercDefinitions[MERC_MULTISLACKER].requiredTaskID,
        maxSize=4,
        elevatorClasses=GroupElevator(
            False,
            'DistributedMultislackerSigilvator',
            'DistributedMultislackerSigilvatorAI',
        ),
        zoneId=[MercDefinitions[MERC_MULTISLACKER].zoneId],
    ),
    GroupType.Majorplayer: GroupDefinition(
        taskRequired=MercDefinitions[MERC_MAJORPLAYER].requiredTaskID,
        maxSize=4,
        elevatorClasses=GroupElevator(
            False,
            'DistributedInstanceMercElevator',
            'DistributedInstanceMercElevatorAI',
        ),
        zoneId=[MercDefinitions[MERC_MAJORPLAYER].zoneId],
    ),
    GroupType.Plutocrat: GroupDefinition(
        taskRequired=MercDefinitions[MERC_PLUTOCRAT].requiredTaskID,
        maxSize=4,
        elevatorClasses=GroupElevator(
            False,
            'DistributedPlutocratSigilvator',
            'DistributedPlutocratSigilvatorAI',
        ),
        zoneId=[MercDefinitions[MERC_PLUTOCRAT].zoneId],
    ),
    GroupType.Chainsaw: GroupDefinition(
        taskRequired=MercDefinitions[MERC_CHAINSAW].requiredTaskID,
        maxSize=4,
        elevatorClasses=GroupElevator(
            False,
            'DistributedChainsawSigilvator',
            'DistributedChainsawSigilvatorAI',
        ),
        zoneId=[MercDefinitions[MERC_CHAINSAW].zoneId],
    ),
    GroupType.Pacesetter: GroupDefinition(
        taskRequired=MercDefinitions[MERC_PACESETTER].requiredTaskID,
        maxSize=4,
        elevatorClasses=GroupElevator(
            False,
            'DistributedInstanceMercElevator',
            'DistributedInstanceMercElevatorAI',
        ),
        zoneId=[MercDefinitions[MERC_PACESETTER].zoneId],
    ),

    # region Events
    GroupType.Highroller: GroupDefinition(
        taskRequired=None,
        maxSize=4,
        elevatorClasses=GroupElevator(
            False,
            'DistributedHighRollerSigilvator',
            'DistributedHighRollerSigilvatorAI',
        ),
        zoneId=[MercDefinitions[MERC_HIGHROLLER].zoneId],
        holidayList=[APRIL_FOOLS],
    ),
    GroupType.FindTheFamily: GroupDefinition(
        options=GroupOptions(
            'Length',
            Options.REGULAR, Options.LENGTH_SHORT, Options.LENGTH_LONG,
        ),
        entrance=Entrances.FindTheForeman,
        maxSize=4,
        requireVisited=True,
        elevatorClasses=GroupElevator(
            True,
            'DistributedFactoryForemanSigilvator',
            'DistributedFactoryForemanSigilvatorAI',
        ),
        suitId=4,
        zoneId=[SellbotHQ, SellbotFactoryExt],
        holidayList=[APRIL_FOOLS],
    ),
    GroupType.OverclockedFindTheFamily: GroupDefinition(
        options=GroupOptions(
            'Instability',
            Options.REGULAR, Options.HIGHLY_UNSTABLE,
        ),
        entrance=Entrances.OverclockedFindTheFamily,
        maxSize=4,
        requireVisited=True,
        elevatorClasses=GroupElevator(
            True,
            'DistributedFactoryForemanSigilvator',
            'DistributedFactoryForemanSigilvatorAI',
        ),
        suitId=4,
        zoneId=[SellbotHQ, SellbotFactoryExt],
        minLaffRec=115,
        minGagRec=5,
        holidayList=[APRIL_FOOLS],
    ),
    GroupType.COO: GroupDefinition(
        maxSize=(2, 3, 4, 5, 6, 7, 8),
        elevatorClasses=GroupElevator(
            False,  # crashes if you warp!! not really a big deal anyway
            'DistributedCMElevator',
            'DistributedCMElevatorAI',
        ),
        zoneId=[BoardbotHQ],
        holidayList=[APRIL_FOOLS],
    ),
    # endregion
    # endregion
    # region Misc
    GroupType.Pizzeria: GroupDefinition(
        options=GroupOptions(
            'Setting',
            Options.SOCIAL_HANGOUT, Options.SOCIAL_PARTY, Options.SOCIAL_ROLEPLAY,
        ),
        maxSize=99, zoneId=[Pizzeria],
        requireVisited=True, forceZoneConstant=True,
    )
    # endregion
}


BossGroupTypes = [GroupType.VP, GroupType.CFO, GroupType.CLO, GroupType.OCLO, GroupType.CEO]
BossGroupToCourtyard = {
    GroupType.VP: SellbotHQ,
    GroupType.CFO: CashbotHQ,
    GroupType.CLO: LawbotHQ,
    GroupType.OCLO: LawbotHQ,
    GroupType.CEO: BossbotHQ,
}
FacilityGroupTypes = [
    GroupType.FrontFactory, GroupType.SideFactory, GroupType.FindTheFamily, GroupType.OverclockedFindTheFamily,
    GroupType.CoinMint, GroupType.DollarMint, GroupType.BullionMint,
    GroupType.LawficeA, GroupType.LawficeB, GroupType.LawficeC,
    GroupType.SilverSprocket, GroupType.GoldenGear, GroupType.DiamondDynamo
]
FacilityGroupToEntranceZone = {}
FacilityGroupToEntranceZone.update({groupType: SellbotFactoryExt for groupType in [GroupType.FrontFactory, GroupType.SideFactory, GroupType.FindTheFamily, GroupType.OverclockedFindTheFamily]})
FacilityGroupToEntranceZone.update({groupType: CashbotHQ for groupType in [GroupType.CoinMint, GroupType.DollarMint, GroupType.BullionMint]})
FacilityGroupToEntranceZone.update({groupType: LawbotOfficeExt for groupType in [GroupType.LawficeA, GroupType.LawficeB, GroupType.LawficeC]})
FacilityGroupToEntranceZone.update({groupType: BossbotHQ for groupType in [GroupType.SilverSprocket, GroupType.GoldenGear, GroupType.DiamondDynamo]})
KartGroupTypes = [GroupType.SilverSprocket, GroupType.GoldenGear, GroupType.DiamondDynamo]

BossDoorTeleportPos = {
    SellbotHQ: (-37.75, -44.5, 10.096, -60),
    CashbotHQ: (121.75, 543.5, 32.246, 0),
    LawbotHQ: (0, 220, 19.5, 0),
    BossbotHQ: (63, 234.5, 0.275, 0),
    BoardbotHQ: (0, 0, 0),
}


for groupType, groupDef in BoardingGroupInformation.items():
    groupDef.groupType = groupType


def getGroupDef(typeEnum: GroupType) -> GroupDefinition:
    """
    Returns a GroupDefinition from BoardingGroupInformation.
    """
    if typeEnum not in BoardingGroupInformation:
        raise Exception("typeEnum not registered in BoardingGroupInformation!")
    return BoardingGroupInformation.get(typeEnum)


GroupTypeLocalizer = {
    # Translates each GroupType into what it is.
    GroupType.VP: TTLocalizer.PrintVP,
    GroupType.CFO: TTLocalizer.PrintCFO,
    GroupType.CLO: TTLocalizer.PrintCLO,
    GroupType.OCLO: TTLocalizer.PrintHMCLO,
    GroupType.CEO: TTLocalizer.PrintCEO,
    GroupType.FrontFactory: TTLocalizer.FrontFactory,
    GroupType.SideFactory: TTLocalizer.SideFactory,
    GroupType.CoinMint: TTLocalizer.ElevatorCashBotMint0,
    GroupType.DollarMint: TTLocalizer.ElevatorCashBotMint1,
    GroupType.BullionMint: TTLocalizer.ElevatorCashBotMint2,
    GroupType.LawficeA: TTLocalizer.FactoryNames[12500],
    GroupType.LawficeB: TTLocalizer.FactoryNames[12600],
    GroupType.LawficeC: TTLocalizer.FactoryNames[12700],
    GroupType.SilverSprocket: TTLocalizer.ElevatorBossBotCourse0,
    GroupType.GoldenGear: TTLocalizer.ElevatorBossBotCourse1,
    GroupType.DiamondDynamo: TTLocalizer.ElevatorBossBotCourse2,
    GroupType.DM: TTLocalizer.suitName('derrman'),
    GroupType.DOLA: TTLocalizer.suitName('dlao'),
    GroupType.DOPR: 'The Dungeon',
    GroupType.DOPA: 'The Directors',
    GroupType.Racing: TTLocalizer.KartPageAltTitle,
    GroupType.Golfing: TTLocalizer.GolfPageAltTitle,
    GroupType.Trolley: TTLocalizer.TrolleyName,
    GroupType.Checkers: TTLocalizer.PGTGameNames[0],
    GroupType.Chess: TTLocalizer.PGTGameNames[1],
    GroupType.TOONO: TTLocalizer.PGTGameNames[2],
    GroupType.BuildingSell: TTLocalizer.DepartmentBuilding % ('%s', TTLocalizer.Sellbot),
    GroupType.BuildingCash: TTLocalizer.DepartmentBuilding % ('%s', TTLocalizer.Cashbot),
    GroupType.BuildingLaw: TTLocalizer.DepartmentBuilding % ('%s', TTLocalizer.Lawbot),
    GroupType.BuildingBoss: TTLocalizer.DepartmentBuilding % ('%s', TTLocalizer.Bossbot),
    GroupType.BuildingBoard: TTLocalizer.DepartmentBuilding % ('%s', TTLocalizer.Boardbot),
    GroupType.Fishing: TTLocalizer.GroupFishing,
    GroupType.DuckShuffler: TTLocalizer.suitName('duckshfl'),
    GroupType.DeepDiver: TTLocalizer.suitName('ddiver'),
    GroupType.Gatekeeper: TTLocalizer.suitName('gatekeep'),
    GroupType.Bellringer: TTLocalizer.suitName('bellring'),
    GroupType.Mouthpiece: TTLocalizer.suitName('mouthp'),
    GroupType.Firestarter: TTLocalizer.suitName('fires'),
    GroupType.Treekiller: TTLocalizer.suitName('treek'),
    GroupType.Featherbedder: TTLocalizer.suitName('fbed'),
    GroupType.Prethinker: TTLocalizer.MercSuffix % TTLocalizer.suitName('prethink'),
    GroupType.Rainmaker: TTLocalizer.MercSuffix % TTLocalizer.suitName('rainmake'),
    GroupType.Witchhunter: TTLocalizer.MercSuffix % TTLocalizer.suitName('whunter'),
    GroupType.Multislacker: TTLocalizer.MercSuffix % TTLocalizer.suitName('mslacker'),
    GroupType.Majorplayer: TTLocalizer.MercSuffix % TTLocalizer.suitName('mplayer'),
    GroupType.Plutocrat: TTLocalizer.MercSuffix % TTLocalizer.suitName('pcrat'),
    GroupType.Chainsaw: TTLocalizer.MercSuffix % TTLocalizer.suitName('chainsaw'),
    GroupType.Pacesetter: TTLocalizer.MercSuffix % TTLocalizer.suitName('psetter'),
    GroupType.FindTheFamily: TTLocalizer.FindTheForemanSubtitle,
    GroupType.OverclockedFindTheFamily: TTLocalizer.ElevatorSellBotFactory4,
    GroupType.COO: TTLocalizer.PrintCOO,
    GroupType.Highroller: TTLocalizer.suitName('hroller'),
    GroupType.Pizzeria: 'Pizzeria',
}


BGLocalizer = {
    # region Localizer dict for GroupTypes.
    GroupType.VP: {
        GroupType.BASE: f"%s{TTLocalizer.PrintVP}",
        Options.ANY_TIER: '',
        Options.TIER_ONE: 'Tier 1 ',
        Options.TIER_TWO: 'Tier 2 ',
        Options.TIER_THREE: 'Tier 3 ',
    },
    GroupType.CFO: {
        GroupType.BASE: f"%s{TTLocalizer.PrintCFO}",
        Options.ANY_TIER: '',
        Options.TIER_ONE: 'Tier 1 ',
        Options.TIER_TWO: 'Tier 2 ',
        Options.TIER_THREE: 'Tier 3 ',
    },
    GroupType.CLO: {
        GroupType.BASE: f"%s{TTLocalizer.PrintCLO}",
        Options.ANY_TIER: '',
        Options.TIER_ONE: 'Tier 1 ',
        Options.TIER_TWO: 'Tier 2 ',
        Options.TIER_THREE: 'Tier 3 ',
    },
    GroupType.OCLO: TTLocalizer.PrintHMCLO,
    GroupType.CEO: {
        GroupType.BASE: f"%s{TTLocalizer.PrintCEO}",
        Options.ANY_TIER: '',
        Options.TIER_ONE: 'Tier 1 ',
        Options.TIER_TWO: 'Tier 2 ',
        Options.TIER_THREE: 'Tier 3 ',
    },
    GroupType.FrontFactory: {
        GroupType.BASE: f"%sSellbot Factory",
        Options.REGULAR: '',
        Options.LENGTH_SHORT: 'Short ',
        Options.LENGTH_LONG: 'Full ',
        Options.LENGTH_TRAINING: 'Training ',
    },
    GroupType.SideFactory: {
        GroupType.BASE: f"%sSide Factory",
        Options.REGULAR: '',
        Options.LENGTH_SHORT: 'Short ',
        Options.LENGTH_LONG: 'Full ',
        Options.LENGTH_TRAINING: 'Training ',
    },
    GroupType.CoinMint: {
        GroupType.BASE: f"%sCoin Mint",
        Options.REGULAR: '',
        Options.LENGTH_MINIMAL: 'Short ',
        Options.LENGTH_FULL: 'Full ',
        Options.LENGTH_TRAINING: 'Training ',
    },
    GroupType.DollarMint: {
        GroupType.BASE: f"%sDollar Mint",
        Options.REGULAR: '',
        Options.LENGTH_MINIMAL: 'Short ',
        Options.LENGTH_FULL: 'Full ',
        Options.LENGTH_TRAINING: 'Training ',
    },
    GroupType.BullionMint: {
        GroupType.BASE: f"%sBullion Mint",
        Options.REGULAR: '',
        Options.LENGTH_MINIMAL: 'Short ',
        Options.LENGTH_FULL: 'Full ',
        Options.LENGTH_TRAINING: 'Training ',
    },
    GroupType.LawficeA: {
        GroupType.BASE: f"%s{TTLocalizer.FactoryNames[12500]}",
        Options.REGULAR: '',
        Options.LENGTH_MINIMAL: 'Short ',
        Options.LENGTH_FULL: 'Full ',
        Options.LENGTH_TRAINING: 'Training ',
    },
    GroupType.LawficeB: {
        GroupType.BASE: f"%s{TTLocalizer.FactoryNames[12600]}",
        Options.REGULAR: '',
        Options.LENGTH_MINIMAL: 'Short ',
        Options.LENGTH_FULL: 'Full ',
        Options.LENGTH_TRAINING: 'Training ',
    },
    GroupType.LawficeC: {
        GroupType.BASE: f"%s{TTLocalizer.FactoryNames[12700]}",
        Options.REGULAR: '',
        Options.LENGTH_MINIMAL: 'Short ',
        Options.LENGTH_FULL: 'Full ',
        Options.LENGTH_TRAINING: 'Training ',
    },
    GroupType.SilverSprocket: {
        GroupType.BASE: f"%sSilver Sprocket Course",
        Options.LENGTH_MINIMAL: 'Short ',
        Options.LENGTH_FULL: 'Full ',
        Options.LENGTH_TRAINING: 'Training ',
    },
    GroupType.GoldenGear: {
        GroupType.BASE: f"%sGolden Gear Course",
        Options.LENGTH_MINIMAL: 'Short ',
        Options.LENGTH_FULL: 'Full ',
        Options.LENGTH_TRAINING: 'Training ',
    },
    GroupType.DiamondDynamo: {
        GroupType.BASE: f"%sDiamond Dynamo Course",
        Options.LENGTH_MINIMAL: 'Short ',
        Options.LENGTH_FULL: 'Full ',
        Options.LENGTH_TRAINING: 'Training ',
    },
    GroupType.DM: TTLocalizer.suitName('derrman'),
    GroupType.DOLA: TTLocalizer.suitName('dlao'),
    GroupType.DOPR: 'The Dungeon',
    GroupType.DOPA: 'The Directors',
    GroupType.Racing: {
        GroupType.BASE: f"%sRacing",
        Options.CASUAL: '',
        Options.COMPETITIVE: 'Competitive ',
    },
    GroupType.Golfing: {
        GroupType.BASE: f"%s",
        Options.EASY: TTLocalizer.GolfCourseNames[0],
        Options.MEDIUM: TTLocalizer.GolfCourseNames[1],
        Options.HARD: TTLocalizer.GolfCourseNames[2],
    },
    GroupType.Trolley: {
        GroupType.BASE: f"%s",
        Options.CASUAL: 'Trolley Games',
        Options.TRACKS: 'Trolley Tracks',
    },
    GroupType.Checkers: {
        GroupType.BASE: f"%s{TTLocalizer.PGTGameNames[0]}",
        Options.CASUAL: '',
        Options.COMPETITIVE: 'Competitive ',
    },
    GroupType.Chess: {
        GroupType.BASE: f"%s{TTLocalizer.PGTGameNames[1]}",
        Options.CASUAL: '',
        Options.COMPETITIVE: 'Competitive ',
    },
    GroupType.TOONO: {
        GroupType.BASE: f"%s{TTLocalizer.PGTGameNames[2]}",
        Options.CASUAL: '',
        Options.COMPETITIVE: 'Competitive ',
    },
    GroupType.BuildingSell: {
        GroupType.BASE: TTLocalizer.GroupCogBuilding % ('%s', '%s', TTLocalizer.Sellbot),
        Options.REGULAR: '',
        Options.LENGTH_TRAINING: 'Training ',
        Options.ONE: '1',
        Options.TWO: '2',
        Options.THREE: '3',
        Options.FOUR: '4',
        Options.FIVE: '5',
        Options.SIX: '6',
    },
    GroupType.BuildingCash: {
        GroupType.BASE: TTLocalizer.GroupCogBuilding % ('%s', '%s', TTLocalizer.Cashbot),
        Options.REGULAR: '',
        Options.LENGTH_TRAINING: 'Training ',
        Options.ONE: '1',
        Options.TWO: '2',
        Options.THREE: '3',
        Options.FOUR: '4',
        Options.FIVE: '5',
        Options.SIX: '6',
    },
    GroupType.BuildingLaw: {
        GroupType.BASE: TTLocalizer.GroupCogBuilding % ('%s', '%s', TTLocalizer.Lawbot),
        Options.REGULAR: '',
        Options.LENGTH_TRAINING: 'Training ',
        Options.ONE: '1',
        Options.TWO: '2',
        Options.THREE: '3',
        Options.FOUR: '4',
        Options.FIVE: '5',
        Options.SIX: '6',
    },
    GroupType.BuildingBoss: {
        GroupType.BASE: TTLocalizer.GroupCogBuilding % ('%s', '%s', TTLocalizer.Bossbot),
        Options.REGULAR: '',
        Options.LENGTH_TRAINING: 'Training ',
        Options.ONE: '1',
        Options.TWO: '2',
        Options.THREE: '3',
        Options.FOUR: '4',
        Options.FIVE: '5',
        Options.SIX: '6',
    },
    GroupType.BuildingBoard: {
        GroupType.BASE: TTLocalizer.GroupCogBuilding % ('%s', '%s', TTLocalizer.Boardbot),
        Options.REGULAR: '',
        Options.LENGTH_TRAINING: 'Training ',
        Options.ONE: '1',
        Options.TWO: '2',
        Options.THREE: '3',
        Options.FOUR: '4',
        Options.FIVE: '5',
        Options.SIX: '6',
    },
    GroupType.Fishing: TTLocalizer.GroupFishing,
    GroupType.DuckShuffler: {
        GroupType.BASE: f"{TTLocalizer.suitName('duckshfl')}%s",
        Options.REGULAR: '',
        Options.DIFFICULT: ' (Difficult)',
        Options.OVERCLOCKED: ' (Overclocked)',
    },
    GroupType.DeepDiver: {
        GroupType.BASE: f"{TTLocalizer.suitName('ddiver')}%s",
        Options.REGULAR: '',
        Options.DIFFICULT: ' (Difficult)',
        Options.OVERCLOCKED: ' (Overclocked)',
    },
    GroupType.Gatekeeper: {
        GroupType.BASE: f"{TTLocalizer.suitName('gatekeep')}%s",
        Options.REGULAR: '',
        Options.DIFFICULT: ' (Difficult)',
        Options.OVERCLOCKED: ' (Overclocked)',
    },
    GroupType.Bellringer: {
        GroupType.BASE: f"{TTLocalizer.suitName('bellring')}%s",
        Options.REGULAR: '',
        Options.DIFFICULT: ' (Difficult)',
        Options.OVERCLOCKED: ' (Overclocked)',
    },
    GroupType.Mouthpiece: {
        GroupType.BASE: f"{TTLocalizer.suitName('mouthp')}%s",
        Options.REGULAR: '',
        Options.DIFFICULT: ' (Difficult)',
        Options.OVERCLOCKED: ' (Overclocked)',
    },
    GroupType.Firestarter: {
        GroupType.BASE: f"{TTLocalizer.suitName('fires')}%s",
        Options.REGULAR: '',
        Options.DIFFICULT: ' (Difficult)',
        Options.OVERCLOCKED: ' (Overclocked)',
    },
    GroupType.Treekiller: {
        GroupType.BASE: f"{TTLocalizer.suitName('treek')}%s",
        Options.REGULAR: '',
        Options.DIFFICULT: ' (Difficult)',
        Options.OVERCLOCKED: ' (Overclocked)',
    },
    GroupType.Featherbedder: {
        GroupType.BASE: f"{TTLocalizer.suitName('fbed')}%s",
        Options.REGULAR: '',
        Options.DIFFICULT: ' (Difficult)',
        Options.OVERCLOCKED: ' (Overclocked)',
    },
    GroupType.Prethinker: {
        GroupType.BASE: f"{TTLocalizer.suitName('prethink')}%s",
        Options.REGULAR: '',
        Options.DIFFICULT: ' (Difficult)',
        Options.OVERCLOCKED: ' (Overclocked)',
    },
    GroupType.Rainmaker: {
        GroupType.BASE: f"{TTLocalizer.suitName('rainmake')}%s",
        Options.REGULAR: '',
        Options.DIFFICULT: ' (Difficult)',
        Options.OVERCLOCKED: ' (Overclocked)',
    },
    GroupType.Witchhunter: {
        GroupType.BASE: f"{TTLocalizer.suitName('whunter')}%s",
        Options.REGULAR: '',
        Options.DIFFICULT: ' (Difficult)',
        Options.OVERCLOCKED: ' (Overclocked)',
    },
    GroupType.Multislacker: {
        GroupType.BASE: f"{TTLocalizer.suitName('mslacker')}%s",
        Options.REGULAR: '',
        Options.DIFFICULT: ' (Difficult)',
        Options.OVERCLOCKED: ' (Overclocked)',
    },
    GroupType.Majorplayer: {
        GroupType.BASE: f"{TTLocalizer.suitName('mplayer')}%s",
        Options.REGULAR: '',
        Options.DIFFICULT: ' (Difficult)',
        Options.OVERCLOCKED: ' (Overclocked)',
    },
    GroupType.Plutocrat: {
        GroupType.BASE: f"{TTLocalizer.suitName('pcrat')}%s",
        Options.REGULAR: '',
        Options.DIFFICULT: ' (Difficult)',
        Options.OVERCLOCKED: ' (Overclocked)',
    },
    GroupType.Chainsaw: {
        GroupType.BASE: f"{TTLocalizer.suitName('chainsaw')}%s",
        Options.REGULAR: '',
        Options.DIFFICULT: ' (Difficult)',
        Options.OVERCLOCKED: ' (Overclocked)',
    },
    GroupType.Pacesetter: {
        GroupType.BASE: f"{TTLocalizer.suitName('psetter')}%s",
        Options.REGULAR: '',
        Options.DIFFICULT: ' (Difficult)',
        Options.OVERCLOCKED: ' (Overclocked)',
    },
    GroupType.Highroller: {
        GroupType.BASE: f"{TTLocalizer.suitName('hroller')}%s",
        Options.REGULAR: '',
        Options.DIFFICULT: ' (Difficult)',
        Options.OVERCLOCKED: ' (Overclocked)',
    },
    GroupType.FindTheFamily: {
        GroupType.BASE: f"%sFind The Family",
        Options.REGULAR: '',
        Options.LENGTH_SHORT: 'Short ',
        Options.LENGTH_LONG: 'Full ',
    },
    GroupType.OverclockedFindTheFamily: {
        GroupType.BASE: f"%s{TTLocalizer.ElevatorSellBotFactory4}",
        Options.REGULAR: '',
        Options.HIGHLY_UNSTABLE: 'Highly Unstable '
    },
    GroupType.COO: TTLocalizer.PrintCOO,
    GroupType.Pizzeria: {
        GroupType.BASE: f'Pizzeria (%s)',
        Options.SOCIAL_HANGOUT: 'Hangout',
        Options.SOCIAL_PARTY: 'Party',
        Options.SOCIAL_ROLEPLAY: 'Roleplay',
    }
    # endregion
}
BGOptionsLocalizer = {
    # region Options names
    Options.REGULAR: 'Regular',
    Options.DIFFICULT: 'Difficult',
    Options.OVERCLOCKED: 'Overclocked',
    Options.CASUAL: 'Casual',
    Options.COMPETITIVE: 'Competitive',
    Options.TRACKS: 'Trolley Tracks',
    Options.ANY_TIER: 'Any Tier',
    Options.TIER_ONE: 'Tier 1',
    Options.TIER_TWO: 'Tier 2',
    Options.TIER_THREE: 'Tier 3',
    Options.LENGTH_MINIMAL: 'Minimal',
    Options.LENGTH_FULL: 'Full',
    Options.LENGTH_TRAINING: 'Training',
    Options.EASY: 'Easy',
    Options.MEDIUM: 'Medium',
    Options.HARD: 'Hard',
    Options.LENGTH_SHORT: 'Short',
    Options.LENGTH_LONG: 'Full',
    Options.ONE: '1',
    Options.TWO: '2',
    Options.THREE: '3',
    Options.FOUR: '4',
    Options.FIVE: '5',
    Options.SIX: '6',
    Options.SOCIAL_HANGOUT: 'Hangout',
    Options.SOCIAL_PARTY: 'Party',
    Options.SOCIAL_ROLEPLAY: 'Roleplay',
    # FTF
    Options.HIGHLY_UNSTABLE: '\1deepRed\1Highly Unstable\2'
    # endregion
}


def groupStruct2Name(group=None, groupCreation=None) -> str:
    """
    Turns a given Group into a name.
    """
    if groupCreation is None:
        if group is None:
            raise AttributeError("You gotta pick one buckaroo")
        groupCreation = group.groupCreation
    groupType = groupCreation.groupType
    opts = groupCreation.groupOptions

    # First, get the name of the group based on type.
    retstr = BGLocalizer.get(groupType, f'{groupType}')

    if type(retstr) is dict:
        # Populate this group with option data.
        retstr = retstr.copy()
        name = retstr.get(GroupType.BASE)
        optionNames = []
        optionsLeft = name.count('%s')
        for opt in opts:
            options = Options(opt)
            if options in retstr:
                optionNames.append(retstr.get(options))
                optionsLeft -= 1
                if optionsLeft <= 0:
                    break
        if optionsLeft > 0:
            optionNames.extend([''] * optionsLeft)
        retstr = name % tuple(optionNames)

    # We're done.
    return retstr


# A complete list of all of the zones that
# can have a group started in them.
GroupZones = {}  # key: zoneId, value: tuple(groupDefs)
FullHoodGroupZones = {}  # key: zoneId, value
for groupDef in BoardingGroupInformation.values():
    potentialZones = groupDef.zoneId
    for zoneId in potentialZones:
        if GroupZones.get(zoneId, None) is None:
            GroupZones[zoneId] = []
        GroupZones[zoneId].append(groupDef)
    if groupDef.allowFullHood:
        for zoneId in groupDef.zoneId:
            FullHoodGroupZones.setdefault(zoneId, [])
            FullHoodGroupZones[zoneId].append(groupDef)
GroupZoneIds = list(GroupZones.keys())


def questsProgToPGRequirement(questsProg):
    """
    Given a quests progression list,
    gives the complete list of hood IDs that
    a given toon has surpassed.
    """
    appendDict = {  # appendix
        2000: DonaldsDock,
        3000: OldeToontown,
        4000: DaisyGardens,
        5000: MinniesMelodyland,
        6000: TheBrrrgh,
        7000: OutdoorZone,
        8000: DonaldsDreamland,
    }
    retZones = [ToontownCentral]
    for zoneId in appendDict.keys():
        if zoneId in questsProg:
            retZones.append(appendDict[zoneId])
    return retZones


entranceType2FacilityZone = {
    Entrances.FrontFactory: SellbotFactoryInt,
    Entrances.SideFactory: SellbotFactorySideInt,

    Entrances.CoinMint: CashbotMintIntA,
    Entrances.DollarMint: CashbotMintIntB,
    Entrances.BullionMint: CashbotMintIntC,

    Entrances.LawficeA: LawbotStageIntA,
    Entrances.LawficeB: LawbotStageIntB,
    Entrances.LawficeC: LawbotStageIntC,

    Entrances.FrontThree: BossbotCountryClubIntA,
    Entrances.MiddleSix: BossbotCountryClubIntB,
    Entrances.BackNine: BossbotCountryClubIntC,

    # Event
    Entrances.FindTheForeman: SellbotFindForemanInt,
    Entrances.OverclockedFindTheFamily: SellbotOcFindFamilyInt,
}
facilityZone2EntranceType = invertDict(entranceType2FacilityZone)


def isNewZoneAcceptable(groupDef: GroupDefinition, oldZone: int, newZone: int):
    """
    Given a group def and old/new zoneId, checks if the group should disband when entering the new zone.
    Only used on the client.
    """

    if groupDef.forceZoneConstant and oldZone != newZone:
        return False

    # Zone ID 1 is a default ID when toons are loading in
    # Their proper zone ID will be filled in soon after.
    fullHoodOkay = groupDef.allowFullHood and (newZone == 1 or ZoneUtil.getHoodId(newZone) == groupDef.zoneId[0])
    if ZoneUtil.getHoodId(newZone) != ZoneUtil.getHoodId(oldZone) and not fullHoodOkay:
        return False

    if newZone not in groupDef.zoneId and not fullHoodOkay:
        return False

    return True


"""
Moderation Stuff
"""


def hasForceDisbandPermission(avatar):
    from toontown.toonbase.PermissionGlobals import Permission
    acceptedPerms = [Permission.Moderation, Permission.TeamLead, Permission.ModerationLA]
    return any([avatar.hasPermission(permEnum) for permEnum in acceptedPerms])
