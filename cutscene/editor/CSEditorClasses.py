"""
All of the relevant classes for the Cutscene Editor.
"""
from copy import deepcopy, copy
import json

from direct.interval.IntervalGlobal import *
from toontown.cutscene.editor.CSEditorEnums import *
from panda3d.core import LPoint3f


class CSEditorException(Exception):
    """
    A custom exception for the Cutscene Editor.
    """
    pass


class EventArgument:
    """
    The argument data of an EventDefinition.
    """
    def __init__(self, kwarg: str = None, name: str = 'Undefined', type: SubEventArgumentType = None, default = None):
        self.kwarg = kwarg
        self.name = name
        self.type = type
        self.default = default


class EventDefinition:
    """
    All of the components to sufficiently define an "event"
    in the Cutscene Editor.

    An Event is a way to describe a single sequence that happens
    in the context of the cutscene.
    """

    def __init__(self, name: str, method: callable, arguments: list, enum: EventDefinitionEnum, category: str):
        self.name = name
        self.method = method
        self.arguments = arguments
        self.enum = enum
        self.category = category

    def getEventArgument(self, kwarg):
        for eventArg in self.arguments:
            if eventArg.kwarg == kwarg:
                return eventArg
        return None


class SubEvent:
    """
    A sequence which is contained in an Event.
    """

    def __init__(self, eventDefEnum: EventDefinitionEnum, kwargs: dict = None):
        if kwargs is None:
            kwargs = {}
        self.eventDefEnum = eventDefEnum
        self.kwargs = kwargs
        self.__post_init__()

    """
    Save/Load
    """

    def toDict(self) -> dict:
        """
        Converts this Event into a cutsceneData dict.
        :return: Dict breakdown of the Event and all of its components.
        """
        return {
            'eventDefEnum': self.eventDefEnum.name,
            'kwargs': json.dumps(
                self.kwargs,
                default=SubEvent.jsonSerialize,
            ),
        }

    @classmethod
    def fromDict(cls, cutsceneData: dict) -> 'SubEvent':
        """
        Makes a Event class from a cutsceneData dict.
        :param cutsceneData: The cutsceneData dict.
        :return: A new Event class.
        """
        return cls(
            eventDefEnum=EventDefinitionEnum[cutsceneData['eventDefEnum']],
            kwargs=cutsceneData['kwargs'] if type(cutsceneData['kwargs']) is dict else json.loads(cutsceneData['kwargs']),
        )

    @staticmethod
    def jsonSerialize(obj):
        """
        Safely serializes classes for json.
        """
        if type(obj) is LPoint3f:
            x, y, z = obj
            return x, y, z

    """
    Class Initialization
    """

    def __post_init__(self):
        """
        Sets all of the default properties.
        """
        kwargDefaults = {}
        for argument in self.eventArgs:
            kwargDefaults[argument.kwarg] = deepcopy(argument.default)
        kwargDefaults.update(self.kwargs)
        self.kwargs = kwargDefaults

    def getDuration(self) -> float:
        """
        Get the duration of the SubEvent, considering any
        duration and delay attributes.
        """
        retVal = 0
        if 'duration' in self.kwargs:
            retVal += self.kwargs['duration']
        if 'delay' in self.kwargs:
            retVal += self.kwargs['delay']
        return retVal

    def __setitem__(self, key, value):
        if self.kwargs[key] != value:
            self.kwargs[key] = value
            messenger.send('updateTrack')
            messenger.send('updateEvents')

    def __getitem__(self, item):
        return self.kwargs[item]

    def updateSubEvent(self, sliderGuis):
        """
        Updates the kwargs of the SubEvents.

        :param sliderGuis: SliderGUI dict. The key is the kwarg, the value is the new value.
        """
        self.kwargs.update(sliderGuis)
        messenger.send('updateTrack')
        messenger.send('updateEvents')

    def getKwargTypeDict(self):
        """
        Gets a dict for GUI building.

        :return: A dictionaries between keyword arguments and SubEventArgumentTypes for GUI.
        """
        return {eventArg.name: eventArg.type for eventArg in self.eventArgs}

    def getEventArgument(self, kwarg):
        return self.eventDef.getEventArgument(kwarg=kwarg)

    @property
    def name(self) -> str:
        """
        Gets the definition name of this subevent.
        :return: A cool name.
        """
        return self.eventDef.name

    @property
    def eventDef(self) -> EventDefinition:
        """
        Gets the event definition class from this SubEvent.
        :return: Some EventDefinition.
        """
        from toontown.cutscene.editor.CSEditorDefs import eventDefinitions
        return eventDefinitions[self.eventDefEnum]

    @property
    def eventArgs(self):
        """
        Gets the event args from this SubEvent's event definitions.
        :return: A list of EventArguments.
        """
        return self.eventDef.arguments


# The default mode to use for Events.
defaultEventMode = EventSequenceMode.Parallel


class Event:
    """
    A collection of SubEvents.
    """

    def __init__(self, name: str = 'Unnamed Event', time: float = 0.0,
                 sequenceMode: EventSequenceMode = defaultEventMode, subEvents: list = None):
        if subEvents is None:
            subEvents = []
        self.name = name
        self.time = time
        self.sequenceMode = sequenceMode
        self.subEvents = subEvents

    """
    Save/Load
    """

    def toDict(self) -> dict:
        """
        Converts this Event into a cutsceneData dict.
        :return: Dict breakdown of the Event and all of its components.
        """
        return {
            'name': self.name,
            'time': self.time,
            'sequenceMode': self.sequenceMode.name,
            'subEvents': {
                str(i): subEvent.toDict() for i, subEvent in enumerate(self.subEvents)
            }
        }

    @classmethod
    def fromDict(cls, cutsceneData: dict) -> 'Event':
        """
        Makes a Event class from a cutsceneData dict.
        :param cutsceneData: The cutsceneData dict.
        :return: A new Event class.
        """
        return cls(
            name=cutsceneData['name'],
            time=cutsceneData['time'],
            sequenceMode=EventSequenceMode[cutsceneData['sequenceMode']],
            subEvents=[
                SubEvent.fromDict(eventDict) for eventDict in cutsceneData['subEvents'].values()
            ]
        )

    """
    Sequence Mode Handling
    """

    def setSequenceMode(self, mode: EventSequenceMode):
        self.sequenceMode = mode

    def getSequenceMode(self):
        return self.sequenceMode

    """
    Name Handling
    """

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    """
    Time Handling
    """

    def getTime(self):
        return round(self.time, 3)

    def setTime(self, time: float):
        self.time = round(time, 3)

    def getDuration(self):
        if not self.subEvents:
            return 0.0
        if self.getSequenceMode() == EventSequenceMode.Parallel:
            return max([subEvent.getDuration() for subEvent in self.subEvents])
        elif self.getSequenceMode() == EventSequenceMode.Sequence:
            return sum([subEvent.getDuration() for subEvent in self.subEvents])

    """
    Subevents
    """

    def getSubEvents(self):
        return self.subEvents

    def addSubEvent(self, eventDefEnum: EventDefinitionEnum):
        newSubevent = SubEvent(eventDefEnum=eventDefEnum)
        self.subEvents.append(newSubevent)
        return newSubevent

    def addExistingSubEvent(self, subEvent):
        self.subEvents.append(subEvent)

    def removeSubEvent(self, subEvent: SubEvent):
        if subEvent not in self.getSubEvents():
            return
        self.subEvents.remove(subEvent)
        messenger.send('updateSubEvent')

    def moveSubEvent(self, subEvent: SubEvent, direction: int):
        if subEvent not in self.getSubEvents():
            return
        currentIndex = self.getSubEvents().index(subEvent)
        newIndex = currentIndex + direction
        newIndex = max(0, min(newIndex, len(self.getSubEvents()) - 1))
        self.subEvents.remove(subEvent)
        self.subEvents.insert(newIndex, subEvent)
        messenger.send('updateTrack')
        messenger.send('updateEvents')

    """
    Sequence Forming
    """

    def toSequence(self, cutsceneDict) -> MetaInterval:
        """
        Turns this Event into a complete sequence.
        :param cutsceneDict: The dict cutscene to use.
        :return: Some MetaInterval.
        """
        from toontown.cutscene.editor import CSEditorDefs
        retInterval = self.sequenceClass()
        for subEvent in self.subEvents:
            if subEvent.eventDefEnum in CSEditorDefs.EventExcludeList:
                continue
            try:
                useKwargs = copy(subEvent.kwargs)
                method = subEvent.eventDef.method
                useKwargs['cutsceneDict'] = cutsceneDict
                retInterval.append(method(**useKwargs))
            except Exception as e:
                # This subEvent likely doesn't have its kwargs defined correctly,
                # or even fully defined at all. This can be a big source of issues,
                # so we'll go ahead and print the exception it generates.
                print()
                print("Exception caught during sequence creation!")
                print(f"Event name: {self.name}")
                print(f"Subevent name: {subEvent.name}")
                print(e)
                continue
        return retInterval

    @property
    def sequenceClass(self):
        """
        The MetaInterval class this Event uses.
        :return: Some Metainterval class.
        """
        if self.sequenceMode == EventSequenceMode.Sequence:
            return Sequence
        elif self.sequenceMode == EventSequenceMode.Parallel:
            return Parallel
        raise CSEditorException("Event's sequenceMode enum value has an undefined sequenceClass.")

    @classmethod
    def buildCutsceneTrack(cls, events, cutsceneDict) -> Track:
        """
        Builds an entire cutscene from an event list.

        :param events: A defined list of events.
        :param cutsceneDict: The dict of information for use in this cutscene.
        :return: A cutscene.
        """
        return Parallel(*[Sequence(Wait(event.time), event.toSequence(cutsceneDict)) for event in events])


class Cutscene:
    """
    The Cutscene dataclass.
    Contains a list of cutscenes.
    """

    def __init__(self, events: list, cutsceneDict: dict):
        self.events = events  # type: List[Event]
        self.cutsceneDict = cutsceneDict

    """
    Save/Load
    """

    def toDict(self) -> list:
        """
        Converts this class into a cutsceneData dict.
        :return: Dict breakdown of the Cutscene and all of its components.
        """
        return [
            event.toDict() for event in self.events
        ]

    @classmethod
    def fromDict(cls, cutsceneDict: dict, cutsceneData: dict) -> 'Cutscene':
        """
        Makes a cutscene class from a cutsceneData dict.
        :param cutsceneData: The cutsceneData dict.
        :return: A new Cutscene class.
        """
        return cls(
            events=[
                Event.fromDict(eventDict) for eventDict in cutsceneData
            ],
            cutsceneDict=cutsceneDict
        )

    @staticmethod
    def jsonSerialize(obj):
        """
        Safely serializes classes for json.
        """
        if type(obj) is LPoint3f:
            x, y, z = obj
            return x, y, z

    """
    Cutscene actions
    """

    def getEndTime(self) -> float:
        """
        Returns the end time of this cutscene.
        :return: The end of the cutscene.
        """
        return max([event.getTime() + event.getDuration() for event in self.events])

    def toTrack(self, callback: callable = None) -> Parallel:
        """
        Turns this Cutscene class into a legitimate Movie.
        :return: The sequence representing the cutscene.
        """
        retCutscene = Parallel(
            *[Sequence(Wait(event.time), event.toSequence(self.cutsceneDict)) for event in self.events]
        )
        if callback is not None:
            retCutscene.append(Sequence(Wait(self.getEndTime()), Func(callback)))
        return retCutscene
