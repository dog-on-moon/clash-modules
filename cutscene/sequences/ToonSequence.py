import random
import math

from direct.showbase.PythonUtil import lerp
from toontown.battle.BattleProps import globalPropPool

from toontown.cutscene.editor.CSEditorEnums import EventDefinitionEnum as EDE
from toontown.cutscene.editor.CSEditorEnums import SubEventArgumentType as SEAT
from toontown.cutscene.CutsceneSequenceBase import cutsceneSequence, getUniqueCutsceneId

from panda3d.core import Point3, LVecBase3f, LVecBase4f, NodePath
from direct.interval.IntervalGlobal import *

from toontown.battle.BattleBase import BattleBase
from toontown.cutscene.editor.CSEditorClasses import EventArgument, CSEditorException
from toontown.cutscene.editor.CSEditorEnums import ToonBlockShape, ToonSubEventTargetGroup
from toontown.building.ElevatorConstants import ElevatorPoints, BigElevatorPoints
from toontown.cutscene.CutsceneSequenceHelpers import NodePathWithState, getHprBetweenPoints
from toontown.toonbase import TTLocalizer
from toontown.effects import DustCloud
from toontown.suit.SuitDNA import allSuitNames


# Conditionally call loop on toon or their disguise.
def loopToonOrDisguise(toon, animName):
    toon.suit.loop(animName) if toon.isDisguised else toon.loop(animName)


@cutsceneSequence(name='Toon: Move Sequence', enum=EDE.moveSingleToon)
def seq_moveSingleToon(toonIndex:       SEAT.dropdown_toons = 0,
                       pos:             SEAT.slider_xyz = (0, 0, 0),
                       duration:        SEAT.slider_min_zero = 0,
                       delay:           SEAT.slider_min_zero = 0,
                       hasAnim:         SEAT.boolean = True,
                       anim:            SEAT.dropdown_toon_anims = 'walk',
                       cutsceneDict:    dict = None) -> Parallel:
    retseq = Parallel()

    toon = cutsceneDict['toons'][toonIndex]
    if not toon:
        return Sequence()
    destination = LVecBase3f(*pos)

    # Complete the full sequence, making sure to neutral afterwards.
    retseq.append(Sequence(
        Wait(delay),
        Parallel(
            ActorInterval(toon, anim, duration=duration, loop=True) if hasAnim else Wait(0.0),
            LerpPosInterval(toon, pos=destination, duration=duration),
        ),
        Wait(0.01),
        Func(loopToonOrDisguise, toon, 'neutral') if hasAnim else Wait(0.0),
    ))

    return retseq


@cutsceneSequence(name='Toon: Relative Turn&Move Sequence', enum=EDE.turnAndMoveToon)
def seq_moveAndTurnToon(toonIndex:       SEAT.dropdown_toons = 0,
                        goalPos:         SEAT.slider_xyz = (0, 0, 0),
                        goalHpr:         SEAT.slider_hpr = (0, 0, 0),
                        moveDuration:    SEAT.slider_min_zero = 3.0,
                        turnDuration:    SEAT.slider_min_zero = 3.0,
                        delay:           SEAT.slider_min_zero = 0,
                        walkAnim:        SEAT.dropdown_toon_anims = 'walk',
                        runAnim:         SEAT.dropdown_toon_anims = 'run',
                        cutsceneDict:    dict = None) -> Parallel:
    toon = cutsceneDict['toons'][toonIndex]
    if not toon:
        return Sequence()

    # Do sequence
    return Sequence(
        Wait(delay),
        Parallel(
            ActorInterval(toon, walkAnim, duration=turnDuration, loop=True),
            LerpHprInterval(toon, turnDuration, LVecBase3f(*goalHpr)),
        ) if turnDuration != 0.0 else Wait(0.0),
        Parallel(
            ActorInterval(toon, runAnim, duration=moveDuration, loop=True),
            LerpPosInterval(toon, moveDuration, LVecBase3f(*goalPos)),
        ) if moveDuration != 0.0 else Wait(0.0),
        Wait(0.01),
        Func(toon.loop, 'neutral'),
    )


@cutsceneSequence(name='Toon: Move Block Sequence', enum=EDE.moveToonsInBlock)
def seq_moveToonsInBlock(target:        SEAT.dropdown_targetGroup = 'All',
                         pos:           SEAT.slider_xyz = (0, 0, 0),
                         duration:      SEAT.slider_min_zero = 0,
                         delay:         SEAT.slider_min_zero = 0,
                         hasAnim:       SEAT.boolean = True,
                         anim:          SEAT.dropdown_toon_anims = 'walk',
                         shape:         SEAT.dropdown_blockShape = 'Elevator',
                         radius:        SEAT.slider_min_zero = 1.5,
                         h:       SEAT.slider_float = 0.0,
                         cutsceneDict:  dict = None) -> Parallel:
    retseq = Parallel()

    targetGroup = ToonSubEventTargetGroup[target]
    blockShape = ToonBlockShape[shape]
    targetRange = _getTargetRange(targetGroup, cutsceneDict['toons'], cutsceneDict['maxPlayers'])
    blockPoints = _toonBlockPositions(pos, shape=blockShape, radius=radius, h=h,
                                      toons=cutsceneDict['toons'][targetRange.start:targetRange.stop])

    for i in targetRange:
        # Each toon can be moved individually in parallel.
        retseq.append(
            seq_moveSingleToon(toonIndex=i, pos=blockPoints[i], duration=duration,
                               delay=delay, anim=anim, hasAnim=hasAnim, cutsceneDict=cutsceneDict)
        )

    return retseq


@cutsceneSequence(name='Toon: Turn All to Node', enum=EDE.turnToonsToNode)
def seq_turnToonsToNode(target:         SEAT.dropdown_targetGroup = 'All',
                        nodeIndex:      SEAT.dropdown_node = None,
                        duration:       SEAT.slider_min_zero = 0,
                        blendType:      SEAT.dropdown_blendType = 'easeInOut',
                        hasAnim:        SEAT.boolean = True,
                        anim:           SEAT.dropdown_toon_anims = 'walk',
                        offset:         SEAT.slider_xyz = (0, 0, 0),
                        cutsceneDict:   dict = None) -> Parallel:
    retseq = Parallel()

    targetGroup = ToonSubEventTargetGroup[target]

    for i in _getTargetRange(targetGroup, cutsceneDict['toons'], cutsceneDict['maxPlayers']):
        # Point each toon individually.
        retseq.append(
            seq_turnSingleToonToNode(toonIndex=i, nodeIndex=nodeIndex, duration=duration,
                                     blendType=blendType, anim=anim, hasAnim=hasAnim,
                                     offset=offset,
                                     cutsceneDict=cutsceneDict)
        )

    return retseq


@cutsceneSequence(name='Toon: Turn One to Node', enum=EDE.turnSingleToonToNode)
def seq_turnSingleToonToNode(toonIndex:     SEAT.dropdown_toons = 0,
                             nodeIndex:     SEAT.dropdown_node = None,
                             duration:      SEAT.slider_min_zero = 0.0,
                             blendType:     SEAT.dropdown_blendType = 'easeInOut',
                             hasAnim:       SEAT.boolean = True,
                             anim:          SEAT.dropdown_toon_anims = 'walk',
                             offset:        SEAT.slider_xyz = (0, 0, 0),
                             cutsceneDict:  dict = None) -> Parallel:
    def getNodePos():
        return cutsceneDict['nodes'][nodeIndex].getPos(render) + LVecBase3f(*offset)
    return seq_turnSingleToonToPoint(
        toonIndex=toonIndex, point=getNodePos,
        duration=duration, blendType=blendType, anim=anim, hasAnim=hasAnim, cutsceneDict=cutsceneDict
    )


@cutsceneSequence(name='Toon: Turn Single to Point', enum=EDE.turnSingleToonToPoint)
def seq_turnSingleToonToPoint(toonIndex:    SEAT.dropdown_toons = 0,
                              point:        SEAT.slider_xyz = (0, 0, 0),
                              duration:     SEAT.slider_min_zero = 0.0,
                              blendType:    SEAT.dropdown_blendType = 'easeInOut',
                              hasAnim:      SEAT.boolean = True,
                              anim:         SEAT.dropdown_toon_anims = 'walk',
                              cutsceneDict: dict = None) -> Parallel:
    retseq = Parallel()

    toon = cutsceneDict['toons'][toonIndex]
    if not toon:
        return Sequence()

    turnDict = {
        'startH': 0,
        'endH': 0
    }

    # Get the goal H for this node.
    def setupTurnDict():
        startH = toon.getH(render) % 360
        a = toon.getPos(render)
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
        toon.setH(render, lerp(turnDict['startH'], turnDict['endH'], t))

    # Create the sequence.
    retseq.append(Sequence(
        Parallel(
            ActorInterval(toon, anim, duration=duration, loop=True) if hasAnim else Wait(0.0),
            Func(setupTurnDict),
            LerpFunc(
                turnCallback,
                duration=duration,
                blendType=blendType
            ),
        ),
        Wait(0.01),
        Func(loopToonOrDisguise, toon, 'neutral') if hasAnim else Wait(0.0),
    ))
    return retseq


@cutsceneSequence(name='Toon: Turn All to Point', enum=EDE.turnToonsToPoint)
def seq_turnToonsToPoint(target:        SEAT.dropdown_targetGroup = 'All',
                         point:         SEAT.slider_xyz = (0, 0, 0),
                         duration:      SEAT.slider_min_zero = 0.0,
                         blendType:     SEAT.dropdown_blendType = 'easeInOut',
                         hasAnim:      SEAT.boolean = True,
                         anim:          SEAT.dropdown_toon_anims = 'walk',
                         cutsceneDict:  dict = None) -> Parallel:
    retseq = Parallel()

    targetGroup = ToonSubEventTargetGroup[target]

    for i in _getTargetRange(targetGroup, cutsceneDict['toons'], cutsceneDict['maxPlayers']):
        # Point each toon individually.
        retseq.append(
            seq_turnSingleToonToPoint(toonIndex=i, point=point, duration=duration,
                                      blendType=blendType, anim=anim, hasAnim=hasAnim,
                                      cutsceneDict=cutsceneDict)
        )

    return retseq


@cutsceneSequence(name='Toon: Turn Single to HPR', enum=EDE.turnSingleToonToHpr)
def seq_turnSingleToonToHpr(toonIndex:    SEAT.dropdown_toons = 0,
                            delay:        SEAT.slider_min_zero = 0,
                            duration:     SEAT.slider_min_zero = 0,
                            hpr:          SEAT.slider_hpr_toon = (0, 0, 0),
                            startHpr:     SEAT.slider_hpr_toon = (0, 0, 0),
                            useStartHpr:  SEAT.boolean = 0,
                            blendType:    SEAT.dropdown_blendType = 'easeInOut',
                            hasAnim:      SEAT.boolean = True,
                            anim:         SEAT.dropdown_toon_anims = 'walk',
                            cutsceneDict: dict = None) -> Parallel:
    retseq = Parallel()

    toon = cutsceneDict['toons'][toonIndex]
    if not toon:
        return Sequence()

    if not useStartHpr:
        startHpr = None
    else:
        startHpr = LVecBase3f(*startHpr)

    retseq.append(Sequence(
        Wait(delay),
        Parallel(
            ActorInterval(toon, anim, duration=duration, loop=True) if hasAnim else Wait(0.0),
            LerpHprInterval(toon, duration, LVecBase3f(*hpr), startHpr=startHpr, blendType=blendType)
        ),
        Wait(0.01),
        Func(loopToonOrDisguise, toon, 'neutral') if hasAnim else Wait(0.0),
    ))
    return retseq


@cutsceneSequence(name='Toon: Turn All to HPR', enum=EDE.turnToonsToHpr)
def seq_turnToonsToHpr(delay:        SEAT.slider_min_zero = 0,
                       duration:     SEAT.slider_min_zero = 0,
                       hpr:          SEAT.slider_hpr = (0, 0, 0),
                       startHpr:     SEAT.slider_hpr = (0, 0, 0),
                       useStartHpr:  SEAT.boolean = 0,
                       blendType:    SEAT.dropdown_blendType = 'easeInOut',
                       hasAnim:      SEAT.boolean = True,
                       anim:         SEAT.dropdown_toon_anims = 'walk',
                       cutsceneDict: dict = None) -> Parallel:
    retseq = Parallel()

    for i, toon in enumerate(cutsceneDict['toons']):
        if not toon:
            continue
        # Point each suit individually.
        retseq.append(
            seq_turnSingleToonToHpr(toonIndex=i, delay=delay, duration=duration, hpr=hpr, startHpr=startHpr,
                                    useStartHpr=useStartHpr, blendType=blendType, hasAnim=hasAnim, anim=anim,
                                    cutsceneDict=cutsceneDict)
        )

    return retseq


@cutsceneSequence(name='Toon: Teleport to Elevator', enum=EDE.tpToonsToElevator)
def seq_moveToonsToElevator(target:             SEAT.dropdown_targetGroup = 'Players',
                            elevatorModelIndex: SEAT.dropdown_elevators = 0,
                            isBig:              SEAT.boolean = 0,
                            cutsceneDict:       dict = None) -> Parallel:
    retParallel = Parallel()

    posList = BigElevatorPoints if isBig else ElevatorPoints
    targetGroup = ToonSubEventTargetGroup[target]

    if elevatorModelIndex is not None:
        for i in _getTargetRange(targetGroup, cutsceneDict['toons'], cutsceneDict['maxPlayers']):
            toon = cutsceneDict['toons'][i]
            if not toon:
                continue
            toonSeq = Sequence()
            toonSeq.append(Func(toon.reparentTo, cutsceneDict['elevators'][elevatorModelIndex]))
            toonSeq.append(Func(toon.setPos, *posList[i]))
            toonSeq.append(Func(toon.setH, 180))
            toonSeq.append(Func(toon.wrtReparentTo, render))
            retParallel.append(toonSeq)

    return retParallel


@cutsceneSequence(name='Toon: Move to Battle Positions', enum=EDE.moveToonsToBattlePos)
def seq_moveToonsToBattlePositions(duration:        SEAT.slider_min_zero = 5.0,
                                   hasAnim:         SEAT.boolean = True,
                                   anim:            SEAT.dropdown_toon_anims = 'walk',
                                   delay:           SEAT.slider_min_zero = 0,
                                   battleNodeIndex: SEAT.dropdown_node = 0,
                                   flipY:           SEAT.boolean = 0,
                                   xyzOffset:       SEAT.slider_xyz = (0, 0, 0),
                                   cutsceneDict:    dict = None) -> Parallel:
    """Moves all of the Toons to their battle positions."""
    retseq = Parallel()
    toons = [toon for toon in cutsceneDict['toons'] if toon]
    toonPoints = BattleBase.toonPoints[len(toons) - 1]
    battlePos = cutsceneDict['nodes'][battleNodeIndex].getPos()
    for i, toon in enumerate(toons):
        # Set the variables used for the block.
        goalPos, goalH = toonPoints[i]

        # set goal pos and H
        goalPos = goalPos + battlePos
        goalHpr = Point3(goalH, 0, 0)

        # do we flip y?
        if flipY:
            x, y, z = goalPos
            goalPos = LVecBase3f(x, -y, z)
            goalHpr = Point3(-goalH + 180, 0, 0)

        # add offset
        xoff, yoff, zoff = xyzOffset
        x, y, z = goalPos
        goalPos = LVecBase3f(x + xoff, y + yoff, z + zoff)

        # Move the toon to the necessary location.
        movementSeq = Parallel(
            ActorInterval(toon, anim, duration=duration, loop=True) if hasAnim else Wait(0.0),
            LerpPosHprInterval(
                toon,
                duration,
                pos=goalPos,
                hpr=goalHpr
            ),
        )

        # Complete the full sequence, making sure to neutral afterwards.
        retseq.append(Sequence(
            Wait(delay),
            movementSeq,
            Wait(0.01),
            Func(loopToonOrDisguise, toon, 'neutral') if hasAnim else Wait(0.0),
        ))

    return retseq


@cutsceneSequence(name='Toon: Animate', enum=EDE.animateSingleToon)
def seq_singleToonDoAnim(toonIndex:       SEAT.dropdown_toons = 0,
                         startAnim:       SEAT.dropdown_toon_anims = 'neutral',
                         loop:            SEAT.boolean = 0,
                         hasDuration:     SEAT.boolean = 0,
                         duration:        SEAT.slider_min_zero = 0,
                         hasStartTime:    SEAT.boolean = 0,
                         startTime:       SEAT.slider_min_zero = 0,
                         hasEndTime:      SEAT.boolean = 0,
                         endTime:         SEAT.slider_min_zero = 0,
                         playRate:        SEAT.slider_float = 1,
                         useEndAnim:      SEAT.boolean = 0,
                         endAnim:         SEAT.dropdown_toon_anims = 'neutral',
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
    toon = cutsceneDict['toons'][toonIndex]
    if not toon:
        return retParallel
    playRate = playRate if playRate else 1.0  # do not let equal 0
    # some math in case we run as a func and not an interval
    animDuration = toon.getDuration(startAnim)
    animFrameCount = toon.getNumFrames(startAnim)
    startFrame = round((startTime / max(animDuration, 0.01)) * animFrameCount) if startTime else 0
    endFrame = round((endTime / max(animDuration, 0.01)) * animFrameCount) if endTime else animFrameCount

    if not loop:
        retParallel.append(Parallel(
            ActorInterval(toon, startAnim, loop=loop, duration=duration,
                          startTime=startTime, endTime=endTime,
                          playRate=playRate) if isInterval else Func(
                toon.play, startAnim, None, startFrame, endFrame
            ),
            Sequence(
                Wait(duration),
                ActorInterval(toon, endAnim)
            ) if duration and endAnim else Sequence(),
        ))
    else:
        retParallel.append(Sequence(
            Func(loopToonOrDisguise, toon, startAnim),
        ))
    return retParallel


@cutsceneSequence(name='Toon: Animate All Toons', enum=EDE.animateAllToons)
def seq_allToonsDoAnim(startAnim:       SEAT.dropdown_toon_anims = 'neutral',
                       loop:            SEAT.boolean = 0,
                       hasDuration:     SEAT.boolean = 0,
                       duration:        SEAT.slider_min_zero = 0,
                       hasStartTime:    SEAT.boolean = 0,
                       startTime:       SEAT.slider_min_zero = 0,
                       hasEndTime:      SEAT.boolean = 0,
                       endTime:         SEAT.slider_min_zero = 0,
                       playRate:        SEAT.slider_float = 1,
                       useEndAnim:      SEAT.boolean = 0,
                       endAnim:         SEAT.dropdown_toon_anims = 'neutral',
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
    for toon in cutsceneDict['toons']:
        if not toon:
            continue
        playRate = playRate if playRate else 1.0  # do not let equal 0
        # some math in case we run as a func and not an interval
        animDuration = toon.getDuration(startAnim)
        animFrameCount = toon.getNumFrames(startAnim)
        startFrame = round((startTime / max(animDuration, 0.01)) * animFrameCount) if startTime else 0
        endFrame = round((endTime / max(animDuration, 0.01)) * animFrameCount) if endTime else animFrameCount

        if not loop:
            retParallel.append(Parallel(
                ActorInterval(toon, startAnim, loop=loop, duration=duration,
                              startTime=startTime, endTime=endTime,
                              playRate=playRate) if isInterval else Func(
                    toon.play, startAnim, None, startFrame, endFrame
                ),
                Sequence(
                    Wait(duration),
                    ActorInterval(toon, endAnim)
                ) if duration and endAnim else Sequence(),
            ))
        else:
            retParallel.append(Sequence(
                Func(loopToonOrDisguise, toon, startAnim),
            ))
    return retParallel


@cutsceneSequence(name='Toon: Pingpong', enum=EDE.pingpongSingleToon)
def seq_toonPingpong(toonIndex:     SEAT.dropdown_toons = 0,
                     anim:          SEAT.dropdown_toon_anims = 'neutral',
                     loop:          SEAT.boolean = 0,
                     hasDuration:   SEAT.boolean = 0,
                     duration:      SEAT.slider_min_zero = 0.0,
                     startTime:     SEAT.slider_min_zero = 0,
                     endTime:       SEAT.slider_min_zero = 0,
                     cutsceneDict:  dict = None) -> Sequence:
    """Makes a toon pingpong an animation."""
    toon = cutsceneDict['toons'][toonIndex]
    if not toon:
        return Sequence()
    if not hasDuration:
        duration = None
    # some math in case we run as a func and not an interval
    animDuration = toon.getDuration(anim)
    animFrameCount = toon.getNumFrames(anim)
    startFrame = round((startTime / max(animDuration, 0.01)) * animFrameCount) if startTime else 0
    endFrame = round((endTime / max(animDuration, 0.01)) * animFrameCount) if endTime else animFrameCount

    track = Sequence(
        Func(toon.pingpong, anim, loop, None, startFrame, endFrame)
    )

    if hasDuration:
        track.append(
            Sequence(
                Wait(duration),
                Func(loopToonOrDisguise(toon, 'neutral'))
            )
        )

    return track


@cutsceneSequence(name='Toon: Pingpong All', enum=EDE.pingpongAllToons)
def seq_allToonsPingpong(anim:          SEAT.dropdown_toon_anims = 'neutral',
                        loop:          SEAT.boolean = 0,
                        hasDuration:   SEAT.boolean = 0,
                        duration:      SEAT.slider_min_zero = 0.0,
                        startTime:     SEAT.slider_min_zero = 0,
                        endTime:       SEAT.slider_min_zero = 0,
                        cutsceneDict:  dict = None) -> Sequence:
    """Makes all toons pingpong an animation."""
    track = Parallel()

    for i in range(len(cutsceneDict['toons'])):
        track.append(seq_toonPingpong(i, anim, loop, hasDuration, duration, startTime, endTime, cutsceneDict))

    return track


@cutsceneSequence(name='Toon: Disguise All Toons (FOR TESTING ONLY!)', enum=EDE.disguiseAllToons)
def seq_disguiseAllToons(delay:         SEAT.slider_min_zero = 0,
                         cutsceneDict:  dict = None) -> Sequence:
    retParallel = Parallel()
    for toon in cutsceneDict['toons']:
        if not toon:
            continue
        retParallel.append(
            Func(toon.putOnSuit, random.choice(allSuitNames))
        )
    return Sequence(
        Wait(delay),
        retParallel
    )


@cutsceneSequence(name='Toon: Undisguise All Toons', enum=EDE.undisguiseAllToons)
def seq_undisguiseAllToons(delay:         SEAT.slider_min_zero = 0,
                         cutsceneDict:  dict = None) -> Sequence:
    retParallel = Parallel()
    for toon in cutsceneDict['toons']:
        if not toon:
            continue
        if not hasattr(toon, 'dustCloud') or toon.dustCloud is None:
            toon.dustCloud = DustCloud.DustCloud()
            toon.dustCloud.setPos(0, 2, 3)
            toon.dustCloud.setScale(0.5)
            toon.dustCloud.setDepthWrite(0)
            toon.dustCloud.setBin('fixed', 0)
            toon.dustCloud.createTrack()
        retParallel.append(
            Sequence(
                Func(toon.dustCloud.reparentTo, toon),
                Func(toon.dustCloud.show),
                Parallel(
                    toon.dustCloud.track,
                    Sequence(Wait(0.3),
                    Func(toon.takeOffSuit),
                    Func(toon.sadEyes),
                    Func(toon.blinkEyes),
                    Func(toon.play, 'slip-backward'),
                    Wait(0.7))
                ),
                #Func(toon.dustCloud.detachNode),
                Func(toon.dustCloud.hide),
                Func(toon.normalEyes),
                #Func(toon.dustCloud.destroy)
            )
        )
    snd = loader.loadSfx('phase_5/audio/sfx/tt_s_ara_cfg_propellerBreaks.ogg')
    return Sequence(
        Wait(delay),
        Func(snd.play),
        retParallel
    )


@cutsceneSequence(name='Toon: Set One Anim State', enum=EDE.setOneAnimState)
def seq_setOneToonAnimState(toonIndex:      SEAT.dropdown_toons = 0,
                            delay:          SEAT.slider_min_zero = 0,
                            animState:      SEAT.dropdown_toon_anim_states = 'Neutral',
                            cutsceneDict:   dict = None) -> Sequence:
    retParallel = Parallel()
    toon = cutsceneDict['toons'][toonIndex]
    if not toon:
        return Sequence()

    extraArgs = []
    if animState == 'Squish':
        # depending on number of toons, lower volume on state transition
        extraArgs = [1 / len(cutsceneDict['toons'])]
    retParallel.append(
        Func(toon.setAnimState, animState, 1.0, None, None, None, extraArgs)
    )
    return Sequence(
        Wait(delay),
        retParallel
    )


@cutsceneSequence(name='Toon: Set All Anim State', enum=EDE.setAllAnimStates)
def seq_setToonAnimState(delay:         SEAT.slider_min_zero = 0,
                         animState:     SEAT.dropdown_toon_anim_states = 'Neutral',
                         cutsceneDict:  dict = None) -> Sequence:
    retParallel = Parallel()
    for toon in cutsceneDict['toons']:
        if not toon:
            continue
        extraArgs = []
        if animState == 'Squish':
            # depending on number of toons, lower volume on state transition
            extraArgs = [1 / len(cutsceneDict['toons'])]
        retParallel.append(
            Func(toon.setAnimState, animState, 1.0, None, None, None, extraArgs)
        )
    return Sequence(
        Wait(delay),
        retParallel
    )


@cutsceneSequence(name='Toon: Emote One', enum=EDE.setOneEmote)
def seq_setOneToonEmote(toonIndex:      SEAT.dropdown_toons = 0,
                        delay:          SEAT.slider_min_zero = 0,
                        emoteIndex:     SEAT.dropdown_toon_emote = 0,
                        cutsceneDict:   dict = None) -> Sequence:
    retParallel = Parallel()
    toon = cutsceneDict['toons'][toonIndex]
    if not toon:
        return Sequence()

    # TODO: Make this work with new hammerspace emote definition
    # Not quite sure how else to fix this so I'm just doing this
    emoteIndex = TTLocalizer.EmoteFuncDict[emoteIndex]

    retParallel.append(
        Func(toon.doEmote, emoteIndex, 1.0, 0, None, [])
    )
    return Sequence(
        Wait(delay),
        retParallel
    )


@cutsceneSequence(name='Toon: Emote All', enum=EDE.setAllEmote)
def seq_setToonEmote(delay:         SEAT.slider_min_zero = 0,
                     emoteIndex:    SEAT.dropdown_toon_emote = 0,
                     cutsceneDict:  dict = None) -> Sequence:
    retParallel = Parallel()
    for i in range(len(cutsceneDict['toons'])):
        retParallel.append(seq_setOneToonEmote(i, 0, emoteIndex, cutsceneDict))
    return Sequence(
        Wait(delay),
        retParallel
    )


@cutsceneSequence(name='Toon: Show', enum=EDE.showToon)
def seq_showToon(toonIndex:     SEAT.dropdown_toons = 0,
                 cutsceneDict:  dict = None) -> Parallel:
    retParallel = Parallel()
    toon = cutsceneDict['toons'][toonIndex]
    if not toon:
        return Sequence()
    retParallel.append(Func(toon.show))
    # retParallel.append(Func(toon.showNametag2d))
    retParallel.append(Func(toon.showNametag3d))
    return retParallel


@cutsceneSequence(name='Toon: Hide', enum=EDE.hideToon)
def seq_hideToon(toonIndex:     SEAT.dropdown_toons = 0,
                 cutsceneDict:  dict = None) -> Parallel:
    retParallel = Parallel()
    toon = cutsceneDict['toons'][toonIndex]
    if not toon:
        return Sequence()
    retParallel.append(Func(toon.hide))
    retParallel.append(Func(toon.hideNametag2d))
    retParallel.append(Func(toon.hideNametag3d))
    return retParallel


@cutsceneSequence(name='Toon: Show All', enum=EDE.showToons)
def seq_showToons(cutsceneDict: dict = None) -> Parallel:
    retParallel = Parallel()
    for toon in cutsceneDict['toons']:
        if not toon:
            continue
        retParallel.append(Func(toon.show))
        # retParallel.append(Func(toon.showNametag2d))
        retParallel.append(Func(toon.showNametag3d))
    return retParallel


@cutsceneSequence(name='Toon: Hide All', enum=EDE.hideToons)
def seq_hideToons(cutsceneDict: dict = None) -> Parallel:
    retParallel = Parallel()
    for toon in cutsceneDict['toons']:
        if not toon:
            continue
        retParallel.append(Func(toon.hide))
        retParallel.append(Func(toon.hideNametag2d))
        retParallel.append(Func(toon.hideNametag3d))
    return retParallel


@cutsceneSequence(name='Toon: Fire From Cannon', enum=EDE.toonFireFromCannon)
def seq_toonFireFromCannon(toonIndex:  SEAT.dropdown_toons = 0,
                           toonFlyDist:SEAT.slider_min_zero = 150,
                           toonFlyDur: SEAT.slider_min_zero = 3.0,
                           delay:      SEAT.slider_min_zero = 0,
                           resetDelay: SEAT.slider_min_zero = 0,
                           cogCannon:  SEAT.boolean = False,
                           aimAtPoint: SEAT.boolean = False,
                           nodeIndex:  SEAT.dropdown_node = 0,
                           startHpr:   SEAT.slider_hpr = (0, 0, 0),
                           hideAvatar: SEAT.boolean = True,
                           cutsceneDict: dict = None) -> Sequence:

    # This whole function is pretty jank when using the editor timeline, so beware.

    suit = cutsceneDict['toons'][toonIndex]
    point = cutsceneDict['nodes'][nodeIndex]
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

    deep = 2.7

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
        b = LVecBase3f(*point.getPos())
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

    if aimAtPoint:
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

    reactIval = Parallel(
        Func(setupCannonAndCog),
        Func(referenceNode.show),
        Sequence(LerpPosHprInterval(cannonHolder, 2.0,
                                Point3(0, 0, 7), Vec3(*startHpr),
                                blendType='easeInOut'),
                Parallel(rotateToPointTrack,
                        playSoundCannonAdjust),
                Wait(2.0 + resetDelay),
                Parallel(LerpHprInterval(barrel, 0.6,
                                        Point3(0, 90, 0),
                                        blendType='easeIn'),
                        playSoundCannonAdjust),
                LerpPosInterval(cannonHolder, 1.0,
                                Point3(0, 0, 0),
                                blendType='easeInOut')),
        Sequence(Wait(0.0),
                Parallel(ActorInterval(suit, 'cringe'),
                        suit.scaleInterval(1.0, 0.8),
                        LerpPosInterval(suit, 0.25, Point3(0, -1.0, 0.0)),
                        Sequence(Wait(0.25),
                                Parallel(playSoundCogPanic,
                                            LerpPosInterval(suit, 1.5, Point3(0, -deep, 0.0),
                                                            blendType='easeIn')))),
                Wait(2.5),
                Parallel(
                    playSoundBomb,
                    playSoundFly,
                    Sequence(Func(smoke.show),
                            Parallel(LerpScaleInterval(smoke, 0.5, 3),
                                        LerpColorScaleInterval(smoke, 0.5, Vec4(2, 2, 2, 0))),
                            Func(smoke.hide)),
                    Sequence(Func(kapow.show),
                            ActorInterval(kapow, 'kapow'),
                            Func(kapow.hide)),
                    LerpPosInterval(suit, toonFlyDur, Point3(0, toonFlyDist, 0.0)),
                    (suit.scaleInterval(toonFlyDur, 0.01) if hideAvatar else suit.scaleInterval(0.01, 1.0)),
                    Sequence(
                        Wait(toonFlyDur),
                        (Sequence(
                            Func(suit.hide),
                            Func(suit.reparentTo, render),
                            Func(suit.setScale, 1.0)
                        ) if hideAvatar else Sequence(Func(suit.wrtReparentTo, render),
                                                      Func(suit.setScale, 1.0)))
                    )
                )
            ))

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


@cutsceneSequence(name='Toon: Squish', enum=EDE.squishToon)
def seq_squishToon(toonIndex:  SEAT.dropdown_toons = 0,
                   cutsceneDict: dict = None):
    toon = cutsceneDict['toons'][toonIndex]
    if not toon:
        return Sequence()
    return Sequence(
        Func(toon.setAnimState, "Squish"),
        Func(toon.playDialogueForString, "!"),
        Wait(2.7),
        Func(toon.setAnimState, "Neutral"),
    )


def _toonBlockPositions(midPos: list, shape: ToonBlockShape, radius: float, h: float = 0.0, toons: list = []):
    """
    Creates the positions for a Toon Block.

    :param midPos: The middle position of the block.
    :param shape: The shape of the block to be generated.
    :param radius: The radius of the block (distance between Toons; exact interpretation depends on block shape).
    :param toons: The toons being moved.
    """
    retBlock = []
    x, y, z = midPos

    if shape is ToonBlockShape.Elevator:
        retBlock.append(Point3(x + radius, y - radius, z))  # Back right
        retBlock.append(Point3(x - radius, y - radius, z))  # Back left
        retBlock.append(Point3(x + radius, y + radius, z))  # Front right
        retBlock.append(Point3(x - radius, y + radius, z))  # Front left
        # Ideally an 8-Toon elevator should use BigElevator sort, as most bosses do, but the normal
        # 4-Toon elevator still has 8 positions defined, and the order is unique from a big elevator.
        retBlock.append(Point3(x + (radius * 3), y - radius, z))  # Back far right
        retBlock.append(Point3(x - (radius * 3), y - radius, z))  # Back far left
        retBlock.append(Point3(x + (radius * 3), y + radius, z))  # Front far right
        retBlock.append(Point3(x - (radius * 3), y + radius, z))  # Front far left
    elif shape is ToonBlockShape.BigElevator:
        retBlock.append(Point3(x + radius, y - radius, z))        # Back mid right
        retBlock.append(Point3(x - radius, y - radius, z))        # Back mid left
        retBlock.append(Point3(x + (radius * 3), y - radius, z))  # Back far right
        retBlock.append(Point3(x - (radius * 3), y - radius, z))  # Back far left
        retBlock.append(Point3(x + radius, y + radius, z))        # Front mid right
        retBlock.append(Point3(x - radius, y + radius, z))        # Front mid left
        retBlock.append(Point3(x + (radius * 3), y + radius, z))  # Front far right
        retBlock.append(Point3(x - (radius * 3), y + radius, z))  # Front far left
    elif shape is ToonBlockShape.SingleFile:
        for i in range(8):
            retBlock.append(Point3(x, y - (radius * i * 2), z))
    elif shape is ToonBlockShape.DoubleFile:
        for i in range(4):
            retBlock.append(Point3(x - radius, y - (radius * i * 2), z))
            retBlock.append(Point3(x + radius, y - (radius * i * 2), z))
    elif shape is ToonBlockShape.FourWide:
        for i in range(-3, 4, 2):
            retBlock.append(Point3(x + (radius * i), y + radius, z))
            retBlock.append(Point3(x + (radius * i), y - radius, z))
    elif shape is ToonBlockShape.EightWide:
        for i in range(-7, 8, 2):
            retBlock.append(Point3(x + (radius * i), y, z))

    # These use h and toons to more dynamically assign positions
    # Position toons in a line, centered on the midpoint. Can be rotated with h.
    elif shape is ToonBlockShape.Line:
        # Get number of actual toons
        numOfToons = len(toons) - toons.count(None)
        distanceMulti = -0.5 * (numOfToons - 1)
        for toon in toons:
            # If toon is a placeholder, put a placeholder position and skip it
            if toon is None:
                retBlock.append(None)
                continue
            # Get distance from midpoint
            distance = distanceMulti * radius
            # If distance is 0, just put them on the midpoint.
            if distance == 0:
                retBlock.append(Point3(x, y, z))
            else:
                # Displace them around a circle based on heading and distance, then apply midpoint offset.
                retBlock.append(
                    Point3(
                        x + (distance * math.cos(math.radians(h))),
                        y + (distance * math.sin(math.radians(h))),
                        z
                    )
                )
            # Increase distance multi
            distanceMulti += 1

    # Position toons in a circle, centered on the midpoint. Can be rotated with h.
    elif shape is ToonBlockShape.Circle:
        # Get number of actual toons
        numOfToons = len(toons) - toons.count(None)
        i = 0
        for toon in toons:
            # If toon is a placeholder, put a placeholder position and skip it
            if toon is None:
                retBlock.append(None)
                continue
            # If there's only one toon, just put them on the midpoint.
            if numOfToons == 1:
                retBlock.append(Point3(x, y, z))
            else:
                # Find degrees for current toon
                degrees = h + (i * (360 / numOfToons))
                # Displace them around a circle based on heading and distance, then apply midpoint offset.
                retBlock.append(
                    Point3(
                        x + (radius * math.cos(math.radians(degrees))),
                        y + (radius * math.sin(math.radians(degrees))),
                        z
                    )
                )
            i += 1

    return retBlock


def _getTargetRange(targetGroup: ToonSubEventTargetGroup, toons: list, maxPlayers: int) -> range:
    """
    Returns a range of Toons in the Toons list which are to be the target of the SubEvent.

    NPCs are placed into the Toons list at the first index
    which cannot be a player, e.g. in a 4-player miniboss
    cutscene, players occupy toons[0:4], and NPCs occupy
    toons[4:]. If fewer than max players are present,
    unoccupied spots in the Toons list are `None`, which
    isn't our problem to deal with here uwu

    :param targetGroup: The ToonSubEventTargetGroup that specifies which Toons should be affected (e.g. only NPCs).
    :param toons: Should be cutsceneDict['toons'].
    """
    if targetGroup is ToonSubEventTargetGroup.All:
        return range(len(toons))
    elif targetGroup is ToonSubEventTargetGroup.NPCs:
        return range(maxPlayers, len(toons))
    elif targetGroup is ToonSubEventTargetGroup.Players:
        return range(0, maxPlayers)

    raise CSEditorException("Got invalid ToonSubEventTargetGroup, or some other issue, while getting targetRange")
