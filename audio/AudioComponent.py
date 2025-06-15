from panda3d.core import NodePath
import math

class AudioComponent3d(NodePath):
    AUDIO_MAX = 1.0
    AUDIO_MIN = 0.0

    def __init__(self, audioFile):
        NodePath.__init__(self, 'AudioComponent3d')

        assert audioFile is not None

        self.__component = base.loader.loadMusic(audioFile)

    def __setattr(self, *args, **kw):
        return setattr(self.__component, *args, **kw)

    def __getattr__(self, *args, **kw):
        return getattr(self.__component, *args, **kw)

    def play(self):
        taskMgr.add(self.__doUpdate, 'audio-update-%s' % self.id)

        self.__component.play()

    def __doUpdate(self, task):
        distance = self.getDistance(base.camera)
        distance = math.radians(math.sqrt(distance)) * math.pi

        if distance > self.AUDIO_MAX:
            distance = self.AUDIO_MAX
        elif distance < self.AUDIO_MIN:
            distance = self.AUDIO_MIN

        self.__component.setVolume(self.AUDIO_MAX - distance)
        return task.cont

    def stop(self):
        taskMgr.remove('audio-update-%s' % self.id)

        self.__component.stop()
