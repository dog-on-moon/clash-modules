"""
A utils file with several functions dedicated
for dealing with Panda3D's color funnies.
"""
from direct.showbase.PythonUtil import lerp
import colorsys

"""
Number Constants
"""

c_black = (0, 0, 0, 1)
c_white = (1, 1, 1, 1)
c_empty = (0, 0, 0, 0)


"""
Number Operations
"""


def lerpColor(a: tuple, b: tuple, t: float = 0.50) -> tuple:
    color = []
    for valA, valB in zip(a, b):
        color.append(lerp(valA, valB, t))
    return tuple(color)


def lerpPColSmart(a: tuple, b: tuple, t: float = 0.50) -> tuple:
    return hsvToPCol(
        *lerpColor(
            pcolToHsv(a),
            pcolToHsv(b),
            t,
        )
    )


def dimColor(col: tuple, t: float = 0.0) -> tuple:
    return lerpColor(col, (0, 0, 0, col[3]), t)


def undimColor(col: tuple, t: float = 0.0) -> tuple:
    return lerpColor(col, (1, 1, 1, col[3]), t)


"""
RGB Conversion Methods
"""


def rgbToPCol(r: int, g: int, b: int, a: int = 255) -> tuple:
    """
    Converts a 0-255 RGBA value to a Panda3D 0-1 value.
    :param r: Red 0-255
    :param g: Green 0-255
    :param b: Blue 0-255
    :param a: (optional) Alpha 0-255
    :return: Tuple, with Panda3D rgba values
    """
    return r / 255, g / 255, b / 255, a / 255


def hexToPCol(hexString: str, a: int = 255) -> tuple:
    """
    Converts a hex string into a Panda3D 0-1 value.
    :param hexString: A 6-character hex string.
    :return: Tuple, with Panda3D rgba values
    """
    hexString = hexString.replace("#", "")
    assert len(hexString) == 6
    assert all(letter in "0123456789ABCDEFabcdef" for letter in hexString)
    return tuple([int(hexString[i:i+2], 16) / 255 for i in (0, 2, 4)] + [a / 255])


def hexToRGB(hexString: str, a: int = 255) -> tuple:
    """
    Converts a hex string into 0 to 255 RGB.
    :param hexString: A 6-character hex string.
    :return: Tuple, with Panda3D rgba values
    """
    hexString = hexString.replace("#", "")
    assert len(hexString) == 6
    assert all(letter in "0123456789ABCDEFabcdef" for letter in hexString)
    return tuple([int(hexString[i:i+2], 16) for i in (0, 2, 4)] + [a])


def hexToHSV(hexString: str, a: int = 255) -> tuple:
    r, g, b, _ = hexToRGB(hexString)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return h, s, v, a / 255


def rgbToHex(r: int, g: int, b: int) -> str:
    """
    Converts 0-255 RGB into a hex string.
    """
    return "{:02x}{:02x}{:02x}".format(r, g, b)


"""
HSV Conversion Methods
"""


def hsvToPCol(hue: float, sat: float, val: float, a: int = 255):
    rgb = colorsys.hsv_to_rgb(hue, sat, val)
    return rgbToPCol(*tuple(map(lambda x: round(x * 255), rgb)), a=a)


def pcolToHsv(pcol: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    r, g, b, a = pcol
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return h, s, v, a * 255


"""
Useful class transformers
"""


def dict_hexToRGB(d: dict, a: int = 255):
    """
    Converts the keys within a passed dictionary
    into RGB format.
    """
    return {hexToRGB(key, a=a): value for key, value in d.items()}


"""
Random color generation
"""
import random


def randomNormalizedColor(a = 1.0):
    return random.random(), random.random(), random.random(), a
