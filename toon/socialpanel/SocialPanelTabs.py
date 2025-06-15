"""
The top row of tabs on the social panel.
"""

from toontown.toon.socialpanel.SocialPanelGlobals import *
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from direct.gui.DirectGui import *


@DirectNotifyCategory()
class SocialPanelTabs(DirectFrame):

    buttonPositions = (-0.18, -0.06, 0.06, 0.18)

    tab_ratio = 123/84
    tab_scale = 0.09

    def __init__(self, parent):
        # Set up the DirectFrame properties of the SocialPanelTabs.
        DirectFrame.__init__(self, parent=parent, relief=None)
        self.initialiseoptions(SocialPanelTabs)

        # Set up the tabs.
        self.button_friendsTab = None
        self.button_groupsTab = None
        # self.button_clubsTab = None
        self.button_closePanel = None

        self.tabFlavors = {}

        # Load the elements of the social panel.
        self.load()

    """
    Overwritten Methods
    """

    def show(self):
        super().show()
        self.tabClicked()

    """
    Button Methods
    """

    def tabClicked(self, tabEnum: int = DEFAULT_TAB):
        self.handleTabVisuals(tabEnum)
        messenger.send('change-tab-social-panel', [tabEnum])

    def closeSocialPanel(self):
        messenger.send('close-social-panel')

    def handleTabVisuals(self, tabEnum):
        # Highlights a given tab when selected.
        pass

    """
    Loading methods
    """

    def load(self):
        # Generate the regular tabs.
        bps = self.buttonPositions

        self.button_friendsTab = DirectButton(
            parent=self, image_scale=(self.tab_ratio, 1, 1), relief=None,
            image=(sp_gui.find('**/HeartButton_N'),
                   sp_gui.find('**/HeartButton_P'),
                   sp_gui.find('**/HeartButton_H')),
            command=self.tabClicked, extraArgs=(TAB_FRIENDS,),
            text=('', 'Friends', 'Friends', ''),
            text_fg=(1, 1, 1, 1),
            text_bg=(0, 0, 0, 0.0),
            text_shadow=(0, 0, 0, 1),
            text_pos=(-0.024, -1.1),
            text_scale=0.6,
        )
        self.button_groupsTab = DirectButton(
            parent=self, image_scale=(self.tab_ratio, 1, 1), relief=None,
            image=(sp_gui.find('**/ToonButton_N'),
                   sp_gui.find('**/ToonButton_P'),
                   sp_gui.find('**/ToonButton_H')),
            command=self.tabClicked, extraArgs=(TAB_GROUPS,),
            text=('', 'Groups', 'Groups', ''),
            text_fg=(1, 1, 1, 1),
            text_bg=(0, 0, 0, 0.0),
            text_shadow=(0, 0, 0, 1),
            text_pos=(-0.024, -1.1),
            text_scale=0.6,
        )
        # self.button_clubsTab = DirectButton(
        #     parent=self, image_scale=(self.tab_ratio, 1, 1), relief=None,
        #     image=(sp_gui.find('**/ClubButton_N'),
        #            sp_gui.find('**/ClubButton_P'),
        #            sp_gui.find('**/ClubButton_H')),
        #     command=self.tabClicked, extraArgs=(TAB_CLUBS,),
        #     text=('', 'Clubs', 'Clubs', ''),
        #     text_fg=(1, 1, 1, 1),
        #     text_bg=(0, 0, 0, 0.0),
        #     text_shadow=(0, 0, 0, 1),
        #     text_pos=(-0.024, -1.1),
        #     text_scale=0.6,
        # )
        self.button_closePanel = DirectButton(
            parent=self, image_scale=(self.tab_ratio, 1, 1), relief=None,
            image=(sp_gui.find('**/Close_N'),
                   sp_gui.find('**/Close_P'),
                   sp_gui.find('**/Close_H')),
            command=self.closeSocialPanel,
            text=('', 'Close', 'Close', ''),
            text_fg=(1, 1, 1, 1),
            text_bg=(0, 0, 0, 0.0),
            text_shadow=(0, 0, 0, 1),
            text_pos=(-0.024, -1.1),
            text_scale=0.6,
        )
        self.setButtonDistances(-0.433, -0.084, -0.889, 0.08)

        self.reloadVariables()
        self.tabClicked()

    def setButtonDistances(self, start, end, zpos, scale):
        buttonList = [
            self.button_friendsTab,
            self.button_groupsTab,
            # self.button_clubsTab,
            self.button_closePanel,
        ]
        for i, b in enumerate(buttonList):
            xpos = start + ((end - start) * (i / (len(buttonList) - 1)))
            b.setPos(xpos, 0, zpos)
            b.setScale(scale)

    def destroy(self):
        self.tabFlavors = {}
        del self.tabFlavors
        del self.button_friendsTab
        del self.button_groupsTab
        # del self.button_clubsTab
        del self.button_closePanel
        super().destroy()

    def reloadVariables(self):
        self.tabFlavors = {
            TAB_FRIENDS: self.button_friendsTab,
            TAB_GROUPS: self.button_groupsTab,
            # TAB_CLUBS: self.button_clubsTab,
        }
