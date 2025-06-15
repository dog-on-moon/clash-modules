"""
Module for QuestText container class.
"""


class QuestText:
    """
    A container class for all quest-related text.
    """

    def __init__(self, dialogue=''):
        if type(dialogue) not in (tuple, list):
            dialogue = (dialogue,)
        self.dialogue = dialogue

    def getDialogue(self):
        return self.dialogue
