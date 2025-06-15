"""
A RNG-generator class for Quests.
"""
import math
import random
from random import Random

from direct.showbase.PythonUtil import lerp, bound

from toontown.quest3.QuestEnums import QuesterType, QuestSource
from toontown.quest3.base.QuestObjective import MultiObjective, QuestObjective


class QuestGenerator:
    """
    A base class for randomly generating MultiObjectives.
    Must be initialized with a Random object, can be seeded.
    """

    def __init__(self, seed: int):
        self.seed = seed

    def makeRandom(self, offset: int = 0) -> Random:
        return random.Random(x=self.seed + offset)

    def generateTask(self, questerType: QuesterType, difficulty: float, questSource: QuestSource, multiObjectiveCls=MultiObjective, forcedObjectiveCount: int = None, **extraArgs) -> MultiObjective:
        """
        Given a "difficulty" float, return a MultiObjective.

        The "difficulty" is a rough estimate of linear growth for task difficulty.
        1.0 is what you'd expect out of TTC, where 2.0 has task difficulties of around "two times TTC," etc etc

        :param questerType: The type of quester getting this task.
        :param difficulty:  The arbitrary difficulty input.
        :param questSource: The quest source to use.
        :param multiObjectiveCls: The class to use as the multi objective.
        :param forcedObjectiveCount: How many objectives there should be?
        :return: A MultiObjective.
        """
        # First, get our real difficulty and objective count.
        if forcedObjectiveCount is None:
            newDifficulty, objectiveCount = self._getDifficultyAndObjectiveCount(difficulty=difficulty)
        else:
            newDifficulty, objectiveCount = difficulty, forcedObjectiveCount
        potentialObjectives = self._getPotentialQuestObjectives(questerType=questerType, difficulty=difficulty, questSource=questSource, **extraArgs)

        # Re-roll if we don't have a lot of potential objectives.
        if objectiveCount > len(potentialObjectives):
            newDifficulty = difficulty
            objectiveCount = 1
            potentialObjectives = self._getPotentialQuestObjectives(questerType=questerType, difficulty=difficulty, questSource=questSource, **extraArgs)

        # Now, make our objectives.
        objectives = []
        for _ in range(objectiveCount):
            potentialClasses = []
            for cls, weight in potentialObjectives.items():
                potentialClasses.extend([cls] * weight)
            index = round(self.makeRandom().random() * (len(potentialClasses) - 1))
            objClass = potentialClasses.pop(index)
            potentialObjectives.pop(objClass)
            objectives.append(
                objClass.generateFromDifficulty(
                    rng=self.makeRandom(offset=int(41737 * self.seed**1.9 - 422 + (self.seed/3 + 41))),
                    difficulty=newDifficulty,
                    questSource=questSource,
                    **extraArgs
                )
            )

        # Return a MultiObjective based off these objectives.
        return multiObjectiveCls(*objectives)

    def _getDifficultyAndObjectiveCount(self, difficulty: float) -> tuple:
        """
        Given an arbitrary difficulty value, parse it into how many
        objectives we should calculate, along with a nerfed difficulty
        value in the case there are multiple quests.

        :param difficulty: An arbitrary difficulty value.
        :return: New difficulty value and objective count.
        """
        # A list of chances to roll for objective count.
        chances = [1, 0, 0]
        objectiveCount = 0

        # Buff the chances depending on our difficulty.
        chances[1] = lerp(0, 0.4, bound(((difficulty - 6) / 50), 0, 1))
        chances[2] = lerp(0, 0.25, bound(((difficulty - 25) / 80), 0, 1))

        # Roll a chance per value in the list.
        for chance in chances:
            if self.makeRandom().random() <= chance:
                objectiveCount += 1

        # Nerf the difficulty by objective count.
        difficulty *= {
            1: 1.0,
            2: 0.8,
            3: 0.65,
        }.get(objectiveCount)

        # Return our result.
        return difficulty, objectiveCount

    @staticmethod
    def _getPotentialQuestObjectives(questerType: QuesterType, difficulty: float, questSource: QuestSource, **extraArgs) -> dict:
        """
        Returns a list of QuestObjective classes that can be randomized.

        :param difficulty: The arbitrary difficulty value.
        :return: Classes of QuestObjectives, weighted as a dict.
        """
        retDict = {}
        for objClass in QuestObjective.objectiveClasses:
            # Get the difficulty range.
            diffRange = objClass.getDifficultyRange(questerType=questerType, questSource=questSource, **extraArgs)

            # If defined as single none, objective cannot be used.
            if diffRange is None:
                continue

            # Get the range.
            diffMin, diffMax = diffRange

            # Parse the range, if any of them are Nones.
            if diffMin is None:
                diffMin = difficulty
            if diffMax is None:
                diffMax = difficulty

            # Do the calculation.
            if diffMin <= difficulty <= diffMax:
                retDict[objClass] = objClass.getObjectiveWeight(questerType=questerType)

        # Return our result.
        return retDict


if __name__ == '__main__':
    # Initialize objectives that can be randomized
    from toontown.quest3.objectives import *
    from collections import defaultdict
    DefeatCogObjective()
    CatchingGameObjective()
    DefeatFacilityObjective()
    BuildingObjective()
    JungleGameObjective()

    for _ in range(100):
        questGen = QuestGenerator(seed=2)
        multiObjective = questGen.generateTask(questerType=QuesterType.Club, difficulty=111.42457745237617)
        print(repr(multiObjective))

    #
    # difficultyDict = defaultdict(list)
    # print("Difficulty Range Rules:")
    # for i in list(range(1, 51, 1)):
    #     print(f"Club with {i} People:")
    #     easy   = round(1.0 + ((math.ceil(i * 1.0) + 0) ** 1.06), 3)
    #     medium = round(1.0 + ((math.ceil(i * 1.2) + 1) ** 1.06), 3)
    #     tough  = round(1.0 + ((math.ceil(i * 1.4) + 2) ** 1.06), 3)
    #     speedrun = round(1.0 + ((math.ceil(i * 0.3) + 2) ** 1.06), 3)
    #     print(f"\tEasy: {easy}")
    #     print(f"\tMedium: {medium}")
    #     print(f"\tHard: {tough}")
    #     print(f"\tSpeedrun: {speedrun}")
    #
    #     # Add to difficulty dict
    #     difficultyDict[round(easy)].append((i, 0))
    #     difficultyDict[round(medium)].append((i, 1))
    #     difficultyDict[round(tough)].append((i, 2))
    #     difficultyDict[round(speedrun)].append((i, 3))
    # print()
    #
    # # OK, we're going to go ahead and simulate the quest generator a lot
    # for i in range(200):
    #     if difficultyDict.get(i + 1):
    #         randomObj = random.Random()
    #         randomObj.seed(i)
    #         questGen = QuestGenerator(rngObj=randomObj)
    #         multiObjective = questGen.generateTask(questerType=QuesterType.Club,
    #                                                difficulty=i + 1,)
    #         print(f'Difficulty {i + 1} : {multiObjective}')
    #
    #         print(f'This can be found at club tasks:')
    #         for count, difficulty in difficultyDict.get(i + 1, []):
    #             if difficulty == 0:
    #                 print(f'Easy task for {count}')
    #             elif difficulty == 1:
    #                 print(f'Medium task for {count}')
    #             elif difficulty == 2:
    #                 print(f'Hard task for {count}')
    #             elif difficulty == 3:
    #                 print(f'Speedrun task for {count}')
    #         print()
