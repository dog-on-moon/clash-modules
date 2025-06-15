from toontown.toon.ToonDNA import ToonDNA
from toontown.utils.AstronStruct import AstronStruct

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from toontown.toon.DistributedToon import DistributedToon
    from toontown.toon.DistributedToonAI import DistributedToonAI


class ToonHeadData(AstronStruct):
    """
    Provides information about what makes up a ToonHead to other classes
    (mainly ToonHeadGUI).
    """

    """
    Creators
    """

    @classmethod
    def makeFromToon(cls, toon: 'DistributedToon'):
        dna: ToonDNA = toon.getStyle()
        hr, hg, hb, _ = dna.getHeadColor()
        er, eg, eb, _ = dna.getEarColor()
        return cls(
            dna.head,
            dna.getEyelashes(),
            (hr, hg, hb),
            (er, eg, eb),
            dna.getEyeColor(),
        )

    @classmethod
    def makeFromToonAI(cls, toon: 'DistributedToonAI'):
        dna: ToonDNA = toon.getStyle()
        hr, hg, hb, _ = dna.getHeadColor()
        er, eg, eb, _ = dna.getEarColor()
        return cls(
            dna.head,
            dna.getEyelashes(),
            (hr, hg, hb),
            (er, eg, eb),
            dna.getEyeColor(),
        )

    """
    Astron
    """

    def __init__(self,
                 headInfo: str = 'kls',
                 eyelashIndex: int = 0,
                 headColor: tuple[float, float, float] = (1, 1, 1),
                 earColor: tuple[float, float, float] = (1, 1, 1),
                 eyeColorIndex: int = 0,):
        self.headInfo = headInfo
        self.eyelashIndex = eyelashIndex
        self.headColor = headColor
        self.earColor = earColor
        self.eyeColorIndex = eyeColorIndex

    def __eq__(self, other):
        return self.headInfo == other.headInfo and \
               self.eyelashIndex == other.eyelashIndex and \
               self.headColor == other.headColor and \
               self.earColor == other.earColor and \
               self.eyeColorIndex == other.eyeColorIndex

    def toStruct(self):
        return [
            self.headInfo,
            self.eyelashIndex,
            [round(col * 255) for col in self.headColor],
            [round(col * 255) for col in self.earColor],
            self.eyeColorIndex,
        ]

    @classmethod
    def fromStruct(cls, struct):
        headInfo, eyelashIndex, headColor, earColor, eyeColorIndex = struct
        headColor = [col / 255 for col in headColor]
        earColor = [col / 255 for col in earColor]
        return cls(headInfo, eyelashIndex, headColor, earColor, eyeColorIndex)

    """
    Getters
    """

    def getHeadInfo(self) -> str:
        """
        Returns the three-letter character string
        representing the Toon's head.
        """
        return self.headInfo

    def getEyelashIndex(self) -> int:
        """Returns the index of the eyelashes."""
        return self.eyelashIndex

    def getHeadColor(self) -> tuple[float, float, float]:
        """Returns the head color."""
        return self.headColor

    def getEarColor(self) -> tuple[float, float, float]:
        """Returns the ear color."""
        return self.earColor

    def getEyeColorIndex(self) -> int:
        """Returns the index of the eye color."""
        return self.eyeColorIndex
