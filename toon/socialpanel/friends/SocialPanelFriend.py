"""
A singular 'friend' row on the SocialPanelFriendsTab.
"""
from direct.gui import DirectGuiGlobals
from panda3d.core import TextNode, Vec3
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from direct.gui.DirectGui import *
from direct.gui.DirectGuiGlobals import FLAT
from toontown.friends.FriendHandle import FriendHandle
from direct.interval.IntervalGlobal import Parallel, LerpPosInterval
from toontown.utils.ColorHelper import hexToPCol

from toontown.toon.socialpanel.SocialPanelGUI import CheckboxButton
from toontown.toon.socialpanel.SocialPanelGlobals import friendYOffset, questCard, sp_gui, sp_gui

COLOR_DEFAULT = hexToPCol('cce0bd')
COLOR_FAVORITE = hexToPCol('32b8d5')
COLOR_SELECTED = hexToPCol('d5e05f')
COLOR_FAVORITE_SELECTED = hexToPCol('d5e05f')


@DirectNotifyCategory()
class SocialPanelFriend(DirectButton):
    shiftPos = Vec3(0.5, 0, 0)
    configurePos = Vec3(-0.25, 0, -0.2275)

    def __init__(self, scrollWheelFrame, handle: FriendHandle, textColor, index, friendsTab, configureMode=False):
        # Set properties of this friend.
        self.handle: FriendHandle = handle
        self.index = index
        self.selected = False
        self.configureMode = configureMode
        self.friendsTab = friendsTab
        self.textColor = textColor

        # Empty references.
        self.button_select = None

        # Set up the DirectLabel properties of the SocialPanelFriend.
        leftPos = scrollWheelFrame['canvasSize'][0]
        super().__init__(
            parent=scrollWheelFrame.getCanvas(), relief=None, command=self.onClick,
            frameSize=(0, 5.0, -friendYOffset, 0), frameColor=(1, 1, 1, 0),
            text=self.handle.getName(), text_scale=0.29, text_align=TextNode.ALeft,
            text_pos=(0.1, -0.07 - (friendYOffset / 2)),
            text_fg=self.getTextColor(),
            text_shadow=self.getTextShadow(),
            geom=(sp_gui.find('**/Box_N'), sp_gui.find('**/Box_P'), sp_gui.find('**/Box_H')), geom_color=self.color,
            geom_scale=(0.5 * (455/42), 1, 0.52), geom_pos=(2.71, 0, -0.24)
        )
        self.initialiseoptions(SocialPanelFriend)
        scrollWheelFrame.bindToScroll(self)
        self.startPos = Vec3(leftPos, 1, 0 - (index * friendYOffset))
        self.endPos = self.startPos + self.shiftPos
        self.setPos(self.startPos)

        self.checkboxBehind = DirectFrame(
            parent=self,
            geom=sp_gui.find('**/Box2_N'),
            geom_color=COLOR_DEFAULT,
            pos=(-0.25, 0, -0.24), scale=0.52,
        )
        scrollWheelFrame.bindToScroll(self.checkboxBehind)

        self.checkbox = CheckboxButton(
            parent=self,
            scale=0.4136 / 0.45,
            frameColor=(0, 0, 0, 0),
            frameSize=(-0.55, 0.55, -0.55, 0.55),
            pos=self.configurePos,
            command=self.onSelect
        )
        self.checkbox.bindToScroll(scrollWheelFrame)

        # Do binds and events.
        self.bind(DirectGuiGlobals.B3PRESS, command=self.onRightClick)
        self.transitionConfigure(instant=True)

    def destroy(self):
        """
        Cleans up all of the SocialPanelFriend stuff.
        """
        self.ignoreAll()
        super().destroy()

    """
    Button methods
    """

    def resetClearState(self):
        self.checkbox.reset()
        self.selected = False
        self.updateColor()

    def onClick(self):
        """
        Lets the world know when this panel is clicked.
        """
        messenger.send('social-panel-friend-click', [self])

    def askSelect(self):
        self.checkbox.getClickCallable()()

    def onSelect(self, force=None, sendCall: bool = True):
        """
        Lets the world know when this panel is selected.
        """
        if force is None:
            self.selected = not self.selected
        else:
            self.selected = force
        self.updateColor()
        if sendCall:
            messenger.send('social-panel-friends-configure', [self])

    def onRightClick(self, args):
        """
        Called when the SocialPanelFriend is right-clicked.
        """
        # Select ourselves, if none are selected.
        if not self.friendsTab.selectedUsers:
            if not self.checkbox.getValue():
                # Fake a click
                self.askSelect()
        # Send the messenger call.
        messenger.send('social-panel-friend-context', [args])

    """
    Some state methods
    """

    def setConfigure(self, mode):
        """
        Sets the configuration state of the SocialPanelFriend.
        """
        if self.configureMode == mode:
            # no need to update
            return
        # update accordingly
        self.configureMode = mode
        self.transitionConfigure()

    def transitionConfigure(self, instant=False):
        """
        Properly transition between configuration states.
        """
        if self.configureMode:
            self.enterConfigure(instant=instant)
        else:
            self.exitConfigure(instant=instant)
        self.updateColor()

    def enterConfigure(self, instant=False):
        """
        Does the visual effect upon
        entering the configuration state.
        """
        track = Parallel(
            LerpPosInterval(self, 0.2, self.endPos, blendType='easeOut'),
        )
        track.start()
        if instant or settings['reduce-gui-movement']:
            track.finish()

    def exitConfigure(self, instant=False):
        """
        Does the visual effect upon
        exiting the configuration state.
        """
        track = Parallel(
            LerpPosInterval(self, 0.2, self.startPos, blendType='easeOut'),
        )
        track.start()
        if instant or settings['reduce-gui-movement']:
            track.finish()

    def updateColor(self):
        """
        Updates the frame color.
        """
        self['geom_color'] = self.color
        self['text_color'] = self.getTextColor()
        self.checkboxBehind['geom_color'] = self.behindColor
        self.checkbox.reset(self.selected)

    """
    Properties
    """

    @property
    def color(self):
        """
        Gets the color this panel should be.
        """
        if self.selected and self.configureMode:
            return COLOR_SELECTED if not self.favorite else COLOR_FAVORITE_SELECTED
        return COLOR_DEFAULT if not self.favorite else COLOR_FAVORITE

    @property
    def behindColor(self):
        return COLOR_SELECTED if self.selected else COLOR_DEFAULT

    def getTextColor(self):
        if self.textColor:
            return self.textColor
        if not self.favorite:
            return 0, 0, 0, 1
        return 1, 1, 1, 1

    def getTextShadow(self):
        if self.favorite:
            return 0, 0, 0, 1
        return None

    @property
    def avId(self):
        """
        Gets the relevant avId of this panel.
        """
        return self.handle.doId

    @property
    def favorite(self):
        """
        Checks if this panel is a favorite.
        """
        return self.avId in base.localAvatar.getFavoriteFriends()
