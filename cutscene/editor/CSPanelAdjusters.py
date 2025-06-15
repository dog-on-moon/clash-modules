"""
Adjusters for the CS Panel.
"""
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectFrame import DirectFrame
from toontown.gui.DirectScrollableOptionMenu import DirectScrollableOptionMenu

from toontown.gui.TTGui import SizerFrame, CheckboxButton, ScrollWheelFrame
from toontown.cutscene.editor.CSEditorDefs import *
from toontown.cutscene.editor.CSEditorEnums import ToonBlockShape
from toontown.utils.DocstringInterpreter import getEnumFromDocstring

from toontown.toonbase import TTLocalizer

CSPanelAdjusters = {}


class CSPanelAdjusterBase:
    """
    The base class for a CSPanelAdjuster.
    """

    height = 0.0
    offset = (0, 0, 0)

    def __init__(self, subevent, kwarg, cutsceneDict, callback=None):
        """
        Used for defining properties of a CSPanelAdjuster.
        :param subevent:    The subevent dataclass this adjuster is tied to.
        :param kwarg:       The keyword of the event to change.
        :param callback:    Any callbacks to fulfill upon update.
        """
        assert kwarg in subevent.kwargs, f"Invalid subevent and kwarg passed in." \
                                         f"\nSubevent Info: {subevent.eventDefEnum}," \
                                         f"with expected kwargs of {subevent.kwargs}." \
                                         f"\nThe kwarg on this adjusted that was received: {kwarg}"
        self.subeventPanel = None
        self.subevent: SubEvent = subevent
        self.kwarg = kwarg
        self.eventArgument = self.subevent.getEventArgument(kwarg)
        self.cutsceneDict = cutsceneDict
        self.callback = callback
        taskMgr.add(self.handleAdjust, self.getAdjustTaskName())

    def destroy_base(self):
        """
        A cleanup method.
        """
        self.subeventPanel = None
        taskMgr.remove(self.getAdjustTaskName())

    def getAdjusterValue(self):
        """
        Must return the value of the adjuster.
        """
        raise NotImplementedError

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        raise NotImplementedError(f"class {self.__class__} must implement bindScroll on its assets")

    def onAdjust(self):
        """
        Called whenever the value of this adjuster is updated.
        Subclasses may be able to adjust this in silly little ways.
        """
        pass

    def handleAdjust(self, task=None):
        """
        This task is continuously called to ensure that
        the subevent has its kwargs set.
        """
        newVal = self.getAdjusterValue()
        if self.subevent[self.kwarg] != newVal:
            self.subevent[self.kwarg] = newVal
            self.subeventPanel.onKwargUpdate(self.kwarg, newVal)
        if task is not None:
            return task.cont

    def getEventArgument(self) -> EventArgument:
        return self.subevent.eventDef.getEventArgument(self.kwarg)

    def getKwargName(self):
        """
        Returns the name of the kwarg.
        """
        return self.getEventArgument().name

    def getAdjustTaskName(self):
        """
        Gets the task name for the adjustor task.
        """
        return f'subevent-adjust-{self.kwarg}'

    def doNewSubevent(self):
        self.onNewSubevent()
        self.handleAdjust()

    def onNewSubevent(self):
        """
        This method gets called if the relevant subevent is new.
        """
        pass

    def onKwargUpdate(self, key, val):
        """Called on all sliders when a kwarg updates."""
        pass

    def setSubeventPanel(self, panel):
        self.subeventPanel = panel


class SliderXYZ(CSPanelAdjusterBase, DirectFrame):
    """
    A XYZ slider, used for adjustments in 3D space.
    Enum: slider_xyz
    """

    height = 0.4

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        optiondefs = (
            ('frameColor', (0, 0, 0, 0), None),
        )
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)
        self.initialiseoptions(SliderXYZ)

        self.sizerNode = DirectFrame(
            parent=self, frameColor=(0, 0, 0, 0), pos=(-0.1, 0, 0),
        )
        self.sizer = SizerFrame(
            self.sizerNode, self.eventArgument.name, 'xyz', self.subevent[kwarg], (-20, 20)
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.sizerNode)
        self.sizer.bindScroll(scrollWheelFrame=scrollWheelFrame)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def getAdjusterValue(self):
        return self.sizer.getValues()


class SliderRGB(CSPanelAdjusterBase, DirectFrame):
    """
    An RGBA slider, used for color adjustments on nodes.
    Enum: slider_rgb
    """

    height = 0.5

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        optiondefs = (
            ('frameColor', (0, 0, 0, 0), None),
        )
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)
        self.initialiseoptions(SliderXYZ)

        self.sizerNode = DirectFrame(
            parent=self, frameColor=(0, 0, 0, 0), pos=(-0.1, 0, 0),
        )
        self.sizer = SizerFrame(
            self.sizerNode, self.eventArgument.name, 'rgba', self.subevent[kwarg], (0, 1)
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.sizerNode)
        self.sizer.bindScroll(scrollWheelFrame=scrollWheelFrame)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def getAdjusterValue(self):
        return self.sizer.getValues()


class SliderHPR(CSPanelAdjusterBase, DirectFrame):
    """
    A HPR slider, used for rotations in 3D space.
    Enum: slider_hpr
    """

    height = 0.4

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        optiondefs = (
            ('frameColor', (0, 0, 0, 0), None),
        )
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)
        self.initialiseoptions(SliderHPR)

        self.sizerNode = DirectFrame(
            parent=self, frameColor=(0, 0, 0, 0), pos=(-0.1, 0, 0),
        )
        self.sizer = SizerFrame(
            self.sizerNode, self.eventArgument.name, 'hpr', self.subevent[kwarg], (-180, 180)
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.sizerNode)
        self.sizer.bindScroll(scrollWheelFrame=scrollWheelFrame)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def getAdjusterValue(self):
        return self.sizer.getValues()


class SliderXYZCamera(CSPanelAdjusterBase, DirectFrame):
    """
    A XYZ slider, used for adjustments in 3D space.
    Updates with the camera.
    Enum: slider_xyz_camera
    """

    height = 0.4

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        optiondefs = (
            ('frameColor', (0, 0, 0, 0), None),
        )
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)
        self.initialiseoptions(SliderXYZCamera)

        self.matchButton = DirectButton(
            parent=self, command=self.match,
            frameSize=(-0.08, 0.08, -0.03, 0.06),
            pos=(0.4081, 0, 0.09), scale=0.7,
            text='match', text_scale=0.05,
        )

        self.sizerNode = DirectFrame(
            parent=self, frameColor=(0, 0, 0, 0), pos=(-0.1, 0, 0),
        )
        self.sizer = SizerFrame(
            self.sizerNode, self.eventArgument.name, 'xyz', self.subevent[kwarg], (-20, 20)
        )

    def match(self):
        self.sizer.setValues(base.camera.getPos())

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.sizerNode)
        self.sizer.bindScroll(scrollWheelFrame=scrollWheelFrame)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def getAdjusterValue(self):
        return self.sizer.getValues()

    def onNewSubevent(self):
        if base.camera.getPos() == (0, 0, 0):
            return
        self.sizer.setValues(newValues=base.camera.getPos(), doCallback=False)


class SliderHPRCamera(CSPanelAdjusterBase, DirectFrame):
    """
    A HPR slider, used for rotations in 3D space.
    Updates with the camera.
    Enum: slider_hpr_camera
    """

    height = 0.4

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        optiondefs = (
            ('frameColor', (0, 0, 0, 0), None),
        )
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)
        self.initialiseoptions(SliderHPRCamera)

        self.matchButton = DirectButton(
            parent=self, command=self.match,
            frameSize=(-0.08, 0.08, -0.03, 0.06),
            pos=(0.4081, 0, 0.09), scale=0.7,
            text='match', text_scale=0.05,
        )

        self.sizerNode = DirectFrame(
            parent=self, frameColor=(0, 0, 0, 0), pos=(-0.1, 0, 0),
        )
        self.sizer = SizerFrame(
            self.sizerNode, self.eventArgument.name, 'hpr', self.subevent[kwarg], (-180, 180)
        )

    def match(self):
        self.sizer.setValues(base.camera.getHpr())

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.sizerNode)
        self.sizer.bindScroll(scrollWheelFrame=scrollWheelFrame)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def getAdjusterValue(self):
        return self.sizer.getValues()

    def onNewSubevent(self):
        if base.camera.getHpr() == (0, 0, 0):
            return
        self.sizer.setValues(newValues=base.camera.getHpr(), doCallback=False)


class SliderMinZero(CSPanelAdjusterBase, DirectFrame):
    """
    A slider. Return values cannot go beneath 0.
    Enum: slider_min_zero
    """

    height = 0.22

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        optiondefs = (
            ('frameColor', (0, 0, 0, 0), None),
        )
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)
        self.initialiseoptions(SliderMinZero)

        self.sizerNode = DirectFrame(
            parent=self, frameColor=(0, 0, 0, 0), pos=(-0.1, 0, 0),
        )
        name = self.getKwargName()
        self.sizer = SizerFrame(
            self.sizerNode, name, name[0].lower(), [self.subevent[kwarg]], (0, 10)
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.sizerNode)
        self.sizer.bindScroll(scrollWheelFrame=scrollWheelFrame)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def getAdjusterValue(self):
        return max(0, self.sizer.getValues()[0])


class SliderMinAlmostZero(CSPanelAdjusterBase, DirectFrame):
    """
    A slider. Return values cannot go beneath 0.001.
    Enum: slider_min_almost_zero
    """

    height = 0.22

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        optiondefs = (
            ('frameColor', (0, 0, 0, 0), None),
        )
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)
        self.initialiseoptions(SliderMinAlmostZero)

        self.sizerNode = DirectFrame(
            parent=self, frameColor=(0, 0, 0, 0), pos=(-0.1, 0, 0),
        )
        name = self.getKwargName()
        self.sizer = SizerFrame(
            self.sizerNode, name, name[0].lower(), [self.subevent[kwarg]], (0, 10)
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.sizerNode)
        self.sizer.bindScroll(scrollWheelFrame=scrollWheelFrame)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def getAdjusterValue(self):
        return max(0.001, self.sizer.getValues()[0])


class SliderFloat(CSPanelAdjusterBase, DirectFrame):
    """
    A slider. Can return any float value.
    Enum: slider_float
    """

    height = 0.22

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        optiondefs = (
            ('frameColor', (0, 0, 0, 0), None),
        )
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)
        self.initialiseoptions(SliderMinZero)

        self.sizerNode = DirectFrame(
            parent=self, frameColor=(0, 0, 0, 0), pos=(-0.1, 0, 0),
        )
        name = self.getKwargName()
        self.sizer = SizerFrame(
            self.sizerNode, name, name[0].lower(), [self.subevent[kwarg]], (-1, 1)
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.sizerNode)
        self.sizer.bindScroll(scrollWheelFrame=scrollWheelFrame)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def getAdjusterValue(self):
        return self.sizer.getValues()[0]


class SliderFOV(CSPanelAdjusterBase, DirectFrame):
    """
    A slider. Return values cannot go beneath 0. Sticks with FOV.
    Enum: slider_fov
    """

    height = 0.22

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        optiondefs = (
            ('frameColor', (0, 0, 0, 0), None),
        )
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)
        self.initialiseoptions(SliderMinZero)

        self.sizerNode = DirectFrame(
            parent=self, frameColor=(0, 0, 0, 0), pos=(-0.1, 0, 0),
        )
        name = self.getKwargName()
        self.sizer = SizerFrame(
            self.sizerNode, name, name[0].lower(), [self.subevent[kwarg]], (0, 100)
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.sizerNode)
        self.sizer.bindScroll(scrollWheelFrame=scrollWheelFrame)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def getAdjusterValue(self):
        return max(0, self.sizer.getValues()[0])

    def onNewSubevent(self):
        newHpr = CameraSequence.camLens.getMinFov()
        self.sizer.setValues(newValues=[newHpr], doCallback=False)


class TextboxString(CSPanelAdjusterBase, DirectFrame):
    """
    An entry for text.
    Enum: textbox_str
    """

    height = 0.2

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        optiondefs = (
            ('frameColor', (0, 0, 0, 0), None),
        )
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)
        self.initialiseoptions(TextboxString)

        self.currentText = self.subevent[kwarg]

        self.entry_text = DirectEntry(
            parent=self, command=self.requestText,
            initialText=self.currentText, width=8, numLines=1, scale=.05,
            pos=(-0.21, 0, 0), frameColor=(0.8, 0.8, 0.8, 0.3),
            text=self.getKwargName(), text_scale=0.06,
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.entry_text)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        self.currentText = newText
        self.entry_text.setText(newText)

    def getAdjusterValue(self):
        return self.currentText


class TextboxFloat(CSPanelAdjusterBase, DirectFrame):
    """
    An entry for text.
    Enum: textbox_float
    """

    height = 0.2

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        optiondefs = (
            ('frameColor', (0, 0, 0, 0), None),
        )
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)
        self.initialiseoptions(TextboxFloat)

        self.currentText = self.subevent[kwarg]

        self.entry_text = DirectEntry(
            parent=self, command=self.requestText,
            initialText=self.currentText, width=8, numLines=1, scale=.05,
            pos=(-0.21, 0, 0), frameColor=(0.8, 0.8, 0.8, 0.3),
            text=self.getKwargName(), text_scale=0.06,
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.entry_text)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        try:
            newText = float(newText)
        except TypeError:
            return
        else:
            self.currentText = float(newText)
        self.entry_text.setText(str(self.currentText))

    def getAdjusterValue(self):
        return float(self.currentText)


class DropdownMessages(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for messages.
    Enum: dropdown_messages
    """

    textLength = 30
    height = 0.1
    offset = (-0.1, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        self.items = list(cutsceneDict['messages']) if cutsceneDict.get('messages', None) else ['No messages detected.']
        for i, item in enumerate(self.items):
            if len(item) > self.textLength:
                self.items[i] = item[0:self.textLength-3] + '...'

        self.selectedIndex = self.subevent[kwarg]
        optiondefs = (
            ('initialitem', self.selectedIndex, None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownMessages)

        self.textLabel = DirectFrame(
            parent=self, text='Msgs', text_scale=1.1,
            text_pos=(-2.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedIndex = self.items.index(newText)

    def getAdjusterValue(self):
        return self.selectedIndex


class DropdownActors(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for actors.
    Enum: dropdown_actors
    """

    textLength = 30
    height = 0.1
    offset = (-0.1, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        self.items = cutsceneDict['actors'][:]

        self.itemIndexDict = {}

        for i, item in enumerate(self.items):
            if item is None:
                continue
            if hasattr(item, 'getName'):
                self.items[i] = str(item.getName().replace('\n', '-')) + f'-{i}'
            else:
                self.items[i] = str(type(item).__name__.replace('\n', '-')) + f'-{i}'
            self.itemIndexDict[self.items[i]] = i

        self.selectedIndex = self.subevent[kwarg]
        optiondefs = (
            ('initialitem', self.selectedIndex, None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownActors)

        self.textLabel = DirectFrame(
            parent=self, text='Actors', text_scale=1.1,
            text_pos=(-2.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedIndex = self.itemIndexDict[newText]

    def getAdjusterValue(self):
        return self.selectedIndex


class DropdownToons(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for toons.
    Enum: dropdown_toons
    """

    textLength = 30
    height = 0.1
    offset = (-0.1, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        self.items = cutsceneDict['toons'][:]

        self.itemIndexDict = {}

        for i, item in enumerate(self.items):
            if item is None:
                continue
            if hasattr(item, 'getName'):
                self.items[i] = str(item.getName().replace('\n', '-')) + f'-{i}'
            else:
                self.items[i] = str(type(item).__name__.replace('\n', '-')) + f'-{i}'
            self.itemIndexDict[self.items[i]] = i

        self.selectedIndex = self.subevent[kwarg]
        optiondefs = (
            ('initialitem', self.selectedIndex, None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownToons)

        self.textLabel = DirectFrame(
            parent=self, text='Toons', text_scale=1.1,
            text_pos=(-2.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedIndex = self.itemIndexDict[newText]

    def getAdjusterValue(self):
        return self.selectedIndex


class DropdownSuits(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for suits.
    Enum: dropdown_suits
    """

    textLength = 30
    height = 0.2
    offset = (-0.1, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        self.items = cutsceneDict['suits'][:]

        self.itemIndexDict = {}

        for i, item in enumerate(self.items):
            if item is None:
                continue
            if hasattr(item, 'getName'):
                self.items[i] = str(item.getName().replace('\n', '-')) + f'-{i}'
            else:
                self.items[i] = str(type(item).__name__.replace('\n', '-')) + f'-{i}'
            self.itemIndexDict[self.items[i]] = i

        self.selectedIndex = self.subevent[kwarg]
        optiondefs = (
            ('initialitem', self.selectedIndex, None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownSuits)

        self.textLabel = DirectFrame(
            parent=self, text='Suits', text_scale=1.1,
            text_pos=(-2.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedIndex = self.itemIndexDict[newText]

    def getAdjusterValue(self):
        return self.selectedIndex


class DropdownBossCogs(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for boss cogs.
    Enum: dropdown_bosses
    """

    textLength = 30
    height = 0.2
    offset = (-0.1, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        self.items = cutsceneDict['bosses'][:]

        self.itemIndexDict = {}

        for i, item in enumerate(self.items):
            if item is None:
                continue
            if hasattr(item, 'getName'):
                self.items[i] = str(item.getName().replace('\n', '-')) + f'-{i}'
            else:
                self.items[i] = str(type(item).__name__.replace('\n', '-')) + f'-{i}'
            self.itemIndexDict[self.items[i]] = i

        self.selectedIndex = self.subevent[kwarg]
        optiondefs = (
            ('initialitem', self.selectedIndex, None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownBossCogs)

        self.textLabel = DirectFrame(
            parent=self, text='Bosses', text_scale=1.1,
            text_pos=(-2.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedIndex = self.itemIndexDict[newText]

    def getAdjusterValue(self):
        return self.selectedIndex


class DropdownToonAnims(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for toon anims.
    Enum: dropdown_toon_anims
    """

    textLength = 30
    height = 0.1
    offset = (-0.1, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        self.items = ['neutral', 'run', 'walk', 'teleport', 'jump', 'running-jump', 'book',
                      'jump-land', 'pushbutton', 'throw', 'victory', 'conked', 'cringe', 'confused', 'sidestep-left',
                      'sidestep-right', 'wave', 'shrug', 'angry', 'left-point', 'right-point', 'duck', 'slip-forward',
                      'slip-backward', 'bored', 'sit']

        self.selectedIndex = self.subevent[kwarg]
        if "'" in self.selectedIndex:
            # no apostrophies pwease
            self.selectedIndex = self.selectedIndex[1:-1]
        optiondefs = (
            ('initialitem', self.items.index(self.selectedIndex), None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownToonAnims)

        self.textLabel = DirectFrame(
            parent=self, text='Toon Anim', text_scale=1.1,
            text_pos=(-3.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedIndex = self.items.index(newText)

    def getAdjusterValue(self):
        return self.items[self.selectedIndex]


class DropdownToonAnimStates(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for toon anim states.
    Enum: dropdown_toon_anim_states
    """

    textLength = 30
    height = 0.1
    offset = (-0.1, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        self.items = ['Neutral', 'Squish', 'TeleportOut', 'TeleportIn']

        self.selectedIndex = self.subevent[kwarg]
        if "'" in self.selectedIndex:
            # no apostrophies pwease
            self.selectedIndex = self.selectedIndex[1:-1]
        optiondefs = (
            ('initialitem', self.items.index(self.selectedIndex), None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownToonAnimStates)

        self.textLabel = DirectFrame(
            parent=self, text='Toon Anim State', text_scale=1.1,
            text_pos=(-3.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedIndex = self.items.index(newText)

    def getAdjusterValue(self):
        return self.items[self.selectedIndex]


class DropdownToonEmote(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for toon emotes.
    Enum: dropdown_toon_emote
    """

    textLength = 30
    height = 0.1
    offset = (-0.1, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        # TODO: Make this work with new hammerspace emote definitions.
        self.items = list(TTLocalizer.EmoteFuncDict.keys())

        self.selectedIndex = self.subevent[kwarg]

        self.itemIndexDict = {}

        for i, item in enumerate(self.items):
            if item is None:
                continue

            self.itemIndexDict[self.items[i]] = i

        optiondefs = (
            ('initialitem', self.selectedIndex, None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownToonEmote)

        self.textLabel = DirectFrame(
            parent=self, text='Toon Emote', text_scale=1.1,
            text_pos=(-3.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedIndex = self.itemIndexDict[newText]

    def getAdjusterValue(self):
        return self.items[self.selectedIndex]


class DropdownSuitAnims(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for suit anims.
    Enum: dropdown_suit_anims
    """

    textLength = 30
    height = 0.1
    offset = (-0.1, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        from toontown.suit.SuitAnimationIndex import AllSuits, AllSuitsMinigame, AllSuitsTutorialBattle, AllSuitsBattle, ExtraSuitAnims
        self.items = list(map(lambda x: x[0], list(AllSuits) + list(AllSuitsMinigame) + list(AllSuitsTutorialBattle) +
                              list(AllSuitsBattle) + list(ExtraSuitAnims)))

        self.selectedIndex = self.subevent[kwarg]
        if "'" in self.selectedIndex:
            # no apostrophies pwease
            self.selectedIndex = self.selectedIndex[1:-1]
        optiondefs = (
            ('initialitem', self.items.index(self.selectedIndex), None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownSuitAnims)

        self.textLabel = DirectFrame(
            parent=self, text='Suit Anim', text_scale=1.1,
            text_pos=(-2.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedIndex = self.items.index(newText)

    def getAdjusterValue(self):
        return self.items[self.selectedIndex]


class DropdownSuitHeadAnims(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for suit head anims.
    Enum: dropdown_suit_head_anims
    """

    textLength = 30
    height = 0.1
    offset = (-0.1, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        from toontown.suit.SuitAnimationIndex import ExtraSuitHeadAnims
        from toontown.suit.heads.AnimatedSuitHead import AllSuitHeads, AllSuitBattleHeads
        self.items = list(map(lambda x: x[0], list(AllSuitHeads) + list(AllSuitBattleHeads) + list(ExtraSuitHeadAnims)))

        self.selectedIndex = self.subevent[kwarg]
        if "'" in self.selectedIndex:
            # no apostrophies pwease
            self.selectedIndex = self.selectedIndex[1:-1]
        optiondefs = (
            ('initialitem', self.items.index(self.selectedIndex), None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownSuitHeadAnims)

        self.textLabel = DirectFrame(
            parent=self, text='Suit Head Anim', text_scale=1.1,
            text_pos=(-2.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedIndex = self.items.index(newText)

    def getAdjusterValue(self):
        return self.items[self.selectedIndex]


class DropdownBossAnims(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for boss anims.
    Enum: dropdown_boss_anims
    """

    textLength = 30
    height = 0.1
    offset = (-0.1, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        from toontown.suit.BossCog import AnimList
        self.items = list(map(lambda x: x[0], list(AnimList)))

        self.selectedIndex = self.subevent[kwarg]
        if "'" in self.selectedIndex:
            # no apostrophies pwease
            self.selectedIndex = self.selectedIndex[1:-1]
        optiondefs = (
            ('initialitem', self.items.index(self.selectedIndex), None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownBossAnims)

        self.textLabel = DirectFrame(
            parent=self, text='Boss Anim', text_scale=1.1,
            text_pos=(-2.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedIndex = self.items.index(newText)

    def getAdjusterValue(self):
        return self.items[self.selectedIndex]


class DropdownNode(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for nodes.
    Enum: dropdown_node
    """

    textLength = 30
    height = 0.1
    offset = (-0.3, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        self.items = cutsceneDict['nodes'][:]

        self.itemIndexDict = {}

        for i, item in enumerate(self.items):
            if item is None:
                continue
            if hasattr(item, 'getName'):
                self.items[i] = str(item.getName().replace('\n', '-')) + f'-{i}'
            else:
                self.items[i] = str(type(item).__name__.replace('\n', '-')) + f'-{i}'
            self.itemIndexDict[self.items[i]] = i

        self.selectedIndex = self.subevent[kwarg]
        optiondefs = (
            ('initialitem', self.selectedIndex, None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownNode)

        self.textLabel = DirectFrame(
            parent=self, text='Nodes', text_scale=1.1,
            text_pos=(-2.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedIndex = self.itemIndexDict[newText]

    def getAdjusterValue(self):
        return self.selectedIndex


class DropdownFunction(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for functions.
    Enum: dropdown_function
    """

    textLength = 30
    height = 0.1
    offset = (-0.3, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        self.items = cutsceneDict['functions'][:]

        self.itemIndexDict = {}

        for i, item in enumerate(self.items):
            if item is None:
                continue
            self.items[i] = f'{item.__name__}-{i}'
            self.itemIndexDict[self.items[i]] = i

        self.selectedIndex = self.subevent[kwarg]
        optiondefs = (
            ('initialitem', self.selectedIndex, None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownFunction)

        self.textLabel = DirectFrame(
            parent=self, text='Functions', text_scale=1.1,
            text_pos=(-2.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedIndex = self.itemIndexDict[newText]

    def getAdjusterValue(self):
        return self.selectedIndex


class DropdownElevators(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for elevators.
    Enum: dropdown_elevators
    """

    textLength = 30
    height = 0.1
    offset = (-0.3, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        self.items = cutsceneDict.get('elevators', [])[:]

        self.itemIndexDict = {}

        for i, item in enumerate(self.items):
            if item is None:
                continue
            if hasattr(item, 'getName'):
                self.items[i] = str(item.getName()) + f'-{i}'
            else:
                self.items[i] = str(type(item).__name__) + f'-{i}'
            self.itemIndexDict[self.items[i]] = i

        self.selectedIndex = self.subevent[kwarg]
        optiondefs = (
            ('initialitem', self.selectedIndex, None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownElevators)

        self.textLabel = DirectFrame(
            parent=self, text='Elevators', text_scale=1.1,
            text_pos=(-2.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedIndex = self.itemIndexDict[newText]

    def getAdjusterValue(self):
        return self.selectedIndex


class DropdownBlendType(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for blend types.
    Enum: dropdown_blendType
    """

    textLength = 30
    height = 0.1
    offset = (-0.1, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        self.items = ['easeIn', 'easeOut', 'easeInOut', 'noBlend']

        self.selectedText = self.subevent[kwarg]
        self.selectedIndex = self.items.index(self.selectedText)
        optiondefs = (
            ('initialitem', self.selectedIndex, None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownBlendType)

        self.textLabel = DirectFrame(
            parent=self, text='Blend', text_scale=1.1,
            text_pos=(-2.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedText = newText

    def getAdjusterValue(self):
        return self.selectedText


class DropdownBlockShape(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for toon block congregation shapes.
    Enum: dropdown_blockShape
    """

    textLength = 30
    height = 0.1
    offset = (-0.1, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        self.items = [name for name, member in ToonBlockShape.__members__.items()]

        self.selectedText = self.subevent[kwarg]
        self.selectedIndex = self.items.index(self.selectedText)
        optiondefs = (
            ('initialitem', self.selectedIndex, None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownBlockShape)

        self.textLabel = DirectFrame(
            parent=self, text='Block Shape', text_scale=1.1,
            text_pos=(-3.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedText = newText

    def getAdjusterValue(self):
        return self.selectedText


class DropdownTargetGroup(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for the target group of a given SubEvent.
    Enum: dropdown_targetGroup
    """

    textLength = 30
    height = 0.1
    offset = (-0.1, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        self.items = [name for name, member in ToonSubEventTargetGroup.__members__.items()]

        self.selectedText = self.subevent[kwarg]
        self.selectedIndex = self.items.index(self.selectedText)
        optiondefs = (
            ('initialitem', self.selectedIndex, None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownTargetGroup)

        self.textLabel = DirectFrame(
            parent=self, text='Target', text_scale=1.1,
            text_pos=(-3.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedText = newText

    def getAdjusterValue(self):
        return self.selectedText


class DropdownParticles(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for particles.
    Enum: dropdown_particles
    """

    textLength = 30
    height = 0.1
    offset = (-0.3, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        self.items = cutsceneDict['particles'][:]

        self.itemIndexDict = {}

        for i, item in enumerate(self.items):
            if item is None:
                continue
            if hasattr(item, 'getName'):
                self.items[i] = str(item.getName().replace('\n', '-')) + f'-{i}'
            else:
                self.items[i] = str(type(item).__name__.replace('\n', '-')) + f'-{i}'
            self.itemIndexDict[self.items[i]] = i

        self.selectedIndex = self.subevent[kwarg]
        optiondefs = (
            ('initialitem', self.selectedIndex, None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownParticles)

        self.textLabel = DirectFrame(
            parent=self, text='Particles', text_scale=1.1,
            text_pos=(-2.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedIndex = self.itemIndexDict[newText]

    def getAdjusterValue(self):
        return self.selectedIndex


class DropdownArguments(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for arguments.
    Enum: dropdown_arguments
    """

    textLength = 30
    height = 0.1
    offset = (-0.3, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        self.items = cutsceneDict['arguments'][:] if 'arguments' in cutsceneDict else []

        self.itemIndexDict = {}

        for i, item in enumerate(self.items):
            if item is None:
                continue
            if isinstance(item, str):
                self.items[i] = f'arg{i}: ' + item
            elif hasattr(item, 'getName'):
                self.items[i] = f'arg{i}: ' + str(item.getName())
            else:
                self.items[i] = f'arg{i}: ' + str(type(item).__name__)
            self.itemIndexDict[self.items[i]] = i

        self.selectedIndex = self.subevent[kwarg]
        optiondefs = (
            ('initialitem', self.selectedIndex, None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownArguments)

        self.textLabel = DirectFrame(
            parent=self, text='Arguments', text_scale=1.1,
            text_pos=(-2.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedIndex = self.itemIndexDict[newText]

    def getAdjusterValue(self):
        return self.selectedIndex


class DropdownSuitFlyChoice(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for the type of suit Supa Fly.
    Enum: dropdown_suitFlyChoice
    """

    textLength = 30
    height = 0.1
    offset = (-0.1, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        self.items = ['None', 'flyOut', 'flyIn', 'flyInQuick']

        self.selectedIndex = self.subevent[kwarg]

        optiondefs = (
            ('initialitem', self.selectedIndex, None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownSuitFlyChoice)

        self.textLabel = DirectFrame(
            parent=self, text='Fly Type', text_scale=1.1,
            text_pos=(-3.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedIndex = self.items.index(newText)

    def getAdjusterValue(self):
        return self.selectedIndex


class DropdownSuitFlyPosChoice(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for if suit Supa fly should get pos.
    Enum: dropdown_suitFlyPosChoice
    """

    textLength = 30
    height = 0.1
    offset = (-0.1, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        self.items = ['False', 'True']

        self.selectedIndex = self.subevent[kwarg]

        optiondefs = (
            ('initialitem', self.selectedIndex, None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownSuitFlyPosChoice)

        self.textLabel = DirectFrame(
            parent=self, text='Get Pos', text_scale=1.1,
            text_pos=(-3.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedIndex = self.items.index(newText)

    def getAdjusterValue(self):
        return self.selectedIndex

class DropdownSoundEffects(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for sounds effects.
    Enum: dropdown_sound_effects
    """

    textLength = 30
    height = 0.2
    offset = (-0.1, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        self.items = cutsceneDict['sounds'][:] if 'sounds' in cutsceneDict else []

        self.itemIndexDict = {}

        for i, item in enumerate(self.items):
            if item is None:
                continue
            if hasattr(item, 'getName'):
                name = str(item.getName())
                self.items[i] = f'{name}-{i}'
            self.itemIndexDict[self.items[i]] = i

        self.selectedIndex = self.subevent[kwarg]
        optiondefs = (
            ('initialitem', self.selectedIndex, None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownSoundEffects)

        self.textLabel = DirectFrame(
            parent=self, text='Sounds', text_scale=1.1,
            text_pos=(-2.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedIndex = self.itemIndexDict[newText]

    def getAdjusterValue(self):
        return self.selectedIndex


class DropdownMusic(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for music.
    Enum: dropdown_music
    """

    textLength = 30
    height = 0.2
    offset = (-0.1, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        self.items = cutsceneDict['music'][:] if 'music' in cutsceneDict else []

        self.itemIndexDict = {}

        for i, item in enumerate(self.items):
            if item is None:
                continue
            self.items[i] = f'{self.items[i]}-{i}'
            self.itemIndexDict[self.items[i]] = i

        self.selectedIndex = self.subevent[kwarg]
        optiondefs = (
            ('initialitem', self.selectedIndex, None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownMusic)

        self.textLabel = DirectFrame(
            parent=self, text='Music', text_scale=1.1,
            text_pos=(-2.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedIndex = self.itemIndexDict[newText]

    def getAdjusterValue(self):
        return self.selectedIndex


class DropdownFogType(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for toon block congregation shapes.
    Enum: dropdown_fogType
    """

    textLength = 30
    height = 0.1
    offset = (-0.1, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        self.items = ['Exponential', 'ExponentialSquared', 'Linear']
        self.selectedText = self.subevent[kwarg]
        self.selectedIndex = self.items.index(self.selectedText)
        optiondefs = (
            ('initialitem', self.selectedIndex, None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownFogType)

        self.textLabel = DirectFrame(
            parent=self, text='Fog Type', text_scale=1.1,
            text_pos=(-3.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedText = newText

    def getAdjusterValue(self):
        return self.selectedText


class DropdownToonExpression(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for toon block congregation shapes.
    Enum: dropdown_toonExpression
    """

    textLength = 30
    height = 0.1
    offset = (-0.1, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        self.items = ['normal', 'angry', 'sad', 'smile', 'laugh', 'surprise']
        self.selectedText = self.subevent[kwarg]
        self.selectedIndex = self.items.index(self.selectedText)
        optiondefs = (
            ('initialitem', self.selectedIndex, None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownToonExpression)

        self.textLabel = DirectFrame(
            parent=self, text='Toon Expression', text_scale=1.1,
            text_pos=(-3.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedText = newText

    def getAdjusterValue(self):
        return self.selectedText


class DropdownToonEyes(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for toon block congregation shapes.
    Enum: dropdown_toonEyes
    """

    textLength = 30
    height = 0.1
    offset = (-0.1, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        self.items = ['normal', 'angry', 'sad', 'surprise']
        self.selectedText = self.subevent[kwarg]
        self.selectedIndex = self.items.index(self.selectedText)
        optiondefs = (
            ('initialitem', self.selectedIndex, None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownToonEyes)

        self.textLabel = DirectFrame(
            parent=self, text='Toon Eyes', text_scale=1.1,
            text_pos=(-3.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedText = newText

    def getAdjusterValue(self):
        return self.selectedText


class DropdownToonSpecies(CSPanelAdjusterBase, DirectScrollableOptionMenu):
    """
    A dropdown panel for toon block congregation shapes.
    Enum: dropdown_toonSpecies
    """

    textLength = 30
    height = 0.1
    offset = (-0.1, 0, 0.1)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)

        from toontown.toon import ToonDNA
        self.items = ToonDNA.toonSpeciesTypes
        self.selectedText = self.subevent[kwarg]
        self.selectedIndex = self.items.index(self.selectedText)
        optiondefs = (
            ('initialitem', self.selectedIndex, None),
            ('items', self.items[:], None),
            ('command', self.requestText, None),
            ('scale', 0.05, None),
        )
        self.defineoptions(kw, optiondefs)
        DirectScrollableOptionMenu.__init__(self, parent, **kw)
        self.initialiseoptions(DropdownToonSpecies)

        self.textLabel = DirectFrame(
            parent=self, text='Toon Species', text_scale=1.1,
            text_pos=(-3.5, -0.01), frameColor=(0, 0, 0, 0),
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def requestText(self, newText):
        if newText in self.items:
            self.selectedText = newText

    def getAdjusterValue(self):
        return self.selectedText


class BooleanType(CSPanelAdjusterBase, DirectFrame):
    """
    A checkbox, essentially.
    Enum: boolean
    """

    height = 0.1
    offset = (-0.1, 0, 0.12)

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        optiondefs = (
            ('frameColor', (0, 0, 0, 0), None),
        )
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)
        self.initialiseoptions(BooleanType)

        self.checkbox = CheckboxButton(
            parent=self, callback=None,
            labelText=self.eventArgument.name,
            pos=(0, 0, 0),
        )
        self.checkbox.setCheck(self.subevent[kwarg])

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.checkbox)
        scrollWheelFrame.bindToScroll(self.checkbox.label)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def getAdjusterValue(self):
        return bool(self.checkbox.checked)


class SliderXYZScale(CSPanelAdjusterBase, DirectFrame):
    """
    A XYZ slider scale, used for adjustments in 3D space from 0 to 1.
    Enum: slider_xyz_scale
    """

    height = 0.4

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        optiondefs = (
            ('frameColor', (0, 0, 0, 0), None),
        )
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)
        self.initialiseoptions(SliderXYZScale)

        self.sizerNode = DirectFrame(
            parent=self, frameColor=(0, 0, 0, 0), pos=(-0.1, 0, 0),
        )
        self.sizer = SizerFrame(
            self.sizerNode, self.eventArgument.name, 'xyz', self.subevent[kwarg], (0.001, 1)
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.sizerNode)
        self.sizer.bindScroll(scrollWheelFrame=scrollWheelFrame)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def getAdjusterValue(self):
        return self.sizer.getValues()


class SliderXYZNode(CSPanelAdjusterBase, DirectFrame):
    """
    A XYZ slider, used for adjustments in 3D space.
    Updates with the node.
    Enum: slider_xyz_node
    """

    height = 0.4

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        optiondefs = (
            ('frameColor', (0, 0, 0, 0), None),
        )
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)
        self.initialiseoptions(SliderXYZNode)

        self.nodeRef = subevent.kwargs.get('nodeIndex')
        if self.nodeRef is None:
            raise AttributeError("Subevent definition must have nodeIndex key!")
        self.nodeRef = cutsceneDict['nodes'][self.nodeRef]

        self.sizerNode = DirectFrame(
            parent=self, frameColor=(0, 0, 0, 0), pos=(-0.1, 0, 0),
        )
        self.sizer = SizerFrame(
            self.sizerNode, self.eventArgument.name, 'xyz', self.subevent[kwarg], (-20, 20)
        )

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.sizerNode)
        self.sizer.bindScroll(scrollWheelFrame=scrollWheelFrame)

    def destroy(self):
        self.nodeRef = None
        self.destroy_base()
        super().destroy()

    def getAdjusterValue(self):
        return self.sizer.getValues()

    def onNewSubevent(self):
        pos = self.nodeRef.getPos()
        self.sizer.setValues(newValues=pos, doCallback=False)

    def onKwargUpdate(self, key, val):
        """Called on all sliders when a kwarg updates."""
        if key == 'nodeIndex':
            self.nodeRef = self.cutsceneDict['nodes'][val]
            self.onNewSubevent()


class SliderHPRNode(CSPanelAdjusterBase, DirectFrame):
    """
    A HPR slider, used for rotations in 3D space.
    Updates with the node.
    Enum: slider_hpr_node
    """

    height = 0.4
    ObjectTypeKey = 'nodes'
    ObjectIndexTypeKey = 'nodeIndex'

    def __init__(self, parent, subevent, kwarg, cutsceneDict, **kw):
        optiondefs = (
            ('frameColor', (0, 0, 0, 0), None),
        )
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        CSPanelAdjusterBase.__init__(self, subevent, kwarg, cutsceneDict)
        self.initialiseoptions(SliderHPRNode)

        self.setNodeRef(subevent, kwarg, cutsceneDict)

        self.sizerNode = DirectFrame(
            parent=self, frameColor=(0, 0, 0, 0), pos=(-0.1, 0, 0),
        )
        self.sizer = SizerFrame(
            self.sizerNode, self.eventArgument.name, 'hpr', self.subevent[kwarg], (-360, 360)
        )

    def setNodeRef(self, subevent, kwarg, cutsceneDict):
        self.nodeRef = subevent.kwargs.get(self.ObjectIndexTypeKey)
        if self.nodeRef is None:
            raise AttributeError(f"Subevent definition must have {self.ObjectIndexTypeKey} key!")
        self.nodeRef = cutsceneDict[self.ObjectTypeKey][self.nodeRef]

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.sizerNode)
        self.sizer.bindScroll(scrollWheelFrame=scrollWheelFrame)

    def destroy(self):
        self.destroy_base()
        super().destroy()

    def getAdjusterValue(self):
        return self.sizer.getValues()

    def onNewSubevent(self):
        hpr = self.nodeRef.getHpr()
        self.sizer.setValues(newValues=hpr, doCallback=False)

    def onKwargUpdate(self, key, val):
        """Called on all sliders when a kwarg updates."""
        if key == self.ObjectIndexTypeKey:
            self.nodeRef = self.cutsceneDict[self.ObjectTypeKey][val]
            self.onNewSubevent()


class SliderHPRToon(SliderHPRNode, CSPanelAdjusterBase):
    """
    A HPR slider, used for rotations in 3D space.
    Updates with the suit.
    Enum: slider_hpr_toon
    """
    ObjectTypeKey = 'toons'
    ObjectIndexTypeKey = 'toonIndex'


class SliderHPRSuit(SliderHPRNode, CSPanelAdjusterBase):
    """
    A HPR slider, used for rotations in 3D space.
    Updates with the suit.
    Enum: slider_hpr_suit
    """
    ObjectTypeKey = 'suits'
    ObjectIndexTypeKey = 'suitIndex'


for adjuster in CSPanelAdjusterBase.__subclasses__():
    methodEnum = SubEventArgumentType[getEnumFromDocstring(adjuster.__doc__)]
    CSPanelAdjusters[methodEnum] = adjuster
