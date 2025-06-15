from toontown.suit.BossCog import *
import random


class BMPBossCog(BossCog):
    def __init__(self):
        super().__init__()
        self.flashInterval = None

    def setAttackCode(self, attackCode, avId = 0):
        self.attackCode = attackCode
        self.attackAvId = avId
        if attackCode == ToontownGlobals.BossCogDizzy:
            self.setDizzy(1)
            self.cleanupAttacks()
            self.doAnimate(None, raised=0, happy=1)
        elif attackCode == ToontownGlobals.BossCogDizzyNow:
            self.setDizzy(1)
            self.cleanupAttacks()
            self.doAnimate('hit', happy=1, now=1)
        elif attackCode == ToontownGlobals.BossCogSwatLeft:
            self.setDizzy(0)
            self.doAnimate('ltSwing', now=1)
        elif attackCode == ToontownGlobals.BossCogSwatRight:
            self.setDizzy(0)
            self.doAnimate('rtSwing', now=1)
        elif attackCode == ToontownGlobals.BossCogAreaAttack:
            self.setDizzy(0)
            self.doAnimate('areaAttack', now=1)
        elif attackCode == ToontownGlobals.BossCogFrontAttack:
            self.setDizzy(0)
            self.doAnimate('frontAttack', now=1)
        elif attackCode == ToontownGlobals.BossCogRecoverDizzyAttack:
            self.setDizzy(0)
            self.doAnimate('frontAttack', now=1)
        elif attackCode == ToontownGlobals.BossCogDirectedAttack or attackCode == ToontownGlobals.BossCogSlowDirectedAttack:
            self.setDizzy(0)
            self.doDirectedAttack(avId, attackCode)
        elif attackCode == ToontownGlobals.BossCogNoAttack:
            self.setDizzy(0)
            self.doAnimate(None, raised=1)

    def disable(self):
        self.cleanupFlash()
        super().disable()

    def cleanupAttacks(self):
        pass

    def cleanupFlash(self):
        if self.flashInterval:
            self.flashInterval.finish()
            self.flashInterval = None

    def flashRed(self):
        self.cleanupFlash()
        self.setColorScale(1, 1, 1, 1)
        i = Sequence(self.colorScaleInterval(0.1, colorScale=VBase4(1, 0, 0, 1)), self.colorScaleInterval(0.3, colorScale=VBase4(1, 1, 1, 1)))
        self.flashInterval = i
        i.start()

    def flashGreen(self):
        self.cleanupFlash()
        if not self.isEmpty():
            self.setColorScale(1, 1, 1, 1)
            i = Sequence(self.colorScaleInterval(0.1, colorScale=VBase4(0, 1, 0, 1)), self.colorScaleInterval(0.3, colorScale=VBase4(1, 1, 1, 1)))
            self.flashInterval = i
            i.start()

    @staticmethod
    def getGearFrisbee():
        return loader.loadModel('phase_9/models/char/gearProp')

    @staticmethod
    def getBookFrisbee():
        model = loader.loadModel('phase_5/models/props/lawbook')
        cBox = CollisionBox(0, 0.5, 0.5, 0.25)
        cBox.setTangible(0)
        cn = CollisionNode('BossZap')
        cn.addSolid(cBox)
        cn.setCollideMask(ToontownGlobals.WallBitmask)
        model.attachNewNode(cn)
        return model

    def doDirectedAttack(self, avId, attackCode):
        toon = base.cr.doId2do.get(avId)
        if toon:
            gearRoot = self.rotateNode.attachNewNode('gearRoot')
            gearRoot.setZ(10)
            gearRoot.setTag('attackCode', str(attackCode))
            if attackCode in (ToontownGlobals.BossCogBookDirectedAttack, ToontownGlobals.BossCogSpreadBookDirectedAttack):
                gearModel = self.getBookFrisbee()
                gearModel.setScale(3.0)
            else:
                gearModel = self.getGearFrisbee()
                gearModel.setScale(0.2)
            gearRoot.headsUp(toon)
            toToonH = PythonUtil.fitDestAngle2Src(0, gearRoot.getH() + 180)
            gearRoot.lookAt(toon)
            neutral = 'Fb_neutral'
            if not self.twoFaced:
                neutral = 'Ff_neutral'
            gearTrack = Parallel()
            timesToDo = 3 if attackCode == ToontownGlobals.BossCogSpreadBookDirectedAttack else 1
            xRanges = [0, -10, 10]
            for i in range(timesToDo):
                for j in range(4):
                    node = gearRoot.attachNewNode(str(i))
                    node.hide()
                    node.setPos(0, 5.85, 4.0)
                    gearModel.instanceTo(node)
                    x = xRanges[i] + random.uniform(-5, 5)
                    z = random.uniform(-3, 3)
                    mult = 1
                    if self.dna.dept == 'l':
                        mult = 2
                    h = random.uniform(-720, 720)
                    gearTrack.append(Sequence(
                        Wait(j * 0.15),
                        Func(node.show),
                        Parallel(
                            node.posInterval(1, Point3(x, 50, z), fluid=1),
                            node.hprInterval(1, VBase3(h*mult, 0, 0), fluid=1)
                        ),
                        Func(node.detachNode)
                    ))
            gearTrack = Sequence(gearTrack)
            if not self.raised:
                neutral1Anim = self.getAnim('down2Up')
                self.raised = 1
            else:
                neutral1Anim = ActorInterval(self, neutral, startFrame=48)
            throwAnim = self.getAnim('throw')
            neutral2Anim = ActorInterval(self, neutral)
            extraAnim = Sequence()
            if attackCode == ToontownGlobals.BossCogSlowDirectedAttack:
                extraAnim = ActorInterval(self, neutral)
            seq = Sequence(
                ParallelEndTogether(
                    self.pelvis.hprInterval(1, VBase3(toToonH, 0, 0)),
                    neutral1Anim
                ),
                extraAnim,
                Parallel(
                    Sequence(
                        Wait(0.19),
                        gearTrack,
                        Func(gearRoot.detachNode),
                        self.pelvis.hprInterval(0.2, VBase3(0, 0, 0))
                    ),
                    Sequence(throwAnim, neutral2Anim)
                )
            )
            self.doAnimate(seq, now=1, raised=1)


# -=- Methods for ease of boss creation -=-
def createBossOfDept(dept: str) -> BMPBossCog:
    boss = BMPBossCog()
    d = SuitDNA.SuitDNA()
    d.newBossCog(dept)
    boss.setDNAString(d.makeNetString())
    boss.loop('Ff_neutral', 0)
    return boss


def createBossRandom() -> BMPBossCog:
    return createBossOfDept(random.choice(['s', 'm', 'l', 'c']))
