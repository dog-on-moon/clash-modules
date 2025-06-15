from toontown.quest3.base.QuestContext import QuestContext


class RacingContext(QuestContext):
    """
    Context for when a race is completed.
    """

    def __init__(self, trackId: int, finishedAvatars: int, participants: int) -> None:
        self.trackId = trackId
        self.finishedAvatars = finishedAvatars
        self.partipants = participants
    
    def getTrackId(self) -> int:
        return self.trackId
    
    def getFinishedAvatars(self) -> int:
        return self.finishedAvatars
    
    def getParticipants(self) -> int:
        return self.partipants
