import random

from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import lerp
from panda3d.core import TransparencyAttrib

from toontown.utils.ColorHelper import hexToPCol
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory


@DirectNotifyCategory()
class LavaLamp(Actor):
    """
    A cute lava lamp model.
    It's very, very, very cute
    """

    modelPath = 'phase_8/models/props/ttcc_prop_lavalamp-zero'
    idleAnimPath = 'phase_8/models/props/ttcc_prop_lavalamp-idle'

    shadowPath = 'phase_3/models/props/drop_shadow'

    colors = (
        ('BA2E28', 'BA682C'),
        ('65BA3B', '4BBA8B'),
        ('3B7BBA', '4032B6'),
        ('9028BA', 'BA296F'),
        ('BAB51C', '5CBA29'),
    )
    colorDuration = 3.0

    def __init__(self, colorIndex: int = 0):
        super().__init__(
            self.modelPath,
            anims={'idle': self.idleAnimPath},
            flattenable=0,
            setFinal=1,
        )
        self.setBlend(frameBlend=base.wantSmoothAnims)  # the frames cannot blend

        # Run the actor interval.
        middleFrame = 40 * colorIndex
        self.idleInterval = Sequence(
            ActorInterval(
                actor=self, animName='idle',
                startFrame=middleFrame, endFrame=199,
            ),
            Func(self.pose, 'idle', 0),
            ActorInterval(
                actor=self, animName='idle',
                startFrame=0, endFrame=middleFrame,
            ),
        )
        self.idleInterval.loop()
        self.idleInterval.setT(random.random() * self.idleInterval.getDuration())

        # Apply a color sequence.
        self.lava = self.find('**/lava')
        colorIndex = colorIndex % len(self.colors)
        self.startColor, self.endColor = list(map(hexToPCol, self.colors[colorIndex]))
        self.colorInterval = Sequence(
            LerpFunctionInterval(
                self.updateColor, duration=self.colorDuration,
                fromData=0.0, toData=1.0,
            ),
            LerpFunctionInterval(
                self.updateColor, duration=self.colorDuration,
                fromData=1.0, toData=0.0,
            ),
        )
        self.colorInterval.loop()
        self.colorInterval.setT(random.random() * self.colorInterval.getDuration())

        self.shadow = loader.loadModel(self.shadowPath)
        self.shadow.reparentTo(self)
        self.shadow.flattenLight()
        self.shadow.setScale(0.30)
        self.shadow.setZ(0.025)
        self.shadow.setColor(0, 0, 0, 0.5)
        self.shadow.setTransparency(TransparencyAttrib.MAlpha)

    def cleanup(self):
        self.idleInterval.finish()
        self.idleInterval = None
        self.colorInterval.finish()
        self.colorInterval = None
        self.lava = None
        self.shadow = None
        super().cleanup()

    def removeNode(self):
        super().removeNode()

    def updateColor(self, t):
        self.lava.setColor(tuple(map(lambda x, y: lerp(x, y, t), self.startColor, self.endColor)))

    def setStartColor(self, pCol: tuple | None = None):
        if pCol is None:
            self.startColor = hexToPCol(self.getDefaultStartColor())
        else:
            self.startColor = pCol

    def setEndColor(self, pCol: tuple | None = None):
        if pCol is None:
            self.endColor = hexToPCol(self.getDefaultEndColor())
        else:
            self.endColor = pCol

    def setSpeed(self, speed: float):
        self.idleInterval.setPlayRate(speed)
        self.colorInterval.setPlayRate(speed)

    def getDefaultStartColor(self) -> str:
        return self.colors[0][0]

    def getDefaultEndColor(self) -> str:
        return self.colors[0][1]
