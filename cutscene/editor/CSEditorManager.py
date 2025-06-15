"""
The manager file for the Cutscene Editor.

Stores all of the information for the currently edited cutscene,
along with all of the necessary functions
"""
import datetime

from direct.showbase.DirectObject import DirectObject
from direct.showbase.MessengerGlobal import messenger
from direct.task.TaskManagerGlobal import taskMgr

from toontown.cutscene.editor.CSEditorDefs import *

from toontown.cutscene.editor.CSEnvConfig import makeCutsceneDict, createCutscene
from toontown.cutscene.editor.CSPanelEvent import CSPanelEvent
from toontown.cutscene.editor.CSPanelPlayer import CSPanelPlayer
from toontown.cutscene.editor.CSPanelSubevent import CSPanelSubevent


class CSEditorManager(DirectObject):

    def __init__(self):
        # Dictionary Information #
        self.cutsceneDict = makeCutsceneDict()
        # Adding a flag to enable cutscene editor specific functionality #
        # (helps with sequences that don't loop well) #
        self.cutsceneDict['isEditor'] = True
        # Similarly, we'll also create a editorCleanup function list in the dictionary #
        # (helps with sequences that need to clean up nodes only when the track is updated) #
        self.cutsceneDict['editorCleanup'] = []  # type: list[function]

        # Flags #
        self.pauseFlags = set()

        # Event Variables #
        self.events = createCutscene(self.cutsceneDict)  # type: List[Event]

        if not self.events:
            self.events = [firstEvent]
        elif self.events[0].time != 0.0:
            self.events.insert(0, firstEvent)
        self.persistentEventCount = len(self.events)

        self.selectedEvent = None  # type: Event
        self.selectedSubEvent = None  # type: SubEvent

        # Track to reset actors and nodes to initial pos, hpr, scale and parent #
        self.initialValuesTrack = Sequence()
        nodesToReset = []
        for key in ('toons', 'suits', 'bosses', 'actors', 'nodes'):
            if key in self.cutsceneDict:
                nodes = [node for node in self.cutsceneDict[key] if node and node not in nodesToReset]
                nodesToReset += nodes
        for node in nodesToReset:
            self.initialValuesTrack.append(
                Sequence(
                    Func(node.setPos, node.getPos()),
                    Func(node.setHpr, node.getHpr()),
                    Func(node.setScale, node.getScale()),
                    Func(node.reparentTo, node.getParent()),
                    Func(node.hide if node.isHidden() else node.show)
                )
            )
            if node in self.cutsceneDict.get('suits', []) or node in self.cutsceneDict.get('bosses', []):
                self.initialValuesTrack.append(
                    Sequence(
                        Func(node.stash if node.isStashed() else node.unstash),
                        Func(node.hideNametag3d if node.isStashed() else node.showNametag3d)
                    )
                )

        # Track Variables #
        self.track = None
        self.trackLength = 15.0
        if self.events:
            cutscene = Cutscene(events=self.events, cutsceneDict=self.cutsceneDict)
            self.trackLength = max(15.0, cutscene.getEndTime())
        self.currentTime = 0.0
        self.updateTrack()

        # GUI i hate gui #
        self.gui_player = CSPanelPlayer(self)
        self.gui_event = CSPanelEvent(self)
        self.gui_subevent = CSPanelSubevent(self)

        # Task and Messenger #
        taskMgr.add(self.updateCurrentTime, 'cseditor-updateCurrentTime')
        self.accept('updateSubEvent', self.updateSubEvent)
        self.accept('updateTrack', self.updateTrack)
        self.accept('updateTime', self.setTrackTime)
        self.accept('jumpEvent', self.jumpEvent)
        self.accept('requestCreateEvent', self.addNewEvent)
        self.accept('requestEventDelete', self.deleteEvent)
        self.accept('requestSelectEvent', self.selectEvent)
        self.accept('requestUpdateDuration', self.setTrackDuration)
        self.accept('requestSelectSubevent', self.selectSubevent)
        self.accept('requestCreateSubevent', self.createSubevent)
        self.accept('requestMoveEventsInRange', self.moveEventsInRange)
        self.accept('space', self.autosave)
        self.accept('p', self.gui_player.swapPauseStatus)

        # Go ahead and select an event #
        if self.events:
            self.events.sort(key=lambda event: event.time)
            self.selectEvent(self.events[0])

    """
    Event Printing
    """

    def autosave(self):
        a = Cutscene(events=self.events, cutsceneDict=self.cutsceneDict)
        with open('cutscene_editor_autosave.json', mode='w') as f:
            json.dump(a.toDict(), f, indent=4)
        print(f'Auto-saved cutscene at {datetime.datetime.now()}')

    """
    Cutscene Playing
    """

    def updateTrack(self):
        """
        Updates the track.
        Makes sure it's set at the right time, too.
        """
        if self.track is None:
            # We gotta make a new track ASAP!
            self.track = None
            self.track = Sequence(self.initialValuesTrack)
            self.track.append(Cutscene(events=self.events, cutsceneDict=self.cutsceneDict).toTrack())
            self.track = Parallel(self.track, Wait(self.trackLength + 0.01))
            self.track.loop()
            self.updateCurrentTime()
            self.requestPauseTrack()
        elif self.track.isPlaying():
            # Remake the track, and get to the
            # time where it was already playing.
            self.track.finish()
            self.track = None
            for action in self.cutsceneDict['editorCleanup']:
                if callable(action):
                    action()
            self.cutsceneDict['editorCleanup'] = []
            self.track = Sequence(self.initialValuesTrack)
            self.track.append(Cutscene(events=self.events, cutsceneDict=self.cutsceneDict).toTrack())
            self.track = Parallel(self.track, Wait(self.trackLength + 0.01))
            self.track.loop()
            self.track.setT(self.currentTime)
            self.requestPauseTrack()
        elif self.track.isStopped():
            # The track is stopped, so we won't
            # have to restart or finish it.
            self.track.finish()
            self.track = None
            for action in self.cutsceneDict['editorCleanup']:
                if callable(action):
                    action()
            self.cutsceneDict['editorCleanup'] = []
            self.track = Sequence(self.initialValuesTrack)
            self.track.append(Cutscene(events=self.events, cutsceneDict=self.cutsceneDict).toTrack())
            self.track = Parallel(self.track, Wait(self.trackLength + 0.01))
            self.track.setT(self.currentTime)
            self.requestPauseTrack()
        else:
            # The track is.. somewhere.
            # Probably we're paused, though.
            self.track.finish()
            self.track = None
            for action in self.cutsceneDict['editorCleanup']:
                if callable(action):
                    action()
            self.cutsceneDict['editorCleanup'] = []
            self.track = Sequence(self.initialValuesTrack)
            self.track.append(Cutscene(events=self.events, cutsceneDict=self.cutsceneDict).toTrack())
            self.track = Parallel(self.track, Wait(self.trackLength + 0.01))
            self.track.loop()
            self.track.setT(self.currentTime)
            self.requestPauseTrack()
            self.updateCurrentTime()

    def updateCurrentTime(self, task=None):
        self.currentTime = self.track.getT()
        if task is not None:
            return task.cont

    def restartTrack(self):
        """
        Restarts the track from the start.
        """
        self.track.finish()
        self.track = None
        self.updateTrack()

    def requestPauseTrack(self):
        """
        Pauses the track, only when flags exist.
        """
        if self.pauseFlags:
            self.track.pause()

    def pauseTrack(self, flag=None):
        """
        Pauses the track.
        """
        if flag is not None:
            self.pauseFlags.add(flag)
        self.track.pause()

    def unpauseTrack(self, flag=None):
        """
        Unpauses the track.
        """
        if flag in self.pauseFlags:
            self.pauseFlags.remove(flag)
        if not self.pauseFlags:
            self.track.resume()

    def resetFlags(self):
        """
        Resets flags.
        """
        self.pauseFlags = set()

    def setTrackTime(self, time: float):
        """
        Sets the time of the current track.
        :param time: New time in track.
        """
        self.updateTrack()
        self.track.setT(time)

    def setTrackDuration(self, time: float):
        """
        Requests to update the track's duration.
        :param time: New duration.
        """
        latestEvent = self.getLatestEvent()
        if time < latestEvent:
            time = latestEvent
        self.trackLength = time
        self.updateTrack()
        messenger.send('updateDuration', [time])

    """
    SubEvent Accessors
    """

    def createSubevent(self, eventDefEnum):
        """
        Adds a new subevent.
        """
        if not self.selectedEvent:
            return
        if not eventDefEnum:
            return
        subevent = self.selectedEvent.addSubEvent(eventDefEnum)
        messenger.send('createSubevent', [subevent])
        self.selectSubevent(subevent)
        messenger.send('newSubevent')

    def selectSubevent(self, subevent):
        if not subevent:
            return
        if not self.selectedEvent:
            return
        if subevent not in self.selectedEvent.getSubEvents():
            return
        self.selectedSubEvent = subevent
        messenger.send('selectedSubevent', [subevent])

    def updateSubEvent(self):
        """
        Updates the selected SubEvent.
        """
        self.selectSubevent(self.selectedSubEvent)
        self.updateTrack()

    """
    Event Accessors
    """

    def addNewEvent(self, subEvents: list = []) -> Event:
        """
        Creates a new event.
        If one already exists at a given time,
        we'll go ahead and return it.

        :param time:    The time for this event.
        :return:        An event at this time.
        """
        time = self.currentTime

        # Remove the check to see if there's an event here already -- it is annoying
        # existingEvent = self.getEventFromTime(time)
        # if existingEvent:
        #     return existingEvent

        # Create a new event.
        self.persistentEventCount += 1
        newEvent = Event(time=time, name=f'Event #{self.persistentEventCount}')
        for subEvent in subEvents:
            newEvent.addExistingSubEvent(subEvent)
        self.events.append(newEvent)
        self.events.sort(key=lambda event: event.time)
        self.selectEvent(newEvent)
        messenger.send('updateEvents')

    def deleteEvent(self, event: Event) -> None:
        """
        Deletes an event from our event list.

        :param event: The event to delete.
        """
        if event.time == 0.0:
            # We don't want to delete the initial event.
            return
        if event not in self.events:
            # This event isn't one of our events!
            return
        newEventIndex = None
        if self.selectedEvent is event:
            # Change our selected event to the one after this one.
            # Or the one before it if this is the last event in the cutscene.
            oldEventIndex = self.events.index(event)
            newEventIndex = oldEventIndex + 1
            if newEventIndex >= len(self.events):
                newEventIndex = oldEventIndex - 1
            self.selectEvent(self.events[newEventIndex])
        # Ok, now go ahead and officially delete this event.
        # Make sure the track is updated to reflect this too.
        self.events.remove(event)
        messenger.send('updateEvents')
        self.updateTrack()

    def selectEvent(self, event: Event) -> None:
        """
        Selects an event in the timeline.

        :param event: The event to select.
        """
        if event not in self.events:
            # Event not defined properly.
            return
        self.selectedEvent = event
        self.setTrackTime(event.getTime())
        self.updateSubEvent()
        messenger.send('updateEvents')
        messenger.send('selectEvent', [event])

    def jumpEvent(self, indexChange: int):
        """
        Jumps event index by indexChange.

        :param indexChange: The indexes to change by.
        """
        if not self.selectedEvent:
            return
        currentIndex = self.events.index(self.selectedEvent)
        newIndex = currentIndex - indexChange
        newIndex = max(0, min(newIndex, len(self.events) - 1))
        self.selectEvent(self.events[newIndex])

    def getEventFromTime(self, time: float = 0.0, width: float = 0.5):
        """
        Gets an event at a given time.

        :param time:    The time to check for an event.
        :param width:   The width of time to check.
        :return:        An event if it exists, or None.
        """
        for event in self.events:
            if -width < (event.getTime() - time) < width:
                return event
        return None

    def getLatestEvent(self) -> float:
        """
        Returns the time of the latest-defined event.
        :return: The time of the latest-defined event.
        """
        return max([event.time + event.getDuration() for event in self.events])

    """
    Edit Tool Functions
    """
    def moveEventsInRange(self, amount, startTime, endTime):
        for event in self.events:
            eventTime = event.getTime()
            if 0 < eventTime <= endTime and eventTime >= startTime:
                event.setTime(max(0, event.getTime() + amount))
        messenger.send('updateTrack')
        messenger.send('updateEvents')
