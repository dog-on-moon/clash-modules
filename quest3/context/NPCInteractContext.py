"""
Module for NPC interaction contexts
"""
from toontown.quest3.base.QuestContext import QuestContext
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from toontown.toon.DistributedNPCToonAI import DistributedNPCToonAI
    from toontown.toon.DistributedToonAI import DistributedToonAI


class NPCInteractContext(QuestContext):

    def __init__(self, npc, av):
        """
        :type npc: DistributedNPCToonAI
        :type av: DistributedToonAI
        """
        self.npc = npc # type: DistributedNPCToonAI
        self.av = av # type: DistributedToonAI

    def getNpcId(self):
        return self.npc.getNpcId()
