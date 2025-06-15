from direct.gui.DirectGui import *
from panda3d.core import *
from toontown.quest3.base.QuestReference import QuestReference
from toontown.quest3.gui.Quest3Poster import QuestPoster
from toontown.toonbase import ToontownTimer
from toontown.toonbase import CustomTypeTimer
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals

from toontown.toonbase.MarginManagerCell import ScreenCellFlag
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory


@DirectNotifyCategory()
class QuestChoice(DirectFrame):
    def __init__(self, suit = False):
        self.suit = suit
        if suit:
            gui = loader.loadModel('phase_3.5/models/gui/suit_detail_panel')
            geom = gui.find('**/avatar_panel')
            gui.removeNode()
            geomScale = 0.31
            geomHpr = (0, 0, 0)
            pos = (0.75, 0, 0)
        else:
            geom = DGG.getDefaultDialogGeom()
            geomScale = (1.85, 1, 0.9)
            geomHpr = (0, 0, -90)
            pos = (0.5, 0, 0)
        DirectFrame.__init__(
            self,
            relief = None,
            parent = base.a2dLeftCenter,
            geom = geom,
            geom_scale = geomScale,
            geom_hpr = geomHpr,
            pos = pos
        )
        self.taskTitle = None
        if not suit:
            self.defineoptions({}, (('geom_color', (0.8, 0.6, 0.4, 1), None),))
        self.initialiseoptions(QuestChoice)
        if suit:
            self.taskTitle = DirectLabel(
                parent = self,
                relief = None,
                text_font = ToontownGlobals.getSuitFont(),
                text = TTLocalizer.QuestChoiceGuiDirectives,
                text_scale = 0.12,
                text_fg = (0.65, 0, 0, 1),
                text_shadow = (0, 0, 0, 1)
            )
            self.setTransparency(1)
            guiButton = loader.loadModel('phase_3.5/models/gui/directives_gui')
            images = (
                guiButton.find('**/cogbutton1'),
                guiButton.find('**/cogbutton3'),
                guiButton.find('**/cogbutton2')
            )
            imageScale = (0.4, 1, 0.125)
            textPos = (0, -0.015)
            font = ToontownGlobals.getSuitFont()
        else:
            guiButton = loader.loadModel('phase_3/models/gui/quit_button')
            images = (
                guiButton.find('**/QuitBtn_UP'),
                guiButton.find('**/QuitBtn_DN'),
                guiButton.find('**/QuitBtn_RLVR')
            )
            imageScale = (0.7, 1, 1)
            textPos = (0, -0.02)
            font = ToontownGlobals.getInterfaceFont()
        self.cancelButton = DirectButton(
            parent = self,
            relief = None,
            image = images,
            image_scale = imageScale,
            text = TTLocalizer.QuestChoiceGuiCancel,
            text_scale = 0.06,
            text_pos = textPos,
            text_font = font,
            command = self.chooseQuest,
        )
        guiButton.removeNode()
        self.questChoicePosters = []
        if suit:
            self.timer = CustomTypeTimer.CustomTypeTimer(timerType = CustomTypeTimer.TIMER_TYPE_OVERCLOCKED)
        else:
            self.timer = ToontownTimer.ToontownTimer()
        self.timer.reparentTo(self)
        self.timer.setScale(0.3)
        base.flagScreenCells(ScreenCellFlag.questChoice, base.leftCells + [base.bottomCells[0], base.bottomCells[1]])

    def setQuests(self, quests, timeout):
        # Cap the limit of quests we can choose from.
        quests = quests[:3]

        for questId in quests:
            qp = QuestPoster(self)
            qp.setQuestReference(QuestReference(questId))
            qp.setChoiceButton(self.chooseQuest)
            self.questChoicePosters.append(qp)

        if len(quests) == 1:
            if self.suit:
                self['geom_scale'] = (0.475, 1, 0.35)
                if self.taskTitle:
                    self.taskTitle.setPos(0, 0, 0.5)
                self.cancelButton.setPos(0.15, 0, -0.565)
                self.timer.setPos(-0.2, 0, -0.54)
            else:
                self['geom_scale'] = (1, 1, 0.9)
                self.cancelButton.setPos(0.15, 0, -0.375)
                self.timer.setPos(-0.2, 0, -0.35)
            self.questChoicePosters[0].setPos(0, 0, 0.1)
        elif len(quests) == 2:
            if self.suit:
                self['geom_scale'] = (0.475, 1, 0.4)
            else:
                self['geom_scale'] = (1.5, 1, 0.9)
            self.questChoicePosters[0].setPos(0, 0, -0.2)
            self.questChoicePosters[1].setPos(0, 0, 0.4)
            self.cancelButton.setPos(0.15, 0, -0.625)
            self.timer.setPos(-0.2, 0, -0.6)
        elif len(quests) == 3:
            if self.suit:
                self['geom_scale'] = (0.475, 1, 0.5)
            else:
                self['geom_scale'] = (1.85, 1, 0.9)
            list([x.setScale(0.95) for x in self.questChoicePosters])
            self.questChoicePosters[0].setPos(0, 0, -0.4)
            self.questChoicePosters[1].setPos(0, 0, 0.125)
            self.questChoicePosters[2].setPos(0, 0, 0.65)
            self.cancelButton.setPos(0.15, 0, -0.8)
            self.timer.setPos(-0.2, 0, -0.775)
        self.timer.countdown(timeout, self.timeout)

    def chooseQuest(self, questId=None):
        base.unflagScreenCells(ScreenCellFlag.questChoice, base.leftCells + [base.bottomCells[0], base.bottomCells[1]])
        self.timer.stop()
        messenger.send('chooseQuest', [questId])

    def timeout(self):
        messenger.send('chooseQuest')
