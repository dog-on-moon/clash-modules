"""
Module class for the QuestReference.
"""
from toontown.quest3.QuestEnums import QuestSource
from toontown.quest3.base.QuestExceptions import QuestDereferenceException
from toontown.utils.AstronStruct import AstronStruct


class QuestId(AstronStruct):
    """
    A class containing the chain and part ID for a Quest.
    """

    def __init__(self, questSource: QuestSource, chainId: int, objectiveId: int, subObjectiveId: int = 0):
        self.questSource = questSource
        self.chainId = chainId
        self.objectiveId = objectiveId
        self.subObjectiveId = subObjectiveId
    
    def __eq__(self, __o) -> bool:
        """
        :param __o: QuestId
        """
        if isinstance(__o, QuestId):
            # We don't care about the sub objective id when determining equality.
            ourAttrs = (self.questSource, self.chainId, self.objectiveId)
            theirAttrs = (__o.questSource, __o.chainId, __o.objectiveId)

            return all([ourAttr == theirAttr for ourAttr, theirAttr in zip(ourAttrs, theirAttrs)])
        return False

    def __repr__(self):
        return f"QuestId({QuestSource(self.questSource).name} : Chain #{self.chainId} : Objective #{self.objectiveId})"

    def toStruct(self):
        """
        :rtype: list
        """
        return [self.questSource, self.chainId, self.objectiveId, self.subObjectiveId]

    def getQuestSource(self) -> QuestSource:
        return self.questSource

    def getChainId(self) -> int:
        return self.chainId

    def getObjectiveId(self) -> int:
        return self.objectiveId

    def getSubObjectiveId(self) -> int:
        return self.subObjectiveId


class QuestReference(AstronStruct):
    """
    A reference to a Quest's defined chain/part ID in the Questline.

    Also contains a 'progress' list to reflect the progress the Quester
    has made in the quest that is being referenced.
    """

    def __init__(self, questId: QuestId, progress = None):
        """
        :type progress: list
        """
        # Set our questId.
        self.questId = questId

        # If we have no progress list set, determine the size
        # of it from the questId passed in.
        from toontown.quest3.base.QuestLine import QuestLine
        try:
            objectiveCount = QuestLine.dereferenceQuestReference(self).getObjectiveCount()
        except Exception as e:
            raise QuestDereferenceException(f'The following QuestID has caused a deref crash: {questId}')

        if progress is None:
            progress = [0] * objectiveCount
        else:
            # Make sure this progress list is long enough.
            # Necessary sanity check, in case quest is initialized w/o enough progress fields
            while len(progress) < objectiveCount:
                progress.append(0)

        # Set our progress list now.
        self.progress = progress
    
    def __eq__(self, __o) -> bool:
        """
        :param __o: QuestReference
        """
        if isinstance(__o, QuestReference):
            return all([ourAttr == theirAttr for ourAttr, theirAttr in zip(self.toStruct(), __o.toStruct())])
        return False

    def __repr__(self):
        return f"QuestReference({self.questId}, progress={self.progress})"

    def toStruct(self):
        """
        :rtype: list
        """
        return [self.questId.toStruct(), self.progress]

    @classmethod
    def fromStruct(cls, struct):
        """
        :param struct: list
        :rtype: QuestReference
        """
        questId, progress = struct
        questId = QuestId.fromStruct(questId)
        return cls(questId=questId, progress=progress)

    @classmethod
    def fromStructList(cls, struct):
        """Turns a list containing structs into a class of specifically this struct.

        :param struct: list
        """
        return [cls.fromStruct(substruct) for substruct in cls.validateRawQuestRefs(struct)]

    @staticmethod
    def validateRawQuestRefs(rawQuestRefs: list) -> list:
        """
        Given a list of raw quest references,
        returns a new list of valid quests.
        """
        newRefs = []
        from toontown.quest3.base.QuestLine import QuestLine
        for ref in rawQuestRefs:
            questId, progress = ref
            questId = QuestId.fromStruct(questId)
            objective = QuestLine.getQuestObjectiveFromId(questId, quester=None)
            if objective:
                newRefs.append(ref)
        return newRefs

    """
    Setters, for progress
    """

    def progressObjective(self, index: int, progress: int) -> None:
        """
        Progresses an objective by a given amount.
        :param index: The amount to progress the objective by.
        :param progress: How much progress we have made.
        """
        self.progress[index] += progress

    """
    Complex getters
    """

    def isQuestComplete(self, quester, objectiveIndex: int = None, context=None):
        """Determines if the quest reference is "complete"."""
        if objectiveIndex is None:
            from toontown.quest3.base.QuestLine import QuestLine
            multiObjective = QuestLine.dereferenceQuestReference(self, quester=quester)

            # Is the multi objective considered complete?
            return multiObjective.isComplete(questReference=self, context=context, quester=quester)
        else:
            from toontown.quest3.base.QuestLine import QuestLine
            questObjective = QuestLine.dereferenceQuestReference(self, quester=quester).getObjectiveIndex(objectiveIndex=objectiveIndex)

            # Is this objective complete?
            return questObjective.isComplete(questReference=self, objectiveIndex=objectiveIndex, quester=quester)

    def getQuestProgress(self, objectiveIndex: int = None):
        """Gets the quest progress."""
        if objectiveIndex is None:
            objectiveIndex = self.getSubObjectiveId()
        return self.progress[objectiveIndex]

    """
    Getters
    """

    def getQuestId(self) -> QuestId:
        return self.questId

    def getQuestSource(self) -> QuestSource:
        return self.getQuestId().getQuestSource()

    def getChainId(self) -> int:
        return self.getQuestId().getChainId()

    def getObjectiveId(self) -> int:
        return self.getQuestId().getObjectiveId()

    def getSubObjectiveId(self) -> int:
        return self.getQuestId().getSubObjectiveId()

    def isEventTask(self) -> bool:
        from toontown.quest3.base.QuestLine import QuestLine
        questChain = QuestLine.getQuestChainFromQuestId(questId=self.getQuestId(), quester=None)
        return bool(questChain.isEventChain())

    def getProgress(self):
        """
        :rtype: list
        """
        return self.progress

    """
    Setters
    """

    def makeComplete(self, quester) -> None:
        """Makes this QuestReference have complete progress."""
        from toontown.quest3.base.QuestLine import QuestLine
        for objectiveIndex in range(len(self.getProgress())):
            questObjective = QuestLine.dereferenceQuestReference(self, quester=quester).getObjectiveIndex(objectiveIndex=objectiveIndex)
            self.progress[objectiveIndex] = questObjective.getCompletionRequirement()
