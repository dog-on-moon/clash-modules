"""
A module containing the contextual results for defeating Cog Buildings.
"""
from toontown.quest3.base.QuestContext import QuestContext


class BuildingContext(QuestContext):
    """
    Context when a building is DEMOLISHED
    """

    def __init__(self, zoneId: int, track: str, floors: int):
        self.zoneId = zoneId
        self.track = track
        self.floors = floors
