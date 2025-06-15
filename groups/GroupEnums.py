import enum
from enum import auto
from typing import List


class GroupType(enum.IntEnum):
    # All of the general Group Types that may show up in the Group Tracker.
    BASE = auto()

    # Bosses
    VP = auto()
    CFO = auto()
    CLO = auto()
    OCLO = auto()
    CEO = auto()

    # Facilities
    FrontFactory = auto()
    SideFactory = auto()

    CoinMint = auto()
    DollarMint = auto()
    BullionMint = auto()

    LawficeA = auto()
    LawficeB = auto()
    LawficeC = auto()

    SilverSprocket = auto()
    GoldenGear = auto()
    DiamondDynamo = auto()

    # Minibosses
    DM = auto()
    DOLA = auto()
    DOPR = auto()
    DOPA = auto()

    # Minigames
    Racing = auto()
    Golfing = auto()
    Trolley = auto()
    Checkers = auto()
    Chess = auto()
    TOONO = auto()

    # Buildings
    BuildingSell = auto()
    BuildingCash = auto()
    BuildingLaw = auto()
    BuildingBoss = auto()
    BuildingBoard = auto()

    # Street Mercs
    DuckShuffler = auto()
    DeepDiver = auto()
    Gatekeeper = auto()
    Bellringer = auto()
    Mouthpiece = auto()
    Firestarter = auto()
    Treekiller = auto()
    Featherbedder = auto()

    # Instance Mercs
    Prethinker = auto()
    Rainmaker = auto()
    Witchhunter = auto()
    Multislacker = auto()
    Majorplayer = auto()
    Plutocrat = auto()
    Chainsaw = auto()
    Pacesetter = auto()

    # Misc
    Fishing = auto()
    Pizzeria = auto()

    # Event
    Highroller = auto()
    FindTheFamily = auto()
    OverclockedFindTheFamily = auto()
    COO = auto()


class Entrances(enum.IntEnum):
    # More specific entrance types.
    # These represent potentially different Elevator entrances.
    # Aren't really necessary for areas with a singular elevator.

    # Factory
    FrontFactory = auto()
    SideFactory = auto()
    # Mints
    CoinMint = auto()
    DollarMint = auto()
    BullionMint = auto()
    # Lawfices
    LawficeA = auto()
    LawficeB = auto()
    LawficeC = auto()
    # CGCs
    FrontThree = auto()
    MiddleSix = auto()
    BackNine = auto()

    # Event
    FindTheForeman = auto()
    OverclockedFindTheFamily = auto()


class Locations(enum.IntEnum):
    """
    NOT USED
    """
    # All potential zones where a particular group may be made.
    MEET_ME_HERE = -1  # The zone that the player themselves are in.
    PLAYGROUND = 0
    ANY_STREET = 1
    SELLBOT_HQ = 2
    SELLBOT_SIDE = 3
    CASHBOT_HQ = 4
    LAWBOT_HQ = 5
    LAWBOT_HQ_SIDE = 6
    BOSSBOT_HQ = 7
    BOARDBOT_HQ = 8
    SPEEDWAY = 9
    MINIGAME_ZONE = 10
    DERRICK_ZONE = 11
    DOLA_ZONE = 12
    DOPR_ZONE = 13
    PRETHINKER_ZONE = 14
    RAINMAKER_ZONE = 15
    WITCHHUNTER_ZONE = 16
    MULTISLACKER_ZONE = 17
    MAJORPLAYER_ZONE = 18
    PLUTOCRAT_ZONE = 19
    CHAINSAW_ZONE = 20
    PACESETTER_ZONE = 21


class Options(enum.IntEnum):
    # Any option that a group may provide.
    # These are options that may be modified in a group.
    # Cog Buildings
    SELLBOT = auto()
    CASHBOT = auto()
    LAWBOT = auto()
    BOSSBOT = auto()
    BOARDBOT = auto()
    # Bosses
    ANY_TIER = auto()
    TIER_ONE = auto()
    TIER_TWO = auto()
    TIER_THREE = auto()
    TIER_OVERCLOCKED = auto()
    # Facilities
    LENGTH_ANY = auto()
    LENGTH_SHORT = auto()
    LENGTH_LONG = auto()
    LENGTH_MINIMAL = auto()
    LENGTH_FULL = auto()
    LENGTH_TRAINING = auto()
    # Mercs
    REGULAR = auto()
    DIFFICULT = auto()
    OVERCLOCKED = auto()
    # General
    CASUAL = auto()
    COMPETITIVE = auto()
    TRACKS = auto()
    EASY = auto()
    MEDIUM = auto()
    HARD = auto()
    # Buildings
    ONE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    # Social
    SOCIAL_HANGOUT = auto()
    SOCIAL_PARTY = auto()
    SOCIAL_ROLEPLAY = auto()
    # FTF
    HIGHLY_UNSTABLE = auto()


class Responses(enum.IntEnum):
    # Responses between client/AI/UD grouptracking.

    OK = 1
    AlreadyInGroup = 2

    # Responses for Group Leave/Disbands.
    LeaveDisbanded = 3
    LeaveKicked = 4

    # Genreal Group keepup codes
    ToonJoined = 5
    ToonLeft = 6
    GroupDisbanded = 7
    ManagerRestart = 8

    # Help codes
    HelpGeneral = 10
    HelpPrivacy = 11
    HelpInvite = 12

    # Error codes for group callbacks
    GroupNonexistent = 30
    GroupFilledUp = 31
    GroupNotPublic = 32
    PlayerGroupBanned = 33
    GeneralError = 34
    PlayerInBattle = 35
    BadLocation = 36
    TooLowTaskProgression = 37
    BossNoSuit = 38
    BossNoMerits = 39
    OverclockedNotUnlocked = 40
    TooBroke2RaceLol = 41
    KickedFromGroup = 42
    HasNoRaceKart = 43
    AreaNotVisited = 44
    SuitTooLowForTier = 45
    TryAgain = 46
    InviteExpired = 47
    UnacceptingInvites = 48
    DistrictDraining = 49
    DistrictFull = 50
    DistrictFullPizzeria = 51
    GroupNotAvailable = 52
    ModeratorDisband = 53

    # Warnings are other error codes, but not sent if
    # we set the force mode on inviting a player
    # slash joining a group to be true.
    # (This logic is handled in the tests for DistributedGroupManagerAI.)
    WarningNeedDirective = 60
    WarningPerhapsTooPoorToRace = 61
    WarningFacilityMissesPart = 62
    WarningBelowLaffRec = 63
    WarningBelowGagRec = 64

    # Response types
    CannotJoinGroup = 70
    CannotInviteUser = 71
    CannotMakeGroup = 72
    Info = 73


# Responses that are considered warnings, i.e. they probably shouldn't join the group but can anyways
ResponseWarnings = {
    Responses.WarningNeedDirective,
    Responses.WarningPerhapsTooPoorToRace,
    Responses.WarningFacilityMissesPart,
    Responses.WarningBelowLaffRec,
    Responses.WarningBelowGagRec,
}

# Responses that are considered fails to join, but they can still see the group anyways
ResponsesFailsButVisible = {
    Responses.BossNoMerits,
    Responses.HasNoRaceKart,
    Responses.TooBroke2RaceLol,
    Responses.PlayerInBattle,
    Responses.DistrictFull
}


class FilterCategoryEnum(enum.IntEnum):
    """
    Categories for the Group SocialPanel's client filters.
    """
    Any = auto()
    Buildings = auto()
    Bosses = auto()
    Minibosses = auto()
    Facilities = auto()
    Activities = auto()
    Social = auto()
    Event = auto()


"""
Group Filtering Classes
"""
# region


class FilterLocation:
    """
    A container class for listing filter locations from a given filter type.
    """

    def __init__(self, name: str, locations: list = None, hoods: list = None):
        """
        Initalizes a location for a filter type.
        :param name: Name of this location.
        :param locations: Associated locations for the location.
        :param hoods: Associated list of hood zoneIDs for this location.
        """
        if locations is None:
            locations = []
        if hoods is None:
            hoods = []
        self.name = name
        self.locations = locations
        self.hoods = hoods


class FilterType:
    """
    A container class for listing filter types under a given category.
    """

    def __init__(self, name: str, filterLocations: list,
                 groupTypes: list = None, options: list = None,
                 wantAll: bool = True):
        """
        Initializes a filter type for a category.
        :param name: The name of this category.
        :param filterLocations: A list of filter locations for this filter type.
        :param groupTypes: A list of group types associated with this filter.
        :param options: A list of options associated with this filter.
        :param wantAll: Do all group types need to be satisfied for the type to be visible?
        """
        if groupTypes is None:
            groupTypes = []
        if options is None:
            options = []
        self.name = name
        self.filterLocations = filterLocations
        self.groupTypes = groupTypes
        self.options = options
        self.wantAll = wantAll

    def getGroupTypes(self) -> List[GroupType]:
        return self.groupTypes

    def getFilterLocations(self, restrict):
        if not restrict:
            return self.filterLocations
        retList = []
        for location in self.filterLocations:
            if not location.hoods:
                # no hoods selected, so presumably all are ok.
                retList.append(location)
            elif base.localAvatar:
                for hood in location.hoods:
                    from toontown.toonbase.ToontownGlobals import HoodsAlwaysVisited
                    if hood in base.localAvatar.getHoodsVisited() + HoodsAlwaysVisited:
                        # this hood is a place we've been to before!
                        retList.append(location)
                        break
        return retList

    def getFilterNames(self, restrict):
        return [location.name for location in self.getFilterLocations(restrict=restrict)]

    def getWantAll(self) -> bool:
        return self.wantAll


class FilterCategory:
    """
    A container class containing the information about a FilterCategory.
    """

    def __init__(self, name: str, enum: FilterCategoryEnum, types: list = None):
        """
        Initializes an entire filter category.
        :param name: The name of the category.
        :param enum: The associated enum for this category.
        :param types: A list of filter types for this category.
        """
        if types is None:
            types = []
        self.name = name
        self.enum = enum
        self.types = types

    def getEnum(self) -> FilterCategoryEnum:
        return self.enum

    def getFilterTypes(self, restrict, filterer):
        if not restrict:
            return self.types
        retList = []
        for filterType in self.types:
            # if this type has no location, we shouldn't add it
            if not filterType.getFilterLocations(restrict):
                continue
            if not base.localAvatar:
                break
            # run a groupfilterer check on this
            if filterType.getWantAll():
                success = True
                for groupType in filterType.getGroupTypes():
                    if filterer.runGroupTestsFromGroupType(base.localAvatar, groupType) is not Responses.OK:
                        success = False
                        break
            else:
                success = False
                for groupType in filterType.getGroupTypes():
                    if filterer.runGroupTestsFromGroupType(base.localAvatar, groupType) is Responses.OK:
                        success = True
                        break
            if success:
                retList.append(filterType)
        return retList

    def getFilterNames(self, restrict, filterer):
        return [t.name for t in self.getFilterTypes(restrict=restrict, filterer=filterer)]


class FilterCategoryList:
    """
    A container class containing a list of filter categories.
    """

    def __init__(self, *categoryList):
        """
        Initializes a filter category list.
        :param categoryList: List of FilterCategories.
        """
        self.categoryList: List[FilterCategory] = list(categoryList)

    def getFilterCategories(self, restrict, filterer):
        if not restrict:
            return self.categoryList
        retList = []
        for category in self.categoryList:
            # if this is the any category, it's ok
            if category.enum is not FilterCategoryEnum.Any:
                # if this type has no type, we shouldn't add it
                if not category.getFilterTypes(restrict, filterer=filterer):
                    continue
            retList.append(category)
        return retList

    def getFilterNames(self, restrict, filterer):
        return [category.name for category in self.getFilterCategories(restrict=restrict, filterer=filterer)]

# endregion
