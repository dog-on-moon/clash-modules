from toontown.quest3.base.QuestContext import QuestContext


class DefeatFacilityContext(QuestContext):
    """
    Context for when a facility is defeated.
    """

    def __init__(self, facilityId: int) -> None:
        self.facilityId = facilityId
    
    def getFacilityId(self) -> int:
        return self.facilityId
