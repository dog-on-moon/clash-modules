"""
Globals file for game audio.
"""


def getAdjustedMusicVolume():
    """
    Calculates the game's true music volume,
    accounting for Panda3D's lack of transposing linear volume.
    """
    return settings['musicVol'] ** 2


def getAdjustedSfxVolume():
    """
    Calculates the game's true sfx volume,
    accounting for Panda3D's lack of transposing linear volume.
    """
    return settings['sfxVol'] ** 2
