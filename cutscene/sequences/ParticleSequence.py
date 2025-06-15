from toontown.cutscene.editor.CSEditorEnums import EventDefinitionEnum as EDE
from toontown.cutscene.editor.CSEditorEnums import SubEventArgumentType as SEAT
from toontown.cutscene.CutsceneSequenceBase import cutsceneSequence

from direct.interval.IntervalGlobal import *
from panda3d.core import Point3, LVecBase3f, LVecBase4f

from toontown.effects import DustCloud


@cutsceneSequence(name='Run Particle System', enum=EDE.particleSystemRun)
def seq_particleSystemRun(particleIndex:        SEAT.dropdown_particles = 0,
                          duration:             SEAT.slider_min_zero = 5.0,
                          delay:                SEAT.slider_min_zero = 0,
                          parentIndex:          SEAT.dropdown_node = 0,
                          renderParentIndex:    SEAT.dropdown_node = 0,
                          leaveItGoingForever:  SEAT.boolean = False,
                          cutsceneDict:         dict = None) -> Sequence:
    if len(cutsceneDict['particles']) - 1 < particleIndex:
        return Sequence()
    particleSystem = cutsceneDict['particles'][particleIndex]
    parent = cutsceneDict['nodes'][parentIndex]
    renderParent = cutsceneDict['nodes'][renderParentIndex]
    return Sequence(
        Wait(delay),
        Func(particleSystem.start, parent=parent, renderParent=renderParent),
        Func(particleSystem.softStart),
        Wait(duration),
        Func(particleSystem.softStop) if not leaveItGoingForever else Wait(0.0),
    )


@cutsceneSequence(name='Move Particle System Pos', enum=EDE.moveParticleSystemPos)
def seq_moveParticleSystemPos(particleIndex:    SEAT.dropdown_particles = 0,
                              duration:         SEAT.slider_min_zero = 0,
                              pos:              SEAT.slider_xyz = (0, 0, 0),
                              delay:            SEAT.slider_min_zero = 0,
                              blendType:        SEAT.dropdown_blendType = 'easeInOut',
                              startPos:         SEAT.slider_xyz = (0, 0, 0),
                              useStartPos:      SEAT.boolean = 0,
                              cutsceneDict: dict = None) -> Sequence:
    if len(cutsceneDict['particles']) - 1 < particleIndex:
        return Sequence()
    if not useStartPos:
        startPos = None
    else:
        startPos = LVecBase3f(*startPos)
    particleSystem = cutsceneDict['particles'][particleIndex]
    return Sequence(
        Wait(delay),
        LerpPosInterval(
            nodePath=particleSystem,
            duration=duration, blendType=blendType,
            startPos=startPos, pos=LVecBase3f(*pos),
        )
    )


@cutsceneSequence(name='Particle System: HPR Interval', enum=EDE.moveParticleSystemHpr)
def seq_moveParticleSystemHpr(particleIndex:    SEAT.dropdown_particles = 0,
                              duration:         SEAT.slider_min_zero = 0,
                              hpr:              SEAT.slider_hpr = (0, 0, 0),
                              delay:            SEAT.slider_min_zero = 0,
                              blendType:        SEAT.dropdown_blendType = 'easeInOut',
                              startHpr:         SEAT.slider_hpr = (0, 0, 0),
                              useStartHpr:      SEAT.boolean = 0,
                              cutsceneDict: dict = None) -> Sequence:
    """this straight up does not work bruh"""
    if len(cutsceneDict['particles']) - 1 < particleIndex:
        return Sequence()
    if not useStartHpr:
        startHpr = None
    else:
        startHpr = LVecBase3f(*startHpr)
    particleSystem = cutsceneDict['particles'][particleIndex]
    return Sequence(
        Wait(delay),
        LerpHprInterval(
            nodePath=particleSystem.attachNewNode('np'),
            duration=duration, blendType=blendType,
            startHpr=startHpr, hpr=LVecBase3f(*hpr),
        )
    )


@cutsceneSequence(name='Dye Particle System', enum=EDE.dyeParticleSystem)
def seq_dyeParticleSystem(particleIndex:    SEAT.dropdown_particles = 0,
                          argumentIndex:    SEAT.dropdown_arguments = 0,
                          cutsceneDict:     dict = None) -> Sequence:
    """Dyes a particle system a given col.
    WARNING: PRETTY BROKEN, DO NOT USE IN ACTUAL SEQUENCE
    JUST DYE THEM DIRECTLY (see WagerBeans.py)
    """
    if not (0 <= particleIndex < len(cutsceneDict['particles'])):
        return Sequence()
    if not (0 <= argumentIndex < len(cutsceneDict['arguments'])):
        return Sequence()
    par = cutsceneDict['particles'][particleIndex]
    col = cutsceneDict['arguments'][argumentIndex]
    if not (par and col):
        # Particle and color undefined
        return Sequence()
    # Verfiy this color
    if type(col) is not list:
        return Sequence()
    if len(col) != 4:
        return Sequence()

    # Dye the particles
    def particleDye():
        for particle in par.getParticlesList():
            if hasattr(particle.renderer, 'setColor'):
                particle.renderer.setColor(LVecBase4f(*col))
            else:
                cim = particle.renderer.getColorInterpolationManager()
                cim.addConstant(0.0, 1.0, LVecBase4f(*col), True)

    return Sequence(Func(particleDye))


@cutsceneSequence(name='Effect: Dustcloud (UNSTABLE IN EDITOR, CAN CRASH)', enum=EDE.dustcloudNode)
def seq_performDustcloud(nodeIndex:        SEAT.dropdown_node = 0,
                         posOffset:        SEAT.slider_xyz = (0, 0, 3),
                         scale:            SEAT.slider_min_zero = 0.4,
                         delay:            SEAT.slider_min_zero = 0.0,
                         rate:             SEAT.slider_min_zero = 24,
                         reattachToRender: SEAT.boolean = True,
                         fBillboard:       SEAT.boolean = False,
                         wantSound:        SEAT.boolean = True,
                         cutsceneDict:     dict = None):
    """Performs a dustcloud effect on a node."""
    node = cutsceneDict['nodes'][nodeIndex]
    if not node:
        return Sequence()
    dustCloud = DustCloud.DustCloud(fBillboard=fBillboard, wantSound=wantSound)
    dustCloud.setBillboardAxis(2.0)

    # Position it more based-ly.
    if reattachToRender:
        dustCloud.reparentTo(render)
        dustCloud.setPos(Vec3(*node.getPos(render)) + Vec3(*posOffset))
        dustCloud.setScale(node.getScale(render) * scale)

        # Now play the track.
        dustCloud.createTrack(rate=rate)
        return Sequence(
            Wait(delay),
            dustCloud.track,
            Func(dustCloud.destroy) if dustCloud else Wait(0.0),
            name='dustCloudIval',
        )
    else:
        # Default dustcloud behavior
        dustCloud.setPos(*posOffset)
        dustCloud.setScale(scale)
        dustCloud.createTrack(rate=rate)
        return Sequence(
            Wait(delay),
            Func(dustCloud.reparentTo, node),
            dustCloud.track,
            Func(dustCloud.destroy),
            name='dustCloudIval',
        )
