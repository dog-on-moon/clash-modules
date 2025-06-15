from toontown.cutscene.editor.CSEditorEnums import EventDefinitionEnum as EDE
from toontown.cutscene.editor.CSEditorEnums import SubEventArgumentType as SEAT
from toontown.cutscene.CutsceneSequenceBase import cutsceneSequence

from direct.interval.IntervalGlobal import *


@cutsceneSequence(name='Audio: Play SFX', enum=EDE.playSoundEffect)
def seq_playSoundEffect(sfxIndex:        SEAT.dropdown_sound_effects = 0,
                        hasNode:         SEAT.boolean = False,
                        nodeIndex:       SEAT.dropdown_node = 0,
                        loop:            SEAT.boolean = False,
                        hasDuration:     SEAT.boolean = False,
                        duration:        SEAT.slider_min_zero = 0.0,
                        volume:          SEAT.slider_min_zero = 1.0,
                        startTime:       SEAT.slider_min_zero = 0.0,
                        isInterval:      SEAT.boolean = True,
                        cutsceneDict:    dict = None) -> Sequence:
    sfx = cutsceneDict['sounds'][sfxIndex]
    if not sfx:
        return Sequence()

    if not hasNode:
        node = None
    else:
        node = cutsceneDict['nodes'][nodeIndex]
    if not hasDuration:
        duration = 0.0

    if isInterval:
        track = SoundInterval(
            sound=sfx,
            loop=loop,
            duration=duration,
            volume=volume,
            startTime=startTime,
            node=node
        )
    else:
        track = Func(base.playSfx, sfx, loop, 1, volume, startTime, node)
        if hasDuration:
            track = Sequence(
                track,
                Wait(duration),
                Func(sfx.stop)
            )

    return track


@cutsceneSequence(name='Audio: Stop SFX', enum=EDE.stopSoundEffect)
def seq_stopSoundEffect(sfxIndex:        SEAT.dropdown_sound_effects = 0,
                        cutsceneDict:    dict = None) -> Interval:
    sfx = cutsceneDict['sounds'][sfxIndex]
    return Func(sfx.stop)


@cutsceneSequence(name='Audio: Play Music', enum=EDE.playMusic)
def seq_playMusic(musicIndex:      SEAT.dropdown_music = 0,
                  loop:            SEAT.boolean = True,
                  volume:          SEAT.slider_min_zero = 1.0,
                  startTime:       SEAT.slider_min_zero = 0.0,
                  cutsceneDict:    dict = None) -> Interval:
    musicCode = cutsceneDict['music'][musicIndex]
    return Func(base.musicMgr.playMusic, musicCode, looping=loop, volume=volume, time=startTime)


@cutsceneSequence(name='Audio: Stop Music', enum=EDE.stopMusic)
def seq_stopMusic(musicIndex:      SEAT.dropdown_music = 0,
                  cutsceneDict:    dict = None) -> Interval:
    musicCode = cutsceneDict['music'][musicIndex]
    return Func(base.musicMgr.stopMusic, musicCode)
