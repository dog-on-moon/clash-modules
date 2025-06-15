"""
The Corporate Clash Social Panel, for use for all Toons
to browse their friends/groups/mail/clubs.

Created by: Moondog
Started: 12/13/2021
"""
if __name__ == "__main__":
    from tools.headless.headlessbase import HeadlessStart
    from tools.headless.headlessbase.HeadlessBase import HeadlessBase
    base = HeadlessBase(wantHotkeys=False)
    if __debug__:
        from toontown.utils.DeveloperInjector import startInjector
        startInjector()
    base.initCR()  # defines base.cr
    base.startHeadlessShow()
    # base.initTalkAssistant()

    from toontown.quest3.objectives import *
    from toontown.quest3.questlines.ClubsQuestLine import *
    from toontown.club.ClubContainerClient import ClubContainerClient
    cc = ClubContainerClient()
    cc.localAvHasPermission = lambda _='ughh hHhh hI LOVE TOONTOWN': 0.412983741928374
    base.cr.clubMgr.clubContainer = cc
    base.cr.clubMgr.inClub = True

    from toontown.toon.DistributedToon import DistributedToon
    base.localAvatar = DistributedToon(cr=base.cr)
    base.localAvatar.doId = 10
    base.localAvatar.zoneId = 2000

    from toontown.groups.GroupClasses import GroupClient, GroupCreation
    from toontown.groups.GroupEnums import GroupType, Options
    gc = GroupClient(
            groupId=0,
            groupCreation=GroupCreation(
                groupType=GroupType.Pizzeria,
                groupOptions=[Options.SOCIAL_PARTY],
                groupSize=99,
            ),
            districtId=0,
            avatarList=[],
            published=True,
            zoneId=3740,
            kickedAvIds=[],
            announcedBattle=False,
            avatarThatEncountered=0,
        )
    base.cr.groupManager.group = gc


from toontown.friends.FriendInviter import showFriendInviter, FriendInviter
from toontown.gui.GUIPositionGlobals import ScreenCorner
from toontown.gui.PositionedGUI import PositionedGUI, OnscreenPositionData
from toontown.toon.socialpanel.friends.SocialPanelFriendsTab import SocialPanelFriendsTab
from toontown.toon.socialpanel.groups.SocialPanelGroupsTab import SocialPanelGroupsTab
from toontown.toon.socialpanel.mail.SocialPanelMailTab import SocialPanelMailTab
from toontown.toon.socialpanel.clubs.SocialPanelClubsTab import SocialPanelClubsTab
from toontown.toon.socialpanel.friends.SocialPanelFriendsInviterTab import SocialPanelFriendsInviterTab
from toontown.toon.socialpanel.SocialPanelGlobals import *
from toontown.toon.socialpanel.SocialPanelTabs import SocialPanelTabs
from toontown.toon.socialpanel.groups.SocialPanelGroupSubtext import SocialPanelGroupSubtext
from toontown.toon.gui import GuiBinGlobals
from direct.fsm.FSM import FSM
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from direct.gui.DirectGui import *
from direct.gui.DirectGuiGlobals import NORMAL
from toontown.toonbase.MarginManagerCell import ScreenCellFlag
from toontown.avatar.AvatarPanel import AvatarPanel

STATE_FRIENDS = 'Friends'
STATE_GROUPS = 'Groups'
# STATE_CLUBS = 'Club'
STATE_FRIEND_INVITE = 'FriendsInvite'


@DirectNotifyCategory()
class SocialPanel(DirectFrame, FSM, PositionedGUI):

    SCREEN_CORNER = ScreenCorner.TOP_RIGHT
    GUI_BOUNDS = OnscreenPositionData(
        width=0.5,
        height=0.5,
        left=0.02,
        down=0.51,
    )
    DEBUG_MARGIN_POS = (-0.25, 0, -0.25)

    enum2State = {
        TAB_FRIENDS: STATE_FRIENDS,
        TAB_GROUPS: STATE_GROUPS,
        # TAB_CLUBS: STATE_CLUBS,
        TAB_FRIENDS_INVITE: STATE_FRIEND_INVITE,
    }

    state2Tab = {
        STATE_FRIENDS: SocialPanelFriendsTab,
        STATE_GROUPS: SocialPanelGroupsTab,
        # STATE_CLUBS: SocialPanelClubsTab,
        STATE_FRIEND_INVITE: SocialPanelFriendsInviterTab,
    }

    image_ratio = 566 / 1092
    shadow_image_ratio = 568 / 1024
    scale_mult = 1.08
    shadow_xscale = 1.06
    shadow_zscale = 1.075

    def __init__(self):
        base.sp = self

        # Set up the DirectFrame properties of the SocialPanel.
        DirectFrame.__init__(self, parent=render2d,
                             image=sp_gui.find('**/SocialPanel_Base'),
                             image_pos=(-0.50 * self.image_ratio, 0, -0.50),
                             image_scale=(self.image_ratio, 1, 1),
                             scale=self.scale_mult, relief=None),
        self.initialiseoptions(SocialPanel)
        self['state'] = NORMAL

        # Set up the FSM.
        FSM.__init__(self, 'social-panel')

        # Initialize the events of the Social Panel.
        self.events = {
            'open-social-panel': self.start,
            'close-social-panel': self.stop,
            'unload-social-panel': self.unload,
            'change-tab-social-panel': self.changeTab,
            'option-update-social-panel-scale': self.updateScale,
        }
        self.open_events()

        # Set up references.
        self.tabs = None
        self.shadow = None
        self.currentTab = None
        self.open = False
        self.groupIcon = None

        # Load the elements of the social panel.
        self.load()

        # Start position management.
        self.startPositionManagement()

    """
    Initialization methods
    """

    def open_events(self):
        for event, callback in self.events.items():
            self.accept(event, callback)

    def close_events(self):
        self.ignoreAll()

    """
    Loading methods
    """

    def updateScale(self, setScale=None, updatePos=True):
        if setScale is None:
            setScale = settings['social-panel-scale']
        new_scale = setScale * self.scale_mult
        self.setScale(new_scale)
        self['image_pos'] = (-0.50 * self.image_ratio, 0, -0.50)
        self['image_scale'] = (self.image_ratio, 1, 1)
        if updatePos:
            self._updatePositionManager()

    def load(self):
        self.setBin('sorted-gui-popup', GuiBinGlobals.SocialPanelBin)

        # Show the group subtext lol
        self.groupIcon = SocialPanelGroupSubtext(
            parent=self, friendsListButtons=[],
            pos=(-0.04635, 0.0, -0.9759),
            scale=0.07391,
        )

        # Add the tabs.
        self.tabs = SocialPanelTabs(self)

        # Add the shadow.
        self.shadow = DirectFrame(
            parent=self, relief=None,
            image=sp_gui.find('**/SocialPanel_Shadow'),
            image_pos=(-0.50 * self.image_ratio, 0, -0.50),
            image_scale=(self.shadow_image_ratio * self.shadow_xscale, 1, self.shadow_zscale),
        )
        self.shadow.setBin('sorted-gui-popup', GuiBinGlobals.SocialPanelBin - 1)

        # We loaded the elements of this panel, go ahead and force hide it now.
        self.stop(instant=True)

    def unload(self):
        self.close_events()
        self.defaultExit()
        self.destroy()

    def destroy(self):
        self.cleanup()
        super().destroy()

    """
    State methods
    """

    def start(self, tab: str | None = None):
        # Called when the social panel is asked to be shown.
        self.requestDefault()
        self.show()
        self.open = True
        messenger.send('social-panel-opened')
        self.updateScale(updatePos=False)
        self._updatePositionManager()
        base.flagScreenCells(ScreenCellFlag.socialPanel, base.rightCells)

    def stop(self, instant: bool = False):
        # Called when the social panel is asked to go away.
        self.defaultExit()
        self.hide()
        self.open = False
        messenger.send('social-panel-closed')
        self._updatePositionManager()
        base.unflagScreenCells(ScreenCellFlag.socialPanel, base.rightCells)

    def requestDefault(self):
        if base.cr.groupManager.group:
            self.request(self.enum2State[TAB_GROUPS])
        else:
            self.request(self.enum2State[DEFAULT_TAB])

    def enterGroup(self, _):
        """
        We've just joined a new group.
        Open up the social panel and go to it.
        """
        # First, see if we can even open.
        if not self.open:
            # if base.localAvatar.bFriendsList.isHidden():
            #     # The friends list button is hidden too, we cannot go to group state
            #     return

            # Open the Social Panel.
            self.start()

        # If we aren't on the Groups tab, transition to it.
        if self.state != self.enum2State[TAB_GROUPS]:
            self.request(self.enum2State[TAB_GROUPS])

    """
    Tab methods
    """

    def changeTab(self, tabEnum, *args):
        if not self.state:
            # we're already in transition, so block the request.
            # maybe somewhat hacky, but allows tabs to request tab changes,
            # so this is worth doing to prevent a crash
            return
        self.request(self.enum2State[tabEnum], *args)
        messenger.send('social-panel-tab-changed')

    """
    Panel states
    """

    def defaultEnter(self, *args):
        messenger.send('wakeup')
        if self.newState != 'Off':
            self.currentTab = self.state2Tab[self.newState](self)

            # hack, get rid of this when i actually place all the assets
            self.currentTab.setPos(-0.26, 0, -0.5)

    def defaultExit(self):
        if self.currentTab is not None:
            self.currentTab.destroy()
            self.currentTab = None

    def enterFriendsInvite(self, *args):
        self.defaultEnter()
        self.hide()

        def leaveState(friendInviter: FriendInviter):
            if AvatarPanel.currentAvatarPanel is not None:
                AvatarPanel.currentAvatarPanel.handleDisableAvatar()
            self.requestDefault()
        if not args:
            args = [None, None, None]
        showFriendInviter(*args, callback=leaveState)

    def exitFriendsInvite(self):
        self.defaultExit()
        self.show()

    """
    Some properties
    """

    @property
    def active(self):
        return self.currentTab is not None

    """
    Social Panel Positioning
    """

    def onscreenPositionActive(self) -> bool:
        """
        Determines if this GUI should be positioned onscreen currently.
        If not, then the GUIPositionManager will ignore this object.

        If this value changes, call self.updatePositionManager().
        """
        return self.open

    def moveInstant(self) -> bool:
        return True


if __name__ == "__main__":
    gui = SocialPanel()
    gui.start()
    from toontown.gui.GUITemplateSliders import GUITemplateSliders
    GUITemplateSliders(
        gui.groupIcon,
        'pos', 'scale'
    )
    from toontown.groups.GroupClasses import GroupClient, GroupCreation, GroupAvatar
    messenger.send('groupUpdate', [GroupClient(
        0, GroupCreation(GroupType.VP, [], 69), 0, [GroupAvatar(
            0, 'bitch', 1, True,
        )], 1, 9000, []
    )])
    base.run()
