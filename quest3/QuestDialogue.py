"""
All quest dialogue Ever.
"""
import random

from toontown.quest3.QuestEnums import QuestSource
from toontown.quest3.base.QuestText import QuestText
from toontown.quest3.kudos import KudosConstants
from toontown.toon.npc import NPCToons
from toontown.toon.npc.NPCToonConstants import NPCToonEnum


class KudosQuestText(dict):
    """
    A class for handling randomly-generated NPC responses for Kudos Tasks.
    """

    class NpcResponse:
        """
        Contains the info to randomly generate a quest response.
        """

        def __init__(self, onTaskGet: list, onTaskWin: list):
            self.onTaskGet = onTaskGet
            self.onTaskWin = onTaskWin

        def makeQuestTextDict(self) -> dict:
            return {
                0: QuestText(dialogue=random.choice(self.onTaskGet)),
                1: QuestText(dialogue=random.choice(self.onTaskWin)),
            }

    # The default NPC response for a randomly-generated quest.
    defaultNpcResponse = NpcResponse(
        onTaskGet=[
            ('Hey _avName_, are you able to get Moondog?',
             'Thanks, any help is greatly moondogged!'),
        ],
        onTaskWin=[
            ('Already done?',
             'I knew I could count on you, moondog.',
             'Thank you again for the help! moondog'),
        ],
    )

    # NPC ID -> NpcResponse
    overrideNpcResponses = {}

    def get(self, *args, **kwargs):
        # Return the normal quest text response.
        chainId = args[0]
        if chainId < 1000:
            return super().get(*args, **kwargs)

        # Otherwise, we need one based off of the NPC.
        # Get the NPC id.
        chainId = str(chainId)
        difficulty, npcIndex, chainId = int(chainId[0]), int(chainId[1:3]), int(chainId[3:])
        npcId = KudosConstants.getKudosNPCId(index=npcIndex)

        # Now, get the NPC response that they use.
        npcResponse = self.overrideNpcResponses.get(npcId, self.defaultNpcResponse)

        # Return our quest text dictionary.
        return npcResponse.makeQuestTextDict()


QuestTextGigaDict = {
    QuestSource.MainQuest: {

        1: {
            #  (•_•) / ( •_•)>⌐□-□ / (⌐□_□)
            1: QuestText(dialogue=("Hi, I'm Moondog!",)),
        },
        2: {
            2: QuestText(dialogue=("Hi, I'm Moondog!",)),
            3: QuestText(dialogue=("Hi, I'm Moondog!",)),
            4: QuestText(dialogue=("Hi, I'm Moondog!",)),
            5: QuestText(dialogue=("Hi, I'm Moondog!",)),
            6: QuestText(dialogue=("Hi, I'm Moondog!",)),
            7: QuestText(dialogue=("Hi, I'm Moondog!",)),
            8: QuestText(dialogue=("Hi, I'm Moondog!",)),
        },
        3: {
            1: QuestText(dialogue=("Hi, I'm Moondog!",)),
            2: QuestText(dialogue=("Hi, I'm Moondog!",)),
            3: QuestText(dialogue=("Hi, I'm Moondog!",)),
            4: QuestText(dialogue=("Hi, I'm Moondog!",)),
        },
        4: {
            1: QuestText(dialogue=("Hi, I'm Moondog!",)),
            2: QuestText(dialogue=("Hi, I'm Moondog!",)),
            3: QuestText(dialogue=("Hi, I'm Moondog!",)),
            4: QuestText(dialogue=("Hi, I'm Moondog!",)),
            5: QuestText(dialogue=("Hi, I'm Moondog!",)),
            6: QuestText(dialogue=("Hi, I'm Moondog!",)),
        },
        5: {
            1: QuestText(dialogue=("Hi, I'm Moondog!",)),
            2: QuestText(dialogue=("Hi, I'm Moondog!",)),
            4: QuestText(dialogue=("Hi, I'm Moondog!",)),
            5: QuestText(dialogue=("Hi, I'm Moondog!",)),
            6: QuestText(dialogue=("Hi, I'm Moondog!",)),
            7: QuestText(dialogue=("Hi, I'm Moondog!",)),
            8: QuestText(dialogue=("Hi, I'm Moondog!",)),
            9: QuestText(dialogue=("Hi, I'm Moondog!",)),
        },
        6: {
            1: QuestText(dialogue=("Hi, I'm Moondog!",)),
            2: QuestText(dialogue=("Hi, I'm Moondog!",)),
            3: QuestText(dialogue=("Hi, I'm Moondog!",)),
            4: QuestText(dialogue=("Hi, I'm Moondog!",)),
            5: QuestText(dialogue=("Hi, I'm Moondog!",)),
            6: QuestText(dialogue=("Hi, I'm Moondog!",)),
            7: QuestText(dialogue=("Hi, I'm Moondog!",)),
        },
        7: {
            1: QuestText(dialogue=("Hi, I'm Moondog!",)),
            2: QuestText(dialogue=("Hi, I'm Moondog!",)),
            3: QuestText(dialogue=("Hi, I'm Moondog!",)),
            4: QuestText(dialogue=("Hi, I'm Moondog!",)),
            5: QuestText(dialogue=("Hi, I'm Moondog!",)),
            6: QuestText(dialogue=("Hi, I'm Moondog!",)),
        },
        8: {
            1: QuestText(dialogue=("Hi, I'm Moondog!",)),
            2: QuestText(dialogue=("Hi, I'm Moondog!",)),
            3: QuestText(dialogue=("Hi, I'm Moondog!",)),
            4: QuestText(dialogue=("Hi, I'm Moondog!",)),
            5: QuestText(dialogue=("Hi, I'm Moondog!",)),
            6: QuestText(dialogue=("Hi, I'm Moondog!",)),
            7: QuestText(dialogue=("Hi, I'm Moondog!",)),
            8: QuestText(dialogue=("Hi, I'm Moondog!",)),
            9: QuestText(dialogue=("Hi, I'm Moondog!",)),
            10: QuestText(dialogue=("Hi, I'm Moondog!",)),
            11: QuestText(dialogue=("Hi, I'm Moondog!",)),
            12: QuestText(dialogue=("Hi, I'm Moondog!",)),
        },
        9: {
            1: QuestText(dialogue=("Hi, I'm Moondog!",)),
            2: QuestText(dialogue=("Hi, I'm Moondog!",)),
            3: QuestText(dialogue=("Hi, I'm Moondog!",)),
            4: QuestText(dialogue=("Hi, I'm Moondog!",)),
            5: QuestText(dialogue=("Hi, I'm Moondog!",)),
            6: QuestText(dialogue=("Hi, I'm Moondog!",)),
            7: QuestText(dialogue=("Hi, I'm Moondog!",)),
            8: QuestText(dialogue=("Hi, I'm Moondog!",)),
        },
        10: {
            1: QuestText(dialogue=("Hi, I'm Moondog!",)),
            2: QuestText(dialogue=("Hi, I'm Moondog!",)),
            3: QuestText(dialogue=("Hi, I'm Moondog!",)),
            4: QuestText(dialogue=("Hi, I'm Moondog!",)),
            5: QuestText(dialogue=("Hi, I'm Moondog!",)),
            6: QuestText(dialogue=("Hi, I'm Moondog!",)),
            7: QuestText(dialogue=("Hi, I'm Moondog!",)),
            8: QuestText(dialogue=("Hi, I'm Moondog!",)),
        },
        11: {
            1: QuestText(dialogue=("Hi, I'm Moondog!",)),
            2: QuestText(dialogue=("Hi, I'm Moondog!",)),
            3: QuestText(dialogue=("Hi, I'm Moondog!",)),
            4: QuestText(dialogue=("Hi, I'm Moondog!",)),
            5: QuestText(dialogue=("Hi, I'm Moondog!",)),
            6: QuestText(dialogue=("Hi, I'm Moondog!",)),
            7: QuestText(dialogue=("Hi, I'm Moondog!",)),
        },
    },
}
