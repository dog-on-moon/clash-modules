"""
Information defining all features of ambience in Toontown.
"""
from direct.interval.IntervalGlobal import *
import random


class Ambience:
    """
    Container class for ambience.
    """
    def __init__(self, title: str, fileLocation: str, ambienceNames: tuple = None, volume: float = 1.0,
                 durationBetween: tuple = None, suffix: str = '.ogg'):
        self.title = title
        self.fileLocation = fileLocation
        self.ambienceNames = ambienceNames
        self.volume = volume
        self.durationBetween = durationBetween
        self.suffix = suffix
        self.loadedAmb = []
        self.taskName = self._getTaskName()

    def cleanup(self):
        """Cleans up the currently playing tasks."""
        self._stopSounds()
        taskMgr.remove(self.taskName)

    def startAmbienceTasks(self, base):
        """Starts the ambience playing tasks."""
        if not self.loadedAmb:
            self.loadedAmb = self._loadAmb(base)
        taskMgr.doMethodLater(self._getDelayTime(), self.loopAmbience, self.taskName)

    def loopAmbience(self, task):
        """Plays the audio accordingly."""
        self._playSound()

        # Continue the task.
        task.delayTime = self._getDelayTime()
        return task.again

    def _playSound(self):
        """Plays a random sound in this container."""
        random.choice(self.loadedAmb).play()

    def _stopSounds(self):
        for sound in self.loadedAmb:
            sound.stop()

    def _loadAmb(self, base) -> tuple:
        """Loads up all of the sounds in this container."""
        retlist = []
        i = -1
        if self.ambienceNames:
            for ambienceName in self.ambienceNames:
                i += 1
                sfx = base.loader.loadSfx(self._getFileName(ambienceName))
                sfx.setVolume(self._getVolume(i))
                retlist.append(sfx)
        else:
            sfx = base.loader.loadSfx(self._getFileName())
            sfx.setVolume(self.volume)
            retlist.append(sfx)
        return tuple(retlist)

    def _getVolume(self, i) -> float:
        """Returns the volume given an index."""
        if type(self.volume) not in (tuple, list):
            return self.volume
        # the volume is a list, so return a useful index from it
        return self.volume[i % len(self.volume)]

    def _getDelayTime(self) -> int:
        """Gets a random delay time."""
        if self.durationBetween is None:
            return 0
        a, b = self.durationBetween
        return random.randint(round(a), round(b))

    def _getTaskName(self) -> str:
        """Gets the task name of the ambience we're looping."""
        return f'amb{self.title}'

    def _getFileName(self, ambienceName: str = '') -> str:
        """Returns the complete file name, given this name."""
        return self.fileLocation + ambienceName + self.suffix


class FieldAmbience(Ambience):
    """
    An Ambience subclass that is dedicated for extended, single sound ambience.
    """

    def __init__(self, fadeInTime: float = 0.0, fadeOutTime: float = 0.0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fadeInTime = fadeInTime
        self.fadeOutTime = fadeOutTime

    def loopAmbience(self, task):
        """Plays the audio accordingly."""
        self._playSound()
        return task.done

    def _playSound(self):
        """Plays a random sound in this container."""
        audio = random.choice(self.loadedAmb)
        audio.setLoop(1)
        audio.setVolume(0.0)
        audio.play()
        LerpFunctionInterval(
            function=audio.setVolume,
            duration=self.fadeInTime,
            fromData=0.0,
            toData=self.volume,
        ).start()

    def _stopSounds(self):
        for audio in self.loadedAmb:
            Sequence(
                LerpFunctionInterval(
                    function=audio.setVolume,
                    duration=self.fadeOutTime,
                    fromData=self.volume,
                    toData=0.0,
                ),
                Func(audio.stop),
            ).start()
