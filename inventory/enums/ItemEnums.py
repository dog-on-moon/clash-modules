"""
A module file containing several enums for item representation.
Includes the high-level types (hats, glasses, etc) and their subtypes.
"""
from enum import IntEnum
from typing import Type, Dict

from toontown.utils.EnhancedIntEnum import EnhancedIntEnum

_ItemTypeToSubtypeClass: Dict['ItemType', Type['ItemType']] = {}
_SubtypeClassToItemType: Dict[Type['IntEnum'], 'ItemType'] = {}


def defineItemSubtypeEnum(itemType: 'ItemType'):
    """
    A decorator to define an item subtype enum.
    """

    def wrapper(cls):
        _ItemTypeToSubtypeClass[itemType] = cls
        _SubtypeClassToItemType[cls] = itemType
        return cls

    return wrapper


class ItemType(IntEnum):
    """
    The highest-level enum which holds each "category" of item.
    These reflect all of the generic kinds of items.
    """
    # Cosmetics
    Cosmetic_Shirt           = 1000
    Cosmetic_Shorts          = 1001
    Cosmetic_Hat             = 1002
    Cosmetic_Glasses         = 1003
    Cosmetic_Backpack        = 1004
    Cosmetic_Shoes           = 1005
    Cosmetic_Neck            = 1006

    # Social
    Social_NametagFont     = 2000
    Social_CheesyEffect    = 2001
    Social_CustomSpeedchat = 2002
    Social_ChatStickers    = 2003
    Social_Emote           = 2004

    # Profile Items
    Profile_Nameplate  = 3000
    Profile_Background = 3001
    Profile_Pose       = 3002

    # Fishing
    Fishing_Rod    = 4000

    # Consumables
    Consumable_Boosters = 6000

    # Misc
    Material = 7000
    Trophy   = 7001

    """
    Item type class accessors
    """

    @staticmethod
    def getSubtypeClass(itemType: 'ItemType') -> Type['ItemType']:
        """
        Gets the item subtype given a specified ItemType.
        """
        assert itemType in _ItemTypeToSubtypeClass, \
            f"itemType {itemType} does not have a specified subtype."
        return _ItemTypeToSubtypeClass.get(itemType)

    @staticmethod
    def getItemType(subtypeCls: Type['IntEnum']) -> 'ItemType':
        """
        Gets the item type given a specified item subtype.
        """
        assert subtypeCls in _SubtypeClassToItemType, \
            f"subtypeCls {subtypeCls} does not have a specified item type."
        return _SubtypeClassToItemType.get(subtypeCls)


"""Cosmetic ItemTypes"""


@defineItemSubtypeEnum(ItemType.Cosmetic_Shirt)
class ShirtItemType(IntEnum):
    """
    Item subtype enum for Shirts.
    """
    Plain = 1                       # old: 0
    BottomStripe = 2                # old: 1
    ButtonUpA = 3                   # old: 2
    DoubleStriped = 4               # old: 3
    Striped = 5                     # old: 4
    PocketPolo = 6                  # old: 5
    Feather = 7                     # old: 8
    Dress = 8                       # old: 9
    TwoToneButtonUp = 9             # old: 10
    Vest = 10                       # old: 11
    ButtonUpB = 11                  # old: 14
    Soccer = 12                     # old: 16
    LightningBolt = 13              # old: 17
    No19 = 14                       # old: 18
    Guayabera = 15                  # old: 19
    Flower = 16                     # old: 6
    FlowerStripe = 17               # old: 7
    DenimVest = 18                  # old: 12
    CuffedBlouse = 19               # old: 13
    Peplum = 20                     # old: 15
    Hearts = 21                     # old: 20
    Stars = 22                      # old: 21
    SingleFlower = 23               # old: 22
    ZipUpHoodie = 24                # old: 25
    Island = 25                     # old: 27
    PurpleStars = 26                # old: 38
    WinterStripes = 27              # old: 26
    No1 = 29                        # old: 28
    GreenStripe = 30                # old: 37
    RedCheckerboardKimono = 31      # old: 39
    GoldenStripes = 32              # old: 23
    PinkBow = 34                    # old: 24
    TiedDress = 35                  # old: 36
    WinterStripe = 36               # old: 40
    TieDye = 37                     # old: 45
    Sheriff = 38                    # old: 52
    CheckeredCowboy = 39            # old: 53
    CactusCowboy = 40               # old: 54
    CowboyVest = 41                 # old: 55
    GreenDrawstring = 42            # old: 56
    BlueDrawstring = 43             # old: 57
    Ghost = 44                      # old: 29
    Pumpkin = 45                    # old: 30
    VampireA = 46                   # old: 114
    Turtle = 47                     # old: 115
    VampireB = 48                   # old: 122
    Toonosaur = 49                  # old: 123
    FishingBubble = 50              # old: 124
    FORE = 51                       # old: 125
    GearBusting = 52                # old: 126
    Snowman = 53                    # old: 31
    Snowflakes = 54                 # old: 32
    CandyCaneHearts = 55            # old: 33
    WinterScarf = 56                # old: 34
    PinkHeart = 57                  # old: 41
    RedHeart = 58                   # old: 42
    WingedHeart = 59                # old: 43
    FieryHeart = 60                 # old: 44
    Cupid = 61                      # old: 69
    DottedHearts = 62               # old: 70
    RedBow = 63                     # old: 96
    LuckyClover = 64                # old: 47
    PotOGold = 65                   # old: 48
    IdesofMarch = 66                # old: 116
    Fisherman = 67                  # old: 49
    Goldfish = 68                   # old: 50
    Pawprint = 69                   # old: 51
    BackpackAndShades = 70          # old: 62
    Lederhosen = 71                 # old: 63
    Watermelon = 72                 # old: 64
    RacingFlag = 73                 # old: 65
    AmericanFlag = 74               # old: 58
    Fireworks = 75                  # old: 59
    GreenButtonUp = 76              # old: 60
    Daisy = 77                      # old: 61
    BananaPeel = 78                 # old: 66
    BikeHorn = 79                   # old: 67
    HypnoGoggles = 80               # old: 68
    ClownFish = 81                  # old: 72
    OldBootA = 82                   # old: 73
    Mole = 83                       # old: 74
    Gardening = 84                  # old: 75
    Cupcake = 85                    # old: 76
    PartyHat = 86                   # old: 77
    RoadsterRaceway = 87            # old: 78
    Roadster = 88                   # old: 79
    CoolSun = 89                    # old: 80
    Beachball = 90                  # old: 81
    DiamondPolo = 91                # old: 82
    DottedPolo = 92                 # old: 83
    GoldMedal = 93                  # old: 86
    SaveTheBuildings = 94           # old: 87
    SaveTheBuildingsNo2 = 95        # old: 88
    ToontaskCompleter = 96          # old: 89
    ToontaskCompleterNo2 = 97       # old: 90
    Trolley = 98                    # old: 91
    TrolleyNo2 = 99                 # old: 92
    WinterGift = 100                # old: 93
    Skeletoon = 101                 # old: 94
    Cobweb = 102                    # old: 95
    MostCogsDefeatedA = 103         # old: 106
    MostVPsDefeated = 104           # old: 110
    SellbotSmasher = 105            # old: 111
    Pirate = 106                    # old: 120
    Supertoon = 107                 # old: 121
    RacerJumpsuit = 108             # old: 118
    NoTimeforCogBuildings = 109     # old: 128
    TrolleyGang = 110               # old: 129
    OldBootB = 111                  # old: 130
    WitchPolo = 112                 # old: 132
    Sledding = 113                  # old: 133
    Bat = 114                       # old: 134
    Mittens = 115                   # old: 135
    PoolShark = 116                 # old: 136
    PianoTuna = 117                 # old: 137
    GolfStripes = 118               # old: 138
    DummyCogPolo = 119              # old: 141
    MostCogsDefeatedforAnts = 120   # old: 142
    TrolleyForAnts = 121            # old: 143
    TrolleySideways = 122           # old: 144
    MostBuildingsDefeated = 123     # old: 145
    MostCogsDefeatedB = 124         # old: 146
    BirthdayCake = 125              # old: 147
    LoonyLabsScientistA = 126       # old: 97
    LoonyLabsScientistB = 127       # old: 98
    LoonyLabsScientistC = 128       # old: 99
    SillyMailbox = 129              # old: 100
    SillyTrashCan = 130             # old: 101
    LoonyLabsLogo = 131             # old: 102
    SillyHydrant = 132              # old: 103
    SillyMeterWhistle = 133         # old: 104
    CogCrusherShirt = 134           # old: 105
    NoMoreCheese = 135              # old: 107
    FlunkyFlannel = 136             # old: 108
    DefeatedSellbots = 137          # old: 109
    JellybeanJar = 138              # old: 112
    Doodle = 139                    # old: 113
    GetConnected = 140              # old: 117
    Bee = 141                       # old: 119
    Meatballs = 142                 # old: 148
    TrashcatsRags = 143             # old: 149
    DrowsyDreamland = 144           # old: 150
    BetaToon = 145                  # old: 151
    YOTTKnight = 146                # old: 152
    BBSailor = 147                  # old: 153
    DGGardening = 148               # old: 154
    TTCFirefighter = 149            # old: 155
    MMLBand = 150                   # old: 156
    TeamBarnyard = 151              # old: 157
    TeamOutback = 152               # old: 158
    BarnyardVacation = 153          # old: 159
    OutbackVacation = 154           # old: 160
    AAParkRanger = 155              # old: 161
    BrrrghSnowflakes = 156          # old: 162
    Alchemist = 157                 # old: 163
    AlchemistOveralls = 158         # old: 164
    Frankentoon = 159               # old: 165
    Spacetoon = 160                 # old: 166
    MadScientist = 161              # old: 167
    Clown = 162                     # old: 168
    Wonderland = 163                # old: 169
    Reaper = 164                    # old: 170
    Scarecrow = 165                 # old: 171
    ScarecrowOveralls = 166         # old: 172
    Wizard = 167                    # old: 173
    GreenElfShirt = 168             # old: 174
    RedElfShirt = 169               # old: 175
    GingerbreadA = 170              # old: 176
    GingerbreadB = 171              # old: 177
    PresentUniform = 172            # old: 178
    RagdollHumble = 173             # old: 179
    RagdollRegal = 174              # old: 180
    RagdollTraditional = 175        # old: 181
    Reindeer = 176                  # old: 182
    TinSoldierHumble = 177          # old: 183
    TinSoldierRegal = 178           # old: 184
    TinSoldierTraditional = 179     # old: 185
    UglySweater = 180               # old: 186
    VintageSnowShirt = 181          # old: 187
    NY2019Suit = 182                # old: 188
    NY2019Dress = 183               # old: 189
    CupidOutfit = 184               # old: 190
    DoesShirt = 185                 # old: 191
    WebstersShirt = 186             # old: 192
    AngelWings = 187                # old: 193
    AviatorShirt = 188              # old: 194
    WingsuitShirt = 189             # old: 195
    DragonWings = 190               # old: 196
    ChibiWings = 191                # old: 197
    BurgerShirt = 192               # old: 198
    SellbotSeeker = 193             # old: 199
    CashbotCatcher = 194            # old: 200
    LawbotLiberator = 195           # old: 201
    BossbotBasher = 196             # old: 202
    OutbackUniform = 197            # old: 203
    OutbackDenim = 198              # old: 204
    AlienShirt = 199                # old: 205
    CandyCornShirt = 200            # old: 206
    Busted = 201                    # old: 207
    LawbotResistance = 202          # old: 208
    RetroRobotShirt = 203           # old: 209
    RidingHoodShirt = 204           # old: 210
    NurseShirt = 205                # old: 211
    LazyBonesShirt = 206            # old: 212
    SailorShirtA = 207              # old: 213
    SailorShirtB = 208              # old: 214
    BlueSailorShirtA = 209          # old: 215
    BlueSailorShirtB = 210          # old: 216
    CyanSailorShirtA = 211          # old: 217
    CyanSailorShirtB = 212          # old: 218
    GreenSailorShirtA = 213         # old: 219
    GreenSailorShirtB = 214         # old: 220
    OrangeSailorShirtA = 215        # old: 221
    OrangeSailorShirtB = 216        # old: 222
    PinkSailorShirtA = 217          # old: 223
    PinkSailorShirtB = 218          # old: 224
    PurpleSailorShirtA = 219        # old: 225
    PurpleSailorShirtB = 220        # old: 226
    RedSailorShirtA = 221           # old: 227
    RedSailorShirtB = 222           # old: 228
    BlackSailorShirtA = 223         # old: 229
    BlackSailorShirtB = 224         # old: 230
    GoldenSailorShirtA = 225        # old: 231
    GoldenSailorShirtB = 226        # old: 232
    TeamTreesShirt = 227            # old: 233
    HomemadeRagdoll = 228           # old: 234
    HomemadeSoldier = 229           # old: 235
    RetroWinterSuit = 230           # old: 236
    RetroWinterDress = 231          # old: 237
    SnowmanShirt = 232              # old: 238
    NewYears2020 = 233              # old: 239
    ValentoonsShirt = 234           # old: 240
    AgentSevensShirt = 235          # old: 241
    StPats2020 = 236                # old: 242
    ClownShirt = 237                # old: 243
    SevenStriped = 238              # old: 244
    TripleRainbow = 239             # old: 245
    BoardbotShirt = 240             # old: 246
    BoredbotShirt = 241             # old: 247
    JesterShirt = 242               # old: 248
    BlackJesterShirt = 243          # old: 249
    Easter2020 = 244                # old: 250
    ExecutiveBoardbot = 245         # old: 251
    LawbotSuitTop = 246             # old: 252
    CooktheCogsShirt = 247          # old: 253
    VacationFroge = 248             # old: 254
    PhantoonShirt = 249             # old: 255
    VolunteerRanger = 250           # old: 256
    ToonsmasPast = 251              # old: 257
    ToonsmasPresent = 252           # old: 258
    ToonsmasFuture = 253            # old: 259
    NewYears2021 = 254              # old: 260
    TumblesShirt = 255              # old: 261
    Valentoons2021 = 256            # old: 262
    HallowopolisShirt = 257         # old: 263
    Detective = 258                 # old: 264
    TwoPocketCargo = 259            # old: 265
    JacketAndFlannel = 260          # old: 266
    BlueNewstoon = 261              # old: 267
    GrayNewstoon = 262              # old: 268
    ChupShirt = 263                 # old: 269
    NewYears2022 = 264              # old: 270
    Valentoons2022 = 265            # old: 271
    DoctorToonShirt = 266           # old: 272
    TrolleyEngineerShirt = 267      # old: 274
    ArtisticShirt = 268             # old: 275
    StarstruckShirt = 269           # old: 276
    RetroShirt = 270                # old: 277
    BattleJacket = 271              # old: 278
    GumballMachineShirt = 272       # old: 279
    CardSuitShirtA = 273            # old: 280
    CardSuitShirtB = 274            # old: 289
    SchoolhouseFlannel = 275        # old: 281
    SleepwalkerShirt = 276          # old: 282
    FruitPieShirt = 277             # old: 283
    PinkDonutShirt = 278            # old: 284
    BlueDonutShirt = 279            # old: 285
    ChocolateDonutShirt = 280       # old: 286
    LemonDonutShirt = 281           # old: 287
    VanillaDonutShirt = 282         # old: 288
    BluePainter = 283               # old: 290
    RedPainter = 284                # old: 291
    GreenPainter = 285              # old: 292
    YellowPainter = 286             # old: 293
    ChefCoat = 287                  # old: 294
    NewYears2023 = 288              # old: 295
    ArmoredChestplate = 289         # old: 296
    RejectedSweater = 290           # old: 297
    HighRollersSuit = 291           # old: 298
    HighRollersProdigalSuit = 292   # old: 299
    CybertoonShirt = 293            # old: 300
    BroVinci = 294                  # old: 273


@defineItemSubtypeEnum(ItemType.Cosmetic_Shorts)
class ShortItemType(IntEnum):
    """
    Item subtype enum for Shorts.
    """
    ShortswithBelt = 1		                # old: 156
    BigPocketsShorts = 2		            # old: 157
    FeatherShorts = 3		                # old: 158
    SidestripedShorts = 4		            # old: 159
    AthleticShortsA = 5		                # old: 160
    FieryShorts = 6		                    # old: 161
    JeanShorts = 7		                    # old: 162
    ValentoonsPinkShorts = 8		        # old: 163
    ValentoonsGreenShorts = 9		        # old: 178
    JeanHeartShorts = 10		            # old: 179
    AthleticShortsB = 11		            # old: 164
    TealAndYellowShorts = 12		        # old: 165
    GreenAndYellowShorts = 13		        # old: 170
    IdesofMarchShorts = 14		            # old: 199
    SnowmanShortsA = 15		                # old: 174
    SnowflakeShorts = 16		            # old: 175
    PeppermintShorts = 17		            # old: 176
    FestiveWinterShorts = 18		        # old: 177
    SupertoonShorts = 19		            # old: 53
    GolfingShorts = 20		                # old: 206
    PleatedSkirt = 21		                # old: 0
    PolkaDotSkirt = 22		                # old: 1
    StripedSkirt = 23		                # old: 2
    BottomStripeSkirt = 24		            # old: 3
    FlowersSkirt = 25		                # old: 4
    JeanPocketsSkirt = 26		            # old: 7
    DenimSkirt = 27		                    # old: 8
    HighPocketsShorts = 28		            # old: 5
    FlowerShorts = 29		                # old: 6
    BlueAndGoldSkirt = 30		            # old: 10
    PinkBowSkirt = 31		                # old: 11
    BlueGreenStarSkirt = 32		            # old: 12
    RedAndWhiteHeartsSkirt = 33		        # old: 13
    ValentoonsHeartsSkirt = 34		        # old: 27
    JeanHeartSkirt = 35		                # old: 28
    RainbowSkirt = 36		                # old: 14
    LuckyCloverShorts = 37		            # old: 15
    IdesofMarchSkirt = 38		            # old: 48
    WesternSkirt = 39		                # old: 16
    ZestyWesternSkirt = 40		            # old: 17
    GoldBuckleShorts = 41		            # old: 167
    SilverBuckleShorts = 42		            # old: 168
    July4thShorts = 43		                # old: 169
    July4thSkirt = 44		                # old: 18
    DaisySkirt = 45		                    # old: 19
    BananaPeelShorts = 46		            # old: 20
    BikeHornShorts = 47		                # old: 21
    HypnoGogglesShorts = 48		            # old: 22
    SnowmanSkirt = 49		                # old: 23
    SnowflakesSkirt = 50		            # old: 24
    PeppermintSkirt = 51		            # old: 25
    FestiveWinterSkirt = 52		            # old: 26
    FishingShorts = 53		                # old: 180
    GardeningShorts = 54		            # old: 181
    PartyShorts = 55		                # old: 182
    CheckeredRacingShorts = 56		        # old: 183
    GoldfishShorts = 57		                # old: 184
    GreenPlaidGolfingShorts = 58		    # old: 185
    BeeShorts = 59		                    # old: 50
    SaveTheBuildingsShorts = 60		        # old: 188
    TrolleyShorts = 61		                # old: 189
    SpiderShorts = 62		                # old: 190
    SkeletoonShorts = 63		            # old: 191
    BlueRacingShorts = 64		            # old: 200
    IndigoRacingShorts = 65		            # old: 207
    TanGolfingShorts = 66		            # old: 208
    CheckeredGolfShorts = 67		        # old: 209
    DarkBlueRacingShorts = 68		        # old: 210
    RacingStripeShorts = 69		            # old: 211
    FishingSkirt = 70		                # old: 29
    GardeningSkirt = 71		                # old: 30
    PartySkirt = 72		                    # old: 31
    RedCheckeredSkirt = 73		            # old: 32
    GrassSkirt = 74		                    # old: 33
    PinkPlaidGolfSkirt = 75		            # old: 34
    BeeSkirt = 76		                    # old: 35
    SupertoonSkirt = 77		                # old: 36
    SaveTheBuildingsSkirt = 78		        # old: 37
    TrolleySkirt = 79		                # old: 38
    SkeletoonSkirt = 80		                # old: 39
    SpiderSkirt = 81		                # old: 40
    CogCrusherShorts = 82		            # old: 44
    SellbotCrusherShorts = 83		        # old: 45
    BlueCheckeredRacingSkirt = 84		    # old: 49
    StarryGolfingSkirt = 85		            # old: 56
    IndigoRacingSkirt = 86		            # old: 57
    RainbowGolfingSkirt = 87		        # old: 58
    BluePlaidGolfingSkirt = 88		        # old: 59
    DarkBlueRacingSkirt = 89		        # old: 60
    RacingStripeSkirt = 90		            # old: 61
    ScientistAShorts = 91		            # old: 41
    ScientistBShorts = 92		            # old: 42
    ScientistCShorts = 93		            # old: 43
    OvercoatVampireShorts = 94		        # old: 46
    TurtleShorts = 95		                # old: 47
    PirateShorts = 96		                # old: 51
    PirateSkirt = 97		                # old: 52
    VampireShorts = 98		                # old: 54
    ToonosaurShorts = 99		            # old: 55
    MeatballsShorts = 100		            # old: 62
    TrashcatsRagsShorts = 101		        # old: 63
    DrowsyDreamlandShorts = 102		        # old: 64
    BetaToonShorts = 103		            # old: 215
    BetaToonSkirt = 104		                # old: 65
    YOTTKnightShorts = 105		            # old: 216
    YOTTKnightSkirt = 106		            # old: 66
    BBSailorShorts = 107		            # old: 217
    BBSailorSkirt = 108		                # old: 67
    DGGardeningShorts = 109		            # old: 218
    DGGardeningSkirt = 110		            # old: 68
    TTCFirefighterShorts = 111		        # old: 219
    TTCFirefighterSkirt = 112		        # old: 69
    MMLBandShorts = 113		                # old: 70
    TeamBarnyardShorts = 114		        # old: 221
    TeamBarnyardSkirt = 115		            # old: 71
    TeamOutbackShorts = 116		            # old: 222
    TeamOutbackSkirt = 117		            # old: 72
    AAParkRangerShorts = 118		        # old: 73
    TBSnowflakeShorts = 119		            # old: 224
    TBSnowflakeSkirt = 120		            # old: 74
    AlchemistShorts = 121		            # old: 225
    AlchemistSkirt = 122		            # old: 75
    FrankentoonShorts = 123		            # old: 76
    SpacetoonShorts = 124		            # old: 77
    MadScientistShorts = 125		        # old: 78
    ClownShortsA = 126		                # old: 229
    ClownSkirtA = 127		                # old: 79
    WonderlandShorts = 128		            # old: 230
    WonderlandSkirt = 129		            # old: 80
    ReaperShorts = 130		                # old: 231
    ReaperSkirt = 131		                # old: 81
    ScarecrowShorts = 132		            # old: 232
    ScarecrowSkirt = 133		            # old: 82
    WitchShorts = 134		                # old: 233
    WitchSkirt = 135		                # old: 83
    GreenElfShorts = 136		            # old: 84
    RedElfShorts = 137		                # old: 85
    GingerbreadShorts = 138		            # old: 236
    GingerbreadSkirt = 139		            # old: 86
    PresentUniformShorts = 140		        # old: 237
    PresentUniformSkirt = 141		        # old: 87
    RagdollHumbleSkirt = 142		        # old: 88
    RagdollRegalSkirt = 143		            # old: 89
    RagdollTraditionalSkirt = 144		    # old: 90
    ReindeerSkirt = 145		                # old: 91
    ReindeerShorts = 146		            # old: 238
    VintageSnowShorts = 147		            # old: 92
    RagdollHumbleShorts = 148		        # old: 243
    RagdollRegalShorts = 149		        # old: 244
    RagdollTraditionalShorts = 150		    # old: 245
    TinHumbleShorts = 151		            # old: 93
    TinRegalShorts = 152		            # old: 94
    TinTraditionalShorts = 153		        # old: 95
    NY2019SuitShorts = 154		            # old: 246
    NY2019DressSkirt = 155		            # old: 96
    CupidShorts = 156		                # old: 247
    CupidSkirt = 157		                # old: 97
    WebstersShorts = 158		            # old: 248
    DoesSkirt = 159		                    # old: 98
    AviatorShorts = 160		                # old: 99
    WingsuitShorts = 161		            # old: 100
    SellbotSeekerSkirt = 162		        # old: 101
    SellbotSeekerShorts = 163		        # old: 102
    CashbotCatcherSkirt = 164		        # old: 103
    CashbotCatcherShorts = 165		        # old: 104
    LawbotLiberatorSkirt = 166		        # old: 105
    LawbotLiberatorShorts = 167		        # old: 106
    BossbotBasherSkirt = 168		        # old: 107
    BossbotBasherShorts = 169		        # old: 108
    OutbackUniformShorts = 170		        # old: 255
    OutbackUniformSkirt = 171		        # old: 109
    AlienShorts = 172		                # old: 110
    CandyCornShorts = 173		            # old: 111
    LawbotResistanceShorts = 174		    # old: 258
    LawbotResistanceSkirt = 175		        # old: 112
    RetroRobotShorts = 176		            # old: 113
    RidingHoodShorts = 177		            # old: 260
    RidingHoodSkirt = 178		            # old: 114
    NurseShorts = 179		                # old: 261
    NurseSkirt = 180		                # old: 115
    LazyBonesShorts = 181		            # old: 116
    SailorShorts = 182		                # old: 263
    SailorSkirt = 183		                # old: 117
    BlueSailorShorts = 184		            # old: 264
    BlueSailorSkirt = 185		            # old: 118
    CyanSailorShorts = 186		            # old: 265
    CyanSailorSkirt = 187		            # old: 119
    GreenSailorShorts = 188		            # old: 266
    GreenSailorSkirt = 189		            # old: 120
    OrangeSailorShorts = 190		        # old: 267
    OrangeSailorSkirt = 191		            # old: 121
    PinkSailorShorts = 192		            # old: 268
    PinkSailorSkirt = 193		            # old: 122
    PurpleSailorShorts = 194		        # old: 269
    PurpleSailorSkirt = 195		            # old: 123
    RedSailorShorts = 196		            # old: 270
    RedSailorSkirt = 197		            # old: 124
    BlackSailorShorts = 198		            # old: 271
    BlackSailorSkirt = 199		            # old: 125
    GoldenSailorShorts = 200		        # old: 272
    GoldenSailorSkirt = 201		            # old: 126
    TeamTreesShorts = 202		            # old: 127
    HomemadeRagdollShorts = 203		        # old: 274
    HomemadeRagdollSkirt = 204		        # old: 128
    HomemadeSoldierShorts = 205		        # old: 129
    RetroWinterShorts = 206		            # old: 276
    RetroWinterSkirt = 207		            # old: 130
    SnowmanShortsB = 208		            # old: 131
    NewYears2020Shorts = 209		        # old: 278
    NewYears2020Skirt = 210		            # old: 132
    AgentSevenSkirt = 211		            # old: 133
    StPattys2020Skirt = 212		            # old: 134
    StPattys2020Shorts = 213		        # old: 279
    ClownSkirtB = 214		                # old: 135
    ClownShortsB = 215		                # old: 280
    SevenStripedSkirt = 216		            # old: 136
    SevenStripedShorts = 217		        # old: 281
    TripleRainbowSkirt = 218		        # old: 137
    TripleRainbowShorts = 219		        # old: 282
    BoardbotShorts = 220		            # old: 138
    JesterSkirt = 221		                # old: 139
    JesterShorts = 222		                # old: 284
    BlackJesterSkirt = 223		            # old: 140
    BlackJesterShorts = 224		            # old: 285
    Easter2020Shorts = 225		            # old: 286
    Easter2020Skirt = 226		            # old: 141
    LawbotSuitPants = 227		            # old: 142
    CooktheCogsShorts = 228		            # old: 288
    CooktheCogsSkirt = 229		            # old: 143
    ExecutiveBoardbotShorts = 230		    # old: 144
    PhantoonShorts = 231		            # old: 145
    ToonsmasPastSkirt = 232		            # old: 146
    ToonsmasPastShorts = 233		        # old: 147
    ToonsmasPresentSkirt = 234		        # old: 148
    ToonsmasPresentShorts = 235		        # old: 149
    ToonsmasFutureSkirt = 236		        # old: 150
    ToonsmasFutureShorts = 237		        # old: 151
    NewYears2021Skirt = 238		            # old: 152
    NewYears2021Shorts = 239		        # old: 153
    TumblesShorts = 240		                # old: 154
    HallowopolisShorts = 241		        # old: 155
    DetectiveShorts = 242		            # old: 289
    FloralShorts = 243		                # old: 290
    BlueNewstoonShorts = 244		        # old: 291
    BlueNewstoonSkirt = 245		            # old: 292
    GrayNewstoonShorts = 246		        # old: 293
    GrayNewstoonSkirt = 247		            # old: 294
    ChupShorts = 248		                # old: 295
    ChupSkirt = 249		                    # old: 296
    NewYears2022Shorts = 250		        # old: 297
    NewYears2022Skirt = 251		            # old: 298
    DoctorToonShorts = 252		            # old: 299
    DoctorToonSkirt = 253		            # old: 300
    TrolleyEngineerShorts = 254		        # old: 302
    TrolleyEngineerSkirt = 255		        # old: 303
    StarstruckSkirt = 256		            # old: 304
    RetroShorts = 257		                # old: 305
    StarstruckShorts = 258		            # old: 306
    SleepwalkerShorts = 259		            # old: 307
    FruitPieShorts = 260		            # old: 308
    FruitPieSkirt = 261		                # old: 309
    GumballMachineShorts = 262		        # old: 310
    GumballMachineSkirt = 263		        # old: 311
    CardSuitShorts = 264		            # old: 312
    CardSuitSkirt = 265		                # old: 313
    PainterShorts = 266		                # old: 314
    PainterSkirt = 267		                # old: 315
    ChefShorts = 268		                # old: 316
    ChefSkirt = 269		                    # old: 317
    NewYears2023Shorts = 270		        # old: 318
    NewYears2023Skirt = 271		            # old: 319
    ArmoredPants = 272		                # old: 320
    ArmoredSkirt = 273		                # old: 321
    HighRollersSuitShorts = 274		        # old: 322
    HighRollersProdigalSuitShorts = 275		# old: 323
    CybertoonShorts = 276		            # old: 324
    CybertoonSkirt = 277		            # old: 325
    BroVinci = 278                          # old: 301


@defineItemSubtypeEnum(ItemType.Cosmetic_Hat)
class HatItemType(IntEnum):
    """
    Item subtype enum for Hats.
    """
    GreenBallcap = 1                # old: [1, 0, 0], hat
    SafariHatBeige = 2              # old: [2, 0, 0], hat
    SafariHatBrown = 3              # old: [2, 5, 0], hat
    SafariHatGreen = 4              # old: [2, 6, 0], hat
    PinkHearts = 5                  # old: [4, 0, 0], hat
    YellowHearts = 6                # old: [4, 3, 0], hat
    TophatBlack = 7                 # old: [5, 0, 0], hat
    TophatBlue = 8                  # old: [5, 4, 0], hat
    AnvilHat = 9                    # old: [6, 0, 0], hat
    FlowerHat = 10                  # old: [7, 0, 0], hat
    SandbagHat = 11                 # old: [8, 0, 0], hat
    WeightHat = 12                  # old: [9, 0, 0], hat
    FezHat = 13                     # old: [10, 0, 0], hat
    GolfHat = 14                    # old: [11, 0, 0], hat
    PartyHat = 15                   # old: [12, 0, 0], hat
    PartyHatToon = 16               # old: [12, 19, 0], hat
    FancyHat = 17                   # old: [13, 0, 0], hat
    Crown = 18                      # old: [14, 0, 0], hat
    BlueBallcap = 19                # old: [1, 7, 0], hat
    OrangeBallcap = 20              # old: [1, 8, 0], hat
    CowboyHat = 21                  # old: [15, 0, 0], hat
    PirateHat = 22                  # old: [16, 0, 0], hat
    PropellerHat = 23               # old: [17, 0, 0], hat
    FishingHat = 24                 # old: [18, 0, 0], hat
    Sombrero = 25                   # old: [19, 0, 0], hat
    StrawHat = 26                   # old: [20, 0, 0], hat
    Antenna = 27                    # old: [22, 0, 0], hat
    BeehiveHair = 28                # old: [23, 0, 0], hat
    BowlerHat = 29                  # old: [24, 0, 0], hat
    ChefHat = 30                    # old: [25, 0, 0], hat
    DetectiveHat = 31               # old: [26, 0, 0], hat
    FancyFeatherHat = 32            # old: [27, 0, 0], hat
    Fedora = 33                     # old: [28, 0, 0], hat
    BandConductorHat = 34           # old: [29, 0, 0], hat
    Sweatband = 35                  # old: [30, 0, 0], hat
    Pompadour = 36                  # old: [31, 0, 0], hat
    ArcherHat = 37                  # old: [33, 0, 0], hat
    RomanHelmet = 38                # old: [34, 0, 0], hat
    WebbedAntenna = 39              # old: [35, 0, 0], hat
    Tiara = 40                      # old: [36, 0, 0], hat
    VikingHelmet = 41               # old: [37, 0, 0], hat
    WitchHat = 42                   # old: [38, 0, 0], hat
    WizardHat = 43                  # old: [39, 0, 0], hat
    ConquistadorHelmet = 44         # old: [40, 0, 0], hat
    FirefighterHelmet = 45          # old: [41, 0, 0], hat
    TinFoilHat = 46                 # old: [42, 0, 0], hat
    MinerHat = 47                   # old: [43, 0, 0], hat
    NapoleonHat = 48                # old: [44, 0, 0], hat
    PilotCap = 49                   # old: [45, 0, 0], hat
    CopHat = 50                     # old: [46, 0, 0], hat
    RainbowWig = 51                 # old: [47, 0, 0], hat
    YellowBallcap = 52              # old: [1, 13, 0], hat
    RedBallcap = 53                 # old: [1, 14, 0], hat
    AquaBallcap = 54                # old: [1, 15, 0], hat
    SailorHat = 55                  # old: [48, 0, 0], hat
    SambaHat = 56                   # old: [49, 0, 0], hat
    BobbyHat = 57                   # old: [50, 0, 0], hat
    JugheadHat = 58                 # old: [51, 0, 0], hat
    PurpleBallcap = 59              # old: [1, 17, 0], hat
    WinterHat = 60                  # old: [52, 0, 0], hat
    ToonosaurHat = 61               # old: [54, 0, 0], hat
    JamboreeHat = 62                # old: [55, 0, 0], hat
    BirdHat = 63                    # old: [56, 0, 0], hat
    PinkBow = 64                    # old: [3, 0, 0], hat
    RedBow = 65                     # old: [3, 1, 0], hat
    PurpleBow = 66                  # old: [3, 2, 0], hat
    SunHat = 67                     # old: [21, 0, 0], hat
    YellowBow = 68                  # old: [3, 9, 0], hat
    CheckerBow = 69                 # old: [3, 10, 0], hat
    LightRedBow = 70                # old: [3, 11, 0], hat
    RainbowBow = 71                 # old: [3, 12, 0], hat
    PrincessHat = 72                # old: [32, 0, 0], hat
    PinkDotBow = 73                 # old: [3, 16, 0], hat
    GreenCheckerBow = 74            # old: [3, 18, 0], hat
    Bandana = 75                    # old: [53, 0, 0], hat
    SpaceHelm = 76                  # old: [57, 0, 0], hat
    BatBow = 77                     # old: [58, 0, 0], hat
    CauldronHat = 78                # old: [59, 0, 0], hat
    ElectricBolts = 79              # old: [60, 0, 0], hat
    PumpkinBucket = 80              # old: [61, 0, 0], hat
    ScarecrowHat = 81               # old: [62, 0, 0], hat
    WizardBlack = 82                # old: [39, 23, 0], hat
    WizardPink = 83                 # old: [39, 26, 0], hat
    WizardRed = 84                  # old: [39, 25, 0], hat
    WizardGreen = 85                # old: [39, 24, 0], hat
    WizardBlue = 86                 # old: [39, 22, 0], hat
    FrankHead = 87                  # old: [63, 0, 0], hat
    AlchemistGoggles = 88           # old: [64, 0, 0], hat
    TiwBow = 89                     # old: [3, 28, 0], hat
    BobbleBlue = 90                 # old: [65, 0, 0], hat
    BobbleGreen = 91                # old: [66, 0, 0], hat
    BobbleGrey = 92                 # old: [67, 0, 0], hat
    BobblePink = 93                 # old: [68, 0, 0], hat
    BobbleRainbow = 94              # old: [69, 0, 0], hat
    BobbleRed = 95                  # old: [70, 0, 0], hat
    SantaRed = 96                   # old: [71, 0, 0], hat
    SantaRainbow = 97               # old: [72, 0, 0], hat
    ElfGreen = 98                   # old: [73, 0, 0], hat
    ElfRed = 99                     # old: [74, 0, 0], hat
    StarHat = 100                   # old: [75, 0, 0], hat
    TinHumble = 101                 # old: [76, 0, 0], hat
    TinRegal = 102                  # old: [77, 0, 0], hat
    TinTradi = 103                  # old: [78, 0, 0], hat
    RagdollHumble = 104             # old: [79, 0, 0], hat
    RagdollTradi = 105              # old: [80, 0, 0], hat
    RagdollRegal = 106              # old: [81, 0, 0], hat
    Antlers = 107                   # old: [82, 0, 0], hat
    DoeBeanie = 108                 # old: [83, 0, 0], hat
    WebsterBookhat = 109            # old: [84, 0, 0], hat
    Umbrella = 110                  # old: [85, 0, 0], hat
    AviatorHat = 111                # old: [86, 0, 0], hat
    CakeHat = 112                   # old: [87, 0, 0], hat
    OutbackHat = 113                # old: [88, 0, 0], hat
    OutbackCorkhat = 114            # old: [89, 0, 0], hat
    OutbackGeckohat = 115           # old: [90, 0, 0], hat
    AlienHat = 116                  # old: [91, 0, 0], hat
    AngelHalo = 117                 # old: [92, 0, 0], hat
    AngelHaloBlue = 118             # old: [92, 29, 0], hat
    AngelHaloGreen = 119            # old: [92, 30, 0], hat
    AngelHaloOrange = 120           # old: [92, 31, 0], hat
    AngelHaloPurple = 121           # old: [92, 32, 0], hat
    AngelHaloRed = 122              # old: [92, 33, 0], hat
    DemonHorns = 123                # old: [93, 0, 0], hat
    DemonHornsBlue = 124            # old: [93, 29, 0], hat
    DemonHornsGreen = 125           # old: [93, 30, 0], hat
    DemonHornsOrange = 126          # old: [93, 31, 0], hat
    DemonHornsPurple = 127          # old: [93, 32, 0], hat
    DemonHornsRed = 128             # old: [93, 33, 0], hat
    RidinghoodHood = 129            # old: [94, 0, 0], hat
    Robophones = 130                # old: [95, 0, 0], hat
    NurseHat = 131                  # old: [48, 34, 0], hat
    SpinDoctorBand = 132            # old: [96, 35, 0], hat
    CandycornBow = 133              # old: [3, 36, 0], hat
    AngelHaloYellow = 134           # old: [92, 37, 0], hat
    DemonHornsYellow = 135          # old: [93, 37, 0], hat
    BowlingBall = 136               # old: [97, 0, 0], hat
    FruitPie = 137                  # old: [98, 0, 0], hat
    RagdollHat = 138                # old: [99, 0, 0], hat
    SkiHelmet = 139                 # old: [100, 0, 0], hat
    SkiHelmetBlue = 140             # old: [100, 38, 0], hat
    SkiHelmetGreen = 141            # old: [100, 39, 0], hat
    SkiHelmetGray = 142             # old: [100, 40, 0], hat
    SkiHelmetPink = 143             # old: [100, 41, 0], hat
    SkiHelmetRainbow = 144          # old: [100, 42, 0], hat
    SkiHelmetRed = 145              # old: [100, 43, 0], hat
    SnowmanHat = 146                # old: [101, 0, 0], hat
    SoldierHat = 147                # old: [102, 0, 0], hat
    TvHat = 148                     # old: [103, 0, 0], hat
    SevenFedora = 149               # old: [28, 44, 0], hat
    StpatsTopLucky = 150            # old: [104, 0, 0], hat
    StpatsTopTart = 151             # old: [105, 0, 0], hat
    StpatsBand = 152                # old: [106, 0, 0], hat
    StpatsClip = 153                # old: [107, 0, 0], hat
    RainbowPhones = 154             # old: [108, 0, 0], hat
    ClownHat = 155                  # old: [109, 0, 0], hat
    JesterHat = 156                 # old: [110, 45, 0], hat
    JesterBHat = 157                # old: [110, 46, 0], hat
    EasterBeanie = 158              # old: [111, 0, 0], hat
    AtticusHat = 159                # old: [112, 47, 0], hat
    Diploma = 160                   # old: [113, 0, 0], hat
    Grill = 161                     # old: [114, 48, 0], hat
    LeafHat = 162                   # old: [115, 0, 0], hat
    CandleHat = 163                 # old: [116, 0, 0], hat
    PresentBand = 164               # old: [117, 0, 0], hat
    FutureHood = 165                # old: [118, 0, 0], hat
    PlantHat = 166                  # old: [119, 0, 0], hat
    NewstoonGrayBow = 167           # old: [120, 0, 0], hat
    HwGibus = 168                   # old: [121, 0, 0], hat
    HatNumber1 = 169                # old: [122, 0, 0], hat
    RibbonBlue = 170                # old: [3, 49, 0], hat
    BandanaDeluxe = 171             # old: [123, 0, 0], hat
    BrovinciHair = 172              # old: [124, 0, 0], hat
    HatIcecube = 173                # old: [125, 0, 0], hat
    HatSmartcap = 174               # old: [126, 0, 0], hat
    HatClownbeanie = 175            # old: [127, 0, 0], hat
    HatBananahat = 176              # old: [128, 0, 0], hat
    HatWingsuitHelmet = 177         # old: [129, 0, 0], hat
    HatEngineerCap = 178            # old: [130, 0, 0], hat
    DonuthatPink = 179              # old: [131, 0, 0], hat
    DonuthatBlue = 180              # old: [131, 50, 0], hat
    DonuthatChocolate = 181         # old: [131, 51, 0], hat
    DonuthatLemon = 182             # old: [131, 52, 0], hat
    DonuthatVanilla = 183           # old: [131, 53, 0], hat
    CrullerBeret = 184              # old: [132, 0, 0], hat
    FlowercrownWhite = 185          # old: [133, 0, 0], hat
    FlowercrownBlue = 186           # old: [133, 54, 0], hat
    FlowercrownCyan = 187           # old: [133, 55, 0], hat
    FlowercrownCyanpurple = 188     # old: [133, 56, 0], hat
    FlowercrownGreen = 189          # old: [133, 57, 0], hat
    FlowercrownOrange = 190         # old: [133, 58, 0], hat
    FlowercrownOrangepink = 191     # old: [133, 59, 0], hat
    FlowercrownPink = 192           # old: [133, 60, 0], hat
    FlowercrownPinkblue = 193       # old: [133, 61, 0], hat
    FlowercrownPurple = 194         # old: [133, 62, 0], hat
    FlowercrownRed = 195            # old: [133, 63, 0], hat
    FlowercrownRedyellow = 196      # old: [133, 64, 0], hat
    FlowercrownYellow = 197         # old: [133, 65, 0], hat
    RosecrownWhite = 198            # old: [134, 0, 0], hat
    RosecrownBlue = 199             # old: [134, 66, 0], hat
    RosecrownCyan = 200             # old: [134, 67, 0], hat
    RosecrownGreen = 201            # old: [134, 68, 0], hat
    RosecrownOrange = 202           # old: [134, 69, 0], hat
    RosecrownPink = 203             # old: [134, 70, 0], hat
    RosecrownPurple = 204           # old: [134, 71, 0], hat
    RosecrownRed = 205              # old: [134, 72, 0], hat
    RosecrownYellow = 206           # old: [134, 73, 0], hat
    HatChainsaw = 207               # old: [135, 0, 0], hat
    HatMultislacker = 208           # old: [136, 0, 0], hat
    HatTreekiller = 209             # old: [137, 0, 0], hat
    HatFeatherbedder = 210          # old: [138, 0, 0], hat
    HatNightcap = 211               # old: [139, 0, 0], hat
    HatBlackberet = 212             # old: [140, 0, 0], hat
    HatGumballhat = 213             # old: [141, 0, 0], hat
    HatCardcrown = 214              # old: [142, 0, 0], hat
    HatCardtophat = 215             # old: [143, 0, 0], hat
    HatButter = 216                 # old: [144, 0, 0], hat
    HatRainmakerDepression = 217    # old: [145, 0, 0], hat
    HatGumballHairbow = 218         # old: [146, 0, 0], hat
    HatFirestarter = 219            # old: [147, 0, 0], hat
    PainterBeret = 220              # old: [148, 0, 0], hat
    HatGumballHairbowB = 221        # old: [146, 74, 0], hat
    HatGumballHairbowBr = 222       # old: [146, 75, 0], hat
    HatGumballHairbowG = 223        # old: [146, 76, 0], hat
    HatGumballHairbowOr = 224       # old: [146, 77, 0], hat
    HatGumballHairbowP = 225        # old: [146, 78, 0], hat
    HatGumballHairbowPu = 226       # old: [146, 79, 0], hat
    HatGumballHairbowRb = 227       # old: [146, 80, 0], hat
    HatWitchhunter = 228            # old: [149, 0, 0], hat
    HatGoonPatrolYellow = 229       # old: [150, 0, 0], hat
    HatGoonPatrolOrange = 230       # old: [150, 81, 0], hat
    HatGoonPatrolRed = 231          # old: [150, 82, 0], hat
    HatGoonPatrolPurple = 232       # old: [150, 83, 0], hat
    HatGoonSecurity = 233           # old: [151, 0, 0], hat
    HatForeman = 234                # old: [112, 84, 0], hat
    HatCogBucket = 235              # old: [152, 0, 0], hat
    HatLowBaller = 236              # old: [153, 0, 0], hat
    HatHighRoller = 237             # old: [154, 0, 0], hat
    GbHairbowBlack = 238            # old: [120, 85, 0], hat
    GbHairbowBlackwhite = 239       # old: [120, 86, 0], hat
    GbHairbowBlue = 240             # old: [120, 87, 0], hat
    GbHairbowGray = 241             # old: [120, 88, 0], hat
    GbHairbowGreen = 242            # old: [120, 89, 0], hat
    GbHairbowOrange = 243           # old: [120, 90, 0], hat
    GbHairbowPink = 244             # old: [120, 91, 0], hat
    GbHairbowPinkblack = 245        # old: [120, 92, 0], hat
    GbHairbowPolkadot = 246         # old: [120, 93, 0], hat
    GbHairbowPurple = 247           # old: [120, 94, 0], hat
    GbHairbowPurpleorange = 248     # old: [120, 95, 0], hat
    GbHairbowRed = 249              # old: [120, 96, 0], hat
    GbHairbowYellow = 250           # old: [120, 97, 0], hat
    GbHairbowYellowblack = 251      # old: [120, 98, 0], hat
    PrideHairbowAce = 252           # old: [120, 99, 0], hat
    PrideHairbowAro = 253           # old: [120, 100, 0], hat
    PrideHairbowBi = 254            # old: [120, 101, 0], hat
    PrideHairbowGay = 255           # old: [120, 102, 0], hat
    PrideHairbowGenderfluid = 256   # old: [120, 103, 0], hat
    PrideHairbowLesbian = 257       # old: [120, 104, 0], hat
    PrideHairbowLgbt = 258          # old: [120, 105, 0], hat
    PrideHairbowNb = 259            # old: [120, 106, 0], hat
    PrideHairbowPan = 260           # old: [120, 107, 0], hat
    PrideHairbowTrans = 261         # old: [120, 108, 0], hat
    HatCyberpunk = 262              # old: [155, 0, 0], hat
    MuzzleRose = 263                # old: [53, 0, 0], glasses
    PainterBrush = 264              # old: [54, 0, 0], glasses


@defineItemSubtypeEnum(ItemType.Cosmetic_Glasses)
class GlassesItemType(IntEnum):
    """
    Item subtype enum for Glasses.
    """
    RoundGlasses = 1            # old: [1, 0, 0], glasses
    WhiteMiniBlinds = 2         # old: [2, 0, 0], glasses
    HollywoodShades = 3         # old: [3, 0, 0], glasses
    StarGlasses = 4             # old: [4, 0, 0], glasses
    MovieGlasses = 5            # old: [5, 0, 0], glasses
    AviatorGlasses = 6          # old: [6, 0, 0], glasses
    CelebShades = 7             # old: [9, 0, 0], glasses
    ScubaMask = 8               # old: [10, 0, 0], glasses
    Goggles = 9                 # old: [11, 0, 0], glasses
    GrouchoGlasses = 10         # old: [12, 0, 0], glasses
    HeartGlasses = 11           # old: [13, 0, 0], glasses
    BugeyeGlasses = 12          # old: [14, 0, 0], glasses
    STMaskBlack = 13            # old: [15, 0, 0], glasses
    STMaskBlue = 14             # old: [15, 1, 0], glasses
    CarnivaleMaskBlue = 15      # old: [16, 0, 0], glasses
    CarnivaleMaskPurple = 16    # old: [16, 2, 0], glasses
    CarnivaleMaskAqua = 17      # old: [16, 3, 0], glasses
    Monocle = 18                # old: [17, 0, 0], glasses
    SmoochGlasses = 19          # old: [18, 0, 0], glasses
    SquareFrames = 20           # old: [19, 0, 0], glasses
    CateyeGlasses = 21          # old: [7, 0, 0], glasses
    NerdGlasses = 22            # old: [8, 0, 0], glasses
    AlienEyes = 23              # old: [21, 0, 0], glasses
    EyepatchSkull = 24          # old: [20, 0, 0], glasses
    EyepatchGem = 25            # old: [20, 4, 0], glasses
    EyepatchLimey = 26          # old: [20, 5, 0], glasses
    SpiderGlasses = 27          # old: [22, 0, 0], glasses
    Hypno = 28                  # old: [23, 0, 0], glasses
    SnowGogglesBlue = 29        # old: [24, 0, 0], glasses
    SnowGogglesGreen = 30       # old: [25, 0, 0], glasses
    SnowGogglesGrey = 31        # old: [26, 0, 0], glasses
    SnowGogglesPink = 32        # old: [27, 0, 0], glasses
    SnowGogglesRainbow = 33     # old: [28, 0, 0], glasses
    SnowGogglesRed = 34         # old: [29, 0, 0], glasses
    SnowGogglesVintage = 35     # old: [30, 0, 0], glasses
    Glasses2019 = 36            # old: [31, 0, 0], glasses
    FlunkyGlasses = 37          # old: [32, 0, 0], glasses
    EyeSpring = 38              # old: [33, 0, 0], glasses
    FlightGoggles = 39          # old: [34, 0, 0], glasses
    OutbackSunnyglasses = 40    # old: [35, 0, 0], glasses
    Hypno2019 = 41              # old: [23, 6, 0], glasses
    XGlassesB = 42              # old: [36, 7, 0], glasses
    XGlassesGo = 43             # old: [36, 8, 0], glasses
    XGlassesGr = 44             # old: [36, 9, 0], glasses
    XGlassesRa = 45             # old: [36, 10, 0], glasses
    XGlassesRed = 46            # old: [36, 11, 0], glasses
    GiftGlasses = 47            # old: [37, 0, 0], glasses
    GiftGlassesBlue = 48        # old: [37, 12, 0], glasses
    GiftGlassesCyan = 49        # old: [37, 13, 0], glasses
    GiftGlassesGreen = 50       # old: [37, 14, 0], glasses
    GiftGlassesOrange = 51      # old: [37, 15, 0], glasses
    GiftGlassesPink = 52        # old: [37, 16, 0], glasses
    GiftGlassesPurple = 53      # old: [37, 17, 0], glasses
    GiftGlassesRed = 54         # old: [37, 18, 0], glasses
    GiftGlassesYellow = 55      # old: [37, 19, 0], glasses
    Glasses2020 = 56            # old: [38, 0, 0], glasses
    SevenGlasses = 57           # old: [23, 20, 0], glasses
    VinnyStache = 58            # old: [39, 21, 0], glasses
    ChairGlasses = 59           # old: [40, 22, 0], glasses
    HypnoBlue = 60              # old: [23, 23, 0], glasses
    HypnoLightblue = 61         # old: [23, 24, 0], glasses
    HypnoOrange = 62            # old: [23, 25, 0], glasses
    HypnoPink = 63              # old: [23, 26, 0], glasses
    HypnoYellow = 64            # old: [23, 27, 0], glasses
    HypnoPurple = 65            # old: [23, 28, 0], glasses
    HypnoDarkpurple = 66        # old: [23, 29, 0], glasses
    HypnoRainbow = 67           # old: [23, 30, 0], glasses
    OrnGlassesBlack = 68        # old: [41, 31, 0], glasses
    OrnGlassesBlue = 69         # old: [41, 32, 0], glasses
    OrnGlassesCyan = 70         # old: [41, 33, 0], glasses
    OrnGlassesGreen = 71        # old: [41, 34, 0], glasses
    OrnGlassesOrange = 72       # old: [41, 35, 0], glasses
    OrnGlassesPink = 73         # old: [41, 36, 0], glasses
    OrnGlassesPurple = 74       # old: [41, 37, 0], glasses
    OrnGlassesRainbow = 75      # old: [41, 38, 0], glasses
    OrnGlassesRed = 76          # old: [41, 39, 0], glasses
    OrnGlassesWhite = 77        # old: [41, 40, 0], glasses
    OrnGlassesYellow = 78       # old: [41, 41, 0], glasses
    HwtownMask = 79             # old: [42, 0, 0], glasses
    CountMask = 80              # old: [43, 0, 0], glasses
    Glasses2022 = 81            # old: [44, 0, 0], glasses
    ScifiVisor = 82             # old: [45, 0, 0], glasses
    BrovinciGlasses = 83        # old: [46, 0, 0], glasses
    GlassesMouthpiece = 84      # old: [47, 0, 0], glasses
    GlassesFunky = 85           # old: [48, 0, 0], glasses
    DdlSleepingmask = 86        # old: [49, 0, 0], glasses
    GlassesPacesetter = 87      # old: [50, 0, 0], glasses
    GlassesCardblack = 88       # old: [51, 0, 0], glasses
    GlassesCardred = 89         # old: [52, 0, 0], glasses
    CookieGlasses = 91          # old: [55, 0, 0], glasses
    LowBallerGlasses = 92       # old: [56, 0, 0], glasses
    CyberpunkGlasses = 93       # old: [57, 0, 0], glasses


@defineItemSubtypeEnum(ItemType.Cosmetic_Backpack)
class BackpackItemType(IntEnum):
    """
    Item subtype enum for Backpacks.
    """
    BlueBackpack = 1                    # old: [1, 0, 0], backpack
    OrangeBackpack = 2                  # old: [1, 1, 0], backpack
    PurpleBackpack = 3                  # old: [1, 2, 0], backpack
    RedDotBackpack = 4                  # old: [1, 3, 0], backpack
    YellowDotBackpack = 5               # old: [1, 4, 0], backpack
    BatWings = 6                        # old: [2, 0, 0], backpack
    BeeWings = 7                        # old: [3, 0, 0], backpack
    DragonflyWings = 8                  # old: [4, 0, 0], backpack
    ScubaTank = 9                       # old: [5, 0, 0], backpack
    SharkFin = 10                       # old: [6, 0, 0], backpack
    AngelWingsClassic = 11              # old: [7, 0, 0], backpack
    AngelWingsClassicRainbow = 12       # old: [7, 5, 0], backpack
    ToyBackpack = 13                    # old: [8, 0, 0], backpack
    ButterflyWings = 14                 # old: [9, 0, 0], backpack
    PixieWings = 15                     # old: [9, 6, 0], backpack
    DragonWings = 16                    # old: [10, 0, 0], backpack
    Jetpack = 17                        # old: [11, 0, 0], backpack
    BugBackpack = 18                    # old: [12, 0, 0], backpack
    PlushBearPack = 19                  # old: [13, 0, 0], backpack
    BirdWings = 20                      # old: [14, 0, 0], backpack
    PlushCatPack = 21                   # old: [15, 0, 0], backpack
    PlushDogPack = 22                   # old: [16, 0, 0], backpack
    PlaneWings = 23                     # old: [17, 0, 0], backpack
    PirateSword = 24                    # old: [18, 0, 0], backpack
    SuperToonCape = 25                  # old: [19, 0, 0], backpack
    VampireCape = 26                    # old: [20, 0, 0], backpack
    ToonosaurTail = 27                  # old: [21, 0, 0], backpack
    JamboreePack = 28                   # old: [22, 0, 0], backpack
    GagAttackPack = 29                  # old: [23, 0, 0], backpack
    CogPack = 30                        # old: [24, 0, 0], backpack
    SpaceBack = 31                      # old: [25, 0, 0], backpack
    WitchBroom = 32                     # old: [26, 0, 0], backpack
    ReaperCape = 33                     # old: [27, 0, 0], backpack
    DraculaCape = 34                    # old: [28, 0, 0], backpack
    TrickortreatBack = 35               # old: [29, 0, 0], backpack
    PotionBack = 36                     # old: [30, 0, 0], backpack
    TinTradi = 37                       # old: [31, 0, 0], backpack
    TinHumble = 38                      # old: [32, 0, 0], backpack
    TinRegal = 39                       # old: [33, 0, 0], backpack
    RagdollHumble = 40                  # old: [34, 0, 0], backpack
    RagdollRegal = 41                   # old: [35, 0, 0], backpack
    RagdollTradi = 42                   # old: [36, 0, 0], backpack
    PresentsSack = 43                   # old: [37, 0, 0], backpack
    Snowboard = 44                      # old: [38, 0, 0], backpack
    CandyCane = 45                      # old: [39, 0, 0], backpack
    CupidBow = 46                       # old: [41, 0, 0], backpack
    CupidBowQuiver = 47                 # old: [42, 0, 0], backpack
    PropPack = 48                       # old: [44, 0, 0], backpack
    Kite = 49                           # old: [45, 0, 0], backpack
    Hangglider = 50                     # old: [46, 0, 0], backpack
    Telescope = 51                      # old: [48, 0, 0], backpack
    OutbackBackpack = 52                # old: [50, 0, 0], backpack
    OutbackBoomerang = 54               # old: [52, 0, 0], backpack
    OutbackDidgeridoo = 55              # old: [53, 0, 0], backpack
    AlienBackpack = 56                  # old: [54, 0, 0], backpack
    AngelWings = 57                     # old: [55, 0, 0], backpack
    AngelWingsBlue = 58                 # old: [55, 7, 0], backpack
    AngelWingsGreen = 59                # old: [55, 8, 0], backpack
    AngelWingsOrange = 60               # old: [55, 9, 0], backpack
    AngelWingsPurple = 61               # old: [55, 10, 0], backpack
    AngelWingsRed = 62                  # old: [55, 11, 0], backpack
    DemonWings = 63                     # old: [56, 0, 0], backpack
    DemonWingsBlue = 64                 # old: [56, 7, 0], backpack
    DemonWingsGreen = 65                # old: [56, 8, 0], backpack
    DemonWingsOrange = 66               # old: [56, 9, 0], backpack
    DemonWingsPurple = 67               # old: [56, 10, 0], backpack
    DemonWingsRed = 68                  # old: [56, 11, 0], backpack
    RidinghoodCloak = 69                # old: [57, 0, 0], backpack
    AngelWingsYellow = 70               # old: [55, 14, 0], backpack
    DemonWingsYellow = 71               # old: [56, 14, 0], backpack
    StabPack = 72                       # old: [62, 34, 0], backpack
    GavelPack = 73                      # old: [63, 33, 0], backpack
    CjPack = 74                        # old: [64, 35, 0], backpack
    StonePack = 75                     # old: [65, 36, 0], backpack
    TntPack = 76                       # old: [66, 0, 0], backpack
    RagdollHomemadeBow = 77            # old: [34, 37, 0], backpack
    SoldierHomemadeKey = 78            # old: [31, 38, 0], backpack
    SeltzerPack = 79                   # old: [68, 0, 0], backpack
    MiniMag = 80                       # old: [70, 40, 0], backpack
    Taser = 81                         # old: [71, 0, 0], backpack
    FusionPack = 82                    # old: [72, 0, 0], backpack
    ChairPack = 83                     # old: [74, 41, 0], backpack
    BunnyBackpack = 84                 # old: [76, 0, 0], backpack
    Spatula = 85                       # old: [77, 44, 0], backpack
    Firework = 86                      # old: [78, 45, 0], backpack
    Spellbook = 87                     # old: [64, 46, 0], backpack
    Tombstone = 88                     # old: [65, 47, 0], backpack
    CandyPumpkin = 89                  # old: [79, 0, 0], backpack
    PlatePack = 90                     # old: [80, 0, 0], backpack
    Extinguisher = 91                  # old: [81, 0, 0], backpack
    PresentCorn = 92                   # old: [82, 0, 0], backpack
    FutureWing = 93                    # old: [83, 0, 0], backpack
    FutureCloak = 94                   # old: [84, 0, 0], backpack
    FutureWingCloak = 95               # old: [85, 0, 0], backpack
    HwtownCape = 96                    # old: [87, 0, 0], backpack
    SadsPack = 97                      # old: [88, 0, 0], backpack
    NewstoonSuitcase = 98              # old: [91, 0, 0], backpack
    NewstoonCamera = 99                # old: [92, 0, 0], backpack
    PrideCapeLgbt = 100                 # old: [94, 0, 0], backpack
    PrideCapeTrans = 101                # old: [94, 62, 0], backpack
    PrideCapeLesbian = 102              # old: [94, 63, 0], backpack
    PrideCapePan = 103                  # old: [94, 64, 0], backpack
    PrideCapeBi = 104                   # old: [94, 65, 0], backpack
    PrideCapeNb = 105                   # old: [94, 66, 0], backpack
    PrideCapeAce = 106                  # old: [94, 67, 0], backpack
    PrideCapeFluid = 107                # old: [94, 68, 0], backpack
    PrideCapeAro = 108                  # old: [94, 69, 0], backpack
    PrideCape = 109                     # old: [94, 87, 0], backpack
    DoodlePack = 110                    # old: [95, 0, 0], backpack
    BackpackMoneybag = 111              # old: [97, 0, 0], backpack
    BackpackPitchfork = 112             # old: [98, 0, 0], backpack
    BackpackWingsuitWings = 113         # old: [99, 0, 0], backpack
    BackpackPillow = 115                # old: [100, 0, 0], backpack
    BackpackMajorplayer = 116           # old: [102, 0, 0], backpack
    BackpackFirestarter = 117           # old: [103, 0, 0], backpack
    BackpackGatekeeper = 118            # old: [104, 0, 0], backpack
    BackpackFruitbasket = 119           # old: [105, 0, 0], backpack
    BackpackRetrobag = 120              # old: [106, 0, 0], backpack
    EeBreadbag = 121                    # old: [107, 0, 0], backpack
    EePaddle = 122                      # old: [109, 0, 0], backpack
    PainterPalette = 123                # old: [110, 0, 0], backpack
    DaShredderOmg = 125                 # old: [111, 0, 0], backpack
    FactoryGear = 126                   # old: [112, 0, 0], backpack
    CyberpunkBackpack = 127             # old: [113, 0, 0], backpack


@defineItemSubtypeEnum(ItemType.Cosmetic_Shoes)
class ShoeItemType(IntEnum):
    """
    Item subtype enum for Shoes.
    """
    GreenAthleticShoes = 1	    # old: [1, 0, 0]
    RedAthleticShoes = 2	    # old: [1, 1, 0]
    GreenToonBoots = 3		    # old: [3, 2, 0]
    GreenSneakers = 4		    # old: [2, 3, 0]
    BoatShoes = 5			    # old: [1, 6, 0]
    YellowAthleticShoes = 6	    # old: [1, 7, 0]
    BlackSneakers = 7		    # old: [2, 8, 0]
    WhiteSneakers = 8		    # old: [2, 9, 0]
    PinkSneakers = 9		    # old: [2, 10, 0]
    CowboyBoots = 10		    # old: [3, 11, 0]
    GreenHiTops = 11		    # old: [2, 13, 0]
    RedSuperToonBoots = 12	    # old: [3, 16, 0]
    GreenTennisShoes = 13	    # old: [1, 17, 0]
    PinkTennisShoes = 14	    # old: [1, 18, 0]
    RedSneakers = 15		    # old: [2, 19, 0]
    AquaToonBoots = 16		    # old: [3, 20, 0]
    BrownToonBoots = 17		    # old: [3, 21, 0]
    YellowToonBoots = 18	    # old: [3, 22, 0]
    Loafers = 19			    # old: [1, 28, 0]
    MotorcycleBoots = 20		# old: [3, 30, 0]
    Oxfords = 21			    # old: [1, 31, 0]
    PinkRainBoots = 22		    # old: [3, 32, 0]
    JollyBoots = 23			    # old: [3, 33, 0]
    BeigeWinterBoots = 24	    # old: [3, 34, 0]
    PinkWinterBoots = 25	    # old: [3, 35, 0]
    WorkBoots = 26			    # old: [2, 36, 0]
    YellowSneakers = 27		    # old: [2, 37, 0]
    PinkToonBoots = 28		    # old: [3, 38, 0]
    PinkHiTops = 29			    # old: [2, 39, 0]
    RedDotsRainBoots = 30	    # old: [3, 40, 0]
    PurpleTennisShoes = 31	    # old: [1, 41, 0]
    VioletTennisShoes = 32	    # old: [1, 42, 0]
    YellowTennisShoes = 33	    # old: [1, 43, 0]
    BlueRainBoots = 34		    # old: [3, 44, 0]
    YellowRainBoots = 35	    # old: [3, 45, 0]
    BlackAthleticShoes = 36	    # old: [1, 46, 0]
    PirateShoes = 37		    # old: [3, 47, 0]
    ToonosaurFeet = 38		    # old: [3, 48, 0]
    Wingtips = 39			    # old: [1, 4, 0]
    BlackFancyShoes = 40	    # old: [2, 5, 0]
    PurpleBoots = 41		    # old: [3, 12, 0]
    BrownFancyShoes = 42	    # old: [2, 14, 0]
    RedFancyShoes = 43		    # old: [2, 15, 0]
    BlueSquareBoots = 44	    # old: [3, 23, 0]
    GreenHeartsBoots = 45	    # old: [3, 24, 0]
    GreyDotsBoots = 46		    # old: [3, 25, 0]
    OrangeStarsBoots = 47	    # old: [3, 26, 0]
    PinkStarsBoots = 48		    # old: [3, 27, 0]
    PurpleFancyShoes = 49	    # old: [2, 29, 0]
    SpaceBoots = 50			    # old: [2, 49, 0]
    WitchShoes = 51			    # old: [3, 50, 0]
    SkeletonShoes = 52		    # old: [2, 51, 0]
    AlchemistShoes = 53		    # old: [3, 52, 0]
    HumbleRagdoll = 54		    # old: [3, 53, 0]
    RegalRagdoll = 55		    # old: [3, 54, 0]
    TraditionalRagdoll = 56	    # old: [3, 55, 0]
    HumbleTin = 57			    # old: [3, 56, 0]
    RegalTin = 58			    # old: [3, 57, 0]
    TraditionalTin = 59		    # old: [3, 58, 0]
    VintageSnow = 60		    # old: [3, 59, 0]
    AviatorBoots = 61		    # old: [3, 60, 0]
    WingsuitBoots = 62		    # old: [3, 61, 0]
    OutbackShoes = 63		    # old: [2, 62, 0]
    PumpkinShoes = 64		    # old: [2, 63, 0]
    LazyBonesSlippers = 65	    # old: [1, 64, 0]
    HomemadeRagdoll = 66	    # old: [3, 65, 0]
    HomemadeTin = 67		    # old: [3, 66, 0]
    RetroWinterSuit = 68	    # old: [2, 67, 0]
    RetroWinterDress = 69	    # old: [2, 68, 0]
    BreaktheLawShoes = 70	    # old: [2, 69, 0]
    TripleRainbowShoes = 71	    # old: [2, 70, 0]
    ChairmanShoes = 72		    # old: [1, 71, 0]
    PhantoonShoes = 73		    # old: [2, 72, 0]
    TumblesShoes = 74		    # old: [2, 73, 0]
    HallowopolisBoots = 75	    # old: [3, 74, 0]
    DiverBoots = 76			    # old: [3, 75, 0]
    TrolleyEngineerBoots = 77   # old: [2, 76, 0]
    FruitPieShoes = 78		    # old: [2, 77, 0]
    CardSuitShoesRed = 79	    # old: [3, 78, 0]
    CardSuitShoesBlack = 80	    # old: [3, 79, 0]
    GatorSlippers = 81		    # old: [3, 80, 0]
    PaintersMocasins = 82	    # old: [2, 81, 0]
    ArmoredGreaves = 83		    # old: [2, 82, 0]
    CybertoonShoes = 84		    # old: [2, 83, 0]


@defineItemSubtypeEnum(ItemType.Cosmetic_Neck)
class NeckItemType(IntEnum):
    """
    Item subtype enum for Neck accessories (scarves, bowties, etc.).
    """
    Scarf2019 = 1                   # old: [40, 0, 0], backpack
    DoeBandana = 2                  # old: [43, 0, 0], backpack
    AviatorScarf = 3                # old: [47, 0, 0], backpack
    PinwheelBowtie = 4              # old: [49, 0, 0], backpack
    BloodsuckerLollipop = 5         # old: [58, 12, 0], backpack
    CjTie = 6                       # old: [59, 13, 0], backpack
    SailorCollarWhite = 7           # old: [60, 0, 0], backpack
    SailorCollarBlue = 8            # old: [60, 15, 0], backpack
    SailorCollarCyan = 9            # old: [60, 16, 0], backpack
    SailorCollarGreen = 10          # old: [60, 17, 0], backpack
    SailorCollarOrange = 11         # old: [60, 18, 0], backpack
    SailorCollarPink = 12           # old: [60, 19, 0], backpack
    SailorCollarPurple = 13         # old: [60, 20, 0], backpack
    SailorCollarRed = 14            # old: [60, 21, 0], backpack
    SailorCollarBlack = 15          # old: [60, 22, 0], backpack
    SailorCollarYellow = 16         # old: [60, 23, 0], backpack
    SailorBowWhite = 17             # old: [61, 0, 0], backpack
    SailorBowBlue = 18              # old: [61, 24, 0], backpack
    SailorBowCyan = 19              # old: [61, 25, 0], backpack
    SailorBowGreen = 20             # old: [61, 26, 0], backpack
    SailorBowOrange = 21            # old: [61, 27, 0], backpack
    SailorBowPink = 22              # old: [61, 28, 0], backpack
    SailorBowPurple = 23            # old: [61, 29, 0], backpack
    SailorBowRed = 24               # old: [61, 30, 0], backpack
    SailorBowBlack = 25             # old: [61, 31, 0], backpack
    SailorBowYellow = 26            # old: [61, 32, 0], backpack
    RetroScarf = 27                 # old: [67, 0, 0], backpack
    Scarf2020 = 28                  # old: [40, 39, 0], backpack
    FlowerTie = 29                  # old: [69, 0, 0], backpack
    ClownBowtie = 30                # old: [73, 0, 0], backpack
    JesterCollar = 31               # old: [75, 42, 0], backpack
    LawBowtie = 32                  # old: [73, 43, 0], backpack
    Scarf2021 = 33                  # old: [40, 48, 0], backpack
    OttomanTie = 34                 # old: [86, 0, 0], backpack
    EyeBowtie = 35                  # old: [89, 0, 0], backpack
    MysteryBowtie = 36              # old: [90, 0, 0], backpack
    NewstoonBlueBowtie = 37         # old: [73, 49, 0], backpack
    Scarf2022 = 38                  # old: [93, 0, 0], backpack
    RibbonBowtie = 39               # old: [40, 50, 0], backpack
    RibbonBowtieRedpolka = 40       # old: [93, 51, 0], backpack
    RibbonBowtiePurple = 41         # old: [93, 52, 0], backpack
    RibbonBowtieYellow = 42         # old: [93, 53, 0], backpack
    RibbonBowtieBluechecker = 43    # old: [93, 54, 0], backpack
    RibbonBowtieRed = 44            # old: [93, 55, 0], backpack
    RibbonBowtieRainbow = 45        # old: [93, 56, 0], backpack
    RibbonBowtiePinkdots = 46       # old: [93, 57, 0], backpack
    RibbonBowtieGreenchecker = 47   # old: [93, 58, 0], backpack
    RibbonBowtieBlue = 48           # old: [93, 59, 0], backpack
    RibbonBowtieCandycorn = 49      # old: [93, 60, 0], backpack
    RibbonBowtieBlack = 50          # old: [93, 61, 0], backpack
    BrovinciNecklace = 51           # old: [96, 0, 0], backpack
    NeckCowbell = 52                # old: [101, 0, 0], backpack
    GbBowtieBlack = 53              # old: [73, 72, 0], backpack
    GbBowtieBlackwhite = 54         # old: [73, 73, 0], backpack
    GbBowtieBlue = 55               # old: [73, 74, 0], backpack
    GbBowtieGray = 56               # old: [73, 75, 0], backpack
    GbBowtieGreen = 57              # old: [73, 76, 0], backpack
    GbBowtieOrange = 58             # old: [73, 77, 0], backpack
    GbBowtiePink = 59               # old: [73, 78, 0], backpack
    GbBowtiePinkblack = 60          # old: [73, 79, 0], backpack
    GbBowtiePolkadot = 61           # old: [73, 80, 0], backpack
    GbBowtiePurple = 62             # old: [73, 81, 0], backpack
    GbBowtiePurpleorange = 63       # old: [73, 82, 0], backpack
    GbBowtieRed = 64                # old: [73, 83, 0], backpack
    GbBowtieYellow = 65             # old: [73, 84, 0], backpack
    GbBowtieYellowblack = 66        # old: [73, 85, 0], backpack
    EeChefscarf = 67                # old: [108, 0, 0], backpack
    BandanaEngineer = 68            # old: [51, 71, 0], backpack
    Scarf2023 = 69                  # old: [40, 86, 0], backpack
    OutbackBandana = 70             # old: [51, 0, 0], backpack
    PrideBowtieAce = 71             # old: [73, 88, 0], backpack
    PrideBowtieAro = 72             # old: [73, 89, 0], backpack
    PrideBowtieBi = 73              # old: [73, 90, 0], backpack
    PrideBowtieGay = 74             # old: [73, 91, 0], backpack
    PrideBowtieFluid = 75           # old: [73, 92, 0], backpack
    PrideBowtieLesbian = 76         # old: [73, 93, 0], backpack
    PrideBowtieLgbt = 77            # old: [73, 94, 0], backpack
    PrideBowtieNb = 78              # old: [73, 95, 0], backpack
    PrideBowtiePan = 79             # old: [73, 96, 0], backpack
    PrideBowtieTrans = 80           # old: [73, 97, 0], backpack


"""Social ItemTypes"""


@defineItemSubtypeEnum(ItemType.Social_CheesyEffect)
class CheesyEffectItemType(IntEnum):
    """
    Item subtype enum for Cheesy Effects.
    """

    BigHead = 1
    SmallHead = 2
    BigLegs = 3
    SmallLegs = 4
    BigToon = 5
    SmallToon = 6
    FlatPortrait = 7
    FlatProfile = 8
    Transparent = 9
    NoColor = 10
    Invisible = 11
    Pumpkin = 12
    BigWhite = 13
    SnowMan = 14
    GreenToon = 15
    PumpkinPale = 16
    PumpkinPurple = 17
    PumpkinFlare = 18
    PumpkinScapegoat = 19
    Spirit = 20
    Stomped = 21
    Backwards = 22
    Amogus = 23
    Wireframe = 77
    Fired = 78


@defineItemSubtypeEnum(ItemType.Social_CustomSpeedchat)
class CustomSpeedchatItemType(IntEnum):
    """
    Item subtype enum for custom Speedchat phrases.
    """
    OhWell = 10
    WhyNot = 20
    Naturally = 30
    ThatsTheWayToDoIt = 40
    RightOn = 50
    WhatUp = 60
    ButOfCourse = 70
    Bingo = 80
    YouveGotToBeKidding = 90
    SoundsGoodToMe = 100
    ThatsKooky = 110
    Awesome = 120
    ForCryingOutLoud = 130
    DontWorry = 140
    Grrrr = 150
    WhatsNew = 160
    HeyHeyHey = 170
    SeeYouTomorrow = 180
    SeeYouNextTime = 190
    SeeYaLaterAlligator = 200
    AfterAWhileCrocodile = 210
    INeedToGoSoon = 220
    IDontKnowAboutThis = 230
    YoureOuttaHere = 240
    OuchThatReallySmarts = 250
    Gotcha = 260
    Please = 270
    ThanksAMillion = 280
    YouAreStylin = 290
    ExcuseMe = 300
    CanIHelpYou = 310
    ThatsWhatImTalkingAbout = 320
    IfYouCantTakeTheHeatStayOutOfTheKitchen = 330
    WellShiverMeTimbers = 340
    WellIsntThatSpecial = 350
    QuitHorsingAround = 360
    CatGotYourTongue = 370
    YoureInTheDogHouseNow = 380
    LookWhatTheCatDraggedIn = 390
    INeedToGoSeeAToon = 400
    DontHaveACow = 410
    DontChickenOut = 420
    YoureASittingDuck = 430
    Whatever = 440
    Totally = 450
    Sweet = 460
    ThatRules = 470
    YeahBaby = 480
    CatchMeIfYouCan = 490
    YouNeedToHealFirst = 500
    YouNeedMoreLaffPoints = 510
    IllBeBackInAMinute = 520
    ImHungry = 530
    YeahRight = 540
    ImSleepy = 550
    ImReady = 560
    ImBored = 570
    ILoveIt = 580
    ThatWasExciting = 590
    Jump = 600
    GotGags = 610
    WhatsWrong = 620
    EasyDoesIt = 630
    SlowAndSteadyWinsTheRace = 640
    Touchdown = 650
    Ready = 660
    Set = 670
    Go = 680
    LetsGoThisWay = 690
    YouWon = 700
    IVoteYes = 710
    IVoteNo = 720
    CountMeIn = 730
    CountMeOut = 740
    StayHereIllBeBack = 750
    ThatWasQuick = 760
    DidYouSeeThat = 770
    WhatsThatSmell = 780
    ThatStinks = 790
    IDontCare = 800
    JustWhatTheDoctorOrdered = 810
    LetsGetThisPartyStarted = 820
    ThisWayEverybody = 830
    WhatInTheWorld = 840
    TheChecksInTheMail = 850
    IHeardThat = 860
    AreYouTalkingToMe = 870
    ThankYouIllBeHereAllWeek = 880
    Hmm = 890
    IllGetThisOne = 900
    IGotIt = 910
    ItsMine = 920
    PleaseTakeIt = 930
    StandBackThisCouldBeDangerous = 940
    NoWorries = 950
    OhMy = 960
    Whew = 970
    Owoooo = 980
    AllAboard = 990
    HotDiggityDog = 1000
    CuriosityKilledTheCat = 1010
    TeamworkMakesTheDreamWork = 1011
    EvenMiraclesTakeALittleTime = 1012
    SometimesTheRightPathIsNotTheEasiestOne = 1013
    TodayIsAGoodDayToTry = 1014
    TodayIsMyLuckyDay = 1015
    GetYourActTogether = 1016
    WellPlayItByEar = 1017
    APieInTheHandIsWorthTwoInTheOven = 1018
    ItsRainingCatsAndDogs = 1019
    IThinkIllCallItADay = 1020
    TakeThis = 1021
    TakeThat = 1022
    Electrifying = 1023
    BeBackInAJiffy = 1024
    IDontSeeWhyNot = 1025
    YouNeverKnowUnlessYouTry = 1026
    SmartMove = 1027
    ThatCantBeAGoodIdea = 1028
    ImDownForTheCount = 1029
    IThinkYouShouldSleepOnIt = 1030
    Valid = 1031
    EverybodyIsWelcome = 1032
    TheresAlwaysASpaceForYou = 1033
    IConcur = 1034
    KindnessIsTheBestPolicy = 1035
    HonestyIsTheBestPolicy = 1036
    ManyDifferentFlowersMakeABouquet = 1037
    GreatMindsThinkAlike = 1038
    IfYouWantToGoFarGoTogether = 1039
    IAmGoingToScream = 1040
    OhYoureApproachingMe = 1041
    Yeah = 1042
    ActYourAge = 2000
    AmIGladToSeeYou = 2010
    BeMyGuest = 2020
    BeenKeepingOutOfTrouble = 2030
    BetterLateThanNever = 2040
    Bravo = 2050
    ButSeriouslyFolks = 2060
    CareToJoinUs = 2070
    CatchYouLater = 2080
    ChangedYourMind = 2090
    ComeAndGetIt = 2100
    DearMe = 2110
    DelightedToMakeYourAcquaintance = 2120
    DontDoAnythingIWouldntDo = 2130
    DontEvenThinkAboutIt = 2140
    DontGiveUpTheShip = 2150
    DontHoldYourBreath = 2160
    DontAsk = 2170
    EasyForYouToSay = 2180
    EnoughIsEnough = 2190
    Excellent = 2200
    FancyMeetingYouHere = 2210
    GiveMeABreak = 2220
    GladToHearIt = 2230
    GoAheadMakeMyDay = 2240
    GoForIt = 2250
    GoodJob = 2260
    GoodToSeeYou = 2270
    GotToGetMoving = 2280
    GotToHitTheRoad = 2290
    HangInThere = 2300
    HangOnASecond = 2310
    HaveABall = 2320
    HaveFun = 2330
    HaventGotAllDay = 2340
    HoldYourHorses = 2350
    Horsefeathers = 2360
    IDontBelieveThis = 2370
    IDoubtIt = 2380
    IOweYouOne = 2390
    IReadYouLoudAndClear = 2400
    IThinkSo = 2410
    IllPass = 2420
    IWishIdSaidThat = 2430
    IWouldntIfIWereYou = 2440
    IdBeHappyTo = 2450
    ImHelpingMyFriend = 2460
    ImHereAllWeek = 2470
    ImagineThat = 2480
    InTheNickOfTime = 2490
    ItsNotOverTilItsOver = 2500
    JustThinkingOutLoud = 2510
    KeepInTouch = 2520
    LovelyWeatherForDucks = 2530
    MakeItSnappy = 2540
    MakeYourselfAtHome = 2550
    MaybeSomeOtherTime = 2560
    MindIfIJoinYou = 2570
    NicePlaceYouHaveHere = 2580
    NiceTalkingToYou = 2590
    NoDoubtAboutIt = 2600
    NoKidding = 2610
    NotByALongShot = 2620
    OfAllTheNerve = 2630
    OkayByMe = 2640
    Righto = 2650
    SayCheese = 2660
    SayWhat = 2670
    TahDah = 2680
    TakeItEasy = 2690
    TaTaForNow = 2700
    ThanksButNoThanks = 2710
    ThatTakesTheCake = 2720
    ThatsFunny = 2730
    ThatsTheTicket = 2740
    TheresACogInvasion = 2750
    Toodles = 2760
    WatchOut = 2770
    WellDone = 2780
    WhatsCooking = 2790
    WhatsHappening = 2800
    WorksForMe = 2810
    YesSirree = 2820
    YouBetcha = 2830
    YouDoTheMath = 2840
    YouLeavingSoSoon = 2850
    YouMakeMeLaugh = 2860
    YouTakeRight = 2870
    YoureGoingDown = 2880
    AnythingThatCanGoWrongWillGoWrong = 2881
    NeverInAMillionYears = 2882
    WouldYouLikeSomeJellybeansWithThat = 2883
    LetTheSleepingDogLie = 2884
    Jinx = 2885
    XMarksTheSpot = 2886
    IsThatLegal = 2887
    ThatIsIllegal = 2888
    IllBeTheJudgeOfThat = 2889
    YouBeTheJudge = 2890
    HowIsThatEvenPossible = 2891
    IDontThinkItMeansWhatYouThinkItMeans = 2892
    Wonderful = 2893
    Terrific = 2894
    Really = 2895
    Nope = 2896
    WithGreatPowerComesGreatResponsibility = 2897
    ItsYourTurn = 2898
    IveMadeUpMyMind = 2899
    SpeakOfTheDevilRay = 2900
    ThisIsAVrbys = 2901
    ThisIsFine = 2092
    BringItOnTinCan = 2093
    IBegYourPardon = 2094
    AnythingYouSay = 3000
    CareIfIJoinYou = 3010
    CheckPlease = 3020
    DontBeTooSure = 3030
    DontMindIfIDo = 3040
    DontSweatIt = 3050
    DontYouKnowIt = 3060
    DontMindMe = 3070
    Eureka = 3080
    FancyThat = 3090
    ForgetAboutIt = 3100
    GoingMyWay = 3110
    GoodForYou = 3120
    GoodGrief = 3130
    HaveAGoodOne = 3140
    HeadsUp = 3150
    HereWeGoAgain = 3160
    HowAboutThat = 3170
    HowDoYouLikeThat = 3180
    IBelieveSo = 3190
    IThinkNot = 3200
    IllGetBackToYou = 3210
    ImAllEars = 3220
    ImBusy = 3230
    ImNotKidding = 3240
    ImSpeechless = 3250
    KeepSmiling = 3260
    LetMeKnow = 3270
    LetThePieFly = 3280
    LikewiseImSure = 3290
    LookAlive = 3300
    MyHowTimeFlies = 3310
    NoComment = 3320
    NowYoureTalking = 3330
    OkayByMeDupe = 3340
    PleasedToMeetYou = 3350
    RightoDupe = 3360
    SureThing = 3370
    ThanksAMillionDupe = 3380
    ThatsMoreLikeIt = 3390
    ThatsTheStuff = 3400
    TimeForMeToHitTheHay = 3410
    TrustMe = 3420
    UntilNextTime = 3430
    WaitUp = 3440
    WayToGo = 3450
    WhatBringsYouHere = 3460
    WhatHappened = 3470
    WhatNow = 3480
    YouFirst = 3490
    YouTakeLeft = 3500
    YouWish = 3510
    YoureToast = 3520
    YoureTooMuch = 3530
    DontKeepMeWaiting = 3531
    DontJudgeABookByItsCover = 3532
    LongTimeNoSee = 3533
    PassTheSaltPlease = 3534
    ItsTimeForTea = 3535
    ThatsAWrap = 3536
    TryAgain = 3537
    GetInLine = 3538
    IsIt = 3539
    ProbablyNot = 3540
    Ding = 3541
    IVolunteer = 3542
    GoodToKnow = 3543
    YouHaveGoodTaste = 3544
    TheCogsAreNoMatchForUs = 3545
    DohIMissed = 3546
    ICantBelieveYouveDoneThis = 3547
    ItsOver = 3548
    ThisWasNotOurFinestMoment = 3549
    YoureNotMyBoss = 3550
    YouCanNeverBeTooSafe = 3551
    ToonsRule = 4000
    CogsDrool = 4010
    ToonsOfTheWorldUnite = 4020
    HowdyPartner = 4030
    MuchObliged = 4040
    GetAlongLittleDoggie = 4050
    ImGoingToHitTheHay = 4060
    ImChompingAtTheBit = 4070
    ThisTownIsntBigEnoughForTheTwoOfUs = 4080
    SaddleUp = 4090
    Draw = 4100
    TheresGoldInThemThereHills = 4110
    HappyTrails = 4120
    ThisIsWhereIRideOffIntoTheSunset = 4130
    LetsSkedaddle = 4140
    YouGotABeeInYourBonnet = 4150
    LandsSake = 4160
    RightAsRain = 4170
    IReckonSo = 4180
    LetsRide = 4190
    WellGoFigure = 4200
    ImBackInTheSaddleAgain = 4210
    RoundUpTheUsualSuspects = 4220
    Giddyup = 4230
    ReachForTheSky = 4240
    ImFixingTo = 4250
    HoldYourHorsesDupe = 4260
    ICantHitTheBroadSideOfABarn = 4270
    YallComeBackNow = 4280
    ItsARealBarnBurner = 4290
    DontBeAYellowBelly = 4300
    FeelingLucky = 4310
    WhatInSamHillsGoinOnHere = 4320
    ShakeYourTailFeathers = 4330
    WellDontThatTakeAll = 4340
    ThatsASightForSoreEyes = 4350
    PickinsIsMightySlimAroundHere = 4360
    TakeALoadOff = 4370
    ArentYouASight = 4380
    ThatllLearnYa = 4390
    Unforgivable = 4391
    IsThatIt = 4392
    ThatsIt = 4393
    ThatsEnoughForMe = 4394
    WeAreMintToBe = 4395
    LettuceCelebrate = 4396
    LetsTacoAboutIt = 4397
    Glue = 4398
    UnderstandableHaveANiceDay = 4399
    LoveThatForYou = 4400
    ComeToThinkOfIt = 4401
    AndFinally = 4402
    IWantCandy = 6000
    IveGotASweetTooth = 6010
    ThatsHalfBaked = 6020
    JustLikeTakingCandyFromABaby = 6030
    TheyreCheaperByTheDozen = 6040
    LetThemEatCake = 6050
    ThatsTheIcingOnTheCake = 6060
    YouCantHaveYourCakeAndEatItToo = 6070
    IFeelLikeAKidInACandyStore = 6080
    SixOfOneHalfADozenOfTheOther = 6090
    LetsKeepItShortAndSweet = 6100
    DoughnutMindIfIDo = 6110
    ThatsPieInTheSky = 6120
    ButItsWaferThin = 6130
    LetsGumUpTheWorks = 6140
    YoureOneToughCookie = 6150
    ThatsTheWayTheCookieCrumbles = 6160
    LikeWaterForChocolate = 6170
    AreYouTryingToSweetTalkMe = 6180
    ASpoonfulOfSugarHelpsTheMedicineGoDown = 6190
    YouAreWhatYouEat = 6200
    EasyAsPie = 6210
    DontBeASucker = 6220
    SugarAndSpiceAndEverythingNice = 6230
    ItsLikeButter = 6240
    TheCandymanCan = 6250
    WeAllScreamForIceCream = 6260
    LetsNotSugarCoatIt = 6270
    KnockKnock = 6280
    WhosThere = 6290
    Lit = 6291
    IllSitThisOneOut = 6292
    IfOnlyIHadAMillionJellybeans = 6293
    Foreshadowing = 6294
    YourePopular = 6295
    NotMe = 6296
    Kaboom = 6297
    AsAMatterOfFact = 6298
    IllComeBackToThatTomorrow = 6299
    ThisIsTooMuchForMe = 6300
    WereGoingToBeSafeAndSound = 6301
    HowArtThou = 6302
    Howdyeth = 6303
    DontBurnethTheCandleAtBothEnds = 6304
    WhatDostThouNeedeth = 6305
    AsIf = 6306
    Actually = 6307
    QuitMonkeyingAround = 7000
    ThatReallyThrowsAMonkeyWrenchInThings = 7010
    MonkeySeeMonkeyDo = 7020
    TheyMadeAMonkeyOutOfYou = 7030
    ThatSoundsLikeMonkeyBusiness = 7040
    ImJustMonkeyingWithYou = 7050
    WhosGonnaBeMonkeyInTheMiddle = 7060
    ThatsAMonkeyOffMyBack = 7070
    ThisIsMoreFunThanABarrelOfMonkeys = 7080
    WellIllBeAMonkeysUncle = 7090
    IveGotMonkeysOnTheBrain = 7100
    WhatsWithTheMonkeySuit = 7110
    HearNoEvil = 7120
    SeeNoEvil = 7130
    SpeakNoEvil = 7140
    LetsMakeLikeABananaAndSplit = 7150
    ItsAJungleOutThere = 7160
    YoureTheTopBanana = 7170
    CoolBananas = 7180
    ImGoingBananas = 7190
    LetsGetIntoTheSwingOfThings = 7200
    ThisPlaceIsSwinging = 7210
    ImDyingOnTheVine = 7220
    LetsMakeLikeATreeAndLeave = 7230
    ThisWholeAffairHasMeUpATree = 7235
    JellybeansDontGrowOnTrees = 7240
    ThatsNotReal = 7241
    YaLikeJazz = 7242
    LetThePiesFly = 7243
    WeDontSpeakOnThat = 7244
    AMagicianShallNeverRevealTheirSecrets = 7245
    OoohWhatDoesThisButtonDo = 7246
    BuhBye = 7247
    MyFavoriteDayIsSundae = 7248
    FingersCrossed = 7249
    ThatsCrazy = 7250
    Gadzooks = 7251
    AhoyMeHearties = 7252
    DontMissTheForestForTheTrees = 7253
    IAgreeWithYourStatement = 7256
    IDisagreeWithYourStatement = 7257
    TrueTrue = 7258
    ThisPlaceIsAGhostTown = 10000
    NiceCostume = 10001
    IThinkThisPlaceIsHaunted = 10002
    TrickOrTreat = 10003
    Boo = 10004
    HappyHaunting = 10005
    HappyHalloween = 10006
    ItsTimeForMeToTurnIntoAPumpkin = 10007
    Spooktastic = 10008
    Spooky = 10009
    ThatsCreepy = 10010
    IHateSpiders = 10011
    DidYouHearThat = 10012
    YouDontHaveAGhostOfAChance = 10013
    YouScaredMe = 10014
    ThatsSpooky = 10015
    ThatsFreaky = 10016
    ThatWasStrange = 10017
    SkeletonsInYourCloset = 10018
    DidIScareYou = 10019
    FlippyNeedsYourHelp = 10020
    HaveYouFoundTheScientistsYet = 10021
    HaveYouSeenTheNewSpookyBuildingOnPolarPlace = 10022
    Spooktacular = 10023
    ThatReallySendsAShiverDownMySpine = 10024
    ImTerrified = 10025
    DontBeAScaredyCat = 10026
    PleaseParkAllYourBroomsAndPumpkinCartsAtTheDoor = 10027
    EatDrinkAndBeScary = 10028
    WitchWayToTheTreats = 10029
    EnterIfYouDare = 10030
    BahHumbug = 11000
    BetterNotPout = 11001
    Brrr = 11002
    ChillOut = 11003
    ComeAndGetItDupe = 11004
    DontBeATurkey = 11005
    GobbleGobble = 11006
    HappyHolidays = 11007
    HappyNewYear = 11008
    HappyThanksgiving = 11009
    HappyTurkeyDay = 11010
    HoHoHo = 11011
    ItsSnowProblem = 11012
    ItsSnowWonder = 11013
    LetItSnow = 11014
    RakeEmIn = 11015
    SeasonsGreetings = 11016
    SnowDoubtAboutIt = 11017
    SnowFarSnowGood = 11018
    YuleBeSorry = 11019
    HaveAWonderfulWinter = 11020
    Festive = 11021
    IcyWhatYouDidThere = 11022
    AllIWantForChristmasIsEwe = 11023
    BeMine = 12000
    BeMySweetie = 12001
    HappyValentoonsDay = 12002
    AwwHowCute = 12003
    ImSweetOnYou = 12004
    ItsPuppyLove = 12005
    LoveYa = 12006
    WillYouBeMyValentoon = 12007
    YouAreASweetheart = 12008
    YouAreAsSweetAsPie = 12009
    YouAreCute = 12010
    YouNeedAHug = 12011
    Lovely = 12012
    ThatsDarling = 12013
    RosesAreRed = 12014
    VioletsAreBlue = 12015
    ThatsSweet = 12016
    ILoveYouMoreThanACogLovesOil = 12050
    YoureDynamite = 12051
    IOnlyHaveHypnoEyesForYou = 12052
    YoureSweeterThanAJellybean = 12053
    YoureValentoonTastic = 12054
    AKissARooFromMeToYou = 12055
    WeAreThePerfectPear = 12056
    YouArePurrFect = 12057
    ImYourBiggestFan = 12058
    YoureTheIcingOnTheCake = 12059
    YoureTheAppleOfMyEye = 12060
    TopOTheMorninToYou = 13000
    HappyStPatricksDay = 13001
    YoureNotWearingGreen = 13002
    ItsTheLuckOfTheIrish = 13003
    ImGreenWithEnvy = 13004
    YouLuckyDog = 13005
    YoureMyFourLeafClover = 13006
    YoureMyLuckyCharm = 13007


@defineItemSubtypeEnum(ItemType.Social_ChatStickers)
class ChatStickersItemType(EnhancedIntEnum):
    """
    Item subtype enum for Chat Stickers.
    """

    # Defaults
    DisgustGator = 0
    ConcernedDog = 1
    ConfusedKangaroo = 2
    CryCat = 3
    GriefKiwi = 4
    BlushBat = 5
    GrinDuck = 6
    HeartRabbit = 7
    GreenedCat = 8
    PensiveFox = 9
    PleadingDog = 10
    SadBat = 11
    SurprisedArmadillo = 12
    SurprisedRaccoon = 13
    SusBeaver = 14
    WinkDeer = 15

    # Regional managers
    Bellringer = 16
    ChainsawConsultant = 17
    DeepDiver = 18
    DuckShuffler = 19
    Featherbedder = 20
    Firestarter = 21
    Gatekeeper = 22
    MajorPlayer = 23
    Mouthpiece = 24
    Multislacker = 25
    Pacesetter = 26
    Plutocrat = 27
    Prethinker = 28
    Rainmaker = 29
    Treekiller = 30
    WitchHunter = 31

    SellbotEmblem = 32
    CashbotEmblem = 33
    LawbotEmblem = 34
    BossbotEmblem = 35
    BoardbotEmblem = 36

    DiceRoll = 40

    HighRoller = 50
    FrustratedForeman = 51

    Litigator = 52
    Stenographer = 53
    CaseManager = 54
    Scapegoat = 55


@defineItemSubtypeEnum(ItemType.Social_NametagFont)
class NametagFontItemType(IntEnum):
    """
    Item subtype enum for Nametag fonts
    """
    # Defaults
    Basic = 0
    Plain = 1
    Shivering = 2
    Wonky = 3
    Fancy = 4
    Silly = 5
    Zany = 6
    Practical = 7
    Nautical = 8
    Whimsical = 9
    Spooky = 10
    Action = 11
    Poetic = 12
    Boardwalk = 13
    Western = 14
    Abstract = 15

    # Kudos Fonts
    IceCream = 16
    Pirate = 17
    Medieval = 18
    Calligraphy = 19
    Playful = 20
    Comical = 21
    Arrogant = 22
    Cinema = 23


@defineItemSubtypeEnum(ItemType.Social_Emote)
class EmoteItemType(IntEnum):
    """
    Item subtype enum for Emotes.
    IDs are identical to the IDs for old emotes.
    """
    Wave = 0
    Happy = 1
    Sad = 2
    Angry = 3
    Sleepy = 4
    Shrug = 5
    Dance = 6
    Think = 7
    Bored = 8
    Applause = 9
    Cringe = 10
    Confused = 11
    BellyFlop = 12
    Bow = 13
    BananaPeel = 14
    ResistanceSalute = 15
    # Skipping 16. This was an unused variant of Laugh.
    LaughUNUSED = 16
    Yes = 17
    No = 18
    OK = 19
    Surprise = 20
    Cry = 21
    Delighted = 22
    Furious = 23
    Laugh = 24
    Taunt = 25
    Yawn = 26
    Shiver = 27


@defineItemSubtypeEnum(ItemType.Profile_Background)
class BackgroundItemType(IntEnum):
    """
    Item subtype enum for Backgrounds.
    """
    Default = 0  # from: 0

    PG_Sky_TTC = 100  # from: 1
    PG_Sky_BB = 101  # from: 23
    PG_Sky_YOTT = 102  # from: 25
    PG_Sky_DG = 103  # from: 24
    PG_Sky_MML = 104  # from: 2
    PG_Sky_TB = 105  # from: 3
    PG_Sky_AA = 106  # from: 26
    PG_Sky_DDL = 107  # from: 4

    PG_TTC = 200  # from: 5
    PG_BB = 201  # from: 6
    PG_YOTT = 202  # from: 8
    PG_DG = 203  # from: 7
    PG_MML = 204  # from: 9
    PG_TB = 205  # from: 10
    PG_AA = 206  # from: 11
    PG_DDL = 207  # from: 12

    HQ_Sellbot = 300  # from: 13
    HQ_Cashbot = 301  # from: 14
    HQ_Lawbot = 302  # from: 15
    HQ_Bossbot = 303  # from: 16
    HQ_Boardbot = 304  # from: 17

    Activity_Fishing = 400  # from: 18
    Activity_Golfing = 401  # from: 27
    Activity_Racing = 402  # from: 28
    Activity_Trolley = 403  # from: 29

    Tasks_Judy = 500  # from: 39

    Event_Winter2018_A = 600  # from: 19
    Event_Winter2018_B = 601  # from: 20
    Event_NewYears2019 = 602  # from: 21
    Event_SkyClan = 603  # from: 22
    Event_Outback = 604  # from: 30
    Event_GoldenCorridor = 605  # from: 31
    Event_NewYears2020 = 606  # from: 32
    Event_BTL = 607  # from: 33
    Event_Valentines2020 = 608  # from: 34
    Event_Easter2020 = 609  # from: 35
    Event_StandIn = 610  # from: 36
    Event_FourthJuly2020 = 611  # from: 37
    Event_Halloween2020 = 612  # from: 38
    Event_Electric      = 613  # from: 49

    Special_PaintMixer = 700  # from: 40

    Kudos_TTC = 800  # from: 41
    Kudos_BB = 801  # from: 42
    Kudos_YOTT = 802  # from: 43
    Kudos_DG = 803  # from: 44
    Kudos_MML = 804  # from: 45
    Kudos_TB = 805  # from: 46
    Kudos_AA = 806  # from: 47
    Kudos_DDL = 807  # from: 48


@defineItemSubtypeEnum(ItemType.Profile_Nameplate)
class NameplateItemType(IntEnum):
    """
    Item subtype enum for Nameplates.
    """
    DefaultBlue = 101  # from: 0
    DefaultGreen = 102  # from: 1 [do not give]
    DefaultPurple = 103  # from: 2 [do not give]
    DefaultRed = 104  # from: 3 [do not give]
    DefaultYellow = 105  # from: 4 [do not give]
    DefaultOrange = 106  # from: 5 [do not give]
    DefaultBlueB = 107  # from: 6 [do not give]
    DefaultDarkBlue = 108  # from: 7 [do not give]
    DefaultDarkGreen = 109  # from: 8 [do not give]

    PG_TTC = 200  # from: 20
    PG_BB = 201  # from: 25
    PG_YOTT = 202  # from: 26
    PG_DG = 203  # from: 10
    PG_MML = 204  # from: 27
    PG_TB = 205  # from: 28
    PG_AA = 206  # from: 29
    PG_DDL = 207  # from: 11

    Activity_Golfing = 300  # from: 22
    Activity_Trolley = 301  # from: 23
    Activity_Racing = 302  # from: 24

    Tasks_Judy = 400  # from: 44

    Special_Stars = 500  # from: 9
    Special_UnderTheSea = 501  # from: 12
    Special_Slippin = 502  # from: 19
    Special_UpToEleven = 503  # from: 37
    Special_SnowballFight = 504  # from: 45
    Special_SellbotPaint = 505  # from: 46

    Event_Tinsel = 600  # from: 13
    Event_Candy = 601  # from: 14
    Event_Wrapping = 602  # from: 15
    Event_NightLights = 603  # from: 16
    Event_NewYears2019 = 604  # from: 17
    Event_SkyClan = 605  # from: 18
    Event_Outback = 606  # from: 21
    Event_LazyBones = 607  # from: 30
    Event_Thanksgiving2019 = 608  # from: 31
    Event_NewYears2020 = 609  # from: 32
    Event_PinkSlip = 610  # from: 33
    Event_Easter2020 = 611  # from: 34
    Event_AtticusDesk = 612  # from: 35
    Event_FourthJuly2020 = 613  # from: 36
    Event_Electric = 614  # from: 55

    Halloween_CandyBlue = 700  # from: 38
    Halloween_CandyGreen = 701  # from: 39
    Halloween_CandyMagenta = 702  # from: 40
    Halloween_CandyPurple = 703  # from: 41
    Halloween_CandyRed = 704  # from: 42
    Halloween_SpookyBat = 705  # from: 43

    Kudos_TTC = 800  # from: 47
    Kudos_BB = 801  # from: 48
    Kudos_YOTT = 802  # from: 49
    Kudos_DG = 803  # from: 50
    Kudos_MML = 804  # from: 51
    Kudos_TB = 805  # from: 52
    Kudos_AA = 806  # from: 53
    Kudos_DDL = 807  # from: 54


@defineItemSubtypeEnum(ItemType.Profile_Pose)
class ProfilePoseItemType(IntEnum):
    """
    Item subtype enum for profile poses.
    """
    Neutral = 0  # from: 0
    Wave = 1  # from: 1
    Sit = 2  # from: 2
    Applause = 3  # from: 3
    Thinking = 4  # from: 4
    Greened = 5  # from: 5
    Taunt = 6  # from: 6
    ImOuttaHere = 7  # from: 7
    Casting = 8  # from: 8
    Yippie = 9  # from: 9
    Selfie = 10  # from: 10
    ResistanceSalute = 11  # from: 11
    Throw = 12  # from: 12
    Hypnotizer = 13  # from: 13
    Running = 14  # from: 14
    Diving = 15  # from: 15
    WhatAreYouDoing = 16  # from: 16
    Slapped = 17  # from: 17
    Surprised = 18  # from: 18
    Presenting = 19  # from: 19
    Victory = 20  # from: 20
    Shrug = 21  # from: 21
    Upset = 22  # from: 22
    ToBeOrNotToBe = 23  # from: 23
    Spooky = 24  # from: 24
    Zombie = 25  # from: 25
    Yawn = 26  # from: 26
    Sinking = 27  # from: 27
    Megaphone = 28  # from: 28
    UpsideDown = 29  # from: 29
    Sideways = 30  # from: 30
    Small = 31  # from: 31
    SilentTreatment = 32  # from: 32
    Banana = 33  # from: 33
    SeltzerBottle = 34  # from: 34
    GagButton = 35  # from: 35
    PieToss = 36  # from: 36
    BecomeDuck = 37  # from: 37
    Treasure = 38  # from: 38
    AtTheGate = 39  # from: 39
    Elegance = 40  # from: 40
    PickUpThePhone = 41  # from: 41
    FireHands = 42  # from: 42
    Rolled = 43  # from: 43
    Naptime = 44  # from: 44


"""Fishing Item Types"""


@defineItemSubtypeEnum(ItemType.Fishing_Rod)
class FishingRodItemType(IntEnum):
    """
    Item subtype enum for fishing rods.
    """
    Cardboard = 1  # from 0
    Twig = 2  # from 1
    Bamboo = 3  # from 2
    Hardwood = 4  # from 3
    Steel = 5  # from 4
    Gold = 6  # from 5
    Platinum = 7  # from 6


"""Consumable Item Types"""


@defineItemSubtypeEnum(ItemType.Consumable_Boosters)
class BoosterItemType(IntEnum):
    """
    Item subtype enum for boosters.
    """
    Jellybeans_Global = 14
    Jellybeans_Bingo  = 24

    Gumballs_Global = 17

    Exp_Gags_Global  = 12
    Exp_Gags_Support = 50
    Exp_Gags_Power   = 51

    Exp_Activity_Global  = 11
    Exp_Activity_Racing  = 20
    Exp_Activity_Trolley = 21
    Exp_Activity_Golf    = 22
    Exp_Activity_Fishing = 23

    Fish_Rarity = 8

    Merit_Global   = 16
    Merit_Sellbot  = 3
    Merit_Cashbot  = 4
    Merit_Lawbot   = 5
    Merit_Bossbot  = 6
    Merit_Boardbot = 7

    Exp_Dept_Global   = 9
    Exp_Dept_Sellbot  = 30
    Exp_Dept_Cashbot  = 31
    Exp_Dept_Lawbot   = 32
    Exp_Dept_Bossbot  = 33
    Exp_Dept_Boardbot = 34

    Reward_Boss_Global   = 13
    Reward_Boss_Sellbot  = 40
    Reward_Boss_Cashbot  = 41
    Reward_Boss_Lawbot   = 42
    Reward_Boss_Bossbot  = 43
    Reward_Boss_Boardbot = 44

    AllStar = 60
    Random  = 70


"""Misc Item Types"""


@defineItemSubtypeEnum(ItemType.Material)
class MaterialItemType(IntEnum):
    """
    Item subtype enum for currencies.
    """
    Jellybeans = 1
    Gumballs = 2
    Batcoin = 3
