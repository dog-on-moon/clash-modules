"""
The GUI panel manager for the Event Panel.

"""
from panda3d.core import TextNode
import direct.gui.DirectGuiGlobals as DGG
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectFrame import DirectFrame


from toontown.gui.TTGui import CheckboxButton, ScrollWheelFrame
from toontown.cutscene.editor.CSEditorClasses import Event
from toontown.cutscene.editor.CSEditorDefs import orderedEventDefinitionList
from toontown.cutscene.editor.CSEditorEnums import EventSequenceMode
from toontown.utils.ColorHelper import hexToPCol
from toontown.utils.text import wordwrapWithVerticalCentering

subeventFrameColor = {
    'ToonSequence': hexToPCol('b3fffa'),
    'SuitSequence': hexToPCol('b19f9d'),
    'CameraSequence': hexToPCol('fff4b3'),
    'GeneralSequence': hexToPCol('bfc1ff'),
    'AudioSequence': hexToPCol('44923b'),
    'ParticleSequence': hexToPCol('ffb3f8'),
    'CogBattleSequence': hexToPCol('ffaa82'),
    'GUISequence': hexToPCol('6865FF'),
    'EnvironmentSequence': hexToPCol('CBFF56'),
    'ToonExpressionSequence': hexToPCol('FF5458'),
}
defaultFrameColor = (0.9, 0.9, 0.9, 0.9)


class CSPanelEvent(DirectFrame):

    frameColor = (0.8, 0.8, 0.8, 0.3)

    def __init__(self, mgr, **kw):
        optiondefs = (
            ('frameColor', self.frameColor, None),
            ('frameSize', (0, 0.8, 0, 1.5), None),
        )
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, base.a2dBottomLeft, **kw)
        self.initialiseoptions(CSPanelEvent)

        # set properties of panel
        self.mgr = mgr  # type: CSEditorManager
        self.event = None

        # get name label
        self.entry_name = DirectEntry(
            parent=self, command=self.event_updateName,
            initialText='Select an event.', width=10, numLines=1,
            scale=.05, pos=(0.02, 0, 1.43), frameColor=self.frameColor,
        )

        self.entry_time = DirectEntry(
            parent=self, command=self.event_updateTime,
            initialText='0.0', width=3, numLines=1,
            scale=.05, pos=(0.55, 0, 1.43), frameColor=self.frameColor,
        )

        # sequence flavor label
        self.checkbox_sequence = CheckboxButton(
            parent=self, callback=self.event_setSequenceMode,
            extraArgs=[EventSequenceMode.Sequence], labelText='Ordered',
            pos=(0.05, 0, 1.37),
        )
        self.checkbox_parallel = CheckboxButton(
            parent=self, callback=self.event_setSequenceMode,
            extraArgs=[EventSequenceMode.Parallel], labelText='Simultaneous',
            pos=(0.45, 0, 1.37),
        )
        self.checkboxes = [self.checkbox_sequence, self.checkbox_parallel]
        self.checkbox_sequence.setBoundCheckboxes(self.checkboxes)
        self.checkbox_parallel.setBoundCheckboxes(self.checkboxes)

        # delete event
        self.button_delete = DirectButton(
            parent=self, command=self.event_delete,
            frameSize=(-0.03, 0.03, -0.03, 0.03),
            frameColor=(0.765, 0.765, 0.765, 1.0),
            text='x', text_scale=0.06, text_pos=(0, -0.01),
            pos=(0.75, 0, 1.45),
        )

        # event jump buttons
        self.button_goLeft = DirectButton(
            parent=self, command=self.mgr.jumpEvent, extraArgs=[1],
            frameSize=(-0.06, 0.06, -0.06, 0.06),
            frameColor=(0.765, 0.765, 0.765, 1.0),
            text='<<', text_scale=0.06, text_pos=(0, -0.01),
            pos=(0.08, 0, 1.6),
        )
        self.button_goRight = DirectButton(
            parent=self, command=self.mgr.jumpEvent, extraArgs=[-1],
            frameSize=(-0.06, 0.06, -0.06, 0.06),
            frameColor=(0.765, 0.765, 0.765, 1.0),
            text='>>', text_scale=0.06, text_pos=(0, -0.01),
            pos=(0.38, 0, 1.6),
        )

        # create event
        self.button_eventCreate = DirectButton(
            parent=self, command=self.mgr.addNewEvent,
            frameSize=(-0.06, 0.06, -0.06, 0.06),
            frameColor=(0.765, 0.765, 0.765, 1.0),
            text='+', text_scale=0.06, text_pos=(0, -0.01),
            pos=(0.23, 0, 1.6),
        )

        # get direct scrolled list for subevents
        self.scroll_subevents = ScrollWheelFrame(
            parent=self,
            pos=(0.02, 0, 1.32),
            canvasSize=(0, 0.68, -2 - 1.31, 0),
            frameSize=(0, 0.76, 0.14 - 1.31, 0),
            frameColor=(0.396, 0.396, 0.396, 0.3),
        )
        self.subevents = []

        self.scroll_subevent_types = ScrollWheelFrame(
            parent=self,
            pos=(0.02, 0, 1.32),
            canvasSize=(0, 0.68, -2 - 1.31, 0),
            frameSize=(0, 0.76, 0.14 - 1.31, 0),
            frameColor=(0.396, 0.396, 0.396, 0.3),
        )
        self.subevent_types = []

        # self.scroll_subevents.hide()
        self.scroll_subevent_types.hide()
        self.viewSubevents = True

        # create event
        self.button_addSubevent = DirectButton(
            parent=self, command=self.changeSubeventMode,
            frameSize=(-0.26, 0.26, -0.06, 0.06),
            frameColor=(0.765, 0.765, 0.765, 1.0),
            text='Add Subevent', text_scale=0.06, text_pos=(0, -0.01),
            pos=(0.4, 0, 0.075),
        )

        # fill out subevent types
        self.updateSubeventTypes()

        # start accepting update call
        self.accept("selectEvent", self.update)
        self.accept('updateTrack', self.update)
        self.accept('createSubevent', self.changeSubeventMode, extraArgs=[None])

    """
    Switch Scrollbar
    """

    def changeSubeventMode(self, force=None, *_):
        if type(force) is not bool:
            self.viewSubevents = not self.viewSubevents
        else:
            self.viewSubevents = force
        if self.viewSubevents:
            # we are viewing the subevents !!
            self.updateSubEvents(self.event)
            self.scroll_subevents.show()
            self.scroll_subevent_types.hide()
        else:
            self.scroll_subevents.hide()
            self.scroll_subevent_types.show()

    """
    Misc Buttons
    """

    def event_delete(self):
        if self.event is None:
            return
        messenger.send('requestEventDelete', [self.event])

    """
    Sequence Settings
    """

    def event_setSequenceMode(self, _, sequenceMode: EventSequenceMode):
        if self.event is None:
            return
        self.event.setSequenceMode(sequenceMode)
        messenger.send('updateTrack')

    def event_updateTime(self, timeStr):
        if self.event is None:
            return
        try:
            float(timeStr)
        except TypeError:
            return
        self.event.setTime(float(timeStr))
        messenger.send('updateTrack')
        messenger.send('updateEvents')

    """
    Name Setting
    """

    def event_updateName(self, newName: str):
        """
        Updates the selected event with a new name.
        """
        if self.event is None:
            return
        self.event.setName(newName)

    """
    Update Methods
    """

    def update(self, event: Event = None):
        if event is None:
            if self.event is None:
                return
            event = self.event
        self.event = event
        self.entry_name.set(event.getName())
        self.entry_time.set(str(event.getTime()))
        for checkbox in self.checkboxes:
            checkbox.setCheck(False)
        if event.getSequenceMode() == EventSequenceMode.Sequence:
            self.checkbox_sequence.setCheck(True)
        elif event.getSequenceMode() == EventSequenceMode.Parallel:
            self.checkbox_parallel.setCheck(True)
        self.changeSubeventMode(force=True)

    def updateSubEvents(self, event: Event):
        # clear subevent list
        for subevent in self.subevents:
            subevent.destroy()
        self.subevents = []
        # create subevent buttons
        for i, subevent in enumerate(event.getSubEvents()):
            newButton = SubeventButton(
                parent=self.scroll_subevents.getCanvas(),
                index=i, event=event, subevent=subevent
            )
            newButton.bindTo(self.scroll_subevents)
            self.subevents.append(newButton)
        # update canvas height
        lowestHeight = self.scroll_subevents['frameSize'][2] - 0.00001
        proposedHeight = 0.14 - ((SubeventButton.border + SubeventButton.height) * (1 + len(self.subevents)))
        x, y, _, v = self.scroll_subevents['canvasSize']
        self.scroll_subevents['canvasSize'] = (x, y, min(lowestHeight, proposedHeight), v)
        self.scroll_subevents.setCanvasSize()

    def updateSubeventTypes(self):
        # clear subevent list
        for subevent in self.subevent_types:
            subevent.destroy()
        self.subevent_types = []
        # create subevent buttons
        for i, seType in enumerate(orderedEventDefinitionList):
            if type(seType) is str:
                # this is an event type label
                newButton = SubeventTypeLabel(
                    parent=self.scroll_subevent_types.getCanvas(),
                    index=i, name=seType
                )
                newButton.bindTo(self.scroll_subevent_types)
                self.subevent_types.append(newButton)
            else:
                # subevent type button label
                newButton = SubeventTypeButton(
                    parent=self.scroll_subevent_types.getCanvas(),
                    index=i, eventDefinition=seType
                )
                newButton.bindTo(self.scroll_subevent_types)
                self.subevent_types.append(newButton)
        # update canvas height
        lowestHeight = self.scroll_subevent_types['frameSize'][2] - 0.00001
        proposedHeight = 0.14 - ((SubeventButton.border + SubeventButton.height) * (1 + len(self.subevent_types)))
        x, y, _, v = self.scroll_subevent_types['canvasSize']
        self.scroll_subevent_types['canvasSize'] = (x, y, min(lowestHeight, proposedHeight), v)
        self.scroll_subevent_types.setCanvasSize()


class SubeventButton(DirectFrame):

    canvas_width = 0.68
    border = 0.015
    height = 0.15
    buttonSize = 0.05
    buttonBorder = 0.01

    def __init__(self, parent, index, event, subevent, **kw):
        optiondefs = (
            ('frameColor', subeventFrameColor.get(subevent.eventDef.category, defaultFrameColor), None),
            ('frameSize', (self.border, self.canvas_width-self.border, -self.height, 0), None),
            ('pos', (0, 0, -self.border - index * (self.height + self.border)), None),
        )
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        self.initialiseoptions(SubeventButton)

        self['state'] = DGG.NORMAL
        self.bind(DGG.B1PRESS, self.selectSubevent)

        self.textLabel = DirectFrame(
            parent=self,
            pos=(0.10, 0, -(self.height / 2) - self.border),
            text=subevent.name,
            text_scale=0.04,
            text_wordwrap=12,
            text_align=TextNode.ALeft,
            frameColor=(0,0,0,0),
        )
        wordwrapWithVerticalCentering(label=self.textLabel, wordwrapValue=12)

        # delete subevent
        blength = self.buttonSize / 2
        self.button_delete = DirectButton(
            parent=self, command=self.removeSubevent,
            frameSize=(-blength, blength, -blength, blength),
            frameColor=(0.765, 0.765, 0.765, 1.0),
            text='x', text_scale=0.06, text_pos=(0, -0.01),
            pos=(self.canvas_width - self.border - blength - self.buttonBorder, 0, -blength - self.buttonBorder),
        )

        # extract subevent into a new event
        self.button_extract = DirectButton(
            parent=self, command=self.extractSubevent,
            frameSize=(-blength, blength, -blength, blength),
            frameColor=(0.765, 0.765, 0.765, 1.0),
            text='>', text_scale=0.06, text_pos=(0, -0.01),
            pos=(self.canvas_width - self.border - blength - self.buttonBorder, 0, -self.height + blength + self.buttonBorder),
        )

        # button reordering
        self.button_moveUp = DirectButton(
            parent=self, command=self.moveSubevent, extraArgs=[-1],
            frameSize=(-blength, blength, -blength, blength),
            frameColor=(0.765, 0.765, 0.765, 1.0),
            text='v', text_scale=-0.06, text_pos=(0, 0.01),
            pos=(self.border + blength + self.buttonBorder, 0, -blength - self.buttonBorder),
        )
        self.button_moveDown = DirectButton(
            parent=self, command=self.moveSubevent, extraArgs=[1],
            frameSize=(-blength, blength, -blength, blength),
            frameColor=(0.765, 0.765, 0.765, 1.0),
            text='v', text_scale=0.06, text_pos=(0, -0.01),
            pos=(self.border + blength + self.buttonBorder, 0, -self.height + blength + self.buttonBorder),
        )

        # set event properties
        self.event = event
        self.subevent = subevent

    def selectSubevent(self, _=None):
        messenger.send('requestSelectSubevent', [self.subevent])

    def moveSubevent(self, direction):
        """
        Moves this subevent.
        """
        self.event.moveSubEvent(subEvent=self.subevent, direction=direction)

    def removeSubevent(self):
        """
        Removes this subevent.
        """
        self.event.removeSubEvent(self.subevent)
        messenger.send('updateTrack')

    def extractSubevent(self):
        """
        Extracts this subevent into a new event.
        """
        messenger.send('requestCreateEvent', [[self.subevent]])
        self.event.removeSubEvent(self.subevent)
        messenger.send('updateTrack')

    def bindTo(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this GUI to the scroll wheel frame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)
        scrollWheelFrame.bindToScroll(self.button_delete)
        scrollWheelFrame.bindToScroll(self.button_moveUp)
        scrollWheelFrame.bindToScroll(self.button_moveDown)


class SubeventTypeButton(DirectFrame):

    canvas_width = 0.68
    border = 0.015
    height = 0.15
    buttonSize = 0.05
    buttonBorder = 0.01

    def __init__(self, parent, index, eventDefinition, **kw):
        optiondefs = (
            ('frameColor', subeventFrameColor.get(eventDefinition.category, defaultFrameColor), None),
            ('frameSize', (self.border, self.canvas_width-self.border, -self.height, 0), None),
            ('pos', (0, 0, -self.border - index * (self.height + self.border)), None),
        )
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        self.initialiseoptions(SubeventTypeButton)

        self['state'] = DGG.NORMAL
        self.bind(DGG.B1PRESS, self.createSubevent)

        self.eventDef = eventDefinition

        self.textLabel = DirectFrame(
            parent=self,
            pos=((self.canvas_width / 2), 0, -(self.height / 2) - self.border),
            text=eventDefinition.name,
            text_scale=0.045,
            text_wordwrap=12,
            frameColor=(0,0,0,0),
        )
        wordwrapWithVerticalCentering(label=self.textLabel, wordwrapValue=12)

    def createSubevent(self, _=None):
        messenger.send('requestCreateSubevent', [self.eventDef.enum])

    def bindTo(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this GUI to the scroll wheel frame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)


class SubeventTypeLabel(DirectFrame):
    frameColor = (0.3, 0.3, 0.3, 0.1)

    canvas_width = 0.68
    border = 0.015
    height = 0.15
    buttonSize = 0.05
    buttonBorder = 0.01

    def __init__(self, parent, index, name, **kw):
        optiondefs = (
            ('frameColor', self.frameColor, None),
            ('frameSize', (self.border, self.canvas_width-self.border, -self.height, 0), None),
            ('pos', (0, 0, -self.border - index * (self.height + self.border)), None),
        )
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        self.initialiseoptions(SubeventTypeLabel)

        self.textLabel = DirectFrame(
            parent=self,
            pos=((self.canvas_width / 2), 0, -(self.height / 2) - self.border),
            text=name,
            text_scale=0.06,
            text_wordwrap=12,
            text_shadow=(0, 0, 0, 1),
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
        )
        wordwrapWithVerticalCentering(label=self.textLabel, wordwrapValue=12)

    def bindTo(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this GUI to the scroll wheel frame.
        """
        scrollWheelFrame.bindToScroll(self)
        scrollWheelFrame.bindToScroll(self.textLabel)

