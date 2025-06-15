from toontown.utils.AstronStruct import AstronStruct
import json


class AstronList(list, AstronStruct):
    """
    An AstronList. All inside elements can be communicated across Astron.
    All of the keys in any nested dict must be strings.
    """

    def __hash__(self):
        return hash(self.toStruct()[0])

    def toStruct(self):
        return [json.dumps(self)]

    @classmethod
    def fromStruct(cls, struct):
        return cls(json.loads(struct[0]))

    @classmethod
    def fromList(cls, l: list):
        return cls(l)


if __name__ == '__main__':
    exampleList = [
        1.0,
        'testing',
        -0.123,
        3984734987234,
        [
            'milk',
            9
        ],
        [
            'gaming',
            10,
        ],
        {
            'gaming': 310,
            '3': 10,
            '18': [123, 56, 999, {'3': 10}],
        },
    ]
    print(f'exampleList:\n{exampleList}\n')
    astronList = AstronList.fromList(exampleList)
    structList = astronList.toStruct()
    print(f'Struct:\n{structList}\n')
    originalList = AstronList.fromStruct(structList)
    print(f'Reconverted:\n{originalList}\n')
    print(f'Success:\n{list(astronList) == list(originalList)}')
