from direct.showbase.PythonUtil import lerp

from toontown.battle import BattleProps, MovieUtil
from toontown.battle.BattleProps import globalPropPool
from toontown.cutscene.editor.CSEditorEnums import EventDefinitionEnum as EDE
from toontown.cutscene.editor.CSEditorEnums import SubEventArgumentType as SEAT
from toontown.cutscene.CutsceneSequenceBase import cutsceneSequence, getUniqueCutsceneId
from toontown.cutscene.CutsceneSequenceHelpers import getHprBetweenPoints, NodePathWithState

from panda3d.core import Point3, LVecBase3f
from direct.interval.IntervalGlobal import *

from toontown.effects import DustCloud

"""
Methods to help generate positions/etc for sequences.
"""


def createSuitMoveIval(suit, destPos, duration, gravityMult=0.4):
    """
    Creates a sequence which moves the suit using propeller in a projectile arc.
    """
    dur = suit.getDuration('landing')
    fr = suit.getFrameRate('landing')
    landingDur = dur
    totalDur = duration
    animTimeInAir = totalDur - dur
    flyingDur = animTimeInAir
    moveIval = Sequence(Func(suit.pose, 'landing', 0),
                        ProjectileInterval(suit, duration=flyingDur, endPos=destPos,
                                           gravityMult=gravityMult), ActorInterval(suit, 'landing'))
    if suit.prop is None:
        suit.prop = BattleProps.globalPropPool.getProp('propeller')
    propDur = suit.prop.getDuration('propeller')
    lastSpinFrame = 8
    fr = suit.prop.getFrameRate('propeller')
    spinTime = lastSpinFrame / fr
    openTime = (lastSpinFrame + 1) / fr
    propTrack = Parallel(SoundInterval(suit.propInSound, duration=flyingDur, node=suit), Sequence(
        ActorInterval(suit.prop, 'propeller', constrainedLoop=1, duration=flyingDur + 1, startTime=0.0,
                      endTime=spinTime),
        ActorInterval(suit.prop, 'propeller', duration=landingDur, startTime=openTime), Func(suit.detachPropeller)))

    result = Parallel(
        Sequence(
            Func(suit.attachPropeller),
            ActorInterval(suit.prop, 'propeller', startFrame=lastSpinFrame, endFrame=suit.prop.getNumFrames('propeller'), playRate=-1.6),
        ),
        Sequence(
            Wait(0.5),
            Parallel(
                moveIval,
                propTrack
            )
        ),
    )
    return result


"""
All cutscene sequences
"""


@cutsceneSequence(name='Suit: Show', enum=EDE.showSuit)
def seq_showSuit(suitIndex:     SEAT.dropdown_suits = 0,
                 cutsceneDict:  dict = None) -> Parallel:
    retParallel = Parallel()
    suit = cutsceneDict['suits'][suitIndex]
    if not suit:
        return Sequence()
    retParallel.append(Func(suit.unstash))
    # retParallel.append(Func(suit.showNametag2d))
    retParallel.append(Func(suit.showNametag3d))
    return retParallel


@cutsceneSequence(name='Suit: Hide', enum=EDE.hideSuit)
def seq_hideSuit(suitIndex:     SEAT.dropdown_suits = 0,
                 cutsceneDict:  dict = None) -> Parallel:
    """Hides a suit."""
    retParallel = Parallel()
    suit = cutsceneDict['suits'][suitIndex]
    if not suit:
        return Sequence()
    retParallel.append(Func(suit.stash))
    retParallel.append(Func(suit.hideNametag2d))
    retParallel.append(Func(suit.hideNametag3d))
    return retParallel


@cutsceneSequence(name='Suit: Show All', enum=EDE.showSuits)
def seq_showSuits(cutsceneDict: dict = None) -> Parallel:
    retParallel = Parallel()
    for suit in cutsceneDict['suits']:
        if not suit:
            continue
        retParallel.append(Func(suit.unstash))
        # retParallel.append(Func(suit.showNametag2d))
        retParallel.append(Func(suit.showNametag3d))
    return retParallel


@cutsceneSequence(name='Suit: Hide All', enum=EDE.hideSuits)
def seq_hideSuits(cutsceneDict: dict = None) -> Parallel:
    retParallel = Parallel()
    for suit in cutsceneDict['suits']:
        if not suit:
            continue
        retParallel.append(Func(suit.stash))
        retParallel.append(Func(suit.hideNametag2d))
        retParallel.append(Func(suit.hideNametag3d))
    return retParallel


@cutsceneSequence(name='Suit: Animation', enum=EDE.doSuitAnim)
def seq_suitAnim(suitIndex:     SEAT.dropdown_suits = 0,
                 anim:          SEAT.dropdown_suit_anims = 'neutral',
                 loop:          SEAT.boolean = 0,
                 hasDuration:   SEAT.boolean = 0,
                 duration:      SEAT.slider_min_zero = 0,
                 hasStartTime:  SEAT.boolean = 0,
                 startTime:     SEAT.slider_min_zero = 0,
                 hasEndTime:    SEAT.boolean = 0,
                 endTime:       SEAT.slider_min_zero = 0,
                 playRate:      SEAT.slider_float = 1,
                 useEndAnim:    SEAT.boolean = 0,
                 endAnim:       SEAT.dropdown_suit_anims = 'neutral',
                 isInterval:    SEAT.boolean = 1,
                 oldStyleEndAnim: SEAT.boolean = 1,
                 cutsceneDict:  dict = None) -> Sequence:
    """Makes a suit do an animation."""
    suit = cutsceneDict['suits'][suitIndex]
    if not suit:
        return Sequence()
    if not hasDuration:
        duration = None
    if not hasStartTime:
        startTime = None
    if not hasEndTime:
        endTime = None
    if not useEndAnim:
        endAnim = None
    playRate = playRate if playRate else 1.0  # do not let equal 0
    # some math in case we run as a func and not an interval
    animDuration = suit.getDuration(anim)
    animFrameCount = suit.getNumFrames(anim)
    startFrame = round((startTime / max(animDuration, 0.01)) * animFrameCount) if startTime else 0
    endFrame = round((endTime / max(animDuration, 0.01)) * animFrameCount) if endTime else animFrameCount

    if not loop:
        ival = ActorInterval(
            suit, anim, loop=loop, duration=duration,
            startTime=startTime, endTime=endTime,
            playRate=playRate
        ) if isInterval else Func(
            suit.play, anim, None, startFrame, endFrame
        )
        # Ensure that cutscenes which use the old version are still compatible.
        # TODO: do something about this post 1.3
        if oldStyleEndAnim:
            return Parallel(
                ival,
                Sequence(
                    Wait(duration),
                    ActorInterval(suit, endAnim)
                ) if duration and endAnim else Sequence(),
            )
        if duration:
            return Parallel(
                ival,
                Sequence(
                    Wait(duration),
                    Func(suit.loop, endAnim)
                ),
            )
        elif endAnim:
            return Sequence(ival, Func(suit.loop, endAnim))
        return Sequence(ival)
    else:
        return Sequence(
            Func(suit.loop, anim),
        )


@cutsceneSequence(name='Suit: Blend Animation', enum=EDE.doSuitBlendAnim)
def seq_suitBlendAnim(suitIndex:     SEAT.dropdown_suits = 0,
                      fromAnim:      SEAT.dropdown_suit_anims = 'neutral',
                      toAnim:        SEAT.dropdown_suit_anims = 'neutral',
                      continueToAnim: SEAT.boolean = True,
                      duration:      SEAT.slider_min_zero = 0,
                      hasFromStartTime:  SEAT.boolean = 0,
                      fromStartTime:     SEAT.slider_min_zero = 0,
                      hasFromEndTime:    SEAT.boolean = 0,
                      fromEndTime:       SEAT.slider_min_zero = 0,
                      hasToStartTime:  SEAT.boolean = 0,
                      toStartTime:     SEAT.slider_min_zero = 0,
                      hasToEndTime:    SEAT.boolean = 0,
                      toEndTime:       SEAT.slider_min_zero = 0,
                      # playRate:      SEAT.slider_float = 1,
                      blendType:     SEAT.dropdown_blendType = 'easeInOut',
                      cutsceneDict:  dict = None) -> Sequence:
    av = cutsceneDict['suits'][suitIndex]
    if not av:
        return Sequence()
    if not hasFromStartTime:
        fromStartTime = None
    if not hasFromEndTime:
        fromEndTime = None
    if not hasToStartTime:
        toStartTime = None
    if not hasToEndTime:
        toEndTime = None

    # some math in case we run as a func and not an interval
    '''
    # fromAnim
    animDuration = av.getDuration(fromAnim)
    animFrameCount = av.getNumFrames(fromAnim)
    fromStartFrame = round((fromStartTime / max(animDuration, 0.01)) * animFrameCount) if fromStartTime else 0
    fromEndFrame = round((fromEndTime / max(animDuration, 0.01)) * animFrameCount) if fromEndTime else animFrameCount

    # toAnim
    animDuration = av.getDuration(toAnim)
    animFrameCount = av.getNumFrames(toAnim)
    toStartFrame = round((toStartTime / max(animDuration, 0.01)) * animFrameCount) if toStartTime else 0
    toEndFrame = round((toEndTime / max(animDuration, 0.01)) * animFrameCount) if toEndTime else animFrameCount
    '''

    animSeq = Parallel(ActorInterval(av, toAnim, loop=True, duration=duration,
                                     startTime=toStartTime, endTime=toEndTime))
    # Add animation blending between neutral and the animation
    animSeq.append(
        ActorInterval(av, fromAnim, duration=duration,
                      startTime=fromStartTime, endTime=fromEndTime)
    )
    animSeq.append(
        LerpAnimInterval(
            av,
            duration,
            fromAnim,
            toAnim,
            blendType=blendType,
        )
    )

    animSeq = Sequence(
        Func(
            av.setBlend,
            frameBlend=base.wantSmoothAnims,
            animBlend=True,
        ),
        Func(av.stop),
        animSeq,
        Func(
            av.setBlend,
            frameBlend=base.wantSmoothAnims,
            animBlend=False,
        ),
    )

    if continueToAnim:
        animSeq.append(ActorInterval(av, toAnim, startTime=toEndTime))

    return animSeq


@cutsceneSequence(name='Suit: Pingpong', enum=EDE.doSuitPingpong)
def seq_suitPingpong(suitIndex:     SEAT.dropdown_suits = 0,
                 anim:          SEAT.dropdown_suit_anims = 'neutral',
                 loop:          SEAT.boolean = 0,
                 hasDuration:   SEAT.boolean = 0,
                 duration:      SEAT.slider_min_zero = 0.0,
                 startTime:     SEAT.slider_min_zero = 0,
                 endTime:       SEAT.slider_min_zero = 0,
                 cutsceneDict:  dict = None) -> Sequence:
    """Makes a suit pingpong an animation."""
    suit = cutsceneDict['suits'][suitIndex]
    if not suit:
        return Sequence()
    if not hasDuration:
        duration = None
    # some math in case we run as a func and not an interval
    animDuration = suit.getDuration(anim)
    animFrameCount = suit.getNumFrames(anim)
    startFrame = round((startTime / max(animDuration, 0.01)) * animFrameCount) if startTime else 0
    endFrame = round((endTime / max(animDuration, 0.01)) * animFrameCount) if endTime else animFrameCount

    track = Sequence(
        Func(suit.pingpong, anim, loop, None, startFrame, endFrame)
    )

    if hasDuration:
        track.append(
            Sequence(
                Wait(duration),
                Func(suit.loop, 'neutral')
            )
        )

    return track


@cutsceneSequence(name='Suit: Animate All', enum=EDE.animateAllSuits)
def seq_allSuitsDoAnim(startAnim:       SEAT.dropdown_suit_anims = 'neutral',
                       loop:            SEAT.boolean = 0,
                       hasDuration:     SEAT.boolean = 0,
                       duration:        SEAT.slider_min_zero = 0,
                       hasStartTime:    SEAT.boolean = 0,
                       startTime:       SEAT.slider_min_zero = 0,
                       hasEndTime:      SEAT.boolean = 0,
                       endTime:         SEAT.slider_min_zero = 0,
                       playRate:        SEAT.slider_float = 1.0,
                       useEndAnim:      SEAT.boolean = 0,
                       endAnim:         SEAT.dropdown_suit_anims = 'neutral',
                       isInterval:      SEAT.boolean = 0,
                       cutsceneDict:    dict = None) -> Parallel:
    if not hasDuration:
        duration = None
    if not hasStartTime:
        startTime = None
    if not hasEndTime:
        endTime = None
    if not useEndAnim:
        endAnim = None
    retParallel = Parallel()
    for suit in cutsceneDict['suits']:
        if not suit:
            continue
        playRate = playRate if playRate else 1.0  # do not let equal 0
        # some math in case we run as a func and not an interval
        animDuration = suit.getDuration(startAnim)
        animFrameCount = suit.getNumFrames(startAnim)
        startFrame = round((startTime / max(animDuration, 0.01)) * animFrameCount) if startTime else 0
        endFrame = round((endTime / max(animDuration, 0.01)) * animFrameCount) if endTime else animFrameCount

        if not loop:
            retParallel.append(Parallel(
                ActorInterval(suit, startAnim, loop=loop, duration=duration,
                              startTime=startTime, endTime=endTime,
                              playRate=playRate) if isInterval else Func(
                    suit.play, startAnim, None, startFrame, endFrame
                ),
                Sequence(
                    Wait(duration),
                    ActorInterval(suit, endAnim)
                ) if duration and endAnim else Sequence(),
            ))
        else:
            retParallel.append(Sequence(
                Func(suit.loop, startAnim),
            ))
    return retParallel


@cutsceneSequence(name='Suit: Pingpong All', enum=EDE.pingpongAllSuits)
def seq_allSuitPingpong(anim:          SEAT.dropdown_suit_anims = 'neutral',
                        loop:          SEAT.boolean = 0,
                        hasDuration:   SEAT.boolean = 0,
                        duration:      SEAT.slider_min_zero = 0.0,
                        startTime:     SEAT.slider_min_zero = 0,
                        endTime:       SEAT.slider_min_zero = 0,
                        cutsceneDict:  dict = None) -> Sequence:
    """Makes all suits pingpong an animation."""
    track = Parallel()

    for i in range(len(cutsceneDict['suits'])):
        suit = cutsceneDict['suits'][i]
        if not suit:
            continue
        track.append(seq_suitPingpong(i, anim, loop, hasDuration, duration, startTime, endTime))

    return track


@cutsceneSequence(name='Suit: Head Animation', enum=EDE.doSuitHeadAnim)
def seq_suitHeadAnim(suitIndex:     SEAT.dropdown_suits = 0,
                     anim:          SEAT.dropdown_suit_head_anims = 'neutral',
                     loop:          SEAT.boolean = 0,
                     hasDuration:   SEAT.boolean = 0,
                     duration:      SEAT.slider_min_zero = 0,
                     hasStartTime:  SEAT.boolean = 0,
                     startTime:     SEAT.slider_min_zero = 0,
                     hasEndTime:    SEAT.boolean = 0,
                     endTime:       SEAT.slider_min_zero = 0,
                     playRate:      SEAT.slider_float = 1,
                     useEndAnim:    SEAT.boolean = 0,
                     endAnim:       SEAT.dropdown_suit_head_anims = 'neutral',
                     isInterval:    SEAT.boolean = 1,
                     cutsceneDict:  dict = None) -> Sequence:
    """Makes a suit's head do an animation."""
    suit = cutsceneDict['suits'][suitIndex]
    if not suit or not suit.specialHead:
        return Sequence()
    if not hasDuration:
        duration = None
    if not hasStartTime:
        startTime = None
    if not hasEndTime:
        endTime = None
    if not useEndAnim:
        endAnim = None
    playRate = playRate if playRate else 1.0  # do not let equal 0
    # some math in case we run as a func and not an interval
    animDuration = suit.specialHead.getDuration(anim)
    animFrameCount = suit.specialHead.getNumFrames(anim)
    startFrame = round((startTime / max(animDuration, 0.01)) * animFrameCount) if startTime else 0
    endFrame = round((endTime / max(animDuration, 0.01)) * animFrameCount) if endTime else animFrameCount

    if not loop:
        return Parallel(
            ActorInterval(suit.specialHead, anim, loop=loop, duration=duration,
                          startTime=startTime, endTime=endTime,
                          playRate=playRate) if isInterval else Func(
                suit.specialHead.play, anim, None, startFrame, endFrame
            ),
            Sequence(
                Wait(duration),
                ActorInterval(suit.specialHead, endAnim)
            ) if duration and endAnim else Sequence(),
        )
    else:
        return Sequence(
            Func(suit.specialHead.loop, anim),
        )


@cutsceneSequence(name='Suit: Unchat All', enum=EDE.clearAllSuitChat)
def seq_allSuitsClearChat(cutsceneDict: dict = None) -> Parallel:
    retParallel = Parallel()
    for suit in cutsceneDict['suits']:
        if not suit:
            continue
        retParallel.append(Func(suit.clearChat))
    return retParallel


"""
Suit Spawning Sequences
"""


@cutsceneSequence(name='Suit: Lock Propeller', enum=EDE.suitLockPropeller)
def seq_suitLockPropeller(suitIndex:    SEAT.dropdown_suits = 0,
                          locked:       SEAT.boolean = 0,
                          cutsceneDict: dict = None) -> Sequence:
    seq = Sequence()

    suit = cutsceneDict['suits'][suitIndex]
    if not suit:
        return Sequence()

    seq.append(Func(suit.setPropellerLocked, locked))
    return seq


@cutsceneSequence(name='Suit: Supa Fly', enum=EDE.suitSupaFly)
def seq_suitFly(suitIndex:      SEAT.dropdown_suits = 0,
                delay:          SEAT.slider_min_zero = 0,
                destPos:        SEAT.slider_xyz = (0, 0, 0),
                flyType:        SEAT.dropdown_suitFlyChoice = 0,
                getPos:         SEAT.dropdown_suitFlyPosChoice = 0,
                speed:          SEAT.slider_min_almost_zero = 1.0,
                cutsceneDict:   dict = None) -> Sequence:
    retParallel = Sequence()

    suit = cutsceneDict['suits'][suitIndex]
    if not suit:
        return Sequence()
    if flyType == 0:
        return Sequence()

    if getPos == 0:
        retParallel.append(Sequence(Wait(delay), suit.beginSupaFlyMove(Point3(*destPos), flyType - 1, None, False, speed=speed)))
        return retParallel
    else:
        retParallel.append(
            Sequence(Wait(delay), suit.beginSupaFlyMove(Point3(*destPos), flyType - 1, None, False, speed=speed, flyOutBasedOnCurrentPos=True)))
        return retParallel


@cutsceneSequence(name='Suit: Projectile Fly', enum=EDE.suitProjectileFly)
def seq_suitProjectileFly(suitIndex:    SEAT.dropdown_suits = 0,
                          delay:        SEAT.slider_min_zero = 0,
                          flyDuration:  SEAT.slider_min_zero = 4.0,
                          gravityMult:  SEAT.slider_min_zero = 0.4,
                          destPos:      SEAT.slider_xyz = (0, 0, 0),
                          cutsceneDict: dict = None) -> Sequence:

    suit = cutsceneDict['suits'][suitIndex]
    if not suit:
        return Sequence()
    destPos = Point3(*destPos)
    moveIval = createSuitMoveIval(suit, destPos, duration=flyDuration, gravityMult=gravityMult)
    suitTrack = Sequence(
        Wait(delay),
        moveIval,
        Func(suit.loop, 'neutral'),
    )

    return suitTrack


@cutsceneSequence(name='Suit: Turn All to Node', enum=EDE.turnSuitsToNode)
def seq_turnSuitsToNode(nodeIndex:      SEAT.dropdown_node = None,
                        duration:       SEAT.slider_min_zero = 0,
                        blendType:      SEAT.dropdown_blendType = 'easeInOut',
                        anim:           SEAT.dropdown_suit_anims = 'walk',
                        offset:         SEAT.slider_xyz = (0, 0, 0),
                        cutsceneDict:   dict = None) -> Parallel:
    retseq = Parallel()

    for i, suit in enumerate(cutsceneDict['suits']):
        if not suit:
            continue
        # Point each toon individually.
        retseq.append(
            seq_turnSingleSuitToNode(suitIndex=i, nodeIndex=nodeIndex, duration=duration,
                                      blendType=blendType, anim=anim, offset=offset,
                                      cutsceneDict=cutsceneDict)
        )

    return retseq


@cutsceneSequence(name='Suit: Turn One to Node', enum=EDE.turnSingleSuitToNode)
def seq_turnSingleSuitToNode(suitIndex:     SEAT.dropdown_suits = 0,
                             nodeIndex:     SEAT.dropdown_node = None,
                             duration:      SEAT.slider_min_zero = 0.0,
                             blendType:     SEAT.dropdown_blendType = 'easeInOut',
                             anim:          SEAT.dropdown_suit_anims = 'walk',
                             offset:        SEAT.slider_xyz = (0, 0, 0),
                             cutsceneDict:  dict = None) -> Parallel:
    def getNodePos():
        return cutsceneDict['nodes'][nodeIndex].getPos(render) + LVecBase3f(*offset)
    return seq_turnSingleSuitToPoint(
        suitIndex=suitIndex, point=getNodePos,
        duration=duration, blendType=blendType, anim=anim, cutsceneDict=cutsceneDict
    )


@cutsceneSequence(name='Suit: Turn Single to Point', enum=EDE.turnSingleSuitToPoint)
def seq_turnSingleSuitToPoint(suitIndex:    SEAT.dropdown_suits = 0,
                              point:        SEAT.slider_xyz = (0, 0, 0),
                              duration:     SEAT.slider_min_zero = 0.0,
                              blendType:    SEAT.dropdown_blendType = 'easeInOut',
                              anim:         SEAT.dropdown_suit_anims = 'walk',
                              cutsceneDict: dict = None) -> Parallel:
    retseq = Parallel()

    suit = cutsceneDict['suits'][suitIndex]
    if not suit:
        return Sequence()

    turnDict = {
        'startH': 0,
        'endH': 0
    }

    # Get the goal H for this node.
    def setupTurnDict():
        startH = suit.getH(render) % 360
        a = suit.getPos(render)
        # Sometimes we're passed in a function instead of a position (for proper turning to node)
        if callable(point):
            b = point()
        elif isinstance(point, tuple):
            b = LVecBase3f(*point)
        else:
            b = point
        endH, _, _ = getHprBetweenPoints(a, b)
        endH %= 360
        difference = startH - endH
        if difference > 180:
            startH -= 360
        elif difference < -180:
            endH -= 360
        turnDict['startH'] = startH
        turnDict['endH'] = endH

    def turnCallback(t):
        suit.setH(render, lerp(turnDict['startH'], turnDict['endH'], t))

    # Create the sequence.
    retseq.append(Sequence(
        Parallel(
            ActorInterval(suit, anim, duration=duration, loop=True),
            Func(setupTurnDict),
            LerpFunc(
                turnCallback,
                duration=duration,
                blendType=blendType
            ),
        ),
        Wait(0.01),
        Func(suit.loop, 'neutral'),
    ))
    return retseq


@cutsceneSequence(name='Suit: Turn All to Point', enum=EDE.turnSuitsToPoint)
def seq_turnSuitsToPoint(point:         SEAT.slider_xyz = (0, 0, 0),
                         duration:      SEAT.slider_min_zero = 0.0,
                         blendType:     SEAT.dropdown_blendType = 'easeInOut',
                         anim:          SEAT.dropdown_toon_anims = 'walk',
                         cutsceneDict:  dict = None) -> Parallel:
    retseq = Parallel()

    for i, suit in enumerate(cutsceneDict['suits']):
        if not suit:
            continue
        # Point each toon individually.
        retseq.append(
            seq_turnSingleSuitToPoint(suitIndex=i, point=point, duration=duration,
                                      blendType=blendType, anim=anim, cutsceneDict=cutsceneDict)
        )

    return retseq


@cutsceneSequence(name='Suit: Turn Single to HPR', enum=EDE.turnSingleSuitToHpr)
def seq_turnSingleSuitToHpr(suitIndex:    SEAT.dropdown_suits = 0,
                            delay:        SEAT.slider_min_zero = 0,
                            duration:     SEAT.slider_min_zero = 0,
                            hpr:          SEAT.slider_hpr_suit = (0, 0, 0),
                            startHpr:     SEAT.slider_hpr_suit = (0, 0, 0),
                            useStartHpr:  SEAT.boolean = 0,
                            blendType:    SEAT.dropdown_blendType = 'easeInOut',
                            anim:         SEAT.dropdown_suit_anims = 'walk',
                            cutsceneDict: dict = None) -> Parallel:
    retseq = Parallel()

    suit = cutsceneDict['suits'][suitIndex]
    if not suit:
        return Sequence()

    if not useStartHpr:
        startHpr = None
    else:
        startHpr = LVecBase3f(*startHpr)

    retseq.append(Sequence(
        Wait(delay),
        Parallel(
            ActorInterval(suit, anim, duration=duration, loop=True),
            LerpHprInterval(suit, duration, LVecBase3f(*hpr), startHpr=startHpr, blendType=blendType)
        ),
        Wait(0.01),
        Func(suit.loop, 'neutral'),
    ))
    return retseq


@cutsceneSequence(name='Suit: Turn All to HPR', enum=EDE.turnSuitsToHpr)
def seq_turnSuitsToHpr(delay:        SEAT.slider_min_zero = 0,
                       duration:     SEAT.slider_min_zero = 0,
                       hpr:          SEAT.slider_hpr = (0, 0, 0),
                       startHpr:     SEAT.slider_hpr = (0, 0, 0),
                       useStartHpr:  SEAT.boolean = 0,
                       blendType:    SEAT.dropdown_blendType = 'easeInOut',
                       anim:         SEAT.dropdown_suit_anims = 'walk',
                       cutsceneDict: dict = None) -> Parallel:
    retseq = Parallel()

    for i, suit in enumerate(cutsceneDict['suits']):
        if not suit:
            continue
        # Point each suit individually.
        retseq.append(
            seq_turnSingleSuitToHpr(suitIndex=i, delay=delay, duration=duration, hpr=hpr, startHpr=startHpr,
                                    useStartHpr=useStartHpr, blendType=blendType, anim=anim, cutsceneDict=cutsceneDict)
        )

    return retseq


@cutsceneSequence(name='Suit: Fire From Cannon', enum=EDE.suitFireFromCannon)
def seq_suitFireFromCannon(suitIndex:  SEAT.dropdown_suits = 0,
                           delay:      SEAT.slider_min_zero = 0,
                           resetDelay: SEAT.slider_min_zero = 0,
                           cogCannon:  SEAT.boolean = False,
                           aimAtPoint: SEAT.boolean = False,
                           aimAtNode:  SEAT.boolean = False,
                           point:      SEAT.slider_xyz = (0, 0, 0),
                           nodeIndex:  SEAT.dropdown_node = 0,
                           fireDelay:  SEAT.slider_min_zero = 2.5,
                           unemployment: SEAT.boolean = True,
                           cutsceneDict: dict = None) -> Sequence:

    # This whole function is pretty jank when using the editor timeline, so beware.

    suit = cutsceneDict['suits'][suitIndex]
    pointNode = cutsceneDict['nodes'][nodeIndex]
    if not suit:
        return Sequence()

    if cogCannon:
        cannon = loader.loadModel('phase_5/models/props/cannon_cog')
    else:
        cannon = loader.loadModel('phase_4/models/minigames/toon_cannon')

    barrel = cannon.find('**/cannon')
    barrel = NodePathWithState(barrel)

    referenceNode = render.attachNewNode('referenceNode-Cannon')
    referenceNode.hide()
    cannonHolder = NodePathWithState('CannonHolder')
    cannonHolder.reparentTo(referenceNode)
    cannon.reparentTo(cannonHolder)
    cannonAttachPoint = barrel.attachNewNode('CannonAttach')
    kapowAttachPoint = barrel.attachNewNode('kapowAttach')
    scaleFactor = 1.6
    iScale = 1 / scaleFactor
    barrel.setScale(scaleFactor, 1, scaleFactor)

    suitLevel = suit.getActualLevel()
    if suitLevel > 12:
        suitLevel = 12
    deep = 2.5 + suitLevel * 0.2

    import math
    suitScale = 0.9 - math.sqrt(suitLevel) * 0.1

    kapow = globalPropPool.getProp('kapow')
    kapow.reparentTo(kapowAttachPoint)
    kapow.hide()
    kapow.setScale(0.25)
    kapow.setBillboardPointEye()

    smoke = loader.loadModel('phase_4/models/props/test_clouds')
    smoke.reparentTo(cannonAttachPoint)
    smoke.setScale(0.5)
    smoke.hide()
    smoke.setBillboardPointEye()

    soundBomb = base.loader.loadSfx('phase_4/audio/sfx/MG_cannon_fire_alt.ogg')
    playSoundBomb = SoundInterval(soundBomb, node=cannonHolder)

    soundFly = base.loader.loadSfx('phase_4/audio/sfx/firework_whistle_01.ogg')
    playSoundFly = SoundInterval(soundFly, node=cannonHolder)

    soundCannonAdjust = base.loader.loadSfx('phase_4/audio/sfx/MG_cannon_adjust.ogg')
    playSoundCannonAdjust = SoundInterval(soundCannonAdjust, duration=0.6, node=cannonHolder)

    soundCogPanic = base.loader.loadSfx('phase_5/audio/sfx/ENC_cogafssm.ogg')
    playSoundCogPanic = SoundInterval(soundCogPanic, node=cannonHolder)

    def getDustCloudIval():
        dustCloud = DustCloud.DustCloud(fBillboard=0, wantSound=1)
        dustCloud.setBillboardAxis(2.0)
        dustCloud.setZ(3)
        dustCloud.setScale(1.0)
        dustCloud.createTrack()
        if not suit:
            return Sequence()
        return Sequence(Func(dustCloud.reparentTo, suit), dustCloud.track, Func(dustCloud.destroy),
                        name='dustCloudIval')

    def makeSuitUnemployed():
        if suit.isSkeleton:
            suit.setSkeleClothes(texOverride='**/skel_body_unemp_gen')
        else:
            suit.setSuitClothes(texOverride='**/suit_body_unemp_gen')
        suit.fired = True
        nameInfo = suit.createNameInfo(wantDept=False)
        suit.setDisplayName(nameInfo)

    def setupCannonAndCog():
        cannon.setPos(0, 0, -8.6)
        cannonHolder.setH(0)
        barrel.setHpr(0, 90, 0)
        referenceNode.setPos(suit.getPos(render))
        referenceNode.setHpr(suit.getHpr(render))
        cannonAttachPoint.setScale(iScale, 1, iScale)
        cannonAttachPoint.setPos(0, 6.7, 0)
        kapowAttachPoint.setPos(0, -0.5, 1.9)
        suit.reparentTo(cannonAttachPoint)
        suit.setPos(0, 0, 0)
        suit.setHpr(0, -90, 0)

    # Allow for aiming at point
    eventId = getUniqueCutsceneId()

    # Get the goal H for this toon.
    def updateHpr(t):
        # Wrapping this in a function call
        # to ensure it works properly.
        a = referenceNode.getPos(render)
        if aimAtNode:
            pos = pointNode.getPos(render)
            pos.setZ(pos.getZ() + 2)
            b = LVecBase3f(*pos)
        else:
            b = LVecBase3f(*point)
        endH, endP, _ = getHprBetweenPoints(a, b)
        endH -= referenceNode.getH()
        h1 = getattr(cannonHolder, f'turnToPoint-{eventId}', cannonHolder.getH())
        p1 = getattr(barrel, f'turnToPoint-{eventId}', barrel.getP())
        goalH = ((endH - h1) * t) + h1
        goalP = ((endP - p1) * t) + p1
        cannonHolder.setH(goalH)
        barrel.setP(goalP)

    def updateStartHpr():
        setattr(cannonHolder, f'turnToPoint-{eventId}', cannonHolder.getH())
        setattr(barrel, f'turnToPoint-{eventId}', barrel.getP())

    if aimAtPoint or aimAtNode:
        rotateToPointTrack = Sequence(
            Func(updateStartHpr),
            LerpFunctionInterval(
                function=updateHpr,
                duration=0.6,
                blendType='easeIn'
            )
        )
    else:
        rotateToPointTrack = LerpHprInterval(
            barrel,
            0.6,
            Point3(0, 45, 0),
            blendType='easeIn'
        )

    reactIval = Parallel(Func(setupCannonAndCog),
                         Func(referenceNode.show),
                         ActorInterval(suit, 'pie-small-react'),
                         Sequence(LerpPosInterval(cannonHolder, 2.0,
                                                  Point3(0, 0, 7),
                                                  blendType='easeInOut'),
                                  Parallel(rotateToPointTrack,
                                           playSoundCannonAdjust),
                                  Wait(fireDelay - 0.5 + resetDelay),
                                  Parallel(LerpHprInterval(barrel, 0.6,
                                                           Point3(0, 90, 0),
                                                           blendType='easeIn'),
                                           playSoundCannonAdjust),
                                  LerpPosInterval(cannonHolder, 1.0,
                                                  Point3(0, 0, 0),
                                                  blendType='easeInOut')),
                         Sequence(Wait(0.0),
                                  Parallel(ActorInterval(suit, 'flail'),
                                           (Parallel(
                                               getDustCloudIval(),
                                               Func(makeSuitUnemployed)
                                           ) if unemployment else Sequence()),
                                           suit.scaleInterval(1.0, suitScale),
                                           LerpPosInterval(suit, 0.25, Point3(0, -1.0, 0.0)),
                                           Sequence(Wait(0.25),
                                                    Parallel(playSoundCogPanic,
                                                             LerpPosInterval(suit, 1.5, Point3(0, -deep, 0.0),
                                                                             blendType='easeIn')))),
                                  Wait(fireDelay),
                                  Parallel(playSoundBomb,
                                           playSoundFly,
                                           Sequence(Func(smoke.show),
                                                    Parallel(LerpScaleInterval(smoke, 0.5, 3),
                                                             LerpColorScaleInterval(smoke, 0.5, Vec4(2, 2, 2, 0))),
                                                    Func(smoke.hide)),
                                           Sequence(Func(kapow.show),
                                                    ActorInterval(kapow, 'kapow'),
                                                    Func(kapow.hide)),
                                           LerpPosInterval(suit, 3.0, Point3(0, 150.0, 0.0)),
                                           suit.scaleInterval(3.0, 0.01)), Func(suit.hide), Func(suit.reparentTo, render), Func(suit.setScale, 1.0)))

    removeThese = (
        referenceNode,
        cannonHolder,
        smoke,
        kapow,
        cannon,
        barrel,
        cannonAttachPoint,
        kapowAttachPoint,
    )

    def cleanup():
        from direct.actor.Actor import Actor
        from panda3d.core import NodePath
        for node in removeThese:
            if isinstance(node, Actor):
                node.cleanup()
            elif isinstance(node, NodePath):
                node.removeNode()

    if cutsceneDict.get('isEditor', False):
        sival = Sequence(reactIval, Func(referenceNode.hide))
        cutsceneDict['editorCleanup'].append(cleanup)
    else:
        sival = Sequence(reactIval, Func(cleanup))

    return Sequence(
        Wait(delay),
        sival,
    )
