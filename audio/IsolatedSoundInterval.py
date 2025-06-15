import time

if __name__ == "__main__":
    from tools.headless.headlessbase import HeadlessStart
    from tools.headless.headlessbase.HeadlessBase import HeadlessBase
    base = HeadlessBase(wantHotkeys=False)
    if __debug__:
        from toontown.utils.DeveloperInjector import startInjector
        startInjector()

from direct.interval.SoundInterval import SoundInterval


class IsolatedSoundInterval(SoundInterval):
    """
    A unique SoundInterval subclass that only allows one sound to play simultaneously.
    """

    # The time between each sound that can be played.
    gracePeriod = 0.12

    # Our private sound dictionary, to keep track of when sounds were played.
    __soundsLastPlayed = {}

    """
    Ival overrides
    """

    def privInitialize(self, t):
        # If the sound was played recently, disable its volume.
        if self.soundPlayedRecently():
            self.volume = 0.0
        return super().privInitialize(t)

    """
    Sound dictionary accessors
    """

    def soundPlayedRecently(self) -> bool:
        """
        Determines if this ival's sound was played too recently.
        """

        # If this sound has not been played before, the sound was not played.
        if self.getSoundName() not in self.__soundsLastPlayed:
            self._markSound()
            return False

        # However, the sound has been played before.
        # If it is within the grace period, it has been played too soon.
        currentTime = time.time()
        lastPlayed = self.__soundsLastPlayed.get(self.getSoundName(), currentTime)
        if (lastPlayed + self.gracePeriod) > currentTime:
            return True

        # The sound has not been played too recently, we can play it now.
        self._markSound()
        return False

    def _markSound(self):
        """
        Marks this ival's sound as being played too soon.
        """
        if not self.sound:
            return
        self.__soundsLastPlayed[self.getSoundName()] = time.time()

    def getSoundName(self):
        """
        Gets the name of the sound in the interval.
        """
        if not self.sound:
            return None
        return self.sound.getName()


if __name__ == "__main__":
    from direct.interval.IntervalGlobal import Parallel
    exampleParallel = Parallel()
    for i in range(5):
        cogSound = base.loader.loadSfx('phase_3.5/audio/sfx/ENC_cogfall_apart.ogg')
        exampleParallel.append(IsolatedSoundInterval(cogSound))
    exampleParallel.loop()
    base.run()
