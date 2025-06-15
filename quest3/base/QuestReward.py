"""
The module class for the QuestReward base.
"""
from toontown.quest3.base.Quester import Quester


class QuestReward:
    """
    The base class for a QuestReward.
    """

    def handleReward(self, quester: Quester, multiplier: float = 1.0) -> None:
        """
        Rewards the Quester with this QuestReward class.
        :param quester:     The Quester object.
        :param multiplier:  A multiplier on the reward amount, for partial rewards.
        :return:            None.
        """
        raise NotImplementedError

    def getRewardString(self, multiplier: float = 1.0) -> list:
        """
        Return a string describing the reward obtained. Returns a list of strings.
        :param multiplier:  A multiplier on the reward amount, for partial rewards.
        :return:            None.
        """
        raise NotImplementedError

    def attemptCombine(self, other, selfMultiplier: float = 1.0, otherMultiplier: float = 1.0):
        """
        Attempts to 'combine' this reward with another of the same type.
        If it doesn't make for the rewards to combine, return False.
        Otherwise, return a new reward of the same type.
        """
        return False
