import math
import time

from direct.interval.FunctionInterval import Func, Wait
from direct.interval.LerpInterval import LerpFunctionInterval
from direct.interval.MetaInterval import Sequence
from panda3d.core import NodePath

from toontown.booster.BoosterBase import BoosterBase
from toontown.gui.EasyManagedItem import EasyManagedItem
from toontown.inventory.enums.ItemEnums import BoosterItemType
from toontown.inventory.registry.ItemTypeRegistry import getItemDefinition
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.gui.TTGui import kwargsToOptionDefs
from toontown.toon.gui import GuiBinGlobals
from toontown.utils.InjectorTarget import InjectorTarget
from toontown.utils.text import formatTimeRemainingIntoString
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from direct.gui.DirectGui import *


@DirectNotifyCategory()
class OnscreenBooster(EasyManagedItem):
    """
    Shows a Gumball on-screen.
    """
    gumballGui = loader.loadModel('phase_3.5/models/gui/boosters')

    durationSwitch = 2.0
    durationHold   = 0.5

    typeToPrefix = {
        BoosterItemType.Merit_Sellbot:  'merit_sell',
        BoosterItemType.Merit_Cashbot:  'merit_cash',
        BoosterItemType.Merit_Lawbot:   'merit_law',
        BoosterItemType.Merit_Bossbot:  'merit_boss',
        BoosterItemType.Merit_Boardbot: 'merit_board',

        BoosterItemType.Fish_Rarity:     'fishing',
        BoosterItemType.Exp_Dept_Global: 'cog',

        BoosterItemType.Exp_Activity_Global: 'jellybean',
        BoosterItemType.Exp_Gags_Global:     'gag_all',
        BoosterItemType.Reward_Boss_Global:  'eyes',
        BoosterItemType.Jellybeans_Global:   'jellybean2',
        BoosterItemType.Jellybeans_Bingo:    'fishing',

        BoosterItemType.Merit_Global: 'merit',

        BoosterItemType.Exp_Activity_Racing:  'racing',
        BoosterItemType.Exp_Activity_Trolley: 'trolley',
        BoosterItemType.Exp_Activity_Golf:    'golf',
        BoosterItemType.Exp_Activity_Fishing: 'fishing',

        BoosterItemType.Exp_Dept_Sellbot:  'sellbot',
        BoosterItemType.Exp_Dept_Cashbot:  'cashbot',
        BoosterItemType.Exp_Dept_Lawbot:   'lawbot',
        BoosterItemType.Exp_Dept_Bossbot:  'bossbot',
        BoosterItemType.Exp_Dept_Boardbot: 'boardbot',

        BoosterItemType.Reward_Boss_Sellbot:  'sellboss',
        BoosterItemType.Reward_Boss_Cashbot:  'cashboss',
        BoosterItemType.Reward_Boss_Lawbot:   'lawboss',
        BoosterItemType.Reward_Boss_Bossbot:  'bossboss',
        BoosterItemType.Reward_Boss_Boardbot: 'boardboss',

        BoosterItemType.Exp_Gags_Power:   'gag_power',
        BoosterItemType.Exp_Gags_Support: 'gag_support',

        BoosterItemType.AllStar: 'mainwashere',
        BoosterItemType.Random:  'random',
    }

    @InjectorTarget
    def __init__(self, parent, boosterType: BoosterItemType = None,
                 boosterInstance: BoosterBase = None, **kw):
        self.booster = boosterType or boosterInstance.getBoostType()
        self.boosterInstance = boosterInstance
        self.notify.debug(f'OnscreenBooster rendering with booster {boosterType}')

        # GUI boilerplate.
        optiondefs = kwargsToOptionDefs(
            relief=None,
            image=self.getBoosterImage(self.booster),
            hoverPositionOffset=None,
            scale=1.0,
            hasRollover=False,
            textCallback=None,

            easyHeight=-0.1,
            easyWidth=0.1,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.initialiseoptions(self.__class__)

        self.hovered = False

        # Add hover text.
        posOffset = list(self.cget('hoverPositionOffset') or (0, 0, 0))
        currentScale = self.cget('scale')
        for i, val in enumerate(posOffset):
            posOffset[i] = val / (currentScale if type(currentScale) not in (tuple, list) else currentScale[i])
        self.hoverText = DirectFrame(
            parent=self, relief=None,
            pos=tuple(posOffset),
            text=':)',
            text_pos=(0.0, -0.7882),
            text_scale=(0.2462, 0.2462),
            text_align=TextNode.ACenter,
            text_fg=(1, 1, 1, 1),
            text_bg=(0, 0, 0, 0.7),
            text_shadow=(0, 0, 0, 1),
            text_wordwrap=11,
        )
        self.hoverText.hide()
        if self.cget('hasRollover'):
            self['state'] = DGG.NORMAL
            for i in range(1):
                self.hoverText.component(f'text{i}').textNode.setBin('sorted-gui-popup')
                self.hoverText.component(f'text{i}').textNode.setDrawOrder(GuiBinGlobals.SocialPanelBin + 1)
            self.setHoverText()
            taskMgr.doMethodLater(1.0, self.setHoverText, self.uniqueName('updateHoverText'))
            self.bind(DGG.ENTER, self.setHoverMode, extraArgs=[True])
            self.bind(DGG.EXIT, self.setHoverMode, extraArgs=[False])

    def destroy(self):
        self.booster = None
        self.boosterInstance = None
        taskMgr.remove(self.uniqueName('updateHoverText'))
        super().destroy()

    """
    Image getters
    """

    @staticmethod
    def getBoosterImage(boosterType: BoosterItemType) -> NodePath:
        """Gets a list of all of the booster images."""
        return OnscreenBooster.gumballGui.find(f'**/{OnscreenBooster.typeToPrefix.get(boosterType)}')

    def getBoosterName(self):
        return getItemDefinition(self.booster).getName(None)

    def getBoosterDesc(self):
        return getItemDefinition(self.booster).getBoostSubtext()

    def getBoosterEndTime(self):
        if not self.boosterInstance:
            return ''
        timeLeft = self.boosterInstance.getTimeLeft()
        if timeLeft > 0:
            return f'{formatTimeRemainingIntoString(timeLeft)}'
        else:
            return f'Expired!'

    def getBoosterType(self) -> BoosterItemType:
        return self.booster

    """
    Hover Text
    """

    def setHoverMode(self, mode: bool, _=None):
        self.hovered = mode
        textCallback = self['textCallback']
        if textCallback is None:
            self.hoverText.show() if mode else self.hoverText.hide()
        else:
            if mode:
                boosterName, boosterDesc, boosterEndStr = self.getBoosterName(), self.getBoosterDesc(), self.getBoosterEndTime()
                textCallback(self, boosterName, boosterDesc, boosterEndStr)
            else:
                textCallback(self, None, None, None)

    def setHoverText(self, task=None, _=None):
        # Updates the hover-over text.
        boosterName, boosterDesc, boosterEndStr = self.getBoosterName(), self.getBoosterDesc(), self.getBoosterEndTime()
        textCallback = self['textCallback']
        if textCallback is None:
            hoverString = f'{boosterName}\n\1TextShrink\1{boosterDesc}\2'
            if boosterEndStr:
                hoverString += f'\1TextSmaller\1\1TextSmaller\1\n\n\2\2\1TextShrink\1{boosterEndStr}\2'
            self.hoverText.setText(hoverString)
        elif self.hovered:
            textCallback(self, boosterName, boosterDesc, boosterEndStr)

        # Restart the task.
        if task is not None:
            task.delayTime = 1.0
            return task.again
