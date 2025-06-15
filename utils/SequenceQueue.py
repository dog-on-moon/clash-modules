from direct.interval.IntervalGlobal import Interval, Sequence, Func


class SequenceQueue:
    """
    A SequenceQueue is a unique kind of Sequence metaclass that is always playing.
    By appending to it, you put a sequence at the end of the SequenceQueue
    so that it gets queued to play.
    """

    def __init__(self, maxSize: int = -1, playRate: float = 1.0, autoSkip: bool = False):
        """
        Initiates an SequenceQueue.
        :param maxSize: The max number of sequences to store. -1 for unlimited.
        """
        self._queue = []
        self._maxSize = maxSize
        self._playRate = playRate
        self._autoSkip = autoSkip
        self._activeInterval = None
        self._playing = False
        self._lock = False

    def lock(self):
        """
        Locks the SequenceQueue.
        Automatically unlocks once it empties.
        :return: None.
        """
        self._lock = True

    def unlock(self):
        """
        Unlocks the SequenceQueue.
        :return: None.
        """
        self._lock = False

    def finish(self):
        """
        Cleans up a SequenceQueue.
        :return: None.
        """
        for interval in self._queue:
            interval.finish()
        if self._activeInterval:
            self._activeInterval.finish()
        self._queue = []
        self._activeInterval = None
        self._lock = False

    def append(self, interval: Interval) -> bool:
        """
        Adds an interval to the SequenceQueue.
        :param interval: The interval to be queued.
        :return: Bool if the operation was successful.
        """
        # If we have a lock, then do not append.
        if self._lock:
            return False

        # Is the queue full?
        while self.isFull():
            if self._autoSkip:
                # If we're autoskipping, then skip currently playing intervals.
                self._play()
            else:
                # Just die
                return False

        # Wrap the interval.
        wrappedInterval = Sequence(
            interval,
            Func(self._play),
        )

        # Add it to our queue.
        self._queue.append(wrappedInterval)

        # If we are not playing, start playing.
        if not self._playing:
            self._playing = True
            self._play()

        # Skip the sequence if we have the reduced gui movement option enabled.
        if settings['reduce-gui-movement']:
            self.finish()

        # We are done here.
        return True

    def getTimeRemaining(self) -> float:
        """
        Gets the time remaining in the SequenceQueue.
        :return: Seconds (float).
        """
        timeLeft = 0.0
        for interval in self._queue:
            timeLeft += interval.getDuration()
        if self._activeInterval:
            timeLeft += self._activeInterval.getDuration() - self._activeInterval.getT()
        return timeLeft

    def isFull(self):
        if self._maxSize == -1:
            return False
        return len(self._queue) >= self._maxSize

    def isEmpty(self):
        return bool(self._queue)

    def isPlaying(self):
        return self._playing

    def _play(self):
        """
        Starts playing the next interval in the queue.
        :return: None.
        """
        # Clean up the active interval.
        if self._activeInterval:
            self._activeInterval.finish()
            self._activeInterval = None

        # If there is nothing left in the queue, we're done playing.
        if not self._queue:
            self._playing = False
            self._lock = False
            return

        # Ok, there's a sequence in the queue. Pop it and play it.
        self._activeInterval = self._queue.pop(0)
        self._activeInterval.start(playRate=self._playRate)
