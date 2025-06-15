"""
A slightly extended Suit for the BMP.
"""
from panda3d.core import *
from direct.interval.IntervalGlobal import *

from toontown.avatar import Avatar
from toontown.battle.attacks.base.AttackEnum import AttackEnum
from toontown.battle.statuses import StatusEffectGlobals # not used here but prevents a circular import.
from toontown.battle.BattleAvatar import BattleAvatar
from toontown.toonbase import ToontownGlobals
from toontown.battle import BattleProps, SuitBattleGlobals
from toontown.suit import SuitTimings
from toontown.suit.Suit import Suit
from toontown.suit import SuitDNA
from toontown.toonbase import TTLocalizer, ToontownGlobals


class BMPSuit(Suit, BattleAvatar):
    HpTextGenerator = TextNode('HpTextGenerator')

    def __init__(self):
        Suit.__init__(self)
        BattleAvatar.__init__(self)
        self.hpText = None
        self.hpTextInterval = None
        self.hp = 1000
        self.maxHp = 1000

        self.superchargeRatio = 0

        from toontown.toonbase import TTRender
        from panda3d.otp import Nametag, NametagGroup
        # self.nametag = NametagGroup()
        # self.nametag.setAvatar(self)
        # self.nametag.setFont(ToontownGlobals.getInterfaceFont())
        # self.nametag2dContents = Nametag.CName | Nametag.CSpeech
        # self.nametag2dDist = Nametag.CName | Nametag.CSpeech
        # self.nametag2dNormalContents = Nametag.CName | Nametag.CSpeech
        # self.nametag3d = self.attachNewNode('nametag3d')
        # self.nametag3d.setTag('cam', 'nametag')
        # self.nametag3d.setLightOff()
        # TTRender.renderReflection(False, self.nametag3d, 'otp_avatar_nametag', None)
        # self.nametag3d.hide(TTRender.ShadowCameraBitmask)
        # self.nametagScale = 1.0
        # self.nametag.setNameWordwrap(8.0)
        # self.nametagJoint = self.find('**/joint_nameTag')
        # self.setPlayerType(NametagGroup.CCSuit)
        # self.initializeNametag3d()
        # self.showNametag3d()
        # self.showNametag2d()

        self.prop = None
        self.propInSound = base.loader.loadSfx('phase_5/audio/sfx/ENC_propeller_in.ogg')
        self.propOutSound = base.loader.loadSfx('phase_5/audio/sfx/ENC_propeller_out.ogg')
        self.lockProp = False

    def delete(self):
        # Get rid of sounds
        if self.propInSound:
            self.propInSound.stop()
            self.propInSound = None
        if self.propOutSound:
            self.propOutSound.stop()
            self.propOutSound = None
        Suit.delete(self)

    def initName(self):
        self.addActive()
        self.setPickable(0)

        nameInfo = self.createNameInfo()
        self.setName(nameInfo)
        self.setDisplayName(nameInfo)
        self.showNametag3d()
        self.hideNametag2d()

    def getStyleDept(self):
        if hasattr(self, 'dna') and self.dna:
            return SuitDNA.getDeptFullname(self.dna.dept)
        else:
            self.notify.error('called getStyleDept() before dna was set!')
            return 'unknown'

    def getHp(self):
        return self.hp  # we're a healthy boy!

    def reviveCheckAndClear(self):
        return 0

    def getMaxHp(self):
        return self.maxHp

    def getActualLevel(self):
        return 10

    def getDoId(self):
        return self.doId

    def getDamageMultiplier(self):
        return 1

    def showHpText(self, number, bonus=0, scale=1, attackTrack=-1, rounds=-1, extraText=''):
        if number != 0 or attackTrack == AttackEnum.TOON_LURE or attackTrack == AttackEnum.TOON_SUE:
            # Get rid of the number if it is already there.
            if self.hpText:
                self.hideHpText()
            # Set the font
            self.HpTextGenerator.setFont(ToontownGlobals.getSignFont())
            if number < 0 or attackTrack == AttackEnum.TOON_LURE:
                self.HpTextGenerator.setText(str(number))
                if attackTrack in TTLocalizer.RoundTrackTerms:
                    if attackTrack == AttackEnum.TOON_LURE:
                        if rounds == -2:
                            trackTerm = TTLocalizer.LuredImmune
                        elif rounds == -1:
                            trackTerm = TTLocalizer.LuredTrappedCog
                        elif rounds == 1:
                            trackTerm = TTLocalizer.LuredOneRound
                        else:
                            trackTerm = TTLocalizer.RoundTrackTerms.get(attackTrack) % rounds
                        self.HpTextGenerator.setText(trackTerm)
                    else:
                        self.HpTextGenerator.setText(str(number) + '\n' + TTLocalizer.RoundTrackTerms.get(attackTrack) % rounds)

            elif attackTrack == AttackEnum.TOON_SUE:
                self.HpTextGenerator.setText(TTLocalizer.CeaseAndDesist)
            else:
                self.HpTextGenerator.setText('+' + str(number))
            if extraText:
                self.HpTextGenerator.setText(self.HpTextGenerator.getText() + f'\n{extraText}')
            # No shadow
            self.HpTextGenerator.clearShadow()
            # Center the number
            self.HpTextGenerator.setAlign(TextNode.ACenter)
            # Red for negative, green for positive, yellow for bonus, orange for kb
            if bonus == 1:
                r = 1.0
                g = 1.0
                b = 0
                a = 1
            elif bonus == 2:
                r = 1.0
                g = 0.5
                b = 0
                a = 1
            elif number < 0:
                r = 0.9
                g = 0
                b = 0
                a = 1
            elif attackTrack == AttackEnum.TOON_LURE:
                if rounds == -1:
                    # Trapped
                    r = 1.0
                    g = 0.0
                    b = 0
                    a = 1
                else:
                    # Regular lured
                    r = 0.31
                    g = 0.75
                    b = 0.31
                    a = 1.0
            elif attackTrack == AttackEnum.TOON_SUE:
                r = 0.9
                g = 0.9
                b = 0.9
                a = 1.0
            else:
                r = 0
                g = 0.9
                b = 0
                a = 1

            self.HpTextGenerator.setTextColor(r, g, b, a)

            self.hpTextNode = self.HpTextGenerator.generate()

            # Put the hpText over the head of the avatar
            self.hpText = self.attachNewNode(self.hpTextNode)
            self.hpText.setScale(scale)
            self.hpText.setColorScaleOff(1)
            # Make sure it is a billboard
            self.hpText.setBillboardPointEye()
            # Render it after other things in the scene.
            self.hpText.setBin('fixed', 100)
            # Initial position ... Center of the body... the "tan tien"
            self.hpText.setPos(0, 0, self.height / 2)

            def setAlphaScale(value):
                if self.hpText:
                    self.hpText.setAlphaScale(value)

            # Fly the number out of the character
            self.hpTextInterval = Sequence(
                self.hpText.posInterval(1.0, Point3(0, 0, self.height + 1.5), blendType='easeOut'),
                Wait(0.85),
                LerpFunctionInterval(setAlphaScale, 0.5, fromData=1.0, toData=0.0),
                Func(self.hideHpText)
            )
            self.hpTextInterval.start()

    def hideHpText(self):
        try:
            if self.hpText:
                taskMgr.remove(self.uniqueName('hpText'))
                self.hpText.removeNode()
                self.hpText = None
            if self.hpTextInterval:
                self.hpTextInterval.finish()
                self.hpTextInterval = None
        except:
            pass

    def showHpString(self, text, duration = 0.85, scale = 0.7, color = (1, 0, 0, 1)):
        if text != '':
            if self.hpText:
                self.hideHpText()
            self.HpTextGenerator.setFont(ToontownGlobals.getSignFont())
            self.HpTextGenerator.setText(text)
            self.HpTextGenerator.clearShadow()
            self.HpTextGenerator.setAlign(TextNode.ACenter)
            self.HpTextGenerator.setTextColor(color)
            self.hpTextNode = self.HpTextGenerator.generate()
            self.hpText = self.attachNewNode(self.hpTextNode)
            self.hpText.setScale(scale)
            self.hpText.setColorScaleOff(1)
            self.hpText.setBillboardAxis()
            self.hpText.setPos(0, 0, self.height / 2)

            def setAlphaScale(value):
                if self.hpText:
                    self.hpText.setAlphaScale(value)

            self.hpTextInterval = Sequence(
                self.hpText.posInterval(1.0, Point3(0, 0, self.height + 1.5), blendType='easeOut'),
                Wait(duration),
                LerpFunctionInterval(setAlphaScale, 0.5, fromData=1.0, toData=0.0),
                Func(self.hideHpText)
            )
            self.hpTextInterval.start()

    def healSuit(self, amount, allowOverheal=False):

        if amount <= 0:
            return

        if not allowOverheal and self.hp + amount >= self.maxHp:
            self.hp = self.maxHp
        else:
            self.hp += amount
        if self.hp > self.maxHp:
            self.overhealed = 1
        else:
            self.overhealed = 0

    def setHp(self, hp):
        """
        Function:    set the current health of this suit, this can
                     be called during battle and at initialization
        Parameters:  hp, value to set health to
        """
        if hp > self.maxHp and not self.overhealed:
            self.hp = self.maxHp
        else:
            self.hp = hp
        if self.hp < self.maxHp:
            self.overhealed = 0

    def setSuperchargeRatio(self, ratio):
        self.superchargeRatio = ratio

    def resetSuperchargeState(self):
        self.superchargeRatio = 0

    def isSupercharged(self):
        if not self.superchargeRatio:
            return False
        return (self.hp / self.maxHp) >= (self.superchargeRatio * 0.999)

    def uniqueName(self, s):
        return f'{s}-{id(self)}'

    def taskName(self, s):
        return self.uniqueName(s)

    def attachPropeller(self):
        """
        attach a propeller to this suit, used when the suit
        is going into it's flying animation
        """
        if self.prop is None:
            self.prop = BattleProps.globalPropPool.getProp('propeller')
        head = self.find('**/to_head')
        if head.isEmpty():
            head = self.find('**/joint_head')

        self.prop.reparentTo(head)

    def setPropellerLocked(self, locked=False):
        self.lockProp = locked
        if not locked:
            self.detachPropeller()

    def detachPropeller(self):
        """
        remove the propeller from a suit if it has one, this
        is used after a suit is done with its flying anim
        """
        if self.lockProp:
            if self.prop:
                self.prop.hide()
            return

        if self.prop:
            self.prop.cleanup()
            self.prop.removeNode()
            self.prop = None

    def beginSupaFlyMove(self, pos, moveIn, trackName, walkAfterLanding=True, speed=1.0, soundSpeed=1.0, flyOutBasedOnCurrentPos=False):
        """
        beginSupaFlyMove(self, Point3 pos, bool moveIn, string trackName)
        Returns an interval that will animate the suit either up into
        the sky or back down to the ground, based on moveIn.
        pos is the point on the street over which the animation takes
        place.
        """

        skyPos = Point3(pos)
        initialZ = 0 if flyOutBasedOnCurrentPos else pos.getZ()
        # calculate a point in the sky based on how fast a suit walks
        # and how long it has been determined that flying away should take
        if moveIn == 1:
            skyPos.setZ(initialZ + SuitTimings.fromSky * ToontownGlobals.SuitWalkSpeed)
        elif moveIn == 2:
            skyPos.setZ(initialZ + (SuitTimings.fromSky - 4.5) * ToontownGlobals.SuitWalkSpeed)
        else:
            skyPos.setZ(initialZ + SuitTimings.toSky * ToontownGlobals.SuitWalkSpeed)


        # calculate some times used to manipulate the suit's landing
        # animation
        groundF = 28
        dur = self.getDuration('landing')
        fr = self.getFrameRate('landing')
        # length of time in animation spent in the air
        if fr:
            animTimeInAir = groundF / fr
        else:
            animTimeInAir = groundF
        animTimeInAir /= speed
        # length of time in animation spent impacting and reacting to
        # the ground
        impactLength = dur - animTimeInAir
        # the frame at which the suit touches the ground
        timeTillLanding = SuitTimings.fromSky - impactLength
        # time suit spends playing the flying portion of the landing anim
        if moveIn == 2:
            timeTillLanding = SuitTimings.fromSky - impactLength - 3
        waitTime = timeTillLanding - animTimeInAir

        # now create info for the propeller's animation
        if self.prop is None:
            self.prop = BattleProps.globalPropPool.getProp('propeller')
        propDur = self.prop.getDuration('propeller')
        lastSpinFrame = 8
        fr = self.prop.getFrameRate('propeller')
        # time from beginning of anim at which propeller plays its spin
        spinTime = lastSpinFrame / fr
        # time from beginning of anim at which propeller starts to close
        openTime = (lastSpinFrame + 1) / fr

        if moveIn:
            # if we are moving into the neighborhood from the sky, move
            # down from above (skyPos) the first waypoint in the suit's
            # current path (pos), first create an interval that will
            # move the suit over time, then create a function interval
            # to set the suit's animation to a single frame (the first)
            # of the landing animation, then create a wait interval to
            # wait for the suit to get closer to the ground, then create
            # an actor interval to play the landing animation so it ends
            # when the suit touches the ground, and lastly create a
            # function interval to make sure the suit goes into it's
            # walk animation once it lands

            # create the lerp intervals that will go in the first track,
            # also reparent the suit's shadow to render and set the
            # position of it below the suit on the ground
            lerpPosTrack = Sequence(self.posInterval(timeTillLanding, pos, startPos=skyPos), Wait(impactLength))
            shadowScale = self.dropShadow.getScale()
            # create a scale interval for the suit's shadow so it scales
            # up as the suit gets closer to the ground

            # keep Z scale at 1. so that lifter doesn't go crazy-go-nuts and set Z to infinity
            shadowTrack = Sequence(Func(self.dropShadow.reparentTo, render),
                                   Func(self.dropShadow.setPos, pos),
                                   self.dropShadow.scaleInterval(timeTillLanding, self.scale, startScale=Vec3(0.01, 0.01, 1.0)),
                                   Func(self.dropShadow.reparentTo, self.getShadowJoint()),
                                   Func(self.dropShadow.setPos, 0, 0, 0),
                                   Func(self.dropShadow.setScale, shadowScale))
            fadeInTrack = Sequence(Func(self.setTransparency, 1),
                                   self.colorScaleInterval(1, colorScale=VBase4(1, 1, 1, 1), startColorScale=VBase4(1, 1, 1, 0)),
                                   Func(self.clearColorScale),
                                   Func(self.clearTransparency))

            # now create the suit animation intervals that will go in the
            # second track
            animTrack = Sequence(Func(self.pose, 'landing', 0),
                                 Wait(waitTime),
                                 ActorInterval(self, 'landing', duration=dur))
            if walkAfterLanding:
                animTrack.append(Func(self.loop, 'walk'))

            # now create the propeller animation intervals that will go in
            # the third and final track
            self.attachPropeller()
            self.propInSound.setPlayRate(speed * soundSpeed)
            propTrack = Parallel(SoundInterval(self.propInSound, duration=waitTime + dur, node=self),
                                 Sequence(Func(self.prop.show),
                                          ActorInterval(self.prop, 'propeller', constrainedLoop=1, duration=waitTime + spinTime, startTime=0.0, endTime=spinTime),
                                          ActorInterval(self.prop, 'propeller', startTime=openTime, playRate=1.2),
                                          Func(self.detachPropeller)))
            return Parallel(lerpPosTrack,
                            shadowTrack,
                            fadeInTrack,
                            animTrack,
                            propTrack,
                            name=self.taskName('trackName'))
        else:
            # move to the sky, move vertically from the current
            # position to some location in the sky, also reparent the
            # suit's shadow to render and set the position of it below
            # the suit on the ground
            if flyOutBasedOnCurrentPos:
                referenceNode = render.attachNewNode(self.uniqueName("flyOutReferenceNode"))

                lerpPosTrack = Sequence(
                    Wait(impactLength),
                    Func(referenceNode.setPos, self, pos),
                    LerpPosInterval(self, timeTillLanding, skyPos, startPos=pos, other=referenceNode),
                    # Func(referenceNode.removeNode)  # Don't remove this node in the editor for BMP Suit
                )
            else:
                lerpPosTrack = Sequence(
                    Wait(impactLength),
                    LerpPosInterval(self, timeTillLanding, skyPos, startPos=pos)
                )
            # create a scale interval for the suit's shadow so it scales
            # down as the suit gets further from the ground

            # keep Z scale at 1. so that lifter doesn't go crazy-go-nuts and set Z to infinity
            shadowTrack = Sequence(Func(self.dropShadow.reparentTo, render),
                                   Func(self.dropShadow.setPos, self, pos) if flyOutBasedOnCurrentPos else Func(self.dropShadow.setPos, pos),
                                   self.dropShadow.scaleInterval(timeTillLanding, Vec3(0.01, 0.01, 1.0), startScale=self.scale),
                                   Func(self.dropShadow.reparentTo, self.getShadowJoint()),
                                   Func(self.dropShadow.setPos, 0, 0, 0))
            fadeOutTrack = Sequence(Func(self.setTransparency, 1),
                                    self.colorScaleInterval(1, colorScale=VBase4(1, 1, 1, 0), startColorScale=VBase4(1, 1, 1, 1)),
                                    Func(self.clearColorScale),
                                    Func(self.clearTransparency),
                                    Func(self.reparentTo, hidden))
            actInt = ActorInterval(self, 'landing', loop=0, startTime=dur, endTime=0.0)
            # now create the propeller animation intervals that will go in
            # the third and final track
            self.attachPropeller()
            self.prop.hide()
            propTrack = Parallel(SoundInterval(self.propOutSound, duration=waitTime + dur, node=self),
                                 Sequence(Func(self.prop.show),
                                          ActorInterval(self.prop, 'propeller', endTime=openTime, startTime=propDur),
                                          ActorInterval(self.prop, 'propeller', constrainedLoop=1, duration=propDur - openTime, startTime=spinTime, endTime=0.0),
                                          Func(self.detachPropeller)))
            return Parallel(ParallelEndTogether(lerpPosTrack,
                                                shadowTrack,
                                                fadeOutTrack),
                            actInt,
                            propTrack,
                            name=self.taskName('trackName'))

    def setChatAbsolute(self, chatString, chatFlags, dialogue=None, interrupt=1, wantBalloonAnim=True, wantHeadAnim=True, wantSound=True):
        Avatar.Avatar.setChatAbsolute(self, chatString, chatFlags, dialogue, interrupt, wantBalloonAnim, wantSound=wantSound)

        # Copy pasting this function to remove the self.cr call

        if self.specialHead and wantHeadAnim:
            type = self.getDialogTypeName(chatString)
            animation = type if type in self.specialHead.getAnimNames() else 'talk'
            seq = Sequence(ActorInterval(self.specialHead, animation), Func(self.specialHead.loopNeutral))
            seq.start()

    def onSuitAttackBegin(self):
        # Run through all visual effects and call this
        for ve in self.getVisualEffects():
            ve.onSuitAttackBegin()

    def onSuitAttackEnd(self):
        # Run through all visual effects and call this
        for ve in self.getVisualEffects():
            ve.onSuitAttackEnd()


# -=- Methods for ease of suit creation -=-
def createSuitOfName(name: str, actualLevel: int = 0) -> BMPSuit:
    suit = BMPSuit()
    d = SuitDNA.SuitDNA()
    d.newSuit(name)
    suit.setDNA(d)
    suit.loop('neutral', 0)
    setattr(suit, 'dna', d)
    setattr(suit, 'getLevel', lambda: 0)
    if actualLevel:
        setattr(suit, 'getActualLevel', lambda: actualLevel)
    setattr(suit, 'getStyleName', lambda: name)
    setattr(suit, 'battleTrapProp', None)
    suit.initName()
    if name in SuitBattleGlobals.ALWAYS_SKELECOGS:
        suit.makeSkeleton()
    return suit


def createSuitRandom(level=None, dept=None, invading=False, wantAlts=True, actualLevel: int = 0) -> BMPSuit:
    suit = BMPSuit()
    d = SuitDNA.SuitDNA()
    d.newSuitRandom(level, dept, invading, wantAlts)
    suit.setDNA(d)
    suit.loop('neutral', 0)
    setattr(suit, 'dna', d)
    setattr(suit, 'getLevel', lambda: 0)
    if actualLevel:
        setattr(suit, 'getActualLevel', lambda: actualLevel)
    setattr(suit, 'getStyleName', lambda: d.name)
    setattr(suit, 'battleTrapProp', None)
    suit.initName()
    return suit
