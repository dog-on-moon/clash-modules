import random

if __name__ == "__main__":
    from tools.headless.headlessbase import HeadlessStart
    from tools.headless.headlessbase.HeadlessBase import HeadlessBase
    base = HeadlessBase(wantHotkeys=False)
    if __debug__:
        from toontown.utils.DeveloperInjector import startInjector
        startInjector()
    # base.initCR()  # defines base.cr
    # base.startHeadlessShow()

from toontown.gui.toon.ToonHeadData import ToonHeadData
from toontown.toon import ToonHead, ToonDNA

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


class ToonHeadGUI(EasyManagedItem):
    """
    A type of Toon Head designed to be placed on GUI elements.
    """

    def __init__(self, parent, **kw):
        # GUI boilerplate.
        optiondefs = TTGui.kwargsToOptionDefs(
            pos = (0, 0, 0),
            scale = 1.0,

            relief = None,
            frameSize=(-0.5, 0.5, -0.5, 0.5),

            headData = [ToonHeadData(), self.checkHeadData],
            headHpr = [(-150, 177, 0), self.place],

            bounce = True,
            bounceRoll = 1.7,
            bounceDur = 6.0,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.postInitialized = False
        self.postInitialiseFuncList.append(lambda: setattr(self, 'postInitialized', True))
        self.initialiseoptions(ToonHeadGUI)  # <-- Update this

        # Set state here.
        self.cachedData: ToonHeadData = self['headData']

        # Toon head nodes.
        self._headNode: GUINode | None = None
        self._headBase: NodePath | None = None
        self._bounceSeq: Sequence | None = None

        # Call these two.
        self._create()
        self.place()

    def _create(self):
        self._headNode = GUINode(parent=self)

        # Create the head.
        self._headBase = self.makeHeadBase()
        self._headBase.reparentTo(self._headNode)

    def checkHeadData(self):
        if not self.postInitialized:
            return
        if self.cachedData != self['headData']:
            self.cachedData = self['headData']
            if self._bounceSeq:
                self._bounceSeq.pause()
                self._bounceSeq = None
            self._headNode.destroy()
            self._create()
            self.place()

    def place(self):
        if not self.postInitialized:
            return

        # Scale head node to fit in frame.
        self._headBase.setPos(0, 0, 0)
        dl = Point3()
        ur = Point3()
        self._headBase.calcTightBounds(dl, ur)
        self._headBase.setPos(-(dl + ur) / 2)
        self._headBase.setY(0)

        l, r, d, u = self.getDefinedBounds()
        self._headNode.setPos((r + l) / 2, 0, (u + d) / 2)
        self._headNode.setScale(min(r - l, u - d) / min(*[l - r for l, r in zip(dl, ur)]))
        self._headNode.setHpr(*self['headHpr'])

        if self['bounce']:
            if not self._bounceSeq:
                def boing(t):
                    self._headNode.setR(((t - 0.5) * 2) * self['bounceRoll'])

                duration = self['bounceDur']
                self._bounceSeq = Sequence(
                    LerpFunctionInterval(
                        boing, duration * 0.25,
                        0.5, 1.0,
                        blendType='easeOut',
                    ),
                    LerpFunctionInterval(
                        boing, duration * 0.50,
                        1.0, 0.0,
                        blendType='easeInOut',
                    ),
                    LerpFunctionInterval(
                        boing, duration * 0.25,
                        0.0, 0.5,
                        blendType='easeIn',
                    )
                )
                self._bounceSeq.loop()
                self._bounceSeq.setT(random.random() * duration)
        else:
            if self._bounceSeq:
                self._bounceSeq.pause()
                self._bounceSeq = None

    def destroy(self):
        if self._bounceSeq:
            self._bounceSeq.pause()
            del self._bounceSeq
        del self.cachedData
        del self._headNode
        del self._headBase
        super().destroy()

    def setFrameSize(self, fClearFrame = 0):
        super().setFrameSize(fClearFrame)
        self.place()

    """
    Toon Head Building
    """

    def makeHeadBase(self) -> ToonHead:
        """
        Creates a base head model for Toons.
        """
        dna = ToonDNA.ToonDNA()
        dna.gender = 'f'
        dna.head = self.headData.getHeadInfo()
        dna.eyelashes = self.headData.getEyelashIndex()
        dna.headColor = LVecBase4f(*self.headData.getHeadColor(), 1)
        dna.earColor = LVecBase4f(*self.headData.getEarColor(), 1)
        dna.eyeColor = self.headData.getEyeColorIndex()
        headModel = ToonHead.ToonHead()
        headModel.setupHead(dna, forGui=ToonHead.GuiTypeEnum.GUI_EYE_FIX)
        return headModel

    def makeHeadBaseAttempt(self) -> NodePath:
        """
        Creates a base head model for Toons.
        This is an attempt to do it outside of ToonHead.
        It failed.
        """
        _headInfo = self.headData.getHeadInfo()
        _type, _height, _muzzle = _headInfo

        # Load the right model.
        assert _type in ToonHead.HeadDict or _headInfo in ToonHead.HeadDict, "Invalid animal"
        model = loader.loadModel(f'phase_3'
                                 f'{ToonHead.HeadDict.get(_type, ToonHead.HeadDict.get(_headInfo))}'
                                 f'{1000}')

        # Some ops...
        self.__cleanupModel(model, self.headData)
        self.__fixEyes(model, self.headData)
        self.__setupEyelashes(model, self.headData)
        self.__setupMuzzles(model, self.headData)
        self.__colorModel(model, self.headData)
        model.flattenStrong()

        # OK, we're good :)
        model.setDepthWrite(1)
        model.setDepthTest(1)
        return model

    @staticmethod
    def __cleanupModel(model: NodePath, data: ToonHeadData):
        _type, _height, _muzzle = data.getHeadInfo()

        # Scrape off all the parts we don't care about.
        if _type != 'd':
            {
                'll': ToonHeadGUI.__fixHeadLongLong,
                'ls': ToonHeadGUI.__fixHeadLongShort,
                'sl': ToonHeadGUI.__fixHeadShortLong,
                'ss': ToonHeadGUI.__fixHeadShortShort,
            }.get(_height + _muzzle)(model, _type)
        else:
            # Dogs are already set up!! WOOT!!!
            # Just kidding. We gotta set up their muzzles manually :/
            dogModelSubnodePaths = ('**/def_head', '**/joint_toHead', '**/__Actor_head')
            for modelPath in dogModelSubnodePaths:
                dogModelSubnode = model.find(modelPath)
                if not dogModelSubnode.isEmpty():
                    loader.loadModel(f'phase_3{ToonHead.DogMuzzleDict[data.getHeadInfo()]}1000').reparentTo(dogModelSubnode)
                    break

    @staticmethod
    def __fixEyes(model: NodePath, data: ToonHeadData):
        # Fix eyes now, copies Actor.drawInFront operations
        if False:
            eyeParts = model.findAllMatches('**/eyes*')
            for part in eyeParts:
                part.setDepthWrite(0)
                part.setDepthTest(0)
            headPart = model.find('**/head-front*')
            headPart.reparentTo(headPart.getParent(), -1)
            eyeParts.reparentTo(headPart)

            pupilParts = model.findAllMatches('**/joint_pupil*')
            if not pupilParts:
                pupilParts = model.findAllMatches('**/def_*_pupil')
            eyePart = model.find('**/eyes*')
            eyePart.reparentTo(eyePart.getParent(), -1)
            pupilParts.reparentTo(eyePart)

        eyes = model.find('**/eyes*')
        if eyes.isEmpty():
            return

        eyes.setColorOff()

        leye = eyes.attachNewNode('leye')
        lmat = Mat4(0.802174, 0.59709, 0, 0,
                    -0.586191, 0.787531, 0.190197,
                    0, 0.113565, -0.152571,
                    0.981746, 0, -0.233634,
                    0.418062, 0.0196875, 1)
        leye.setMat(lmat)

        reye = eyes.attachNewNode('reye')
        rmat = Mat4(0.786788, -0.617224, 0, 0,
                    0.602836, 0.768447, 0.214658,
                    0, -0.132492, -0.16889,
                    0.976689, 0, 0.233634,
                    0.418062, 0.0196875, 1)
        reye.setMat(rmat)

        __lpupil = leye.attachNewNode('lpupil')
        __rpupil = reye.attachNewNode('rpupil')
        lpt = eyes.attachNewNode('')
        rpt = eyes.attachNewNode('')
        lpt.wrtReparentTo(__lpupil)
        rpt.wrtReparentTo(__rpupil)
        if not model.find('**/joint_pupilL*').isEmpty():
            lp = model.find('**/joint_pupilL*')
            rp = model.find('**/joint_pupilR*')
        else:
            lp = model.find('**/def_left_pupil*')
            rp = model.find('**/def_right_pupil*')
        lp.reparentTo(lpt)
        rp.reparentTo(rpt)
        __lpupil.adjustAllPriorities(1)
        __rpupil.adjustAllPriorities(1)
        __lpupil.flattenStrong()
        __rpupil.flattenStrong()

        __eyesOpen = ToonHead.ToonHead.EyesOpen
        __eyesOpen.setMinfilter(Texture.FTLinear)
        __eyesOpen.setMagfilter(Texture.FTLinear)
        eyes.setTexture(__eyesOpen, 1)
        __lpupil.show()
        __rpupil.show()

        eyeColorIndex = data.getEyeColorIndex()
        try:
            eyeColor = ToonDNA.eyeColorsList[eyeColorIndex]
        except Exception:
            eyeColor = ToonDNA.eyeColorsList[0]
        __lpupil.setColorScale(eyeColor)
        __rpupil.setColorScale(eyeColor)

    @staticmethod
    def __setupEyelashes(model: NodePath, data: ToonHeadData):
        _type, _height, _ = data.getHeadInfo()
        _eyelashIndex = data.getEyelashIndex()

        if not _eyelashIndex:
            return

        eyelashModel = loader.loadModel('phase_3' + ToonHead.EyelashDict[_type])
        styleString = ToonDNA.toonEyelashNames[_eyelashIndex]
        openString, closedString = {
            'l': ('-long', '-closed-long'),
            's': ('-short', '-closed-short'),
        }.get(_height)
        __eyelashOpen = eyelashModel.find('**/' + styleString + openString).copyTo(model)
        # __eyelashClosed = eyelashModel.find('**/' + styleString + closedString).copyTo(model)
        if _type == 'f':
            __eyelashOpen.setScale(1.1)
            # __eyelashClosed.setScale(1.1)
        eyelashModel.removeNode()

    @staticmethod
    def __setupMuzzles(model: NodePath, data: ToonHeadData):
        # muzzle = model.find('**/muzzle' if _type == 'd' else '**/muzzle*neutral')
        model.find(f'**/muzzle*surprise').hide()
        model.find(f'**/muzzle*angry').hide()
        model.find(f'**/muzzle*sad').hide()
        model.find(f'**/muzzle*smile').hide()
        model.find(f'**/muzzle*laugh').hide()

    @staticmethod
    def __colorModel(model: NodePath, data: ToonHeadData):
        _type, *_ = data.getHeadInfo()
        headCol = data.getHeadColor()

        parts = model.findAllMatches('**/head*')
        parts.setColor(LVecBase4f(*headCol, 1))

        # color the ears
        if _type not in ('x',):
            parts = model.findAllMatches('**/ear?*')
            parts.setColor(LVecBase4f(*data.getEarColor(), 1))

    @staticmethod
    def __fixHeadLongLong(model, t):
        for part in model.findAllMatches('**/*short*'):
            part.removeNode()

    @staticmethod
    def __fixHeadLongShort(model, t):
        # alligator, duck, kiwi, turkey
        if t not in ('a', 'f', 'k', 'g',):
            model.find('**/ears-short' if t != 'r' else '**/ears-long').removeNode()
        model.find('**/joint_pupilL_short').removeNode()
        model.find('**/joint_pupilR_short').removeNode()
        model.find('**/head-short').removeNode()
        model.find('**/head-front-short').removeNode()
        for part in model.findAllMatches('**/muzzle-short*' if t != 'r' else '**/muzzle-long'):
            part.removeNode()

    @staticmethod
    def __fixHeadShortLong(model, t):
        # alligator, duck, kiwi, turkey
        if t not in ('a', 'f', 'k', 'g',):
            model.find('**/ears-short' if t == 'r' else '**/ears-long').removeNode()
        model.find('**/joint_pupilL_long').removeNode()
        model.find('**/joint_pupilR_long').removeNode()
        model.find('**/head-long').removeNode()
        model.find('**/head-front-long').removeNode()
        for part in model.findAllMatches('**/muzzle-short*' if t == 'r' else '**/muzzle-long'):
            part.removeNode()

    @staticmethod
    def __fixHeadShortShort(model, t):
        for part in model.findAllMatches('**/*long*'):
            part.removeNode()

    """
    GUI Properties
    """

    @property
    def headData(self) -> ToonHeadData:
        return self['headData']

    """
    Toon Head Properties
    """


if __name__ == "__main__":
    gui = ToonHeadGUI(
        parent=aspect2d,
        headData=ToonHeadData(
            headInfo='dls',
            headColor=(0.3, 0.3, 0.3),
        )
        # headHpr=(180, 0, 0),
        # any kwargs go here
    )

    print('dls')
    startType = 'dls'
    toonHeadTypes = ToonDNA.toonHeadTypes

    def forward():
        global startType
        nextTypeIndex = toonHeadTypes.index(startType) + 1
        if nextTypeIndex >= len(toonHeadTypes):
            nextTypeIndex = 0
        startType = toonHeadTypes[nextTypeIndex]
        print(startType)
        gui['headData'] = ToonHeadData(
            headInfo=startType,
            headColor=(0.3, 0.3, 0.3),
        )
    base.accept('a', forward)

    GUITemplateSliders(
        gui,
        'frameSize', 'headHpr'
    )
    base.run()
