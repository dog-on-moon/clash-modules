from toontown.utils.AstronUUID import AstronUUID


class ItemID(AstronUUID):
    """
    A unique identifier for a given item.
    """

    def __repr__(self):
        return f'ItemID({self.int % 10000})'  # short ID for readability

    @classmethod
    def makeUniqueId(cls) -> 'ItemID':
        """
        Creates a unique ItemID class
        """
        return cls.uuid4()
