"""
This module defines the abstract Quester object.
"""
from toontown.quest3.QuestEnums import QuestSource
from toontown.quest3.base.QuestHistory import QuestHistory
from toontown.quest3.base.QuestReference import QuestId, QuestReference


class Quester:
    """
    A Quester is some base class representing an object that contains
    QuestReference objects. Questers can be objects such as Toons with ToonTasks,
    or other objects such as Clubs that contain Club Tasks.
    """

    questerType = None

    def addQuest(self, questId: QuestId) -> bool:
        """
        Adds a new Quest to the Quester.
        :param questId: The questId of the quest.
        :return: True if successful, False if not.
        """
        raise NotImplementedError

    def addQuestHistory(self, questHistory: QuestHistory) -> None:
        """
        Adds new QuestHistory to the Quester.
        :param questHistory: The QuestHistory object.
        """
        raise NotImplementedError

    def getQuestReferences(self):
        """
        Gets the list of QuestReferences off of the Quester.

        :rtype: List[QuestReference]
        """
        raise NotImplementedError

    def getVisibleQuests(self):
        """
        Gets all visible quests off the Quester.

        :rtype: List[QuestReference]
        """
        from toontown.quest3.base.QuestGlobals import HiddenQuestSources
        return self.getQuestReferencesOfSource(*HiddenQuestSources, negate=True)

    def getQuestReferencesOfSource(self, *questSources, negate: bool = False):
        """
        Gets the quest references of a type.

        :param questSources: A QuestSource, or a tuple.
        :param negate: Get all quest sources except those listed.
        """
        if not negate:
            return [questRef for questRef in self.getQuestReferences() if questRef.getQuestSource() in questSources]
        else:
            return [questRef for questRef in self.getQuestReferences() if questRef.getQuestSource() not in questSources]

    def getQuestHistory(self):
        """
        Gets the list of QuestHistory off of the Quester.

        :rtype: List[QuestHistory]
        """
        raise NotImplementedError

    def updateQuestProgress(self) -> None:
        """
        Whenever the QuestManagerAI updates our quest references,
        this method gets called.
        """
        raise NotImplementedError

    """
    Handy accessors
    """

    def completedQuestId(self, questId: QuestId, matchOk: bool = False) -> bool:
        """
        Determines if the Quester has completed a QuestID.
        Includes current chain IDs in questrefs.

        TODO : Currently, does not account for branching path objectives, which we don't
         even do yet, so eventually, QuestChains should get a getter that calculates all
         possible "routes" of a QuestChain (i.e. returns a list of all ordered step lists).
         From these lists, we find which lists the refQuestId's objective ID are in,
         and determine if the questId's objective ID comes after the refQuestId's objective
         ID in those lists. Right now, it just natively compares "is the questId objective ID
         behind the refQuestId objective ID" to test completion.

        :param questId: The quest ID to check.
        :param matchOk: If the questId is equal to a quest we are currently on, should we return true?
        """
        # Is the chain completed in history?
        if self.hasCompletedQuest(questSource=questId.getQuestSource(), chainId=questId.getChainId()):
            # This quest ID is in history.
            return True

        # Is the quest in a current questref?
        # We check all of them and iterate through just in case.
        for questRef in self.getQuestReferences():
            # Get a couple variables.
            refQuestId = questRef.getQuestId()

            # Only compare if we're the same chain and source.
            if questId.getQuestSource() != refQuestId.getQuestSource():
                continue
            if questId.getChainId() != refQuestId.getChainId():
                continue

            # If we're OK with matching questId objectives, then we check if
            # we are currently on this objective Id and return True if so.
            if matchOk and questId.getObjectiveId() == refQuestId.getObjectiveId():
                return True

            # If the ID objective is greater than or equal to the reference ID objective,
            # then we can assume that we have not completed it, and we check other questrefs.
            if questId.getObjectiveId() >= refQuestId.getObjectiveId():
                # The ID we think we could be complete, we have not got to its objective yet.
                continue

            # Ok, we can assume we have completed it.
            return True

        # This quest ID has not been completed.
        return False

    def hasCompletedQuestHistory(self, questHistory: QuestHistory) -> bool:
        return questHistory in self.getQuestHistory()

    def hasCompletedQuest(self, questSource: QuestSource, chainId: int) -> bool:
        """
        Determine if this Quester has completed the indicated quest.
        """
        questHistory = QuestHistory(questSource, chainId)
        return self.hasCompletedQuestHistory(questHistory)

    def hasQuest(self, questId: QuestId, history: bool = False) -> bool:
        """
        Determine whether the given QuestId exists in any of this
        Quester's QuestReferences.
        """
        # Check their refs.
        for ref in self.getQuestReferences():
            qid = ref.getQuestId()
            if (qid.getQuestSource(), qid.getChainId()) == (questId.getQuestSource(), questId.getChainId()):
                return True

        # Check history (if we want to do that)
        if history and self.hasCompletedQuest(
                questSource=questId.getQuestSource(),
                chainId=questId.getChainId(),
            ):
            return True

        # They do not have it
        return False

    def getQuestObjectivesOfType(self, questObjectiveCls, includeComplete: bool = False,
                                 source=None  # type: QuestSource | None
                                 ) -> list:
        """Given a quest objective class, returns a list of all matching objectives of type"""
        from toontown.quest3.base.QuestLine import QuestLine
        retObjectives = []
        for questRef in self.getQuestReferences():
            if source is not None and questRef.getQuestSource() != source:
                continue

            multiObjective = QuestLine.dereferenceQuestReference(questRef, quester=self)
            for i, objective in enumerate(multiObjective.getQuestObjectives()):
                if not includeComplete and objective.isComplete(questReference=questRef,
                                                                objectiveIndex=i, quester=self):
                    continue
                if type(objective) is questObjectiveCls:
                    retObjectives.append(objective)
        return retObjectives
    
    def hasReachedQuest(self, questSource: QuestSource, chainId: int, objectiveId: int=1) -> bool:
        """Determines if the quester either has the quest in their quest references, or if
        the chain id exists in their quest history.
        """
        # First, find it in their quest history.
        questHistory = QuestHistory(questSource, chainId)
        if questHistory in self.getQuestHistory():
            return True
        
        # Then, try to find it in their quest references.
        for questReference in self.getQuestReferences():
            questReference: QuestReference
            if questReference.getQuestSource() == questSource and questReference.getChainId() == chainId and \
                questReference.getObjectiveId() >= objectiveId:
                return True

        # They haven't reached the quest yet.
        return False
    
    def getQuestIdsFromRefs(self) -> list:
        return [qr.getQuestId() for qr in self.getQuestReferences()]
    
    def getQuestHistoryOfSource(self, questSource: QuestSource) -> list:
        return [questHistory for questHistory in self.getQuestHistory() \
            if questHistory.questSource == questSource]
    
    def getHighestChainIdOfSource(self, questSource: QuestSource) -> int:
        qhOfSrc = self.getQuestHistoryOfSource(questSource)
        if not qhOfSrc:
            return
        return max([qr.getChainId() for qr in qhOfSrc])
