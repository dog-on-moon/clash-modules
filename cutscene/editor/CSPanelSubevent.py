"""
The GUI panel manager for the Subevent Panel.

"""
from toontown.cutscene.editor.CSEditorEnums import SubEventArgumentType
from toontown.gui.TTGui import ScrollWheelFrame
from toontown.cutscene.editor.CSEditorClasses import EventArgument
from toontown.cutscene.editor.CSPanelAdjusters import CSPanelAdjusters

# if TYPE_CHECKING:
#     from toontown.cutscene.editor.CSEditorManager import CSEditorManager


class CSPanelSubevent(ScrollWheelFrame):

    frameColor = (0.8, 0.8, 0.8, 0.3)

    adjusterStartHeight = 0.18
    height = 1.5
    width = 1.1
    sliderWidth = 0.06

    def __init__(self, mgr, **kw):
        optiondefs = (
            ('frameColor', self.frameColor, None),
            ('frameSize', (0, self.width, -self.height, 0), None),
            ('pos', (-self.width, 0, self.height), None),
            ('scrollBarWidth', self.sliderWidth, None),
        )
        self.defineoptions(kw, optiondefs)
        ScrollWheelFrame.__init__(self, base.a2dBottomRight, **kw)
        self.initialiseoptions(CSPanelSubevent)

        # set properties of panel
        self.mgr = mgr  # type: CSEditorManager
        self.cutsceneDict = mgr.cutsceneDict
        self.subevent = None

        self.adjusters = []

        self.updateCanvasSize()
        self.accept('selectedSubevent', self.update)
        self.accept('newSubevent', self.newSubevent)

    def update(self, subevent):
        self.subevent = subevent
        self.hide()
        if subevent is None:
            return
        self.show()

        self.makeAdjusters()

        self.updateCanvasSize()

    def cleanupAdjusters(self):
        for adjuster in self.adjusters:
            adjuster.destroy()
        self.adjusters = []

    def makeAdjusters(self):
        self.cleanupAdjusters()
        currentHeight = -self.adjusterStartHeight
        eventDefinition = self.subevent.eventDef
        for argument in eventDefinition.arguments:
            argument: EventArgument
            if argument.type in CSPanelAdjusters:
                adjusterClass = CSPanelAdjusters[argument.type]
                x, y, z = adjusterClass.offset
                adjusterObject = adjusterClass(
                    parent=self.getCanvas(), subevent=self.subevent,
                    kwarg=argument.kwarg, cutsceneDict=self.cutsceneDict,
                    pos=(x + (self.width / 2), y, currentHeight + z),
                )
                self.adjusters.append(adjusterObject)
                adjusterObject.setSubeventPanel(self)
                adjusterObject.bindScroll(scrollWheelFrame=self)
                currentHeight -= adjusterClass.height

    def getAdjusterHeights(self):
        retHeight = self.adjusterStartHeight
        for adjuster in self.adjusters:
            retHeight += adjuster.height
        return retHeight

    def updateCanvasSize(self):
        x1, x2, y1, y2 = self['frameSize']
        self['canvasSize'] = (x1, x2 - self.sliderWidth, min(y1 - 0.001, -self.getAdjusterHeights()), y2)
        self.setCanvasSize()

    def newSubevent(self):
        """
        If this subevent is new, tell our adjusters.
        """
        for adjuster in self.adjusters:
            adjuster.doNewSubevent()

    def onKwargUpdate(self, key, val):
        """
        When a kwarg is updated, tell all adjusters.
        """
        for adjuster in self.adjusters:
            adjuster.onKwargUpdate(key, val)
