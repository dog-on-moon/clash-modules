from toontown.utils.AstronStruct import AstronStruct
from typing import Tuple
from uuid import UUID, uuid4


class AstronUUID(UUID, AstronStruct):
    """
    A class for a Universally Unique IDentifier that can be
    used Responsibly through the medium of Astron.

    We subdivide into quarters to ensure that the UUID
    is safe for Mongo, as Mongo only supports up to 8-byte INTS
    ( while splitting in halves can create 8-byte uints ... )
    """

    QUARTER_BITMASK = (2 ** 32) - 1

    def __hash__(self) -> int:
        return self.int

    def __eq__(self, other) -> bool:
        if not isinstance(other, AstronUUID):
            return False
        return self.int == other.int

    def toStruct(self) -> list:
        return list(self.UUIDtoInts())

    @classmethod
    def fromStruct(cls, struct) -> 'AstronUUID':
        return cls.intsToUUID(*struct)

    def toMongo(self) -> dict:
        return {
            'i': self.UUIDtoInts()
        }

    @classmethod
    def fromMongo(cls, json) -> 'AstronUUID':
        return cls.intsToUUID(*json['i'])

    @classmethod
    def uuid4(cls) -> 'AstronUUID':
        return cls(int=uuid4().int)

    """
    UUID conversion
    """

    def UUIDtoInts(self) -> Tuple[int, int, int, int]:
        bigInt = self.int
        intA = int((bigInt >> 96) & AstronUUID.QUARTER_BITMASK)
        intB = int((bigInt >> 64) & AstronUUID.QUARTER_BITMASK)
        intC = int((bigInt >> 32) & AstronUUID.QUARTER_BITMASK)
        intD = int(bigInt         & AstronUUID.QUARTER_BITMASK)
        return intA, intB, intC, intD

    @classmethod
    def intsToUUID(cls, intA, intB, intC, intD) -> 'AstronUUID':
        return cls(int=int(intA << 96)
                     + int(intB << 64)
                     + int(intC << 32)
                     + int(intD))
