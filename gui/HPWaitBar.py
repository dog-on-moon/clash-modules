from direct.directtools.DirectUtil import CLAMP

from toontown.toonbase.PythonUtil import inverseLerp

if __name__ == "__main__":
    from tools.headless.headlessbase import HeadlessStart
    from tools.headless.headlessbase.HeadlessBase import HeadlessBase
    base = HeadlessBase(wantHotkeys=False)
    if __debug__:
        from toontown.utils.DeveloperInjector import startInjector
        startInjector()
    # base.initCR()  # defines base.cr
    # base.startHeadlessShow()

import random

from direct.showbase.DirectObject import DirectObject

from toontown.suit.DistributedSuitBase import DistributedSuitBase
from toontown.toon.DistributedToonBase import DistributedToonBase

from toontown.gui.EasyWaitBar import EasyWaitBar, EasyWBSegment

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
from toontown.toonbase import ToontownGlobals

from toontown.utils.InjectorTarget import InjectorTarget
from toontown.utils import ColorHelper
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase import PythonUtil
from panda3d.core import *

from typing import Optional, Union, List, Dict, Tuple, TYPE_CHECKING
if TYPE_CHECKING:
    from toontown.utils.InjectorHelper import *


class HPWBObject(DirectObject):
    """
    An object whose sole purpose is to serve HPWaitBar.
    Mainly for testing, probably xd
    """

    def __init__(self, hp: int = 0, maxHp: int = 1, updates: bool = False) -> None:
        self.hp = hp
        self.maxHp = maxHp
        self.updates = updates

    def update(self) -> None:
        if not self.updates:
            return
        messenger.send(self.getUpdateMessage())

    def getUpdateMessage(self) -> str:
        return f'update-{id(self)}'

    def setHp(self, hp: int) -> None:
        self.hp = hp
        self.update()

    def setMaxHp(self, maxHp: int) -> None:
        self.maxHp = maxHp
        self.update()

    def getHp(self) -> int:
        return self.hp

    def getMaxHp(self) -> int:
        return self.maxHp


class HPWaitBar(EasyWaitBar):
    """
    A wait bar designed for showing health state in mind.
    Attach to an object with HPWaitBar.setTarget(do)
    """

    COLOR_FULL_HEALTH = ColorHelper.hexToPCol('68FF65')
    COLOR_NONE_HEALTH = ColorHelper.hexToPCol('FF5858')
    COLOR_LOSE_HEALTH = ColorHelper.hexToPCol('ffffff')
    COLOR_GAIN_HEALTH = ColorHelper.hexToPCol('A8FF80')
    COLOR_OVER_HEALTH = ColorHelper.hexToPCol('9758FF')

    HEALTH_RATIO_SPEED = 0.27

    OVER_RATIO = 1.5

    @InjectorTarget
    def __init__(self, parent, **kw):
        # GUI boilerplate.
        optiondefs = TTGui.kwargsToOptionDefs(
            segmentCount=3,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.postInitialized = False
        self.postInitialiseFuncList.append(lambda: setattr(self, 'postInitialized', True))
        self.initialiseoptions(HPWaitBar)

        # HP Bar State
        self.do = None
        self.lastHpRatio = 1.0
        self.lastDeltaRatio = 0.0
        self.delta: int = 0

        # Sequence State
        self._demoSeq: Sequence | None = None
        self._deltaSeq: Sequence | None = None

        # Segment Data
        self.healthSegment: EasyWBSegment | None = None
        self.demoSegment:   EasyWBSegment | None = None
        self.deltaSegment:  EasyWBSegment | None = None

        self._create()
        self.place(instant=True)

    def destroy(self):
        if self._demoSeq:
            self._demoSeq.pause()
            self._demoSeq = None
        if self._deltaSeq:
            self._deltaSeq.pause()
            self._deltaSeq = None
        self.ignoreAll()
        del self.do
        super().destroy()

    def _create(self):
        self.healthSegment = EasyWBSegment(
            ratio=1.0, ratioSpeed=self.HEALTH_RATIO_SPEED,
            color=self.COLOR_FULL_HEALTH,
            relief=DGG.RAISED,
            borderWidth=(0.003, 0.003),
        )
        self.demoSegment   = EasyWBSegment(ratio=0.0, colorSpeed=0, color=(0, 0, 0, 0))
        self.deltaSegment  = EasyWBSegment(ratio=0.0, ratioSpeed=0, color=self.COLOR_LOSE_HEALTH)
        self.setSegments([self.healthSegment, self.demoSegment, self.deltaSegment])
        super()._create()

    def place(self, instant: bool = False):
        if not self.postInitialized:
            return
        if not self.do:
            return

        addressDelta = True

        # Set health segment params.
        hpRatio = self.getHpRatio()
        if hpRatio != self.lastHpRatio:
            self.healthSegment.setRatioSpeed(self.HEALTH_RATIO_SPEED)
            self.healthSegment.setRatio(hpRatio)
            if hpRatio < 1.0:
                targetCol = ColorHelper.lerpPColSmart(
                    self.COLOR_NONE_HEALTH, self.COLOR_FULL_HEALTH, hpRatio
                )
            elif hpRatio < self.OVER_RATIO:
                targetCol = ColorHelper.lerpPColSmart(
                    self.COLOR_FULL_HEALTH, self.COLOR_OVER_HEALTH, CLAMP(inverseLerp(1.0, self.OVER_RATIO, hpRatio), 0.0, 1.0)
                )
            else:
                targetCol = self.COLOR_OVER_HEALTH
            self.healthSegment.setColor(targetCol)

            # If there's a difference, show it.
            if not instant:
                difference = hpRatio - self.lastHpRatio
                if difference:
                    # Kill deltas.
                    if self.delta:
                        self.delta = False
                        addressDelta = False
                        self.deltaSegment.setRatio(0)
                        if self._deltaSeq:
                            self._deltaSeq.pause()
                            self._deltaSeq = None

                    # Adjust demo.
                    self.demoSegment.setRatio(-difference)
                    self.demoSegment.setColor(self.COLOR_LOSE_HEALTH if difference < 0 else self.COLOR_GAIN_HEALTH)

                    if self._demoSeq:
                        self._demoSeq.pause()
                        self._demoSeq = None
                    else:
                        self.lastHpRatio = hpRatio

                    def endDemoSeq():
                        self.lastHpRatio = hpRatio
                        self._demoSeq = None

                    self._demoSeq = Sequence(
                        Wait(1.0),
                        Func(self.healthSegment.setRatioSpeed, 0.0),
                        Parallel(
                            self.demoSegment.makeLerpSequence(
                                waitBar=self,
                                duration=0.30,
                                ratio=0.0,
                            ),
                            # self.healthSegment.makeLerpSequence(
                            #     waitBar=self,
                            #     duration=0.30,
                            #     color=targetCol,
                            # ),
                        ),
                        Func(self.demoSegment.setColor, (0, 0, 0, 0)),
                        Func(self.healthSegment.setRatioSpeed, self.HEALTH_RATIO_SPEED),
                        Func(endDemoSeq),
                    )
                    self._demoSeq.start()
                else:
                    self.lastHpRatio = hpRatio
            else:
                self.healthSegment.setColor(targetCol)
                self.lastHpRatio = hpRatio

        # Show deltas if present.
        deltaRatio = self.getDeltaRatio()
        if deltaRatio != self.lastDeltaRatio and addressDelta:
            if self._demoSeq:
                self._demoSeq.finish()
                self._demoSeq = None
            self.lastDeltaRatio = deltaRatio
            currHealthSpeed = self.healthSegment.getRatioSpeed()
            self.healthSegment.setRatioSpeed(0)
            self.deltaSegment.setRatio(deltaRatio)
            super().place(instant=instant)
            self.healthSegment.setRatioSpeed(currHealthSpeed)

            # Color sequence
            if self._deltaSeq:
                self._deltaSeq.pause()
                self._deltaSeq = None
            baseCol = self.COLOR_LOSE_HEALTH if deltaRatio < 0 else self.COLOR_GAIN_HEALTH
            nextCol = (baseCol[0], baseCol[1], baseCol[2], 0.0)
            self._deltaSeq = self.deltaSegment.makeMultiColorSequence(
                waitBar=self,
                colors=[baseCol, nextCol],
                duration=1.0,
            )
            self._deltaSeq.loop()

        # Set text.
        self.setText(self.getText())

        # Call up to finish segment placing.
        super().place(instant=instant)

    """
    Interface
    """

    def setTarget(self, do, instant: bool = True):
        """
        Sets a target for this HP bar.
        """
        self.ignoreAll()

        # Attach to this DO and setup message.
        self.do = do
        self._setupMessage()

        # Now update values.
        self.place(instant=instant)

    def setDelta(self, delta: int, update: bool = False):
        """
        Sets a delta amount.
        """
        self.delta = delta
        if update:
            self.place()

    """
    Internals
    """

    def _setupMessage(self):
        if isinstance(self.do, DistributedToonBase):
            self.accept(self.do.uniqueName('hpChange'), lambda *_: self.place())
        elif isinstance(self.do, DistributedSuitBase):
            self.accept(f'suitHpChanged-{self.do.doId}', lambda *_: self.place())
        elif isinstance(self.do, HPWBObject):
            self.accept(self.do.getUpdateMessage(), self.place)
        else:
            raise KeyError

    def getText(self) -> str:
        return f'{self.getHp()} / {self.getMaxHp()}'

    """
    Getters
    """

    def getHp(self) -> int:
        if isinstance(self.do, DistributedToonBase):
            return self.do.getHp()
        elif isinstance(self.do, DistributedSuitBase):
            return self.do.getHp()
        elif isinstance(self.do, HPWBObject):
            return self.do.getHp()
        else:
            raise KeyError

    def getMaxHp(self) -> int:
        if isinstance(self.do, DistributedToonBase):
            return self.do.getMaxHp()
        elif isinstance(self.do, DistributedSuitBase):
            return self.do.getMaxHp()
        elif isinstance(self.do, HPWBObject):
            return self.do.getMaxHp()
        else:
            raise KeyError

    def getDelta(self) -> int:
        return self.delta

    def getHpRatio(self) -> float:
        return self.getHp() / self.getMaxHp()

    def getDeltaRatio(self) -> float:
        return self.getDelta() / self.getMaxHp()


if __name__ == "__main__":
    gui = HPWaitBar(
        parent=aspect2d,
        # any kwargs go here
    )

    obj = HPWBObject(
        hp=20, maxHp=30
    )

    gui.setTarget(obj)

    def lmao():
        # obj.setHp(random.randint(0, 100))
        # obj.setMaxHp(random.randint(20, 70))

        obj.setHp(random.randint(0, 30))
        gui.place()

    def based():
        gui.setDelta(random.randint(-10, 10), update=True)

    base.accept('a', lmao)
    base.accept('b', based)

    GUITemplateSliders(
        gui.frame_text,
        'text_pos', 'text_scale',
        # 'range', 'value'
    )
    base.run()
