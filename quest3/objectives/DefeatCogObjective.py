import math

from direct.showbase.PythonUtil import bound

from toontown.battle.SuitBattleGlobals import COG_MINIBOSSES
from toontown.quest3 import SpecialQuestZones, QuestLocalizer
from toontown.quest3.base.QuestObjective import *
from toontown.quest3.context.DefeatCogContext import DefeatCogContext
from toontown.quest3.QuestLocalizer import (HL_Wanted, OBJ_Defeat, PROG_Defeat, SC_Defeat,
                                            SC_DefeatLocation, QuestProgress_Complete, PFX_DEFEAT)
from toontown.quest3.daily.DailyConstants import QuestTier
from toontown.suit import SuitDNA, SuitHoodGlobals
from toontown.toonbase.ToontownGlobals import ToontownCentral, DonaldsDock, OldeToontown, DaisyGardens, \
    MinniesMelodyland, HoodHierarchy, SellbotHQ, CashbotHQ, LawbotHQ, BossbotHQ, TheBrrrgh, OutdoorZone, \
    DonaldsDreamland, SpecialQuestCogHQZones2Facility, LowestToonLevelPerHQ


# Areas that allow cog levels higher than whats on the street
AllowLevelsHigherThanZone = (DaisyGardens, MinniesMelodyland, TheBrrrgh, OutdoorZone, DonaldsDreamland)
AllowBoostedLevelKudosZones = (DaisyGardens, MinniesMelodyland, TheBrrrgh, OutdoorZone, DonaldsDreamland)
BoostedLevelPossibleZones = {
    DaisyGardens: 1, MinniesMelodyland: 2, TheBrrrgh: 2, OutdoorZone: 3, DonaldsDreamland: 4,
    SellbotHQ: 2, CashbotHQ: 3, LawbotHQ: 4, BossbotHQ: 5, SpecialQuestZones.AnyCogHQ: 2
}
AnywhereBoostedLevelPossible = 4

# Certain suits coughoclocough are imitations of other suits. They should still count toward what they're imitating.
SuitNameOverrides = {
    'clo_hm': 'clo'
}


class DefeatCogObjective(QuestObjective):
    def __init__(self,
                 npc=2001,
                 rewards=None,
                 nextStep=None,
                 npcReturnable: bool = True,
                 zoneUnlocks=None,
                 cogCount: int = 1,
                 cogLocation: int = None,
                 cogType: str = None,
                 cogLevelMin: int = None,
                 cogTrack: str = None,
                 skelecog: bool = False,
                 virtual: bool = False,
                 revives: bool = False,
                 executive: bool = False,
                 manager: bool = False,
                 boss: bool = False,
                 taskManagerBoss: bool = False):
        super().__init__(npc=npc, rewards=rewards, nextStep=nextStep, npcReturnable=npcReturnable, zoneUnlocks=zoneUnlocks)
        self.cogCount = cogCount
        self.cogLocation = cogLocation
        self.cogType = cogType
        self.cogLevelMin = cogLevelMin
        self.cogTrack = cogTrack
        self.skelecog = skelecog
        self.virtual = virtual
        self.revives = revives
        self.executive = executive
        self.manager = manager
        self.boss = boss

        # The TaskManagerBoss attribute indicates that this is a boss in the taskline to be defeated.
        # It ignores location based calculation and also does other special task renders.
        self.taskManagerBoss = taskManagerBoss

    def calculateProgress(self, context: DefeatCogContext, questReference: QuestReference, quester: Quester,
                          cappedProgress: bool=True) -> int:
        if type(context) is not DefeatCogContext:
            return 0
        suitsDefeated = 0
        for suitEncounter in context.encounters:
            # First, match zoneId.
            zoneId = context.zoneId

            if (self.cogLocation is not None) and not self.taskManagerBoss:
                locationCounts = self.doesLocationCount(zoneId)
                # Keep going if this location does not count
                if not locationCounts:
                    continue

            suitEncounterTypes = [suitEncounter.type]
            if suitEncounter.type in SuitNameOverrides:
                suitEncounterTypes.append(SuitNameOverrides[suitEncounter.type])

            # Now match EVERY ARG EVER
            if self.cogType is not None and self.cogType not in suitEncounterTypes:
                continue
            if self.cogLevelMin is not None and (suitEncounter.level is None or suitEncounter.level < self.cogLevelMin):
                continue
            if self.cogTrack is not None and suitEncounter.track != self.cogTrack:
                continue
            if self.skelecog and suitEncounter.isSkelecog != self.skelecog:
                continue
            if self.virtual and suitEncounter.isVirtual != self.virtual:
                continue
            if self.revives and suitEncounter.hasRevives != self.revives:
                continue
            if self.executive and suitEncounter.isElite != self.executive:
                continue
            if self.manager and (suitEncounter.ignoreManagerFlag or suitEncounter.type not in COG_MINIBOSSES):
                continue
            if self.boss and not suitEncounter.isBoss:
                continue

            # This suit must count.
            suitsDefeated += 1
        
        # Return the capped result if desired.
        if cappedProgress:
            return min(suitsDefeated, self.cogCount - questReference.getQuestProgress(self.objectiveIndex))
        
        return suitsDefeated

    def doesLocationCount(self, zoneId):
        # Match to any Cog HQ
        if self.cogLocation == SpecialQuestZones.AnyCogHQ:
            if not ZoneUtil.isCogHQZone(zoneId):
                return False

        # Match by specific facility zone
        elif self.cogLocation in SpecialQuestCogHQZones2Facility.keys():
            if zoneId not in SpecialQuestCogHQZones2Facility[self.cogLocation]:
                return False

        # Match by Hood
        elif ZoneUtil.getHoodId(self.cogLocation) == self.cogLocation:
            if ZoneUtil.getHoodId(self.cogLocation) != ZoneUtil.getHoodId(zoneId):
                # This cog was killed in the wrong hood.
                return False

        # Match by Branch
        elif ZoneUtil.getBranchZone(self.cogLocation) == self.cogLocation:
            if ZoneUtil.getBranchZone(self.cogLocation) != ZoneUtil.getBranchZone(zoneId):
                # This cog was killed in the wrong branch.
                return False

        # Undefined match
        else:
            raise AttributeError("DefeatCogObjective given undefined zoneId to parse")

        return True

    """
    Random Task Generation
    """

    @staticmethod
    def getDifficultyRange(questerType: QuesterType, questSource: QuestSource, **extraArgs):
        return None, None

    @classmethod
    def generateFromDifficulty(cls, rng, difficulty: float, questSource: QuestSource, **extraArgs):
        """
        Given an arbitrary difficulty value, generate a QuestObjective.
        For more info, seek QuestGenerator.py.

        :param rng:        A seeded Random instance. Use this for .random() or .randint() calculations.
        :param difficulty: The arbitrary difficulty of the task.
        :return:           This QuestObjective, set with values to match the arbitrary difficulty.
        """
        # Set initial parameters.
        cogCount = 3.0 * (difficulty ** 1.7)
        cogType = None
        cogTrack = None
        cogLevelMin = None
        executive = False
        manager = False
        skelecog = False
        zoneId = extraArgs.get("zoneId")
        questTier = extraArgs.get("questTier")

        # Figure out how many modifiers we want to apply. Up to 3.
        maxModifiers = round(bound(math.log(max(1.0, difficulty ** 1.5), 10), 0, 3))
        modifierCount = rng.randint(0, maxModifiers)
        modifierList = [
            rng.choice(('cogType', 'cogTrack')),
            'cogLevelMin',
            'executive',
        ]
        if difficulty >= 7 and rng.random() > 0.5:
            modifierList.append('manager')
        rng.shuffle(modifierList)
        modifiers = [modifierList.pop() for _ in range(modifierCount)]

        # Don't let these modifiers combine
        if "cogType" in modifiers and "cogLevelMin" in modifiers:
            modifiers.remove("cogLevelMin")

        if "manager" in modifiers:
            # Replace cog type modifiers with cog track (if manager)
            if 'cogType' in modifiers:
                modifiers.remove('cogType')
                modifiers.append('cogTrack')
            # Managers are implicitly exe
            if 'executive' in modifiers:
                modifiers.remove('executive')

        # Apply the modifiers.
        for modifier in modifiers:
            if modifier == 'cogType':
                suitDict = {ToontownCentral:   (("ca", "f", "bf", "sc", "cc"), ("cn", "p", "b", "pf", "pp", "tm"), ("sw", "ym", "dt", "nn", "tw", "nd")),
                            DonaldsDock:       (("cn", "p", "b", "pf", "pp", "tm"), ("sw", "ym", "dt", "nn", "tw", "nd"), ("mdm", "mm", "ac", "cv", "bc", "gh")),
                            OldeToontown:      (("sw", "ym", "dt", "nn", "tw", "nd"), ("mdm", "mm", "ac", "cv", "bc", "gh"), ("txm", "ds", "bs", "ad", "nc", "ms")),
                            DaisyGardens:      (("mdm", "mm", "ac", "cv", "bc", "gh"), ("txm", "ds", "bs", "ad", "nc", "ms"), ("mg", "hh", "sd", "sh", "mb", "tf")),
                            MinniesMelodyland: (("txm", "ds", "bs", "ad", "nc", "ms"), ("mg", "hh", "sd", "sh", "mb", "tf"), ("bfh", "cr", "le", "br", "ls", "mi")),
                            -1:                (("mg", "hh", "sd", "sh", "mb", "tf"), ("bfh", "cr", "le", "br", "ls", "mi"), ("hho", "tbc", "bw", "rb", "mh")),
                            }
                listChoice = rng.randint(0, 2)
                pgSuits = suitDict.get(zoneId, suitDict.get(-1))
                cogType = rng.choice(pgSuits[listChoice])
                cogCount *= (0.15 - ((listChoice / 10.0) * 0.5))
                cogCount *= 0.75
            elif modifier == 'cogTrack':
                cogTrack = rng.choice(['s', 'm', 'l', 'c', 'g'])
                cogCount *= 0.75
                if cogTrack == 'g':
                    # boardbot tasks are crazy hard without bdhq!
                    # remove this later after bdhq is in
                    cogCount *= 0.7
            elif modifier == 'cogLevelMin':
                cogLevelMin = min(round(2 + (difficulty ** 0.5)), 12) + rng.randint(-1, 1)
                cogCount = cogCount * (1.0 - (cogLevelMin / 17))
            elif modifier == 'executive':
                executive = True
                cogCount *= 0.38
            elif modifier == 'manager':
                manager = True

        cogLocation = None

        # Chance for it to be location based
        if not ("cogType" in modifiers or "manager" in modifiers):
            locDict = {}
            # 35% Chance to be Cog HQ related zone, if applicable
            if rng.random() < 0.35 and zoneId in (DaisyGardens, MinniesMelodyland, TheBrrrgh, OutdoorZone, DonaldsDreamland):
                hqs = (SellbotHQ, CashbotHQ, LawbotHQ, BossbotHQ)  # TODO: Add Boardbot HQ eventually
                zoneRange = 0
                if zoneId:
                    if zoneId == DaisyGardens:
                        zoneRange = 1
                    elif zoneId == MinniesMelodyland:
                        zoneRange = 2
                    elif zoneId == TheBrrrgh:
                        zoneRange = 3
                    elif zoneId == OutdoorZone:
                        zoneRange = 4
                    elif zoneId == DonaldsDreamland:
                        zoneRange = 4  # TODO: 5 for boardbot eventually
                elif questTier:
                    tier2ZoneRange = {QuestTier.DG: 1, QuestTier.MML: 2, QuestTier.TB: 3, QuestTier.AA: 4, QuestTier.DDL: 4}
                    zoneRange = tier2ZoneRange[questTier]
                else:
                    zoneRange = 4
                for i in range(zoneRange):
                    locDict[hqs[i]] = 0.6  # HQ specific is 40% less cogs

                # Ignore DG for AnyCogHQ, since DG toons can only do SBHQ
                if zoneId in (MinniesMelodyland, TheBrrrgh, OutdoorZone, DonaldsDreamland):
                    locDict[SpecialQuestZones.AnyCogHQ] = 0.8  # Any HQ is 20% less cogs

                cogLocation = rng.choice(tuple(locDict.keys()))

                # Chance for HQ specific cog tasks to ask for skelecogs, with a lower count
                if rng.random() < 0.4:
                    skelecog = True
                    cogCount *= 0.35
                    # Cut them down slightly *again* if its a Bossbot HQ task. They don't have much.
                    if cogLocation == BossbotHQ:
                        cogCount *= 0.66

                if cogTrack:
                    if cogTrack == 'g':
                        # We have this because boardbot cog tasks are
                        # crazy hard without bdhq!
                        # Remove after we have bdhq.
                        # This is to undo a previous operation that decreased boardbot tasks by 30%
                        cogCount /= 0.7
                    cogTrack = None  # No cog tracks if it is in an hq
                    cogCount /= 0.75  # Undo the operation that nerfs the quest requirements

                # Ever so slightly buff the cog level min for HQ objectives
                if cogLevelMin:
                    cogLevelMin += 1

            # 25% Chance to be Playground related zone
            elif rng.random() < 0.25:
                locDict = {zoneId: 0.5}  # PG Wildcard is 50% less cogs
                for zone in HoodHierarchy.get(zoneId, []):
                    locDict[zone] = 0.25  # Branch specific is 75% less cogs

                cogLocation = rng.choice(tuple(locDict.keys()))

                if cogLevelMin and zoneId not in AllowLevelsHigherThanZone:
                    if cogLocation in HoodHierarchy.get(zoneId, []):
                        # This quest is for a specific street
                        highestBranchLevel = SuitHoodGlobals.SuitHoodInfo.get(cogLocation).getCogMax()
                        cogLevelMin = min(cogLevelMin, highestBranchLevel)

            if cogLocation:
                # Multiply by the cog count modifier given by this zone.
                cogCount *= locDict.get(cogLocation)

        if manager:
            cogCount = 0.5 * difficulty
            if cogLevelMin:
                cogLevelMin += 5
                cogCount *= 0.75

        # 30% chance to have a large boosted level amount (will also lower count)
        if zoneId in AllowBoostedLevelKudosZones and cogLevelMin and (cogLocation is None or cogLocation in AllowLevelsHigherThanZone) and rng.random() <= 0.30:
            boostedLevelAmt = AnywhereBoostedLevelPossible if cogLocation is None else rng.randrange(1, BoostedLevelPossibleZones[cogLocation] + 1)
            cogLevelMin += boostedLevelAmt
            cogCount *= (1.0 - (0.1 * boostedLevelAmt))

        # Round off our cog count so that it is pretty.
        cogCount = math.ceil(cogCount)
        if cogCount < 1:
            cogCount = 1
        elif cogCount < 10:
            pass
        elif cogCount < 20:
            cogCount = round(round(cogCount / 2) * 2)
        elif cogCount < 50:
            cogCount = round(round(cogCount / 5) * 5)
        elif cogCount < 100:
            cogCount = round(round(cogCount / 10) * 10)
        elif cogCount < 200:
            cogCount = round(round(cogCount / 20) * 20)
        elif cogCount < 2000:
            cogCount = round(round(cogCount / 50) * 50)
        else:
            cogCount = round(round(cogCount / 100) * 100)

        # Return our objective.
        return cls(
            cogCount=math.ceil(cogCount),
            cogLocation=cogLocation,
            cogType=cogType,
            cogTrack=cogTrack,
            cogLevelMin=cogLevelMin,
            executive=executive,
            manager=manager,
            skelecog=skelecog,
            npcReturnable=False,
        )

    def getCompletionRequirement(self) -> int:
        return self.cogCount

    @staticmethod
    def getObjectiveWeight(questerType: QuesterType) -> int:
        return 100

    def getLowestToonLevel(self) -> Optional[int]:
        if self.cogLocation and ZoneUtil.isCogHQZone(self.cogLocation):
            return LowestToonLevelPerHQ[ZoneUtil.getHoodId(self.cogLocation)]

        return self.lowestToonLevel

    def getReturnPosterColor(self):
        if self.executive:
            return 'darkGrey'
        elif self.manager:
            return 'red'
        else:
            return 'blue'

    def modifyPoster(self, questReference: QuestReference, poster):
        complete = questReference.isQuestComplete(base.localAvatar, self.objectiveIndex)
        cogPoster = poster.CENTER if not (complete and self.npcReturnable) else poster.LEFT
        self.setCogFrame(cogPoster, poster, complete)

        # If we're complete, bonus info
        if complete:
            if self.npcReturnable:
                poster.visual_setFrameColor(poster.RIGHT, self.getReturnPosterColor())
                poster.visual_setNpcFrame(poster.RIGHT, self.getToNpcId())
                poster.visual_setFrameText(poster.RIGHT, self.getToNpcName())
                poster.label_auxillaryText.show()
        # And if we're not, show progress
        else:
            value, range, textFormat = self.getProgressFormat(questReference)
            poster.visual_setProgressInfo(value=value, range=range, textFormat=textFormat)
            if self.cogCount == 1:
                poster.waitbar_questProgress.hide()

    def getProgressFormat(self, questReference):
        return questReference.getQuestProgress(self.objectiveIndex), self.cogCount, PROG_Defeat

    def setCogFrame(self, cogPoster, poster, complete=False, declarative=False):
        if self.executive:
            poster.visual_setFrameColor(cogPoster, 'darkGrey')
        elif self.manager:
            poster.visual_setFrameColor(cogPoster, 'red')
        else:
            poster.visual_setFrameColor(cogPoster, 'blue')
        if self.cogType == 'mplayer':
            poster.visual_setFrameText(cogPoster, 'Perform With Dave')
        else:
            prefix = PFX_DEFEAT if not declarative else ''
            poster.visual_setFrameText(cogPoster, prefix + self.getCogNameString(declarative=declarative, count=self.cogCount))
        if self.cogTrack is not None and not self.skelecog:
            cogIcons = loader.loadModel('phase_3/models/gui/cog_icons')
            icon = cogIcons.find({
                'c': '**/CorpIcon',
                's': '**/SalesIcon',
                'l': '**/LegalIcon',
                'm': '**/MoneyIcon',
                'g': '**/BoardIcon',
            }.get(self.cogTrack))
            geom = icon.copyTo(hidden)
            # from toontown.suit.Suit import Suit
            # geom.setColor(Suit.medallionColors[self.cogTrack])
            poster.visual_setFrameGeom(cogPoster, geom, scale=0.12)
            cogIcons.removeNode()
        elif self.cogType is None:
            # Any cog will do
            iconScale = 0.15
            if self.skelecog:
                bookModel = loader.loadModel("phase_3.5/models/gui/stickerbook_gui")
                lIconGeom = bookModel.find("**/skelecog5")
                bookModel.removeNode()
                iconScale = 0.13
            elif self.virtual:
                statusEffectImages = base.loader.loadModel('phase_3.5/models/gui/battlegui/status_effects')
                lIconGeom = statusEffectImages.find('**/virtual_icon')
                statusEffectImages.removeNode()
            else:
                cogIcons = loader.loadModel('phase_3/models/gui/cog_icons')
                lIconGeom = cogIcons.find('**/cog')
                cogIcons.removeNode()
            poster.visual_setFrameGeom(cogPoster, lIconGeom, scale=iconScale)
        else:
            # Use a suit head

            # This block obscures managers if the local player has not encountered them
            # This also acts as a spoiler protection from people with completed tasks
            isMgr = False
            if not complete and base.localAvatar:
                lavGal = base.localAvatar.getGalleryStatus()
                isMgr = self.cogType in COG_MINIBOSSES
                if (lavGal.get(self.cogType, 0) <= 0) and isMgr:  # Only want to obscure manager cogs
                    silhouette = True
                else:
                    silhouette = False
            else:
                silhouette = False
            poster.visual_setSuitHead(cogPoster, self.cogType, silhouette=silhouette)
            if isMgr:
                poster.visual_setFrameColor(cogPoster, 'red')

    def getInfoTextStrings(self, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex) and self.npcReturnable:
            # Return the goal location
            return super().getInfoTextStrings(questReference)
        else:
            # Tell them where the cogs are
            return self.getLocationName(self.cogLocation),

    def getSpeedchatMessages(self, quester, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(quester, self.objectiveIndex):
            if self.npcReturnable:
                return self.getFinishToontaskStrings()
            return tuple()

        # Get the message formatting.
        cogName = self.getCogNameString(speedchat=True, count=self.cogCount)
        forceSingle = False
        if self.taskManagerBoss and self.cogLocation and '\n' in self.getLocationName(zoneId=self.cogLocation):
            forceSingle = True
        if self.cogLocation is None or forceSingle:
            message = SC_Defeat
            return message % cogName,
        else:
            message = SC_DefeatLocation
            locName = self.getLocationName(zoneId=self.cogLocation)
            return message % (cogName, locName),

    def getHeadline(self, questReference: QuestReference, objectiveSelected: int = 0) -> str:
        return HL_Wanted
    
    def getObjectiveGoal(self) -> str:
        return OBJ_Defeat % self.getCogNameString(count=self.cogCount)
    
    def getProgressString(self, questReference: QuestReference, progress: int) -> str:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex):
            return QuestProgress_Complete
        elif self.cogCount == 1:
            return ''
        return PROG_Defeat.format(value=min(progress, self.cogCount), range=self.cogCount)

    """text makin methods"""

    @property
    def genericCogName(self):
        if self.virtual:
            return TTLocalizer.VirtualSkeleton
        elif self.skelecog:
            return TTLocalizer.Skeleton
        else:
            return TTLocalizer.Cog

    @property
    def genericCogNameP(self):
        if self.virtual:
            return TTLocalizer.VirtualSkeletonP
        elif self.skelecog:
            return TTLocalizer.SkeletonP
        else:
            return TTLocalizer.Cogs

    def getCogNameString(self, forcePlural=False, declarative=False, speedchat=False, count=0):
        cogTrackName = SuitDNA.suitDeptFullnames.get(self.cogTrack)
        prefix = '' if self.cogLevelMin is None else f'Level {self.cogLevelMin}+ '
        prefix += '' if not self.executive else 'Executive '
        prefix += '' if not self.manager else 'Manager '
        if speedchat:
            if count == 1:
                if self.taskManagerBoss:
                    return f'the {TTLocalizer.suitName(self.cogType, index=0)}'
                elif self.cogTrack:
                    return f"a {prefix}{cogTrackName}"
                elif self.cogType is None:
                    return f"a {prefix}{self.genericCogName}"
                else:
                    name = f"{prefix}{TTLocalizer.suitName(self.cogType, index=0)}"
                    name = ('an ' if name.lower()[0] in ('a', 'e', 'i', 'o', 'u') else 'a ') + name
                    return name
            else:
                if self.cogTrack:
                    return f"some {prefix}{cogTrackName}s"
                elif self.cogType is None:
                    return f"some {prefix}{self.genericCogNameP}"
                else:
                    return f"some {prefix}{TTLocalizer.suitName(self.cogType, index=2)}"
        if declarative:
            # Then the cog name.
            if self.taskManagerBoss:
                return f'The {TTLocalizer.suitName(self.cogType, index=0)}'
            elif self.cogTrack:
                return f"{prefix or 'The '}{cogTrackName}s"
            elif self.cogType is None:
                return f'{prefix}{self.genericCogNameP}'
            else:
                return f"{prefix}{TTLocalizer.suitName(self.cogType, index=2)}"
        if count == 1 and not forcePlural:
            if self.taskManagerBoss:
                return f'The {TTLocalizer.suitName(self.cogType, index=0)}'
            elif self.cogTrack:
                return f"A {prefix}{cogTrackName}"
            elif self.cogType is None:
                return f'A {prefix}{self.genericCogName}'
            else:
                name = f'{prefix}{TTLocalizer.suitName(self.cogType, index=0)}'
                name = ('an ' if name.lower()[0] in ('a', 'e', 'i', 'o', 'u') else 'a ') + name
                return name
        elif self.cogTrack:
            return f'{count} {prefix}{cogTrackName}s'
        elif self.cogType is None:
            return f'{count} {prefix}{self.genericCogNameP}'
        else:
            return f'{count} {prefix}{TTLocalizer.suitName(self.cogType, index=2)}'

    def getLocationName(self, zoneId: int = None, lowercaseAnywhere: bool = False, raw: bool = False):
        if zoneId in QuestLocalizer.DefeatCogZoneNames:
            return QuestLocalizer.DefeatCogZoneNames.get(zoneId)
        return super().getLocationName(zoneId, lowercaseAnywhere, raw)

    def _getKwargStr(self):
        kwargstr = super()._getKwargStr()
        if self.cogCount != 1:
            kwargstr += f'cogCount={self.cogCount}, '
        if self.cogLocation:
            kwargstr += f'cogLocation={self._numToLocStr(self.cogLocation)}, '
        if self.cogType:
            kwargstr += f"cogType='{self.cogType}', "
        if self.cogTrack:
            kwargstr += f"cogTrack='{self.cogTrack}', "
        if self.cogLevelMin:
            kwargstr += f"cogLevelMin={self.cogLevelMin}, "
        if self.executive:
            kwargstr += f'executive={self.executive}, '
        if self.manager:
            kwargstr += f'manager={self.manager}'
        if self.skelecog:
            kwargstr += f'skelecog={self.skelecog}'
        if self.virtual:
            kwargstr += f'virtual={self.virtual}'
        if self.revives:
            kwargstr += f'revives={self.revives}'
        if self.boss:
            kwargstr += f'boss={self.boss}, '
        return kwargstr

    def __repr__(self):
        return f'DefeatCogObjective({self._getKwargStr()[:-2]})'
