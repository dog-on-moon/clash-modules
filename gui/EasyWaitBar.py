import random

from direct.directtools.DirectUtil import CLAMP

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
from toontown.gui.ScaledFrame import ScaledFrame
from toontown.gui.UiLerper import UILerper
from toontown.toon.gui import GuiBinGlobals
from toontown.toonbase import ToontownGlobals

from toontown.utils.InjectorTarget import InjectorTarget
from toontown.utils import ColorHelper
from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase import PythonUtil
from panda3d.core import *


class EasyWBSegment:
    """
    Holds value data for an EasyWaitBar.

    You can operate on this class separately from the wait bar,
    even configuring various params, and they will become
    visible & update on the main class upon EasyWaitBar.place().
    """

    def __init__(self,
                 ratio: float,
                 color: tuple[float, float, float, float],
                 ratioSpeed: float = 0.27,
                 colorSpeed: float = 0.27,
                 blend: str = 'easeOut',
                 startRatio: float | None = None,
                 relief = DGG.FLAT,
                 borderWidth = (0.01, 0.01)):
        """
        :param ratio: The amount of info to show on the EasyWB.
        :param color: The color of the WB segment.
        :param ratioSpeed: The time (in seconds) to lerp between ratio.
        :param colorSpeed: The time (in seconds) to lerp between colors.
        :param blend: The blending to apply to segment lerping.
        :param startRatio: Override the start ratio.
        :param relief: Panda3d GUI render mode
        :param borderWidth: Panda3d GUI render mode
        """
        self.__ratio = ratio
        self.__color = color
        self.__ratioSpeed = ratioSpeed
        self.__colorSpeed = colorSpeed
        self.__blend = blend
        self.__startRatio = startRatio
        self.__relief = relief
        self.__borderWidth = borderWidth

    """
    Setter Interface
    """

    def setRatio(self, ratio: float):
        self.__ratio = ratio

    def setColor(self, color: tuple[float, float, float, float]):
        self.__color = color

    def setRatioSpeed(self, speed: float):
        self.__ratioSpeed = speed

    def setColorSpeed(self, speed: float):
        self.__colorSpeed = speed

    def setBlend(self, blend: str):
        self.__blend = blend

    def setStartRatio(self, startRatio: float | None):
        self.__startRatio = startRatio

    """
    Sequence Interface
    """

    def makeLerpSequence(self,
                         waitBar: 'EasyWaitBar',
                         duration: float = 1.0,
                         blendType: str = 'easeOut',
                         ratio: float | None = None,
                         color: tuple[float, float, float, float] | None = None,
                         startRatio: float | None = None,
                         startColor: tuple[float, float, float, float] | None = None,
                         smartLerp: bool = True) -> Sequence:
        """
        Creates a sequence to lerp the segment from any param to another.
        """
        assert (ratio is not None) or (color is not None), "why"
        if startRatio is None:
            startRatio = self.getRatio()
        if startColor is None:
            startColor = self.getColor()

        originalRatioSpeed = self.getRatioSpeed()
        originalColorSpeed = self.getColorSpeed()

        if color is not None:
            startColorHsv = ColorHelper.pcolToHsv(startColor)
            endColorHsv = ColorHelper.pcolToHsv(color)

        def lerpFunc(t: float):
            # Update our params.
            if ratio is not None:
                self.setRatio(lerp(startRatio, ratio, t))
            if color is not None:
                if smartLerp:
                    self.setColor(ColorHelper.hsvToPCol(
                        *ColorHelper.lerpColor(
                            startColorHsv, endColorHsv, t
                        ),
                    ))
                else:
                    self.setColor(
                        ColorHelper.lerpColor(
                            startColor, color, t
                        )
                    )

            # Ask the WaitBar to update.
            EasyWaitBar.place(waitBar)

        return Sequence(
            Func(self.setRatioSpeed, 0) if ratio is not None else Wait(0.0),
            Func(self.setColorSpeed, 0) if color is not None else Wait(0.0),
            LerpFunctionInterval(
                lerpFunc, duration=duration, blendType=blendType,
            ),
            Func(self.setRatioSpeed, originalRatioSpeed) if ratio is not None else Wait(0.0),
            Func(self.setColorSpeed, originalColorSpeed) if color is not None else Wait(0.0),
        )

    def makeMultiColorSequence(self,
                               waitBar: 'EasyWaitBar',
                               colors: list[tuple[float, float, float, float]] = None,
                               duration: float = 3.0,
                               blendType: str = 'noBlend',
                               smartLerp: bool = True):
        assert colors, "why"
        self.setColor(colors[0])
        return Sequence(
            *[
                self.makeLerpSequence(waitBar, duration, blendType, color=nextCol, startColor=currCol, smartLerp=smartLerp)
                for currCol, nextCol in zip(colors, colors[1:])
            ],
            self.makeLerpSequence(waitBar, duration, blendType, color=colors[0], startColor=colors[-1], smartLerp=smartLerp)
        )

    """
    Getters
    """

    def getRatio(self) -> float:
        return self.__ratio

    def getColor(self) -> tuple[float, float, float, float]:
        return self.__color

    def getRatioSpeed(self) -> float:
        return self.__ratioSpeed

    def getColorSpeed(self) -> float:
        return self.__colorSpeed

    def getBlend(self) -> str:
        return self.__blend

    def getStartRatio(self) -> float | None:
        return self.__startRatio

    def getRelief(self):
        return self.__relief

    def getBorderWidth(self):
        return self.__borderWidth


class EasyWaitBar(EasyManagedItem):
    """
    A custom variant of DirectWaitBar.
    Supports more intelligent functionality.
    """

    @InjectorTarget
    def __init__(self, parent, **kw):
        # GUI boilerplate.
        optiondefs = TTGui.kwargsToOptionDefs(
            relief=DGG.SUNKEN, borderWidth=(0.01, 0.01),
            frameSize=(-1, 1, -0.08, 0.08),
            frameColor=(0.149, 0.149, 0.149, 1.0),

            segmentCount=1,
            bin=GuiBinGlobals.EasyWaitBarDefault,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.postInitialized = False
        self.postInitialiseFuncList.append(lambda: setattr(self, 'postInitialized', True))
        self.initialiseoptions(EasyWaitBar)
        self.setBin('sorted-gui-popup', self['bin'])

        # WaitBar State
        self._segments: list[EasyWBSegment] = []
        self.__created = False

        # WaitBar Elements
        self._frames: list[DirectFrame] = []
        self.frame_text: DirectFrame | None = None

        self._create()
        self.place()

    def destroy(self):
        del self._segments
        del self._frames
        super().destroy()

    def _create(self):
        if self.__created:
            return
        self.__created = True
        self._frames = [
            DirectFrame(parent=self)
            for _ in range(self.segmentCount)
        ]
        b = self['bin']
        for i, frame in enumerate(self._frames):
            b += 1
            frame.setBin('sorted-gui-popup', b)
            frame.hide()
        self.frame_text = DirectFrame(
            parent=self, relief=None,
            text='',
            text_pos=(0.26543, -0.05086),
            text_scale=0.04318,
            text_align=TextNode.ACenter,
            text_fg=(1, 1, 1, 1),
            text_shadow=(0, 0, 0, 1),
        )
        self.frame_text.setBin('sorted-gui-popup', b + 1)

    def place(self, instant: bool = False):
        if not self.postInitialized:
            return

        # Hide all frames.
        for frame in self._frames:
            frame.hide()

        # Calculate domain of frames.
        left, right, down, up = self.getDefinedBounds()
        hb, vb = self['borderWidth']
        fLeft = left + hb
        fRight = right - hb
        fDown = down + hb
        fUp = up - hb
        fWidth = fRight - fLeft
        fHeight = fUp - fDown
        fHMid = (fRight + fLeft) / 2
        fVMid = (fUp + fDown) / 2

        x = fLeft
        lefts = []
        rights = []
        for segment in self._segments:
            # Placement loop.
            # Calculate constants.
            segmentWidth = segment.getRatio() * fWidth
            if segment.getStartRatio() is not None:
                x = fLeft + (segment.getStartRatio() * fWidth)

            # Get left and right dimensions.
            left = CLAMP(x, fLeft, fRight)
            right = CLAMP(x + segmentWidth, fLeft, fRight)
            lefts.append(min(left, right))
            rights.append(max(left, right))

            # Bars should only ever be going right --
            # if we're dealing with negative ratios, we want future bars
            # to be built on the right of them, rather on where they end.
            if segmentWidth > 0:
                x += segmentWidth

        for frame, segment in zip(self._frames, self._segments):
            # Bizarre placement logic...
            # We grab the lefts and rights in order of what was pre-calculated.
            left = lefts.pop(0)
            right = rights.pop(0)

            # Now, we want to cap the right at this point,
            # if there is an upcoming element that is further left than it is right.
            if lefts:
                right = min(min(lefts), right)

            # Calculate lerp targets.
            targetFrameSize = (min(left, right), max(left, right), fDown, fUp)
            targetColor = segment.getColor()

            # Perform lerps.
            frame.show()
            UILerper.lerpOption(
                frame,
                'frameSize',
                end=targetFrameSize,
                duration=segment.getRatioSpeed(),
                blendType=segment.getBlend(),
                instant=segment.getRatioSpeed() == 0 or frame['frameSize'] is None or instant,
            )
            UILerper.lerpOption(
                frame,
                'frameColor',
                end=targetColor,
                duration=segment.getColorSpeed(),
                blendType=segment.getBlend(),
                instant=segment.getColorSpeed() == 0 or frame['frameColor'] is None or instant,
                lerpMode=UILerper.LerpMode.COLOR
            )

            relief = segment.getRelief()
            if frame['relief'] != relief:
                frame['relief'] = relief
            borderWidth = segment.getBorderWidth()
            if frame['borderWidth'] != borderWidth:
                frame['borderWidth'] = borderWidth

        # Place text.
        self.frame_text['text_pos'] = (
            fHMid - (0.00486 * (fHeight / 0.16)),
            fVMid - (0.0444 * (fHeight / 0.16)),
        )
        self.frame_text['text_scale'] = 0.17 * (fHeight / 0.16)

        # 0.8 - x = -0.0364
        #

    """
    Interface
    """

    def setSegments(self, segments: list[EasyWBSegment]):
        """
        Sets the list of segments on the bar.
        """
        assert len(segments) <= self.segmentCount, "EasyWaitBar must be defined with greater \"segmentCount\" config"

        # Update new ones.
        self._segments = segments

        # Request visual update.
        self.place(instant=True)

    def setText(self, text=None):
        if hasattr(self, 'frame_text'):
            self.frame_text.setText(text)

    """
    Internals
    """

    def setFrameSize(self, fClearFrame = 0):
        super().setFrameSize(fClearFrame)
        self.place(instant=True)

    def segmentUpdated(self):
        """
        A segment will call this when a property is updated.
        """
        self.place()

    """
    Properties
    """

    @property
    def segmentCount(self) -> int:
        return self['segmentCount']


if __name__ == "__main__":
    gui = EasyWaitBar(
        parent=aspect2d,
        segmentCount=4,
        # any kwargs go here
    )
    segments = [
        EasyWBSegment(0.30,  ColorHelper.hexToPCol('58FF90'), blend='easeOut'),
        EasyWBSegment(0.55,  ColorHelper.hexToPCol('6DDFFF'), blend='easeOut'),
        EasyWBSegment(-0.15, ColorHelper.hexToPCol('FF8A99'), blend='easeOut'),
    ]
    gui.setSegments(segments)

    def silly():
        for s in segments:
            s.setRatio(random.randint(-20, 40) / 100)
            s.setColor((random.random(), random.random(), random.random(), 1))
        gui.place()

    base.accept('a', silly)

    segments[-1].makeMultiColorSequence(
        gui, duration=1.0, colors=[
            ColorHelper.hexToPCol('FF8A99'),
            ColorHelper.hexToPCol('58FF90'),
            ColorHelper.hexToPCol('6DDFFF'),
            ColorHelper.hexToPCol('945EFF')
        ],
    ).loop()
    segments[1].makeMultiColorSequence(
        gui, duration=0.7, colors=[
            ColorHelper.hexToPCol('ffffff', a=0),
            ColorHelper.hexToPCol('ffffff'),
        ], blendType='easeIn',
    ).loop()

    # def x(t):
    #     for i, s in enumerate(segments):
    #         s.setRatio((0.2 * t) + (0.1 * i))
    #         s.setColor(((0.7 * t) + (0.1 * i),
    #                     (0.4 * t) + (0.2 * i),
    #                     (0.1 * t) + (0.3 * i), 1))
    #     segments[-1].setRatio((-0.1))
    #     s.setColor(ColorHelper.lerpColor(
    #         ColorHelper.hexToPCol('FF8A99'),
    #         ColorHelper.hexToPCol('2F171A'),
    #         t
    #     ))
    #     gui.place()
    #
    # Sequence(
    #     LerpFunctionInterval(x, 2.0, 0, 1, 'easeInOut'),
    #     LerpFunctionInterval(x, 2.0, 1, 0, 'easeInOut'),
    # ).loop()

    GUITemplateSliders(
        gui,
        'pos', 'scale'
    )
    base.run()
