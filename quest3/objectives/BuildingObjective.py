import math

from toontown.quest3.QuestLocalizer import HL_Wanted, OBJ_Defeat, PROG_Defeat, QuestProgress_Complete, SC_Building, \
    PFX_TAKEDOWN
from toontown.quest3.base.QuestObjective import *
from toontown.quest3.context.BuildingContext import BuildingContext
from toontown.quest3.daily.DailyConstants import QuestTierToPlayground
from toontown.suit import SuitDNA


PlaygroundToMinimumFloor = {
    ToontownGlobals.MinniesMelodyland: 3,
    ToontownGlobals.TheBrrrgh: 4,
    ToontownGlobals.OutdoorZone: 5,
    ToontownGlobals.DonaldsDreamland: 5,
}


class BuildingObjective(QuestObjective):
    def __init__(self,
                 npc=2001,
                 rewards=None,
                 nextStep=None,
                 npcReturnable: bool = True,
                 zoneUnlocks=None,
                 buildingLocation: int = None,
                 cogTrack: str = None,
                 floorMinimum: int = 1,
                 buildingCount: int = 1,
                 wantFloors: bool = False):
        super().__init__(npc=npc, rewards=rewards, nextStep=nextStep, npcReturnable=npcReturnable, zoneUnlocks=zoneUnlocks)
        self.cogTrack = cogTrack
        self.floorMinimum = floorMinimum
        self.buildingLocation = buildingLocation
        self.buildingCount = buildingCount
        self.wantFloors = wantFloors

    def calculateProgress(self, context: BuildingContext, questReference: QuestReference, quester: Quester) -> int:
        if type(context) is not BuildingContext:
            return 0

        # Match zone id.
        zoneId = context.zoneId

        if self.buildingLocation is not None:
            # Match by Hood
            if ZoneUtil.getHoodId(self.buildingLocation) == self.buildingLocation:
                if ZoneUtil.getHoodId(self.buildingLocation) != ZoneUtil.getHoodId(zoneId):
                    # This cog was killed in the wrong hood.
                    return 0

            # Match by Branch
            elif ZoneUtil.getBranchZone(self.buildingLocation) == self.buildingLocation:
                if ZoneUtil.getBranchZone(self.buildingLocation) != ZoneUtil.getBranchZone(zoneId):
                    # This cog was killed in the wrong branch.
                    return 0

            # Undefined match
            else:
                raise AttributeError("DefeatCogObjective given undefined zoneId to parse")

        # Match the other args.
        if self.cogTrack is not None:
            if self.cogTrack != context.track:
                return 0

        if self.floorMinimum > context.floors:
            return 0

        # This building counts.
        if self.wantFloors:
            return context.floors
        return 1

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
        return 3, None

    @staticmethod
    def getObjectiveWeight(questerType: QuesterType) -> int:
        """
        The likelihood for this objective to be chosen in a pool.
        The de facto amount is 100.
        """
        return 35

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

        # 40% chance to be building floors.
        wantFloors = rng.random() <= 0.7
        if wantFloors:
            buildingCount = 0.5 * (difficulty ** 1.37)
            floorMinimum = 1
            cogTrack = None
        else:
            buildingCount = 0.4 * (difficulty ** 1.37)
            cogTrack = None

            # Roll floor minimum.
            floorMinimumDict = {
                1: 0.95,
                2: 0.75,
                3: 0.55,
                4: 0.35,
                5: 0.25,
                6: 0.15,
            }

            floorRangeMinimum = 1
            zoneId = extraArgs.get('zoneId')
            questTier = extraArgs.get('questTier')
            if questTier is not None:
                zoneId = QuestTierToPlayground.get(questTier, ToontownGlobals.ToontownCentral)
            if zoneId is not None:
                floorRangeMinimum = PlaygroundToMinimumFloor.get(zoneId, 1)
            # First, roll the amount of max floors to pick from.
            floorMinimum = min(int((difficulty / 3.0)), 6)
            # Then, randomly pick a floor.
            if floorRangeMinimum >= floorMinimum + 1:
                floorMinimum = floorRangeMinimum
            else:
                floors = list(range(floorRangeMinimum, floorMinimum + 1))
                floorMinimum = rng.choices(floors, [f ** 2 for f in floors])[0]
            buildingCount *= floorMinimumDict.get(floorMinimum)

            # Roll a cog track.
            if rng.random() < 0.33:
                cogTracks = ['s', 'm', 'l', 'c', 'g']
                cogTrack = rng.choice(cogTracks)
                buildingCount *= 0.66

        # Round off our building count so that it is pretty.
        buildingCount = math.ceil(buildingCount)
        if buildingCount < 1:
            buildingCount = 1
        elif buildingCount < 20:
            pass
        elif buildingCount < 50:
            buildingCount = round(round(buildingCount / 2) * 2)
        else:
            buildingCount = round(round(buildingCount / 5) * 5)
        
        # Building time
        return cls(
            buildingCount=buildingCount,
            floorMinimum=floorMinimum,
            cogTrack=cogTrack,
            npcReturnable=False,
            wantFloors=wantFloors,
        )
    
    def getCompletionRequirement(self) -> int:
        return self.buildingCount

    def modifyPoster(self, questReference: QuestReference, poster):
        complete = questReference.isQuestComplete(base.localAvatar, self.objectiveIndex)
        buildingPoster = poster.CENTER if not (complete and self.npcReturnable) else poster.LEFT

        geom, offset = self.getBuildingIconGeom()
        poster.fitGeometry(geom=geom, fFlip=0)
        if self.cogTrack:
            self.loadElevator(geom, self.floorMinimum)
            poster.visual_setFrameGeom(
                buildingPoster, geom=geom, scale=0.15, 
                pos=(-0.06 + offset, 10, 0), hpr=(180, 0, 0)
            )
        else:
            poster.visual_setFrameGeom(buildingPoster, geom=geom, scale=0.13)
        buildingName = self.getBuildingName(capitalize=True, accurate=True)
        if not complete:
            buildingName = buildingName[0].lower() + buildingName[1:]
            visualStr = PFX_TAKEDOWN + buildingName
        else:
            visualStr = buildingName
        poster.visual_setFrameText(buildingPoster, visualStr, maxRows=1 if complete else 2)
        poster.visual_setFrameColor(buildingPoster, 'blue')

        # If we're complete, bonus info
        if complete:
            if self.npcReturnable:
                poster.visual_setFrameColor(poster.RIGHT, 'blue')
                poster.visual_setNpcFrame(poster.RIGHT, self.getToNpcId())
                poster.visual_setFrameText(poster.RIGHT, self.getToNpcName())
                poster.label_auxillaryText.show()
        # And if we're not, show progress
        else:
            if self.buildingCount > 1:
                value, range, textFormat = self.getProgressFormat(questReference)
                poster.visual_setProgressInfo(value=value, range=range, textFormat=textFormat)

    def getProgressFormat(self, questReference):
        return questReference.getQuestProgress(self.objectiveIndex), self.buildingCount, PROG_Defeat

    def getInfoTextStrings(self, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex) and self.npcReturnable:
            # Return the goal location
            return super().getInfoTextStrings(questReference)
        else:
            # Tell them where the cogs are
            return self.getLocationName(self.buildingLocation),

    def getSpeedchatMessages(self, quester, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(quester, self.objectiveIndex):
            if self.npcReturnable:
                return self.getFinishToontaskStrings()
            return tuple()

        # Get the message formatting.
        buildingName = self.getBuildingName()

        # Get locaton formatting.
        locName = ''
        if self.buildingLocation is not None:
            locName = self.getLocationName(zoneId=self.buildingLocation)

        return SC_Building % (buildingName, locName),

    def getHeadline(self, questReference: QuestReference, objectiveSelected: int = 0) -> str:
        return HL_Wanted
    
    def getObjectiveGoal(self) -> str:
        return OBJ_Defeat % self.getBuildingName()
    
    def getProgressString(self, questReference: QuestReference, progress: int) -> str:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex):
            return QuestProgress_Complete
        elif self.buildingCount == 1:
            return ''
        return PROG_Defeat.format(value=min(progress, self.buildingCount), range=self.buildingCount)

    """a little methodology"""

    def getBuildingName(self, capitalize=False, accurate=False):
        if self.wantFloors:
            return f"{self.buildingCount} Building Floor{'s' if self.buildingCount > 1 else ''}"

        buildingName = 'a ' if self.buildingCount == 1 else ('some ' if not accurate else f'{self.buildingCount} ')
        if capitalize:
            buildingName = buildingName[0].upper() + buildingName[1:]
        if self.floorMinimum != 1:
            numberName = {
                2: 'two+',
                3: 'three+',
                4: 'four+',
                5: 'five+',
                6: 'six',
            }.get(self.floorMinimum) + (' story ' if not capitalize else ' Story ')
            if capitalize:
                numberName = numberName[0].upper() + numberName[1:]
            buildingName = buildingName + numberName
        if self.cogTrack is not None:
            suitName = SuitDNA.suitDeptFullnames.get(self.cogTrack)
            buildingName = buildingName + suitName + ' '
        buildingName = buildingName + 'Cog Building' + ('' if self.buildingCount == 1 else 's')
        return buildingName

    def getBuildingIconGeom(self):
        if self.cogTrack:
            filepath, offset = {
                'c': ('phase_4/models/modules/suit_landmark_corp', -0.02),
                'l': ('phase_4/models/modules/suit_landmark_legal', 0.0),
                'm': ('phase_4/models/modules/suit_landmark_money', 0.0),
                's': ('phase_4/models/modules/suit_landmark_sales', 0.0),
                'g': ('phase_4/models/modules/suit_landmark_board', 0.02),
            }.get(self.cogTrack)
            return loader.loadModel(filepath), offset

        bookModel = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
        geom = bookModel.find('**/COG_building')
        bookModel.removeNode()
        return geom, 0

    @staticmethod
    def loadElevator(building, numFloors):
        elevatorNodePath = hidden.attachNewNode('elevatorNodePath')
        elevatorModel = loader.loadModel('phase_4/models/modules/elevator')
        floorIndicator = [None, None, None, None, None, None]
        npc = elevatorModel.findAllMatches('**/floor_light_?;+s')
        for np in npc:
            floor = int(np.getName()[-1:]) - 1
            floorIndicator[floor] = np
            if floor < numFloors:
                np.setColor(Vec4(0.5, 0.5, 0.5, 1.0))
            else:
                np.hide()

        elevatorModel.reparentTo(elevatorNodePath)
        suitDoorOrigin = building.find('**/*_door_origin')
        elevatorNodePath.reparentTo(suitDoorOrigin)
        elevatorNodePath.setPosHpr(0, 0, 0, 0, 0, 0)

    def _getKwargStr(self):
        kwargstr = super()._getKwargStr()
        if self.buildingLocation is not None:
            kwargstr += f'buildingLocation={self._numToLocStr(self.buildingLocation)}, '
        if self.cogTrack is not None:
            kwargstr += f"cogTrack='{self.cogTrack}', "
        if self.floorMinimum != 1:
            kwargstr += f"floorMinimum={self.floorMinimum}, "
        if self.buildingCount != 1:
            kwargstr += f"buildingCount={self.buildingCount}, "
        return kwargstr

    def __repr__(self):
        return f'BuildingObjective({self._getKwargStr()[:-2]})'
