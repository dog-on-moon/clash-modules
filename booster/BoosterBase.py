"""
The base class for a Booster.
"""
import datetime
import time

from toontown.booster.BoosterGlobals import *
from toontown.inventory.enums.ItemEnums import BoosterItemType
from toontown.utils.AstronStruct import AstronStruct


class BoosterBase(AstronStruct):
    """
    A base class representing a Booster, which is a limited-time
    booster which a Toon may have associated with it.
    """

    def __init__(self, boosterType: BoosterItemType, endTimestamp=0, startTimestamp=round(time.time())):
        self.boosterType = boosterType
        self.endTimestamp = endTimestamp
        self.startTimestamp = startTimestamp

    def toStruct(self) -> list:
        """Converts this Booster into an Astron struct."""
        return [self.boosterType.value, self.endTimestamp, self.startTimestamp]

    @classmethod
    def fromStruct(cls, struct: list):
        """Converts a struct into an AstronStruct subclass."""
        boosterTypeInt, endTimestamp, startTimestamp = struct
        boosterType = BoosterItemType(boosterTypeInt)
        return cls(boosterType=boosterType, endTimestamp=endTimestamp, startTimestamp=startTimestamp)

    def toDict(self) -> dict:
        return {
            'boosterType': self.boosterType.value,
            'endTimestamp': self.endTimestamp,
            'startTimestamp': self.startTimestamp,
        }

    @classmethod
    def fromDict(cls, d) -> 'BoosterBase':
        boosterTypeInt = d['boosterType']
        endTimestamp = d['endTimestamp']
        startTimestamp = d.get('startTimestamp', round(time.time()))
        return cls(boosterType=BoosterItemType(boosterTypeInt), endTimestamp=endTimestamp, startTimestamp=startTimestamp)

    """
    Boost Initializers
    """

    def setDuration(self, currentTime: float, timeDelta: datetime.timedelta):
        """
        Sets the duration of this booster relative to now.

        :param currentTime: The current time.
        :param timeDelta: Some sort of defined timedelta instance.
        :return: None.
        """
        self.startTimestamp = round(currentTime)
        self.endTimestamp = round(currentTime + timeDelta.total_seconds())
        return self

    def extendDuration(self, timeDelta: datetime.timedelta):
        """
        Extends the duration of the boost by a timeDelta.

        :param timeDelta: Some sort of defined timedelta instance.
        :return: None.
        """
        if self.durationExtendsPastMax():
            # This duration ends more than a week away,
            # so we won't extend the duration any further.
            return self

        # Update the timestamp.
        self.endTimestamp = round(self.endTimestamp + timeDelta.total_seconds())
        return self

    def durationExtendsPastMax(self):
        return self.endTimestamp > (time.time() + MAX_BOOSTER_DURATION)

    """
    Boost Handlers
    """

    def getBoostType(self) -> BoosterItemType:
        """
        Gets the type of this boost.
        :return: A BoosterItemType.
        """
        return self.boosterType

    def isExpired(self) -> bool:
        """
        Checks if this Boost is expired.
        :return: True/False.
        """
        return self.getTimeLeft() <= 0

    def getTimeLeft(self) -> float:
        """
        Gets the time (in seconds) left on this booster.
        :return: Seconds relative to server's end time.
        """
        return self.endTimestamp - time.time()

    def getEndTime(self) -> float:
        """
        Gets the time when this booster ends.
        :return: Seconds relative to server's epoch.
        """
        return self.endTimestamp

    def getStartTime(self) -> int:
        """
        Gets the time when this booster starts.
        """
        return self.startTimestamp

    def getDuration(self) -> int:
        """
        Returns the duration of this booster in seconds.
        """
        return self.endTimestamp - self.startTimestamp
