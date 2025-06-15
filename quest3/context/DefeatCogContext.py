"""
A module containing the contextual results for defeating Cogs.
"""
from toontown.quest3.base.QuestContext import QuestContext


class DefeatCogContext(QuestContext):
    """
    A dataclass for battle information when a Cog is defeated.
    """

    def __init__(self, suitsKilled, zoneId: int):
        """
        :param suitsKilled: list
        """
        self.encounters = [SuitEncounter(**encData) for encData in suitsKilled]
        self.zoneId = zoneId


class SuitEncounter:
    """
    A dataclass for suit encounter data.
    """

    def __init__(self, type: str, level: int, track: str, isSkelecog: bool,
                 isForeman: bool, isBoss: bool, isSupervisor: bool,
                 isVirtual: bool, hasRevives: bool, isElite: bool, activeToons, **kwargs):
        self.type = type
        self.level = level
        self.track = track
        self.isSkelecog = isSkelecog
        self.isForeman = isForeman
        self.isBoss = isBoss
        self.isSupervisor = isSupervisor
        self.isVirtual = isVirtual
        self.hasRevives = hasRevives
        self.isElite = isElite
        self.activeToons = activeToons  # type: list
        self.ignoreManagerFlag = kwargs.get('ignoreManagerFlag', False)
