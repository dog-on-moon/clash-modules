from toontown.cutscene.editor.CSEditorEnums import EventDefinitionEnum as EDE
from toontown.cutscene.editor.CSEditorEnums import SubEventArgumentType as SEAT
from toontown.cutscene.CutsceneSequenceBase import cutsceneSequence

from direct.interval.IntervalGlobal import *
from panda3d.core import Point3, LVecBase3f, LVecBase4f


@cutsceneSequence(name='Expression: Set', enum=EDE.setToonExpression)
def seq_setToonExpression(toonIndex:       SEAT.dropdown_toons = 0,
                          toonExpression:  SEAT.dropdown_toonExpression = 'normal',
                          cutsceneDict:    dict = None) -> Sequence:
    toon = cutsceneDict['toons'][toonIndex]
    if not toon:
        return Sequence()

    def setMuzzle():
        toon.hideAllMuzzles()
        {
            'normal': toon.showNormalMuzzle,
            'angry': toon.showAngryMuzzle,
            'sad': toon.showSadMuzzle,
            'smile': toon.showSmileMuzzle,
            'laugh': toon.showLaughMuzzle,
            'surprise': toon.showSurpriseMuzzle,
        }.get(toonExpression)()

    return Sequence(Func(setMuzzle))


@cutsceneSequence(name='Species: Set', enum=EDE.setToonSpecies)
def seq_setToonSpecies(toonIndex:    SEAT.dropdown_toons = 0,
                       toonSpecies:  SEAT.dropdown_toonSpecies = 'v',
                       active:       SEAT.boolean = False,
                       cutsceneDict: dict = None) -> Sequence:
    toon = cutsceneDict['toons'][toonIndex]
    if not toon:
        return Sequence()

    def updateSpecies():
        if not active:
            return
        toon.style.head = f'{toonSpecies}{toon.style.head[1:]}'
        toon.updateToonDNA(toon.style, fForce=1)
        toon.setBlend(frameBlend=base.wantSmoothAnims)
        toon.setLODAnimation(base.lodMaxRange, base.lodMinRange, base.lodDelayFactor)
        toon.initializeDropShadow()
        toon.stopLookAround()
        toon.loop('neutral')

    return Sequence(Func(updateSpecies))


@cutsceneSequence(name='Eyes: Set', enum=EDE.setToonEyes)
def seq_setToonEyes(toonIndex:       SEAT.dropdown_toons = 0,
                    toonEyes:  SEAT.dropdown_toonEyes = 'normal',
                    cutsceneDict:    dict = None) -> Sequence:
    toon = cutsceneDict['toons'][toonIndex]
    if not toon:
        return Sequence()

    def setMuzzle():
        if toonEyes == 'normal':
            toon.normalEyes()
            toon.openEyes()
            toon.startBlink(instant=True)
            return

        toon.stopBlink()
        toon.blinkEyes()
        {
            'angry': toon.angryEyes,
            'sad': toon.sadEyes,
            'surprise': toon.surpriseEyes,
        }.get(toonEyes)()

    return Sequence(Func(setMuzzle))
