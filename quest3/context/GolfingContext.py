from toontown.quest3.base.QuestContext import QuestContext


class GolfingContext(QuestContext):
    """
    Context for when a golf course is completed.
    """

    def __init__(self, courseId: int, ranking: int, participants: int, coursePar: int, totalScore: int) -> None:
        self.courseId = courseId
        self.ranking = ranking
        self.partipants = participants
        self.coursePar = coursePar
        self.totalScore = totalScore
    
    def getCourseId(self) -> int:
        return self.courseId
    
    def getRanking(self) -> int:
        return self.ranking
    
    def getParticipants(self) -> int:
        return self.partipants
    
    def getUnderPar(self) -> bool:
        return self.coursePar - self.totalScore > 0
