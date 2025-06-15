"""
The GUI panel manager for the sequence timer bar.
"""
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectFrame import DirectFrame
import direct.gui.DirectGuiGlobals as DGG

from toontown.cutscene.editor.CSEditorEnums import PauseFlags


class CSPanelPlayer(DirectFrame):

    tl_width = 2.0
    tl_marker_size = 0.3

    def __init__(self, mgr, **kw):
        optiondefs = ()
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, aspect2d, **kw)
        self.initialiseoptions(CSPanelPlayer)

        self.mgr = mgr  # type: CSEditorManager

        # The second and duration labels at the top.

        self.entry_secondLabel = DirectEntry(
            parent=base.a2dTopLeft, command=self.enterTime,
            initialText='0.0', width=4, numLines=1, scale=.05,
            pos=(0.01, 0, -0.06),
            frameColor=(0.8, 0.8, 0.8, 0.3),
            focusInCommand=self.setUpdateSecondMode, focusInExtraArgs=[False],
            focusOutCommand=self.setUpdateSecondMode, focusOutExtraArgs=[True],
        )
        self.entry_durationLabel = DirectEntry(
            parent=base.a2dTopRight, command=self.enterDuration,
            initialText=str(round(self.mgr.trackLength)), width=4, numLines=1, scale=.05,
            pos=(-0.21, 0, -0.06), frameColor=(0.8, 0.8, 0.8, 0.3),
        )
        self.updateSecond = True

        taskMgr.add(self.updateTimeEntry, 'cspanelplayer-updateTime')
        self.accept('updateDuration', self.updateDuration)

        # The cutscene progress bar at the top.

        self.frame_progressBar = DirectFrame(
            parent=aspect2d, pos=(0, 0, 0.95),
            frameSize=(-self.tl_width / 2, self.tl_width / 2, -0.025, 0.025),
            frameColor=(0.184, 0.192, 0.212, 1.0),
        )

        self.frame_progressMarker = DirectFrame(
            parent=self.frame_progressBar, pos=((-self.tl_width / 2)-(-self.tl_width / (200 / self.tl_marker_size)), 0, 0),
            frameSize=(-self.tl_width / (200 / self.tl_marker_size), self.tl_width / (200 / self.tl_marker_size), -0.025, 0.025),
            frameColor=(0.973, 0.953, 0.784, 1.0),
        )

        self.timelineState = False

        self.frame_progressBar.bind(DGG.B1PRESS, self.setTimelineState, extraArgs=[True])
        self.frame_progressMarker.bind(DGG.B1PRESS, self.setTimelineState, extraArgs=[True])
        self.frame_progressBar['state'] = DGG.NORMAL
        self.frame_progressMarker['state'] = DGG.NORMAL
        self.accept('mouse1-up', self.setTimelineState, extraArgs=[False])

        taskMgr.add(self.updateTimeline, 'cspanelplayer-updateTimeline')

        # Pause button

        self.button_pause = DirectButton(
            parent=base.a2dTopLeft, command=self.swapPauseStatus,
            text="=", text_scale=0.06, text_pos=(0, -0.01),
            pos=(0.12, 0, -0.15), frameSize=(-0.05, 0.05, -0.05, 0.05),
            frameColor=(0.863, 0.773, 0.616, 1.0),
        )

        self.pauseState = False

        # Event Marker Buttons

        self.buttons_eventMarkers = []
        self.updateEventMarkers()
        self.accept('updateEvents', self.updateEventMarkers)

    """
    Event Marker Builders
    """

    def clearEventMarkers(self):
        for button in self.buttons_eventMarkers:
            button.destroy()
        self.buttons_eventMarkers = []

    def updateEventMarkers(self, _=None):
        self.clearEventMarkers()
        events = self.mgr.events
        selectedEvent = self.mgr.selectedEvent
        yposEndDict = {}
        for event in events:
            # get the start and end pos of the bars
            startPos = -self.tl_width / 2
            endPos = self.tl_width / 2
            # get our xpos start and frame width
            xpos_start = ((event.time / max(self.mgr.trackLength, 0.01)) * (endPos - startPos)) + startPos
            frame_width = max((event.getDuration() / max(self.mgr.trackLength, 0.01) * (endPos - startPos), 0.030))
            end_pos = xpos_start + frame_width
            # update the yposenddict for each value we have passed
            for ypos, ypos_end_pos in yposEndDict.copy().items():
                if ypos_end_pos < xpos_start:
                    yposEndDict.pop(ypos)
            # update the list of startpos and endpos shown
            ypos = -0.08
            while ypos in yposEndDict:
                ypos -= 0.06
            # update the dict with the position we have taken
            yposEndDict[ypos] = end_pos

            button = DirectButton(
                parent=self.frame_progressBar, pos=(xpos_start, 0, ypos),
                frameSize=(0, frame_width, 0, 0.05),
                frameColor=(0.11, 0.533, 0.106, 1.0) if event is not selectedEvent else (0.729, 0.557, 0.227, 1.0),
                command=messenger.send, extraArgs=['requestSelectEvent', [event]],
                text='', text_scale=0.05, text_fg=(1, 1, 1, 1), text_shadow=(1, 1, 1, 0),
                text_pos=(frame_width / 2, 0),
            )
            button.setBin('fixed', 20)
            def doSetText(b, newName, *_):
                b.setText(newName)
                b.setBin('fixed', 20)
                if newName:
                    b.setBin('fixed', 60)
            button.bind(DGG.B3PRESS, self.enterTime, extraArgs=[event.time])
            button.bind(DGG.ENTER, doSetText, extraArgs=[button, event.name])
            button.bind(DGG.EXIT, doSetText, extraArgs=[button, ''])
            self.buttons_eventMarkers.append(button)

    """
    Pause Contraption
    """

    def swapPauseStatus(self):
        self.pauseState = not self.pauseState
        if self.pauseState:
            # now pausing
            self.mgr.pauseTrack(flag=PauseFlags.PauseButton)
            self.button_pause.setText('>')
        else:
            # now unpausing
            self.mgr.unpauseTrack(flag=PauseFlags.PauseButton)
            self.button_pause.setText('=')

    """
    Timer Progress Bar
    """

    def setTimelineState(self, mode, _=None):
        if not self.timelineState and mode:
            # entering timeline state
            self.mgr.pauseTrack(PauseFlags.TimelineState)
        elif self.timelineState and not mode:
            # exiting timeline state
            self.mgr.unpauseTrack(PauseFlags.TimelineState)
        self.timelineState = mode

    def updateTimeline(self, task):
        if base.mouseWatcherNode.hasMouse():
            if self.timelineState:
                ratio = base.getAspectRatio()
                timePos = max(-1.0, min(base.mouseWatcherNode.getMouseX(), 1.0)) * max(ratio, 1)
                startPos = -self.tl_width / 2
                endPos = self.tl_width / 2
                xpos = max(startPos, min(round(timePos, 4), endPos))
                self.enterTime(((xpos - startPos) / (endPos - startPos)) * self.mgr.trackLength)
            else:
                startPos = -self.tl_width / 2
                endPos = self.tl_width / 2
                range = endPos - startPos
                ratio = self.mgr.currentTime / max(self.mgr.trackLength, 0.01)
                xpos = max(startPos, min(startPos + (range * ratio), endPos))
            self.frame_progressMarker.setPos(xpos - (self.tl_width / (200 / self.tl_marker_size)), 0, 0)
        return task.cont

    """
    Time and Duration Entry
    """

    def enterTime(self, timeStr, _=None):
        """
        Updates the current time.
        """
        try:
            time = float(timeStr)
        except TypeError:
            # wasn't a string, so ignore..
            return
        if not 0 <= time <= self.mgr.trackLength:
            return
        messenger.send('updateTime', [time])

    def updateTimeEntry(self, task=None):
        """
        Updates the secondLabel entry.
        """
        if self.updateSecond:
            self.entry_secondLabel.set(str(round(self.mgr.currentTime, 2)))
        if task is not None:
            return task.cont

    def setUpdateSecondMode(self, mode):
        self.updateSecond = mode
        if mode:
            # we are re-enabling focus
            self.mgr.unpauseTrack(PauseFlags.ChangingTime)
        else:
            # we are putting focus on the second
            self.mgr.pauseTrack(PauseFlags.ChangingTime)

    def enterDuration(self, timeStr):
        """
        Updates the current duration.
        """
        try:
            time = float(timeStr)
        except TypeError:
            # wasn't a string, so ignore..
            return
        if time < 0:
            return
        messenger.send('requestUpdateDuration', [time])

    def updateDuration(self, time: float):
        """
        Updates the duration on the GUI.
        :param time:  The new duration.
        """
        self.entry_durationLabel.set(str(round(time, 2)))
        self.updateEventMarkers()
