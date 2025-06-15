"""
This module defines the base class for a QuestLine.
"""
from typing import TYPE_CHECKING

from toontown.quest3.base.QuestExceptions import QuestDereferenceException
from toontown.quest3.base.QuestObjective import QuestObjective, END, MultiObjective
from toontown.quest3.base.QuestReference import QuestReference, QuestId
from toontown.quest3.base.QuestReward import QuestReward
from toontown.quest3.base.Quester import Quester
from toontown.quest3.QuestEnums import QuestSource
from toontown.quest3.requirements.QuestRequirement import QuestRequirement


if TYPE_CHECKING:
    from toontown.quest3.base.QuestChain import QuestChain


class QuestLine:
    """
    The base class for the QuestLine.
    """

    __slots__ = ('questLine',)

    # Define a QuestSource here.
    questSource = None

    # A reference to all QuestLine objects, based on questSource.
    questLines = {}

    def __init__(self, questLine) -> None:
        """
        :param questLine: "Dict[int, QuestChain]"
        """
        # Set our local questLine dictionary.
        self.questLine = questLine

        # Define the questLine variable with our QuestLine object.
        assert self.questSource not in self.questLines, "QuestSource defined with multiple QuestLines"
        self.questLines[self.questSource] = self

    """
    Quest Line Accessors
    """

    def getValidQuestChains(self, quester: Quester):
        """Get every quest chain that the indicated quester can access.

        :rtype: List[Tuple[int, QuestChain]]
        """
        return [(chainId, chain) for chainId, chain in self.questLine.items() if chain.validate(quester)]
    
    @classmethod
    def filterQuestChains(cls, questSource: QuestSource,
                          rewardCls: QuestReward = None, 
                          requirementCls: QuestRequirement = None):
        """Generates a filtered list of QuestChains based on the
        parameters given.

        :rtype: List[Tuple[int, QuestChain]]
        """
        # Find the questSource in the questLines dictionary.
        questLine: QuestLine = cls.questLines.get(questSource)

        # The questline for this quest source is currently not implemented.
        if not questLine:
            return []

        chains = []

        for chainId, chain in questLine.questLine.items():
            # Filter based on reward class specified.
            if None not in (rewardCls, chain.rewards) and \
                not any([isinstance(reward, rewardCls) for reward in chain.rewards]):
                continue
            # Filter based on requirement class specified.
            elif None not in (requirementCls, chain.required) and \
                not any([isinstance(req, requirementCls) for req in chain.required]):
                continue
            
            # All checks have been passed, add the chain.
            chains.append((chainId, chain))
        
        return chains

    @classmethod
    def getQuestChainFromId(cls, questSource: QuestSource, chainId: int, quester: Quester):
        """
        Gets a QuestChain by id.

        :param questSource: The QuestSource associated with the chian.
        :param chainId:     The ID of the QuestChain.
        :param quester:     The quester.
        :return:            The QuestChain.
        :rtype:             QuestChain
        """
        # Find the questSource in the questLines dictionary.
        assert questSource in cls.questLines, "QuestSource has undefined questLine object."
        questLine: QuestLine = cls.questLines.get(questSource)

        # Locate the chainId in this questLine's dictionary.
        questChain = questLine.getQuestChainFromChainId(questSource, chainId, quester)

        return questChain

    @classmethod
    def getQuestChainFromQuestId(cls, questId: QuestId, quester: Quester):
        """
        Returns a QuestChain from a QuestId.
        :param questId: The QuestId associated with the chain.
        :param quester: The Quester.
        :return:        The QuestChain.
        :rtype:         QuestChain
        """
        questSource, chainId, objectiveId, subObjectiveId = questId.toStruct()
        return cls.getQuestChainFromId(questSource=questSource, chainId=chainId, quester=quester)

    @classmethod
    def dereferenceQuestReference(cls, questReference: QuestReference, quester: Quester = None) -> MultiObjective:
        """
        'Dereferences' a QuestReference, granting access to the objectives
        associated with the targetted questReference.

        :param questReference: A questReference object. Points to the questDef.
        :param quester:        Some Quester. Usually not needed, except in edge cases.
        :param wantAll:        Get the list of quest references, and not the specific one.
        """
        try:
            return cls.getQuestObjectiveFromId(questReference.getQuestId(), quester=quester)
        except AttributeError as e:
            print(f'(Subexception: {e})')
            raise QuestDereferenceException(f"Failed to dereference QuestRef with ID {repr(questReference.getQuestId())}")

    @classmethod
    def getQuestObjectiveFromId(cls, questId: QuestId, quester: Quester) -> MultiObjective:
        """
        Returns a questObjective from a given questId.
        :param questId: The questId to hunt for.
        :param quester: Some Quester.
        """
        questSource, chainId, objectiveId, subObjectiveId = questId.toStruct()

        # Get the questChain.
        questChain = cls.getQuestChainFromQuestId(questId=questId, quester=quester)

        # Return the questObjectives from this QuestChain.
        questObjectives: MultiObjective = questChain.getQuestObjectivesAtId(objectiveId)
        return questObjectives

    @classmethod
    def getNextQuestId(cls, questId: QuestId, quester: Quester, objectiveIndexCompleted: int = 0):
        """
        Given a QuestId, returns the next QuestId associated with it.
        :param questId:                 Some questId.
        :param quester:                 Some Quester.
        :param objectiveIndexCompleted: The index of the objective that was completed. Used for questTypes that
                                        may be able to complete on their own, causing branches (VisitQuests).
        :return:                        The questId afterwards.
        :rtype: Optional[QuestId]
        """
        questSource, chainId, objectiveId, subObjectiveId = questId.toStruct()

        # First, we get the questObjective at this questId.
        multiObjective: MultiObjective = cls.getQuestObjectiveFromId(questId=questId, quester=quester)
        questObjective: QuestObjective = multiObjective.getObjectiveIndex(objectiveIndexCompleted)

        # With this questObjective, we get the next step in line.
        nextStep = questObjective.getNextStep()

        # If there is a next step, stay in the chain.
        if nextStep != END:
            # Return the next QuestId.
            return QuestId(
                questSource=questSource,
                chainId=chainId,
                objectiveId=nextStep,
                subObjectiveId=objectiveIndexCompleted,
            )

        # Otherwise, this is the end of this chain. Perhaps we go to the next chain?
        # So first, get the questChain.
        questChain = cls.getQuestChainFromQuestId(questId=questId, quester=quester)

        # Are we going to a next chain?
        nextChainId = questChain.getNextChainId()

        # Go to the next chain.
        if nextChainId is not None:
            # Cool, get the next chain id.
            nextQuestChain = cls.getQuestChainFromId(questSource=questSource, chainId=nextChainId, quester=quester)

            # Get the initial objective of this quest chain.
            startObjectiveId = nextQuestChain.getStartObjectiveId()

            # Return our next QuestId.
            return QuestId(
                questSource=questSource,
                chainId=nextChainId,
                objectiveId=startObjectiveId,
                subObjectiveId=objectiveIndexCompleted,
            )

        # We have reached the end of the quest chain. No quest ID to give.
        return None

    @classmethod
    def getQuestChainFromChainId(cls, questSource: int, chainId: int, quester: Quester):
        return cls.questLines.get(questSource).questLine.get(chainId)
