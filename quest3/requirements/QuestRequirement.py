from toontown.quest3.base.Quester import Quester


class QuestRequirement:
    """
    A list of these are passed in as an argument to a QuestPart init.
    Each of these have a unique isMet function
    that checks an aspect of the Toon to see if they are allowed to take the quest.
    """

    def check(self, quester: Quester):
        """
        :param quester: Takes Quester, does some checks.
        :return: Returns True if requirement is met.
        """
        return True
