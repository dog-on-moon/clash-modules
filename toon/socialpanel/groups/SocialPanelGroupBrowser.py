"""
The ScrollWheelFrame containing SocialPanelGroup instances.
"""

from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from direct.gui.DirectGuiGlobals import FLAT
from direct.fsm.FSM import FSM
from direct.interval.IntervalGlobal import Func, Sequence, Parallel
from direct.interval.LerpInterval import LerpFunctionInterval
from direct.task.TaskManagerGlobal import taskMgr

from toontown.groups.GroupClasses import GroupClient
from toontown.groups.GroupFilterer import GroupFilterer
from toontown.toon.socialpanel.SocialPanelGUI import SelectorButton
from toontown.gui import TTGui
from toontown.gui.TTGui import ScrollWheelFrame
from toontown.toon.socialpanel.SocialPanelGlobals import *
from toontown.toon.socialpanel.groups.SocialPanelGroup import SocialPanelGroup, EmptySocialPanelGroup
from toontown.groups.GroupGlobals import *
from toontown.utils.ColorHelper import hexToPCol

from typing import List, TYPE_CHECKING

from toontown.utils.SequenceQueue import SequenceQueue

from toontown.toonbase.TTLocalizer import SocialPanelGroupFilterData as FILTER_DATA

if TYPE_CHECKING:
    from toontown.groups.DistributedGroupManager import DistributedGroupManager


STATE_BROWSER = 'Browser'
STATE_FILTER = 'Filter'


@DirectNotifyCategory()
class SocialPanelGroupBrowser(ScrollWheelFrame, FSM):

    DEFAULT_SIZE = (-1.93, 1.943, 0, 6.2)  # same in SocialPanelGroup.py
    CALLBACK_FAILURE_SIZE = 1
    SCROLLBAR_WIDTH = 0.39

    SELECTED_DARK = hexToPCol('3b5336')
    SELECTED_LIGHT = hexToPCol('92c084')
    SELECTED_GIGALIGHT = hexToPCol('bde8ae')

    accessClicked = hexToPCol('cccccc')
    accessUnclicked = hexToPCol('545454')

    # verticalScrollImageScale

    def __init__(self, parent, mgr):
        # create the filter settings
        selectorBgAlpha = 0.33
        self.selectorButton_category = SelectorButton(
            parent=parent, pos=(0.65, 0, 1.606-0.36), width=0.6, title='Category',
            frameSize=(-0.723, 0.394, -0.07, 0.07), frameColor=(0.42, 0.675, 0.384, selectorBgAlpha),
            callback=self.selector_updateCategory,
            darkCol=self.SELECTED_DARK, lightCol=self.SELECTED_GIGALIGHT,
        )
        self.selectorButton_type = SelectorButton(
            parent=parent, pos=(0.65, 0, 1.114-0.36), width=0.6, title='Type',
            frameSize=(-0.723, 0.394, -0.07, 0.07), frameColor=(0.302, 0.6, 0.259, selectorBgAlpha),
            callback=self.selector_updateType,
            darkCol=self.SELECTED_DARK, lightCol=self.SELECTED_LIGHT,
        )
        self.selectorButton_location = SelectorButton(
            parent=parent, pos=(0.65, 0, 0.622-0.36), width=0.6, title='Location',
            frameSize=(-0.723, 0.394, -0.07, 0.07), frameColor=(0.42, 0.675, 0.384, selectorBgAlpha),
            callback=self.selector_updateLocation,
            darkCol=self.SELECTED_DARK, lightCol=self.SELECTED_GIGALIGHT,
        )
        self.bottomFramePanel = DirectFrame(
            parent=parent, pos=(0.65, 0, 0.13-0.36), relief=DGG.FLAT, scale=0.42,
            frameSize=(-0.723, 0.394, -0.07, 0.07), frameColor=(0.302, 0.6, 0.259, selectorBgAlpha),
            text='Access', text_pos=(-0.555, -0.024), text_scale=0.08,
            text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1),
        )

        for button in (self.selectorButton_category, self.selectorButton_type, self.selectorButton_location):
            button.setScale(0.42)
            button['relief'] = DGG.FLAT
            button.titleText['text_pos'] = (-0.555, -0.020)
            button.titleText['text_scale'] = 0.08
            button.setOptions(
                values=[1],
                texts=["wip"],
                setIndex=0, wraparound=False,
            )
        for i, button in enumerate([self.selectorButton_category, self.selectorButton_type,
                                    self.selectorButton_location, self.bottomFramePanel]):
            button.setPos(0.07, 0, 0.365 - (i * 0.0587))
        self.button_availabilityAvailable = DirectButton(
            parent=parent, frameColor=(0.796, 0.702, 0.078, 1.0),
            relief=None, pos=(0, 0, 0.188),  # frameSize=(-0.15, 0.15, -0.1, 0.1),
            text='Available', text_scale=0.035, text_fg=Vec4(1, 1, 1, 1),
            text_shadow=Vec4(0, 0, 0, 1), text_pos=(0.0, -0.009),
            geom=(
                sp_gui.find('**/OrangeButton_N'),
                sp_gui.find('**/OrangeButton_P'),
                sp_gui.find('**/OrangeButton_H'),
            ), geom_scale=(0.06 * (164 / 63), 1, 0.06), geom_color=self.accessClicked,
            scale=0.8, command=self.enableRestrictMode,
        )
        self.button_availabilityAll = DirectButton(
            parent=parent, frameColor=(0.796, 0.702, 0.078, 1.0),
            relief=None, pos=(0.14, 0, 0.188),  # frameSize=(-0.15, 0.15, -0.1, 0.1),
            text='All', text_scale=0.035, text_fg=Vec4(1, 1, 1, 1),
            text_shadow=Vec4(0, 0, 0, 1), text_pos=(0.0, -0.009),
            geom=(
                sp_gui.find('**/OrangeButton_N'),
                sp_gui.find('**/OrangeButton_P'),
                sp_gui.find('**/OrangeButton_H'),
            ), geom_scale=(0.06 * (164 / 63), 1, 0.06), geom_color=self.accessUnclicked,
            scale=0.8, command=self.disableRestrictMode,
        )
        # Set up the ScrollWheelFrame properties of the SocialPanelGroupBrowser.
        self.verticalScrollImage = DirectFrame(
            parent=parent, relief=None, scale=0.104, pos=(0.21, 0, 0.023),
            image=sp_gui.find('**/ScrollBar_BAR'),
            image_scale=((49 / 714) * 7.7, 1, 7.21),
            # image_pos=(1.765, 0, 2.5),
        )
        ScrollWheelFrame.__init__(
            self, parent=parent, relief=FLAT, scale=0.12, pos=(0, 0, -0.349),
            frameSize=self.DEFAULT_SIZE,
            canvasSize=self.DEFAULT_CANVAS_SIZE,
            scrollBarWidth=self.SCROLLBAR_WIDTH,
            scrollDistance=0.4,
            manageScrollBars=0,
            frameColor=(0.224, 0.549, 0.259, 0.0),
            verticalScroll_relief=None,
        )
        self['verticalScroll_relief'] = None
        self['verticalScroll_thumb_relief'] = None
        # self['verticalScroll_thumb_frameSize'] = (-0.21, 0.21, -0.68, 0.68)
        self['verticalScroll_thumb_frameColor'] = (1, 0, 1, 1)
        self['verticalScroll_resizeThumb'] = 0
        self['verticalScroll_thumb_image'] = sp_gui.find('**/ScrollBar')
        self['verticalScroll_thumb_image_scale'] = (0.3987, 1, 0.39)  # ((58 / 154) * 1.47 * 1.1, 1, 1.47)
        self['verticalScroll_thumb_image_pos'] = (-0.0032, 0, 0)
        self.verticalScroll.incButton.destroy()
        self.verticalScroll.decButton.destroy()
        self.initialiseoptions(SocialPanelGroupBrowser)
        # self.verticalScroll.thumb.hide()
        self.horizontalScroll.hide()

        PLANE = PlaneNode(f'groupfilter_clipplane')
        PLANE.setPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 6.2)))
        self.filter_clipNP = self.attachNewNode(PLANE)
        # self.filter_clipNP.show()

        for button in (self.selectorButton_category, self.selectorButton_type, self.selectorButton_location,
                       self.button_availabilityAvailable, self.button_availabilityAll, self.bottomFramePanel):
            button.setClipPlane(self.filter_clipNP)

        self.reliefBackground = DirectFrame(
            parent=self.getCanvas(), relief=FLAT, pos=(0, 0, 0),
            frameSize=(-1.9916, 1.9933 - self.SCROLLBAR_WIDTH, -1000, 1000),
            frameColor=(0.263, 0.584, 0.278, 0.0),
        )
        self.bindToScroll(self.reliefBackground)

        self.loadingText = DirectFrame(
            parent=self, relief=None, pos=(-0.1564, 0, 3.5334),
            text="Loading...", text_fg=(0.122, 0.278, 0.106, 1.0),
            text_scale=0.36, text_pos=(0, -0.2),
        )
        self.loadingText.hide()

        self.mgr = mgr  # type: DistributedGroupManager
        self.groups: List[SocialPanelGroup] = []

        self.sequenceQueue = SequenceQueue(maxSize=4, playRate=1.8, autoSkip=True)

        self.restrictMode = True  # true: restrict groups this toon has not seen. false: not that
        self.filterer = GroupFilterer()

        self.panelOpened = False

        self.destroyed = False
        self.hasRefreshed = False
        self.accept('group-manager-update', self.refresh)

        self.accept('social-panel-groups-new-state', self.refresh)

        self.guisParentedNotToSelf = [
            self.verticalScrollImage,
            self.selectorButton_category, self.selectorButton_type,
            self.selectorButton_location, self.bottomFramePanel, self.button_availabilityAll,
            self.button_availabilityAvailable,
        ]

        self.accept(self.uniqueName('moveWidgetFrameTop'), self.setVerticalScrollFrameSize)
        self.accept(self.uniqueName('moveWidgetFrameBottom'), self.setVerticalScrollFrameSize)

        self.setFilterChoices()

        FSM.__init__(self, 'social-panel-group-browser')
        self.show()

    """
    Loader methods
    """

    def show(self):
        if not self:
            return
        super().show()
        for gui in self.guisParentedNotToSelf:
            gui.show()
        self.request(STATE_BROWSER, True)
        # make sure the frame size is set properly omg
        self['frameSize'] = self.DEFAULT_SIZE

        # def ensure():
        #     self['frameSize'] = self.DEFAULT_SIZE
        #     self.verticalScrollImage['image_scale'][2] = 3.9
        #
        # self.sequenceQueue.append(Func(ensure))
        # ensure()
        # send call for fresh groups
        self.destroyChildren()
        self.groups = []
        self.loadingText.show()
        self.hasRefreshed = False
        messenger.send('groups-refresh')
        taskMgr.remove('group-browser-delay-refresh')
        taskMgr.doMethodLater(3.0, self.delayedRefresh, 'group-browser-delay-refresh')

    def destroyChildren(self, exceptions=None):
        super().destroyChildren(exceptions=[self.reliefBackground])

    def hide(self):
        taskMgr.remove('group-browser-delay-refresh')
        self.sequenceQueue.finish()
        if self.panelOpened:
            self.closePanel()

        # make sure the frame size is set properly omg
        self['frameSize'] = self.DEFAULT_SIZE

        # def ensure():
        #     self['frameSize'] = self.DEFAULT_SIZE
        #     self.verticalScroll['image_scale'][2] = 3.9
        #
        # self.sequenceQueue.append(Func(ensure))
        # ensure()
        for gui in self.guisParentedNotToSelf:
            gui.hide()
        super().hide()

    def destroy(self):
        taskMgr.remove('group-browser-delay-refresh')
        del self.guisParentedNotToSelf
        self.sequenceQueue.finish()
        self.cleanup()
        super().destroy()

    def refresh(self, *_):
        self.loadingText.hide()
        self.hasRefreshed = True
        self.destroyChildren()
        self.groups = []
        if not self.joinableGroups:
            # Are we filtering?
            filterCategory = self.selectorButton_category.getChoice()
            isFiltering = filterCategory.getEnum() != FilterCategoryEnum.Any if filterCategory else False

            # Make the group text.
            group = EmptySocialPanelGroup(self.getCanvas(), group=None, pos=self.index2GroupPos(0),
                                          isFiltering=isFiltering)
            group.bindToScroll(self)
            self.groups.append(group)
        else:
            # Sort joinable groups.
            orderedGroups = self.getOrderedGroups(self.joinableGroups)
            for index, groupStruct in enumerate(orderedGroups):
                group = SocialPanelGroup(self.getCanvas(), groupStruct, pos=self.index2GroupPos(index))
                group.bindToScroll(self)
                self.groups.append(group)
        self.updateCanvasSize()

    def getOrderedGroups(self, groupList: List[GroupClient]) -> List[GroupClient]:
        """
        Filters a list of groups in terms of relevancy for the client.
        :return:
        """
        # First, separate empty groups and full groups.
        emptyGroups = [group for group in groupList if not group.isFull]
        fullGroups = [group for group in groupList if group.isFull]

        # Put full groups at the end.
        return emptyGroups + fullGroups

    def delayedRefresh(self, task):
        """called after a delay, in case we never got our server ping back for regular refresh"""
        if not self.hasRefreshed:
            self.refresh()
        return task.done

    def index2GroupPos(self, index, ypos: float = 0.0):
        # get the constants
        canvasSize = self.DEFAULT_CANVAS_SIZE
        canvasWidth = canvasSize[1] - canvasSize[0]
        canvasHeight = canvasSize[2] - canvasSize[3]
        canvasXDist = canvasWidth / groupsPerRow
        canvasZDist = canvasHeight / groupsPerCol
        canvasXStart = canvasSize[0] + (canvasXDist / 2)
        canvasZStart = -canvasHeight

        # get the positional multipliers
        zmult, xmult = divmod(index, groupsPerRow)
        xpos = canvasXStart + (xmult * canvasXDist)
        zpos = canvasZStart + (zmult * canvasZDist)
        return xpos, ypos, zpos

    def updateCanvasSize(self):
        """
        Properly updates the canvas size on the group browser.
        :return: None.
        """
        self['canvasSize'] = self.CANVAS_SIZE
        self.setCanvasSize()
        if self.canScroll:
            self.verticalScroll.setValue(0)
            # self.verticalScroll.thumb.hide()
            self.setVerticalScrollFrameSize()
            # self.verticalScroll.thumb.show()
        else:
            self.verticalScroll.setValue(0)
            # self.verticalScroll.thumb.hide()
            self.setVerticalScrollFrameSize()

    def setVerticalScrollFrameSize(self):
        return
        # self.verticalScroll.thumb['frameSize'] = (-0.21, 0.21, -0.68, 0.68)

    """
    State methods
    """

    def switchFilterStatus(self, force=False):
        """
        Switches between the two states.
        """
        if self.state == STATE_BROWSER:
            self.request(STATE_FILTER, force)
        else:
            self.request(STATE_BROWSER, force)

    def enterBrowser(self, force=False):
        self['frameSize'] = self.DEFAULT_SIZE
        # self.verticalScrollImage['image_scale'][2] = 3.9

    def exitBrowser(self):
        pass

    def enterFilter(self, force=False):
        self.openFilter()

    def exitFilter(self):
        self.closeFilter()

    """
    Filter Handling
    """

    def setFilterChoices(self):
        """Sets the initial choices for the filter buttons."""
        newValues = FILTER_DATA.getFilterCategories(self.restrictMode, self.filterer)
        newNames = FILTER_DATA.getFilterNames(self.restrictMode, self.filterer)
        priorChoice = self.selectorButton_category.getChoice()
        setIndex = 0
        if priorChoice in newValues:
            setIndex = newValues.index(priorChoice)
        self.selectorButton_category.setOptions(
            values=newValues,
            texts=newNames,
            setIndex=setIndex,
        )
        self.selector_updateCategory()

    def selector_updateCategory(self, _=None):
        filterCategory: FilterCategory = self.selectorButton_category.getChoice()
        if filterCategory is not None:
            newValues = filterCategory.getFilterTypes(self.restrictMode, self.filterer)
            newNames = filterCategory.getFilterNames(self.restrictMode, self.filterer)
            priorChoice = self.selectorButton_type.getChoice()
            setIndex = 0
            if priorChoice in newValues:
                setIndex = newValues.index(priorChoice)
            self.selectorButton_type.setOptions(
                values=newValues, texts=newNames,
                setIndex=setIndex, canDisable=True,
            )
        else:
            self.selectorButton_type.setOptions(canDisable=True)
        self.selector_updateType()

    def selector_updateType(self, _=None):
        filterType: FilterType = self.selectorButton_type.getChoice()
        if filterType is not None:
            newValues = filterType.getFilterLocations(self.restrictMode)
            newNames = filterType.getFilterNames(self.restrictMode)
            priorChoice = self.selectorButton_type.getChoice()
            setIndex = 0
            if priorChoice in newValues:
                setIndex = newValues.index(priorChoice)
            self.selectorButton_location.setOptions(
                values=newValues, texts=newNames,
                setIndex=setIndex, canDisable=True,
            )
        else:
            self.selectorButton_location.setOptions(canDisable=True)
        self.selector_updateLocation()

    def selector_updateLocation(self, _=None):
        self.refresh()

    def enableRestrictMode(self):
        self.button_availabilityAvailable['geom_color'] = self.accessClicked
        self.button_availabilityAll['geom_color']       = self.accessUnclicked
        self.restrictMode = True
        self.setFilterChoices()

    def disableRestrictMode(self):
        self.button_availabilityAvailable['geom_color'] = self.accessUnclicked
        self.button_availabilityAll['geom_color']       = self.accessClicked
        self.restrictMode = False
        self.setFilterChoices()

    """
    Callback waiting
    """

    def scaleVerticalScrollImage(self, t):
        if not self.verticalScrollImage:
            return
        if not self.filter_clipNP:
            return
        nofilter_z = 0.023
        onfilter_z = -0.094
        diff_z = (onfilter_z - nofilter_z) * t
        nofilter_s = 7.21
        onfilter_s = 4.94
        diff_s = (onfilter_s - nofilter_s) * t
        self.verticalScrollImage.setPos(0.21, 0, nofilter_z + diff_z)
        self.verticalScrollImage['image_scale'] = ((49 / 714) * 7.7, 1, nofilter_s + diff_s)

        # move clip NP
        clip_startZ = 6.2 - 6.2
        clip_endZ = 4.24 - 6.2
        diff_z = (clip_endZ - clip_startZ) * t
        self.filter_clipNP.setPos(0, 0, clip_startZ + diff_z)

    def openFilter(self):
        if not hasattr(self, '_optionInfo'):
            return Sequence()
        self.sequenceQueue.append(Sequence(
            Parallel(
                TTGui.moveWidgetFrameTop(self, 0.3, self.DEFAULT_SIZE[3]-1.97,
                                         startY=self.DEFAULT_SIZE[3], blendType='easeInOut'),
                # TTGui.widgetImageZScale(self.verticalScrollImage, 0.3, 0.34, startZ=4.36, blendType='easeInOut'),
                LerpFunctionInterval(self.scaleVerticalScrollImage, 0.3, fromData=0, toData=1, blendType='easeInOut'),
            ),
        ))

    def closeFilter(self):
        if not hasattr(self, '_optionInfo'):
            return Sequence()
        self.sequenceQueue.append(Sequence(
            Parallel(
                TTGui.moveWidgetFrameTop(self, 0.3, self.DEFAULT_SIZE[3],
                                         startY=self.DEFAULT_SIZE[3]-1.97, blendType='easeInOut'),
                # TTGui.widgetImageZScale(self.verticalScrollImage, 0.3, 4.36, startZ=0.34, blendType='easeInOut'),
                LerpFunctionInterval(self.scaleVerticalScrollImage, 0.3, fromData=1, toData=0, blendType='easeInOut'),
            ),
        ))

    """
    Various properties
    """

    @property
    def joinableGroups(self):
        """Go ahead and process all of the inbound groups for filtering."""
        retList = []
        for group in self.mgr.getJoinableGroups():
            group: GroupClient
            # If our filters are enabled, apply them.
            filterCategory = self.selectorButton_category.getChoice()
            isFiltering = filterCategory.getEnum() != FilterCategoryEnum.Any if filterCategory else False
            if isFiltering:
                # Some filtering is being applied. Ok.
                filterType = self.selectorButton_type.getChoice()
                if filterType:
                    # Ok, this filter type exists.
                    if filterType.getGroupTypes():
                        if group.groupType not in filterType.getGroupTypes():
                            # This group's type is being filtered out.
                            continue
                    if filterType.options:
                        success = False
                        for option in filterType.options:
                            if option in group.groupOptions:
                                success = True
                                break
                        if not success:
                            # This group's options are IRRELEVANT to us.
                            continue
                # What about location?
                filterLocation = self.selectorButton_location.getChoice()
                if filterLocation and filterLocation.hoods:
                    if ZoneUtil.getHoodId(group.zoneId) not in filterLocation.hoods:
                        # We aren't searching for any hoods, it seems.
                        continue
            # Determine the group joinability.
            result = self.filterer.runGroupTestsFromGroupType(base.localAvatar, group.groupType, force=False)
            if result == Responses.OK:
                group.setJoinMode(0)
            elif result in ResponseWarnings:
                group.setJoinMode(1)
            else:
                group.setJoinMode(2)
            if self.restrictMode and result != Responses.OK and result not in ResponseWarnings and result not in ResponsesFailsButVisible:
                # This group is filtered. Skip it.
                continue
            # Everything seems fine.
            retList.append(group)
        return retList

    @property
    def DEFAULT_CANVAS_SIZE(self):
        canvasSize = list(self.DEFAULT_SIZE)
        canvasSize[1] -= self.SCROLLBAR_WIDTH
        canvasSize[2] -= 0.001
        return canvasSize

    @property
    def CANVAS_SIZE(self):
        # set default values of canvas
        canvasSize = self.DEFAULT_CANVAS_SIZE

        # consider how many groups we have
        groupsUnderneath = self.groupsOffscreen
        if groupsUnderneath > 0:
            canvasSize[2] -= self.VERTICAL_CANVAS_OFFSCREEN

        # we're done here
        return canvasSize

    @property
    def VERTICAL_CANVAS_OFFSCREEN(self):
        """
        Returns how much vertical canvas there is offscreen.
        """
        distIncrease = self.DEFAULT_CANVAS_SIZE[3] / groupsPerCol
        rowsBeneath = (self.groupsOffscreen + 1) // groupsPerRow
        return distIncrease * (rowsBeneath - 1)

    @property
    def canScroll(self):
        """
        Checks to see if the panel is long
        enough and able to be scrolled.
        """
        return (len(self.groups) - (groupsPerRow * groupsPerCol)) > 0

    @property
    def groupsOffscreen(self) -> int:
        """
        Returns how many groups there are offscreen.
        :return: int
        """
        return len(self.groups) - (groupsPerRow * groupsPerCol)
