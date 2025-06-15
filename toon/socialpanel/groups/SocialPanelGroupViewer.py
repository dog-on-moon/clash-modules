"""
SocialPanelGroupViewer is used for viewing detailed information about a group.
"""
import time

from toontown.groups import GroupGlobals
from toontown.hood import ZoneUtil
from toontown.toon.gui import GuiBinGlobals
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from direct.gui.DirectGui import *
from direct.gui.DirectGuiGlobals import FLAT

from toontown.toon.socialpanel.SocialPanelGUI import SocialPanelContextDropdown
from toontown.toon.socialpanel.groups.SocialPanelGroupViewerToonsList import SocialPanelGroupViewerToonsList
from toontown.gui.TTGui import ScrollWheelFrame, OnscreenTextOutline, ExtendedOnscreenText
from toontown.toon.socialpanel.SocialPanelGlobals import STATE_BROWSE, sp_gui, getSocialPanelGroupBg, sp_gui

from toontown.groups.GroupGlobals import *
from toontown.groups.GroupClasses import GroupClient, GroupAvatarUDToon

from typing import TYPE_CHECKING, List

from toontown.utils.ColorHelper import c_white, c_black

if TYPE_CHECKING:
    from toontown.groups.DistributedGroupManager import DistributedGroupManager


ShowForceDisbandButton = False


@DirectNotifyCategory()
class SocialPanelGroupViewer(DirectFrame):
    TeleportCdTime = 3

    def __init__(self, parent, mgr, **kwargs):
        # Set up the DirectFrame properties of the SocialPanelGroupViewer.
        DirectFrame.__init__(self, parent=parent, **kwargs)
        self.initialiseoptions(SocialPanelGroupViewer)
        self.mgr = mgr  # type: DistributedGroupManager
        self.group = None
        self.viewingLocalGroup = False
        self.contextMenu = None
        self.doForce = False
        self.lastTpTime = 0

        self.infoFrame = ExtendedOnscreenText(
            parent=self,
            text='',
            pos=(-0.0701, 0.261),
            scale=0.034,
            fg=(1, 1, 1, 1.0),
            shadow=(0, 0, 0, 1),
        )

        # Set up some buttons.
        self.button_cancelView = DirectButton(
            parent=self, pos=(0.1657, 0, 0.3221),
            geom=(
                sp_gui.find('**/OrangeButton_N'),
                sp_gui.find('**/OrangeButton_P'),
                sp_gui.find('**/OrangeButton_H'),
            ),
            # geom_color=(1, 0, 0, 1.0),
            text_fg=(1, 1, 1, 1),
            text_shadow=(0, 0, 0, 1),
            frameColor=(0, 0, 0, 0),
            frameSize=(-0.06, 0.06, -0.03, 0.03),
            relief=None, text='Back',
            command=self.requestCancel,
            geom_scale=(0.1381, 1, 0.0533),
            text_scale=0.034,
            text_pos=(0, -0.01),
        )
        self.button_groupAction = DirectButton(
            parent=self, pos=(0.1657, 0, 0.2688),
            geom=(
                sp_gui.find('**/OrangeButton_N'),
                sp_gui.find('**/OrangeButton_P'),
                sp_gui.find('**/OrangeButton_H'),
            ),
            # geom_color=(1, 1, 0, 1.0),
            text_fg=(1, 1, 1, 1),
            text_shadow=(0, 0, 0, 1),
            frameColor=(0, 0, 0, 0),
            frameSize=(-0.06, 0.06, -0.03, 0.03),
            relief=None, text='',
            geom_scale=(0.1381, 1, 0.0533),
            text_scale=0.034,
            text_pos=(0, -0.01),
        )
        self.button_groupPrivacy = DirectFrame(
            parent=self, pos=(0.1657, 0, 0.2182),
            geom=sp_gui.find('**/POPUPBAR_TITLEAREA'),
            geom_color=(1, 1, 1, 0.0),
            text_fg=(1, 1, 1, 1),
            text_shadow=(0, 0, 0, 1),
            frameColor=(0, 0, 0, 0),
            frameSize=(-0.06, 0.06, -0.03, 0.03),
            relief=None, text='Public',
            geom_scale=(0.1381, 1, 0.05),
            text_scale=0.034,
            text_pos=(0, -0.01),
        )
        # Force disband for mods
        self.button_forceDisband = DirectButton(
            parent=self, pos=(-0.14, 0, 0.375), scale=0.8,
            geom=(
                sp_gui.find('**/OrangeButton_N'),
                sp_gui.find('**/OrangeButton_P'),
                sp_gui.find('**/OrangeButton_H'),
            ),
            geom_color=(1, 0.4, 0.4, 1.0),
            text_fg=(1, 1, 1, 1),
            text_shadow=(0, 0, 0, 1),
            frameColor=(0, 0, 0, 0),
            frameSize=(-0.06, 0.06, -0.03, 0.03),
            relief=None, text='MOD: Disband',
            command=self.mod_forceDisband,
            geom_scale=(0.1381*1.6, 1, 0.0533),
            text_scale=0.034,
            text_pos=(0, -0.01),
        )
        self.button_forceDisband.hide()
        self.button_forceDisband.setBin('sorted-gui-popup', GuiBinGlobals.GroupForceDisbandBin)

        self.frame_base = DirectFrame(
            parent=self, pos=(0.0012, 0, 0.4119), relief=None,
            frameColor=(1, 1, 1, 0), text='', scale=0.1344,
            text_align=TextNode.ALeft,
            geom=sp_gui.find('**/SocialPanel_Groups_Box_Base'),
            geom_scale=(456 / 129, 1, 1),
            geom_color=(0.85, 0.85, 0.85, 1),
        )
        self.frame_image = DirectFrame(
            parent=self.frame_base, relief=None,
            frameColor=(1, 1, 1, 0), text='',
            text_align=TextNode.ALeft,
            geom=sp_gui.find('**/SocialPanel_Groups_Box_Base'),
            geom_scale=(0.96 * (456 / 129), 1, 0.83),
            geom_color=(0.7, 0.7, 0.7, 1),
        )
        self.title_text = OnscreenTextOutline(
            parent=self.frame_base,
            text='',
            scale=0.35,
            fg=c_white,
            outline_fg=c_black,
            wordwrap=7.44,
            pos=(0, -0.1),
            text_dist=0.035,
        )

        # Silly toon panel
        self.toonsList = SocialPanelGroupViewerToonsList(
            parent=self, group=self.group,
            pos=(0.0, 0.0, 0.19694),
            frameSize=(-0.23399, 0.23415, -0.54534, 0.0),
        )

    def startTasks(self):
        if not taskMgr.hasTaskNamed('spgroupviewer-askforgroupinfo'):
            taskMgr.add(self.askForGroupInfo, 'spgroupviewer-askforgroupinfo')

    def destroy(self):
        taskMgr.remove('spgroupviewer-askforgroupinfo')
        if self.contextMenu:
            self.contextMenu.destroy()
            self.contextMenu = None
        super().destroy()

    def askForGroupInfo(self, task):
        if self.group:
            self.mgr.askForGroupInfo(self.group)
        task.delayTime = 5.0
        return task.again

    def show(self):
        self.toonsList.onShow()
        self.doForce = False
        super().show()

    def hide(self):
        self.toonsList.onHide()
        self.doForce = False
        super().hide()

    """
    Button update
    """

    def updateGroup(self, group: GroupClient):
        self.group = group

        # Is this our own group?
        self.viewingLocalGroup = False
        if self.mgr.group:
            if self.group.groupId == self.mgr.group.groupId:
                self.group = self.mgr.group
                self.viewingLocalGroup = True
        self.startTasks()  # start tasks if we haven't started yet

        # Update the Action button.
        bAction = self.button_groupAction
        if self.avId not in group.avIds:
            # We're not in the group, prompt to join.
            bAction.configure(text='Join', command=self.requestJoin)
        elif group.owner == self.avId:
            # We're the owner of the group, prompt to disband.
            bAction.configure(text='Actions', command=self.expandActionsDropdown)
        else:
            # Show non-leader context menu
            # Group has an announced that a battle exists, show non-leader actions menu
            bAction.configure(text='Actions', command=self.expandActionsDropdown,
                              geom=(
                                  sp_gui.find('**/OrangeButton_N'),
                                  sp_gui.find('**/OrangeButton_P'),
                                  sp_gui.find('**/OrangeButton_H'),
            ))

        # Update group-specific info.
        self.infoFrame.setTextWithVerticalAlignment(
            f"{self.group.shardName}\n{self.group.location}\n"
            f"{len(self.group.avatarList)}/{self.group.groupSize} Toons"
        )
        self.title_text['wordwrap'] = 7.44
        self.title_text['scale'] = 0.35
        self.title_text['pos'] = (0, -0.1)
        # Placeholder to reset text back to 1 line
        self.title_text['text'] = 'i'
        self.title_text.setTextWithVerticalAlignment(self.group.getName())
        oldLines = self.title_text.textNode.getNumRows()
        oldYScale = self.title_text.getYScale()
        # Cap the text to 2 rows
        self.title_text.capTextToLineCount(lines=2)
        # Adjust Y pos downwards if we were originally above 2 rows
        if oldLines > 2:
            self.title_text._shiftYPosByLineCount(2 - oldLines, yScale=oldYScale)
        self.frame_image['geom'] = getSocialPanelGroupBg(self.group, pgOnly=False)

        # Update the Privacy button.
        self.button_groupPrivacy.configure(
            text=TTLocalizer.GroupPublic if self.group.published else TTLocalizer.GroupPrivate,
            # command=self.requestPrivacy,
        )

        if ShowForceDisbandButton and GroupGlobals.hasForceDisbandPermission(base.localAvatar):
            self.button_forceDisband.show()
        else:
            self.button_forceDisband.hide()

    def updateGroupHeavy(self, group: GroupClient, detailAvatarList: List[GroupAvatarUDToon]):
        self.updateGroup(group=group)
        self.toonsList.updateGroup(group)
        self.toonsList.updateToonData(detailAvatarList)

    """
    Action Button methods
    """

    def requestCancel(self):
        messenger.send('social-panel-groups-new-state', [STATE_BROWSE])

    def requestJoin(self):
        if not self.group:
            return
        if base.localAvatar.getDoId() in self.group.avIds:
            return
        self.mgr.requestGroup(self.group.owner, force=self.doForce)
        self.doForce = True

    def requestLeave(self):
        if not self.group:
            return
        if base.localAvatar.getDoId() not in self.group.avIds:
            return
        self.mgr.leaveGroup()  # todo add context confirmation

    def mod_forceDisband(self):
        if not self.group:
            return

        if GroupGlobals.hasForceDisbandPermission(base.localAvatar):
            self.mgr.mod_forceDisband(self.group)

    """
    Actions dropdown
    """

    def expandActionsDropdown(self):
        isLeader = self.group.localAvIsOwner()
        self.contextMenu = SocialPanelContextDropdown(
            parent=self, labelText='Group Actions', survive=True
        )
        battleTeleportButton = False
        if self.group.announcedBattle and base.localAvatar.doId != self.group.avatarThatEncountered:
            battleTeleportButton = True
            # Let the AV teleport to the battle
            self.contextMenu.addButton(
                text='Teleport to Battle',
                callback=self.requestTeleportToBattle
            )
        if not battleTeleportButton and not isLeader:
            self.contextMenu.addButton(
                text='Teleport to Group Leader',
                callback=self.teleportToGroupLeader,
            )
        groupType = self.group.groupDefinition.groupType
        if groupType in GroupGlobals.BossGroupTypes and base.localAvatar.zoneId == GroupGlobals.BossGroupToCourtyard[groupType]:
            self.contextMenu.addButton(
                text='Teleport to Boss Doors',
                callback=self.teleportToBossDoors,
            )
        if groupType in GroupGlobals.FacilityGroupTypes and base.localAvatar.zoneId == GroupGlobals.FacilityGroupToEntranceZone[groupType]:
            elevatorWords = ("Kart", "Sigil")
            ourWord = "Elevator"
            for potentialWord in elevatorWords:
                if self.group.elevatorClass.find(potentialWord) != -1:
                    ourWord = potentialWord
                    break

            self.contextMenu.addButton(
                text=f'Teleport to {ourWord}',
                callback=self.teleportToFacilityElevator,
            )
        if isLeader:
            self.contextMenu.addButton(
                text='Make Private' if self.group.published else 'Make Public',
                callback=self.requestPrivacy,
            )
        self.contextMenu.addButton(
            text='Disband' if isLeader else 'Leave', red=True,
            callback=self.requestDisband if isLeader else self.requestLeave,
        )

    def requestPrivacy(self):
        """Toggle the privacy setting of the group."""
        if not self.group:
            return
        if not self.group.localAvIsOwner:
            return
        self.mgr.publishGroup(not self.group.published)

    def requestDisband(self):
        if not self.group:
            return
        if not self.group.localAvIsOwner:
            return
        self.mgr.disbandGroup()  # todo add context confirmation

    def requestTeleportToBattle(self):
        """Requests this client to teleport to the battle the AV is in"""
        if not self.group:
            return
        if not self.group.announcedBattle:
            return
        place = base.localAvatar.getPlace()
        if not place:
            return
        if place.getState() not in ('walk', 'stickerBook'):
            return

        if base.localAvatar.isTeleportAllowed() and time.time() >= (self.lastTpTime + self.TeleportCdTime):
            self.lastTpTime = time.time()
            self.mgr.requestTeleportToGroupBattle()

    def teleportToBossDoors(self):
        """Teleports the local avatar to the boss doors of the cog hq if they are in a cog boss group"""
        if not self.group:
            return
        place = base.localAvatar.getPlace()
        if not place:
            return
        if place.getState() not in ('walk', 'stickerBook'):
            return

        # Go ahead and send off the teleport request.
        if base.localAvatar.isTeleportAllowed() and time.time() >= (self.lastTpTime + self.TeleportCdTime):
            self.lastTpTime = time.time()
            avZoneId = base.localAvatar.zoneId
            base.cr.playGame.getPlace().request('TeleportOut', {'loader': ZoneUtil.getLoaderName(avZoneId),
                                                                'where': ZoneUtil.getWhereName(avZoneId, 1),
                                                                'how': 'TeleportIn',
                                                                'hoodId': ZoneUtil.getHoodId(avZoneId),
                                                                'zoneId': avZoneId,
                                                                'shardId': None,
                                                                'overrideDrain': True,
                                                                'cogHQDoor': True})

    def teleportToFacilityElevator(self):
        """Teleports the local avatar to the entrance elevator of a facility if they're in the right zone"""
        if not self.group:
            return
        place = base.localAvatar.getPlace()
        if not place:
            return
        if place.getState() not in ('walk', 'stickerBook'):
            return

        elevatorId = None
        for elevatorObj in base.cr.doFindAll(self.group.elevatorClass):
            if elevatorObj.getElevatorEntranceType() == self.group.groupDefinition.entrance:
                elevatorId = elevatorObj.doId
                break
        if not elevatorId:
            return

        # Go ahead and send off the teleport request.
        if base.localAvatar.isTeleportAllowed() and time.time() >= (self.lastTpTime + self.TeleportCdTime):
            self.lastTpTime = time.time()
            avZoneId = base.localAvatar.zoneId
            base.cr.playGame.getPlace().request('TeleportOut', {'loader': ZoneUtil.getLoaderName(avZoneId),
                                                                'where': ZoneUtil.getWhereName(avZoneId, 1),
                                                                'how': 'TeleportIn',
                                                                'hoodId': ZoneUtil.getHoodId(avZoneId),
                                                                'zoneId': avZoneId,
                                                                'shardId': None,
                                                                'overrideDrain': True,
                                                                'elevatorId': elevatorId})

    def teleportToGroupLeader(self):
        """Teleports the local avatar to the group leader"""
        if not self.group:
            return
        if self.group.localAvIsOwner():
            return
        place = base.localAvatar.getPlace()
        if not place:
            return
        if place.getState() not in ('walk', 'stickerBook'):
            return

        if base.localAvatar.isTeleportAllowed() and time.time() >= (self.lastTpTime + self.TeleportCdTime):
            self.lastTpTime = time.time()
            messenger.send('gotoAvatar', [self.group.owner, self.group.ownerName, f'foo123placeholderFake-{self.group.owner}'])

    """
    Various properties
    """

    @property
    def avId(self):
        return base.localAvatar.getDoId()
