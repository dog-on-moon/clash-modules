from direct.gui.DirectGui import *
from toontown.gui.ScaledFrame import ScaledFrame
from toontown.toon import ToonHead
# from toontown.distributed import DelayDelete
from panda3d.otp import *
from toontown.toonbase import ToontownGlobals


class ScaledToonHeadFrame(ScaledFrame):
    def __init__(self, av, directStyle=False, wantLookAround=True, shadow=0.0, frameSize=None):
        ScaledFrame.__init__(
            self,
            relief=None,
            frameSize=frameSize or (-1/2, 1/2, -0.5/2, 0.5/2),
            pos=(0, 0, 0),
            sortOrder=2,
            borderScale=0.035,
        )
        if directStyle:
            style = av
        else:
            style = av.style

        self.directStyle = directStyle
        self.initialiseoptions(self.__class__)
        if shadow > 0:
            self['shadowStrength'] = shadow

        self.av = av

        self.head = self.stateNodePath[0].attachNewNode('head', 20)
        self.head.setPosHprScale(-0.27, 10.0, -0.09, 180.0, 0.0, 0.0, 0.2, 0.2, 0.2)

        self.headModel = ToonHead.ToonHead()
        self.headModel.startBlink()
        if wantLookAround:
            self.headModel.startLookAround()
        self.headModel.setupHead(style, forGui=1)
        self.headModel.reparentTo(self.head)

        # now enable a chat balloon
        self.tag1Node = NametagFloat2d()
        self.tag1Node.setContents(Nametag.CSpeech | Nametag.CThought)
        if directStyle == False: self.av.nametag.addNametag(self.tag1Node)

        self.tag1 = self.attachNewNode(self.tag1Node)
        self.tag1.setPosHprScale(-0.16, 0, -0.09, 0, 0, 0, 0.055, 0.055, 0.055)

        # As well as a nametag just to display the name.
        self.tag2Node = NametagFloat2d()
        self.tag2Node.setContents(Nametag.CName)
        if directStyle == False: self.av.nametag.addNametag(self.tag2Node)
        self.tag2 = self.attachNewNode(self.tag2Node)
        self.tag2.setPosHprScale(-0.27, 10.0, 0.16, 0, 0, 0, 0.05, 0.05, 0.05)

        self.extraData = DirectLabel(
            parent=self,
            relief=None,
            pos=(0.0, 0.0, 0.06),
            scale=1.0,
            text='',
            text0_fg=(0.3, 0.2, 1, 1),
            text_scale=(0.14, 0.06),
            text_pos=(0, -0.01)
        )
        self.extraData.hide()

    def destroy(self):
        ScaledFrame.destroy(self)
        self.headModel.delete()
        del self.headModel
        self.head.removeNode()
        del self.head

        if not self.directStyle:
            if not self.av.isEmpty():
                self.av.nametag.removeNametag(self.tag1Node)
                self.av.nametag.removeNametag(self.tag2Node)
        self.tag1.removeNode()
        self.tag2.removeNode()
        del self.tag1
        del self.tag2
        del self.tag1Node
        del self.tag2Node

        del self.av
        self.extraData.removeNode()
        del self.extraData


class MiniScaledToonHeadFrame(ScaledToonHeadFrame):
    def __init__(self, av, directStyle=False, wantLookAround=True, shadow=0.0):
        xScale, zScale = 0.3, 0.7
        frame = ((-1 / 2)*xScale, (1 / 2)*xScale, (-0.5 / 2)*zScale, (0.5 / 2)*zScale)
        ScaledToonHeadFrame.__init__(self, av, directStyle=directStyle, wantLookAround=wantLookAround, shadow=shadow, frameSize=frame)
        self.head.setScale(0.47 * xScale, 0.2, 0.2 * zScale)
        self.head.setPos(0, 0, -0.1 * zScale)
        # Chat bubble
        self.tag1Node.setActive(1)
        self.tag1.setPos(0.3 * xScale, 0, 0.18 * zScale)
        self.tag1.setScale(0.1540 * xScale, 0, 0.066 * zScale)
        # name tag
        self.tag2.setPos(0, 0, 0.15 * zScale)
        self.tag2.setScale(0.117 * xScale, 0, 0.05 * zScale)
