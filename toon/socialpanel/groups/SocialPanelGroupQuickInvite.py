"""
The ScrollWheelFrame which handles quick invites of users.
"""
from toontown.toon.socialpanel.friends import SocialPanelFriend
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from direct.gui.DirectGui import *
from direct.gui.DirectGuiGlobals import FLAT
from direct.interval.FunctionInterval import Func
from direct.interval.LerpInterval import LerpPosInterval
from direct.interval.MetaInterval import Sequence

from toontown.club.ClubGetters import ClubGetters
from toontown.groups.GroupGlobals import *
from toontown.toon.socialpanel.SocialPanelGUI import CheckboxButton

from toontown.toon.socialpanel.SocialPanelGlobals import sp_gui, sp_gui, sp_gui
from toontown.gui.TTGui import ScrollWheelFrame, moveWidgetFrameBottom

from typing import TYPE_CHECKING, Tuple, List

from toontown.utils.text import wordwrapWithVerticalCentering
from toontown.utils.ColorHelper import hexToPCol

if TYPE_CHECKING:
    from toontown.groups.DistributedGroupManager import DistributedGroupManager


@DirectNotifyCategory()
class SocialPanelGroupQuickInvite(ScrollWheelFrame, ClubGetters):

    DEFAULT_SIZE = (-1.93, 1.943, -0.06, 5.14)
    SCROLLBAR_WIDTH = 0.39

    def __init__(self, parent):
        # Set up the ScrollWheelFrame properties of the SocialPanelGroupBrowser.
        self.groupsTab = parent
        ScrollWheelFrame.__init__(
            self, parent=parent, relief=FLAT, scale=0.12, pos=(0, 0, -0.143),
            frameSize=self.DEFAULT_SIZE,
            canvasSize=self.DEFAULT_CANVAS_SIZE,
            scrollBarWidth=self.SCROLLBAR_WIDTH,
            manageScrollBars=0,
            frameColor=hexToPCol('2e6132', a=200),
            verticalScroll_image=sp_gui.find('**/ScrollBar_BAR'),
            verticalScroll_image_scale=(0.4583, 1.0, 5.24837),
            verticalScroll_image_pos=(1.7627, 0, 2.54119),
            verticalScroll_relief=None,
            scrollDistance=0.8,
        )
        # self['verticalScroll_thumb_frameSize'] = (-0.21, 0.21, -0.68, 0.68)
        self['verticalScroll_thumb_frameColor'] = (1, 0, 1, 0)
        self['verticalScroll_resizeThumb'] = 0
        self['verticalScroll_thumb_image'] = sp_gui.find('**/ScrollBar')
        self['verticalScroll_thumb_image_scale'] = (0.3913, 1, 0.3971)
        self['verticalScroll_thumb_image_pos'] = (0.0095, 0, 0)
        self.verticalScroll.incButton.destroy()
        self.verticalScroll.decButton.destroy()
        self.initialiseoptions(SocialPanelGroupQuickInvite)
        # self.verticalScroll.thumb.hide()
        self.horizontalScroll.destroy()

        PLANE = PlaneNode(f'quickinvite_clipplane')
        PLANE.setPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 5.14)))
        self.filter_clipNP = self.attachNewNode(PLANE)
        # self.filter_clipNP.show()
        self.setClipPlane(self.filter_clipNP)

        self.moveSeq = None

        # just some references
        self.mgr = base.cr.groupManager  # type: DistributedGroupManager

        # get the list of quick invite entries
        self.inviteGroups = []  # type: List[QuickInviteToonGroup]

        # and create our invite groups
        self.createInviteGroups()

        self.accept('social-panel-groups-tab-enter-create', self.createInviteGroups)

    def getInvitedAvIds(self) -> list:
        """Returns a complete list of invited avIds."""
        avIdSet = set()
        for group in self.inviteGroups:
            for avId in group.getSelectedAvIds():
                avIdSet.add(avId)
        return list(avIdSet)

    def getGroupsTab(self):
        return self.groupsTab

    """
    Making Invite Entries
    """

    def show(self):
        self.initInviteGroups()
        taskMgr.add(self.makeThumbGood, 'spgqi-makeThumbGood')
        if self.moveSeq:
            self.moveSeq.finish()
            self.moveSeq = None
        self.moveSeq = Sequence(Func(super().show), LerpPosInterval(
            nodePath=self.filter_clipNP, duration=0.2,
            pos=(0, 0, -5.2), startPos=(0, 0, 0), blendType='easeOut'
        ))
        self.moveSeq.start()
        if settings['reduce-gui-movement']:
            self.moveSeq.finish()
        messenger.send('spgqi-open')

    def hide(self, instant=True):
        taskMgr.remove('initInviteGroups')
        taskMgr.remove('spgqi-makeThumbGood')
        if self.moveSeq:
            self.moveSeq.finish()
            self.moveSeq = None
        self.moveSeq = Sequence(LerpPosInterval(
            nodePath=self.filter_clipNP, duration=0.2,
            pos=(0, 0, 0), startPos=(0, 0, -5.2), blendType='easeIn'
        ), Func(super().hide))
        self.moveSeq.start()
        if instant or settings['reduce-gui-movement']:
            self.moveSeq.finish()
        messenger.send('spgqi-close')

    def destroy(self):
        taskMgr.remove('initInviteGroups')
        taskMgr.remove('spgqi-makeThumbGood')
        if self.moveSeq:
            self.moveSeq.finish()
            self.moveSeq = None
        self.destroyInviteGroups()
        self.ignoreAll()
        super().destroy()

    def createInviteGroups(self):
        """Creates all of the QuickInviteToonGroups."""
        self.destroyInviteGroups()
        # Create the Nearby Toons invite group.
        toonDict = {}
        for objId, obj in list(base.cr.doId2do.items()):
            if obj.dclass == base.cr.dclassesByName['DistributedToon']:
                if obj.ghostMode:  # If toon is in ghost mode don't show them in the list
                    continue
                if obj.doId == base.localAvatar.doId:
                    continue
                toonDict[obj.doId] = obj.getName()
        quickInviteToonGroup = QuickInviteToonGroup(
            parent=self.getCanvas(), quickInvitePanel=self,
            toonGroupName=TTLocalizer.SocialPanelFriendsSortNearby, toonDict=toonDict
        )
        quickInviteToonGroup.bindToScroll(self)
        self.inviteGroups.append(quickInviteToonGroup)
        # Create the Online Friends invite group.
        onlineAvIdList = []
        if base.localAvatar:
            onlineAvIdList = [avId for avId, _ in base.localAvatar.friendsList if base.cr.isFriendOnline(avId)]
        toonDict = {}
        for avId in onlineAvIdList:
            if avId == base.localAvatar.getDoId():
                continue
            handle = base.cr.identifyFriend(avId)
            if not handle:
                continue
            toonDict[avId] = handle.getName()
        quickInviteToonGroup = QuickInviteToonGroup(
            parent=self.getCanvas(), quickInvitePanel=self,
            toonGroupName=TTLocalizer.SocialPanelFriendsSortOnline, toonDict=toonDict)
        quickInviteToonGroup.bindToScroll(self)
        self.inviteGroups.append(quickInviteToonGroup)
        # If we are in a club, create the Online Clubmates invite group.
        if self.getClubMgr().isInClub():
            clubToonList = []
            if base.localAvatar:
                clubToonList = [clubToon for clubToon in self.getClubContainer().getClubToons() if clubToon.isOnline()]
            toonDict = {}
            for clubToon in clubToonList:
                avId = clubToon.getAvId()
                if avId == base.localAvatar.getDoId():
                    continue
                toonDict[avId] = clubToon.getToonName()
            quickInviteToonGroup = QuickInviteToonGroup(
                parent=self.getCanvas(), quickInvitePanel=self,
                toonGroupName=TTLocalizer.SocialPanelFriendsSortOnlineClub, toonDict=toonDict)
            quickInviteToonGroup.bindToScroll(self)
            self.inviteGroups.append(quickInviteToonGroup)
        # finish up
        taskMgr.add(self.initInviteGroups, 'initInviteGroups')

    def initInviteGroups(self, task=None):
        """Init placements on the invite groups"""
        currentHeight = self.DEFAULT_CANVAS_SIZE[3]
        for group in self.inviteGroups:
            group.setPos(self.HORIZONTAL_MIDPOINT, 0, currentHeight)
            currentHeight -= group.getTotalHeight()
            group.initPlacements()
        self.updateCanvasSize()
        if task is not None:
            return task.done

    def destroyInviteGroups(self):
        """Cleans up all of the QuickInviteToonGroups."""
        for group in self.inviteGroups:
            group.destroy()
        self.inviteGroups = []

    """
    Handling Canvas Size
    """

    def getTotalHeight(self):
        return sum([entry.getTotalHeight() for entry in self.inviteGroups])

    def getCanvasTop(self):
        return self.DEFAULT_CANVAS_SIZE[3] - self.getTotalHeight()

    def makeThumbGood(self, task):
        """the thumb never wants to update"""
        # self.verticalScroll.thumb['frameSize'] = (-0.21, 0.21, -0.68, 0.68)
        return task.cont

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
            # self.verticalScroll.thumb['frameSize'] = (-0.21, 0.21, -0.68, 0.68)
            # self.verticalScroll.thumb.show()
        else:
            self.verticalScroll.setValue(0)
            # self.verticalScroll.thumb.hide()
            # self.verticalScroll.thumb['frameSize'] = (-0.21, 0.21, -0.68, 0.68)

    @property
    def HORIZONTAL_MIDPOINT(self):
        l, r, *_ = self.DEFAULT_SIZE
        return (r + l - self.SCROLLBAR_WIDTH) / 2

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

        # set the height of the canvas accordingly
        canvasSize[2] = min(canvasSize[2], self.getCanvasTop())

        # we're done here
        return canvasSize

    @property
    def canScroll(self):
        """
        Checks to see if the panel is long
        enough and able to be scrolled.
        """
        return self.DEFAULT_CANVAS_SIZE != self.CANVAS_SIZE


class QuickInviteToonGroup(DirectButton):
    """
    A group of Toons in the QuickInvite panel.
    """

    HEIGHT = 0.5
    PADDING_MULT = 0.97  # lower -> panels closer together

    def __init__(self, parent, quickInvitePanel, toonGroupName: str, toonDict: dict, **kw):
        """
        Defines a QuickInviteToonGroup.

        :param parent: The parent of the GUI element.
        :param quickInvitePanel: The QuickInvite panel.
        :param toonGroupName: The name of the ToonGroup.
        :param toonDict: A dictionary of all Toons in this group {avId: name}.
        :param kw: Any associated kwargs.
        """
        optiondefs = ()
        self.defineoptions(kw, optiondefs)
        self.quickInvitePanel = quickInvitePanel
        self.toonGroupName = toonGroupName
        w = self.getCanvasWidth()
        h = self.HEIGHT
        DirectButton.__init__(
            self, parent=parent, pos=((-w/2) + h/2, 0, -h/2), relief=None,
            text=toonGroupName, text_scale=0.03, text_pos=(0, -0.33),
            frameSize=(-w, w, -h, 0), frameColor=(0, 0, 0, 0),
            geom=(sp_gui.find('**/Box_N'), sp_gui.find('**/Box_P'), sp_gui.find('**/Box_H')),
            geom_scale=(h * (455 / 42), 1, h), geom_pos=(0, 0, -h/2),
            geom_color=(0.755, 0.763, 0.778, 1.0), textMayChange=1,
            **kw
        )
        self.initialiseoptions(QuickInviteToonGroup)

        # Create all of our Toons.
        self.toonList, self.checkboxList = self._makeToonList(toonDict=toonDict)

        # Create our own checkbox.
        self.checkbox = CheckboxButton(
            parent=self, checkboxGroup=self.checkboxList, relief=None, frameColor=(0, 0, 0, 0),
            frameSize=(-h/2, h/2, -h/2, h/2), pos=(-1.5202, 0, -0.2467), scale=1,
            checkboxGroupSelectAllPartialHandlerCallable=self.getGroupsTab().canInviteToons
        )

        self['state'] = DGG.NORMAL
        self.bind(DGG.B1PRESS, self.pseudoClickCheckbox)

    def bindToScroll(self, scrollPanel):
        # Binds this panel to the scroll wheel.
        scrollPanel.bindToScroll(self)
        self.checkbox.bindToScroll(scrollPanel)
        for toon in self.toonList:
            toon.bindToScroll(scrollPanel)

    def pseudoClickCheckbox(self, _=None):
        """
        Wrapped for the checkbox click.
        :param _: Pain.
        :return: None.
        """
        self.checkbox.getClickCallable()()

    def initPlacements(self):
        w = self.getCanvasWidth()
        h = self.HEIGHT
        # self['pos'] = ((-w / 2) + h / 2, 0, -h / 2)
        self['text_scale'] = 0.26
        self['text_pos'] = (0, -0.31)
        self['text_wordwrap'] = 12
        self.setText(self.toonGroupName)
        self['geom'] = (sp_gui.find('**/Box_N'), sp_gui.find('**/Box_P'), sp_gui.find('**/Box_H'))
        self['geom_scale'] = (h * (455 / 42), 1, h)
        self['geom_pos'] = (0, 0, -h / 2)
        self['geom_color'] = (0.755, 0.763, 0.778, 1.0)
        self['frameSize'] = (-w, w, -h, 0)
        self['frameColor'] = (0, 0, 0, 0)
        height = -self.HEIGHT * self.PADDING_MULT
        for toon in self.toonList:
            toon.initPlacements(height)
            height -= self.HEIGHT * self.PADDING_MULT

    def getQuickInvitePanel(self):
        return self.quickInvitePanel

    def getGroupsTab(self):
        return self.getQuickInvitePanel().getGroupsTab()

    def getCanvasWidth(self):
        return self.getQuickInvitePanel().getCanvasWidth()

    def getTotalHeight(self):
        return (self.HEIGHT + sum([self.HEIGHT for toon in self.toonList])) * self.PADDING_MULT

    def getSelectedAvIds(self) -> list:
        """
        Returns a list of all selected avIds.
        :return: A list of all avIds.
        """
        retList = self.checkbox.getValue(ignoreGroupNones=True)
        if retList is None:
            return []
        return retList

    def destroy(self):
        """Cleanup references."""
        for toon in self.toonList:
            toon.destroy()
        del self.toonList
        del self.checkboxList
        del self.quickInvitePanel
        super().destroy()

    def _makeToonList(self, toonDict: dict) -> Tuple[list, list]:
        """
        Creates a list of QuickInviteToons given a toonDict {avId: name}.
        :return: A list of the QuickInviteToons.
        """
        panelList, checkboxList = [], []
        currHeight = self.HEIGHT
        orderedDict = {k: v for k, v in sorted(toonDict.items(), key=lambda item: item[1])}
        for avId, name in orderedDict.items():
            quickInviteToon = QuickInviteToon(parent=self, avId=avId, name=name)
            panelList.append(quickInviteToon)
            checkboxList.append(quickInviteToon.checkbox)
            currHeight += self.HEIGHT
        return panelList, checkboxList


class QuickInviteToon(DirectButton):
    """
    A singleton Toon in a QuickInviteToonGroup.
    """

    def __init__(self, parent: QuickInviteToonGroup, avId: int, name: str, **kw):
        """
        Defines a QuickInviteToon.

        :param parent: The parent of the GUI element.
        :param avId: The avatar ID of the Toon.
        :param name: The Toon's name.
        :param kw: Any associated kwargs.
        """
        optiondefs = ()
        self.defineoptions(kw, optiondefs)
        self.qiToonGroup = parent
        self.toonName = name
        self.selected = False
        self.avId = avId
        h = parent.HEIGHT
        w = parent.getCanvasWidth()
        super().__init__(
            parent=parent, relief=None,
            text="", text_scale=0.23,
            text_pos=(0, -0.3),
            # text_align=TextNode.ALeft,
            geom=(sp_gui.find('**/Box_N'), sp_gui.find('**/Box_P'), sp_gui.find('**/Box_H')),
            geom_scale=(h * (455 / 42), 1, h), geom_pos=(0, 0, -h/2),
            frameSize=(-w, w, -h, 0), frameColor=(0, 0, 0, 0), textMayChange=1,
            **kw
        )
        self.initialiseoptions(QuickInviteToon)

        self['state'] = DGG.NORMAL
        self.bind(DGG.B1PRESS, self.onLabelClicked)

        self['geom_color'] = self.color
        if self.favorite:
            self['text_fg'] = (1, 1, 1, 1)
            self['text_shadow'] = (0, 0, 0, 1)

        # Create a checkbox.
        self.checkbox = CheckboxButton(
            parent=self, value=avId, command=self.onClick,
            checkCallableOnCheck=self.getGroupsTab().canInviteToons,
            pos=(-1.5202, 0, -0.2467), relief=None, scale=1,
        )

        self.accept('social-panel-toon-quick-invited', self.onToonInvited)

    def bindToScroll(self, scrollPanel):
        # Binds this toon to the scroll wheel.
        scrollPanel.bindToScroll(self)
        self.checkbox.bindToScroll(scrollPanel)

    def initPlacements(self, height):
        w = self.getCanvasWidth()
        h = self.qiToonGroup.HEIGHT
        self.setPos(0, 0, height)
        self['text_scale'] = 0.23
        self['text_pos'] = (0, -0.31)
        self['text_wordwrap'] = 12
        self.setText(self.toonName)
        self['geom'] = (sp_gui.find('**/Box_N'), sp_gui.find('**/Box_P'), sp_gui.find('**/Box_H'))
        self['geom_scale'] = (h * (455 / 42), 1, h)
        self['geom_pos'] = (0, 0, -h / 2)
        self['frameSize'] = (-w, w, -h, 0)
        self['frameColor'] = (0, 0, 0, 0)
        self['geom_color'] = self.color
        if self.favorite:
            self['text_fg'] = (1, 1, 1, 1)
            self['text_shadow'] = (0, 0, 0, 1)
        wordwrapWithVerticalCentering(self, 12, text=self.toonName)

    def getGroupsTab(self):
        return self.qiToonGroup.getGroupsTab()

    def getCanvasWidth(self):
        return self.qiToonGroup.getCanvasWidth()

    def onLabelClicked(self, _=None):
        """The label was clicked, redirect function."""
        self.checkbox.onClick()

    def onToonInvited(self, avId, mode):
        if avId == self.avId and mode != self.selected:
            self.onLabelClicked()

    def onClick(self):
        """
        Called when this button gets clicked.
        :return: None.
        """
        if self.checkbox.checked:
            # This label is checked.
            self.selected = True
        else:
            # This label is not checked.
            self.selected = False

        # Messenger call to alert a toon was quick invited.
        self['geom_color'] = self.color
        messenger.send('social-panel-toon-quick-invited', [self.avId, self.selected])

    def destroy(self):
        """Cleanup references."""
        self.checkbox.destroy()
        del self.checkbox
        self.ignoreAll()
        super().destroy()

    @property
    def color(self):
        """
        Gets the color this panel should be.
        """
        if self.selected:
            return SocialPanelFriend.COLOR_SELECTED if not self.favorite else SocialPanelFriend.COLOR_FAVORITE_SELECTED
        return SocialPanelFriend.COLOR_DEFAULT if not self.favorite else SocialPanelFriend.COLOR_FAVORITE

    @property
    def favorite(self):
        """
        Checks if this panel is a favorite.
        """
        return self.avId in base.localAvatar.getFavoriteFriends()
