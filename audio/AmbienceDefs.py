"""
Information defining all features of ambience in Toontown.
"""
from toontown.audio.Ambience import Ambience, FieldAmbience


zoneId2Ambience = {
    # Lovely YOTT bird funnies
    tuple(range(7000, 7400)): Ambience(
        title='YOTTBirdsRavens',
        fileLocation='phase_7/audio/sfx/yott_',
        ambienceNames=('r1', 'r2', 'c1', 'c2', 'rc1', 'rc2'),
        volume=0.65, durationBetween=(6, 16)
    ),
    # Rainmake ambience
    'rainmaker_rain': FieldAmbience(
        title='RainmakerRain',
        fileLocation='phase_11/audio/bgm/merc/amb_rainmaker_rain',
        volume=0.30,
        fadeInTime=5.0,
        fadeOutTime=5.0,
    ),
    'rainmaker_oil': FieldAmbience(
        title='RainmakerOil',
        fileLocation='phase_11/audio/bgm/merc/amb_rainmaker_oil',
        volume=0.35,
        fadeInTime=5.0,
        fadeOutTime=5.0,
    ),
    'rainmaker_fog': FieldAmbience(
        title='rainmaker_fog',
        fileLocation='phase_11/audio/bgm/merc/amb_rainmaker_fog',
        volume=0.25,
        fadeInTime=5.0,
        fadeOutTime=5.0,
    ),
    'rainmaker_heavyrain': FieldAmbience(
        title='RainmakerHeavyRain',
        fileLocation='phase_11/audio/bgm/merc/amb_rainmaker_oil',
        volume=0.70,
        fadeInTime=5.0,
        fadeOutTime=5.0,
    ),
    'rainmaker_storm': FieldAmbience(
        title='RainmakerStorm',
        fileLocation='phase_11/audio/bgm/merc/amb_rainmaker_rain',
        volume=0.50,
        fadeInTime=5.0,
        fadeOutTime=5.0,
    ),
    # Can also define regular strings in here.
    # ToontownAudio will accept 'ambienceKeyStart' and 'ambienceKeyEnd'
    # 'example': Ambience()
}


def getAmbience(zoneId):
    """Returns a proper Ambience class given a zoneId, if it exists."""
    for zoneIdTuple in zoneId2Ambience.keys():
        if type(zoneIdTuple) not in (tuple, list):
            # it's not a tuple, compare directly.
            if zoneId == zoneIdTuple:
                return zoneId2Ambience[zoneIdTuple]
        else:
            # it is a tuple, see if the zoneId is in there.
            if zoneId in zoneIdTuple:
                return zoneId2Ambience[zoneIdTuple]
    # doesn't exist? just go home
    return None


def getAllZoneAmbience() -> list:
    """Returns a list of all zoneId-based ambience."""
    retlist = []
    for zoneIdTuple in zoneId2Ambience.keys():
        if type(zoneIdTuple) not in (tuple, list):
            # it's not a tuple, check its type.
            if type(zoneIdTuple) not in (str,):
                retlist.append(zoneId2Ambience[zoneIdTuple])
        else:
            # it is a tuple, see if the zoneId is in there.
            for value in zoneIdTuple:
                if type(value) not in (str,):
                    retlist.append(zoneId2Ambience[zoneIdTuple])
                    break
    return retlist


zoneAmbienceList = getAllZoneAmbience()
