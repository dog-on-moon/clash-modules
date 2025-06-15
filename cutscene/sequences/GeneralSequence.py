import random

from toontown.battle import MovieUtil
from toontown.cutscene.editor.CSEditorEnums import EventDefinitionEnum as EDE
from toontown.cutscene.editor.CSEditorEnums import SubEventArgumentType as SEAT
from toontown.cutscene.CutsceneSequenceBase import cutsceneSequence
from toontown.building import ElevatorUtils, ElevatorConstants

from direct.interval.IntervalGlobal import *
from panda3d.core import Point3, LVecBase3f, LVecBase4f
from panda3d.otp import CFSpeech, CFTimeout

from toontown.suit.Suit import Suit


@cutsceneSequence(name='Actor: Dialogue', enum=EDE.actorDialogue)
def seq_actorDialogue(messageIndex:     SEAT.dropdown_messages = 0,
                      actorIndex:       SEAT.dropdown_actors = 0,
                      delay:            SEAT.slider_min_zero = 0.0,
                      duration:         SEAT.slider_min_zero = 3.0,
                      moveNametag:      SEAT.boolean = False,
                      xyz:              SEAT.slider_xyz = (0, 0, 0),
                      scale:            SEAT.slider_min_zero = 1.0,
                      hideNametag:      SEAT.boolean = False,
                      wantHeadAnim:     SEAT.boolean = True,
                      wantSound:        SEAT.boolean = True,
                      disable:          SEAT.boolean = False,
                      bindToHead:       SEAT.boolean = False,
                      cutsceneDict:     dict = None) -> Sequence:
    """
    Condenses dialogue related things into one sequence.
    Can define a duration, move the nametag (speech bubble), and hide the nametag afterwards.
    If the nametag is moved, it will move back to the original position after the dialogue duration.
    """
    if disable:
        return Sequence()
    actor = cutsceneDict['actors'][actorIndex]
    nametag = actor.nametag3d
    track = Sequence(Wait(delay))
    originalScale = nametag.getScale()
    if moveNametag:
        originalPos = nametag.getPos()
        track.append(Func(nametag.setPos, LVecBase3f(*xyz)))
    ogParent = nametag.getParent()
    if bindToHead and hasattr(actor, 'specialHead'):
        track.append(Func(nametag.reparentTo, actor.specialHead))
    if isinstance(actor, Suit):
        chatFunc = Func(actor.setChatAbsolute, cutsceneDict['messages'][messageIndex], CFSpeech | CFTimeout, wantHeadAnim=wantHeadAnim, wantSound=wantSound)
    else:
        chatFunc = Func(actor.setChatAbsolute, cutsceneDict['messages'][messageIndex], CFSpeech | CFTimeout)
    track = Sequence(
        track,
        Func(nametag.setScale, scale),
        Func(nametag.show),
        chatFunc,
        Wait(duration),
        Func(actor.clearChat),
        Func(nametag.setScale, originalScale)
    )
    if hideNametag:
        track.append(Func(nametag.hide))
    if bindToHead:
        track.append(Func(nametag.reparentTo, ogParent))
    if moveNametag:
        track.append(Func(nametag.setPos, originalPos))
    return track


@cutsceneSequence(name='Actor: Iterative Dialogue', enum=EDE.actorDialogueIt)
def seq_actorDialogueIt(messageIndex:     SEAT.dropdown_messages = 0,
                      actorIndex:       SEAT.dropdown_actors = 0,
                      delay:            SEAT.slider_min_zero = 0.0,
                      duration:         SEAT.slider_min_zero = 3.0,
                      moveNametag:      SEAT.boolean = False,
                      xyz:              SEAT.slider_xyz = (0, 0, 0),
                      scale:            SEAT.slider_min_zero = 1.0,
                      hideNametag:      SEAT.boolean = False,
                      disable:          SEAT.boolean = False,
                      cutsceneDict:     dict = None) -> Sequence:
    '''
    Condenses dialogue related things into one sequence.
    Can define a duration, move the nametag (speech bubble), and hide the nametag afterwards.
    If the nametag is moved, it will move back to the original position after the dialogue duration.
    '''
    if disable:
        return Sequence()
    actor = cutsceneDict['actors'][actorIndex]
    nametag = actor.nametag3d
    track = Sequence(Wait(delay))
    originalScale = nametag.getScale()
    if moveNametag:
        originalPos = nametag.getPos()
        track.append(Func(nametag.setPos, LVecBase3f(*xyz)))
    track = Sequence(
        track,
        Func(nametag.setScale, scale),
        Func(nametag.show),
        Func(actor.setChatIterative,
             cutsceneDict['messages'][messageIndex], CFSpeech | CFTimeout),
        Wait(duration),
        Func(actor.clearChat),
        Func(nametag.setScale, originalScale)
    )
    if hideNametag:
        track.append(Func(nametag.hide))
    if moveNametag:
        track.append(Func(nametag.setPos, originalPos))
    return track


@cutsceneSequence(name='Actor: Show Nametag', enum=EDE.showNametag)
def seq_actorShowNametag(actorIndex:   SEAT.dropdown_actors = 0,
                         cutsceneDict: dict = None) -> Sequence:
    actor = cutsceneDict['actors'][actorIndex]
    if not actor:
        return Sequence()
    return Sequence(Func(actor.nametag3d.show))


@cutsceneSequence(name='Actor: Hide Nametag', enum=EDE.hideNametag)
def seq_actorHideNametag(actorIndex:   SEAT.dropdown_actors = 0,
                         cutsceneDict: dict = None) -> Sequence:
    actor = cutsceneDict['actors'][actorIndex]
    if not actor:
        return Sequence()
    return Sequence(Func(actor.nametag3d.hide))


@cutsceneSequence(name='Actor: Chat', enum=EDE.actorChat)
def seq_actorSays(messageIndex: SEAT.dropdown_messages = 0,
                  actorIndex:   SEAT.dropdown_actors = 0,
                  delay:        SEAT.slider_min_zero = 0.0,
                  disable:      SEAT.boolean = False,
                  cutsceneDict: dict = None) -> Sequence:
    if disable:
        return Sequence()
    return Sequence(
        Wait(delay),
        Func(cutsceneDict['actors'][actorIndex].setChatAbsolute,
             cutsceneDict['messages'][messageIndex], CFSpeech | CFTimeout)
    )


@cutsceneSequence(name='Actor: Chat Off', enum=EDE.actorShutUp)
def seq_actorUnsays(actorIndex:     SEAT.dropdown_actors = 0,
                    delay:          SEAT.slider_min_zero = 0.0,
                    cutsceneDict:   dict = None) -> Sequence:
    return Sequence(
        Wait(delay),
        Func(cutsceneDict['actors'][actorIndex].clearChat)
    )


@cutsceneSequence(name='Time Sleep', enum=EDE.timeSleep)
def seq_wait(time:          SEAT.slider_min_zero = 0.0,
             cutsceneDict:  dict = None) -> Sequence:
    return Sequence(Wait(time))


@cutsceneSequence(name='Actor: Move Sequence', enum=EDE.moveActor)
def seq_moveActor(actorIndex:   SEAT.dropdown_actors = 0,
                  duration:     SEAT.slider_min_zero = 0.0,
                  delay:        SEAT.slider_min_zero = 0.0,
                  blendType:    SEAT.dropdown_blendType = 'easeInOut',
                  xyz:          SEAT.slider_xyz = (0, 0, 0),
                  useStartPos:  SEAT.boolean = 0,
                  startPos:     SEAT.slider_xyz = (0, 0, 0),
                  cutsceneDict: dict = None) -> Sequence:
    if not useStartPos:
        startPos = None
    else:
        startPos = LVecBase3f(*startPos)
    actorDo = cutsceneDict['actors'][actorIndex]
    return Sequence(
        Wait(delay),
        LerpPosInterval(
            nodePath=actorDo,
            pos=LVecBase3f(*xyz),
            duration=duration,
            startPos=startPos,
            blendType=blendType,
        ),
    )


@cutsceneSequence(name='Actor: Turn Sequence', enum=EDE.turnActor)
def seq_turnActor(actorIndex:   SEAT.dropdown_actors = 0,
                  duration:     SEAT.slider_min_zero = 0.0,
                  delay:        SEAT.slider_min_zero = 0.0,
                  blendType:    SEAT.dropdown_blendType = 'easeInOut',
                  hpr:          SEAT.slider_hpr = (0, 0, 0),
                  useStartHpr:  SEAT.boolean = 0,
                  startHpr:     SEAT.slider_hpr = (0, 0, 0),
                  cutsceneDict: dict = None) -> Sequence:
    if not useStartHpr:
        startHpr = None
    else:
        startHpr = LVecBase3f(*startHpr)
    actorDo = cutsceneDict['actors'][actorIndex]
    return Sequence(
        Wait(delay),
        LerpHprInterval(
            nodePath=actorDo,
            hpr=LVecBase3f(*hpr),
            duration=duration,
            startHpr=startHpr,
            blendType=blendType,
        ),
    )


@cutsceneSequence(name='Node: Set Pos/HPR/Scale', enum=EDE.nodePosHprScale)
def seq_nodeSetPosHprScale(nodeIndex:       SEAT.dropdown_node = 0,
                           delay:           SEAT.slider_min_zero = 0,
                           pos:             SEAT.slider_xyz = (0, 0, 0),
                           hpr:             SEAT.slider_hpr = (0, 0, 0),
                           scale:           SEAT.slider_xyz = (1, 1, 1),
                           cutsceneDict:    dict = None) -> Sequence:
    node = cutsceneDict['nodes'][nodeIndex]

    if node is camera and not cutsceneDict['affectsCamera']:
        return Sequence()
    if node in (render, hidden):
        print('WARNING! Cutscene tried to move render or hidden!')
        return Sequence()

    return Sequence(
        Wait(delay),
        Func(node.setPos, LVecBase3f(*pos)),
        Func(node.setHpr, LVecBase3f(*hpr)),
        Func(node.setScale, LVecBase3f(*scale)),
    )


@cutsceneSequence(name='Node: Show', enum=EDE.showNode)
def seq_showNode(nodeIndex:     SEAT.dropdown_node = 0,
                 cutsceneDict:  dict = None) -> Sequence:
    node = cutsceneDict['nodes'][nodeIndex]
    if not node:
        return Sequence()
    return Sequence(Func(node.show))


@cutsceneSequence(name='Node: Hide', enum=EDE.hideNode)
def seq_hideNode(nodeIndex:     SEAT.dropdown_node = 0,
                 cutsceneDict:  dict = None) -> Sequence:
    node = cutsceneDict['nodes'][nodeIndex]
    if not node:
        return Sequence()
    return Sequence(Func(node.hide))


@cutsceneSequence(name='Node: Reparent to Node', enum=EDE.reparentNode)
def seq_reparentNode(nodeIndex:     SEAT.dropdown_node = 0,
                     targetIndex:     SEAT.dropdown_node = 0,
                     wrt:             SEAT.boolean = 0,
                     disable:         SEAT.boolean = True,
                     cutsceneDict:    dict = None) -> Sequence:
    # Disabled by default so you don't mess up your editor instance by reparenting random stuff!
    if disable:
        return Sequence()
    node = cutsceneDict['nodes'][nodeIndex]
    if node is None:
        return Sequence()
    if node is camera and not cutsceneDict['affectsCamera']:
        return Sequence()
    if node in (render, hidden):
        print('WARNING! Cutscene tried to reparent render or hidden!')
        return Sequence()

    target = cutsceneDict['nodes'][targetIndex]
    if target is node:
        return Sequence()
    if target is None:
        return Sequence()
    if wrt:
        return Func(node.wrtReparentTo, target)
    else:
        return Func(node.reparentTo, target)


@cutsceneSequence(name='Node: Move Sequence', enum=EDE.moveNode)
def seq_moveNode(nodeIndex:     SEAT.dropdown_node = 0,
                 delay:         SEAT.slider_min_zero = 0,
                 duration:      SEAT.slider_min_zero = 0.0,
                 pos:           SEAT.slider_xyz_node = (0, 0, 0),
                 startPos:      SEAT.slider_xyz_node = (0, 0, 0),
                 useStartPos:   SEAT.boolean = 0,
                 hpr:           SEAT.slider_hpr_node = (0, 0, 0),
                 startHpr:      SEAT.slider_hpr_node = (0, 0, 0),
                 useStartHpr:   SEAT.boolean = 0,
                 blendType:     SEAT.dropdown_blendType = 'easeInOut',
                 cutsceneDict:  dict = None) -> Sequence:
    node = cutsceneDict['nodes'][nodeIndex]
    if not node:
        return Sequence()
    if node is camera and not cutsceneDict['affectsCamera']:
        return Sequence()
    if node in (render, hidden):
        print('WARNING! Cutscene tried to move render or hidden!')
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
            node, duration=duration,
            pos=LVecBase3f(*pos), startPos=startPos,
            hpr=LVecBase3f(*hpr), startHpr=startHpr,
            blendType=blendType,
        )
    )


@cutsceneSequence(name='Node: Pos Relative To Other', enum=EDE.posRelativeToOther)
def seq_posRelativeToOtherNode(nodeIndex:          SEAT.dropdown_node = 0,
                               delay:              SEAT.slider_min_zero = 0,
                               duration:           SEAT.slider_min_zero = 0.0,
                               otherNodeIndex:     SEAT.dropdown_node = 0,
                               pos:                SEAT.slider_xyz_node = (0, 0, 0),
                               startPos:           SEAT.slider_xyz_node = (0, 0, 0),
                               useStartPos:        SEAT.boolean = 0,
                               blendType:          SEAT.dropdown_blendType = 'easeInOut',
                               cutsceneDict:       dict = None) -> Sequence:
    node = cutsceneDict['nodes'][nodeIndex]
    if not node:
        return Sequence()
    otherNode = cutsceneDict['nodes'][otherNodeIndex]
    if not otherNode:
        return Sequence()
    if node is camera and not cutsceneDict['affectsCamera']:
        return Sequence()
    if node in (render, hidden):
        print('WARNING! Cutscene tried to move render or hidden!')
        return Sequence()

    if not useStartPos:
        startPos = None
    else:
        startPos = LVecBase3f(*startPos)

    return Sequence(
        Wait(delay),
        LerpPosInterval(
            node, duration=duration,
            pos=LVecBase3f(*pos), startPos=startPos,
            other=otherNode, blendType=blendType,
        )
    )


@cutsceneSequence(name='Node: Rotate Sequence', enum=EDE.rotateNode)
def seq_rotateNode(nodeIndex:     SEAT.dropdown_node = 0,
                   delay:         SEAT.slider_min_zero = 0,
                   duration:      SEAT.slider_min_zero = 0.0,
                   hpr:           SEAT.slider_hpr_node = (0, 0, 0),
                   startHpr:      SEAT.slider_hpr_node = (0, 0, 0),
                   useStartHpr:   SEAT.boolean = 0,
                   blendType:     SEAT.dropdown_blendType = 'easeInOut',
                   cutsceneDict:  dict = None) -> Sequence:
    node = cutsceneDict['nodes'][nodeIndex]
    if not node:
        return Sequence()
    if node is camera and not cutsceneDict['affectsCamera']:
        return Sequence()
    if node in (render, hidden):
        print('WARNING! Cutscene tried to rotate render or hidden!')
        return Sequence()

    if not useStartHpr:
        startHpr = None
    else:
        startHpr = LVecBase3f(*startHpr)
    return Sequence(
        Wait(delay),
        LerpHprInterval(
            node, duration=duration,
            hpr=LVecBase3f(*hpr), startHpr=startHpr,
            blendType=blendType,
        )
    )


@cutsceneSequence(name='Node: Scale Sequence', enum=EDE.scaleNode)
def seq_scaleNode(nodeIndex:        SEAT.dropdown_node = 0,
                  delay:            SEAT.slider_min_zero = 0,
                  duration:         SEAT.slider_min_zero = 0,
                  scale:            SEAT.slider_xyz = (1, 1, 1),
                  startScale:       SEAT.slider_xyz = (1, 1, 1),
                  useStartScale:    SEAT.boolean = 0,
                  blendType:        SEAT.dropdown_blendType = 'easeInOut',
                  cutsceneDict:     dict = None) -> Sequence:
    node = cutsceneDict['nodes'][nodeIndex]
    if not node:
        return Sequence()
    if node is camera and not cutsceneDict['affectsCamera']:
        return Sequence()
    if node in (render, hidden):
        print('WARNING! Cutscene tried to scale render or hidden!')
        return Sequence()

    if not useStartScale:
        startScale = None
    if scale:
        scale = list(scale)
        scale[0] = max(scale[0], 0.001)
        scale[1] = max(scale[1], 0.001)
        scale[2] = max(scale[2], 0.001)
        scale = tuple(scale)
    if startScale:
        startScale = list(startScale)
        startScale[0] = max(startScale[0], 0.001)
        startScale[1] = max(startScale[1], 0.001)
        startScale[2] = max(startScale[2], 0.001)
        startScale = tuple(startScale)
    return Sequence(
        Wait(delay),
        LerpScaleInterval(
            node, duration=duration, scale=scale, startScale=startScale, blendType=blendType,
        )
    )


@cutsceneSequence(name='Node: Color Scale Sequence', enum=EDE.colorScaleNode)
def seq_colorScaleNode(nodeIndex:           SEAT.dropdown_node = 0,
                       delay:               SEAT.slider_min_zero = 0,
                       duration:            SEAT.slider_min_zero = 0,
                       colorScale:          SEAT.slider_rgb = (1, 1, 1, 1),
                       startColorScale:     SEAT.slider_rgb = (1, 1, 1, 1),
                       useStartColorScale:  SEAT.boolean = 0,
                       blendType:           SEAT.dropdown_blendType = 'easeInOut',
                       cutsceneDict:        dict = None) -> Sequence:
    node = cutsceneDict['nodes'][nodeIndex]
    if not node:
        return Sequence()
    if node is camera and not cutsceneDict['affectsCamera']:
        return Sequence()

    if not useStartColorScale:
        startColorScale = None

    if colorScale:
        colorScale = LVecBase4f(*colorScale)
    if startColorScale:
        startColorScale = LVecBase4f(*startColorScale)

    return Sequence(
        Wait(delay),
        LerpColorScaleInterval(
            node, duration=duration, colorScale=colorScale, startColorScale=startColorScale, blendType=blendType,
        )
    )


@cutsceneSequence(name='Node: Alpha Scale Sequence', enum=EDE.alphaScaleNode)
def seq_alphaScaleNode(nodeIndex:           SEAT.dropdown_node = 0,
                       delay:               SEAT.slider_min_zero = 0,
                       duration:            SEAT.slider_min_zero = 0,
                       alphaScale:          SEAT.slider_min_zero = 1,
                       startAlphaScale:     SEAT.slider_min_zero = 1,
                       blendType:           SEAT.dropdown_blendType = 'easeInOut',
                       cutsceneDict:        dict = None) -> Sequence:
    node = cutsceneDict['nodes'][nodeIndex]
    if not node:
        return Sequence()
    if node is camera and not cutsceneDict['affectsCamera']:
        return Sequence()

    return Sequence(
        Wait(delay),
        LerpFunctionInterval(
            node.setAlphaScale, duration=duration, fromData=startAlphaScale, toData=alphaScale, blendType=blendType,
        )
    )


@cutsceneSequence(name='Node: Color Sequence', enum=EDE.colorNode)
def seq_colorNode(nodeIndex:      SEAT.dropdown_node = 0,
                  delay:          SEAT.slider_min_zero = 0,
                  duration:       SEAT.slider_min_zero = 0,
                  color:          SEAT.slider_rgb = (1, 1, 1, 1),
                  startColor:     SEAT.slider_rgb = (1, 1, 1, 1),
                  useStartColor:  SEAT.boolean = 0,
                  blendType:      SEAT.dropdown_blendType = 'easeInOut',
                  cutsceneDict:   dict = None) -> Sequence:
    node = cutsceneDict['nodes'][nodeIndex]
    if not node:
        return Sequence()
    if node is camera and not cutsceneDict['affectsCamera']:
        return Sequence()

    if not useStartColor:
        startColorScale = None

    if color:
        colorScale = LVecBase4f(*color)
    if startColor:
        startColor = LVecBase4f(*startColor)

    return Sequence(
        Wait(delay),
        LerpColorInterval(
            node, duration=duration, color=color, startColor=startColor, blendType=blendType,
        )
    )


@cutsceneSequence(name='Function: Call', enum=EDE.functionCall)
def seq_functionCall(functionIndex:       SEAT.dropdown_function = 0,
                     delay:               SEAT.slider_min_zero = 0,
                     disable:             SEAT.boolean = True,
                     hasArgument:         SEAT.boolean = False,
                     argumentIndex:       SEAT.dropdown_arguments = 0,
                     returnsInterval:     SEAT.boolean = False,
                     cutsceneDict:        dict = None) -> Sequence:
    # Disabled by default so you don't crash your editor instance by calling functions without the proper functions!
    if disable:
        return Sequence()
    function = cutsceneDict['functions'][functionIndex]
    if not function:
        return Sequence()
    if hasArgument:
        arguments = cutsceneDict['arguments'][argumentIndex]
        if not isinstance(arguments, list):
            arguments = [arguments]
    else:
        arguments = []

    track = Sequence(Wait(delay))

    if returnsInterval:
        track.append(function(*arguments))
    else:
        track.append(Func(function, *arguments))

    return track


@cutsceneSequence(name='Function: Lerp', enum=EDE.functionLerp)
def seq_functionLerp(functionIndex:       SEAT.dropdown_function = 0,
                     delay:               SEAT.slider_min_zero = 0,
                     disable:             SEAT.boolean = True,
                     hasExtraArg:         SEAT.boolean = False,
                     argumentIndex:       SEAT.dropdown_arguments = 0,
                     fromData:            SEAT.slider_float = 0,
                     toData:              SEAT.slider_float = 1,
                     duration:            SEAT.slider_min_zero = 0,
                     blendType:           SEAT.dropdown_blendType = 'easeInOut',
                     cutsceneDict:        dict = None) -> Sequence:
    # Disabled by default so you don't crash your editor instance by calling functions without the proper functions!
    if disable:
        return Sequence()
    function = cutsceneDict['functions'][functionIndex]
    if not function:
        return Sequence()
    if hasExtraArg:
        arguments = cutsceneDict['arguments'][argumentIndex]
        if not isinstance(arguments, list):
            arguments = [arguments]
    else:
        arguments = []

    return Sequence(
        Wait(delay),
        LerpFunc(function, duration=duration, fromData=fromData, toData=toData,
                 blendType=blendType, extraArgs=arguments)
    )


@cutsceneSequence(name='Elevator Close', enum=EDE.closeElev)
def seq_closeElev(elevatorModelIndex: SEAT.dropdown_elevators = 0,
                 cutsceneDict:        dict = None) -> Parallel:
    bem = cutsceneDict['elevators'][elevatorModelIndex]
    retParallel = Parallel(
        ElevatorUtils.getCloseInterval(
            None,
            bem.find("**/left_door"),
            bem.find("**/right_door"),
            None,
            None,
            ElevatorConstants.ELEVATOR_DERRICK_MAN
        )
    )
    return retParallel


@cutsceneSequence(name='Elevator Open', enum=EDE.openElev)
def seq_openElev(elevatorModelIndex: SEAT.dropdown_elevators = 0,
                 cutsceneDict:        dict = None) -> Parallel:
    bem = cutsceneDict['elevators'][elevatorModelIndex]
    retParallel = Parallel(
        ElevatorUtils.getOpenInterval(
            None,
            bem.find("**/left_door"),
            bem.find("**/right_door"),
            None,
            None,
            ElevatorConstants.ELEVATOR_DERRICK_MAN
        )
    )
    return retParallel


@cutsceneSequence(name='Node: Set clear Color Scale', enum=EDE.setClearColorScale)
def seq_setClearColorScale(nodeIndex:    SEAT.dropdown_node = 0,
                           delay:        SEAT.slider_min_zero = 0,
                           setClear:     SEAT.boolean = True,
                           cutsceneDict: dict = None) -> Sequence:
    node = cutsceneDict['nodes'][nodeIndex]
    if not node:
        return Sequence()
    if setClear:
        return Sequence(
            Wait(delay),
            Func(node.setColorScaleOff, 1),
        )
    else:
        return Sequence(
            Wait(delay),
            Func(node.setColorScaleOff, 0),
        )


@cutsceneSequence(name='Create Explosion', enum=EDE.createExplosion)
def seq_createExplosion(nodeIndex: SEAT.dropdown_node = 0,
                        scale: SEAT.slider_min_zero = 1,
                        cutsceneDict: dict = None) -> Sequence:
    parent = cutsceneDict['nodes'][nodeIndex]
    if not parent:
        return Sequence()

    toonPlacerNode = NodePath("toonPlacerNode")
    toonPlacerNode.reparentTo(parent)
    toonPlacerNode.setY(-5)

    toonPos = toonPlacerNode.getPos(render)

    toonPlacerNode.removeNode()

    point = Point3(*toonPos)
    point.setZ(point.getZ() + parent.getHeight() + 1)
    return MovieUtil.createKapowExplosionTrack(render, explosionPoint=point, scale=scale)


@cutsceneSequence(name='Node: Jiggle Vicariously', enum=EDE.jiggleNode)
def seq_jigglejiggleji(nodeIndex:           SEAT.dropdown_node = 0,
                       delay:               SEAT.slider_min_zero = 0.0,
                       duration:            SEAT.slider_min_zero = 1.0,
                       startJig:            SEAT.slider_min_zero = 0.0,
                       endJig:              SEAT.slider_min_zero = 5.0,
                       offset:              SEAT.slider_xyz = (0, 0, 0),
                       blendType:           SEAT.dropdown_blendType = 'easeInOut',
                       cutsceneDict:        dict = None) -> Sequence:
    node = cutsceneDict['nodes'][nodeIndex]
    if not node:
        return Sequence()
    if node is camera and not cutsceneDict['affectsCamera']:
        return Sequence()

    def performJiggle(t: float):
        x, y, z = offset
        delta = lerp(startJig, endJig, t)
        xx = ((random.random() * 2) - 1) * delta
        yy = ((random.random() * 2) - 1) * delta
        zz = ((random.random() * 2) - 1) * delta
        node.setPos(x + xx, y + yy, z + zz)

    return Sequence(
        Wait(delay),
        LerpFunctionInterval(
            function=performJiggle,
            duration=duration,
            blendType=blendType,
        )
    )

