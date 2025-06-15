import random

from direct.gui.OnscreenText import OnscreenText
from direct.showbase.PythonUtil import lerp

from toontown.battle.BattleProps import globalPropPool
from toontown.battle.BattleSounds import globalBattleSoundCache
from toontown.cutscene.CutsceneSequenceHelpers import NodePathWithState, getHprBetweenPoints
from toontown.cutscene.editor.CSEditorEnums import EventDefinitionEnum as EDE
from toontown.cutscene.editor.CSEditorEnums import SubEventArgumentType as SEAT
from toontown.cutscene.CutsceneSequenceBase import cutsceneSequence, getUniqueCutsceneId

from direct.interval.IntervalGlobal import *

from toontown.toonbase import ToontownGlobals
from toontown.toonbase.ToontownTimer import ToontownTimer
from toontown.utils import ColorHelper

from panda3d.core import *


@cutsceneSequence(name='Major Player: Apply Stagelight', enum=EDE.applyStagelight)
def seq_applyStagelight(targetIndex:        SEAT.dropdown_actors = None,
                        delay:              SEAT.slider_min_zero = 0.0,
                        stagelightAlpha:    SEAT.slider_min_zero = 0.28,
                        disableColorScale:  SEAT.boolean = True,
                        fadeawayDuration:   SEAT.slider_min_zero = 0.0,
                        cutsceneDict:       dict = None, **kwargs) -> Sequence:
    """Applies a stagelight effect onto a target."""
    # Do we have a target?
    target = cutsceneDict['actors'][targetIndex]
    if not target:
        return Sequence()

    # Hack to clear a stagelight
    if hasattr(target, 'cutsceneStagelight'):
        target.cutsceneStagelight.removeNode()
        del target.cutsceneStagelight

    # Make the stagelight.
    stagelight = globalPropPool.getProp('stagelight')
    setattr(target, 'cutsceneStagelight', stagelight)
    stagelight.hide()
    node = stagelight.node()
    node.setBounds(OmniBoundingVolume())
    node.setFinal(1)
    stagelight.find('**/stagelight').hide()

    # Position the stagelight.
    stagelight.reparentTo(target)
    stagelight.setPos(0, 0, 15 * 2)
    stagelight.setScale(1, 1, 2)
    stagelight.setColor(ColorHelper.hexToPCol('FEFDA8', a=int(stagelightAlpha * 255)))

    target.setColorScale(1, 1, 1, 1)

    # Stagelight SFX sequence
    soundIval = SoundInterval(sound=loader.loadSfx('phase_11/audio/sfx/LB_camera_shutter_2.ogg'))

    if fadeawayDuration != 0.0:
        soundIval = Parallel(
            soundIval,
            Sequence(
                LerpColorInterval(
                    nodePath=stagelight, duration=fadeawayDuration,
                    color=ColorHelper.hexToPCol('FEFDA8', a=0),
                    startColor=ColorHelper.hexToPCol('FEFDA8', a=int(stagelightAlpha * 255)),
                    blendType='easeOut',
                ),
                Func(stagelight.hide),
            )
        )

    return Sequence(
        Wait(delay),
        Func(stagelight.show),
        (Func(target.setColorScaleOff, 1) if disableColorScale else Wait(0.0)),
        # (Func(target.overrideClearScaleFunc, target) if disableColorScale else Wait(0.0)),
        soundIval,
    )


@cutsceneSequence(name='Timescale: Show Change', enum=EDE.showTimescaleChange)
def seq_timescaleChange(enterDuration: SEAT.slider_min_zero = 1.0,
                        holdDuration:  SEAT.slider_min_zero = 1.0,
                        exitDuration:  SEAT.slider_min_zero = 1.0,
                        timerScale:    SEAT.slider_min_zero = 1.0,
                        cutsceneDict:  dict = None) -> Sequence:
    # Create the timer.
    startScale, endScale, *_ = cutsceneDict['arguments']
    timer = ToontownTimer()
    timer.setScale(timerScale)
    timer.hide()
    OnscreenText(
        parent=timer,
        text='Battle Speed',
        scale=0.27,
        pos=(0, -0.55),
        fg=(1, 1, 1, 1),
        font=ToontownGlobals.getSignFont(),
    )

    def setTime(time):
        if timer:
            timer.setTimeStr(f'x{"{:.2f}".format(time)}', scale=0.145)
    setTime(startScale)

    def lerpTimerText(t):
        setTime(lerp(startScale, endScale, t))

    # Make our sequence.
    return Sequence(
        # Enter Interval
        Func(timer.show),
        LerpPosInterval(
            timer, enterDuration,
            pos=(0, 0, 0), startPos=(0, 0, 2.0),
            blendType='easeOut',
        ),
        # Hold Interval
        LerpFunctionInterval(
            lerpTimerText, duration=holdDuration, blendType='easeInOut',
        ),
        # Leave Interval
        LerpPosInterval(
            timer, exitDuration,
            pos=(0, 0, -2.0), startPos=(0, 0, 0),
            blendType='easeIn',
        ),
        # Cleanup
        Func(timer.destroy),
    )


@cutsceneSequence(name='Suit: Heavy Drop Death', enum=EDE.heavyDropKill, hidden=True)
def seq_heavyDropKill(suitIndex:    SEAT.dropdown_suits = 0,
                      cutsceneDict: dict = None) -> Sequence:
    """
    Kills a suit with heavy drop.
    """
    suit = cutsceneDict['suits'][suitIndex]
    if not suit:
        return Sequence()

    crushSound = globalBattleSoundCache.getSound('TL_train_cog.ogg')
    fallSound = globalBattleSoundCache.getSound('cogbldg_land.ogg')
    suitScale = suit.getScale()

    # Functions for quick death drop extension.
    finalSeq = Sequence(
        Wait(3),  # Delay 3 seconds
        LerpScaleInterval(suit, 0.5, (0.01, 0.01, 0.01), blendType='easeIn'),  # Shrink the silhouette
        Func(suit.hide),  # Hide the silhouette
    )

    # Define this here so that we can grab the length.
    suitFlatten = Sequence(
        Parallel(LerpFunc(suit.setZ, duration=0.125, fromData=suit.getZ(), toData=suit.getZ() - 1),
                 ActorInterval(suit, 'flatten', startFrame=0, endFrame=4)))
    suitFlattenDuration = suitFlatten.getDuration() - 0.3

    def waitPlaySquishSound():
        seq = Sequence(Wait(suitFlattenDuration), Func(base.playSfx, crushSound))
        seq.start()

    suitReact = Sequence(Func(waitPlaySquishSound),  # Set up our squish sound now to time it properly
                         suitFlatten,
                         # Suit falls through the floor a little bit, play the first few frames of the crush animation
                         Func(suit.nametag3d.hide),
                         Func(base.playSfx, fallSound, volume=0.65),  # Play fall sfx
                         Func(suit.clearSplats),  # Clear suit splats
                         Func(suit.setColor, (0, 0, 0, 1)),  # THE BLACKENED
                         Func(suit.pose, 'flatten', 5),  # Flatten the suit
                         # Position the suit slightly above the ground to prevent clipping
                         Func(suit.setZ, (suit.getZ() + 0.1)),
                         Func(suit.setScale, suitScale[0], suitScale[1], 0.025),
                         # Set the scale of the suit to be regular, but flattened
                         Func(suit.specialHead.pose, 'neutral', 0) if suit.specialHead else Sequence(),
                         # Stop the animated head if it exists
                         finalSeq,
                         Func(suit.setColor, 1, 1, 1, 1),
                         LerpScaleInterval(suit, 0.0, (1.0, 1.0, 1.0)),
                         Func(suit.loop, 'neutral'),
                         )
    return suitReact


@cutsceneSequence(name='Cannon: Fake Control', enum=EDE.fakeCannonControl)
def seq_toonFireFromCannon(nodeIndex:  SEAT.dropdown_node = 0,
                           delay:      SEAT.slider_min_zero = 0,
                           posOffset:  SEAT.slider_xyz = (0, 0, 0),
                           startHpr:   SEAT.slider_hpr = (0, 0, 0),
                           hpr:        SEAT.slider_hpr = (0, 0, 0),
                           awakenTime: SEAT.slider_min_zero = 2.0,
                           adjustTime: SEAT.slider_min_zero = 0.6,
                           holdTime:   SEAT.slider_min_zero = 2.0,
                           cogCannon:  SEAT.boolean = True,
                           cutsceneDict: dict = None) -> Sequence:

    # This whole function is pretty jank when using the editor timeline, so beware.

    point = cutsceneDict['nodes'][nodeIndex]
    if not point:
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
    scaleFactor = 1.6
    iScale = 1 / scaleFactor
    barrel.setScale(scaleFactor, 1, scaleFactor)

    soundCannonAdjust = base.loader.loadSfx('phase_4/audio/sfx/MG_cannon_adjust.ogg')
    playSoundCannonAdjust = SoundInterval(soundCannonAdjust, duration=adjustTime, node=cannonHolder)

    def setupCannonAndCog():
        cannon.setPos(0, 0, -8.6)
        cannonHolder.setH(0)
        barrel.setHpr(0, 90, 0)
        referenceNode.setPos(point.getPos(render))
        referenceNode.setHpr(point.getHpr(render))
        cannonAttachPoint.setScale(iScale, 1, iScale)
        cannonAttachPoint.setPos(0, 6.7, 0)

    # Allow for aiming at point
    eventId = getUniqueCutsceneId()

    # Get the goal H for this toon.
    def updateHpr(t):
        # Wrapping this in a function call
        # to ensure it works properly.
        endH, endP, _ = hpr
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

    rotateToPointTrack = Sequence(
        Func(updateStartHpr),
        LerpFunctionInterval(
            function=updateHpr,
            duration=adjustTime,
            blendType='easeIn'
        )
    )

    reactIval = Parallel(
        Func(setupCannonAndCog),
        Func(referenceNode.show),
        Sequence(LerpPosHprInterval(cannonHolder, awakenTime,
                                Point3(0, 0, 7) + Point3(*posOffset), Vec3(*startHpr),
                                startPos=Point3(*posOffset),
                                blendType='easeInOut'),
                Parallel(rotateToPointTrack,
                        playSoundCannonAdjust),
                Wait(holdTime),
                Parallel(LerpHprInterval(barrel, adjustTime,
                                        Point3(0, 90, 0),
                                        blendType='easeOut'),
                        playSoundCannonAdjust),
                LerpPosInterval(cannonHolder, 1.0,
                                Point3(*posOffset),
                                blendType='easeInOut')),
        )
    removeThese = (
        referenceNode,
        cannonHolder,
        cannon,
        barrel,
        cannonAttachPoint,
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
