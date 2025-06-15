"""
The localizer file for Quest names and other data.
"""
from toontown.quest3.QuestDialogue import QuestTextGigaDict
from toontown.quest3.QuestEnums import QuestSource, QuestItemName, QuestItemName
from toontown.quest3.base.QuestReference import QuestReference, QuestId
from toontown.quest3.base.QuestText import QuestText
from toontown.quest3.SpecialQuestZones import SpecialQuestZones as SQZ
from toontown.toonbase import ToontownGlobals

"""
QUEST SOURCE
"""

SourceDescriptions = {
    QuestSource.MainQuest:  'For the main taskline.',
}

"""
QUEST HEADLINES
"""

# The task headlines for quest chains.
QuestChainHeadlines = {
    QuestSource.MainQuest: {
        1: "Welcome to Moondog!",
        2: "Time for Moondog",
        3: "Zit's Time to Pump Moondog",
        4: "Moondog Jam",
        5: "Moondog Situation",
        6: "The Numbers Moondog...",
        7: "Letter Moondog!",
        8: "A Taste of Moondog",
        9: "Gathering Moondog",
        10: "Smart Moondog Think Unalike",
        11: "Find The Moondog",
    },
}

"""
Various Single-Strings
"""
Gag = "Gag"
Gags = "Gags"
AuxillaryText_Complete = "Return to:"
AuxillaryText_For = "for:"
AuxillaryText_From = 'from:'
AuxillaryText_To = 'to:'
AuxillaryText_Against = 'against:'
AuxillaryText_With = 'with:'
AuxillaryText_Less_Than = 'with less than:'
QuestObjective_Complete = "COMPLETE"
TheFish = 'the Fish'
AtYourHome = 'At your estate'
LevelXGag = '{amount} Level {level} {gag}'
OnDaTrolley = 'The Trolley'
OnTheTrolley = "On the trolley"
TreasureDive = "Treasure Dive"
InThePlayground = 'In the playground'
RideTheTrolley = 'Ride on the trolley'
GoSwim = 'Go for a Swim'
AtTheGagShop = "At the Gag Shop"
Anywhere = "Anywhere"
JungleVines = 'Jungle Vines'
IceSlide = 'Ice Slide'
BefriendCog = "Make friends with a Cog"
GivenLaff = "%s Laff"
GivenBut1Laff = "Nevermind...\nGood luck!"
QuestProgress_Complete = "Complete"

"""
Objective Headlines
"""

HL_Throw = "THROW"
HL_Collect = "COLLECT"
HL_Trolley = "TROLLEY"
HL_Visit = "VISIT"
HL_Swim = "SWIM"
HL_Recover = "RECOVER"
HL_Win = "WIN"
HL_Fish = "GO FISHING"
HL_Search = "SEARCH"
HL_Purchase = "PURCHASE"
HL_Book = "SHTIKERBOOK"
HL_Obtain = "OBTAIN"
HL_Mail = "MAIL"
HL_Investigate = "INVESTIGATE"
HL_Deliver = "DELIVER"
HL_Defeat = "DEFEAT"
HL_Infiltrate = "INFILTRATE"
HL_Wanted = "WANTED"
HL_CogFriend = "BEFRIEND A COG"
HL_Disguise = "SUIT UP"
HL_PicnicGames = "PICNIC GAMES"
HL_Earn = "EARN"
HL_Complete = "COMPLETE"
HL_Race = "RACE"
HL_Stun = "STUN"
HL_Damage = "DAMAGE"
HL_Feed = "FEED"
HL_Destroy = "DESTROY"
HL_Stomp = "STOMP"
HL_Golf = "GOLF"
HL_SAD = "SADDEN"
HL_KNOCK = "LAUGH"
HL_Ride = "RIDE"
HL_JumpOn = "JUMP ON"
HL_Interact = "INTERACT"

"""
Objective prefixes
"""

PFX_DEFEAT = 'Defeat '
PFX_INFILTRATE = 'Infiltrate '
PFX_VISIT = 'Visit '
PFX_FISH = 'Fish up '
PFX_RECOVER = 'Recover '
PFX_DELIVER = 'Deliver '
PFX_OBTAIN = 'Obtain '
PFX_INVESTIGATE = 'Investigate '
PFX_DIVEFOR = 'Dive for '
PFX_TAKEDOWN = 'Take down '
PFX_SWINGFOR = 'Vine swing for '
PFX_CATCH = 'Catch '
PFX_GRAB = 'Grab '
PFX_THROW = 'Throw '
PFX_EARN = 'Earn '
PFX_DESTROY = 'Destroy '
PFX_JUMP_ON_MML = 'Jump on a Drum '
PFX_INTERACT = 'Interact with '

"""
Objective progress
"""

PROG_Throw = '{value} of {range} items thrown'
PROG_Collect = '{value} of {range} collected'
PROG_Recover = '{value} of {range} recovered'
PROG_Defeat = '{value} of {range} defeated'
PROG_Infiltrate = '{value} of {range} infiltrated'
PROG_Deliver = '{value} of {range} delivered'
PROG_Win = '{value} of {range} won'
PROG_Play = '{value} of {range} played'
PROG_Earn = '{value} of {range} earned'
PROG_Complete = '{value} of {range} completed'
PROG_Stun = '{value} of {range} stuns'
PROG_Damage = '{value} of {range} damage'
PROG_Feed = '{value} of {range} fed'
PROG_Destroy = '{value} of {range} destroyed'
PROG_Stomp = '{value} of {range} stomped'
PROG_GolfHits = '{value} of {range} hits'
PROG_Rotations = '{value} of {range} rotations'
PROG_Jumps = '{value} of {range} jumps'
PROG_Interact = '{value} of {range} interacted'

"""
Objective goals
"""

OBJ_Recover = "Recover %s from %s"
OBJ_Defeat = "Defeat %s"
OBJ_Infiltrate = "Infiltrate %s"
OBJ_Visit = "Visit %s"
OBJ_Catch = "Catch %s"
OBJ_Assemble = "Assemble a %s Cog Disguise"
OBJ_CogFriend = "Befriend a Cog"
OBJ_Deliver = "Deliver %s"
OBJ_DeliverTo = "Deliver %s to %s"
OBJ_Investigate = "Investigate %s"
OBJ_Collect = "Collect %s"
OBJ_Mailbox = "Check your Mailbox"
OBJ_Obtain = "Obtain %s"
OBJ_OpenBook = "Open your Shtikerbook"
OBJ_PurchaseGag = "Purchase a Gag"
OBJ_Win = "Win a %s"
OBJ_Play = "Play a %s"
OBJ_Throw = "Throw %s"
OBJ_Earn = "Earn %s %s"
OBJ_Complete = "Complete a %s"
OBJ_RacePlacement = "Place %s in a %s Race"
OBJ_GolfPlacement = "Place %s in a %s Course"
OBJ_Stun = "Stun %s"
OBJ_Feed = "Feed %s"
OBJ_Stomp = "Stomp %s"
OBJ_Sad = "Find a way to go Sad"
OBJ_Knock = "Laugh at a knock knock joke"
OBJ_Ride = "Ride %s"
OBJ_JumpOn = "Jump on %s"
OBJ_Destroy = "Destroy %s"
OBJ_Damage = "Deal %s damage"
OBJ_Interact = "Interact with %s"

"""
Reward phrases
"""

RWD_Background = '\1white\1\5reward_packageIcon\5\2 %s Profile Background'
RWD_Gumballs = '\1white\1\5reward_gumballIcon\5\2 %s Gumballs'
RWD_Jellybeans = '\1white\1\5reward_beanJarIcon\5\2 %s Jellybeans'
RWD_CheesyEffect = '\1white\1\5reward_packageIcon\5\2 %s Cheesy Effect'
RWD_ToonExp = '\1white\1\5reward_expIcon\5\2 %s Experience'
RWD_Furniture = '\1white\1\5reward_packageIcon\5\2 %s'
RWD_Shirt = '\1white\1\5reward_packageIcon\5\2 %s Shirt'
RWD_Short = '\1white\1\5reward_packageIcon\5\2 %s Shorts'
RWD_Skirt = '\1white\1\5reward_packageIcon\5\2 %s Skirt'
RWD_Accessory = '\1white\1\5reward_packageIcon\5\2 %s'
RWD_Laff = '\1white\1\5reward_laffIcon%s\5\2 Laff Boost'
RWD_Nameplate = '\1white\1\5reward_packageIcon\5\2 %s Profile Nameplate'
RWD_Nametag = '\1white\1\5reward_packageIcon\5\2 %s Nametag Font'
RWD_ProfilePose = '\1white\1\5reward_packageIcon\5\2 %s Profile Pose'
RWD_TPAccess = '\1white\1\5reward_teleportIcon\5\2 %s Teleport Access'
RWD_Booster = '%s Hour %s'

"""
Speedchat Phrases
"""

SC_GoFishing = "I need to fish up %s from %s."
SC_Defeat = "I need to defeat %s."
SC_DefeatLocation = "I need to defeat %s%s."
SC_Infiltrate = "I need to infiltrate %s."
SC_InfiltrateLocation = "I need to infiltrate %s%s."
SC_RecoverCogs = "I need to recover %s from %s%s."
SC_Deliver = "I need to deliver {}."
SC_Obtain = "I need to obtain %s."
SC_Investigate = "I need to investigate the %s."
SC_Mail = 'I need to check my mail.'
SC_DeliverGags = 'I need to deliver a Level %s Gag.'
SC_Book = 'I need to open my Shtickerbook.'
SC_Snowball = 'I need to collect some snowballs.'
SC_TreasureChest = 'I need to go diving for some Treasure Chests.'
SC_DeliverJbs = 'I need to deliver some Jellybeans.'
SC_EarnJbs = 'I need to earn some Jellybeans.'
SC_Building = "I need to defeat %s%s."
SC_Laff_Building = "I need to defeat %s%s with less than %s%% Laff."
SC_Laff_Building_1Laff = "I need to defeat %s%s without going sad, whelp."
SC_CogDisguise = 'I need to assemble my %s Cog disguise.'
SC_ThrowPies = 'I need to throw some pies.'
SC_Treasure = 'I need to collect some treasures.'
SC_Trolley = 'I need to ride the trolley.'
SC_Swim = 'I need to go for a swim.'
SC_Search = "I need to search for a %s."
SC_Gags = 'I need to buy some gags from the Gag Shop.'
SC_JungleVines = 'I need to play Jungle Vines for some bananas.'
SC_IceSlide = 'I need to play Ice Slide for some treasure barrels.'
SC_CogFriend = 'I need to make friends with a Cog.'
SC_CatchingGame = 'I need to play Catching Game for some %s.'
SC_Fishing = 'I need to catch %s "%s" fish.'
SC_Visit = 'I need to see %s.'
SC_VisitPlayground = 'I need to go to %s Playground.'
SC_VisitSpecific = 'I need to go %(to)s %(street)s in %(hood)s.'
SC_VisitBuilding = 'I need to visit %s%s.'
SC_VisitBuildingWhere = 'Where is %s%s?'
SC_PGTWin = 'I need to win %s.'
SC_PGTPlay = 'I need to play %s.'
SC_GagExp = 'I need to earn %s %s experience.'
SC_RaceComplete = 'I need to complete {totalRaces}{trackName} race{s}.'
SC_GolfComplete = 'I need to complete %s %s golf courses.'
SC_Stun = 'I need to stun %s %s.'
SC_Damage = 'I need to deal %s damage to %s.'
SC_DamageWeapon = 'I need to deal %s damage to %s with %s.'
SC_Feed = 'I need to feed %s %s.'
SC_Collect = 'I need to collect %s%s.'
SC_Destroy = 'I need to destroy %s %s with %s.'
SC_Stomp = 'I need to stomp %s%s.'
SC_GolfHits = 'I need to hit %s with %s golf balls.'
SC_Sad = 'I need to go Sad.'
SC_Knock = 'I need to go laugh at a knock knock joke.'
SC_Ride = 'I need to ride the piano %s time%s.'
SC_JumpOn = 'I need to jump on a drum %s time%s.'
SC_Interact = 'I need to interact with %s.'

"""
Quest poster specific strings
"""

QP_JustForFun = "Just for fun!"
QP_Expire = "Expires in %s days!"
QP_ConfirmDelete = 'Are you sure you want to delete this ToonTask?'

"""
Cog Zone Name Overrides
"""

DefeatCogZoneNames = {
    ToontownGlobals.SchoolHouse: ' in the Schoolhouse Basement',
    ToontownGlobals.LighthouseInt: ' at the Lighthouse Pier',
    ToontownGlobals.ChainsawLogging: ' at Cut to the Chase! Logging Co',
}

"""
Various QuestEnum matches
"""


QuestItemNames = {
    'default':                                  ('The World\'s Most Radical Trout!!', 'The World\'s Most Radical Trouts!!', 'a '),
    QuestItemName.Moondog:             ('Moondog', 'Moondog', 'some '),
}


def itemTuple2Word(itemTuple: tuple, count: int = 1, capitalizeFirstInSingular: bool = False):
    """Converts an item tuple to a word, given a count of the rewards."""
    if count == 1:
        prefix = itemTuple[2]
        if capitalizeFirstInSingular:
            prefix = prefix.capitalize()
        return f'{prefix}{itemTuple[0]}'
    else:
        return f'{count} {itemTuple[1]}'


def getQuestItemText(questItem: QuestItemName, count: int = 1, capitalizeFirstInSingular: bool = False):
    questItemTuple = QuestItemNames.get(questItem, QuestItemNames['default'])
    return itemTuple2Word(itemTuple=questItemTuple, count=count, capitalizeFirstInSingular=capitalizeFirstInSingular).strip()


"""
Functions for localization access.
"""


def getQuestHeadline(questReference: QuestReference, objectiveSelected: int = 0):
    """Given a quest reference, get the quest headline."""
    questId = questReference.getQuestId()

    # Do we have a part headline?
    questSourceHeadline = QuestChainObjectiveHeadlines.get(questId.getQuestSource())
    if questSourceHeadline:
        # Is the quest chain in here?
        questChainHeadline = questSourceHeadline.get(questId.getChainId())
        if questChainHeadline:
            # Is the quest part in here?
            questObjectiveHeadline = questChainHeadline.get(questId.getObjectiveId())
            if questObjectiveHeadline:
                # This is the objective's headline (overrides the chain).
                return questObjectiveHeadline.strip()

    # Use the quest chain's defined headline.
    questSourceHeadline = QuestChainHeadlines.get(questId.getQuestSource())
    if questSourceHeadline:
        # Is the quest chain in here?
        questChainHeadline = questSourceHeadline.get(questId.getChainId())
        if questChainHeadline:
            # This is the headline.
            return questChainHeadline.strip()

    # Try the quest objective headline.
    from toontown.quest3.base.QuestLine import QuestLine
    questObjective = QuestLine.dereferenceQuestReference(questReference).getObjectiveIndex(objectiveSelected)
    questObjectiveHeadline = questObjective.getHeadline(questReference, objectiveSelected)
    if questObjectiveHeadline:
        # This is the headline.
        return questObjectiveHeadline.strip()

    # No defined headline.
    return ''


def getQuestObjectiveText(questReference: QuestReference, objectiveSelected: int = 0):
    """Given a quest reference, get the quest objective headline text."""
    # Get the quest objective headline.
    from toontown.quest3.base.QuestLine import QuestLine
    questObjective = QuestLine.dereferenceQuestReference(questReference).getObjectiveIndex(objectiveSelected)
    questObjectiveHeadline = questObjective.getHeadline(questReference, objectiveSelected)
    if questObjectiveHeadline:
        # This is the headline.
        return questObjectiveHeadline.strip()
    return ''


def getQuestAuxillaryText(questReference: QuestReference, objectiveSelected: int = 0):
    """Given a quest reference, get the quest auxillary text."""
    # Get the quest auxillary text.
    from toontown.quest3.base.QuestLine import QuestLine
    questObjective = QuestLine.dereferenceQuestReference(questReference).getObjectiveIndex(objectiveSelected)
    questObjectiveAuxillaryText = QuestObjectiveAuxillaryText.get(type(questObjective))
    if questObjectiveAuxillaryText:
        # This is the aux text.
        return questObjectiveAuxillaryText.strip()
    return ''


def getQuestInfoText(questReference: QuestReference, objectiveSelected: int = 0):
    """Given a quest reference, get the quest info text."""
    # Get the quest info text format.
    from toontown.quest3.base.QuestLine import QuestLine
    questObjective = QuestLine.dereferenceQuestReference(questReference).getObjectiveIndex(objectiveSelected)
    questObjectiveInfoFormat = QuestInfoFormats.get(type(questObjective), None)

    # Format the info text in a way the objective wants.
    objectiveTextStrings = questObjective.getInfoTextStrings(questReference=questReference)

    # If there are no text strings, no formatting.
    if not objectiveTextStrings:
        return None

    # Otherwise, format them.
    if questObjectiveInfoFormat:
        return (questObjectiveInfoFormat % objectiveTextStrings).strip()
    else:
        return '\n'.join(objectiveTextStrings).strip()


def getQuestText(questId: QuestId, assigned: bool = False) -> QuestText:
    """Gets the QuestText object from a questId."""
    questTextSourceDict = QuestTextGigaDict.get(questId.getQuestSource(), None)
    if questTextSourceDict is None:
        return QuestText()
    questTextChainDict = questTextSourceDict.get(questId.getChainId())
    if not questTextChainDict:
        return QuestText()

    # We are being assigned a new quest. Use the first (0th) dialogue.
    if assigned:
        questText = questTextChainDict.get(0)
    else:
        questText = questTextChainDict.get(questId.getObjectiveId())

    if not questText:
        return QuestText()
    if type(questText) not in (tuple, list):
        return questText
    return questText[questId.getSubObjectiveId()]


"""
Misc localization strings
"""

# Key: NPC ID, Value: Unique Dialogue
QuestChoiceUnique = {
}

QuestChoice = 'Choose a ToonTask.'

# Key: NPC ID, Value: Unique Dialogue
QuestChoiceCancelUnique = {
}

QuestChoiceCancel = 'Come back when you are ready to decide! Bye!'

InstanceNotAvailable = {
    # Derrick Man
    1: "You hear the sounds of Moondog bubbling and machines whirring. You decide not to enter.",
}

SpecialQuestZone2Name = {
    SQZ.AnyCogHQ: ("to", "in", "Any Cog HQ"),
    SQZ.SellbotFactory: ("to the", "in the", "Sellbot Factory"),
    SQZ.CashbotMints: ("to the", "in the", "Cashbot Mints"),
    SQZ.LawbotLawfices: ("to the", "in the", "Lawbot Lawfices"),
    SQZ.BossbotGolfCourses: ("to the", "in the", "Bossbot Golf Courses"),
    SQZ.SellbotBoss: ("to the", "in the", "Sellbot Towers Rooftop"),
    SQZ.LawbotBoss: ("to the", "in the", "Lawbot Executive Lawfice"),
    SQZ.HM_LawbotBoss: ("to the", "in the", "Lawbot Executive Lawfice"),
    SQZ.CeosOffice: ("to the", "in the", "C.E.O.'s Office"),
}

KudosQuestNameBase = '{xpType} Kudos Task'
KudosQuestPrefixNames = {
    1: 'Bronze',
    2: 'Silver',
    3: 'Gold',
}
