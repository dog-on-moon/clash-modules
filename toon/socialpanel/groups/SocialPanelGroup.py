"""
A singular 'group' GUI element on the Social Panel.
"""

from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from direct.gui.DirectGui import *
from direct.gui.DirectGuiGlobals import GROOVE, FLAT
from toontown.groups.GroupGlobals import *
from toontown.groups.GroupClasses import GroupClient, GroupCreation
from toontown.toon.socialpanel.SocialPanelGlobals import groupsPerCol, sp_gui_bgs, getSocialPanelGroupBg, \
    sp_gui
from toontown.gui.TTGui import ExtendedOnscreenText
from toontown.utils.ColorHelper import *


class SocialPanelGroup:
    pass


@DirectNotifyCategory()
class SocialPanelGroup(DirectFrame):

    DEFAULT_SIZE = (-1.9916, 1.9933, 0, 6.14)  # same in SocialPanelGroupBrowser.py
    h_padding = 0.27
    v_padding = 0.04

    NORMAL = 0
    WARNING = 1
    FAILURE = 2

    GRADIENT_COLORS = {
        0: hexToPCol('D5FAD2'),
        1: hexToPCol('FADBBF'),
        2: hexToPCol('FAC1C4'),
    }
    MODELS = {
        0: sp_gui.find('**/SocialPanel_Groups_Box_Base'),
        1: sp_gui.find('**/SocialPanel_Groups_Box_Base_Warn'),
        2: sp_gui.find('**/SocialPanel_Groups_Box_Base_Fail'),
    }

    def __init__(self, canvas, group: GroupClient, pos):
        # Set up the DirectFrame properties of the SocialPanelGroup.
        l, r, *_ = self.DEFAULT_SIZE
        DirectFrame.__init__(
            self, parent=canvas, pos=pos, relief=GROOVE,
            frameSize=(l + self.h_padding, r - self.h_padding,
                       self.getPanelHeight() + self.v_padding, 0 - self.v_padding),
            frameColor=(0.89, 0.925, 0.914, 0.0),
            borderWidth=(0.01, 0.01),
        )
        self.initialiseoptions(SocialPanelGroup)

        self.force = 0

        # Set references.
        self.group = group
        self.joinMode = group.getJoinMode() if group else 0
        self.text_title = None
        self.text_desc = None
        self.text_toons = None
        self.frame_base = None
        self.frame_image = None
        self.frame_gradient = None
        self.button_view = None
        self.button_join = None

        # Load the elements of the social panel.
        self.load()

    """
    Loading methods
    """

    def load(self):
        self.frame_base = DirectFrame(
            parent=self, pos=(0, 0, self.getPanelHeight() / 2), relief=None,
            frameColor=(1, 1, 1, 0), text='',
            text_align=TextNode.ALeft,
            geom=sp_gui.find('**/SocialPanel_Groups_Box_Base'),
            geom_scale=(456/129, 1, 1),
        )
        self.frame_image = DirectFrame(
            parent=self, pos=(0, 0, self.getPanelHeight() / 2), relief=None,
            frameColor=(1, 1, 1, 0), text='',
            text_align=TextNode.ALeft,
            geom=getSocialPanelGroupBg(self.group),
            geom_scale=(0.96 * (456 / 129), 1, 0.83),
        )
        self.frame_gradient = DirectFrame(
            parent=self, pos=(0, 0, self.getPanelHeight() / 2), relief=None,
            frameColor=(1, 1, 1, 0), text='',
            text_align=TextNode.ALeft,
            geom=sp_gui.find('**/SocialPanel_Groups_Box_Gradient'),
            geom_scale=(0.96 * (456 / 129), 1, 0.83),
        )
        self.text_title = ExtendedOnscreenText(
            parent=self, scale=0.24, pos=(-1.64, -0.33),
            align=TextNode.ALeft, fg=c_black,
            text=self.truncateName(self.group.getName()),
            wordwrap=14,
        )
        self.text_desc = OnscreenText(
            parent=self, scale=0.2, pos=(-1.64, -0.65),
            align=TextNode.ALeft, fg=c_black,
            text=self.description,
        )
        self.text_toons = OnscreenText(
            parent=self, scale=0.24, pos=(0.41, -0.84),
            align=TextNode.ARight, fg=c_black,
            text=self.toons_description,
        )
        self.button_view = DirectButton(
            parent=self,
            pos=(1.38, 0, -0.77), relief=None,
            frameSize=(-0.29, 0.29, -0.14, 0.14),
            frameColor=(0.153, 0.408, 0.125, 1.0),
            geom=(
                sp_gui.find('**/OrangeButton_N'),
                sp_gui.find('**/OrangeButton_P'),
                sp_gui.find('**/OrangeButton_H'),
            ), geom_scale=(0.21 * (151 / 55), 1, 0.26), geom_color=(0.85, 0.85, 0.85, 1),
            text="View", text_scale=0.21, text_pos=(0, -0.062),
            text_fg=(1, 1, 1, 1), scale=1,
            command=self.handleView,
        )
        self.button_join = DirectButton(
            parent=self,
            pos=(0.75, 0, -0.77), relief=None,
            frameSize=(-0.29, 0.29, -0.14, 0.14),
            frameColor=(0.153, 0.408, 0.125, 0.0),
            geom=(
                sp_gui.find('**/OrangeButton_N'),
                sp_gui.find('**/OrangeButton_P'),
                sp_gui.find('**/OrangeButton_H'),
            ), geom_scale=(0.21 * (151 / 55), 1, 0.26), geom_color=(0.85, 0.85, 0.85, 1),
            text="Join", text_scale=0.21, text_pos=(0, -0.062),
            text_fg=(1, 1, 1, 1), scale=1,
            command=self.handleJoin,
        )

        # if this is the local avatar's group (or localav in a group)
        # we want to respect that, and hide the join button
        if base.localAvatar:
            avId = base.localAvatar.getDoId()
            localGroup = base.cr.groupManager.group
            if avId in self.group.avIds or (localGroup and avId in localGroup.avIds):
                self.button_join.hide()

        self.setBaseColors()

    def truncateName(self, name):
        if len(name) >= 30:
            return name[:27] + '...'
        return name

    def bindToScroll(self, scrollWheelFrame):
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.frame_base)
        scrollWheelFrame.bindToScroll(self.frame_image)
        scrollWheelFrame.bindToScroll(self.frame_gradient)
        scrollWheelFrame.bindToScroll(self.button_join)
        scrollWheelFrame.bindToScroll(self.button_view)

    def handleView(self):
        messenger.send('social-panel-groups-new-state', ['View', self.group])

    def handleJoin(self):
        messenger.send('social-panel-groups-request-join', [self.group.owner, self.force])
        self.force = True

    def setBaseColors(self, joinMode: int = None):
        if joinMode is not None:
            self.joinMode = joinMode
        self.frame_base['geom'] = self.MODELS.get(self.joinMode)
        self.frame_gradient['geom_color'] = self.GRADIENT_COLORS.get(self.joinMode)

    @property
    def description(self):
        shardName = self.group.shardName
        location = self.group.location
        return f"{shardName}\n{location}"

    @property
    def toons_description(self):
        avIds = len(self.group.avatarList)
        groupSize = self.group.groupSize
        return f"{avIds}/{groupSize}"

    """
    Group Placement Positions
    """

    def getPanelHeight(self):
        """Height of the group panel"""
        canvasSize = self.DEFAULT_SIZE
        return (canvasSize[2] - canvasSize[3]) / groupsPerCol


class EmptySocialPanelGroup(SocialPanelGroup):

    def __init__(self, canvas, group, pos, isFiltering: bool):
        self.isFiltering = isFiltering
        if group is None:
            group = GroupClient(
                groupId=0, groupCreation=GroupCreation(
                    groupType=GroupType.TOONO, groupOptions=[], groupSize=0,
                ), districtId=0, avatarList=[], published=True, zoneId=0,
                kickedAvIds=[],
            )
        super().__init__(canvas, group, pos)
        self.initialiseoptions(EmptySocialPanelGroup)

    def load(self):
        super().load()

        # Post-load settings to make this group display empty.
        for gui in (self.frame_gradient, self.frame_image, self.text_desc,
                    self.text_toons, self.button_view, self.button_join):
            gui.hide()

        self.text_title.setPos(0, -0.57)
        self.text_title.setAlign(TextNode.ACenter)
        if not self.isFiltering:
            if base.localAvatar and base.localAvatar.zoneId in GroupZones:
                self.text_title.setTextWithVerticalAlignment('No groups available.\n\1TextShrink\1Press Create to make a group\nin your area.\2')
            else:
                self.text_title.setTextWithVerticalAlignment('No groups available.')
        else:
            self.text_title.setTextWithVerticalAlignment('No filtered groups available.\n\1TextShrink\1Change your filter settings or\ndisable the filter to see Groups.\2')
