import random
import math

from direct.gui.DirectFrame import DirectFrame
from direct.showbase.PythonUtil import lerp

from direct.gui import DirectGuiGlobals as DGG

from toontown.cutscene.editor.CSEditorEnums import EventDefinitionEnum as EDE
from toontown.cutscene.editor.CSEditorEnums import SubEventArgumentType as SEAT
from toontown.cutscene.CutsceneSequenceBase import cutsceneSequence
from direct.interval.IntervalGlobal import *


@cutsceneSequence(name='Screen: Fade Color', enum=EDE.doScreenFade)
def seq_fadeColor(delay:            SEAT.slider_min_zero = 0,
                  color:            SEAT.slider_rgb = (0, 0, 0),
                  fadeInDuration:   SEAT.slider_min_zero = 1.0,
                  fadeInBlendType:  SEAT.dropdown_blendType = 'noBlend',
                  holdDuration:     SEAT.slider_min_zero = 1.0,
                  fadeOutDuration:  SEAT.slider_min_zero = 1.0,
                  fadeOutBlendType: SEAT.dropdown_blendType = 'noBlend',
                  cutsceneDict:     dict = None) -> Sequence:
    screenGui = DirectFrame(
        parent=render2d, relief=DGG.FLAT,
        frameSize=(-1, 1, -1, 1),
        frameColor=(0, 0, 0, 0),
    )
    r, g, b = color

    def lerpScreenColor(t):
        if screenGui:
            screenGui['frameColor'] = (r, g, b, t)

    def cleanup():
        if screenGui:
            screenGui.destroy()

    return Sequence(
        Wait(delay),
        LerpFunctionInterval(function=lerpScreenColor, duration=fadeInDuration,
                             fromData=0, toData=1, blendType=fadeInBlendType),
        Func(lerpScreenColor, 1.0),
        Wait(holdDuration),
        LerpFunctionInterval(function=lerpScreenColor, duration=fadeOutDuration,
                             fromData=1, toData=0, blendType=fadeOutBlendType),
        Func(cleanup),
    )


@cutsceneSequence(name='Node: Basic Label', enum=EDE.basicLabel)
def seq_basicLabel(nodeIndex:    SEAT.dropdown_node = 0,
                   useRender2d:  SEAT.boolean = False,
                   messageIndex: SEAT.dropdown_messages = 0,
                   delay:        SEAT.slider_min_zero = 0.0,
                   duration:     SEAT.slider_min_zero = 1.2,

                   # Positioning
                   pos: SEAT.slider_xyz = (0, 0, 0),
                   hpr: SEAT.slider_hpr = (0, 0, 0),
                   scale: SEAT.slider_min_zero = 1.0,
                   cutsceneDict: dict = None, **kwargs) -> Sequence:
    node = cutsceneDict['nodes'][nodeIndex]
    if node in (hidden, camera):
        return Sequence()
    message = cutsceneDict['messages'][messageIndex]

    guiPos = pos
    guiHpr = hpr

    from toontown.gui.ScaledFrame import ScaledFrame
    label = ScaledFrame(
        parent=node if not useRender2d else render2d,
        pos=tuple(guiPos), hpr=tuple(guiHpr), scale=scale,
        text=message, # frameColor=(1, 1, 1, 0),
        text_fg=(1, 1, 1, 0),
        scaledTexture='phase_3/maps/gui/ttcc_gui_scaledFrame_shadow.png',
        borderScale=0.3,
    )
    label2 = DirectFrame(
        parent=label, relief=None,
        pos=(0, -0.05, 0),
        text=message, frameColor=(1, 1, 1, 0),
        text_fg=(1, 1, 1, 1),
    )
    label.hide()
    label.setBin('fixed', 5000)
    for c in range(label['numStates']):
        label2.component(f'text{c}').setDecal(1)
        label2.component(f'text{c}').setTransparency(TransparencyAttrib.M_multisample, 1)

    dl, ur = label.component(f'text0').getTightBounds()
    left, _, down = dl
    right, _, up = ur
    label['frameSize'] = tuple(map(lambda x: (x * 0.9) / scale, (left * 1.12, right * 1.12, down, up)))

    def doShow():
        if label:
            label.show()

    enterSequence = Parallel()
    enterSequence.append(Func(doShow))
    enterSequence.append(Wait(duration))

    def cleanup():
        if label:
            label['text'] = ''
            label.setColorScale(1, 1, 1, 0)
            label.destroy()

    return Sequence(
        Wait(delay),
        enterSequence,
        Func(cleanup),
    )
