if __name__ == "__main__":
    from tools.headless.headlessbase import HeadlessStart
    from tools.headless.headlessbase.HeadlessBase import HeadlessBase
    base = HeadlessBase()

from direct.gui.DirectGui import *
from panda3d.core import *

from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.gui.TTGui import kwargsToOptionDefs


@DirectNotifyCategory()
class ChatBubbleTextFrame(DirectFrame):
    """
    There's something really funky with this class that makes it not properly construct itself but
    I am too lazy to find out what it is and fix it right now so oh well.
    """
    BalloonPath = 'phase_3/models/props/chatbox'
    DefaultTopHeight = 2.5
    MidScaleDiffFactor = -2.0
    BeginXScalePoint = 8.72

    def __init__(self, parent=aspect2d, **kw):
        self.topHeight = self.DefaultTopHeight
        self.midScale = self.topHeight + self.MidScaleDiffFactor
        self.xScale = 1.0
        # Determines if the chat bubble should scale on the X Axis before it reaches its designated
        # "scaling point". This basically will make it shrink on the X to fit smaller bubbles
        # rather than only larger ones.
        self.scaleBeforeScalePoint = False
        # These exist bc this class refuses to construct properly and I don't get it
        # You can get rid of these if you can fix it.
        # Otherwise, it appears to work properly applying these later.
        self.wordwrap = None
        self.textScale = 1.0
        self.textAlign = TextNode.ACenter
        chatBalloon = loader.loadModel(self.BalloonPath)
        chatBalloon.find('**/top').setPos(1, 0, self.topHeight)
        chatBalloon.find('**/middle').setScale(1, 1, self.midScale)
        optiondefs = kwargsToOptionDefs(
            relief=None,
            text_scale=1.0,
            text_pos=(2, 1),
            textMayChange=1,
            textAlign=TextNode.ALeft
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent=parent)
        super().initialiseoptions(ChatBubbleTextFrame)
        chatBalloon.removeNode()

    def resetImage(self):
        chatBalloon = loader.loadModel(self.BalloonPath)
        chatBalloon.find('**/top').setPos(1, 0, self.topHeight)
        chatBalloon.find('**/middle').setScale(1, 1, self.midScale)
        chatBalloon.find('**/chatBalloon').setScale(self.xScale, 1, 1)
        self['image'] = chatBalloon
        chatBalloon.removeNode()

    def scaleToText(self):
        self['text_pos'] = (5.45, self.DefaultTopHeight - 0.5)
        self['text_wordwrap'] = self.wordwrap
        self['text_scale'] = self.textScale
        self['text_align'] = self.textAlign
        text0 = self.component('text0')
        bounds = text0.getTightBounds()
        # Bounds will be none if no text is set.
        if bounds is None:
            return

        bMin, bMax = bounds
        textHeight = bMax[2] - bMin[2]
        self.topHeight = max(self.DefaultTopHeight, textHeight + 1.3)
        self.midScale = self.topHeight + self.MidScaleDiffFactor
        textWidth = bMax[0] - bMin[0]
        self.xScale = textWidth / self.BeginXScalePoint
        if not self.scaleBeforeScalePoint:
            self.xScale = max(1.0, self.xScale)
        xPosMod = {
            TextNode.ALeft: -textWidth/2,
            TextNode.ARight: textWidth/2
        }.get(self.textAlign, 0.0)
        self['text_pos'] = ((5.45 * self.xScale) + xPosMod, self.topHeight - 0.5)
        self.resetImage()


if __name__ == "__main__":
    hoverBubble = ChatBubbleTextFrame(parent=aspect2d)
    hoverBubble.setScale(0.1)
    hoverBubble.setPos(-1.1, 0, -0.5)
    text = "\1deepBlue\1Step Rewards\2\n"
    text += "\1TextShrink\1"
    text += "67 Jellybeans\n7193 Experience\n"
    text += "\n\2"
    text += "\1deepBlue\1Completion Rewards\2\n"
    text += "\1TextShrink\1"
    text += "67 Jellybeans\n7193 Experience\n"
    text += "\n\2"
    text += "\1deepBlue\1"
    text += "3 steps left\2"
    hoverBubble['text'] = text
    hoverBubble.scaleToText()

    base.setBackgroundColor(1, 1, 1, 1)
    base.run()

