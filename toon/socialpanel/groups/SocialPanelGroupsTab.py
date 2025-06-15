"""
The Groups tab of the Social Panel.
"""
from toontown.building.DistributedElevatorStreet import DistributedElevatorStreet
from toontown.district.DistrictGlobals import DistrictState
from toontown.hood import ZoneUtil
from toontown.notifications.notificationData.GenericTextNotification import GenericTextNotification, GenericTextId
from toontown.toon.gui import GuiBinGlobals
from toontown.toonbase.TTLocalizerEnglish import GroupCreateFailure, GroupCreateFailureHeading
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from direct.gui.DirectGui import *
from direct.fsm.FSM import FSM

from toontown.building.DistributedBuilding import DistributedBuilding
from toontown.groups.GroupGlobals import *
from toontown.groups.GroupClasses import GroupClient, GroupAvatarUDToon, GroupCreation

from typing import TYPE_CHECKING, List

from toontown.hood.ZoneUtil import zoneIdToName
from toontown.notifications.notificationData.GroupCallbackNotification import GroupCallbackNotification
from toontown.toon.socialpanel.SocialPanelGUI import SelectorButton
from toontown.toon.socialpanel.SocialPanelGlobals import STATE_VIEW, STATE_BROWSE, STATE_CREATE, sp_gui, TAB_GROUPS
from toontown.toon.socialpanel.groups.SocialPanelGroupBrowser import SocialPanelGroupBrowser
from toontown.toon.socialpanel.groups.SocialPanelGroupQuickInvite import SocialPanelGroupQuickInvite
from toontown.toon.socialpanel.groups.SocialPanelGroupViewer import SocialPanelGroupViewer
from toontown.utils.InjectorTarget import InjectorTarget

if TYPE_CHECKING:
    from toontown.distributed.DistributedDistrict import DistributedDistrict
    from toontown.groups.DistributedGroupManager import DistributedGroupManager


@DirectNotifyCategory()
class SocialPanelGroupsTab(DirectFrame, FSM):

    @InjectorTarget
    def __init__(self, parent):
        # Set up the DirectFrame properties of the SocialPanelGroupsTab.
        DirectFrame.__init__(self, parent=parent, relief=None)
        self.initialiseoptions(SocialPanelGroupsTab)

        # Handle FSM stuff.
        FSM.__init__(self, 'social-panel-groups-tab')

        # Set up references.
        self.mgr = base.cr.groupManager  # type: DistributedGroupManager
        self.scroll_groupList = None
        self.button_groupCreate = None
        self.button_groupFilter = None
        self.button_groupInfo = None
        self.browseButtons = []

        # Group creation buttons.
        self.selectorButton_groupType = None
        self.selectorButton_location = None
        self.selectorButton_condition = None
        self.selectorButton_groupSize = None
        self.selectorButton_privacy = None
        self.text_groupCapacity = None
        self.button_toggleInvitePanel = None
        self.button_completeGroup = None
        self.button_cancelGroup = None
        self.button_groupPrivacyInfo = None
        self.quickInvitePanel = None
        self.createButtons = []
        self.createSelectorButtons = []

        # Viewer buttons.
        self.socialPanelGroupsView = None  # type: SocialPanelGroupViewer
        self.viewButtons = []

        # Set up calls.
        self.accept('groupCallbackFailure', self.handleCallbackFailure)
        self.accept('social-panel-groups-new-state', self.request)
        self.accept('social-panel-groups-request-join', self.attemptEnterGroup)
        self.accept('zoneChange', self.refreshCreate)
        self.accept('joinedNewGroup', self.request, extraArgs=[STATE_VIEW])
        self.accept('groupUpdate', self.updateView)
        self.accept('receiveGroupInfo', self.updateViewHeavy)
        self.accept('groupLeaveResponse', self.handleGroupLeave)
        self.accept('social-panel-toon-quick-invited', lambda _, __: self.updateCapacityText())
        self.accept('groupSystemCrashed', self.handleSystemCrash)

        # Keep track of the invited toons for creating a group.
        self.invitedToons = []
        self.groupDef = None
        self.invitePanelOpen = False
        self.wantForce = False

        # Load the elements of the social panel.
        self.load()
        self.hideButtons(exceptions=[self.scroll_groupList])

        # Enter our first state.
        if self.group:
            self.request(STATE_VIEW, self.group)
        else:
            self.request(STATE_BROWSE)

        # Some messenger calls
        self.accept('spgqi-open', self.openInvitePanel)
        self.accept('spgqi-close', self.closeInvitePanel)

    def destroy(self):
        self.cleanup()
        self.ignoreAll()
        super().destroy()

    """
    Loading methods
    """

    def load(self):
        """
        Browser Buttons
        """
        self.scroll_groupList = SocialPanelGroupBrowser(self, self.mgr)
        self.button_groupCreate = DirectButton(
            parent=self, frameColor=(0.796, 0.702, 0.078, 1.0),
            relief=None, pos=(-0.127, 0, 0.4348), # frameSize=(-0.15, 0.15, -0.1, 0.1),
            text='Create',
            text_align=TextNode.ACenter,
            text_scale=0.04,
            text_pos=(0.024, -0.011),
            text_fg=Vec4(1, 1, 1, 1),
            text_shadow=Vec4(0, 0, 0, 1),
            command=self.handleCreate,
            geom=(
                sp_gui.find('**/GroupAdd_N'),
                sp_gui.find('**/GroupAdd_P'),
                sp_gui.find('**/GroupAdd_H'),
            ), geom_scale= (0.08 * (221 / 84), 1, 0.08),
        )
        self.button_groupFilter = DirectButton(
            parent=self, frameColor=(0.796, 0.702, 0.078, 1.0),
            relief=None, pos=(0.083, 0, 0.4348), # frameSize=(-0.15, 0.15, -0.1, 0.1),
            text='Filter',
            text_align=TextNode.ACenter,
            text_scale=0.04,
            text_pos=(0.024, -0.011),
            text_fg=Vec4(1, 1, 1, 1),
            text_shadow=Vec4(0, 0, 0, 1),
            command=self.handleFilter,
            geom=(
                sp_gui.find('**/GroupSearch_N'),
                sp_gui.find('**/GroupSearch_P'),
                sp_gui.find('**/GroupSearch_H'),
            ), geom_scale=(0.08 * (221 / 84), 1, 0.08)
        )
        self.button_groupInfo = DirectButton(
            parent=self, frameColor=(0.392, 0.114, 0.706, 1.0),
            relief=None, pos=(0.2101, 0, 0.4348),  # frameSize=(-0.05, 0.05, -0.1, 0.1),
            command=self.handleInfo, extraArgs=[Responses.HelpGeneral],
            geom=(
                sp_gui.find('**/Question_N'),
                sp_gui.find('**/Question_P'),
                sp_gui.find('**/Question_H'),
            ), geom_scale=(0.1 * (40 / 84), 1, 0.08)
        )
        self.browseButtons = [self.scroll_groupList, self.button_groupCreate,
                              self.button_groupFilter, self.button_groupInfo]
        """
        Group Create Buttons
        """
        TOP = 0.3828
        BOTTOM = -0.09
        STEP = (BOTTOM - TOP) / 3
        self.selectorButton_groupType = SelectorButton(parent=self, pos=(0, 0, TOP), width=0.6, title='Group Type', callback=self.updateGroupType)
        self.selectorButton_condition = SelectorButton(parent=self, pos=(0, 0, TOP + STEP), width=0.6, title='Condition')
        self.selectorButton_condition_hide = SelectorButton(parent=self, pos=(0, 0, TOP + STEP), width=0.6, disabled=True, title='Condition')
        self.selectorButton_location = SelectorButton(parent=self, pos=(0, 0, BOTTOM - STEP), width=0.6, title='Location')
        self.selectorButton_groupSize = SelectorButton(parent=self, pos=(-0.124, 0, BOTTOM), width=0.20, title='Group Size', callback=self.updateCapacityText)
        self.selectorButton_privacy = SelectorButton(parent=self, pos=(0.124, 0, BOTTOM), width=0.20, title='Privacy')
        self.selectorButton_privacy.titleText['text_pos'] = (-0.03, 0.086)
        self.button_groupPrivacyInfo = DirectButton(
            parent=self, frameColor=(0.392, 0.114, 0.706, 1.0),
            relief=None, pos=(0.1921, 0, -0.02811), scale=0.6254,
            command=self.handleInfo, extraArgs=[Responses.HelpPrivacy],
            geom=(
                sp_gui.find('**/Question_N'),
                sp_gui.find('**/Question_P'),
                sp_gui.find('**/Question_H'),
            ), geom_scale=(0.047, 1.0, 0.0782)
        )
        self.quickInvitePanel = SocialPanelGroupQuickInvite(parent=self)
        self.quickInvitePanel.hide()
        self.text_groupCapacity = DirectFrame(
            parent=self, relief=None, pos=(0, 0, -0.20262),
            text=TTLocalizer.GroupCapacityLabel,
            text_scale=0.04,
            text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1),
        )
        self.button_toggleInvitePanel = DirectButton(
            parent=self, pos=(0.00151, 0.0, -0.26443), relief=None,
            text='Invite Toons', text_pos=(0, -0.01), scale=0.8,
            geom=(
                sp_gui.find('**/OrangeButton_N'),
                sp_gui.find('**/OrangeButton_P'),
                sp_gui.find('**/OrangeButton_H'),
            ), geom_scale=(0.09 * (164 / 63), 1, 0.09), geom_color=(0.9, 0.9, 0.9, 1.0),
            text_scale=0.039, command=self.toggleInvitePanelVisibility,
            text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1),
        )
        self.button_completeGroup = DirectButton(
            parent=self, pos=(-0.1149, 0, -0.38484), relief=None,
            text='Create', text_pos=(0, -0.01), scale=1,
            geom=(
                sp_gui.find('**/OrangeButton_N'),
                sp_gui.find('**/OrangeButton_P'),
                sp_gui.find('**/OrangeButton_H'),
            ), geom_scale=(0.09 * (164 / 63), 1, 0.09), geom_color=(0.9, 0.9, 0.9, 1.0),
            text_scale=0.039, command=self.createGroup,
            text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1),
        )
        self.button_completeGroup.setBin('sorted-gui-popup', GuiBinGlobals.SocialPanelBin + 5)
        self.button_cancelGroup = DirectButton(
            parent=self,
            pos=(0.11779, 0.0, -0.38484),
            scale=1.0,
            relief=None,
            text='Cancel', text_pos=(0, -0.01),
            geom=(
                sp_gui.find('**/RedButton_N'),
                sp_gui.find('**/RedButton_P'),
                sp_gui.find('**/RedButton_H'),
            ), geom_scale=(0.23325, 1.0, 0.09), geom_color=(0.9, 0.9, 0.9, 1.0),
            text_scale=0.039, command=messenger.send, extraArgs=['change-tab-social-panel', [TAB_GROUPS]],
            text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1),
        )
        self.button_cancelGroup.setBin('sorted-gui-popup', GuiBinGlobals.SocialPanelBin + 5)
        self.createSelectorButtons = [
            self.selectorButton_groupType, self.selectorButton_location,
            self.selectorButton_condition, self.selectorButton_groupSize,
            self.selectorButton_privacy
        ]
        self.createButtons = self.createSelectorButtons + [self.quickInvitePanel,
                              self.text_groupCapacity, self.button_completeGroup,
                              self.button_toggleInvitePanel,
                              self.button_cancelGroup, self.selectorButton_condition_hide,
                              self.button_groupPrivacyInfo]
        """
        View Create Buttons
        """
        self.socialPanelGroupsView = SocialPanelGroupViewer(self, self.mgr)
        self.viewButtons = [self.socialPanelGroupsView]

    def hideButtons(self, exceptions=None):
        if exceptions is None:
            exceptions = []
        for button in self.browseButtons + self.createButtons + self.viewButtons:
            if button in exceptions:
                continue
            button.hide()

    """
    State methods
    """

    #
    # The Browse state represents the actual browser
    # mode of the Groups Tab. It's effectively the
    # standard mode, unless you are already in a group,
    # in which case you'll start in the View state.
    #

    def enterBrowse(self):
        for button in self.browseButtons:
            if not button:
                # Oops, we're cleaned up.
                return
            button.show()
        if not self.mgr.group:
            self.button_groupCreate.setText('Create')
        else:
            self.button_groupCreate.setText('View')
    
        # Update the button image depending on if we have a group or not
        prefix = 'Add' if not self.mgr.group else 'View'
        geomList = (
                sp_gui.find(f'**/Group{prefix}_N'),
                sp_gui.find(f'**/Group{prefix}_P'),
                sp_gui.find(f'**/Group{prefix}_H'),
            )
        self.button_groupCreate['geom'] = geomList

    def exitBrowse(self):
        for button in self.browseButtons:
            button.hide()

    def doShardClosedNotification(self) -> None:
        base.localAvatar.addNotification(GenericTextNotification(
            textId=GenericTextId.DistrictMaintenanceCantCreateGroup,
            title=GroupCreateFailureHeading[Responses.DistrictDraining],
            subtitle=GroupCreateFailure[Responses.DistrictDraining],
        ))

    def doShardFullNotification(self) -> None:
        base.localAvatar.addNotification(GenericTextNotification(
            textId=GenericTextId.DistrictFullCantCreateGroup,
            title=GroupCreateFailureHeading[Responses.DistrictFull],
            subtitle=GroupCreateFailure[Responses.DistrictFull],
        ))

    def doShardFullPizzeriaNotification(self) -> None:
        base.localAvatar.addNotification(GenericTextNotification(
            textId=GenericTextId.DistrictMaintenanceCantCreateGroup,
            title=GroupCreateFailureHeading[Responses.DistrictFull],
            subtitle=GroupCreateFailure[Responses.DistrictFull],
        ))

    def handleCreate(self):
        if self.zoneId not in GroupZones and ZoneUtil.getHoodId(self.zoneId) not in FullHoodGroupZones:
            return

        # Don't let the local av create a group if this shard is down for maintenance
        localShard: 'DistributedDistrict' = base.cr.getLocalShard()
        if localShard:
            if localShard.available != DistrictState.ONLINE:
                self.doShardClosedNotification()
                return

            # Don't let the local av create a group if this shard has reached max pop
            if localShard.avatarCount >= localShard.maxPop:
                self.doShardFullNotification()
                return

        groupDefs = []
        if self.zoneId in GroupZones:
            groupDefs.extend(GroupZones[self.zoneId].copy())
        # Add full hood groups as well
        if ZoneUtil.getHoodId(self.zoneId) in FullHoodGroupZones:
            for fullHoodGroupDef in FullHoodGroupZones[ZoneUtil.getHoodId(self.zoneId)].copy():
                # We may have duplicates if you are sitting in a playground, so filter those out.
                if fullHoodGroupDef not in groupDefs:
                    groupDefs.append(fullHoodGroupDef)
        # Now filter out group defs that aren't available (Holiday requirement)
        groupDefs = [groupDef for groupDef in groupDefs if groupDef.isGroupAvailable]
        groupDefs = self.filterForCogBuildings(groupDefs)
        if not groupDefs:
            return
        if not self.mgr.group:
            self.request(STATE_CREATE)
        else:
            self.request(STATE_VIEW, self.mgr.group)

    def handleFilter(self):
        self.scroll_groupList.switchFilterStatus()

    @staticmethod
    def handleInfo(helpResponse):
        # Spawn a Toon-Tip describing the Group Viewer.
        if base.localAvatar:
            base.localAvatar.addNotification(
                GroupCallbackNotification(
                    errorType=Responses.Info,
                    errorCode=helpResponse,
                )
            )

    #
    # The View state is active when we're
    # looking at a specific group.
    # Gets passed a GroupStruct to build information.
    #

    def enterView(self, group: GroupClient):
        self.hideButtons()
        for button in self.viewButtons:
            button.show()

        # Now that we've activated all the relevant view information,
        # we're going to just go ahead and have our groupStruct fill in everything.
        self.updateView(group)

    def exitView(self):
        for button in self.viewButtons:
            button.hide()

    def updateView(self, group: GroupClient):
        if self.state is None:
            if self.newState != STATE_VIEW:
                return
        elif self.state != STATE_VIEW:
            return
        # Update the Group Viewer.
        self.socialPanelGroupsView.updateGroup(group)

    def updateViewHeavy(self, group: GroupClient, detailAvatarList: List[GroupAvatarUDToon]):
        if self.state != STATE_VIEW:
            return
        # We've finally received more information,
        # so let's go ahead and incorporate it.
        self.socialPanelGroupsView.updateGroupHeavy(group, detailAvatarList)

    #
    # The Create state is when we're looking
    # to create a brand new group ourselves.
    #

    def enterCreate(self):
        # First, we'll go ahead and show all the create buttons.
        for button in self.createButtons:
            button.show()

        # 'Cept the invite panel.
        self.quickInvitePanel.hide()
        self.invitePanelOpen = False

        # Refresh our invited toons list.
        self.invitedToons = []
        self.groupDef = None

        # Then, refresh the buttons.
        self.refreshCreate()

    def exitCreate(self):
        for button in self.createButtons:
            button.hide()

        # Reset stuffs
        self.invitedToons = []
        self.invitePanelOpen = False
        self.groupDef = None
        self.wantForce = False

    def refreshCreate(self, _=None):
        if self.state is None:
            if self.newState != STATE_CREATE:
                return
        else:
            if self.state != STATE_CREATE:
                return

        # First, go ahead and use our zone id.
        groupDefs = []
        if self.zoneId in GroupZones:
            groupDefs.extend(GroupZones[self.zoneId].copy())
        # Add full hood groups as well
        if ZoneUtil.getHoodId(self.zoneId) in FullHoodGroupZones:
            for fullHoodGroupDef in FullHoodGroupZones[ZoneUtil.getHoodId(self.zoneId)].copy():
                # We may have duplicates if you are sitting in a playground, so filter those out.
                if fullHoodGroupDef not in groupDefs:
                    groupDefs.append(fullHoodGroupDef)
        # Now filter out group defs that aren't available (Holiday requirement)
        groupDefs = [groupDef for groupDef in groupDefs if groupDef.isGroupAvailable]
        # Filter out cog buildings.
        groupDefs = self.filterForCogBuildings(groupDefs)

        # No group defs? Push back to browse.
        if not groupDefs:
            self.request(STATE_BROWSE)
            return

        # Update options gaming
        groupTexts = []
        for groupDef in groupDefs:
            localizerText = GroupTypeLocalizer[groupDef.groupType]
            if '%s' in localizerText:
                # hack for cog buildings, but i'm tired
                optString = BGOptionsLocalizer.get(groupDef.getOptions()[1].default, '%s')
                localizerText = localizerText % optString
            groupTexts.append(localizerText)
        self.selectorButton_groupType.setOptions(
            values=groupDefs,
            texts=groupTexts,
            setIndex=0,
        )
        self.groupDef = self.selectorButton_groupType.getChoice()
        if not self.groupDef:
            self.request(STATE_BROWSE)
            return
        self.updateGroupType(self.groupDef)
        locationZoneId = ZoneUtil.getHoodId(self.zoneId) if self.groupDef.allowFullHood else self.zoneId
        if locationZoneId in TTLocalizer.GroupShortLocationNames:
            locationName = TTLocalizer.GroupShortLocationNames[locationZoneId]
        else:
            locationName = zoneIdToName(locationZoneId)[1]
        self.selectorButton_location.setOptions(
            values=[None],
            texts=[locationName],
            setIndex=0,
        )
        self.selectorButton_privacy.setOptions(
            values=[True, False],
            texts=[TTLocalizer.GroupPublic, TTLocalizer.GroupPrivate],
            setIndex=0, wraparound=True,
        )

        messenger.send('social-panel-groups-tab-enter-create')

    def updateCapacityText(self, newCap=None):
        cap = newCap or self.selectorButton_groupSize.getChoice()
        self.invitedToons = self.quickInvitePanel.getInvitedAvIds()[:cap - 1]
        self.text_groupCapacity.setText(
            TTLocalizer.GroupCapacityLabel % (len(self.invitedToons) + 1, cap)
        )

    def canInviteToons(self) -> bool:
        """
        Method check to see if we can invite more toons.
        :return: True if there's room open, False otherwise.
        """
        cap = self.selectorButton_groupSize.getChoice()
        return len(self.quickInvitePanel.getInvitedAvIds()) < (cap - 1)

    def updateGroupType(self, groupDef: GroupDefinition):
        self.groupDef = groupDef
        options: GroupOptions = groupDef.getOptions()[0]
        if options is not None:
            self.selectorButton_condition.show()
            self.selectorButton_condition.setTitleText(options.label)
            self.selectorButton_condition.setOptions(
                values=options.options,
                texts=[BGOptionsLocalizer[opt] for opt in options.options],
                setIndex=0,
            )
            self.selectorButton_condition_hide.hide()
        else:
            self.selectorButton_condition.hide()
            self.selectorButton_condition_hide.show()
        self.selectorButton_groupSize.setOptions(
            values=groupDef.maxSize,
            texts=groupDef.maxSize,
        )
        self.updateCapacityText()
        self.wantForce = False

    def createGroup(self):
        if self.state != STATE_CREATE:
            return
        groupDef = self.selectorButton_groupType.getChoice()
        # Cancel out if they somehow managed to try and create a group for a restricted group
        if not groupDef.isGroupAvailable:
            return

        groupType = groupDef.groupType
        groupOptions = groupDef.defaultOptions[:]
        if self.selectorButton_condition.options and groupOptions:
            groupOptions[0] = self.selectorButton_condition.getChoice().value
        groupSize = self.selectorButton_groupSize.getChoice()
        published = self.selectorButton_privacy.getChoice()
        self.mgr.createGroup(GroupCreation(groupType, groupOptions, groupSize), self.invitedToons, published, force=self.wantForce)
        self.wantForce = True

    def toggleInvitePanelVisibility(self):
        """
        Sets the invite panel to be open or closed.
        :return: None.
        """
        self.invitePanelOpen = not self.invitePanelOpen
        if self.invitePanelOpen:
            # the panel is now open
            self.quickInvitePanel.show()
        else:
            # the panel is now closed
            self.quickInvitePanel.hide(instant=False)

    def openInvitePanel(self):
        for button in self.createSelectorButtons:
            button.setButtonState(False)
        self.button_groupPrivacyInfo['state'] = DGG.DISABLED

    def closeInvitePanel(self):
        for button in self.createSelectorButtons:
            button.updateButtons()
        self.button_groupPrivacyInfo['state'] = DGG.NORMAL

    """
    Interactions with mgr
    """

    def handleCallbackFailure(self, errorCode: Responses, errorType: Responses):
        """
        Message received from DistributedGroupManager.
        Gets called whenever a failure of some form occurs.
        """
        pass

    def attemptEnterGroup(self, avId, force=False):
        """
        Attempts to join an avId's group.
        """
        self.mgr.requestGroup(avId, force=force)

    """
    Response handling
    """

    def handleGroupLeave(self, response: Responses):
        responseFunc = {
            Responses.LeaveDisbanded: self.handleDisband,
            Responses.LeaveKicked: self.handleKicked,
        }.get(response, None)
        if responseFunc is not None:
            responseFunc()
        if response != Responses.LeaveDisbanded:
            self.request(STATE_BROWSE)

    def handleDisband(self):
        if self.state == STATE_VIEW:
            if self.socialPanelGroupsView.viewingLocalGroup:
                # Our group got disbanded while we were looking at it.
                messenger.send('change-tab-social-panel', [TAB_GROUPS])
        elif self.state == STATE_BROWSE:
            # Reload the browser since our group disbanded.
            messenger.send('change-tab-social-panel', [TAB_GROUPS])

    def handleKicked(self):
        # This is called both when the client is kicked/leaves their group.
        if self.state == STATE_VIEW:
            if self.socialPanelGroupsView.viewingLocalGroup:
                # We got kicked from the group we were in.
                messenger.send('change-tab-social-panel', [TAB_GROUPS])
        elif self.state == STATE_BROWSE:
            # Reload the browser since we got kicked from our group.
            messenger.send('change-tab-social-panel', [TAB_GROUPS])

    def handleSystemCrash(self):
        # The group system crashed, go to browse state.
        self.request(STATE_BROWSE)

    """
    Various properties
    """

    @property
    def inGroup(self):
        return bool(self.mgr.group)

    @property
    def group(self):
        if not self.inGroup:
            return None
        return self.mgr.group

    @property
    def zoneId(self):
        if base.localAvatar:
            return base.localAvatar.zoneId
        return 2000

    """
    Static methods
    """

    @staticmethod
    def filterForCogBuildings(groupDefs: list):
        """
        We filter for local cog buildings given a list of groupDefs.

        Basically, we just make our own groupDefs,
        based on the context of nearby buildings.

        :param groupDefs: A list of groupDefs.
        """
        # Clear out cog building groupdefs.
        retGroupDefs = []
        for groupDef in groupDefs:
            if groupDef.zoneId is BuildingZones:
                continue
            retGroupDefs.append(groupDef)

        # Build our own groupdefs.
        elevatorClassName = 'DistributedElevatorStreet'
        for do in base.cr.doId2do.values():
            if do.__class__.__name__ == elevatorClassName:
                do: DistributedElevatorStreet
                bldg: DistributedBuilding = do.bldg
                if bldg.mode != 'suit':
                    continue
                if not hasattr(bldg, 'track'):
                    continue

                # OK, we can make a groupdef with this elevator
                track = bldg.track
                floors = bldg.numFloors
                trackOpt = {
                    'c': GroupType.BuildingBoss,
                    's': GroupType.BuildingSell,
                    'l': GroupType.BuildingLaw,
                    'm': GroupType.BuildingCash,
                    'g': GroupType.BuildingBoard,
                }.get(chr(track))
                floorOpt = [Options.ONE, Options.TWO, Options.THREE,
                            Options.FOUR, Options.FIVE, Options.SIX][floors - 1]
                groupDef = makeBuildingGroupDef(floors=[floorOpt], forceType=trackOpt)
                retGroupDefs.append(groupDef)

        # Our group defs are gamer now.
        return retGroupDefs
