from panda3d.core import CardMaker
from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectButton
from direct.gui import DirectGuiGlobals as DGG
from direct.task import Task
from toontown.gui.ScaledFrame import ScaledFrame
from toontown.quest3.QuestEnums import QuestSource
from toontown.quest3.base.QuestLine import QuestLine
from toontown.quest3.base.QuestObjective import MultiObjective, QuestObjective
from toontown.quest3.base.QuestReference import QuestId, QuestReference
from toontown.quest3.objectives.InvestigateObjective import InvestigateObjective
from toontown.quest3.objectives.QuestFishObjective import QuestFishObjective
from toontown.hood import ZoneUtil
from toontown.quest3.objectives.TossPieObjective import TossPieObjective
from toontown.quest3.objectives.VisitObjective import VisitObjective
from toontown.toonbase import ToontownGlobals
from toontown.quest3.base import QuestGlobals
from toontown.suit import SuitHoodGlobals
from toontown.quest3.gui import QuestMapGlobals
from toontown.shtiker import SuitPage
from toontown.shtiker import CogPageGlobals
from toontown.toonbase.ToontownGlobals import *


class QuestMap(DirectFrame):
    def __init__(self, av, **kw):
        DirectFrame.__init__(self, relief = None, sortOrder = 50)
        self.initialiseoptions(QuestMap)
        self.container = DirectFrame(parent = self, relief = None)
        self.marker = DirectFrame(parent = self.container, relief = None)
        self.cogInfoFrame = DirectFrame(parent = self.container, relief = DGG.RAISED)
        cm = CardMaker('bg')
        cm.setFrame(-0.5, 0.5, -0.5, 0.5)
        bg = self.cogInfoFrame.attachNewNode(cm.generate())
        bg.setTransparency(1)
        bg.setColor(0.5, 0.5, 0.5, 0.5)
        bg.setBin('fixed', 0)

        self.cogInfoFrame['geom'] = bg
        self.cogInfoFrame['geom_pos'] = (0, 0, -0.4)
        self.cogInfoFrame['geom_scale'] = (6, 1, 5.2)
        self.cogInfoFrame['borderWidth'] = (0.12, 0.12)
        self.cogInfoFrame['pad'] = (0, 0)
        self.cogInfoFrame['frameColor'] = (0.3, 0.25, 0.25, 0.3)
        self.cogInfoFrame.setScale(0.05)
        self.cogInfoFrame.setPos(0, 0, 0.6)

        self.buildingMarkers = []
        self.suitBuildingMarkers = []
        self.questBlocks = []
        self.av = av

        self.wantToggle = ConfigVariableBool('want-toggle-quest-map', True).getValue()

        self.updateMarker = True
        self.cornerPosInfo = None
        self.hqPosInfo = None
        self.fishingSpotInfo = None
        self.load()
        self.setScale(1.5)
        self.setAlphaScale(0.8)
        bg.removeNode()
        self.hoodId = None
        self.zoneId = None
        self.suitPercentage = {}
        self.sidequestsMade = []
        self.mapImage = None

        for zoneId, branchDef in SuitHoodGlobals.SuitHoodInfo.items():
            spawnDef = branchDef.getCogSpawnDefinition()
            self.suitPercentage[zoneId] = (spawnDef.getCogTrackChances(), spawnDef.getExecutiveSpawnChance())

        return

    def load(self):
        gui = loader.loadModel('phase_4/models/questmap/questmap_gui')
        icon = gui.find('**/tt_t_gui_qst_arrow')
        iconNP = aspect2d.attachNewNode('iconNP')
        icon.reparentTo(iconNP)
        icon.setR(90)
        self.marker['geom'] = iconNP
        self.marker['image'] = iconNP
        self.marker.setScale(0.05)
        iconNP.removeNode()
        self.mapOpenButton = DirectButton(
            image = (
                gui.find('**/tt_t_gui_qst_mapClose'),
                gui.find('**/tt_t_gui_qst_mapClose'),
                gui.find('**/tt_t_gui_qst_mapTryToOpen')
            ),
            relief = None,
            pos = (-0.08, 0, 0.37),
            parent = base.a2dBottomRight,
            scale = 0.205,
            command = self.show
        )
        self.mapCloseButton = DirectButton(
            image = (
                gui.find('**/tt_t_gui_qst_mapOpen'),
                gui.find('**/tt_t_gui_qst_mapOpen'),
                gui.find('**/tt_t_gui_qst_mapTryToClose')
            ),
            relief = None,
            pos = (-0.08, 0, 0.37),
            parent = base.a2dBottomRight,
            scale = 0.205,
            command = self.hide
        )
        self.mapOpenButton.hide()
        self.mapCloseButton.hide()
        gui.removeNode()
        icons = loader.loadModel('phase_3/models/gui/cog_icons')
        cIcon = icons.find('**/CorpIcon')
        lIcon = icons.find('**/LegalIcon')
        mIcon = icons.find('**/MoneyIcon')
        sIcon = icons.find('**/SalesIcon')
        gIcon = icons.find('**/BoardIcon')
        cogInfoTextColor = (0.2, 0.2, 0.2, 1)
        textPos = (1.1, -0.2)
        textScale = 0.8
        self.cInfo = DirectLabel(
            parent = self.cogInfoFrame, text = '', text_fg = cogInfoTextColor, text_pos = textPos,
            text_scale = textScale, geom = cIcon, geom_pos = (-0.1, 0, 0), geom_scale = 0.6,
            relief = None)
        self.cInfo.setPos(0.8, 0, 0.5)
        self.lInfo = DirectLabel(
            parent = self.cogInfoFrame, text_fg = cogInfoTextColor, text = '', text_pos = textPos,
            text_scale = textScale, geom = lIcon, geom_pos = (-0.1, 0, 0), geom_scale = 0.6,
            relief = None)
        self.lInfo.setPos(-2.2, 0, -0.5)
        self.mInfo = DirectLabel(
            parent = self.cogInfoFrame, text_fg = cogInfoTextColor, text = '', text_pos = textPos,
            text_scale = textScale, geom = mIcon, geom_pos = (-0.1, 0, 0), geom_scale = 0.6,
            relief = None)
        self.mInfo.setPos(0.8, 0, -0.5)
        self.sInfo = DirectLabel(
            parent = self.cogInfoFrame, text_fg = cogInfoTextColor, text = '', text_pos = textPos,
            text_scale = textScale, geom = sIcon, geom_pos = (-0.1, 0, 0), geom_scale = 0.6,
            relief = None)
        self.sInfo.setPos(-0.75, 0, -1.5)
        self.gInfo = DirectLabel(
            parent = self.cogInfoFrame, text_fg = cogInfoTextColor, text = '', text_pos = textPos,
            text_scale = textScale, geom = gIcon, geom_pos = (-0.1, 0, 0), geom_scale = 0.6,
            relief = None)
        self.gInfo.setPos(-2.2, 0, 0.5)
        self.execInfo = DirectLabel(
            parent = self.cogInfoFrame, text_fg = cogInfoTextColor, text = '',
            text_pos = (0.8, -0.2), text_scale = (0.675, 0.675), relief = None)
        self.execInfo.setPos(-0.75, 0, -2.5)
        self.streetInfo = DirectLabel(
            parent = self.cogInfoFrame, text_fg = cogInfoTextColor, text = '',
            text_pos = (0, 1.4), text_scale = (0.675, 0.675), relief = None)
        icons.removeNode()
        return

    def loadCogInfo(self):
        streetName = StreetNames.get(ZoneUtil.getCanonicalBranchZone(self.zoneId))[2]
        trackPercentage, execChance = self.suitPercentage.get(self.zoneId)
        if trackPercentage is None:
            return
        self.gInfo['text'] = '%s%%' % trackPercentage.get('g', 0)
        self.cInfo['text'] = '%s%%' % trackPercentage.get('c', 0)
        self.lInfo['text'] = '%s%%' % trackPercentage.get('l', 0)
        self.mInfo['text'] = '%s%%' % trackPercentage.get('m', 0)
        self.sInfo['text'] = '%s%%' % trackPercentage.get('s', 0)
        self.execInfo['text'] = f'Exec. Chance: {execChance}%'
        self.streetInfo['text'] = streetName
        return

    def destroy(self):
        self.ignore('questPageUpdated')
        self.mapOpenButton.destroy()
        self.mapCloseButton.destroy()
        del self.mapOpenButton
        del self.mapCloseButton
        DirectFrame.destroy(self)

    def putBuildingMarker(self, pos, mapIndex = None, isSuitBlock = False, isSideQuest = False):
        marker = DirectLabel(
            parent = self.container,
            text = '',
            text_pos = (-0.05, -0.15),
            text_fg = (1, 1, 1, 1),
            relief = None
        )
        gui = loader.loadModel('phase_4/models/parties/schtickerbookHostingGUI')
        icon = gui.find('**/startPartyButton_inactive')
        iconNP = aspect2d.attachNewNode('iconNP')
        icon.reparentTo(iconNP)
        icon.setX(-12.0792 / 30.48)
        icon.setZ(-9.7404 / 30.48)
        marker['text'] = '%s' % mapIndex
        marker['text_scale'] = 0.7
        marker['image'] = iconNP
        if isSuitBlock:  # Make the bubble appear gray if a cog took over a task building
            marker['image_color'] = (0.5, 0.5, 0.5, 1)
        elif isSideQuest:
            marker['image_color'] = (1, 1, 0, 1)
        else:
            marker['image_color'] = (1, 0, 0, 1)
        marker['image_scale'] = 6
        marker.setScale(0.05)
        if pos:
            relX, relY = self.transformAvPos(pos)
            marker.setPos(relX, 0, relY)
            self.buildingMarkers.append(marker)
        iconNP.removeNode()
        gui.removeNode()
        return

    def putSuitBuildingMarker(self, pos, blockNumber = None, track = None, floors = None):
        if SuitPage.SuitPage.getDepartmentDefeated(SuitPage, CogPageGlobals.indexToCogDepartment.index(track)) >= 100:
            buildingLabelText = TTLocalizer.DepartmentBuildingFloor if floors == 1 else (TTLocalizer.DepartmentBuildingFloorS % floors)
            buildingLabelPosition = 3.45 if floors == 1 else 3.85
            floorLabel = ScaledFrame(
                parent=self.container,
                frameSize=(-0.5, buildingLabelPosition, -1 / 2, 1 / 2),
                # pos=(0.95, -0.2),
                text=buildingLabelText,
                text_font=ToontownGlobals.getSuitFont(),
                text_align=TextNode.ALeft,
                text_wordwrap=16,
                text_scale=0.7,
                text_pos=(0.7, -0.2),
                text_fg=(1, 1, 1, 1),
                scaledTexture='phase_3/maps/gui/ttcc_gui_scaledFrame_shadow.png'
            )
            marker = DirectButton(
                parent=self.container,
                frameSize=(-0.575, 0.575, -0.575, 0.575),
                text_pos=(0.95, -0.2),
                text_fg=(0, 0, 0, 1),
                text_shadow=(1, 1, 1, 0),
                text_align=TextNode.ALeft,
                text_scale=0.7,
                text_font=ToontownGlobals.getSuitFont(),
                relief=None,
                rolloverSound=None,
                clickSound=None,
                pressEffect=0
            )
            icon = self.getSuitIcon(track)
            iconNP = aspect2d.attachNewNode('suitBlock-%s' % blockNumber)
            icon.reparentTo(iconNP)
            marker['image'] = iconNP
            marker['image_scale'] = 1

            marker.bind(DGG.WITHIN, self.__handleMouseEnterBuilding, extraArgs=[floorLabel])
            marker.bind(DGG.WITHOUT, self.__handleMouseExitBuilding, extraArgs=[floorLabel])
            marker.setScale(0.05)
            floorLabel.setScale(0.05)
            floorLabel.hide()
            marker.floorLabel = floorLabel
            if pos:
                relX, relY = self.transformAvPos(pos)
                marker.setPos(relX, 0, relY)
                floorLabel.setPos(relX, 0, relY)
                self.suitBuildingMarkers.append(marker)
            iconNP.removeNode()
        else:
            pass

    def __handleMouseEnterBuilding(self, floorLabel, _):
        floorLabel.show()

    def __handleMouseExitBuilding(self, floorLabel, _):
        floorLabel.hide()

    def getSuitIcon(self, dept):
        icons = loader.loadModel('phase_3/models/gui/cog_icons')
        if dept == 'c':
            corpIcon = icons.find('**/CorpIcon')
        elif dept == 's':
            corpIcon = icons.find('**/SalesIcon')
        elif dept == 'l':
            corpIcon = icons.find('**/LegalIcon')
        elif dept == 'm':
            corpIcon = icons.find('**/MoneyIcon')
        elif dept == 'g':
            corpIcon = icons.find('**/BoardIcon')
        else:
            corpIcon = None
        icons.removeNode()
        return corpIcon

    def updateBuildingInfo(self):
        for blockIndex in range(base.cr.playGame.dnaStore.getNumBlockNumbers()):
            blockNumber = base.cr.playGame.dnaStore.getBlockNumberAt(blockIndex)
            if base.cr.playGame.dnaStore.isSuitBlock(
                blockNumber) and blockNumber not in self.questBlocks:  # check if bldg is a cog bldg
                self.putSuitBuildingMarker(
                    base.cr.playGame.dnaStore.getDoorPosHprFromBlockNumber(blockNumber).getPos(render),
                    blockNumber,
                    base.cr.playGame.dnaStore.getSuitBlockTrack(blockNumber),
                    base.cr.playGame.dnaStore.getSuitBlockFloors(blockNumber))

    def updateQuestInfo(self):
        """Creates all of the quest markers for currently available sidequests,
        as well as all currently owned quests based on the current branch zone.
        """
        # Get the branch zone of the avatar.
        branchZone = ZoneUtil.getCanonicalBranchZone(self.av.zoneId)

        # First, let's handle mapping out the sidequests.

        # Get all sidequests available on this street.
        availableSidequests = QuestGlobals.getAvailableSidequests(self.av, branchZone=branchZone)

        # Iterate through every sidequest QuestId.
        for i, questId in enumerate(availableSidequests):
            questId: QuestId
            # Create a QuestReference from the questId for useful
            # functionality.
            questReference = QuestReference(questId)
            # Get the (initial) MultiObjective from the questline.
            multiObjective: MultiObjective = QuestLine.dereferenceQuestReference(questReference, quester=self.av)

            # Iterate all of the objectives within this objective.
            for index, questObjective in enumerate(multiObjective.getQuestObjectives()):
                questObjective: QuestObjective

                # Create the building marker for this quest objective.
                self.labelQuestObjective(questObjective, questReference, True, index, "!")

        # Next, handle all of their current quest references.
        for i, questReference in enumerate(self.av.getVisibleQuests()):
            questReference: QuestReference
            # Get the (initial) MultiObjective from the questline.
            multiObjective: MultiObjective = QuestLine.dereferenceQuestReference(questReference, quester=self.av)

            # The number displayed on the icon.
            mapIndex = i + 1

            # Iterate all of the objectives within this objective.
            for index, questObjective in enumerate(multiObjective.getQuestObjectives()):
                questObjective: QuestObjective

                # Create the building marker for this quest objective.
                self.labelQuestObjective(questObjective, questReference, False, index, mapIndex)

    def labelQuestObjective(self, questObjective: QuestObjective,
                            questReference: QuestReference, start: bool, index: int, mapIndex) -> None:
        if not base.localAvatar:
            return

        # Get the quest ref properties.
        sidequest = questReference.getQuestSource() == QuestSource.SideQuest
        complete = questReference.isQuestComplete(base.localAvatar, index)

        # Figure out where the NPC is.
        if isinstance(questObjective, InvestigateObjective) and not complete:
            npcZoneId = questObjective.getZoneId()
        else:
            npcZoneId = questObjective.getFromNpcZone() if start else questObjective.getToNpcZone()

        hoodId = ZoneUtil.getCanonicalHoodId(npcZoneId)
        branchId = ZoneUtil.getCanonicalBranchZone(npcZoneId)

        if not start and not complete:
            # Use a specific building marker for fishing objectives.
            if isinstance(questObjective, QuestFishObjective) and \
                    (questObjective.fishLocation is None or
                     ZoneUtil.getCanonicalBranchZone(questObjective.fishLocation) == branchId):
                self.putBuildingMarker(self.fishingSpotInfo, mapIndex=mapIndex, isSideQuest=sidequest)
                return
            # Only allow incomplete visit quests (excluding toss pie objectives) to have markers.
            elif isinstance(questObjective, TossPieObjective) or not \
                    (isinstance(questObjective, VisitObjective) or isinstance(questObjective, InvestigateObjective)):
                return

        if (self.hoodId != hoodId) or (self.zoneId != branchId):  # sanity check?
            return

        for blockIndex in range(base.cr.playGame.dnaStore.getNumBlockNumbers()):
            blockNumber = base.cr.playGame.dnaStore.getBlockNumberAt(blockIndex)
            zoneId = base.cr.playGame.dnaStore.getZoneFromBlockNumber(blockNumber)
            interiorZoneId = (zoneId - (zoneId % 100)) + 500 + blockNumber
            if npcZoneId == interiorZoneId:
                self.questBlocks.append(blockNumber)

                door = base.cr.playGame.dnaStore.getDoorPosHprFromBlockNumber(blockNumber)
                # check if door exists
                if door:
                    self.putBuildingMarker(
                        door.getPos(render),
                        mapIndex = mapIndex,
                        isSuitBlock = base.cr.playGame.dnaStore.isSuitBlock(blockNumber),
                        isSideQuest = sidequest
                    )

    def transformAvPos(self, pos):
        if self.cornerPosInfo is None:
            print("ERR: map has no cornerPosInfo")
            return (0, 0)
        topRight = self.cornerPosInfo[0]
        bottomLeft = self.cornerPosInfo[1]
        relativeX = (pos.getX() - bottomLeft.getX()) / (topRight.getX() - bottomLeft.getX()) - 0.5
        relativeY = (pos.getY() - bottomLeft.getY()) / (topRight.getY() - bottomLeft.getY()) - 0.5

        return (relativeX, relativeY)

    def update(self, task):
        if self.av:
            if self.updateMarker:
                relX, relY = self.transformAvPos(self.av.getPos())
                self.marker.setPos(relX, 0, relY)
                self.marker.setHpr(0, 0, -180 - self.av.getH())

        return Task.cont

    def updateMap(self):
        if self.av and self.mapImage and not self.mapImage.isEmpty():
            self.destroyMarkers()
            self.updateQuestInfo()
            self.updateBuildingInfo()
            taskMgr.add(self.update, 'questMapUpdate')
        else:
            self.stop()

    def start(self):
        self.container.show()
        self.accept('questPageUpdated', self.updateMap)
        self.handleMarker()

        if self.av:
            hoodId = ZoneUtil.getCanonicalHoodId(self.av.getLocation()[1])
            zoneId = ZoneUtil.getCanonicalBranchZone(self.av.getLocation()[1])
            '''canMakeMap = ZoneUtil.getLoaderName(zoneId) == 'townLoader' and zoneId < 
            ToontownGlobals.DynamicZonesBegin
            if canMakeMap:'''
            try:
                mapsGeom = loader.loadModel('phase_4/models/questmap/%s_maps' % ToontownGlobals.dnaMap[hoodId])
                self.mapOpenButton.show()
                self.mapCloseButton.hide()
            except Exception:
                self.stop()
                return

            streetAddress = '%s_%s_english' % (ToontownGlobals.dnaMap[hoodId], zoneId)

            if mapsGeom.find('**/' + streetAddress + '_HW').isEmpty():
                self.mapImage = mapsGeom.find('**/' + streetAddress)
            else:
                # todo - if more holidays are added here, refactor this
                #  aprilToons check is here for erfit's building in particular
                # Not needed for AT 2023
                # if base.wantHalloween or (base.wantAprilFools and ConfigVariableBool('want-halloween-with-april-fools').getValue()):
                #     self.mapImage = mapsGeom.find('**/' + streetAddress + '_HW')
                # else:
                self.mapImage = mapsGeom.find('**/' + streetAddress)
            if not self.mapImage.isEmpty():
                self.container['image'] = self.mapImage
                self.resetFrameSize()
                self.cornerPosInfo = QuestMapGlobals.CornerPosTable.get(streetAddress)
                self.hqPosInfo = QuestMapGlobals.HQPosTable.get(streetAddress)
                self.fishingSpotInfo = QuestMapGlobals.FishingSpotPosTable.get(streetAddress)
                self.cogInfoPos = QuestMapGlobals.CogInfoPosTable.get(streetAddress)
                self.cogInfoFrame.setPos(self.cogInfoPos)
                self.hoodId = hoodId
                self.zoneId = zoneId
                self.loadCogInfo()
            else:
                self.stop()
            mapsGeom.removeNode()

    def initMarker(self, task):
        if self.av:
            if not hasattr(base.cr.playGame.getPlace(), 'isInterior') or not base.cr.playGame.getPlace().isInterior:
                relX, relY = self.transformAvPos(self.av.getPos())
                self.marker.setPos(relX, 0, relY)
                self.marker.setHpr(0, 0, -180 - self.av.getH())
                self.marker['geom_scale'] = 1.4 * task.time % 0.5 * 10 + 1
                self.marker['geom_color'] = (1, 1, 1, 0.8 - 1.4 * task.time % 0.5 * 2 / 0.8 + 0.2)
            if task.time < 1:
                return Task.cont
            else:
                self.marker['geom_color'] = (1, 1, 1, 0)
                return Task.done

    def show(self):
        self.updateMap()
        # taskMgr.add(self.initMarker, 'questMapInit')
        DirectFrame.show(self)
        self.mapOpenButton.hide()
        if self.container['image']:
            self.mapCloseButton.show()

    def hide(self):
        taskMgr.remove('questMapInit')
        DirectFrame.hide(self)
        if self.container['image']:
            self.mapOpenButton.show()
        self.mapCloseButton.hide()

    def toggle(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()

    def obscureButton(self):
        self.mapOpenButton.hide()
        self.mapCloseButton.hide()

    def stop(self):
        self.container['image'] = None
        self.destroyMarkers()
        self.container.hide()
        self.hide()
        self.obscureButton()
        self.ignore('questPageUpdated')
        taskMgr.remove('questMapUpdate')

    def destroyMarkers(self) -> None:
        for marker in self.buildingMarkers:
            marker.destroy()
        for marker in self.suitBuildingMarkers:
            marker.floorLabel.destroy()
            marker.destroy()

        self.buildingMarkers = []
        self.suitBuildingMarkers = []
        self.questBlocks = []

    def handleMarker(self):
        if hasattr(base.cr.playGame.getPlace(), 'isInterior') and base.cr.playGame.getPlace().isInterior:
            self.updateMarker = False
        else:
            self.updateMarker = True

    def acceptOnscreenHooks(self):
        if self.wantToggle:
            self.accept(base.STREET_MAP_KEY, self.toggle)
        else:
            self.accept(base.STREET_MAP_KEY, self.show)
            self.accept(base.STREET_MAP_KEY + '-up', self.hide)

    def ignoreOnscreenHooks(self):
        self.ignore(base.STREET_MAP_KEY)
        self.ignore(base.STREET_MAP_KEY + '-up')
        self.obscureButton()
