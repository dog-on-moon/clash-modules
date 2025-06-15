from direct.showbase.PythonUtil import lerp

from toontown.battle import BattleProps, MovieUtil
from toontown.battle.BattleProps import globalPropPool
from toontown.cutscene.editor.CSEditorEnums import EventDefinitionEnum as EDE
from toontown.cutscene.editor.CSEditorEnums import SubEventArgumentType as SEAT
from toontown.cutscene.CutsceneSequenceBase import cutsceneSequence, getUniqueCutsceneId
from toontown.cutscene.CutsceneSequenceHelpers import getHprBetweenPoints, NodePathWithState

from panda3d.core import Point3, LVecBase4f, LVecBase3f, Vec3
from direct.interval.IntervalGlobal import *

"""
All cutscene sequences
"""


@cutsceneSequence(name='Boss Cog: Show', enum=EDE.showBoss)
def seq_showBoss(bossIndex:     SEAT.dropdown_bosses = 0,
                 cutsceneDict:  dict = None) -> Parallel:
    retParallel = Parallel()
    boss = cutsceneDict['bosses'][bossIndex]
    if not boss:
        return Sequence()
    retParallel.append(Func(boss.unstash))
    # retParallel.append(Func(boss.showNametag2d))
    retParallel.append(Func(boss.showNametag3d))
    return retParallel


@cutsceneSequence(name='Boss Cog: Hide', enum=EDE.hideBoss)
def seq_hideBoss(bossIndex:     SEAT.dropdown_bosses = 0,
                 cutsceneDict:  dict = None) -> Parallel:
    """Hides a boss."""
    retParallel = Parallel()
    boss = cutsceneDict['bosses'][bossIndex]
    if not boss:
        return Sequence()
    retParallel.append(Func(boss.stash))
    retParallel.append(Func(boss.hideNametag2d))
    retParallel.append(Func(boss.hideNametag3d))
    return retParallel


@cutsceneSequence(name='Boss Cog: Show All', enum=EDE.showBosses)
def seq_showBosses(cutsceneDict: dict = None) -> Parallel:
    retParallel = Parallel()
    for boss in cutsceneDict['bosses']:
        if not boss:
            continue
        retParallel.append(Func(boss.unstash))
        # retParallel.append(Func(suit.showNametag2d))
        retParallel.append(Func(boss.showNametag3d))
    return retParallel


@cutsceneSequence(name='Boss Cog: Hide All', enum=EDE.hideBosses)
def seq_hideBosses(cutsceneDict: dict = None) -> Parallel:
    retParallel = Parallel()
    for boss in cutsceneDict['suits']:
        if not boss:
            continue
        retParallel.append(Func(boss.stash))
        retParallel.append(Func(boss.hideNametag2d))
        retParallel.append(Func(boss.hideNametag3d))
    return retParallel


@cutsceneSequence(name='Boss Cog: Animation', enum=EDE.doBossAnimation)
def seq_bossAnim(bossIndex:     SEAT.dropdown_bosses = 0,
                 anim:          SEAT.dropdown_boss_anims = 'Ff_neutral',
                 loop:          SEAT.boolean = 0,
                 hasDuration:   SEAT.boolean = 0,
                 duration:      SEAT.slider_min_zero = 0,
                 hasStartTime:  SEAT.boolean = 0,
                 startTime:     SEAT.slider_min_zero = 0,
                 hasEndTime:    SEAT.boolean = 0,
                 endTime:       SEAT.slider_min_zero = 0,
                 playRate:      SEAT.slider_float = 1,
                 useEndAnim:    SEAT.boolean = 0,
                 endAnim:       SEAT.dropdown_boss_anims = 'Ff_neutral',
                 isInterval:    SEAT.boolean = 1,
                 cutsceneDict:  dict = None) -> Sequence:
    """Makes a suit do an animation."""
    boss = cutsceneDict['bosses'][bossIndex]
    if not boss:
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
    animDuration = boss.getDuration(anim)
    animFrameCount = boss.getNumFrames(anim)
    startFrame = round((startTime / max(animDuration, 0.01)) * animFrameCount) if startTime else 0
    endFrame = round((endTime / max(animDuration, 0.01)) * animFrameCount) if endTime else animFrameCount

    if not loop:
        return Parallel(
            ActorInterval(boss, anim, loop=loop, duration=duration,
                          startTime=startTime, endTime=endTime,
                          playRate=playRate) if isInterval else Func(
                boss.play, anim, None, startFrame, endFrame
            ),
            Sequence(
                Wait(duration),
                ActorInterval(boss, endAnim)
            ) if duration and endAnim else Sequence(),
        )
    else:
        return Sequence(
            Func(boss.loop, anim),
        )


@cutsceneSequence(name='Boss Cog: Roll To Point', enum=EDE.bossRollToPoint)
def seq_bossRollToPoint(bossIndex:     SEAT.dropdown_bosses = 0,
                        fromPos:       SEAT.slider_xyz = (0, 0, 0),
                        fromHpr:       SEAT.slider_hpr = (0, 0, 0),
                        toPos:         SEAT.slider_xyz = (0, 0, 0),
                        toHpr:         SEAT.slider_hpr = (0, 0, 0),
                        reverse:       SEAT.boolean = False,
                        cutsceneDict:  dict = None) -> Sequence:
    """Makes a boss roll to the given point."""
    boss = cutsceneDict['bosses'][bossIndex]
    if not boss:
        return Sequence()

    track, hpr = boss.rollBossToPoint(Vec3(*fromPos), Vec3(*fromHpr), Vec3(*toPos), Vec3(*toHpr), reverse)
    return Sequence(track)
