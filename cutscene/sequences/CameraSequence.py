from toontown.cutscene.editor.CSEditorEnums import EventDefinitionEnum as EDE
from toontown.cutscene.editor.CSEditorEnums import SubEventArgumentType as SEAT
from toontown.cutscene.CutsceneSequenceBase import cutsceneSequence

from panda3d.core import LVecBase3f
from direct.interval.IntervalGlobal import *

from toontown.toonbase import ToontownGlobals

ElevatorFOV = ToontownGlobals.CBElevatorFov
cam = camera
camLens = base.camLens


@cutsceneSequence(name='Camera: Move Sequence', enum=EDE.moveCameraPos)
def seq_moveCameraPos(duration:     SEAT.slider_min_zero = 0.0,
                      delay:        SEAT.slider_min_zero = 0.0,
                      pos:          SEAT.slider_xyz_camera = (0, 0, 0),
                      blendType:    SEAT.dropdown_blendType = 'easeInOut',
                      startPos:     SEAT.slider_xyz_camera = (0, 0, 0),
                      useStartPos:  SEAT.boolean = 0,
                      cutsceneDict: dict = None) -> Sequence:
    if not cutsceneDict['affectsCamera']:
        return Sequence()

    if not useStartPos:
        startPos = None
    else:
        startPos = LVecBase3f(*startPos)
    return Sequence(
        Wait(delay),
        LerpPosInterval(
            nodePath=cam,
            duration=duration, blendType=blendType,
            startPos=startPos, pos=LVecBase3f(*pos),
        )
    )


@cutsceneSequence(name='Camera: Rotate Sequence', enum=EDE.moveCameraHpr)
def seq_moveCameraHpr(duration:     SEAT.slider_min_zero = 0.0,
                      delay:        SEAT.slider_min_zero = 0.0,
                      hpr:          SEAT.slider_hpr_camera = (0, 0, 0),
                      blendType:    SEAT.dropdown_blendType = 'easeInOut',
                      startHpr:     SEAT.slider_hpr_camera = (0, 0, 0),
                      useStartHpr:  SEAT.boolean = 0,
                      cutsceneDict: dict = None) -> Sequence:
    if not cutsceneDict['affectsCamera']:
        return Sequence()

    if not useStartHpr:
        startHpr = None
    else:
        startHpr = LVecBase3f(*startHpr)
    return Sequence(
        Wait(delay),
        LerpHprInterval(
            nodePath=cam,
            duration=duration, blendType=blendType,
            startHpr=startHpr, hpr=LVecBase3f(*hpr),
        )
    )


@cutsceneSequence(name='Camera: Move/Rotate Sequence', enum=EDE.moveCameraPosHpr)
def seq_moveCameraPosHpr(duration:      SEAT.slider_min_zero = 0.0,
                         delay:         SEAT.slider_min_zero = 0.0,
                         pos:           SEAT.slider_xyz_camera = (0, 0, 0),
                         hpr:           SEAT.slider_hpr_camera = (0, 0, 0),
                         useStartPos:   SEAT.boolean = 0,
                         useStartHpr:   SEAT.boolean = 0,
                         blendType:     SEAT.dropdown_blendType = 'easeInOut',
                         startPos:      SEAT.slider_xyz_camera = (0, 0, 0),
                         startHpr:      SEAT.slider_hpr_camera = (0, 0, 0),
                         cutsceneDict:  dict = None) -> Sequence:
    if not cutsceneDict['affectsCamera']:
        return Sequence()

    if not useStartPos:
        startPos = None
    else:
        startPos = LVecBase3f(*startPos)
    if not useStartHpr:
        startHpr = None
    else:
        startHpr = LVecBase3f(*startHpr)
    return Sequence(
        Wait(delay),
        LerpPosHprInterval(
            nodePath=cam,
            duration=duration, blendType=blendType,
            startPos=startPos, pos=LVecBase3f(*pos),
            startHpr=startHpr, hpr=LVecBase3f(*hpr),
        )
    )


@cutsceneSequence(name='Camera: FOV Sequence', enum=EDE.changeCameraFov)
def seq_changeCameraFov(duration:       SEAT.slider_min_zero = 0.0,
                        delay:          SEAT.slider_min_zero = 0.0,
                        end:            SEAT.slider_fov = 42,
                        blendType:      SEAT.dropdown_blendType = 'easeInOut',
                        start:          SEAT.slider_fov = 42,
                        useStart:       SEAT.boolean = 0,
                        cutsceneDict:   dict = None) -> Sequence:
    if not cutsceneDict['affectsCamera']:
        return Sequence()

    def setFov(t):
        if t != 0:
            camLens.setMinFov(t)

    if (not start) or (not useStart):
        start = camLens.getMinFov()
    return Sequence(
        Wait(delay),
        LerpFunctionInterval(
            function=setFov,
            duration=duration, blendType=blendType,
            fromData=start, toData=end,
        )
    )


@cutsceneSequence(name='Camera: Reparent to Node', enum=EDE.reparentCamera)
def seq_reparentCamera(targetIndex:     SEAT.dropdown_node = 0,
                       wrt:             SEAT.boolean = 0,
                       cutsceneDict:    dict = None) -> Sequence:
    if not cutsceneDict['affectsCamera']:
        return Sequence()

    if cutsceneDict['nodes'][targetIndex] is cam:
        return Sequence()
    if wrt:
        return Func(cam.wrtReparentTo, cutsceneDict['nodes'][targetIndex])
    else:
        return Func(cam.reparentTo, cutsceneDict['nodes'][targetIndex])


@cutsceneSequence(name='Camera: Move to Elevator', enum=EDE.cameraToElevator, hidden=True)
def seq_putCameraToElevator(elevatorModelIndex: SEAT.dropdown_elevators = 0.0,
                            cutsceneDict:       dict = None) -> Parallel:
    if not cutsceneDict['affectsCamera']:
        return Sequence()

    return Parallel(
        Func(cam.reparentTo, cutsceneDict['elevators'][elevatorModelIndex]),
        seq_moveCameraPosHpr(
            duration=0.0, delay=0.0, pos=[0, 12, 4], hpr=[180, 0, 0],
            useStartPos=False, useStartHpr=False, blendType='noBlend',
            startPos=[0, 0, 0], startHpr=[0, 0, 0], cutsceneDict=cutsceneDict,
        ),
    )

