"""
The Friends tab of the Social Panel.
"""
from direct.interval.FunctionInterval import Wait

from toontown.chat.constants import ChatEvents, ChatGlobals
from toontown.club.ClubContainerClient import ClubContainerClient
from toontown.club.ClubGetters import ClubGetters
from toontown.friends.FriendHandle import FriendHandle
from toontown.notifications.notificationData.AddFriendNotification import AddFriendNotification
from toontown.toon.socialpanel.SocialPanelGUI import CheckboxButton, SocialPanelContextDropdown
from toontown.toon.socialpanel.friends.SocialPanelFriend import SocialPanelFriend, COLOR_DEFAULT, COLOR_SELECTED
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.toon.socialpanel.SocialPanelGlobals import *
from toontown.gui.TTGui import ScrollWheelFrame, LockingEntry
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from direct.gui.DirectGui import *
from direct.gui.DirectGuiGlobals import NORMAL, DISABLED, FLAT
from direct.interval.IntervalGlobal import Parallel, LerpFunctionInterval

SORT_ONLINE_FRIENDS = 0
SORT_ALL_FRIENDS = 1
SORT_NEARBY_TOONS = 2
SORT_ONLINE_CLUBMATES = 3
SORT_ALL_CLUBMATES = 4

START_SORT = SORT_ONLINE_FRIENDS

LEFT = -1
RIGHT = 1

FRIEND_COUNT = 10


@DirectNotifyCategory()
class SocialPanelFriendsTab(DirectFrame, ClubGetters):

    sortOrder = (
        SORT_NEARBY_TOONS, SORT_ONLINE_FRIENDS, SORT_ALL_FRIENDS, SORT_ONLINE_CLUBMATES, SORT_ALL_CLUBMATES
    )
    sortNames = {
        SORT_NEARBY_TOONS: TTLocalizer.SocialPanelFriendsSortNearby,
        SORT_ONLINE_FRIENDS: TTLocalizer.SocialPanelFriendsSortOnline,
        SORT_ALL_FRIENDS: TTLocalizer.SocialPanelFriendsSortAll,
        SORT_ONLINE_CLUBMATES: TTLocalizer.SocialPanelFriendsSortOnlineClub,
        SORT_ALL_CLUBMATES: TTLocalizer.SocialPanelFriendsSortAllClub,
    }
    BOTTOM_PADDING = 0.4
    defaultCanvasSize = (-1.931, 1.95 + 0.3751, -5.38 - 0.4, 0)  # 0.4 is bottom padding

    # sequence information
    initial_search_text = TTLocalizer.FriendsListSearchBarDefaultText

    text_zpos = 0.25
    text_sort_xshift = 0.034
    text_sort_startpos = (0.001, 0, 0.44)
    button_selectall_pos = (-0.205 + 0.012, 0, 0.342)
    button_selectall_xshift = -0.012

    text_panel_ratio = 492 / 74
    text_panel_scale = 0.0704
    arrow_button_ratio = 30 / 35
    arrow_button_scale = 0.6
    misc_button_ratio = 81 / 76
    misc_button_scale = 1.0
    search_bar_ratio = 327 / 62
    search_bar_scale = 1.0

    def __init__(self, parent):
        # Set up the DirectFrame properties of the SocialPanelFriendsTab.
        DirectFrame.__init__(self, parent=parent, relief=None)
        self.initialiseoptions(SocialPanelFriendsTab)
        self.accept('social-panel-tab-changed', self.finishStateChange)

        # Set up references.
        self.text_sort = None
        self.button_sortLeft = None
        self.button_sortRight = None
        self.frame_behindCheckbox = None
        self.checkbox_selectAll = None

        self.scroll_friendsList = None
        self.frame_infoBar = None

        self.button_openContext = None
        self.button_configure = None
        self.button_addFriend = None
        self.type_searchBar = None

        self.contextMenu = None
        self.confirmationContextMenu = None

        self.tracks = []

        # Set up default mode.
        self.selectedSort = START_SORT
        self.searchedText = ''
        self.configureMode = False
        self.friendPanels = []
        self.selectedUsers = set()
        self.contextSelectedUsers = set()
        self.sortScratch = []

        # Set up keybinds.
        self.ctrlPressed = False

        def pressCtrl(x):
            self.ctrlPressed = x
        self.accept('control', pressCtrl, [True])
        self.accept('control-up', pressCtrl, [False])

        # Load the elements of the social panel.
        self.load()
        self.bind(DGG.B3PRESS, command=self.openContextMenu)
        self.scroll_friendsList.bind(DGG.B3PRESS, command=self.openContextMenu)
        self.accept('reload-social-panel', self.reload)
        self.accept('friendsListChanged', self.reload)
        self.accept('favorite-friends-updated', self.reload)
        self.accept('social-panel-friend-context', self.openContextMenu)
        self.accept('social-panel-friend-click', self.friendButtonClicked)
        self.accept('social-panel-friends-configure', self.friendButtonSelectorClicked)

        # pain
        taskMgr.add(self.finishStateChange, 'spft-update')

    """
    Loading methods
    """

    def load(self):
        """
        Loads the contents of the Friends Tab.
        """
        button_offset = 2.8

        # Create the top row of buttons.
        self.frame_behindCheckbox = DirectFrame(
            parent=self, relief=None,
            geom=sp_gui.find('**/POPUPBAR_TITLEAREA'),
            # geom_color=COLOR_DEFAULT,
            pos=(-0.021, 0, 0.318), scale=0.05,
            geom_scale=(8.4, 1, 0.8587),
            geom_pos=(-0.0386, 0, 0.0129),
        )

        self.checkbox_selectAll = CheckboxButton(
            parent=self,
            frameColor=(0, 0, 0, 0),
            frameSize=(-0.55, 0.55, -0.55, 0.55),
            # command=self.toggleAllSelectors,
            pos=(-0.203, 0, 0.3193), scale=0.04 / 0.45,
        )

        self.text_sort = DirectLabel(parent=self, relief=None,
                                     scale=self.text_panel_scale,
                                     pos=self.text_sort_startpos,
                                     image=sp_gui.find('**/TitleBarThing'),
                                     image_scale=(self.text_panel_ratio, 1, 1),
                                     text='', text_pos=(-0.037, -0.178),
                                     text_scale=0.625,
                                     text_fg=(1, 1, 1, 1), text_shadow = (0, 0, 0, 1))
        self.text_sort['state'] = DGG.NORMAL
        self.button_sortLeft  = DirectButton(parent=self.text_sort, relief=None,
                                             image=(
                                                 sp_gui.find('**/Arrow_N'),
                                                 sp_gui.find('**/Arrow_P'),
                                                 sp_gui.find('**/Arrow_H'),
                                                 sp_gui.find('**/Arrow_D'),
                                             ),
                                             image_scale=(-self.arrow_button_ratio, 1, 1),
                                             pos=(-button_offset, 0, 0), scale=self.arrow_button_scale,
                                             command=self.sortChange, extraArgs=[LEFT])
        self.button_sortRight = DirectButton(parent=self.text_sort, relief=None,
                                             image=(
                                                 sp_gui.find('**/Arrow_N'),
                                                 sp_gui.find('**/Arrow_P'),
                                                 sp_gui.find('**/Arrow_H'),
                                                 sp_gui.find('**/Arrow_D'),
                                             ),
                                             image_scale=(self.arrow_button_ratio, 1, 1),
                                             pos=(button_offset, 0, 0), scale=self.arrow_button_scale,
                                             command=self.sortChange, extraArgs=[RIGHT])

        # The Configure button.
        self.button_configure = DirectButton(
            parent=self, relief=None, pos=(-0.194, 0, 0.372), scale=0.067, command=self.toggleConfigure,
            image_scale=(1.2143, 1, 1.0238), image=(
                sp_gui.find('**/Gear_N'),
                sp_gui.find('**/Gear_P'),
                sp_gui.find('**/Gear_H'),
            ),
            text=('', 'Configure', 'Configure', ''),
            text_scale=0.5,
            text_fg=(1, 1, 1, 1),
            text_bg=(0, 0, 0, 0.56),
            text_shadow=(0, 0, 0, 1),
            text_pos=(-0.05, 0.8),
        )

        # The Add Friend button.
        self.button_addFriend = DirectButton(
            parent=self, relief=None, pos=(-0.1188, 0, 0.372), scale=0.067, command=self.addFriend,
            image_scale=(1.2143, 1, 1.0238), image=(
                sp_gui.find('**/Add_N'),
                sp_gui.find('**/Add_P'),
                sp_gui.find('**/Add_H'),
            ),
            text=('', 'Add Friend', 'Add Friend', ''),
            text_scale=0.5,
            text_fg=(1, 1, 1, 1),
            text_bg=(0, 0, 0, 0.56),
            text_shadow=(0, 0, 0, 1),
            text_pos=(-0.05, 0.8),
        )

        # Create the scroll wheel frame.
        self.scroll_friendsList = ScrollWheelFrame(
            parent=self, relief=None, scale=0.12, pos=(0, 0, 0.296),
            frameSize=(-1.931, 1.95, -5.38 - self.BOTTOM_PADDING, 0),
            canvasSize=self.defaultCanvasSize,
            scrollBarWidth=0.3751,
            scrollDistance=0.4,
            manageScrollBars=1,
            verticalScroll_image=sp_gui.find('**/ScrollBar_BAR'),
            verticalScroll_image_scale=(0.4389, 1, 5.43),
            verticalScroll_image_pos=(1.7645, 0, -2.69),
            verticalScroll_relief=None,
        )
        self.scroll_friendsList['verticalScroll_thumb_frameColor'] = (1, 1, 1, 0)
        self.scroll_friendsList['verticalScroll_resizeThumb'] = 0
        self.scroll_friendsList['verticalScroll_thumb_image'] = sp_gui.find('**/ScrollBar')
        self.scroll_friendsList['verticalScroll_thumb_image_scale'] = (0.3813, 1, 1.35)
        self.scroll_friendsList['verticalScroll_thumb_image_pos'] = (0, 0, 0.012)
        self.scroll_friendsList.horizontalScroll.removeNode()
        self.scroll_friendsList.verticalScroll.incButton.destroy()
        self.scroll_friendsList.verticalScroll.decButton.destroy()

        PLANE = PlaneNode(f'friendslist_scroll_clipplane')
        PLANE.setPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, -5.38)))
        clipNP = self.scroll_friendsList.attachNewNode(PLANE)
        self.scroll_friendsList.setClipPlane(clipNP)

        # Create the search bar.
        self.type_searchBar = LockingEntry(
            parent=self, relief=None, scale=0.051, pos=(-0.0748, 0, 0.3632), borderWidth=(0.05, 0.05),
            frameColor=((1, 1, 1, 1), (1, 1, 1, 1), (0.5, 0.5, 0.5, 0.5)), state=DGG.NORMAL,
            text_align=TextNode.ALeft, text_scale=0.7, width=8.3, numLines=1,
            focus=0, backgroundFocus=0, cursorKeys=1, text_fg=(0, 0, 0, 1), suppressMouse=1, autoCapitalize=0,
            image=sp_gui.find('**/TextBox'), image_scale=(6.1984, 1, 1.2633),
            image_pos=(2.9857, 0, 0.1968), initialText=self.initial_search_text, clearOnFocus=True,
        )

        self.frame_infoBar = DirectFrame(
            parent=self, relief=None,
            pos=(-0.021, 0, 0.318), scale=0.05,
            geom=sp_gui.find('**/TitleBarThing'),
            geom_scale=(8.4, 1, 0.8587),
            geom_pos=(-0.0386, 0, 0.0129),
            text=TTLocalizer.FriendsListTitleStatus.get('no_friends'),
            text_scale=0.7,
            text_pos=(0, -0.2),
            text_fg=(1, 1, 1, 1),
            text_shadow=(0, 0, 0, 1),
            text_bg=(1, 1, 1, 0),
            frameSize=(-4.3, 1, -0.45, 0.45)
        )
        self.frame_infoBar['state'] = DGG.NORMAL

        self.button_openContext = DirectButton(
            parent=self, relief=None, command=self.buttonOpenContextMenu,
            pos=(0.212, 0, 0.319), scale=0.045,
            image_scale=(1.0315, 1, 1), image=(
                sp_gui.find('**/ARROWBUTTON_N'),
                sp_gui.find('**/ARROWBUTTON_P'),
                sp_gui.find('**/ARROWBUTTON_H'),
                sp_gui.find('**/ARROWBUTTON_D'),
            ), image_pos=(-0.0032, 0, -0.0257),
            text=('', 'Configure Selected', 'Configure Selected', ''),
            text_scale=0.75,
            text_fg=(1, 1, 1, 1),
            text_bg=(0, 0, 0, 0.67),
            text_shadow=(0, 0, 0, 1),
            text_pos=(-2.62, 0.8),
        )
        self.button_openContext['state'] = DGG.DISABLED

        taskMgr.remove('friends-searching')
        taskMgr.add(self.searchEntry, 'friends-searching')
        self.reload()
        self.scroll_friendsList.verticalScroll.setValue(0)

    def destroy(self):
        """
        Cleanup function for the friends tab.
        """
        self.ignoreAll()
        for track in self.tracks:
            if track and hasattr(track, 'finish'):
                track.finish()
        self.cleanupContextMenu()
        taskMgr.remove('friends-searching')
        taskMgr.remove('spft-update')
        super().destroy()

    def runTrack(self, track):
        """
        Helper function for stacking sequences,
        to make sure we properly clean them up.
        """
        self.tracks.append(track)
        track.start()
        if settings['reduce-gui-movement']:
            track.finish()

    """
    Reload methods
    """

    def reload(self):
        """
        On a status change, this reloads everything visible
        on the friends tab, including visual states, along
        with repopulating the friends list entirely.
        """
        self.cleanupContextMenu()
        self.clearAllSelectors()
        self.reloadButtonState()
        self.reloadFriends()
        self.reloadCanvas()
        self.reloadTextLabels()
        self.reloadInfoBar()

    def reloadButtonState(self):
        """
        Sets the left/right selectors to change sort
        to be disabled or normal depending on their
        position in the sort menu.
        """
        self.button_sortLeft['state'] = DISABLED
        self.button_sortRight['state'] = DISABLED
        if self.sortIndex > 0:
            self.button_sortLeft['state'] = NORMAL
        if self.getClubMgr().isInClub():
            if self.sortIndex < (len(self.sortOrder) - 1):
                self.button_sortRight['state'] = NORMAL
        else:
            if self.sortIndex < (len(self.sortOrder) - 1 - 2):
                self.button_sortRight['state'] = NORMAL

    def reloadCanvas(self):
        """
        Does some magic to make sure that the friends
        list has the right canvas size.
        """
        if self.canScroll:
            self.scroll_friendsList['canvasSize'] = (
                self.defaultCanvasSize[0], self.defaultCanvasSize[1],
                self.defaultCanvasSize[3] - (friendYOffset * self.friendCount) - self.BOTTOM_PADDING,
                self.defaultCanvasSize[3]
            )
        else:
            self.scroll_friendsList['canvasSize'] = self.defaultCanvasSize

        self.scroll_friendsList.setCanvasSize()
        if self.canScroll or True:
            self.scroll_friendsList.verticalScroll.thumb.show()
        else:
            self.scroll_friendsList.verticalScroll.thumb.hide()

    def reloadTextLabels(self):
        """
        Sets the relevant text labels to
        have the correct text.
        """
        self.text_sort.setText(self.sortNames[self.selectedSort])

    def reloadFriends(self):
        """
        Runs all relevant sort functionality.
        """
        self.preSort()
        if base.localAvatar:
            {
                SORT_NEARBY_TOONS: self.sortNearbyToons,
                SORT_ONLINE_FRIENDS: self.sortOnlineFriends,
                SORT_ALL_FRIENDS: self.sortAllFriends,
                SORT_ONLINE_CLUBMATES: self.sortOnlineClubmates,
                SORT_ALL_CLUBMATES: self.sortAllClubmates,
            }.get(self.selectedSort)()
        self.postSort()

        # Update the select all button's selected checkboxes.
        checkboxes = [panel.checkbox for panel in self.friendPanels]
        self.checkbox_selectAll.defineCheckboxGroup(checkboxes)

    def reloadInfoBar(self):
        if not self.configureMode:
            titleSuffix = {
                SORT_ONLINE_FRIENDS: 'friends',
                SORT_ALL_FRIENDS: 'total',
                SORT_NEARBY_TOONS: 'nearby',
                SORT_ONLINE_CLUBMATES: 'clubmates',
                SORT_ALL_CLUBMATES: 'total_clubmates',
            }.get(self.selectedSort)
            # We are not configuring, so just base on present friends
            text = {
                0: TTLocalizer.FriendsListTitleStatus[f'no_{titleSuffix}'],
                1: TTLocalizer.FriendsListTitleStatus[f'one_{titleSuffix}'],
            }.get(self.friendCount, TTLocalizer.FriendsListTitleStatus[f'x_{titleSuffix}'] % self.friendCount)
            self.frame_infoBar.setText(text)
        else:
            # We are based on configuring, so let's do on selected friends
            userCount = len(self.selectedUsers)
            text = {
                0: TTLocalizer.FriendsListTitleStatus['no_selected'],
                1: TTLocalizer.FriendsListTitleStatus['one_selected'],
            }.get(userCount, TTLocalizer.FriendsListTitleStatus['x_selected'] % userCount)
            self.frame_infoBar.setText(text)

    def finishStateChange(self, task=None):
        """
        Called when the SocialPanel finishes a state change.
        """
        self.scroll_friendsList.setCanvasSize()
        self.scroll_friendsList.verticalScroll.thumb['frameSize'] = (-0.21, 0.21, -0.68, 0.68)
        if task is not None:
            if not hasattr(task, 'count'):
                setattr(task, 'count', 0)
            task.count += 1
            if task.count < 2:
                return task.cont
            else:
                return task.done

    """
    Sort methods
    """

    def preSort(self):
        """
        Functions to run immediately prior to sorting the friends list.
        Basically, general cleanup.
        """
        self.scroll_friendsList.destroyChildren()  # POGGGGGGERSSSSSSSSS
        self.selectedUsers.clear()
        self.button_openContext['state'] = DGG.DISABLED
        self.friendPanels = []
        self.sortScratch = []

    def sortNearbyToons(self):
        """
        Grabs every DistributedToon in the area,
        and inserts their avId into the scroll.
        """
        for objId, obj in list(base.cr.doId2do.items()):
            if obj.dclass == base.cr.dclassesByName['DistributedToon']:
                if obj.ghostMode:  # If toon is in ghost mode don't show them in the list
                    continue
                self.sortScratch.append(obj.doId)

    def sortOnlineFriends(self):
        """
        Nabs the avId of all friends in the friends list,
        given that they're all online.
        """
        self.sortScratch.extend([avId for avId, _ in base.localAvatar.friendsList if base.cr.isFriendOnline(avId)])

    def sortAllFriends(self):
        """
        Nabs the avId of all friends in the friends list in general.
        """
        self.sortScratch.extend([avId for avId, _ in base.localAvatar.friendsList])

    def sortOnlineClubmates(self):
        if not self.getClubContainer():
            return
        self.sortScratch.extend([(clubToon.getAvId(), clubToon.getToonName()) for clubToon in self.getClubContainer().getClubToons() if clubToon.isOnline()])

    def sortAllClubmates(self):
        if not self.getClubContainer():
            return
        self.sortScratch.extend([(clubToon.getAvId(), clubToon.getToonName()) for clubToon in self.getClubContainer().getClubToons()])

    def postSort(self):
        """
        Any functions to do after the sort is complete.
        """
        # First, let's go through and sort it all alphabetically.
        def avId2Name(doId):
            if isinstance(doId, tuple):
                doId, name = doId
                return name
            handle: FriendHandle = base.cr.identifyFriend(doId)
            if not handle:
                return ''
            return handle.getName()
        self.sortScratch.sort(key=avId2Name)

        # Now, let's get the favorites and non-favorites.
        if base.localAvatar:
            f = base.localAvatar.getFavoriteFriends()
            if f:
                favorites, nonfavorites = [], []
                for toonData in self.sortScratch:
                    if isinstance(toonData, tuple):
                        avId, name = toonData
                    else:
                        avId = toonData
                    favorites.append(avId) if avId in f else nonfavorites.append(avId)

                # Update ths sort scratch to put the favorites in the front.
                self.sortScratch = favorites + nonfavorites

        # Now that we have all of the avIds in our sort scratch,
        # let's go ahead and add them all into the scroll.
        for toonData in self.sortScratch:
            if isinstance(toonData, tuple):
                avId, name = toonData
            else:
                avId = toonData
                name = None
            self.insertFriendIntoScroll(avId, name)

    def insertFriendIntoScroll(self, avId, name: str = None):
        """
        Given an avId, retrieve their handle, along with any other information,
        and then create a SocialPanelFriend based on that information.
        """
        handle: FriendHandle = base.cr.identifyFriend(avId)
        if not handle:
            if name is None:
                return
            else:
                # we have a name made, so just make a dummy handle
                handle = FriendHandle(avId, name, None)

        # Get a couple more properties of this friend.
        friend = avId in [avId for avId, _ in base.localAvatar.friendsList]
        textColor = None

        if friend:
            # the toon is a silly little friend of ours
            if handle and hasattr(handle, 'getLastOnline'):
                # if they haven't been online in a long time,
                # go ahead and have the text color reflect that.
                lastOnline = handle.getLastOnline()
                if isinstance(lastOnline, list):
                    lastOnline = lastOnline[0]
                if lastOnline and lastOnline < (base.cr.getServerTimeOfDay() - 6 * 30 * 24 * 60 * 60):
                    textColor = ToontownGlobals.ColorAvatarInactive
        else:
            # this toon is not one of our friends
            pass

        # oh yeah, let's make sure searching works too, lmao
        if self.checkSearchInvalid(handle):
            return

        # create the button
        self.friendPanels.append(
            SocialPanelFriend(self.scroll_friendsList, handle, textColor, self.friendCount, self, self.configureMode)
        )

    def checkSearchInvalid(self, handle: FriendHandle):
        """
        Given a FriendHandle, decide if it passes
        our relevant search query.
        """
        searchedText = self.searchedText.lower().replace(" ", "")
        return searchedText and searchedText not in handle.getName().lower().replace(" ", "")

    """
    Button methods
    """

    def friendButtonClicked(self, spf: SocialPanelFriend):
        """
        This gets called from a messenger call whenever
        any SocialPanelFriend gets clicked.
        """
        self.cleanupContextMenu()
        if not self.ctrlPressed and not self.configureMode:
            # We aren't trying to select them, so let's open their toon panel.
            messenger.send('clickedNametag', [spf.handle])
        else:
            # Go ahead and tell the SPF that we've selected it.
            spf.askSelect()

            # Also, guarantee that we're in the configure mode now.
            self.toggleConfigure(force=True)

    def friendButtonSelectorClicked(self, spf: SocialPanelFriend):
        """
        This gets called when the selector on
        the SocialPanelFriend gets clicked.
        """
        self.cleanupContextMenu()
        if spf.selected:
            # The SPF is now selected, let's keep up with that.
            self.selectedUsers.add(spf)
        else:
            if spf in self.selectedUsers:
                # The SPF is now no longer selected, let's throw that away.
                self.selectedUsers.remove(spf)

        # Take the Select All button, and make sure
        # it reflects the change to SelectedUsers.
        self.updateSelectAllButton()

        # Guarantee we're in selected mode now.
        self.toggleConfigure(force=True)

    def toggleAllSelectors(self):
        """
        Gets called when the Select All button is pressed.
        When it happens, we toggle the selection status
        on all SocialPanelFriend buttons.
        - If any selectors are unselected, it will select all buttons.
        - If all selectors are selected, it will unselect all buttons.
        """
        if not self.configureMode:
            return

        # First, enter Configure mode.
        self.toggleConfigure(force=True)

        # Now, go in and see if we need to set all of the user
        # buttons to be unselected, if one or more are unselected.
        anyUnselected = any(panel for panel in self.friendPanels if not panel.selected)
        if anyUnselected:
            self.clearAllSelectors()

        # Now that we've set the status on each one, let's go ahead
        # and run the onSelect call on each friend panel directly.
        for panel in self.friendPanels:
            panel.askSelect()

    def clearAllSelectors(self):
        """
        A function to directly unselect every single
        SocialFriendPanel.
        """
        for panel in self.friendPanels:
            panel.onSelect(False, False)
        self.selectedUsers.clear()
        self.updateSelectAllButton()

    def updateSelectAllButton(self):
        """
        A function to update the visual
        appearance of the Select All button.
        """
        usersSelected = len(self.selectedUsers)
        if usersSelected == 0:
            self.button_openContext['state'] = DGG.DISABLED
            # self.frame_behindCheckbox['geom_color'] = COLOR_DEFAULT
        elif usersSelected == len(self.friendPanels):
            self.button_openContext['state'] = DGG.NORMAL
            # self.frame_behindCheckbox['geom_color'] = COLOR_SELECTED
        else:
            self.button_openContext['state'] = DGG.NORMAL
            # self.frame_behindCheckbox['geom_color'] = COLOR_DEFAULT

    def sortChange(self, direction):
        """
        Gets called whenever the sort index
        chooses to change.
        """
        if 0 <= (self.sortIndex + direction) <= (len(self.sortOrder) - 1):
            # we can move the selected sort accordingly
            self.selectedSort = self.sortOrder[self.sortIndex + direction]
            global START_SORT
            START_SORT = self.selectedSort
            self.reload()
            self.scroll_friendsList.verticalScroll.setValue(0)

    def toggleConfigure(self, force=None):
        """
        Toggles the configuration mode of the Friends tab.
        """
        # First, set the mode to what we want.
        if force is not None:
            if self.configureMode == force:
                # We're already in the relevant mode, so shut up.
                self.reloadInfoBar()
                return
            self.configureMode = force
        else:
            self.configureMode = not self.configureMode
            self.updateSelectAllButton()

        def scale_text_sort(t):
            # t goes 0 to 1, where 1 is shifted and 0 is not
            x, y, z = (-0.021, 0, 0.318)
            self.frame_infoBar.setPos(x + (t * 0.0316), y, z)
            start_scale = 8.4
            scale_diff = 8.4 - 7.21
            self.frame_infoBar['geom_scale'] = (
                start_scale - (scale_diff * t), 1, 0.8587
            )
            start_left = -4.3
            left_diff = 2.0
            self.frame_infoBar['frameSize'] = (
                start_left + (left_diff * t), 1, -0.45, 0.45
            )

        # And now, handle stuff accordingly.
        d = 0.2
        if self.configureMode:
            # Enable the configure mode
            self.runTrack(Parallel(
                LerpFunctionInterval(scale_text_sort, duration=d,
                                     fromData=0.0, toData=1.0, blendType='easeOut', extraArgs=[])
            ))
        else:
            # Disable the configure mode
            self.selectedUsers.clear()
            self.button_openContext['state'] = DGG.DISABLED
            self.runTrack(Parallel(
                LerpFunctionInterval(scale_text_sort, duration=d,
                                     fromData=1.0, toData=0.0, blendType='easeOut', extraArgs=[])
            ))

        # Let the friends know to set their configure mode.
        for button in self.friendPanels:
            button.setConfigure(self.configureMode)
            if not self.configureMode:
                # Clear their button state
                button.resetClearState()

        # Update title text.
        self.reloadInfoBar()

    def addFriend(self):
        """
        Lets the world know we're trying to add a brand new Friend.
        """
        if base.localAvatar:
            base.localAvatar.addNotification(AddFriendNotification())

    def searchEntry(self, task):
        """
        Called whenever the search bar updates
        from any mean necessary.
        """
        if hasattr(self.type_searchBar, 'guiItem'):
            if self.type_searchBar.get() != self.initial_search_text:
                if self.searchedText != self.type_searchBar.get():
                    self.searchedText = self.type_searchBar.get()
                    self.reload()
        return task.cont

    """
    Context menu
    """

    def buttonOpenContextMenu(self):
        self.openContextMenu(fromButton=True)

    def openContextMenu(self, _=None, *, fromButton=False):
        """
        Called whenever any SocialPanelFriend gets right-clicked.
        Opens the contextual menu.
        """
        if not base.mouseWatcherNode.hasMouse():
            return
        if not self.selectedUsers:
            return

        # Create our context menu.
        self.cleanupContextMenu()
        self.contextSelectedUsers = self.selectedUsers.copy()

        if self.contextSelectedUsers:
            if len(self.contextSelectedUsers) == 1:
                # Single-selected
                self.contextMenu = SocialPanelContextDropdown(
                    parent=self, labelText=self.handle.getName(), survive=fromButton
                )
                self.contextMenu.addButton(text='View Stats', callback=self.context_viewStats)
                self.contextMenu.addButton(text='Send Whisper', callback=self.context_sendWhisper)
                if not self.isLocalAvatar:
                    if base.cr.groupManager.group:
                        self.contextMenu.addButton(text='Invite to Group', callback=self.context_inviteToGroup)
                    if not self.allNonFriends:
                        # Club invite time!!
                        clubContainer = base.cr.clubMgr.getLocalClub()  # type: ClubContainerClient
                        if clubContainer:
                            avId = self.handle.getDoId()
                            if avId not in clubContainer.getAvIds() and self.allNearby:
                                self.contextMenu.addButton(
                                    text='Invite to Club', red=False,
                                    callback=self.context_inviteToClub,
                                )
                        self.contextMenu.addButton(
                            text='Remove Favorite' if self.allFavorites else 'Add Favorite',
                            red=True if self.allFavorites else False,
                            callback=self.context_markFavorite,
                        )
                    self.contextMenu.addButton(
                        text='Add as Friend' if self.allNonFriends else 'Remove Friend',
                        red=False if self.allNonFriends else True,
                        callback=self.context_addFriend if self.allNonFriends else self.context_removeFriends,
                    )
            else:
                # Multi-selected
                self.contextMenu = SocialPanelContextDropdown(
                    parent=self, labelText='Multiple Toons', survive=fromButton
                )

                if base.cr.groupManager.group:
                    self.contextMenu.addButton(text='Invite Selected\nto Group', callback=self.context_inviteToGroup)
                addedFavorites = False
                if not self.allNonFriends:
                    self.contextMenu.addButton(
                        text='Mark as Favorites' if not self.allFavorites else 'Remove Favorites',
                        red=False if not self.allFavorites else True,
                        callback=self.context_markFavorite,
                    )
                    addedFavorites = True
                if not self.anyNonFriends:
                    if not addedFavorites:
                        self.contextMenu.addButton(
                            text='Mark as Favorites' if not self.allFavorites else 'Remove Favorites',
                            red=False if not self.allFavorites else True,
                            callback=self.context_markFavorite,
                        )
                    self.contextMenu.addButton(
                        text='Remove Friends',
                        red=True,
                        callback=self.context_removeFriends,
                    )

        # No context menu if no buttons.
        if self.contextMenu.getButtonCount() == 0:
            self.cleanupContextMenu()

    def cleanupContextMenu(self):
        if self.contextMenu:
            self.contextMenu.destroy()
            self.contextMenu = None
        if self.confirmationContextMenu:
            self.confirmationContextMenu.destroy()
            self.confirmationContextMenu = None

    """
    Context menu logic
    """

    def context_viewStats(self):
        """
        Views the stats of the singular handle we have.
        """
        messenger.send('clickedNametag', [self.handle])
        messenger.send('openPanelDetails')

    def context_sendWhisper(self):
        """
        Opens a whisper conversation with this toon.
        """
        handle = self.handle
        messenger.send(ChatEvents.UI_RequestWhisper, [handle.getDoId(), handle.getName()])
        self.clearAllSelectors()

    def context_inviteToGroup(self):
        """
        Invites these toons to your Group.
        """
        base.cr.groupManager.invitePlayer(self.avIds)
        self.clearAllSelectors()

    def context_inviteToClub(self):
        """
        Invites a toon into your Group.
        """
        if self.avIds:
            messenger.send('inviteAvIdToClub', [self.avIds[0]])
        self.clearAllSelectors()

    def context_addFriend(self):
        """
        Attempts to add this toon as a friend.
        """
        messenger.send('requestNewFriend', [self.handle.getDoId()])
        self.clearAllSelectors()

    def context_markFavorite(self):
        """
        Attempts to mark all handle toons as
        favorites, or unfavorites.
        """
        if not self.allFavorites:
            # make sure they're all our favorites
            base.localAvatar.addFavoriteFriend(self.avIds)
        else:
            # remove them their Favorite Status
            base.localAvatar.removeFavoriteFriend(self.avIds)
        self.clearAllSelectors()

    def context_removeFriends(self):
        """
        Attempts to remove all friends.
        """
        if not base.mouseWatcherNode.hasMouse():
            return
        self.confirmationContextMenu = SocialPanelContextDropdown(
            parent=self, survive=True, labelText='Are you sure?',
        )
        self.confirmationContextMenu.addButton(text='Yes', callback=self.__confirmRemoveFriends)
        self.confirmationContextMenu.addButton(text='No', callback=self.clearAllSelectors, red=True)

    def __confirmRemoveFriends(self):
        base.cr.removeFriendMass(self.avIds)
        messenger.send('reload-social-panel')

    """
    Super helpful context properties
    """

    @property
    def handle(self):
        """
        Gets the handle of the context selected users.
        """
        for user in self.contextSelectedUsers:
            return user.handle

    @property
    def handles(self):
        return [user.handle for user in self.contextSelectedUsers]

    @property
    def avIds(self):
        """
        Returns a list of all selected avIds.
        """
        return [user.avId for user in self.contextSelectedUsers]

    @property
    def favoriteFriends(self):
        """
        Returns a list of the LocalAvatar's favorite avIds.
        """
        return base.localAvatar.getFavoriteFriends()

    @property
    def friendsList(self):
        """
        Returns the LocalAvatar's friends list.
        Breaks them up so it's just the avIds.
        """
        return [x[0] for x in base.localAvatar.getFriendsList()]

    @property
    def allFavorites(self):
        """
        Returns true if all selected avIds
        are considered favorite.
        """
        f = self.favoriteFriends
        return all(user.avId in f for user in self.contextSelectedUsers)

    @property
    def allNonFriends(self):
        """
        Returns true if all selected avIds
        are not on our friends list.
        """
        f = self.friendsList
        return all(user.avId not in f for user in self.contextSelectedUsers)

    @property
    def allNearby(self):
        """Returns true if all selected users are nearby."""
        return all(user.avId in base.cr.doId2do for user in self.contextSelectedUsers)

    @property
    def anyNonFriends(self):
        """
        Returns true if any selected avIds
        are not on our friends list.
        """
        f = self.friendsList
        return any(user.avId not in f for user in self.contextSelectedUsers)

    @property
    def isLocalAvatar(self):
        """
        Checks if the selected avId
        is the LocalAvatar.
        """
        return self.avIds[0] == base.localAvatar.getDoId()

    """
    Various properties
    """

    @property
    def sortIndex(self):
        """
        Retrieves the current selected sort index.
        """
        return self.sortOrder.index(self.selectedSort)

    @property
    def friendCount(self):
        """
        Retrieves the number of current friendPanels.
        """
        return len(self.friendPanels)

    @property
    def canScroll(self):
        """
        Checks to see if the panel is long
        enough and able to be scrolled.
        """
        return self.friendCount > FRIEND_COUNT
