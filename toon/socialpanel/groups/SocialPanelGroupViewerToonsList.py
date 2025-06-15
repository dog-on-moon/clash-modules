"""
The ScrollWheelFrame containing SocialPanelGroupViewerToon instances.
"""
from toontown.building.interior.globals import PizzaRankGlobals
from toontown.utils.ColorHelper import hexToPCol

if __name__ == "__main__":
    from tools.headless.headlessbase.HeadlessBase import HeadlessBase
    base = HeadlessBase(wantHotkeys=False)
    if __debug__:
        from toontown.utils.DeveloperInjector import startInjector
        startInjector()
    # base.initCR()  # defines base.cr
    # base.startHeadlessShow()

from typing import List, TYPE_CHECKING, Optional

from toontown.battle.gui.special.TrackWidget import TrackWidget
from toontown.gui import UiHelpers
from toontown.toon.socialpanel.SocialPanelGUI import SocialPanelContextDropdown
from toontown.gui.EasyManagedButton import EasyManagedButton
from toontown.friends.FriendHandle import FriendHandle
from toontown.groups.GroupEnums import Options
from toontown.modifiers.contentsync.ContentSyncDefinitions import GroupTypeToGTSDef, ContentSyncDefinitions
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from direct.gui.DirectGuiGlobals import FLAT

from toontown.gui.EasyScrolledFrame import EasyScrolledFrame
from toontown.gui.EasyManagedItem import EasyManagedItem

from toontown.groups.GroupClasses import GroupAvatarUDToon, GroupCreation, GroupClient, GroupAvatar
from toontown.toon.gui import GuiBinGlobals
from toontown.toon.socialpanel.SocialPanelGlobals import *
from toontown.battle import BattleGlobals
from toontown.gui.TTGui import kwargsToOptionDefs, OnscreenTextOutline

from direct.interval.IntervalGlobal import *

if TYPE_CHECKING:
    pass


@DirectNotifyCategory()
class SocialPanelGroupViewerToonsList(EasyScrolledFrame):

    def __init__(self, parent, group, **kw):
        # Set up the SocialPanelClubsTabBase properties of the SocialPanelClubsTabMembers.
        optiondefs = kwargsToOptionDefs(
            pos=(0, 0, 0), scale=1.0, relief=FLAT,
            frameSize=(-0.0, 0.5, -0.5, 0.0),
            frameColor=(0.278, 0.424, 0.259, 0.33),

            # Scroll bar parameters
            clipFrame=False,
            scrollBarWidth=0,
            hideScroll=True,
            hideThumb=True,
            scrollDistance=0.0655,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent=parent, relief=None)
        self.initialiseoptions(SocialPanelGroupViewerToonsList)

        # Define state
        self.group: GroupClient = group
        self.detailAvatarList: List[GroupAvatarUDToon] = []
        self.toonsList = {}
        self.toonFrames = []
        self.previousPos = None
        self.previousCollapsed = True
        self.frame_panelTitle = None
        self.contextMenu = None

        # GUI defined
        self.text_loading = DirectFrame(
            parent=self, relief=None,
            pos=(0.00588, 0.0, -0.08289),
            scale=0.15344,
            text="Loading...", text_fg=(0.122, 0.278, 0.106, 1.0),
            text_scale=0.36, text_pos=(0, 0),
        )
        self.text_loading.hide()

        # Event hooks
        self.accept('spgvtl-updatePositions', self.updateItemPositions)

    def debug(self):
        return
        self.group = GroupClient(
            groupId=0,
            groupCreation=GroupCreation(
                groupType=GroupType.Pizzeria,
                groupOptions=[Options.SOCIAL_PARTY],
                groupSize=99,
            ),
            districtId=0,
            avatarList=[
                GroupAvatar(10, '', 0, False),
                GroupAvatar(20, '', 1, False),
                GroupAvatar(30, '', 0, True),
                GroupAvatar(40, '', 1, True),
                GroupAvatar(50, '', 0, False),
            ],
            published=True,
            zoneId=3740,
            kickedAvIds=[],
            announcedBattle=False,
            avatarThatEncountered=0,
        )
        self.updateToonData(
            [
                GroupAvatarUDToon(10, 'John', 3740, 0, 100, [5, 5, 5, 5, 5, 5, 5, 5], [-1, -1, -1, -1, -1, -1, -1, -1]),
                GroupAvatarUDToon(20, 'marcus', 3740, 0, 110, [5, 5, 5, 5, 5, 5, 5, 5],
                                  [-1, -1, -1, -1, -1, -1, -1, -1]),
                GroupAvatarUDToon(30, 'the legend fabled across time and space', 3740, 0, 120, [5, 5, 5, 5, 5, 5, 5, 5],
                                  [-1, -1, -1, -1, -1, -1, -1, -1]),
                GroupAvatarUDToon(40, 'JOHN TWO', 3740, 0, 130, [5, 5, 5, 5, 5, 5, 5, 5],
                                  [-1, -1, -1, -1, -1, -1, -1, -1]),
                GroupAvatarUDToon(50, 'mrowm eow', 3069, 0, 140, [5, 5, 5, 5, 5, 5, 5, 5],
                                  [-1, -1, -1, -1, -1, -1, -1, -1]),
            ]
        )

    def onHide(self):
        self.group = None
        self.removeAllItems()

    def onShow(self):
        self.group = None
        self.removeAllItems()
        self.text_loading.show()
        self.debug()

    def destroy(self):
        self.ignoreAll()
        self.cleanupContextMenu()
        super().destroy()

    def cleanupContextMenu(self):
        if self.contextMenu:
            self.contextMenu.destroy()
            self.contextMenu = None

    def updateGroup(self, group):
        self.group = group

    def updateToonData(self, detailAvatarList: List[GroupAvatarUDToon] = None):
        """
        Updates the Toon Data from the SPGVTL.
        :return: None.
        """
        self.text_loading.show()
        if detailAvatarList:
            self.detailAvatarList = detailAvatarList
        self.createToonGUI()

    def createToonGUI(self):
        if not self.group:
            self.removeAllItems()
            return

        # Hide GUI.
        self.text_loading.hide()

        # Get some consts.
        groupSize = self.group.groupSize
        currentToonCount = len(self.detailAvatarList)
        missingToonCount = groupSize - currentToonCount

        # Figure out our frame class.
        frameCls = self.getFrameClass()

        # Prepare panel work
        avs = 0
        openedPanels = []
        for frame in self.getCanvasItems():
            if isinstance(frame, frameCls) and frame.menuOpen:
                openedPanels.append(frame.av.avId)
        self.removeAllItems()

        # Create toon panels for everyone.
        for av in self.detailAvatarList:
            avs += 1
            frameCls(
                av=av, group=self.group,
                detailAvatarList=self.detailAvatarList,
                index=avs, openedPanels=openedPanels,
                easyScrolledFrame=self,
            )

        for i in range(missingToonCount):
            avs += 1
            frameCls(
                av=None, group=self.group,
                detailAvatarList=self.detailAvatarList,
                index=avs, openedPanels=openedPanels,
                easyScrolledFrame=self,
            )

        self.updateItemPositions()

    def getFrameClass(self) -> type:
        groupType = self.group.groupType
        if groupType == GroupType.Pizzeria:
            return SPGVTLPizzaToonFrame
        return SPGVTLToonFrame


class SPGVTLToonFrame(EasyManagedItem):
    """
    A toon frame for the Social Panel Clubs Members Tab.
    """

    # Height consts
    closeHeight = -0.05
    openHeight = -0.34

    # Button Zpos
    zpos_kick = -0.25691
    zpos_info = -0.12464

    # State icons
    icons = {
        'leader': sp_gui_icons.find('**/star'),
        'invite': sp_gui_icons.find('**/envelope'),
        'ready': sp_gui_icons.find('**/thumbsup_green'),
        'not-here': sp_gui_icons.find('**/thumbsup_grey'),
    }

    def __init__(self, av: Optional[GroupAvatarUDToon], group: GroupClient,
                 detailAvatarList: List[GroupAvatarUDToon], parent=aspect2d, **kw):
        # GUI boilerplate.
        optiondefs = kwargsToOptionDefs(
            relief=DGG.FLAT,
            frameSize=(0, 1.0, -0.5, 0),
            text='',
            openedPanels=None,
            index=0,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)

        # Make clip plane.
        clipPlane = PlaneNode('clippingPlane')
        clipPlane.setPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, self.closeHeight)))
        self.clipNP = self.attachNewNode(clipPlane)
        self.setClipPlane(self.clipNP)

        # GUI elements
        self.button_dropdown = DirectButton(
            parent=self, relief=None,
            pos=(0.44346, 0.0, -0.02553),
            scale=0.042,
            image=(
                sp_gui.find('**/Arrow_N'),
                sp_gui.find('**/Arrow_P'),
                sp_gui.find('**/Arrow_H'),
                sp_gui.find('**/Arrow_D'),
            ),
            image_scale=(30 / 42, 1, 1),
            command=self.onButtonPress,
        )
        self.icon_status = DirectButton(
            parent=self, relief=None,
            pos=(0.0291, 0.0, -0.02587), scale=0.04322,
            frameSize=(-0.5, 0.5, -0.5, 0.5),
        )
        self.rollover_text = OnscreenText(
            parent=aspect2d, text='', scale=0.05,
            fg=(1, 1, 1, 1), bg=(0, 0, 0, 0.6),
            shadow=(0, 0, 0, 1), wordwrap=10,
        )
        self.rollover_text.hide()
        self.rollover_text.setBin('sorted-gui-popup', GuiBinGlobals.HoverTextBin+10)

        # Options time
        self.initialiseoptions(SPGVTLToonFrame)

        # GUI state
        self.av = av  # type: Optional[GroupAvatarUDToon]
        self.group = group  # type: GroupClient
        self.detailAvatarList = detailAvatarList  # type: List[GroupAvatarUDToon]
        self.menuOpen = False
        self.moveSeq = None
        self.cleanedUp = False
        self.generatedInfo = False
        self.easyHeight = self.closeHeight

        # Force open if we are open.
        self.attemptReopen()

        # Event hooks
        self.accept('groupMemberOpened', self.groupMemberOpened)

        # Now set to the toon.
        if av is not None:
            self.button_kickToon = EasyManagedButton(
                parent=self, relief=None,
                pos=(0.41703, 0.0, self.zpos_kick),
                scale=0.0853,
                image=(
                    sp_gui.find('**/Foot_N'),
                    sp_gui.find('**/Foot_P'),
                    sp_gui.find('**/Foot_H'),
                ),
                image_scale=(64 / 58, 1, 1),
                text=('', 'Kick Toon', 'Kick Toon', ''),
                text_fg=(1, 1, 1, 1),
                text_shadow=(0, 0, 0, 1),
                text_bg=(0, 0, 0, 0.7),
                text_pos=(-0.77601, -0.15244),
                text_scale=0.5,
                text_align=TextNode.ARight,
                command=self.openKick,
            )
            self.button_kickToon.setBin('sorted-gui-popup', GuiBinGlobals.HoverTextBin + 10)
            if av and group and (base.localAvatar.doId != group.owner or av.avId == base.localAvatar.doId):
                self.button_kickToon['state'] = DGG.DISABLED
                self.button_kickToon['image_color'] = (0.3, 0.3, 0.3, 1.0)
            self.button_checkId = EasyManagedButton(
                parent=self, relief=None,
                pos=(0.41703, 0.0, self.zpos_info),
                scale=0.0853,
                image=(
                    sp_gui.find('**/ID_N'),
                    sp_gui.find('**/ID_P'),
                    sp_gui.find('**/ID_H'),
                ),
                image_scale=(64 / 58, 1, 1),
                text=('', 'Open Profile', 'Open Profile', ''),
                text_fg=(1, 1, 1, 1),
                text_shadow=(0, 0, 0, 1),
                text_bg=(0, 0, 0, 0.7),
                text_pos=(-0.77601, -0.15244),
                text_scale=0.5,
                text_align=TextNode.ARight,
                command=self.openProfile,
            )
            self.button_checkId.setBin('sorted-gui-popup', GuiBinGlobals.HoverTextBin + 10)
            if (not av or not group) or not group.getGroupAvatar(base.localAvatar.doId):
                self.button_checkId['state'] = DGG.DISABLED
                self.button_checkId['image_color'] = (0.3, 0.3, 0.3, 1.0)
            self['easyScrolledFrame'].bindToScroll(self.button_kickToon)
            self['easyScrolledFrame'].bindToScroll(self.button_checkId)
            self.setToAv(av)
        else:
            self.setToClear()

    """
    Loading methods
    """

    def destroy(self):
        self.cleanupContextMenu()
        self.cleanedUp = True
        if self.moveSeq:
            self.moveSeq.finish()
            self.moveSeq = None
        self.clipNP = None
        self.rollover_text.destroy()
        self.rollover_text = None
        del self.group
        del self.detailAvatarList
        super().destroy()

    def cleanupContextMenu(self):
        if self.cleanedUp:
            return
        self['easyScrolledFrame'].cleanupContextMenu()

    def bindToScroll(self, easyScrolledFrame):
        easyScrolledFrame.bindToScroll(self.button_dropdown)
        easyScrolledFrame.bindToScroll(self.icon_status)
        super().bindToScroll(easyScrolledFrame)

    def attemptReopen(self):
        """When the group panel refreshes, we need to reopen any closed avs."""
        openedPanels = self['openedPanels']
        if None not in (openedPanels, self.av):
            if self.av.avId in openedPanels:
                self.onButtonPress()
                if self.moveSeq:
                    self.moveSeq.finish()

    """
    GUI maker
    """

    def setToAv(self, av: GroupAvatarUDToon):
        """
        Set the attributes of this frame to match to an avatar.
        """
        index = self['index']

        # How much HP does this av have?
        syncType = GroupTypeToGTSDef.getSyncType(self.group.getGroupCreation())
        csDef = ContentSyncDefinitions.getDefinition(syncType) if syncType else None
        laff = av.getHp()
        if csDef:
            laff = csDef.getConstrainedLaff(hp=av.getHp())

        # Set text.
        self.processSetText(av.name, f' ({laff})')
        self['text_fg'] = (0, 0, 0, 1)
        self['text_scale'] = 0.032
        self['text_pos'] = (0.058, -0.036)
        self['text_align'] = TextNode.ALeft

        # Set frame.
        self['frameColor'] = (0.537, 0.757, 0.525, 1.0) if index % 2 else (0.431, 0.655, 0.42, 1.0)

        # Set extra properties.
        self.setStatusImage()

    def setToClear(self):
        """
        Set the attributes of this frame to be empty.
        """
        index = self['index']

        # Set text.
        self.setText(waitingForToon)
        self['text_fg'] = (0.149, 0.282, 0.125, 1.0)
        self['text_scale'] = 0.032
        self['text_pos'] = (0.011, -0.036)
        self['text_align'] = TextNode.ALeft

        # Set frame.
        self['frameColor'] = (0.478, 0.624, 0.459, 1.0) if index % 2 else (0.388, 0.529, 0.369, 1.0)

        # Hide dropdown button.
        self.button_dropdown.hide()

    def setStatusImage(self):
        """
        Sets the status image.
        """
        # Get some constants.
        toon = self.av
        groupOwner = self.group.owner
        groupAv = self.group.getGroupAvatar(toon.avId)
        detailedOwner: Optional[GroupAvatarUDToon] = None
        for detailedAv in self.detailAvatarList:
            if detailedAv.avId == groupOwner:
                detailedOwner = detailedAv
                break
        if not detailedOwner:
            return

        # Figure out which icon we'll be using.
        iconString = 'not-here'
        if self.av.avId == groupOwner:
            iconString = 'leader'
        elif groupAv.reserved:
            iconString = 'invite'
        elif toon.zoneId == detailedOwner.zoneId and toon.districtId == detailedOwner.districtId:
            iconString = 'ready'
        icon = self.icons[iconString]

        # Now set the icon.
        self.icon_status['image'] = icon

        # Let's also set the rollover text now too.
        def onEnter(gui, iconStr, toonName, avId, *_):
            if not self.rollover_text:
                return
            self.rollover_text.show()
            x, _, y = gui.getPos(aspect2d)
            self.rollover_text.setPos(x, y - 0.15)
            if avId != base.localAvatar.doId:
                self.rollover_text.setText(
                    TTLocalizer.GroupRolloverDialogue.get(iconStr) % toonName
                )
            else:
                self.rollover_text.setText(
                    TTLocalizer.GroupRolloverLocalDialogue.get(iconStr)
                )

        def onExit(*_):
            if not self.rollover_text:
                return
            self.rollover_text.hide()
        self.icon_status.bind(DirectGuiGlobals.ENTER, onEnter, extraArgs=[self.icon_status, iconString, toon.name, toon.avId])
        self.icon_status.bind(DirectGuiGlobals.EXIT,  onExit, extraArgs=[])

    def setExtraInfo(self):
        """
        Sets the extra GUI for this avatar.
        The default will be to show their Gags.
        """
        # Figure out max level.
        syncType = GroupTypeToGTSDef.getSyncType(self.group.getGroupCreation())
        csDef = ContentSyncDefinitions.getDefinition(syncType) if syncType else None
        maxLevel = BattleGlobals.LAST_REGULAR_GAG_LEVEL if not csDef else csDef.getMaxGagLevel()

        # Create frame and elements.
        frame = DirectFrame(
            parent=self,
            pos=(0.18881, 0.0, -0.1311),
            scale=1.52837,
        )
        # GUITemplateSliders(frame, 'pos', 'scale')
        widgets = []
        for track in BattleGlobals.GAG_TRACK_ORDER:
            w = TrackWidget(
                parent=frame,
                scale=0.10,
                track=track,
                level=min(self.av.gagLevels[track] - 1, maxLevel),
                prestige=bool(self.av.gagPrestiges[track] != -1),
            )
            w.bindToScroll(self['easyScrolledFrame'])
            widgets.append(w)
        UiHelpers.fillGridWithElements(
            initialGuiList=widgets,
            horizontalCount=4, verticalCount=2,
            startPos=(0, 0, 0),
            centering=True,
            scale=0.10,
        )

    def processSetText(self, prefix, suffix, maxWidth: float = 8.0):
        # Set the text.
        self.setText(prefix)

        # Now shrink the text.
        textNode = self.component('text0').textNode
        if textNode.getWidth() > maxWidth and self.av:
            while textNode.getWidth() > maxWidth and len(self['text']) > 10:
                text = self['text']
                self.setText(text[:-1])
            text = self['text']
            while text and text[-1] == ' ':
                text = text[:-1]
            self.setText(text + '...')

        # Now add the prefix.
        self.setText(self['text'] + suffix)

    """
    Button actions
    """

    def openProfile(self):
        messenger.send('clickedNametag', [FriendHandle(self.av.avId, self.av.name, None)])

    def openKick(self):
        self.cleanupContextMenu()
        self['easyScrolledFrame'].contextMenu = SocialPanelContextDropdown(
            parent=self,
            labelText=self.getKickLabelText(),
            survive=1
        )

        self['easyScrolledFrame'].contextMenu.addButton(text='Yes', callback=self.performKick, red=False)
        self['easyScrolledFrame'].contextMenu.addButton(text='No', callback=lambda: 0, red=True)

    def performKick(self):
        base.cr.groupManager.kickPlayer(self.av.avId)

    """
    Text Getters
    """

    def getKickLabelText(self):
        return 'Kick from Group?'

    """
    Move sequence
    """

    def onButtonPress(self):
        if self.moveSeq:
            self.moveSeq.pause()
            self.moveSeq = None
        self.menuOpen = not self.menuOpen
        if self.menuOpen:
            messenger.send('groupMemberOpened', [self])
            self.doOpenSequence()
            if not self.generatedInfo:
                self.generatedInfo = True
                self.setExtraInfo()
        else:
            self.doCloseSequence()

    def groupMemberOpened(self, memberOpening):
        if self is not memberOpening and self.menuOpen:
            self.onButtonPress()

    def doOpenSequence(self):
        self.moveSeq = Sequence(
            LerpFunctionInterval(self.moveClipPlane, duration=0.2, blendType='easeOut',
                                 fromData=0, toData=1,)
        )
        self.moveSeq.start()

    def doCloseSequence(self):
        self.moveSeq = Sequence(
            LerpFunctionInterval(self.moveClipPlane, duration=0.2, blendType='easeOut',
                                 fromData=1, toData=0, )
        )
        self.moveSeq.start()
        if settings['reduce-gui-movement']:
            self.moveSeq.finish()

    def moveClipPlane(self, t):
        if not self or self.cleanedUp:
            return
        startPos = self.closeHeight
        endPos = self.openHeight
        currPos = startPos + ((endPos - startPos) * t)
        self.easyHeight = currPos
        self.clipNP.setPos(0, 0, currPos - startPos)
        self.button_dropdown.setHpr(0, 0, t * 90)
        messenger.send('spgvtl-updatePositions')

    def getEasyHeight(self) -> float:
        return self.easyHeight


class SPGVTLPizzaToonFrame(SPGVTLToonFrame):
    """
    A toon frame for the Social Panel Clubs Members Tab.
    For pizzeria groups!
    """

    openHeight = -0.235
    zpos_kick = -0.18048
    zpos_info = -0.09525

    icons = SPGVTLToonFrame.icons.copy()
    icons['ready'] = sp_gui_icons.find('**/thumbsup_pizza')

    def __init__(self, av: Optional[GroupAvatarUDToon], group: GroupClient,
                 detailAvatarList: List[GroupAvatarUDToon], parent=aspect2d, **kw):
        # GUI boilerplate.
        optiondefs = kwargsToOptionDefs()
        self.defineoptions(kw, optiondefs)
        super().__init__(av, group, detailAvatarList, parent, **kw)
        self.initialiseoptions(SPGVTLPizzaToonFrame)

    def setExtraInfo(self):
        """
        Sets the extra GUI for this avatar.
        The default will be to show their Gags.
        """
        # Look for this Toon.
        av = base.cr.doId2do.get(self.av.avId, None)

        # Yawn . . .
        if av is None:
            # If it is not in the area, give a simple FAILURE message.
            OnscreenTextOutline(
                parent=self,
                text='Toon not found.\n\1TextSmaller\1Pizza analytics only visible\nfor nearby Toons.\2',
                pos=(0.18489, -0.116),
                scale=0.042,
                fg=hexToPCol('FFF9CA'), outline_fg=hexToPCol('8C2528'),
                text_dist=0.0037,
                precision=5,
            )

        # IT'S PIZZA TIME!!
        else:
            # Show rank label.
            OnscreenTextOutline(
                parent=self,
                pos=(0.18489, -0.105),
                scale=0.03645,
                text='\1white\1\5pineapple\5\2PIZZA RANK {rank}\1white\1\5pineapple\5\2'
                     '\n\1SlightSlant\1\1TextSmaller\1{name}\2\2'.format(
                    rank=PizzaRankGlobals.getPizzaRank(av),
                    name=PizzaRankGlobals.getPizzaRankName(av),
                ),
                fg=hexToPCol('FFF9CA'), outline_fg=hexToPCol('8C2528'),
                text_dist=0.0037,
                precision=5,
            )

            # And progress bar.
            currXp = PizzaRankGlobals.getCurrentPizzaXP(av)
            maxXp = PizzaRankGlobals.getMaxPizzaXP(av)
            DirectWaitBar(
                parent=self,
                relief=DGG.SUNKEN, borderWidth=(0.032, 0.032),
                pos=(0.18813, 0.0, -0.11846),
                scale=0.17055,
                frameSize=(-1.0, 0.96473, -0.53556, -0.18754),
                frameColor=hexToPCol('FFF9CA'),
                barColor=hexToPCol('8C2528'),
                value=currXp, range=maxXp,
            )
            labelText = OnscreenTextOutline(
                parent=self,
                pos=(0.18709, -0.19165),
                scale=0.03733,
                text='{currXp} / {maxXp} XP'.format(currXp=currXp, maxXp=maxXp),
                fg=hexToPCol('FFF9CA'), outline_fg=hexToPCol('8C2528'),
                text_dist=0.0037,
                precision=5,
            )
            labelText.setBin('sorted-gui-popup', GuiBinGlobals.HoverTextBin+5)

    def getKickLabelText(self):
        return 'Kick from Pizza?'


if __name__ == "__main__":
    gui = SocialPanelGroupViewerToonsList(
        parent=aspect2d,
        group=GroupClient(
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
        # any kwargs go here
    )
    gui.updateToonData(
        [
            GroupAvatarUDToon(10, 'John', 3740, 0, 100, [5, 5, 5, 5, 5, 5, 5, 5], [-1, -1, -1, -1, -1, -1, -1, -1]),
            GroupAvatarUDToon(10, 'marcus', 3740, 0, 110, [5, 5, 5, 5, 5, 5, 5, 5], [-1, -1, -1, -1, -1, -1, -1, -1]),
            GroupAvatarUDToon(10, 'david', 3740, 0, 120, [5, 5, 5, 5, 5, 5, 5, 5], [-1, -1, -1, -1, -1, -1, -1, -1]),
            GroupAvatarUDToon(10, 'JOHN TWO', 3740, 0, 130, [5, 5, 5, 5, 5, 5, 5, 5], [-1, -1, -1, -1, -1, -1, -1, -1]),
            GroupAvatarUDToon(10, 'mrowm eow', 3740, 0, 140, [5, 5, 5, 5, 5, 5, 5, 5], [-1, -1, -1, -1, -1, -1, -1, -1]),
        ]
    )
    # GUITemplateSliders(
    #     gui,
    #     'pos', 'frameSize', 'scale'
    # )
    base.run()

