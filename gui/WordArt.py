if __name__ == "__main__":
    from tools.headless.headlessbase import HeadlessStart
    from tools.headless.headlessbase.HeadlessBase import HeadlessBase
    base = HeadlessBase(wantHotkeys=False)
    if __debug__:
        from toontown.utils.DeveloperInjector import startInjector
        startInjector()
    # base.initCR()  # defines base.cr
    # base.startHeadlessShow()

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
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.InjectorTarget import InjectorTarget
from toontown.utils import ColorHelper
from direct.gui.DirectGui import *
from typing import Optional, List, Tuple, Dict, Set, TYPE_CHECKING
from direct.interval.IntervalGlobal import *
if TYPE_CHECKING:
    from toontown.utils.InjectorHelper import *


@DirectNotifyCategory()
class WordArt(DirectFrame, Bounds):
    """
    Use for displaying words super duper well!!!
    """

    @InjectorTarget
    def __init__(self, parent, **kw):
        # GUI boilerplate.
        optiondefs = TTGui.kwargsToOptionDefs(
            pos = (0, 0, 0),
            hpr = (0, 0, 0),
            scale = 1.0,

            text = '',
            textA = (1, 0, 0, 1),
            textB = (0, 1, 0, 1),
            textCount = 100,
            textDist = 0.005,
            textSpeed = 1.0,
            relief = None,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.postInitialized = False
        self.postInitialiseFuncList.append(lambda: setattr(self, 'postInitialized', True))
        self.initialiseoptions(self.__class__)
        self.destroycomponent('text0')

        # Parent components
        self.node_a = GUINode(parent=self)
        self.node_b = GUINode(parent=self.node_a)
        self.node_c = GUINode(parent=self.node_b)
        self.node_d = GUINode(parent=self.node_c)
        self.node_end = GUINode(parent=self.node_d)

        # Critical text positioning (SENSITIVE)
        self.delta = 0
        self.frames = []
        start_y = -(self['textDist'] * self['textCount'] / 2)
        for i in range(self['textCount']):
            frame = DirectFrame(
                parent=self.node_end,
                relief = self['relief'],
                pos=(0, start_y + (self['textDist'] * i), 0),
                text=self['text'],
                # text_fg=ColorHelper.lerpColor(self['textA'], self['textB'], i / self['textCount']),
            )
            self.frames.append(frame)

        # Critical spinning motion
        Parallel(
            Sequence(
                LerpHprInterval(self.node_a, 2.0, (-20, -20, -20), startHpr=(20, 20, 20), blendType='easeInOut'),
                LerpHprInterval(self.node_a, 2.0, (20, 20, 20), blendType='easeInOut'),
            )
        ).loop()
        Parallel(
            Sequence(
                LerpHprInterval(self.node_b, 16.0, (-582, 581, -492), startHpr=(170, 0, 36), blendType='easeInOut'),
                LerpHprInterval(self.node_b, 16.0, (170, 0, 36), blendType='easeInOut'),
            )
        ).loop()
        # Parallel(
        #     Sequence(
        #         LerpPosQuatScaleShearInterval(
        #             nodePath=self.node_c,
        #             duration=4.0,
        #             pos=(0.1, 0.1, 0.1),
        #             startPos=(-0.1, -0.1, -0.1),
        #             hpr=(90, 90, 90),
        #             startHpr=(-90, -90, -90),
        #             shear=128.1,
        #             startShear=-49.1,
        #             scale=0.1,
        #             startScale=2.0,
        #             blendType='easeIn',
        #         )
        #     )
        # ).loop()

        # Perform coloring.
        self.colorize()

    def destroy(self):
        taskMgr.remove(self.uniqueName('uhhhhh'))
        super().destroy()

    def colorize(self, task=None):
        if task is not None:
            self.delta += (self['textSpeed'] * task.time)
        for i, frame in enumerate(self.frames):
            delta = i / self['textCount']
            delta += self.delta
            frame['text_fg'] = ColorHelper.hsvToPCol(delta % 1.0, 1.0, 1.0)

        if task is None:
            taskMgr.add(self.colorize, self.uniqueName('uhhhhh'))
        else:
            task.delayTime = 0.01
            return task.again


if __name__ == "__main__":
    from toontown.utils.text import splitTextByWordwrap
    gui = WordArt(
        parent=aspect2d,
        text='\n'.join(splitTextByWordwrap(
            text="""hi guys:)""",
            wordwrapValue=50.0,
        )),
        scale=0.08,
        text_fg=(1, 1, 1, 1),
        textCount=30 * 5,
        textDist=0.05 / 5,
        textSpeed=1.0,
        # any kwargs go here
    )
    GUITemplateSliders(
        gui,
        'pos', 'scale'
    )
    base.run()
