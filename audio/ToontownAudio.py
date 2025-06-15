from toontown.audio.AmbienceDefs import *
from panda3d.core import FilterProperties
from direct.interval.IntervalGlobal import *
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory


@DirectNotifyCategory()
class ToontownAudio:
    def __init__(self, base):
        self.filterProperties = FilterProperties()
        self.playingAmbience = []

        # tell ToonBase about events to listen into
        base.ignore('zoneChange')
        base.ignore('ambienceKeyStart')
        base.ignore('ambienceKeyEnd')
        base.ignore('clientLogout')
        base.accept('zoneChange', self.handleZoneChange)
        base.accept('ambienceKeyStart', self.ambienceKeyStart)
        base.accept('ambienceKeyEnd', self.ambienceKeyEnd)
        base.accept('clientLogout', self.clearZoneAmbience)

    """
    Ambience-Related Functions
    """

    def handleZoneChange(self, zoneId: int):
        """Tries to update ambience given a zone change."""
        if zoneId == 1:
            # changing zones entirely, clear the zome ambience pwease
            self.clearZoneAmbience()
        ambience = getAmbience(zoneId)
        if ambience is not None and ambience not in self.playingAmbience:
            ambience.startAmbienceTasks(base)
            self.playingAmbience.append(ambience)

    def ambienceKeyStart(self, key: str):
        """
        Plays an ambience directly through a key.
        Note that it must be cleaned up manually as well.
        """
        self.notify.info(f'ambienceKeyStart({key})')
        ambience = getAmbience(key)
        if ambience is not None and ambience not in self.playingAmbience:
            ambience.startAmbienceTasks(base)
            self.playingAmbience.append(ambience)

    def ambienceKeyEnd(self, key: str):
        """Cleans up an ambience set directly from a key."""
        self.notify.info(f'ambienceKeyEnd({key})')
        ambience = getAmbience(key)
        if ambience is not None and ambience in self.playingAmbience:
            ambience.cleanup()
            self.playingAmbience.remove(ambience)

    def clearZoneAmbience(self):
        """Stops playing all zone-based ambiences."""
        self.notify.info(f'clearZoneAmbience')
        for ambience in zoneAmbienceList:
            ambience: Ambience
            if ambience in self.playingAmbience:
                ambience.cleanup()
                self.playingAmbience.remove(ambience)

