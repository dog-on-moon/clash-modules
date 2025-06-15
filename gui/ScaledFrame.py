if __name__ == "__main__":
    from tools.headless.headlessbase import HeadlessStart
    from tools.headless.headlessbase.HeadlessBase import HeadlessBase
    base = HeadlessBase()

from panda3d.core import Texture, NodePath, Vec4
from toontown.gui.Bounds import Bounds
from direct.gui.DirectGui import *
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from direct.interval.IntervalGlobal import *


@DirectNotifyCategory()
class ScaledFrame(DirectFrame, Bounds):
    """
    A nine-slice DirectFrame asset.
    Provides a backing texture which scales on the edges/corners.
    """

    scaledModelPath = 'phase_3/models/gui/ttcc_gui_scaledFrame'
    corners = ('top_left', 'top_right', 'bottom_left', 'bottom_right')
    edges = ('top_middle', 'center_right', 'bottom_middle', 'center_left')
    middle = 'center_middle'

    showClipPlanes = False

    def __init__(self, parent=None, **kw):
        # GUI boilerplate.
        assert 'image' not in kw, "ScaledFrame cannot accept 'image' keyword"
        optiondefs = (
            ('relief', None, None),
            ('frameSize', None, None),
            ('scaledTexture', 'phase_3/maps/gui/ttcc_gui_scaledFrame_generic.png', self.setImageTexture),
            ('scaledColor', Vec4(1.0, 1.0, 1.0, 1.0), self.scaleImage),
            ('borderScale', 0.06, self.scaleImage),
            ('scale', 1, self.scaleImage),
            ('borderShrinkStart', 0.3, None),
            ('popIn', False, None),
            ('shadowStrength', 0.0, self.scaleImage),
            ('shadowDirection', 'left', self.scaleImage),
            ('wantClipping', True, None),
            ('wantClipElements', True, None),
            ('hiddenNodes', [], None),
        )
        self.defineoptions(kw, optiondefs)
        self.clipPlanes = []

        self.shadowImage = None

        self.prePopInFrameSize = None

        # Initiate geom.
        self.scaledImage = loader.loadModel(self.scaledModelPath)
        for np in self['hiddenNodes']:
            self.scaledImage.find(f'**/{np}').hide()
        self.setImageTexture()
        self.scaleImage(updateImage=0)

        # Finish initialization
        self.clipPlanes = [
            PlaneNode('sf_left'),
            PlaneNode('sf_right'),
            PlaneNode('sf_down'),
            PlaneNode('sf_up'),
        ] if self['wantClipping'] else []
        self.setPlanes()

        super().__init__(parent, image=self.scaledImage, **kw)
        self.clipNodePaths = [self.attachNewNode(p) for p in self.clipPlanes]
        self.initialiseoptions(ScaledFrame)

        if self.showClipPlanes:
            for np in self.clipNodePaths:
                np.show()

        # Do a pop-in animation
        self.moveSequence = None
        if self.cget('popIn'):
            self.doPopInAnimation()

    def destroy(self):
        if self.moveSequence:
            self.moveSequence.finish()
            self.moveSequence = None
        if self.scaledImage:
            self.scaledImage.removeNode()
            self.scaledImage = None
        if self.shadowImage:
            self.shadowImage.removeNode()
            self.shadowImage = None
        del self.prePopInFrameSize
        super().destroy()

    def doPopInAnimation(self, extraSeq=None):
        goalSize = self['frameSize']
        if not goalSize:
            return

        self.prePopInFrameSize = self['frameSize']

        def popinScale(t, side):
            if side == 0:
                delta_a = t
                delta_b = 0
            else:
                delta_a = 1
                delta_b = t
            l, r, d, u = goalSize
            self['frameSize'] = (
                l * delta_a, r * delta_a,
                d * delta_b, u * delta_b
            )

        baseScale = self.cget('scale')
        popinSpeed = 0.07
        scaleTop = 1.03
        self.moveSequence = Sequence(
            LerpFunctionInterval(popinScale, duration=(popinSpeed / 3) * 2, blendType='easeIn', extraArgs=[0]),
            Parallel(
                Sequence(
                    LerpFunctionInterval(popinScale, duration=popinSpeed, blendType='easeInOut',
                                         fromData=0.0, toData=1.0, extraArgs=[1]),
                ),
                Sequence(
                    self.scaleInterval(duration=popinSpeed, blendType='easeIn',
                                       startScale=1.0 * baseScale, scale=scaleTop * baseScale),
                    self.scaleInterval(duration=popinSpeed, blendType='easeOut',
                                       startScale=scaleTop * baseScale, scale=1.0 * baseScale),
                )
            )
            # LerpFunctionInterval(popinScale, duration=0.07, blendType='easeInOut',
            #                          fromData=1.06, toData=1.0, extraArgs=[1]),
        )
        if extraSeq:
            self.moveSequence = Parallel(
                extraSeq,
                self.moveSequence
            )
        self.moveSequence.start()
        if settings['reduce-gui-movement']:
            self.moveSequence.finish()
        # baseScale = self.cget('scale')
        # self.moveSequence = Sequence(
        #     self.scaleInterval(duration=0.20, blendType='easeInOut',
        #                        startScale=0.01 * baseScale, scale=1.1 * baseScale),
        #     self.scaleInterval(duration=0.09, blendType='easeInOut',
        #                        startScale=1.10 * baseScale, scale=1.0 * baseScale),
        # )

    def hide(self, *args):
        super().hide(*args)
        if self.moveSequence:
            self.moveSequence.finish()
            self.moveSequence = None
        if self.prePopInFrameSize:
            self['frameSize'] = self.prePopInFrameSize

    def createcomponent(self, componentName, componentAliases, componentGroup,
                        widgetClass, *widgetArgs, **kw):
        component = super().createcomponent(componentName, componentAliases, componentGroup,
                                            widgetClass, *widgetArgs, **kw)
        if self.cget('wantClipElements'):
            self.clipWithinFrame(component)
        return component

    def clipWithinFrame(self, *gui):
        """Sets a GUI to clip within our clip planes."""
        for clipNP in self.clipNodePaths:
            for g in gui:
                g.setClipPlane(clipNP)

    @staticmethod
    def setupTexture(texture, texMode=Texture.WMClamp):
        texture.setMinfilter(Texture.FTLinearMipmapLinear)
        texture.setMagfilter(Texture.FTLinear)
        texture.setWrapU(texMode)
        texture.setWrapV(texMode)

    def setImageTexture(self):
        """
        Updates the image texture of the sliced tex.
        """
        imageTex = loader.loadTexture(self.cget('scaledTexture'))
        self.setupTexture(imageTex)
        self.scaledImage.setTexture(imageTex, 1)

    def setFrameSize(self, fClearFrame = 0):
        super().setFrameSize(fClearFrame=fClearFrame)
        self.scaleImage()

    @property
    def scaledGeom(self):
        return self['geom']

    def scaleInterval(self, duration: float, scale: float, startScale: float, blendType: str = 'easeOut'):
        def updateScale(s):
            self.setScale(s)
            self['scale'] = s
        return Parallel(
            LerpFunctionInterval(
                updateScale, duration=duration,
                fromData=startScale, toData=scale,
                blendType=blendType,
            ),
        )

    def setPlanes(self, updateImage=False):
        if not self.clipPlanes:
            return

        # Calculate the bounds of the image.
        cFrameScale = self.cget('scale')
        scaledFrameSize = Vec4(*(self['frameSize'] or (0, 0, 0, 0))) * cFrameScale
        left, right, down, up = scaledFrameSize

        # If updateImage is False, then image_pos doesn't exist
        imagePos = (0, 0, 0) if not updateImage else self['image_pos']

        # left right down up
        self.clipPlanes[0].setPlane(Plane(Vec3(1, 0, 0), Point3(left, 0, 0) + Point3(*imagePos)))
        self.clipPlanes[1].setPlane(Plane(Vec3(-1, 0, 0), Point3(right, 0, 0) + Point3(*imagePos)))
        self.clipPlanes[2].setPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, down) + Point3(*imagePos)))
        self.clipPlanes[3].setPlane(Plane(Vec3(0, 0, -1), Point3(0, 0, up) + Point3(*imagePos)))

    def scaleImage(self, updateImage=1):
        if not self.scaledImage:
            return

        if self.shadowImage:
            self.shadowImage.removeNode()

        # Calculate the bounds of the image.
        cFrameScale = self.cget('scale')
        scaledFrameSize = Vec4(*(self['frameSize'] or (0, 0, 0, 0))) * cFrameScale
        left, right, down, up = scaledFrameSize
        width = max(right - left, 0.001)
        height = max(up - down, 0.001)
        center = Vec3((left + right) / 2, 0, (down + up) / 2)
        borderScale = self.cget('borderScale') / max(cFrameScale, 0.001)

        # Lerp our border scale with a 0-1 mult if our scale iess than th border scale.
        borderScale *= max(0.001, min((cFrameScale / self.cget('borderShrinkStart')), 1))

        # First, handle the corners.
        for cornerString in self.corners:
            node = self.scaledImage.find(f'**/{cornerString}')
            node.setScale(borderScale)
            pos = {
                'top_left':     ((left - borderScale / 2), 1, (up + borderScale / 2)),
                'top_right':    ((right + borderScale / 2), 1, (up + borderScale / 2)),
                'bottom_left':  ((left - borderScale / 2), 1, (down - borderScale / 2)),
                'bottom_right': ((right + borderScale / 2), 1, (down - borderScale / 2)),
            }.get(cornerString)
            node.setPos(pos)

        # Then, handle the sides.
        for edgeString in self.edges:
            node = self.scaledImage.find(f'**/{edgeString}')
            scale = {
                'top_middle':    (width, 1, borderScale),
                'center_right':  (borderScale, 1, height),
                'bottom_middle': (width, 1, borderScale),
                'center_left':   (borderScale, 1, height),
            }.get(edgeString)
            node.setScale(scale)
            pos = {
                'top_middle':    (center.x, 0, up + borderScale / 2),
                'center_right':  (right + borderScale / 2, 0, center.z),
                'bottom_middle': (center.x, 0, down - borderScale / 2),
                'center_left':   (left - borderScale / 2, 0, center.z),
            }.get(edgeString)
            node.setPos(pos)

        # Set the center piece.
        self.scaleMidNode(center, width, height, borderScale)

        wantShadow = self.cget('shadowStrength') > 0
        if wantShadow:
            imageNode = hidden.attachNewNode('ScaledFrame-image-node')
            self.shadowImage = self.scaledImage.copyTo(imageNode, -10)
            shadowTexPath = 'phase_3/maps/gui/ttcc_gui_scaledFrame_shadow.png'
            shadowTex = loader.loadTexture(shadowTexPath)
            self.setupTexture(shadowTex)
            self.shadowImage.setTexture(shadowTex, 1)
            shadowStrength = self.cget('shadowStrength')
            dirMult = -1 if self.cget('shadowDirection') == 'left' else 1
            self.shadowImage.setPos(shadowStrength*dirMult, -0.1, -shadowStrength)
            self.scaledImage.copyTo(imageNode, 10)
        else:
            imageNode = self.scaledImage.copyTo(NodePath('np'))

        self.finalizeScaledImage(imageNode, updateImage, wantShadow)

        if self.clipPlanes:
            self.setPlanes(updateImage)

    def scaleMidNode(self, center, width, height, borderScale):
        centerMid = self.scaledImage.find('**/center_middle')
        centerMid.setScale(width, 1, height)
        centerMid.setPos(center)

    def finalizeScaledImage(self, imageNode, updateImage, wantShadow):
        # Update geom.
        if updateImage:
            if self.shadowImage:
                self.shadowImage.setColorScaleOff(1)
            imageNode.setColorScale(self.cget('scaledColor'))
            # imageNode.flattenStrong()
            self['image'] = imageNode
        if wantShadow:
            imageNode.removeNode()


if __name__ == "__main__":
    frame = ScaledFrame(
        parent=base.aspect2d,
        frameSize=(-0.5, 0.4, -0.5, 0.6),
        scaledColor=(0.5, 0.5, 0.5, 1.0),
        # scaledTexture='phase_4/maps/normalDistrict.png',
    )
    frame['shadowStrength'] = 0.04

    base.setBackgroundColor(1, 1, 1)

    from direct.interval.IntervalGlobal import *

    Sequence(
        Wait(0.3),
        Func(frame.show),
        Func(frame.doPopInAnimation),
        Wait(2.0),
        Func(frame.hide)
    ).loop()

    base.run()

    # frame = ScaledFrame(
    #     parent=base.aspect2d,
    #     frameSize=(-0.5, 0.4, -0.5, 0.6),
    #     scaledTexture='phase_4/maps/normalDistrict.png',
    #     text='YOUR SOUL\nIS MINE',
    #     text_scale=0.3,
    #     text_fg=(0, 0, 0, 1),
    # )
    #
    # import math
    #
    # def funnyScale(t):
    #     frame['frameSize'] = (
    #         -((-math.cos(t) * 0.25) + 0.5),
    #         ((math.sin(t * 1.4) * 0.25) + 0.5),
    #         -((math.cos(t * 1.8) * 0.25) + 0.5),
    #         ((-math.sin(t * 2.2) * 0.25) + 0.5),
    #     )
    #
    # from direct.interval.IntervalGlobal import *
    # Parallel(
    #     Sequence(
    #         Parallel(
    #             Sequence(
    #                 frame.scaleInterval(duration=0.2, startScale=0.01, scale=1.1, blendType='easeInOut'),
    #                 frame.scaleInterval(duration=0.2, startScale=1.1, scale=1.0, blendType='easeInOut'),
    #             )
    #         ),
    #         Wait(1.0),
    #         # LerpHprInterval(frame, 1.0, (360, 360, 360), startHpr=(0, 0, 0), blendType='easeInOut'),
    #         frame.scaleInterval(duration=0.2, startScale=1.0, scale=0.01, blendType='easeInOut'),
    #     ),
    #     Sequence(
    #         LerpFunctionInterval(funnyScale, duration=0.8,
    #                              fromData=0, toData=math.pi * 1,
    #                              blendType='easeInOut'),
    #         LerpFunctionInterval(funnyScale, duration=0.8,
    #                              fromData=math.pi * 1, toData=0,
    #                              blendType='easeInOut'),
    #     )
    # ).loop()
    #
    # base.run()

