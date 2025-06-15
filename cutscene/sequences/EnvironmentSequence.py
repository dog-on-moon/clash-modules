from direct.showbase import PythonUtil

from toontown.cutscene.editor.CSEditorEnums import EventDefinitionEnum as EDE
from toontown.cutscene.editor.CSEditorEnums import SubEventArgumentType as SEAT
from toontown.cutscene.CutsceneSequenceBase import cutsceneSequence

from direct.interval.IntervalGlobal import *
from panda3d.core import Point3, LVecBase3f, LVecBase4f
from panda3d.core import Fog


fogdefmap = {
    'Exponential':        Fog.MExponential,
    'ExponentialSquared': Fog.MExponentialSquared,
    'Linear':             Fog.MLinear,
}
fogmap = {}


@cutsceneSequence(name='Fog: Create', enum=EDE.createFog)
def seq_createFog(nodeIndex:            SEAT.dropdown_node = 0,
                  fogType:              SEAT.dropdown_fogType = 'Exponential',
                  expDensity:           SEAT.slider_min_zero = 0.5,
                  fogColor:             SEAT.slider_rgb = (1, 1, 1),
                  cutsceneDict:         dict = None) -> Sequence:
    node = cutsceneDict['nodes'][nodeIndex]
    if node is None:
        raise AttributeError("Fog node is bad")
    if fogType == 'Linear':
        raise AttributeError("Linear Fog is not yet supported")

    def makeFog():
        fog = Fog('cutsceneFog')
        fog.setExpDensity(expDensity)
        fog.setColor(*fogColor)
        node.setFog(fog)
        fogmap[node] = fog

    return Sequence(
        Func(node.clearFog),
        Func(makeFog),
    )


@cutsceneSequence(name='Fog: Destroy', enum=EDE.destroyFog)
def seq_destroyFog(nodeIndex:            SEAT.dropdown_node = 0,
                   cutsceneDict:         dict = None) -> Sequence:
    node = cutsceneDict['nodes'][nodeIndex]
    if node is None:
        raise AttributeError("Fog node is bad")
    def clearFog():
        if node in fogmap:
            node.clearFog()
            del fogmap[node]
    return Sequence(Func(clearFog))


@cutsceneSequence(name='Fog: Lerp Color', enum=EDE.setFogColor)
def seq_lerpFogColor(nodeIndex:      SEAT.dropdown_node = 0,
                       delay:        SEAT.slider_min_zero = 0.0,
                       duration:     SEAT.slider_min_zero = 1.0,
                       startColor:   SEAT.slider_rgb = (1, 1, 1),
                       endColor:     SEAT.slider_rgb = (0, 0, 0),
                       blendType:    SEAT.dropdown_blendType = 'noBlend',
                       cutsceneDict: dict = None) -> Sequence:
    node = cutsceneDict['nodes'][nodeIndex]
    if node is None:
        raise AttributeError("Fog node is bad")
    def setColor(t):
        fog = fogmap.get(node)
        if fog is None:
            return
        r1, g1, b1 = startColor
        r2, g2, b2 = endColor
        fog.setColor(
            PythonUtil.lerp(r1, r2, t),
            PythonUtil.lerp(g1, g2, t),
            PythonUtil.lerp(b1, b2, t),
        )
    return Sequence(
        Wait(delay),
        LerpFunctionInterval(
            setColor, duration, blendType=blendType,
        )
    )


@cutsceneSequence(name='Fog: Lerp Density', enum=EDE.setFogDensity)
def seq_lerpFogDensity(nodeIndex:    SEAT.dropdown_node = 0,
                       delay:        SEAT.slider_min_zero = 0.0,
                       duration:     SEAT.slider_min_zero = 1.0,
                       startDensity: SEAT.slider_min_zero = 0.0,
                       endDensity:   SEAT.slider_min_zero = 0.5,
                       blendType:    SEAT.dropdown_blendType = 'noBlend',
                       cutsceneDict: dict = None) -> Sequence:
    node = cutsceneDict['nodes'][nodeIndex]
    if node is None:
        raise AttributeError("Fog node is bad")
    def setDensity(t):
        fog = fogmap.get(node)
        if fog is None:
            return
        fog.setExpDensity(PythonUtil.lerp(startDensity, endDensity, t))
    return Sequence(
        Wait(delay),
        LerpFunctionInterval(
            setDensity, duration, blendType=blendType,
        )
    )


"""
Event onesies
"""


@cutsceneSequence(name='Fog: Lerp Density', enum=EDE.setFogDensity)
def seq_lerpFogDensity(nodeIndex:    SEAT.dropdown_node = 0,
                       delay:        SEAT.slider_min_zero = 0.0,
                       duration:     SEAT.slider_min_zero = 1.0,
                       startDensity: SEAT.slider_min_zero = 0.0,
                       endDensity:   SEAT.slider_min_zero = 0.5,
                       blendType:    SEAT.dropdown_blendType = 'noBlend',
                       cutsceneDict: dict = None) -> Sequence:
    node = cutsceneDict['nodes'][nodeIndex]
    if node is None:
        raise AttributeError("Fog node is bad")
    def setDensity(t):
        fog = fogmap.get(node)
        if fog is None:
            return
        fog.setExpDensity(PythonUtil.lerp(startDensity, endDensity, t))
    return Sequence(
        Wait(delay),
        LerpFunctionInterval(
            setDensity, duration, blendType=blendType,
        )
    )
