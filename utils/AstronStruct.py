"""
Similar to AstronStruct, but without annotations and dataclasses,
since it seems like they make the game very unhappy to build.
"""


class AstronStruct:

    def toStruct(self):
        """
        Converts this dataclass into an Astron struct.
        
        :rtype list:
        """
        raise NotImplementedError

    def toDict(self):
        """
        Converts this dataclass into a standard Python dictionary.
        """
        if self.__slots__:
            return {s: getattr(self, s, None) for s in self.__slots__ if hasattr(self, s)}

        return {
            k: v if not isinstance(v, AstronStruct) else v.toDict()
            for k, v in self.__dict__.items()
            if not (k.startswith('__') or k.endswith('__'))
        }

    @classmethod
    def fromStruct(cls, struct):
        """
        Converts a struct into an AstronStruct subclass.

        :param struct: list
        """
        if struct:
            return cls(*struct)
        else:
            return cls()

    @classmethod
    def fromStructList(cls, struct):
        """Turns a list containing structs into a class of specifically this struct.
        
        :param struct: list
        """
        return [cls.fromStruct(substruct) for substruct in struct]

    @staticmethod
    def toStructList(astronStructs):
        """Turns a list of astronStructs into a list of just their structs.
        
        :param astronStructs: list
        """
        return [astronStruct.toStruct() for astronStruct in astronStructs]

    def copy(self):
        return self.fromStruct(self.toStruct())
