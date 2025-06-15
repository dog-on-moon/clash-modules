from toontown.gui.PositionedGUI import PositionedGUI
from toontown.gui.game.GameGUIGlobals import UI_SCALED_SHADOW_ALPHA

if __name__ == "__main__":
    from tools.headless.headlessbase import HeadlessStart
    from tools.headless.headlessbase.HeadlessBase import HeadlessBase
    base = HeadlessBase(wantHotkeys=False)
    if __debug__:
        from toontown.utils.DeveloperInjector import startInjector
        startInjector()
    # base.initCR()  # defines base.cr
    # base.startHeadlessShow()

from toontown.toon.socialpanel.SocialPanel import STATE_FRIENDS, STATE_GROUPS, STATE_CLUBS, STATE_MAIL
from toontown.toon.socialpanel.SocialPanelGlobals import sp_gui
from toontown.toon.socialpanel.groups.SocialPanelGroupSubtext import SocialPanelGroupSubtext

from toontown.gui import TTGui
from toontown.gui.GUITemplateSliders import GUITemplateSliders
from toontown.gui.GUINode import GUINode
from toontown.gui.CornerAnchor import CornerAnchor
from toontown.gui import UiHelpers
from toontown.gui.EasyManagedItem import EasyManagedItem
from toontown.gui.EasyManagedButton import EasyManagedButton
from toontown.gui.EasyScrolledFrame import EasyScrolledFrame
from toontown.gui.Bounds import Bounds
from toontown.gui.GUIPositionGlobals import ScreenCorner
from toontown.gui.ScaledFrame import ScaledFrame
from toontown.toon.gui import GuiBinGlobals
from toontown.toonbase import ToontownGlobals, TTLocalizer

from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.InjectorTarget import InjectorTarget
from toontown.utils import ColorHelper
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase import PythonUtil
from typing import Optional, List, Tuple, Dict, Set, TYPE_CHECKING
if TYPE_CHECKING:
    from toontown.utils.InjectorHelper import *

from toontown.gui.PositionedGUI import OnscreenPositionData


@DirectNotifyCategory()
class SocialPanelButtons(DirectFrame, Bounds, PositionedGUI):
    """
    The buttons to access the Social Panel at the top right of the screen.
    """

    SCREEN_CORNER = ScreenCorner.TOP_RIGHT
    POS_OFFSET = Vec3(-0.045, 0.0, -0.045)
    GUI_BOUNDS = OnscreenPositionData(
        width=4.3,
        height=0.15,
        right=0.6,
        top=0.6,
        left=0.02,
        down=0.6,
    )

    buttonData = {
        STATE_FRIENDS: ('Friends', 'ffffff'),
        STATE_GROUPS: ('Groups', 'ffffff'),
        STATE_CLUBS: ('Club', 'ffffff'),
        # STATE_MAIL: ('Test', 'ffffff'),
    }
    stateList = [
        STATE_FRIENDS, STATE_GROUPS, STATE_CLUBS,
    ]

    @InjectorTarget
    def __init__(self, parent=base.a2dTopRight, **kw):
        # GUI boilerplate.
        optiondefs = TTGui.kwargsToOptionDefs(
            pos=(-0.08, 0.0, 0.0),
            scale=0.11229,
            # relief = None,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.postInitialized = False
        self.postInitialiseFuncList.append(lambda: setattr(self, 'postInitialized', True))
        self.initialiseoptions(SocialPanelButtons)
        self.setBin('sorted-gui-popup', GuiBinGlobals.FriendsListButtonBin)

        # Set GUI prototypes here.
        self.buttons: dict[str, EasyManagedButton] = {}
        self.shadow: ScaledFrame | None = None
        self.groupIcon = None

        # Call these two.
        self._create()
        self.place()

        self.accept('social-panel-opened', self.onOpen)
        self.accept('social-panel-closed', self.onClose)

        self.accept('joinedNewGroup', lambda *_: self.openPanel(STATE_GROUPS))

        self.startPositionManagement()

    def show(self):
        if self.isHidden():
            super().show()
            self.startPositionManagement()

    def hide(self):
        if not self.isHidden():
            super().hide()
            self.stopPositionManagement()

    def _create(self):
        shadowGui = loader.loadModel('phase_3.5/models/gui/socialpanel/ttcc_avatar_panel_shadows')
        for state in self.stateList:
            name, col, *_ = self.buttonData.get(state)
            col = ColorHelper.hexToPCol(col)
            self.buttons[state] = EasyManagedButton(
                parent=self,
                pos=(0, 0, 0), scale=1.8 if state == STATE_FRIENDS else 1.0, relief=None,
                easyWidth=1.25, easyHeight=-1.0,
                # This text is managed by self.groupIcon, unfortunately
                text=('', name, name),
                text_fg=Vec4(1, 1, 1, 1),
                text_shadow=Vec4(0, 0, 0, 1),
                text_pos=(0.0, -0.75),
                text_scale=0.34,
                text_font=ToontownGlobals.getInterfaceFont(),
                image=(sp_gui.find('**/Icon_N'),
                       sp_gui.find('**/Icon_P'),
                       sp_gui.find('**/Icon_H')),
                image_color=col,
                command=self.openPanel, extraArgs=[state],
            )
            friendsListShadow = DirectFrame(
                parent=self.buttons[state],
                relief=None,
                geom=shadowGui.find('**/social_button_shadow'),
                geom_scale=1.24,
            )
            friendsListShadow.setBin('sorted-gui-popup', GuiBinGlobals.FriendsListButtonBin - 1)
            if state != STATE_FRIENDS:
                self.buttons[state].hide()
        shadowGui.removeNode()

        self.groupIcon = SocialPanelGroupSubtext(
            parent=self.buttons[STATE_CLUBS],
            friendsListButtons=self.buttons.values(),
            pos=(0.80759, 0.0, -0.29301),
        )

    def place(self):
        if not self.postInitialized:
            return

        buttons = [self.buttons[state] for state in self.stateList]

    def destroy(self):
        self.ignoreAll()
        del self.buttons
        super().destroy()

    def openPanel(self, tab: str):
        messenger.send('open-social-panel', [tab])
        for button in self.buttons.values():
            self.enableButton(button)
        self.disableButton(self.buttons[tab])

    def closePanel(self, *_):
        messenger.send('close-social-panel')

    def onOpen(self):
        if self.groupIcon:
            self.groupIcon.destroy()
            self.groupIcon = None
        for button in self.buttons.values():
            button['text_fg'] = (1, 1, 1, 0)
            button['text_shadow'] = (0, 0, 0, 0)
        base.localAvatar.refreshOnscreenButtons()

    def onClose(self):
        if not self.groupIcon:
            self.groupIcon = SocialPanelGroupSubtext(
                parent=self.buttons[STATE_CLUBS],
                friendsListButtons=self.buttons.values(),
                pos=(0.80759, 0.0, -0.29301),
            )
        for button in self.buttons.values():
            button['text_fg'] = (1, 1, 1, 1)
            button['text_shadow'] = (0, 0, 0, 1)
            self.enableButton(button)
        base.localAvatar.refreshOnscreenButtons()

    def onscreenPositionBounds(self) -> OnscreenPositionData:
        return self.GUI_BOUNDS

    def enableButton(self, b: DirectButton):
        b['image_color'] = (1.0, 1.0, 1.0, 1.0)
        b['command'] = self.openPanel

    def disableButton(self, b: DirectButton):
        b['image_color'] = (0.7, 0.7, 0.7, 1.0)
        b['command'] = self.closePanel


if __name__ == "__main__":
    gui = SocialPanelButtons(
        # any kwargs go here
    )
    gui.groupIcon.show()
    gui.groupIcon['text'] = 'Swag Group FNAF ROleplay Factory\1TextSmaller\1\nWaiting for You\n7 Not Nearby\n8/8 Toons\2'
    GUITemplateSliders(
        gui.groupIcon,
        'pos', 'scale'
    )
    base.run()
