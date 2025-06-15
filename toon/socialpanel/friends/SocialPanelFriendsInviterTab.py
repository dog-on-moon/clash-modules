"""
The Friend Inviter tab of the Social Panel.
Mostly a dummy tab, logic is handled in state transitions
of the Socialpanel.
"""
from toontown.friends.FriendInviter import FriendInviter, unloadFriendInviter, showFriendInviter, getFriendInviter
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from direct.gui.DirectGui import *


@DirectNotifyCategory()
class SocialPanelFriendsInviterTab(DirectFrame):

    def __init__(self, parent):
        # Set up the DirectFrame properties of the SocialPanelFriendsInviterTab.
        DirectFrame.__init__(self, parent=parent, relief=None)
        self.initialiseoptions(SocialPanelFriendsInviterTab)
