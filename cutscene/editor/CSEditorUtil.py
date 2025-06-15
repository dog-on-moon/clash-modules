"""
This module is dedicated to providing some useful utility functions for the cutscene editor.
"""


def getKwargs(kwargs: dict, *arguments: str):
    """Dev function to confirm certain kwargs exist."""
    if __debug__:
        missingArgs = [arg for arg in arguments if arg not in kwargs]
        if missingArgs:
            raise KeyError(f"Given kwargs for cutscene is missing arguments: {missingArgs}")
    return [kwargs.get(arg) for arg in arguments]


def makeToons(count: int = 1):
    from toontown.toon.npc import NPCToons
    from toontown.utils.bmp.BMPToon import BMPToon
    return [NPCToons.createRandomLocalNPC(toonClass=BMPToon) for _ in range(count)]


def makeToonsFromNPCToons(*npcToons):
    """Makes Toons from NPCToon objects."""
    from toontown.utils.bmp.BMPToon import BMPToon
    return [
        npc.createNPCLocal(toonClass=BMPToon)
        for npc in npcToons
    ]


def makeSuits(*suitNames):
    from toontown.utils.bmp import BMPSuit
    return [BMPSuit.createSuitOfName(t) for t in suitNames]


def makeBosses(*deptNames):
    from toontown.utils.bmp import BMPBossCog
    return [BMPBossCog.createBossOfDept(d) for d in deptNames]


def makeCameraMover(*animPaths):
    from direct.actor.Actor import Actor
    animDict = {}
    for path in animPaths:
        name = path[path.find('camera_actor-')+len('camera_actor-'):]
        animDict.update({name: path})
    cameraMover = Actor('phase_3.5/models/misc/camera_actor', animDict)
    cameraMover.setBlend(frameBlend=base.wantSmoothAnims)
    return cameraMover


def moveActorsToBattlePositions(toons: list = None, suits: list = None, newParent=None):
    toons = toons or []
    suits = suits or []
    if newParent is not None:
        [actor.reparentTo(newParent) for actor in toons + suits]
    from toontown.battle.BattleBase import BattleBase
    for i, suit in enumerate(suits):
        suitPointList = BattleBase.suitPoints[len(suits) - 1]
        xyz, h = suitPointList[i]
        suit.setPos(xyz)
        suit.setH(h)
    for i, toon in enumerate(toons):
        toonPointList = BattleBase.toonPoints[len(toons) - 1]
        xyz, h = toonPointList[i]
        toon.setPos(xyz)
        toon.setH(h)


def populateList(l: list, n: int = 4, value=None) -> None:
    """Populates a list up to n elements."""
    while len(l) < n:
        l.append(value)
