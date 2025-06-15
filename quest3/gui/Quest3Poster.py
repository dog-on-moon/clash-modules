"""
The module containing the GUI element for QuestPosters.
"""
import math
import random

from panda3d.core import NodePath, Texture
from direct.actor.Actor import Actor
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *

from toontown.gui import TTDialog
from toontown.gui.ChatBubbleTextFrame import ChatBubbleTextFrame
from toontown.gui.EasyManagedItem import EasyManagedItem
from toontown.gui.TTGui import ExtendedOnscreenText, kwargsToOptionDefs
from toontown.quest3 import QuestLocalizer
from toontown.quest3.QuestEnums import QuestSource
from toontown.quest3.QuestLocalizer import *
from toontown.quest3.base.QuestChain import QuestChain
from toontown.quest3.base.QuestLine import QuestLine
from toontown.quest3.base.QuestObjective import MultiObjective, QuestObjective
from toontown.quest3.base.QuestReference import QuestReference
from toontown.quest3.base.Quester import Quester
from toontown.quest3.rewards import KudosReward
from toontown.suit import BossCog, SuitGlobals
from toontown.suit.Suit import ModelDict, Suit, CustomSkelecogHeads
from toontown.suit.SuitDNA import SuitDNA, getSuitBodyType, getSuitDept
from toontown.toon.gui import GuiBinGlobals
from toontown.toon.npc.NPCToons import NPCToonDict
from toontown.toon.ToonHead import ToonHead
from toontown.toonbase import ToontownGlobals, TTLocalizer, RealmGlobals
from toontown.utils.ColorHelper import hexToPCol
from toontown.utils.InjectorTarget import InjectorTarget
from toontown.utils.text import capTextScaleToWidth
from toontown.toon.OldLaffMeter import OldLaffMeter


class QuestPoster(EasyManagedItem):
    """
    The new QuestPoster GUI for the Quest3 system.
    """

    # Enums for positioning
    LEFT = 0
    CENTER = 1
    RIGHT = 2

    # Positioning globals
    IMAGE_SCALE_LARGE = 0.2
    IMAGE_SCALE_SMALL = 0.15
    POSTER_WIDTH = 0.7
    TEXT_SCALE = TTLocalizer.QPtextScale
    TEXT_WORDWRAP = TTLocalizer.QPtextWordwrap
    AuxillaryTextDefaultPos = (0, 0, 0.09)

    DefaultPosterOffset = (-0.003, 0, 0)
    SourcePosterOffset = {
        QuestSource.Directive: (0, 0, 0),
        QuestSource.KudosQuest: (0, 0, 0),
    }
    DefaultReversePosterOffset = (0.003, 0, 0)
    SourceReversePosterOffset = {
        QuestSource.Directive: (0, 0, 0),
        QuestSource.KudosQuest: (0, 0, 0),
    }

    PosterImageScale = Vec3(0.8, 1.0, 0.58)
    PosterReverseImageScale = Vec3(-0.8, 1.0, 0.58)

    KudosRibbons = {
        1: 'Bronze',
        2: 'Silver',
        3: 'Gold',
        'rank_up': 'RankUp',
    }

    # Color globals
    DefaultTextColor = hexToPCol('4d4033')
    SourceTextColor = {
        QuestSource.ClubQuest: hexToPCol('112a48'),
        QuestSource.Directive: hexToPCol('e6e6e6'),
        QuestSource.DailyQuest: hexToPCol('773134'),
    }
    EventTextColor = hexToPCol('47274d')
    DefaultCompleteTextColor = hexToPCol('004d00')
    SourceCompleteTextColor = {
        QuestSource.Directive: hexToPCol('b3ccb3'),
    }

    DefaultDescriptionCompleteTextColor = hexToPCol('4d4033')
    SourceDescriptionCompleteTextColor = {
        QuestSource.ClubQuest: hexToPCol('112a48'),
        QuestSource.Directive: hexToPCol('e6e6e6'),
        QuestSource.DailyQuest: hexToPCol('004d00'),
    }

    DefaultProgressFrameColor = hexToPCol('d8d5c0')
    SourceProgressFrameColor = {
        QuestSource.MainQuest: hexToPCol('f1d496'),
        QuestSource.ClubQuest: hexToPCol('b5c6e7'),
        QuestSource.Directive: (0.8, 0.8, 0.8, 1.0),
        QuestSource.KudosQuest: (1, 0.95, 0.9, 1.0),
        QuestSource.DailyQuest: hexToPCol('f8c69a'),
    }
    EventProgressFrameColor = hexToPCol('ecb1cd')

    DefaultProgressTextColor = (0.05, 0.14, 0.4, 1)
    SourceProgressTextColor = {
        QuestSource.MainQuest: hexToPCol('4d4033'),
        QuestSource.ClubQuest: hexToPCol('112a48'),
        QuestSource.Directive: hexToPCol('232323'),
        QuestSource.KudosQuest: hexToPCol('4d4033'),
    }

    DefaultRewardHoverColor = hexToPCol('cec6ac')
    SourceRewardHoverColor = {
        QuestSource.MainQuest: hexToPCol('eabc79'),
        QuestSource.ClubQuest: hexToPCol('81abd8'),
        QuestSource.Directive: hexToPCol('6c7782'),
        QuestSource.KudosQuest: hexToPCol('f0ede4'),
        QuestSource.DailyQuest: hexToPCol('fab470'),
    }
    EventRewardHoverColor = hexToPCol('eba3b8')
    DefaultRewardHoverCompleteColor = hexToPCol('a1cd87')
    SourceRewardHoverCompleteColor = {
        QuestSource.Directive: hexToPCol('60857D'),
        QuestSource.KudosQuest: hexToPCol('bcedc4'),
    }

    DefaultTaskColor = hexToPCol('ffffff')
    SourceTaskColor = {
        QuestSource.Directive: hexToPCol('e6e6e6'),
    }
    DefaultCompleteTaskColor = (1, 1, 1, 1)
    SourceCompleteTaskColor = {
        QuestSource.Directive: hexToPCol('c8ffdc'),
        QuestSource.KudosQuest: hexToPCol('c8ffdc'),
    }

    SourceDescriptionTextScale = {
        QuestSource.MainQuest: 0.8,
        QuestSource.SideQuest: 0.8,
        QuestSource.Directive: 0.8,
        QuestSource.KudosQuest: 0.8,
    }

    SourceFrameDescriptionTextScale = {
        QuestSource.Directive: 0.8
    }

    DefaultMinnieFont = ToontownGlobals.getMinnieFont()
    SourceMinnieFont = {
        QuestSource.Directive: ToontownGlobals.getSuitFont(),
    }

    DefaultInterfaceFont = ToontownGlobals.getInterfaceFont()
    SourceInterfaceFont = {
        QuestSource.Directive: ToontownGlobals.getSuitFont(),
    }

    DefaultWaitBarTextScale = 0.19
    SourceWaitBarTextScale = {
        QuestSource.Directive: 0.17
    }

    RewardIcon_Color = (0.741, 0.678, 0.529, 1.0)
    RewardIcon_Color_LastStep = (1, 0.973, 0.435, 1.0)

    colors = {
        'white': (1, 1, 1, 1),
        'lightGrey': (0.9, 0.9, 0.9, 1),
        'darkGrey': (0.35, 0.35, 0.35, 1),
        'blue': (0.45, 0.45, 0.8, 1),
        'lightBlue': (0.42, 0.671, 1.0, 1.0),
        'green': (0.45, 0.8, 0.45, 1),
        'lightGreen': (0.584, 0.85, 0.663, 1),
        'red': (0.8, 0.45, 0.45, 1),
        'rewardRed': (0.8, 0.3, 0.3, 1),
        'managerRed': (0.75, 0.5, 0.5, 1),
        'brightRed': (1.0, 0.16, 0.16, 1.0),
        'brown': (0.52, 0.42, 0.22, 1),
        'orange': (0.9, 0.6, 0.4, 1),
        'yellow': (0.9, 0.9, 0.5, 1),
        'ourple': (0.518, 0.322, 0.686, 1.0),
    }
    confirmDeleteButtonEvent = 'confirmDeleteButtonEvent'

    # Etc
    SNOWMAN_ID = 3015
    SUIT_NPC_IDS = {
        12101: 'judy',
    }

    @InjectorTarget
    def __init__(self, parent, questReference: QuestReference = None, **kw):
        # GUI boilerplate.
        posterModel = loader.loadModel('phase_3.5/models/gui/quests/ttcc_quest_posters')
        optiondefs = kwargsToOptionDefs(
            relief=None,
            image=posterModel.find('**/standard_task_scroll'),
            image_scale=self.PosterImageScale,
            state=DGG.NORMAL,

            # Default easy padding
            easyHeight=-0.65,
            easyWidth=0.8,
            easyPadLeft=-0.02,
            easyPadRight=0.02,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.initialiseoptions(QuestPoster)

        # Define objects of this GUI.
        self.container_questFrame = None
        self.label_headLine = None
        self.label_objective = None
        self.text_questInfo = None
        self.label_mapIndex = None
        self.frame_leftPicture = None
        self.frame_middlePicture = None
        self.frame_rightPicture = None
        self.frame_leftQuestIcon = None
        self.frame_middleQuestIcon = None
        self.frame_rightQuestIcon = None
        self.label_auxillaryText = None
        self.waitbar_questProgress = None
        self.label_debugQuestId = None
        self.label_rewardsHover = None
        self.label_rewardsHoverIcon = None
        self.label_rewardsHoverText = None
        self.label_justForFun = None
        self.label_expireDate = None
        self.button_deleteQuest = None
        self.dialog_confirmDelete = None
        self.button_objectiveLeft = None
        self.button_objectiveRight = None

        # Define our quest reference.
        self.questReference = questReference
        self.objectiveSelected = 0

        # Other quest poster variables.
        self.reversed = False
        self.deleteCallback = None
        self.wantObjectiveArrows = True
        self.mapIndex = None

        self.ignoreRewardHover = False

        # Load elements of this GUI.
        self.load()

        # Start defining some of the visual elements of the quest poster.
        self.setQuestReference(questReference)

        # Cleanup the book model too
        posterModel.removeNode()

    """
    Loading methods
    """

    def load(self):
        """Load all of the gui elements in more detail."""
        # Some stupid GUI to load
        guiItems = loader.loadModel('phase_5.5/models/gui/catalog_gui')
        circle = guiItems.find('**/cover/blue_circle')
        jb = loader.loadModel('phase_5.5/models/estate/jellyBean')
        trashcanGui = loader.loadModel('phase_3/models/gui/trashcan_gui')
        jb.setColor(random.choice([
            (1, 0, 0, 1),
            (0, 1, 0, 1),
            (0, 0, 1, 1),
            (1, 1, 0, 1),
            (1, 0, 1, 1),
            (0, 1, 1, 1)
        ]))
        gui = loader.loadModel('phase_4/models/parties/schtickerbookHostingGUI')
        mapIcon = gui.find('**/startPartyButton_inactive')
        mapIconNP = aspect2d.attachNewNode('iconNP')
        mapIcon.reparentTo(mapIconNP)
        mapIcon.setX((-12.0792 + 0.2) / 30.48)
        mapIcon.setZ((-9.7404 + 1) / 30.48)
        monthAsset = loader.loadModel('phase_4/models/parties/tt_m_gui_sbk_calendar')
        questIcons = loader.loadModel('phase_3.5/models/gui/quests/ttcc_quest_icons')
        glass = questIcons.find('**/magnifyingGlass')
        questIcons.removeNode()

        # We define a quest container for everything to hide in.
        self.container_questFrame = DirectFrame(
            parent=self,
            relief=None
        )

        # Main headline
        self.label_headLine = DirectLabel(
            parent=self.container_questFrame,
            relief=None,
            text='',
            text_font=ToontownGlobals.getMinnieFont(),
            text_fg=self.DefaultTextColor,
            text_scale=0.04,
            text_align=TextNode.ACenter,
            text_wordwrap=24.0,
            textMayChange=1,
            # Pos is modified later, but still sync the default to this
            pos=(0.0215, 0, 0.225)
        )
        self.label_objective = DirectLabel(
            parent=self.container_questFrame,
            relief=None,
            text='',
            text_font=ToontownGlobals.getMinnieFont(),
            text_fg=self.DefaultTextColor,
            text_scale=0.03,
            text_align=TextNode.ACenter,
            text_wordwrap=12.0,
            textMayChange=1,
            pos=(0, 0, 0.195)
        )

        # Detail information about the quest
        self.text_questInfo = ExtendedOnscreenText(
            parent=self.container_questFrame,
            text='',
            fg=self.DefaultTextColor,
            scale=self.TEXT_SCALE,
            align=TextNode.ACenter,
            pos=(0, -0.105)  # position gets set below
        )
        self.label_mapIndex = DirectLabel(
            parent=self.container_questFrame,
            relief=None,
            text=' ',
            text_fg=(1, 1, 1, 1),
            text_scale=0.035,
            text_align=TextNode.ACenter,
            image=mapIconNP,
            image_scale=0.3,
            image_color=(1, 0, 0, 1),
            pos=(0.3, 0, 0.118)
        )
        self.label_mapIndex.hide()  # Hide independently

        self._makeFrames()

        self.label_auxillaryText = DirectLabel(
            parent=self.container_questFrame,
            relief=None,
            text='',
            text_scale=TTLocalizer.QPauxText,
            text_fg=self.DefaultTextColor,
            text_align=TextNode.ACenter,
            textMayChange=1
        )

        self.waitbar_questProgress = DirectWaitBar(
            parent=self.container_questFrame,
            relief=DGG.SUNKEN,
            frameSize=(-0.95, 0.95, -0.1, 0.12),
            borderWidth=(0.025, 0.025),
            scale=0.2,
            frameColor=self.DefaultProgressFrameColor,
            barColor=(0.5, 0.7, 0.5, 1),
            text='0/0',
            text_scale=0.19,
            text_fg=(0.05, 0.14, 0.4, 1),
            text_align=TextNode.ACenter,
            text_pos=(0, -0.04),
            pos=(0, 0, -0.18)
        )

        # Adding a print which is only enabled when the client is in Debug mode
        self.label_debugQuestId = DirectLabel(
            parent=self.container_questFrame,
            relief=None,
            text='Quest ID:',
            text_fg=(1, 1, 1, 1),
            text_shadow=(0, 0, 0, 1),
            text_bg=(0, 0, 0, 0.6),
            text_scale=0.04,
            text_align=TextNode.ACenter,
            text_wordwrap=24.0,
            textMayChange=1,
            pos=(0, 0, -0.26)
        )
        self.label_debugQuestId.setBin('gui-popup', 100)

        # Reward circles for XP, jellybeans

        self.label_rewardsHover = DirectLabel(
            parent=self.container_questFrame, relief=None,
            pos=(-0.11, 0, -0.34), scale=0.18,  # position gets changed in code below
            image=circle,
            image_color=self.DefaultRewardHoverColor,
            text='',
            text_scale=0.3,
            text_pos=(-1.08, 0.92),
            text_fg=(1, 1, 1, 1),
            text_shadow=(0, 0, 0, 1),
        )
        self.label_rewardsHoverIcon = DirectFrame(
            parent=self.label_rewardsHover,
            relief=None,
            image=glass,
            pos=(-1.04, 0, 1.04),
            scale=0.54,
        )

        self.label_rewardsHoverText = ChatBubbleTextFrame(parent=self.label_rewardsHover, scale=0.25, pos=(0.1, 0.2, 0.6))
        self.label_rewardsHoverText.hide()
        self.label_rewardsHoverText.setBin('sorted-gui-popup', GuiBinGlobals.HoverTextBin)

        self.label_rewardsHover['state'] = DGG.NORMAL
        self.label_rewardsHover.bind(DGG.ENTER, lambda _: self.label_rewardsHoverText.show())
        self.label_rewardsHover.bind(DGG.EXIT, lambda _: self.label_rewardsHoverText.hide())

        # Tilted ~~Towers~~ labels
        self.label_justForFun = DirectLabel(
            parent=self.container_questFrame, relief=None,
            text=QuestLocalizer.QP_JustForFun,
            text_fg=(0.0, 0.439, 1.0, 1.0),
            text_shadow=(0, 0, 0, 1),
            pos=(-0.2825, 0, 0.2), scale=0.03
        )
        self.label_expireDate = DirectLabel(
            parent=self.container_questFrame,
            relief=None,
            text=QuestLocalizer.QP_Expire % 0,
            text_fg=(1, 0, 1, 1),
            text_shadow=(0, 0, 0, 0.5),
            pos=(-0.2825, 0, 0.2),
            scale=0.03
        )

        # Buttons
        self.button_deleteQuest = DirectButton(
            parent=self.container_questFrame,
            image=(
                trashcanGui.find('**/TrashCan_CLSD'),
                trashcanGui.find('**/TrashCan_OPEN'),
                trashcanGui.find('**/TrashCan_RLVR')
            ),
            text=(
                '', TTLocalizer.AvatarChoiceDelete, TTLocalizer.AvatarChoiceDelete
            ),
            text_fg=(1, 1, 1, 1),
            text_shadow=(0, 0, 0, 1),
            text_scale=0.18,
            text_pos=(0, -0.12),
            relief=None,
            pos=(0.3, 0, -0.145),
            scale=0.3,
            command=self.onPressedDeleteButton,
        )
        self.button_deleteQuest.hide()
        arrowUp = monthAsset.find('**/month_arrowR_up')
        arrowDown = monthAsset.find('**/month_arrowR_down')
        arrowHover = monthAsset.find('**/month_arrowR_hover')
        self.button_objectiveLeft = DirectButton(
            parent=self.container_questFrame,
            relief=None,
            image=(arrowUp, arrowDown, arrowHover, arrowUp),
            image3_color=Vec4(1, 1, 1, 0.5),
            pos=(-0.3, 0, 0),
            scale=(-0.5, 0.5, 0.5),
            command=self.swapObjective,
            extraArgs=[-1],
        )
        self.button_objectiveRight = DirectButton(
            parent=self.container_questFrame,
            relief=None,
            image=(arrowUp, arrowDown, arrowHover, arrowUp),
            image3_color=Vec4(1, 1, 1, 0.5),
            pos=(0.3, 0, 0),
            scale=0.5,
            command=self.swapObjective,
            extraArgs=[1],
        )

        # Angle these texts because it looks spicy.
        self.label_justForFun.setR(-30)
        self.label_expireDate.setR(-30)

        # Hide all of these extra GUI.
        self.hideExtraGui()

        # Cleanup model
        guiItems.removeNode()
        jb.removeNode()
        trashcanGui.removeNode()
        gui.removeNode()
        mapIcon.removeNode()
        monthAsset.removeNode()

    def destroy(self):
        super().destroy()
        self.ignoreAll()

    def hideExtraGui(self):
        """Hides all auxillary GUI."""
        for gui in (self.frame_leftPicture, self.frame_middlePicture, self.frame_rightPicture,
                    self.waitbar_questProgress, self.label_auxillaryText,
                    self.label_debugQuestId, self.label_justForFun,
                    self.label_rewardsHover, self.label_expireDate,
                    self.button_objectiveLeft, self.button_objectiveRight):
            if not gui.isEmpty():
                gui.hide()

    def bindToScroll(self, easyScrolledFrame):
        easyScrolledFrame.bindToScroll(self)
        for gui in (
            self.container_questFrame, self.label_headLine, self.label_objective,
            self.label_mapIndex, self.frame_leftPicture,
            self.frame_middlePicture, self.frame_rightPicture, self.frame_leftQuestIcon,
            self.frame_middleQuestIcon, self.frame_rightQuestIcon, self.label_auxillaryText,
            self.waitbar_questProgress, self.label_debugQuestId, self.label_rewardsHover,
            self.label_justForFun, self.label_expireDate, self.button_deleteQuest,
            self.dialog_confirmDelete, self.button_objectiveLeft, self.button_objectiveRight,
        ):
            if gui:
                easyScrolledFrame.bindToScroll(gui)

    def _makeFrames(self):
        """Makes the frames."""
        for frame in (self.frame_leftPicture, self.frame_middlePicture, self.frame_rightPicture):
            if frame:
                frame.destroy()
        bookModel = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
        posterModel = loader.loadModel('phase_3.5/models/gui/quests/ttcc_quest_posters')
        self.frame_leftPicture = DirectFrame(
            parent=self.container_questFrame, relief=None,
            pos=(-0.18, 0, 0.10),
            image=bookModel.find('**/questPictureFrame'),
            image_scale=self.IMAGE_SCALE_SMALL,
            text='',
            text_pos=(0, -0.11),
            text_fg=self.DefaultTextColor,
            text_scale=self.TEXT_SCALE,
            text_align=TextNode.ACenter,
            text_wordwrap=11.0,
            textMayChange=1
        )
        self.frame_middlePicture = DirectFrame(
            parent=self.container_questFrame, relief=None,
            pos=(-0.00, 0, 0.10),
            image=bookModel.find('**/questPictureFrame'),
            image_scale=self.IMAGE_SCALE_SMALL,
            text='',
            text_pos=(0, -0.11),
            text_fg=self.DefaultTextColor,
            text_scale=self.TEXT_SCALE,
            text_align=TextNode.ACenter,
            text_wordwrap=12.0,  # are you ABSOLUTELY SURE you want to change this?
            textMayChange=1
        )
        self.frame_rightPicture = DirectFrame(
            parent=self.container_questFrame, relief=None,
            pos=(0.18, 0, 0.10),
            image=bookModel.find('**/questPictureFrame'),
            image_scale=self.IMAGE_SCALE_SMALL,
            text='',
            text_pos=(0, -0.11),
            text_fg=self.DefaultTextColor,
            text_scale=self.TEXT_SCALE,
            text_align=TextNode.ACenter,
            text_wordwrap=11.0,
            textMayChange=1
        )
        self.frame_leftQuestIcon = DirectFrame(
            parent=self.frame_leftPicture,
            relief=None,
            text=' ',
            text_font=ToontownGlobals.getSuitFont(),
            text_pos=(0, -0.03),
            text_fg=self.DefaultTextColor,
            text_scale=0.13,
            text_align=TextNode.ACenter,
            text_wordwrap=13.0,
            textMayChange=1)
        self.frame_leftQuestIcon.setColorOff(-1)
        self.frame_middleQuestIcon = DirectFrame(
            parent=self.frame_middlePicture,
            relief=None,
            text=' ',
            text_font=ToontownGlobals.getSuitFont(),
            text_pos=(0, -0.03),
            text_fg=self.DefaultTextColor,
            text_scale=0.13,
            text_align=TextNode.ACenter,
            text_wordwrap=13.0,
            textMayChange=1)
        self.frame_leftQuestIcon.setColorOff(-1)
        self.frame_rightQuestIcon = DirectFrame(
            parent=self.frame_rightPicture,
            relief=None,
            text=' ',
            text_font=ToontownGlobals.getSuitFont(),
            text_pos=(0, -0.03),
            text_fg=self.DefaultTextColor,
            text_scale=0.13,
            text_align=TextNode.ACenter,
            text_wordwrap=13.0,
            textMayChange=1
        )
        self.frame_rightQuestIcon.setColorOff(-1)
        for frame in (self.frame_leftPicture, self.frame_middlePicture, self.frame_rightPicture):
            frame.hide()
        
        # Reset the task image.
        self['image'].removeNode()
        self['image'] = posterModel.find('**/standard_task_scroll')
        self['image_color'] = self.SourceTaskColor.get(QuestSource.MainQuest, self.DefaultTaskColor)

        posterModel.removeNode()
        bookModel.removeNode()

    """
    Visual handlers
    """

    def setQuestId(self, questId: QuestId = None, resetIndex: bool = True):
        self.setQuestReference(
            questReference=QuestReference(questId=questId) if questId is not None else None,
            resetIndex=resetIndex,
        )

    def setQuestReference(self, questReference: QuestReference = None, resetIndex: bool = True):
        """
        Sets the details of the poster to match a given QuestReference.
        :param questReference: The QuestReference to match.
        :param resetIndex:     Reset the objective selected index.
        :return: None
        """
        self.hideExtraGui()
        self.questReference = questReference

        if resetIndex:
            # Find the first non-completed index.
            self.objectiveSelected = 0
            while questReference:
                if self.objectiveSelected >= self.getObjectiveCount() - 1:
                    break

                # Break if this quest is not completed.
                if not self.isComplete():
                    break

                # Increment until we find it.
                self.objectiveSelected += 1

        # Remake frames.
        self._makeFrames()

        # Initialize simple quest properties.
        self.setQuestPreProperties(self.questReference)

        if self.questReference is None:
            # No quest ref, don't attempt to do anything else, except
            # cleanup things that ABSOLUTELY should not exist w/o questref
            self.setDeleteCallback()
            return

        # Let the objective modify us.
        self.performPosterModification(self.getQuestObjective(), self.questReference)

        # Any properties we set that override poster moficiation.
        self.setQuestPostProperties(self.questReference)

        # Update objective buttons.
        self.updateObjectiveButtonStatus()

        # Show the reward button if rewards exist.
        self.showRewardLabels()

    def overrideQuestComplete(self, questReference: QuestReference = None):
        """
        A helpful method to set a quest poster to look complete, even if it's not.
        """
        questSource = questReference.getQuestSource() if questReference else None
        textColor = self.SourceCompleteTextColor.get(questSource, self.DefaultCompleteTextColor)
        descriptionTextColor = self.SourceDescriptionCompleteTextColor.get(questSource, self.DefaultDescriptionCompleteTextColor)
        taskColor = self.SourceCompleteTaskColor.get(questSource, self.DefaultCompleteTaskColor)
        rewardHoverColor = self.SourceRewardHoverCompleteColor.get(questSource, self.DefaultRewardHoverCompleteColor)

        self.label_headLine['text_fg'] = textColor
        self.label_objective['text_fg'] = textColor
        self.label_auxillaryText['text_fg'] = descriptionTextColor
        self.text_questInfo.setFg(descriptionTextColor)
        for pictureFrame in (self.frame_leftPicture, self.frame_middlePicture, self.frame_rightPicture):
            pictureFrame['text_fg'] = descriptionTextColor
        self['image_color'] = taskColor
        if questSource != QuestSource.KudosQuest:
            self.label_rewardsHover['image_color'] = rewardHoverColor

    def performPosterModification(self, questObjective, questReference):
        """
        Performs poster modification from a quest reference.
        Purpose of this method is to allow poster subclasses to
        decide exactly what should be visible on the poster.
        """
        questObjective.modifyPoster(questReference, self)

    def setQuestPreProperties(self, questReference: QuestReference = None):
        """
        Sets some of the simple GUI on this Poster.
        """
        # Some quest property looks.
        questSource = questReference.getQuestSource() if questReference else None
        eventTask = questReference and questReference.isEventTask()
        minnieFont = self.SourceMinnieFont.get(questSource, self.DefaultMinnieFont)
        normalFont = self.SourceInterfaceFont.get(questSource, self.DefaultInterfaceFont)
        textColor = self.SourceTextColor.get(questSource, self.DefaultTextColor) if not eventTask else self.EventTextColor
        taskColor = self.SourceTaskColor.get(questSource, self.DefaultTaskColor)
        rewardHoverColor = self.SourceRewardHoverColor.get(questSource, self.DefaultRewardHoverColor) if not eventTask else self.EventRewardHoverColor
        descriptionTextColor = self.SourceTextColor.get(questSource, self.DefaultTextColor) if not eventTask else self.EventTextColor
        descriptionTextScale = self.SourceDescriptionTextScale.get(questSource, 0.8)
        frameDescriptionTextScale = self.SourceFrameDescriptionTextScale.get(questSource, 1.0)
        if not self.reversed:
            posterOffset = self.SourcePosterOffset.get(questSource, self.DefaultPosterOffset)
        else:
            posterOffset = self.SourceReversePosterOffset.get(questSource, self.DefaultReversePosterOffset)

        # Overrides if the quest is complete.
        if self.isComplete():
            # The quest is considered complete. Greenify.
            textColor = self.SourceCompleteTextColor.get(questSource, self.DefaultCompleteTextColor)
            descriptionTextColor = self.SourceDescriptionCompleteTextColor.get(questSource, self.DefaultDescriptionCompleteTextColor)
            taskColor = self.SourceCompleteTaskColor.get(questSource, self.DefaultCompleteTaskColor)
            rewardHoverColor = self.SourceRewardHoverCompleteColor.get(questSource, self.DefaultRewardHoverCompleteColor)

        # Source-specific properties.
        if questSource == QuestSource.Directive:
            self.frame_leftPicture.setZ(0.125)
            self.frame_rightPicture.setZ(0.125)

        if questSource == QuestSource.Directive:
            self.label_rewardsHover.setPos(-0.11, 0, -0.34 - 0.035)
            self.button_deleteQuest.setPos(0.303, 0, -0.145 - 0.03)
        elif questSource == QuestSource.KudosQuest:
            self.label_rewardsHover.setPos(-0.12, 0, -0.34 - 0.035)
            self.button_deleteQuest.setPos(0.313, 0, -0.145 - 0.033)
        else:
            if not self.reversed:
                self.label_rewardsHover.setPos(-0.11, 0, -0.34)
                self.button_deleteQuest.setPos(0.3, 0, -0.145)
            else:
                x = 0.015
                self.label_rewardsHover.setPos(-0.11 + x, 0, -0.34)
                self.button_deleteQuest.setPos(0.3 + x, 0, -0.145)

        # Set the task image.
        self['image'].removeNode()
        self['image'] = self._getTaskImage()
        self['image_color'] = taskColor
        if questSource == QuestSource.KudosQuest:
            self['image_scale'] = Vec3(0.8, 1.0, 0.58) * 1.05
        else:
            self['image_scale'] = (0.8, 1.0, 0.58)

        # Reposition the container if reversed.
        self.container_questFrame.setPos((0, 0, 0) if not self.reversed else posterOffset)
        self['image_scale'] = self.PosterImageScale if not self.reversed else self.PosterReverseImageScale

        # Shift for quest sources.
        if questSource == QuestSource.KudosQuest:
            self['image_scale'] = self['image_scale'] * 1.05

        # Set the headline.
        self.label_headLine['text_fg'] = textColor
        self.label_headLine['text_font'] = minnieFont
        # Check for a Kudos XP headline title
        highestKudosXp = self._getHighestKudosXp(questReference)
        if questSource == QuestSource.KudosQuest and highestKudosXp != -1:
            self.label_headLine['text'] = QuestLocalizer.KudosQuestNameBase.format(xpType=QuestLocalizer.KudosQuestPrefixNames.get(highestKudosXp, 'Bronze'))
        else:
            self.label_headLine['text'] = '' if not questReference else getQuestHeadline(questReference, self.objectiveSelected)
        self.fitLabel(self.label_headLine)

        # Set the objective.
        self.label_objective['text_fg'] = textColor
        self.label_objective['text_font'] = minnieFont
        self.label_objective['text'] = '' if not questReference else getQuestObjectiveText(questReference, self.objectiveSelected)
        # self.label_objective.show()
        self.label_objective.hide()

        # Position things based on source.
        titleXOffset = 0.0215 if not self.reversed else -0.0215
        self.label_headLine.setPos(titleXOffset, 0, 0.212)
        if questSource == QuestSource.Directive:
            self.label_headLine.setPos(0, 0, 0.223)
            # self.label_objective.setPos(0, 0, 0.205)
        elif questSource == QuestSource.KudosQuest:
            self.label_headLine.setPos(0, 0, 0.19)
            # self.label_objective.hide()

        self.waitbar_questProgress.setPos(0, 0, -0.18)
        if questSource in (QuestSource.Directive, QuestSource.KudosQuest):
            self.waitbar_questProgress.setPos(0, 0, -0.195)

        # Set the auxillary text.
        self.label_auxillaryText['text_fg'] = descriptionTextColor
        self.label_auxillaryText['text_font'] = normalFont
        self.label_auxillaryText['text_scale'] = TTLocalizer.QPauxText * descriptionTextScale
        self.label_auxillaryText['text'] = '' if not questReference else getQuestAuxillaryText(questReference, self.objectiveSelected)
        self.label_auxillaryText.setPos(*self.AuxillaryTextDefaultPos)
        if questSource == QuestSource.Directive:
            self.label_auxillaryText.setPos(0, 0, 0.12)

        # Set the quest info text.
        self.text_questInfo.setFg(descriptionTextColor)
        self.text_questInfo.setFont(normalFont)
        self.text_questInfo.setScale(self.TEXT_SCALE * descriptionTextScale)
        self.text_questInfo.setTextWithVerticalAlignment('')
        self.text_questInfo.setPos(0, -0.091)
        if questSource == QuestSource.Directive:
            self.text_questInfo.setPos(0, -0.09)
        elif questSource == QuestSource.KudosQuest:
            self.text_questInfo.setPos(0, -0.096)
        self.text_questInfo.setTextWithVerticalAlignment('' if not questReference else getQuestInfoText(questReference, self.objectiveSelected))

        # Position the map index.
        if questSource == QuestSource.Directive:
            self.label_mapIndex.setPos(0.32, 0, 0.224)
        elif questSource == QuestSource.KudosQuest:
            self.label_mapIndex.setPos(0.33243, 0.0, 0.21382)
        else:
            if not self.reversed:
                self.label_mapIndex.setPos(0.3, 0, 0.118)
            else:
                self.label_mapIndex.setPos(0.31, 0, 0.118)

        # Set all the picture frame text data.
        for pictureFrame in (self.frame_leftPicture, self.frame_middlePicture, self.frame_rightPicture):
            pictureFrame['text'] = ''
            pictureFrame['text_fg'] = descriptionTextColor
            pictureFrame['text_font'] = normalFont
            pictureFrame['text_scale'] = 0.0325 * frameDescriptionTextScale
        self.frame_middlePicture['text_scale'] = self.TEXT_SCALE * frameDescriptionTextScale
        self.frame_middlePicture['text_wordwrap'] = 12.0

        # Modify the rewards hover
        self._modifyRewardsHover(questReference)
        # Set the reward hover color.
        if questSource != QuestSource.KudosQuest:
            self.label_rewardsHover['image_color'] = rewardHoverColor

        # Show quest debug label in developer environment.
        if RealmGlobals.getCurrentRealm().isPrivateRealm() and questReference:
            questSource, chainId, objectiveId, subObjectiveId = questReference.getQuestId().toStruct()
            if questSource in (QuestSource.ClubQuest, QuestSource.KudosQuest):
                return
            self.label_debugQuestId.show()
            self.label_debugQuestId['text'] = 'Quest ID: ' \
                                              f'{questSource}/{chainId}/{objectiveId}/{self.objectiveSelected} || {questReference.getProgress()}\nNPC ID: {self.getQuestObjective().getToNpcId()}'

    def setQuestPostProperties(self, questReference: QuestReference):
        """Post-properties to set on quest stuff, more important than when it is set from the quest itself"""
        objective = self.getQuestObjective()
        if self.isComplete():
            # Update the auxillary text to use this dialogue instead.
            if objective.poster_canUpdateAux and objective.npcReturnable:
                self.label_auxillaryText['text'] = AuxillaryText_Complete
            self.label_objective['text'] = QuestObjective_Complete

        # Move the info text down if we're about to overlap.
        questSource = questReference.getQuestSource() if questReference else None
        if questSource not in (QuestSource.KudosQuest, QuestSource.Directive):
            # Get our conditionals.
            roomNeeded = not self.frame_leftPicture.isHidden()
            taskComplete = self.isComplete()
            waitbarHidden = self.waitbar_questProgress.isHidden()
            textBig = self.getMaxFrameLineCounts() >= 2.0
            # if taskComplete or waitbarHidden or textBig:
            if (roomNeeded and taskComplete) or textBig:
                self.text_questInfo.move(y=-0.035)
                if not waitbarHidden:
                    x, y, z = self.waitbar_questProgress.getPos()
                    self.waitbar_questProgress.setPos(x, y, z - 0.015)

    def getMaxFrameLineCounts(self):
        """Gets the max line count off of all of the frame texts."""
        pictureFrames = (self.frame_leftPicture, self.frame_middlePicture, self.frame_rightPicture)
        return max(frame.component('text0').textNode.getHeight() for frame in pictureFrames)

    def _getTaskImage(self):
        # Load models and stuff
        questSource = self.questReference.getQuestSource() if self.questReference else None
        if questSource == QuestSource.Directive:
            return loader.loadModel('phase_3.5/models/gui/directiveCard')
        elif questSource == QuestSource.KudosQuest:
            kudosModel = loader.loadModel('phase_3.5/models/gui/kudos/kudos_board_gui')
            if self.questReference:
                cardIndex = (self.questReference.getChainId() % 4) + 1
            else:
                cardIndex = self.mapIndex if isinstance(self.mapIndex, int) else 1
            paperIndex = {1: 1, 2: 4, 3: 3, 4: 2}.get(cardIndex, 1)
            questCard = kudosModel.find(f"**/Paper{paperIndex}")
            kudosModel.removeNode()
            return questCard
        else:
            posterModel = loader.loadModel('phase_3.5/models/gui/quests/ttcc_quest_posters')
            if self.isComplete() and questSource in (QuestSource.MainQuest, QuestSource.SideQuest, QuestSource.DailyQuest, QuestSource.ClubQuest):
                questCard = posterModel.find('**/complete_task_scroll')
            elif questSource == QuestSource.ClubQuest:
                questCard = posterModel.find('**/side_task_scroll')
            elif questSource == QuestSource.DailyQuest:
                questCard = posterModel.find('**/daily_task_scroll')
            elif questSource == QuestSource.MainQuest:
                questCard = posterModel.find('**/main_task_scroll')
            elif self.questReference and self.questReference.isEventTask():
                questCard = posterModel.find('**/event_task_scroll')
            else:
                questCard = posterModel.find('**/standard_task_scroll')
            posterModel.removeNode()

            return questCard

    def _getHighestKudosXp(self, questReference):
        questSource = questReference.getQuestSource() if questReference else None
        if questSource != QuestSource.KudosQuest:
            return -1

        questChain = self.getQuestChain()
        rewards = questChain.getQuestRewards()
        highestKudosXp = -1
        # Iterate over each reward, checking for highest kudos amount
        for reward in rewards:
            if isinstance(reward, KudosReward):
                highestKudosXp = max(highestKudosXp, reward.getKudos())

        return highestKudosXp

    def _modifyRewardsHover(self, questReference):
        questSource = questReference.getQuestSource() if questReference else None
        # Turn the reward hover into a ribbon if we have a Kudos quest !!
        if questSource == QuestSource.KudosQuest:
            # Get the highest level of kudos xp from this quest.
            highestKudosXp = self._getHighestKudosXp(questReference)
            if highestKudosXp == -1:
                # None of the objectives from this task gave any kudos XP, we can assume its a rank-up.
                ribbonImage = self.KudosRibbons['rank_up']
            else:
                # Yay, we had Funny Kudos XP. We can show the equivalent XP ribbon.
                ribbonImage = self.KudosRibbons.get(highestKudosXp, highestKudosXp)

            kudosGui = loader.loadModel('phase_3.5/models/gui/kudos/kudos_board_gui')
            self.label_rewardsHoverIcon.hide()
            self.label_rewardsHover['image_color'] = (1, 1, 1, 1)
            self.label_rewardsHover['image'] = kudosGui.find(f'**/Kudos_Ribbon_{ribbonImage}')
            self.label_rewardsHover['image_pos'] = (-1.0, 0, 0.95)
            kudosGui.removeNode()
        else:
            guiItems = loader.loadModel('phase_5.5/models/gui/catalog_gui')
            circle = guiItems.find('**/cover/blue_circle')
            self.label_rewardsHover['image'] = circle
            self.label_rewardsHover['image_pos'] = (0, 0, 0)
            self.label_rewardsHoverIcon.show()
            guiItems.removeNode()

    def setChoiceButton(self, command=None) -> None:
        if not hasattr(self, "choiceButton"):
            pos = (0.285, 0, 0.245)
            if self.questReference.getQuestSource() == QuestSource.Directive:
                guiButton = loader.loadModel('phase_3.5/models/gui/directives_gui')
                image = (
                    guiButton.find('**/cogbutton1'),
                    guiButton.find('**/cogbutton3'),
                    guiButton.find('**/cogbutton2')
                )
                imageScale = (0.4, 1, 0.125)
                textPos = (0, -0.015)
                scale = 0.575
                font = ToontownGlobals.getSuitFont()
            else:
                guiButton = loader.loadModel('phase_3/models/gui/quit_button')
                image = (
                    guiButton.find('**/QuitBtn_UP'),
                    guiButton.find('**/QuitBtn_DN'),
                    guiButton.find('**/QuitBtn_RLVR')
                )
                imageScale = (0.7, 1, 1)
                textPos = (0, -0.02)
                scale = 0.65
                font = ToontownGlobals.getInterfaceFont()

                if self.questReference.getQuestSource() == QuestSource.KudosQuest:
                    pos = (0.3, 0.0, 0.25)

            extraKwargs = dict(sortOrder=10) if self.questReference.getQuestSource() == QuestSource.KudosQuest else {}
            self.choiceButton = DirectButton(
                parent=self.container_questFrame,
                relief=None,
                image=image,
                image_scale=imageScale,
                text=TTLocalizer.QuestPageChoose,
                text_scale=0.06,
                text_pos=textPos,
                text_font=font,
                pos=pos,
                scale=scale,
                **extraKwargs,
            )
        
        self.choiceButton["command"] = command
        self.choiceButton["extraArgs"] = [self.questReference.getQuestId().toStruct()]
        if command is None:
            self.choiceButton.hide()
        else:
            self.choiceButton.show()

    def showRewardLabels(self) -> None:
        if self.ignoreRewardHover:
            return

        # Show any bean/exp rewards on the poster.
        questChain = self.getQuestChain()
        questObjective = self.getQuestObjective()

        rewards = questChain.getQuestRewards()
        dynamicRewards = questChain.getDynamicQuestRewards()
        stepRewards = questObjective.getQuestRewards()

        questLength = questChain.getQuestChainLength()
        rewardMultiplier = 1.0 / max(1, questLength)

        # Calculate rewards for full completion.
        uncombinedDynamicRewards = list(dynamicRewards)[:]
        rewardNames = []
        for reward in rewards:
            # Combine with any rewards present in the dynamic rewards.
            thisReward = reward
            for dynamicReward in dynamicRewards:
                # Is this the same type?
                if type(dynamicReward) is not type(thisReward):
                    continue
                # Is this a combinable reward?
                combinedReward = thisReward.attemptCombine(other=dynamicReward, otherMultiplier=rewardMultiplier)
                if not combinedReward:
                    continue
                # This reward has combined.
                # If this is a single-step quest, we avoid redundancy,
                # since this reward is getting merged into the completion rewards.
                if dynamicReward in uncombinedDynamicRewards and questLength == 1:
                    uncombinedDynamicRewards.remove(dynamicReward)
                thisReward = combinedReward
            # Extend the string.
            rewardNames.extend(thisReward.getRewardString())

        # Calculate rewards dynamically assigned per step.
        dynamicRewardNames = []
        for reward in uncombinedDynamicRewards:
            dynamicRewardNames.extend(reward.getRewardString(multiplier=rewardMultiplier))

        # Calculate the rewards presented on this step only.
        stepRewardNames = []
        for reward in stepRewards:
            stepRewardNames.extend(reward.getRewardString())

        # Set up for text.
        text = ''
        self.label_rewardsHover.show()
        isComplete = self.isComplete()

        # Build the rewards text.
        objectiveRewardNames = dynamicRewardNames + stepRewardNames
        if objectiveRewardNames:
            text += '\1deepBlue\1Step Rewards\2\1TextShrink\1'

            # Fill in a step per reward.
            for rewardString in objectiveRewardNames:
                text += '\n' + rewardString

            # Fill the end of the text.
            text += '\2'

        if rewardNames:
            if text:
                text += '\1TextShrink\1\n\n\2'
            text += '\1deepBlue\1Completion Rewards\2\1TextShrink\1'

            # Fill in a step per reward.
            for rewardString in rewardNames:
                text += '\n' + rewardString

            # Fill the end of the text.
            text += '\2'

        if self.canShowSteps(questLength=questLength, isComplete=isComplete):
            # If the quest isn't considered complete, show the steps left and things
            if text:
                text += '\1TextShrink\1\n\n\2'
            stepsLeft = questChain.getStepsLeftFromObjective(questObjective)
            text += f'\1deepBlue\1{stepsLeft} step{"s" if stepsLeft != 1 else ""} left\2'

        # Set the text.
        self.label_rewardsHoverText['text'] = text if text else "No reward"
        self.label_rewardsHoverText.scaleToText()
        bMin, bMax = self.label_rewardsHoverText.component('image0').getTightBounds()
        xScale = self.label_rewardsHoverText.xScale
        xModifier = (1.0 if xScale <= 1.0 else xScale * 0.9)
        xPos = bMin[0] - (1.4 * xModifier)
        zPos = bMin[2] + 1.0
        self.label_rewardsHoverText.setPos(xPos, 0, zPos)

    def canShowSteps(self, questLength, isComplete):
        # Can we show the steps remaining on the poster?
        # This is separated so that the sidequest poster can override.
        return questLength > 1

    """
    Setters
    """

    def setMapIndex(self, i):
        """Sets the map index GUI."""
        self.label_mapIndex.setText(str(i))
        self.label_mapIndex.show()
        self.mapIndex = i

    """
    Getters
    """

    def getObjectiveCount(self):
        """Gets the number of objectives."""
        return len(QuestLine.dereferenceQuestReference(self.questReference, quester=base.localAvatar).getQuestObjectives())

    def getQuestObjectives(self) -> MultiObjective:
        """Returns the quest objectives."""
        return QuestLine.dereferenceQuestReference(self.questReference, quester=base.localAvatar)

    def getQuestObjective(self) -> QuestObjective:
        """
        Gets the current QuestObjective associated with the QuestPoster.
        :return:
        """
        return self.getQuestObjectives().getObjectiveIndex(self.objectiveSelected)
    
    def getQuestChain(self) -> QuestChain:
        """Returns the quest chain."""
        return QuestLine.getQuestChainFromQuestId(self.questReference.getQuestId(), quester=base.localAvatar)

    def isComplete(self):
        if not self.questReference:
            return False
        return self.questReference.isQuestComplete(base.localAvatar, self.objectiveSelected)

    """
    Delete Button
    """

    def setDeleteCallback(self, callback=None):
        self.deleteCallback = callback
        self.button_deleteQuest['state'] = DGG.NORMAL
        if callback is not None:
            self.button_deleteQuest.show()
        else:
            self.button_deleteQuest.hide()

    def onPressedDeleteButton(self):
        self.button_deleteQuest['state'] = DGG.DISABLED
        self.accept(self.confirmDeleteButtonEvent, self.confirmedDeleteButton)
        deleteDialogue = {
            QuestSource.SideQuest: QuestLocalizer.QP_ConfirmSideDelete,
            QuestSource.Directive: QuestLocalizer.QP_SuitConfirmDelete,
            QuestSource.KudosQuest: QuestLocalizer.QP_ConfirmKudosDelete,
        }.get(self.questReference.getQuestSource(), QuestLocalizer.QP_ConfirmDelete)
        self.dialog_confirmDelete = TTDialog.TTGlobalDialog(
            doneEvent = self.confirmDeleteButtonEvent,
            message = deleteDialogue,
            style = TTDialog.YesNo,
            okButtonText = TTLocalizer.AvatarChoiceDelete,
            cancelButtonText = TTLocalizer.AvatarChoiceDeleteCancel,
        )
        self.dialog_confirmDelete.doneStatus = ''
        self.dialog_confirmDelete.show()

    def confirmedDeleteButton(self):
        self.ignore(self.confirmDeleteButtonEvent)
        if self.dialog_confirmDelete.doneStatus == 'ok':
            if self.deleteCallback:
                self.deleteCallback(self.questReference)
        self.button_deleteQuest['state'] = DGG.NORMAL
        self.dialog_confirmDelete.cleanup()
        del self.dialog_confirmDelete

    """
    Objective swapping
    """

    def updateObjectiveButtonStatus(self):
        """Updates the objective buttons."""
        objectiveCount = self.getObjectiveCount()
        if objectiveCount == 1:
            # One objective, hide the buttons
            self.button_objectiveLeft.hide()
            self.button_objectiveRight.hide()
        elif self.wantObjectiveArrows:
            # Show the buttons depending on objective index
            self.button_objectiveLeft.show()
            self.button_objectiveRight.show()
            if self.objectiveSelected == 0:
                self.button_objectiveLeft.hide()
            elif self.objectiveSelected == objectiveCount - 1:
                self.button_objectiveRight.hide()

    def swapObjective(self, direction: int):
        # Moves our objective selected.
        self.objectiveSelected += direction
        self.objectiveSelected = max(0, min(self.objectiveSelected, self.getObjectiveCount() - 1))

        # Update the poster.
        self.setQuestReference(self.questReference, resetIndex=False)

        # Send a call letting the world know.
        messenger.send('objectiveSwapped', [self])

    """
    Visual hooks for quest objectives
    """

    def visual_setNpcFrame(self, positionIndex: int, npcId: int):
        """Sets an NPC Toon Head on one of the picture frames."""
        geomPos = (0, 0, 0)
        geomHpr = (0, 0, 0)
        geomScale = self.IMAGE_SCALE_SMALL

        # Make the geom
        if npcId == self.SNOWMAN_ID:
            geom = loader.loadModel('phase_8/models/props/snowman_steve')
            geom.setDepthWrite(1)
            geom.setDepthTest(1)
            geom.setTwoSided(True)
            geomScale = 0.019
            geomPos = (0, 10, -0.07)
        elif npcId in self.SUIT_NPC_IDS:
            geom = self.createSuitHead(self.SUIT_NPC_IDS[npcId])
        else:
            geom = self.createToonHead(npcId)

        # Position it now.
        frame = self.getFrameFromPositionIndex(positionIndex)
        questIcon = self.getQuestIconFromPositionIndex(positionIndex)

        questIcon['geom'] = geom
        questIcon['geom_pos'] = geomPos
        questIcon['geom_hpr'] = geomHpr
        questIcon['geom_scale'] = geomScale
        frame.show()

    def visual_hideFrame(self, positionIndex: int):
        """Hides the picture frame."""
        frame = self.getFrameFromPositionIndex(positionIndex)
        frame.hide()

    def visual_setFrameText(self, positionIndex: int, text: str, maxRows=2, scaleOverRow=None, scaleOverRowAmount=None):
        """Sets the picture frame text."""
        # If the questObjective is passed in, use it for setting text
        frame = self.getFrameFromPositionIndex(positionIndex)
        frame['text'] = text
        if positionIndex == self.CENTER:
            capTextScaleToWidth(frame, 0.65)
        # Keep shrinking the text scale until it fits on 2 lines
        iterations = 0
        while frame.component('text0').textNode.getNumRows() > maxRows:
            currTextScale = frame['text_scale']
            frame['text_scale'] = (currTextScale[0] * 0.97, currTextScale[1] * 0.97)
            frame['text_wordwrap'] = frame['text_wordwrap'] / 0.97

            # break early if this operation takes too long
            iterations += 1
            if iterations > 60:
                break
        # Shrink text scale once if its over a certain number of rows
        if scaleOverRow is not None and frame.component('text0').textNode.getNumRows() >= scaleOverRow:
            currTextScale = frame['text_scale']
            frame['text_scale'] = (currTextScale[0] * scaleOverRowAmount, currTextScale[1] * scaleOverRowAmount)
            frame['text_wordwrap'] = frame['text_wordwrap'] / scaleOverRowAmount
        frame.show()

    def visual_setFrameColor(self, positionIndex: int, color: str):
        """Sets the picture frame colors."""
        frame = self.getFrameFromPositionIndex(positionIndex)
        frame['image_color'] = self.getColorFromString(color)
        frame.show()

    def visual_setFrameGeom(self, positionIndex: int, geom, scale=None, pos=None, hpr=None):
        """Sets the picture frame geom."""
        frame = self.getFrameFromPositionIndex(positionIndex)
        questIcon = self.getQuestIconFromPositionIndex(positionIndex)
        questIcon['geom'] = geom
        if isinstance(geom, OnscreenImage):
            geom.detachNode()
        questIcon['geom_scale'] = scale or 1.0
        questIcon['geom_pos'] = pos or (0, 10, 0)
        questIcon['geom_hpr'] = hpr or (0, 0, 0)
        frame.show()

    def visual_setFramePackageGeom(self, positionIndex: int):
        """Sets the frame to have the package geom."""
        bookModel = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
        geom = bookModel.find('**/package')
        self.visual_setFrameGeom(positionIndex, geom=geom, scale=0.12)
        bookModel.removeNode()

    def visual_setLaffMeterGeom(self, positionIndex: int, laffRatio: int):
        """Sets the frame to have the Toon's laff meter geom."""
        laffMeter = OldLaffMeter(base.localAvatar.style, base.localAvatar.getHp(), base.localAvatar.getMaxHp(), animated=False)
        laffMeter.adjustFace(laffRatio, base.localAvatar.getMaxHp())
        laffMeter.eyes.hide()
        self.visual_setFrameGeom(positionIndex, geom=laffMeter, scale=0.045)
        laffMeter.removeNode()

    def visual_setFrameQuestionGeom(self, positionIndex: int):
        """Sets the frame to have the question mark geom."""
        questionModel = base.loader.loadModel('phase_3/models/gui/quest_question')
        geom = questionModel.find("**/quest_exclaim")
        self.visual_setFrameGeom(positionIndex, geom=geom, scale=0.12)
        questionModel.removeNode()
    
    def visual_setShtikerBookGeom(self, positionIndex: int) -> None:
        """Sets the frame to have the shtiker book geom."""
        bookModel = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
        geom = bookModel.find('**/BookIcon_CLSD')
        self.visual_setFrameGeom(positionIndex, geom=geom, scale=0.2, pos=(-0.035, 10, 0.035))
        bookModel.removeNode()
    
    def visual_setSnowballGeom(self, positionIndex: int) -> None:
        """Sets the frame to have the snowball geom."""
        snowballModel = loader.loadModel('phase_13/models/events/toonseltown/winter_icons')
        geom = snowballModel.find('**/snowball')
        self.visual_setFrameGeom(positionIndex, geom=geom, scale=0.07)
        snowballModel.removeNode()
    
    def visual_setRaceTrophyGeom(self, positionIndex: int) -> None:
        """Sets the frame to have the racing trophy."""
        geom = loader.loadModel('phase_6/models/gui/racingTrophy')
        self.visual_setFrameGeom(positionIndex, geom=geom, scale=0.015, pos=(0, 10, -0.05))
        geom.removeNode()

    def visual_setGolfTrophyGeom(self, positionIndex: int) -> None:
        """Sets the frame to have the golfing trophy."""
        geom = loader.loadModel('phase_6/models/golf/golfTrophy')
        self.visual_setFrameGeom(positionIndex, geom=geom, scale=0.015, pos=(0, 10, -0.05))
        geom.removeNode()

    def visual_setTrolleyGeom(self, positionIndex: int) -> None:
        """Sets the frame to have the trolley."""
        gui = loader.loadModel('phase_3.5/models/gui/trolleyImage')
        geom = gui.find('**/trolley')
        self.visual_setFrameGeom(positionIndex, geom=geom, scale=0.13)
        gui.removeNode()

    def visual_setSuitHead(self, positionIndex: int, suitType: str, silhouette=False):
        """Gives a suit head for funsies"""
        headGeom = self.createSuitHead(suitName=suitType)
        if silhouette:
            headGeom.setColorScale(0, 0, 0, 1)

        self.visual_setFrameGeom(
            positionIndex=positionIndex,
            geom=headGeom,
            scale=0.15,
        )
    
    def visual_setBossHead(self, positionIndex: int, suitType: str, silhouette=False):
        """Sets the frame to have a boss of the indicated suitType."""
        headGeom = self.createBossHead(suitType)
        if silhouette:
            headGeom.setColorScale(0, 0, 0, 1)

        self.visual_setFrameGeom(
            positionIndex=positionIndex,
            geom=headGeom,
            scale=0.15
        )
    
    def visual_setFacilityGeom(self, positionIndex: int, dept: str):
        """Sets the frame to have a facility icon of the indicated dept."""
        if dept == "l":
            geom = self.createLawbotFacilityElevator()
            scale = 0.15
        else:
            dept2ModelPath = {
                "s": "factoryIcon2",
                "m": "CashBotMint",
                "c": "BossBotKart",
            }
            bookModel = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
            geom = bookModel.find(f'**/{dept2ModelPath[dept]}')
            bookModel.removeNode()
            scale = 0.13
        
        self.visual_setFrameGeom(
            positionIndex=positionIndex,
            geom=geom,
            scale=scale
        )

    def visual_setAuxText(self, auxText: str):
        """Sets the aux text"""
        self.label_auxillaryText.setText(auxText)

    def visual_setAuxTextPosition(self, auxTextPos = (0, 0, 0.09)):
        """Sets the position of the auxillary text.
        :type auxTextPos: tuple
        """
        self.label_auxillaryText.setPos(*auxTextPos)

    def visual_setProgressInfo(self, value: int, range: int, textFormat: str):
        """Sets the progress bar"""
        eventTask = self.questReference and self.questReference.isEventTask()
        self.waitbar_questProgress['value'] = value
        self.waitbar_questProgress['range'] = range
        self.waitbar_questProgress['text'] = textFormat.format(value=value, range=range)
        self.waitbar_questProgress['text_font'] = self.SourceInterfaceFont.get(
            self.questReference.getQuestSource(), self.DefaultInterfaceFont)
        self.waitbar_questProgress['text_scale'] = self.SourceWaitBarTextScale.get(
            self.questReference.getQuestSource(), self.DefaultWaitBarTextScale)
        self.waitbar_questProgress['text_fg'] = self.SourceProgressTextColor.get(
            self.questReference.getQuestSource(), self.DefaultProgressTextColor)
        self.waitbar_questProgress['frameColor'] = self.SourceProgressFrameColor.get(
            self.questReference.getQuestSource(), self.DefaultProgressFrameColor) if not eventTask else self.EventProgressFrameColor
        self.waitbar_questProgress.show()

    def getFrameFromPositionIndex(self, positionIndex: int):
        return {
            self.LEFT:      self.frame_leftPicture,
            self.CENTER:    self.frame_middlePicture,
            self.RIGHT:     self.frame_rightPicture,
        }.get(positionIndex)

    def getQuestIconFromPositionIndex(self, positionIndex: int):
        return {
            self.LEFT:      self.frame_leftQuestIcon,
            self.CENTER:    self.frame_middleQuestIcon,
            self.RIGHT:     self.frame_rightQuestIcon,
        }.get(positionIndex)

    def getColorFromString(self, colorStr: str):
        return self.colors.get(colorStr)

    """
    Geom creators
    """

    @staticmethod
    def createToonHead(npcId):
        geom = ToonHead()
        geom.setupHead(NPCToonDict.get(npcId).getToonDNA(), forGui=1)
        QuestPoster.fitGeometry(geom, fFlip=1)
        return geom

    @staticmethod
    def createSuitHead(suitName, dimension=0.8, rotHeadAdjust=True, fitGeom=True, setH=180, wantSkelecog=False, elite=False):
        head = NodePath('head')

        headParts = SuitGlobals.suitProperties[suitName][SuitGlobals.SKELE_HEADS_INDEX if wantSkelecog else SuitGlobals.HEADS_INDEX]
        for part in headParts:
            part: str
            if suitName in ToontownGlobals.animSuitHeadsPosedNeutral:
                headPart = Actor(part, {'neutral': part.replace("zero", "neutral")})
                headPart.pose('neutral', 5)
            else:
                headPart = loader.loadModel(part)
            headPart.setTwoSided(True)
            headPart.setDepthTest(1)
            headPart.setDepthWrite(1)
            headTexPath = SuitGlobals.suitProperties[suitName][SuitGlobals.SKELE_HEAD_TEXTURE_INDEX if wantSkelecog else SuitGlobals.HEAD_TEXTURE_INDEX]
            if elite and wantSkelecog and suitName not in CustomSkelecogHeads:
                headTexPath = f'**/skel_body_{SuitGlobals.DeptCharToTexShorthand[getSuitDept(suitName)]}_exe'
            if headTexPath:
                if headTexPath.find('**/') != -1:
                    texCard = loader.loadModel('char/suit/models/cc_m_texcard_ene_skel_body_common')
                    headTex = texCard.find(headTexPath).findTexture('*')
                    texCard.removeNode()
                else:
                    headTex = loader.loadTexture(headTexPath)
                headTex.setMinfilter(Texture.FTLinearMipmapLinear)
                headTex.setMagfilter(Texture.FTLinear)
                headPart.setTexture(headTex, 1)
            if suitName in list(ToontownGlobals.rotatedSuitHeads.keys()) and rotHeadAdjust:
                headPart.setH(ToontownGlobals.rotatedSuitHeads[suitName])
            headPart.reparentTo(head)

        if fitGeom:
            QuestPoster.fitGeometry(head, fFlip=1, dimension=dimension, setH=setH)

        return head
    
    @staticmethod
    def createBossHead(dept, dimension = .8):
        headModel = loader.loadModel(BossCog.ModelDict[dept] + '-head-zero')
        headModel.setHpr(90, 0, -90)
        head = hidden.attachNewNode('head')
        copyHead = headModel.copyTo(head)
        copyHead.setDepthTest(1)
        copyHead.setDepthWrite(1)
        QuestPoster.fitGeometry(head, fFlip = 1, dimension=dimension)
        return head
    
    @staticmethod
    def createLawbotFacilityElevator():
        geom = loader.loadModel('phase_11/models/lawbotHQ/lawbotElevator')
        QuestPoster.fitGeometry(geom, fFlip = 0)
        return geom

    """
    Geom positioning
    """

    @staticmethod
    def fitGeometry(geom, fFlip=0, dimension=0.8, setH=180):
        p1 = Point3()
        p2 = Point3()
        geom.calcTightBounds(p1, p2)
        if fFlip:
            t = p1[0]
            p1.setX(-p2[0])
            p2.setX(-t)
        d = p2 - p1
        biggest = max(d[0], d[2])
        s = dimension / biggest
        mid = (p1 + d / 2.0) * s
        geomXform = hidden.attachNewNode('geomXform')
        for child in geom.getChildren():
            child.reparentTo(geomXform)

        geomXform.setPosHprScale(-mid[0], -mid[1] + 1, -mid[2], setH, 0, 0, s, s, s)
        geomXform.reparentTo(geom)

    def fitLabel(self, label, lineNo = 0, preScale = 1):
        text = label['text']
        label['text_scale'] = self.TEXT_SCALE * preScale
        label['text_wordwrap'] = self.TEXT_WORDWRAP
        if len(text) > 0:
            lines = text.split('\n')

            # We pass in the string to textNode.calcWidth, instead of
            # using textNode.getWidth(), because we don't want to
            # consider the wordwrapping in this calculation.
            lineWidth = label.component('text0').textNode.calcWidth(lines[lineNo])
            # Do not divide by zero on an empty line
            if lineWidth > 0:
                textScale = self.POSTER_WIDTH / lineWidth
                label['text_scale'] = min(self.TEXT_SCALE * preScale, textScale)
                label['text_wordwrap'] = max(self.TEXT_WORDWRAP, lineWidth + 0.05)

    """
    Misc
    """

    def reverseBG(self, reverse: int):
        self.reversed = reverse
        self.setQuestReference(self.questReference)
    
    def getProgressInterval(self, updatedQuest: QuestReference, toon: Quester) -> Sequence:
        seq = Sequence()

        # Container for waitbar sequences.
        self.miniSeqs = []

        self.button_objectiveLeft.hide()
        self.button_objectiveRight.hide()
        self.wantObjectiveArrows = False

        resetIndex = self.questReference.getQuestId() != updatedQuest.getQuestId()

        for index, questObjective in enumerate(self.getQuestObjectives().getQuestObjectives()):
            questObjective: QuestObjective

            # Ignore it if it is complete.
            if questObjective.isComplete(self.questReference, index, toon):
                continue

            oldProgress = self.questReference.getQuestProgress(index)

            # Hack for completing multiobjectives.
            # Upon completing one, a different quest will take its place.
            if resetIndex:
                completed = True
                newProgress = questObjective.getCompletionRequirement()
            else:
                completed = updatedQuest.isQuestComplete(toon, index)
                newProgress = updatedQuest.getQuestProgress(index)

            progress = newProgress - oldProgress

            # Ignore if it there was no progress.
            if not progress:
                continue

            if not seq:
                seq.append(Func(self.button_objectiveLeft.hide))
                seq.append(Func(self.button_objectiveRight.hide))

            def setObjectiveSelected(newIndex):
                self.objectiveSelected = newIndex

            seq.append(Func(setObjectiveSelected, index))
            seq.append(Func(self.setQuestReference, self.questReference, resetIndex=False))

            def updateQuest(delta, old, new, questRef, newQuestRef, complete):
                miniSeq = Sequence()
                if not self.waitbar_questProgress.isHidden():
                    tickDelay = 1.0 / 60
                    numTicks = int(math.ceil(0.5 / tickDelay))
                    for i in range(numTicks):
                        t = (i + 1) / float(numTicks)
                        newValue = int(old + t * delta + 0.5)
                        if complete and newValue == new:
                            miniSeq.append(Func(self.setQuestReference, newQuestRef, resetIndex=resetIndex))
                        else:
                            miniSeq.append(Func(self.waitbar_questProgress.setProp, "value", newValue))
                            miniSeq.append(Func(self.waitbar_questProgress.setProp, "text", questObjective.getProgressString(questRef, newValue)))
                        miniSeq.append(Wait(tickDelay))
                elif complete:
                    miniSeq.append(Func(self.setQuestReference, updatedQuest, resetIndex=resetIndex))
                if hasattr(self, "miniSeqs"):
                    miniSeq.start()
                    self.miniSeqs.append(miniSeq)
            
            seq.append(Func(updateQuest, progress, oldProgress, newProgress, self.questReference, updatedQuest, completed))
            seq.append(Wait(1.5))

            def cleanupSeqs():
                # Purge the container for waitbar sequences.
                if getattr(self, "miniSeqs", []):
                    for miniSeq in self.miniSeqs:
                        miniSeq.finish()
                    del self.miniSeqs
            
            seq.append(Func(cleanupSeqs))

        return seq
