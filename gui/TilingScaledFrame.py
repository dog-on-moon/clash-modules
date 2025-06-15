if __name__ == "__main__":
    from tools.headless.headlessbase import HeadlessStart
    from tools.headless.headlessbase.HeadlessBase import HeadlessBase
    base = HeadlessBase(wantHotkeys=False)
    if __debug__:
        from toontown.utils.DeveloperInjector import startInjector
        startInjector()

from panda3d.core import *
from direct.interval.IntervalGlobal import *
from toontown.gui.ScaledFrame import ScaledFrame
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
import time


@DirectNotifyCategory()
class TilingScaledFrame(ScaledFrame):
    def __init__(self, parent=None, **kwargs):
        self.patternNode = NodePath()
        self.__patternLastMoveTime = 0
        self.__patternSeq = None
        self.fInit = 1

        optiondefs = (
            ('frameBin', 0, None),
            ('patternTexture', 'core/gui/maps/cc_t_gui_sframe_pat_testblue.png', None),
            ('scaledTexture', 'phase_3/maps/gui/ttcc_gui_scaledFrame_test_shadow.png', None),
            ('patternSpeed', (0.02, -0.02), self.setPatternSpeed),
            ('patternScale', 0.14, self.setPatternScale),
        )
        self.defineoptions(kwargs, optiondefs)
        super().__init__(parent=parent, **kwargs)
        self.initialiseoptions(TilingScaledFrame)
        self.patternNode.reparentTo(self)
        # Need to ensure the borders are above the pattern texture
        self.setBin('sorted-gui-popup', self['frameBin'])
        self.patternNode.setBin('sorted-gui-popup', self['frameBin'] - 1)

    def destroy(self):
        if self.__patternSeq:
            self.__patternSeq.finish()
            self.__patternSeq = None
        if self.patternNode:
            self.patternNode.removeNode()
            self.patternNode = None
        super().destroy()

    def finalizeScaledImage(self, imageNode, updateImage, wantShadow):
        if self.shadowImage:
            # Ensure the shadow texture is below all other parts
            self.shadowImage.setBin('sorted-gui-popup', self['frameBin'] - 2)

        centerMid = self.scaledImage.find('**/center_middle')
        centerLeft = self.scaledImage.find('**/center_left')
        topMid = self.scaledImage.find('**/top_middle')

        if not self.patternNode:
            # Create the pattern node that will hold the tiling texture
            self.patternNode = centerMid.copyTo(self.patternNode)
            newTex = loader.loadTexture(self['patternTexture'])
            self.setupTexture(newTex, texMode=Texture.WMRepeat)
            self.patternNode.setTexture(newTex, 1)

        newScale = (centerMid.getScale()[0] + centerLeft.getScale()[0], 1, centerMid.getScale()[2] + topMid.getScale()[2])
        ourScale = self.cget('scale')
        # Pattern node scale is based on overall frame scale as well as the scale of the center mid piece,
        # center left piece, and top mid piece.
        self.patternNode.setScale(newScale[0] * ourScale, newScale[1] * ourScale, newScale[2] * ourScale)
        self.setPatternScale()
        scaledFrameSize = Vec4(*(self['frameSize'] or (0, 0, 0, 0)))
        l, r, d, u = scaledFrameSize
        # Don't try to grab image pos if in the middle of init of DirectGUI
        imagePos = self['image_pos'] if not self.fInit else (0, 0, 0)
        # Update the pattern node pos to fit within the new bounds
        self.patternNode.setPos(((r + l) / 2) + imagePos[0], 0, ((d + u) / 2) + imagePos[2])
        # This helps the pattern to look less awkward when the frameSize changes
        ratioFactor = ((-4/3) / self['patternScale'])
        self.patternNode.setTexOffset(TextureStage.getDefault(), ((r - l) / 2)*ratioFactor, ((u - d) / 2)*ratioFactor)

        # Update geom.
        super().finalizeScaledImage(imageNode, updateImage, wantShadow)

    def setPatternScale(self):
        centerMid = self.scaledImage.find('**/center_middle')
        centerLeft = self.scaledImage.find('**/center_left')
        topMid = self.scaledImage.find('**/top_middle')

        newScale = (centerMid.getScale()[0] + centerLeft.getScale()[0], 1, centerMid.getScale()[2] + topMid.getScale()[2])
        ourScale = self.cget('scale')
        # Update tex scale based on our pattern scale var
        self.patternNode.setScale(newScale[0] * ourScale, newScale[1] * ourScale, newScale[2] * ourScale)
        self.patternNode.setTexScale(TextureStage.getDefault(), newScale[0] / max(self['patternScale'], 0.01),
                                     newScale[2] / max(self['patternScale'], 0.01))

    def setPatternSpeed(self):
        if self.__patternSeq:
            self.__patternSeq.finish()
            self.__patternSeq = None

        patternSpeed = self['patternSpeed']
        if patternSpeed == 0:
            return
        if type(patternSpeed) in (tuple, list) and (patternSpeed[0] == 0 and patternSpeed[1] == 0):
            return

        # Begin the seq to move the pattern tile
        self.__patternSeq = Sequence(LerpFunctionInterval(self.__movePattern, duration=1.0))
        self.__patternSeq.loop()

    def __movePattern(self, _):
        newTime = time.time()

        patternSpeed = self['patternSpeed']
        if type(patternSpeed) in (tuple, list):
            offX, offZ = patternSpeed[0], patternSpeed[1]
        else:
            offX, offZ = patternSpeed, patternSpeed

        # Keeps the overall distance moved of the pattern consistent and wrapped within (0, 1)
        offX = -((offX * newTime) / self['patternScale']) % 1
        offZ = -((offZ * newTime) / self['patternScale']) % 1

        self.patternNode.setTexOffset(TextureStage.getDefault(), offX, offZ)
        self.__patternLastMoveTime = newTime


if __name__ == "__main__":
    frame = TilingScaledFrame(
        parent=base.aspect2d,
        frameSize=(-0.5, 0.4, -0.5, 0.6),
        # scaledTexture='phase_4/maps/normalDistrict.png',
        text='YOUR SOUL\nIS MINE',
        text_scale=0.07,
        text_fg=(0, 0, 0, 1),
    )
    frame['shadowStrength'] = 0.04
    frame.doPopInAnimation()

    base.setBackgroundColor(1, 1, 1)

    from toontown.gui.GUITemplateSliders import GUITemplateSliders

    GUITemplateSliders(
        frame,
        'frameSize', 'patternScale'
    )

    # Sequence(
    #     Wait(0.3),
    #     Func(frame.show),
    #     Func(frame.doPopInAnimation),
    #     Wait(2.0),
    #     Func(frame.hide)
    # ).loop()

    base.run()
