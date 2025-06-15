from toontown.utils.AstronStruct import AstronStruct
import json


class AstronDict(dict, AstronStruct):
    """
    An AstronDict. All inside elements can be communicated across Astron.
    All of the keys in any nested dict must be strings.
    """

    def __hash__(self):
        return hash(self.toStruct()[0])

    def toStruct(self):
        return [json.dumps(self)]

    @classmethod
    def fromStruct(cls, struct):
        return cls(json.loads(struct[0]))

    def toMongo(self) -> dict:
        return dict(self)

    @classmethod
    def fromMongo(cls, json) -> 'AstronDict':
        return cls.fromDict(json)

    @classmethod
    def fromDict(cls, d: dict):
        return cls(d)
    
    def copy(self):
        return self.fromDict(dict(self))


if __name__ == '__main__':
    exampleDict = {
        'alphabet': 'abcdefghijklmnopqrstuvwxyz',
        'integer': 1,
        'other': -48149,
        'numbers': [
            1, 2, 3, {'5': {'6': {'7': [8, 2, [5]]}}}
        ],
    }
    print(f'ExampleDict:\n{exampleDict}\n')
    astronDict = AstronDict.fromDict(exampleDict)
    structDict = astronDict.toStruct()
    print(f'Struct:\n{structDict}\n')
    originalDict = AstronDict.fromStruct(structDict)
    print(f'Reconverted:\n{originalDict}\n')
    print(f'Success:\n{dict(exampleDict) == dict(originalDict)}')
