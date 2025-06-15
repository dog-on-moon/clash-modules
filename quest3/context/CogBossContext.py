from toontown.quest3.base.QuestContext import QuestContext


class CogBossContext(QuestContext):
    """
    Context for when a Toon defeats a COGS boss.

    This is to be populated with more fields as needed.
    """
    
    def __init__(self, cogTrack: str, stunCount: int, bossDamage: int) -> None:
        self.cogTrack = cogTrack
        self.stunCount = stunCount
        self.bossDamage = bossDamage
    
    def getStunCount(self) -> int:
        return self.stunCount
    
    def getCogTrack(self) -> str:
        return self.cogTrack
    
    def getBossDamage(self) -> int:
        return self.bossDamage


"""
Subclasses for specific boss cogs
"""


class CashbotBossContext(CogBossContext):
    """
    Context for when a Toon defeats a CFO.
    """

    def __init__(self, cogTrack: str, stunCount: int, bossDamage: int, safeDamage: int, goonDamage: int, unstunnedGoonDamage: int) -> None:
        super().__init__(cogTrack, stunCount, bossDamage)
        self.safeDamage = safeDamage
        self.goonDamage = goonDamage
        self.unstunnedGoonDamage = unstunnedGoonDamage
    
    def getSafeDamage(self) -> int:
        return self.safeDamage

    def getGoonDamage(self) -> int:
        return self.goonDamage

    def getUnstunnedGoonDamage(self) -> int:
        return self.unstunnedGoonDamage

    def getTotalGoonDamage(self) -> int:
        return self.goonDamage + self.unstunnedGoonDamage


class LawbotBossContext(CogBossContext):
    """
    Context for when a Toon defeats a CLO.
    """

    def __init__(self, cogTrack: str, stunCount: int, bossDamage: int, evidence: int, cogsDestroyed: tuple,
                 exesDestroyed: tuple) -> None:
        super().__init__(cogTrack, stunCount, bossDamage)
        self.evidence = evidence
        self.cogsDestroyed = cogsDestroyed
        self.exesDestroyed = exesDestroyed
    
    def getEvidence(self) -> int:
        return self.evidence
    
    def getCogsDestroyed(self, activeRound: int) -> int:
        return self.cogsDestroyed[activeRound]
    
    def getExesDestroyed(self, activeRound: int) -> int:
        return self.exesDestroyed[activeRound]


class BossbotBossContext(CogBossContext):
    """
    Context for when a Toon defeats a CEO.
    """

    def __init__(self, cogTrack: str, stunCount: int, bossDamage: int, dinersFed: int, exesFed: int,
                 golfHits: int) -> None:
        super().__init__(cogTrack, stunCount, bossDamage)
        self.dinersFed = dinersFed
        self.exesFed = exesFed
        self.golfHits = golfHits
    
    def getDinersFed(self) -> int:
        return self.dinersFed
    
    def getExesFed(self) -> int:
        return self.exesFed
    
    def getGolfHits(self) -> int:
        return self.golfHits
