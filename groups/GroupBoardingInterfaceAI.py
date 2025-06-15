from abc import ABC, abstractmethod
from typing import List, Optional

from toontown.groups.GroupClasses import GroupAI
from toontown.notifications.notificationData.GenericTextNotification import GenericTextNotification, GenericTextId
from toontown.toon.DistributedToonAI import DistributedToonAI
from toontown.utils.RateLimiter import IdRateLimiter

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from toontown.ai.ToontownAIRepository import ToontownAIRepository


class GroupBoardingInterfaceAI(ABC):
    """
    This class helps to provide an interface for handling complex Group boarding
    procedures on the AI. This is useful for elevators, Trolley, golf karts, etc.

    Since elevators are notoriously programmed differently throughout the TT codebase,
    this interface exists to help unify boarding behavior between different elevators.
    """

    base_elevator_time = 30  # The time it takes for the elevator to fully depart.
    groupType = None         # type: GroupType

    # Ratelimit Constants
    reserve_ratelimit_maxHits = 3    # The number of times any individual Toon can reserve an elevator.
    reserve_ratelimit_period  = 60   # The duration of the ratelimit for Toons reserving an elevator.

    # Timing Constants
    elevator_fill_seconds = 6        # Where does the timer drop to when the elevator fills?
    elevator_fill_group_seconds = 6  # Same as above, but if a Group fills the elevator instead.

    def __init__(self, air):
        # We keep track of any avIds we may be ratelimiting for elevator reserves.
        self.rateLimiter = IdRateLimiter(max_hits=self.reserve_ratelimit_maxHits, period=self.reserve_ratelimit_period)
        self.air = air  # type: ToontownAIRepository

    """
    Public Methods. These must be called.
    """

    def canBoardElevator(self, avId: int) -> bool:
        """
        Determines if an avId is able to board an elevator.
        """
        toonGroup = self.air.groupManager.getGroupOfAvId(avId)
        specificGroupType = self.getSpecificGroupType()
        ourGroupType = specificGroupType if isinstance(specificGroupType, (list, tuple, set)) else [specificGroupType]
        # We have a group and the group types are differing, die.
        if toonGroup and toonGroup.groupDefinition.groupType not in ourGroupType:
            self.sendWrongElevatorNotification(avId)
            return False

        # If the elevator is empty, we have to reserve it.
        if self.getBoarderCount() == 0:

            # If the user is blocked from reserving, they cannot board.
            if self.rateLimiter.userBlocked(avId):
                self.sendReserveBanNotification(avId)
                return False

            # Otherwise, they are able to board.
            return True

        # if the elevator is full, the elevator cannot be boarded.
        if self.isFull():
            return False

        # The elevator is not empty, but it's not full either.
        else:
            # We need to find the current reserved "group" in the elevator.
            # Only members of this current reserved group can join.
            reservedGroup = self._getReservedGroup()

            # If these groups are indeed one in the same, then the toon can board.
            # Otherwise, the elevator does not have a Group for the Toon.
            if toonGroup == reservedGroup:
                return True
            else:
                # If the avId is not in a group, then we can
                # let them attempt to join the reserved group.
                if reservedGroup:
                    # Only try if its a public group, else its occupied so Die
                    if reservedGroup.published and self.air.groupManager.requestGroup(targetAvId=reservedGroup.owner, force=True, avId=avId, respondToAv=False):
                        return True
                    else:
                        # They couldn't join the group either, so just say that it is occupied.
                        self.sendOccupiedNotification(avId)
                        return False
                # No reserved group, lets see if there's enough room for *our* group
                else:
                    if toonGroup:
                        return len(toonGroup.avatarList) <= self.getSpaceLeft()
                    else:
                        # No reserved group, and we don't have a group. We're safe to join.
                        return True

    def onToonBoard(self):
        """
        Call this whenever a Toon successfully boards the elevator.
        They must be present in self.getCurrentBoarders() for this to be functional.
        """
        group = self._getReservedGroup()
        # If we have a reserved group and the group makes up all elevator members...
        if group and len(group.avatarList) >= self.getBoarderCount():
            # If the entire group has entered the elevator now, reduce the timer to 0 seconds.
            # If this group is not the only set of people in the elevator, it will only fill if its full.
            currentBoarders = self.getCurrentBoarders()
            for groupAvId in group.avIds:
                if groupAvId not in currentBoarders:
                    # The entire group has not boarded yet -- return.
                    return

            # If we are at this point, then all members in the group are present in the elevator.
            if self.getDepartTimeRemaining() > self.elevator_fill_group_seconds:
                self.setBoardingTimer(seconds=self.elevator_fill_group_seconds)
        else:
            # No group? Reduce the timer to 5 seconds if the elevator has filled.
            if self.isFull() and self.getDepartTimeRemaining() > self.elevator_fill_seconds:
                self.setBoardingTimer(seconds=self.elevator_fill_seconds)

    """ 
    Abstract Methods
    """

    @abstractmethod
    def setBoardingTimer(self, seconds: int = 0) -> None:
        """
        Sets the boarding timer to the seconds mentioned.
        This must be able to support 0 seconds as well.
        """
        raise NotImplementedError

    """
    Abstract Getters
    """

    def getSpecificGroupType(self):
        """
        Gets the specific group type for this elevator
        Returns generic group type by default
        """
        return self.groupType

    @abstractmethod
    def getDepartTimeRemaining(self) -> float:
        """
        Gets the current time of departure for the elevator.
        """
        raise NotImplementedError

    @abstractmethod
    def getCurrentBoarders(self) -> List[int]:
        """
        Returns a list of all Toon avIds on board.
        """
        raise NotImplementedError

    @abstractmethod
    def getElevatorSize(self) -> int:
        """
        Returns the size of the elevator.
        """
        raise NotImplementedError

    @staticmethod
    def getTransportationName() -> str:
        return 'Elevator'

    """
    Internal Logic
    """

    def _getReservedGroup(self) -> Optional[GroupAI]:
        """
        Returns the current Group that is reserved in the elevator.
        """
        # Iterate over each avId that is currently boarded.
        for avId in self.getCurrentBoarders():

            # Find the group that they are in.
            group = self.air.groupManager.getGroupOfAvId(avId)

            # If they're in a group, let's check it out.
            if group is not None:

                # If we've defined a groupType, we need to make sure this group matches the group type.
                if self.groupType is not None:

                    # Does the groupType check out?
                    # If it's not the same group tye, we need to look at the other avIds.
                    if isinstance(self.groupType, (tuple, list, set)):
                        if group.getGroupCreation().getGroupType() not in self.groupType:
                            continue
                    else:
                        if group.getGroupCreation().getGroupType() != self.groupType:
                            continue

                # This group is reserved in the elevator.
                return group

        # No group is reserved in the elevator.
        return None

    """
    Notifications
    """

    def sendReserveBanNotification(self, avId: int):
        av = self.air.doId2do.get(avId)
        if av:
            av.addNotification(GenericTextNotification(
                textId=GenericTextId.BoardingInfo,
                title='Reserve Banned',
                subtitle=f'You have been temporarily prohibited from reserving this {self.getTransportationName()}.',
            ))

    def sendOccupiedNotification(self, avId: int):
        av = self.air.doId2do.get(avId)
        if av:
            av.addNotification(GenericTextNotification(
                textId=GenericTextId.BoardingInfo,
                title=f'{self.getTransportationName()} Occupied',
                subtitle=f'You cannot board the {self.getTransportationName()}, as it is currently occupied by another Group.',
            ))

    def sendWrongElevatorNotification(self, avId: int):
        av = self.air.doId2do.get(avId)
        if av:
            av.addNotification(GenericTextNotification(
                textId=GenericTextId.BoardingInfo,
                title=f"Can't Board {self.getTransportationName()}",
                subtitle=f'You cannot board the {self.getTransportationName()} because you are in a different group.'
            ))

    """
    Useful getters
    """

    def isEmpty(self) -> bool:
        """
        Returns True if the elevator is empty.
        """
        return self.getBoarderCount() == 0

    def isFull(self) -> bool:
        """
        Returns True if the elevator is full.
        """
        return self.getBoarderCount() == self.getElevatorSize()

    def getSpaceLeft(self) -> int:
        """
        Returns the number of space for boarders left.
        """
        return self.getElevatorSize() - self.getBoarderCount()

    def getBoarderCount(self) -> int:
        """
        Returns the number of boarders on the elevator.
        """
        return len(self.getCurrentBoarders())
