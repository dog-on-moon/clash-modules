"""
This module holds the container class required to define a full quest chain.
"""
from datetime import datetime, timedelta

from toontown.quest3.base.QuestObjective import QuestObjective, END, MultiObjective
from toontown.quest3.base.QuestReward import QuestReward
from toontown.quest3.base.Quester import Quester
from toontown.quest3.requirements.QuestRequirement import QuestRequirement
from toontown.time.ToontownTimeZone import ToontownTimeZone


class QuestChain:
    """
    The QuestChain container class.

    Contains all of the information required to define a full QuestChain.
    """

    __slots__ = ['source', 'steps', 'nextChain', 'rewards', 'dynamicRewards',
                 'questChainLength', 'deletable', 'startDate', 'endDate', 'required']

    def __init__(self,
                 steps,
                 nextChain = None,
                 rewards = None,
                 dynamicRewards = None,
                 deletable: bool = False,
                 startDate: datetime = None,
                 endDate: datetime = None,
                 required: list = None) -> None:
        """
        Defines a QuestChain.

        :param steps:           A dictionary holding all of the QuestTypes within a QuestChain.
        :type: Dict[int, Union[QuestObjective, MultiObjective]]

        :param nextChain:       After this Quest Chain is completed, give the Quester the next quest chain.
        :type: Optional[int]

        :param rewards:         A list of rewards to be granted to the Quester upon chain completion.
        :type: Union[QuestReward, tuple, None]

        :param dynamicRewards:  A list of rewards to be granted to the Quester. The reward is split dynamically,
                                given to the Quester for each QuestStep completed.
        :type: Union[QuestReward, tuple, None]

        :param deletable:       Can this QuestChain be deleted from the Quester?
        :param startDate:       The start date this QuestChain is offered.
        :param endDate:         The end date this QuestChain expires.

        :param required:        A list of prerequisites for this QuestChain.
        :type: Union[QuestRequirement, list, None]
        """
        # Process the args.
        ##########################
        if rewards is None:
            rewards = []
        elif isinstance(rewards, QuestReward):
            rewards = [rewards]
        ##########################
        if dynamicRewards is None:
            dynamicRewards = []
        elif isinstance(dynamicRewards, QuestReward):
            dynamicRewards = [dynamicRewards]
        ##########################
        if required is None:
            required = []
        elif isinstance(required, QuestRequirement):
            required = [required]
        ##########################

        # Define the variables of the QuestChain.
        self.steps = steps
        self.nextChain = nextChain
        self.rewards = rewards
        self.dynamicRewards = dynamicRewards
        self.deletable = deletable
        self.startDate = startDate
        self.endDate = endDate
        self.required = required

        # Do some post-processing on the QuestChain.
        self._processSteps()
        self.questChainLength = self._calculateLength()

    def _processSteps(self) -> None:
        """
        Processes our Steps dictionary.
        nextStep is assigned to each QuestObjective, and we wrap
        all QuestObjectives in a list for each step.
        """
        if not self.steps:
            return
        lastQuestIndex = max(self.steps.keys())
        for index, multiObjective in self.steps.items():
            if not isinstance(multiObjective, MultiObjective):
                # Turn this quest objective into a single-length multi objective.
                multiObjective = MultiObjective(multiObjective)
                self.steps[index] = multiObjective

            # Process the QuestData, assigning nextSteps accordingly.
            for objectiveIndex, questObjective in enumerate(multiObjective.getQuestObjectives()):
                questObjective: QuestObjective
                questObjective.assignObjectiveIndex(objectiveIndex=objectiveIndex)

                # If no nextStep assigned, assign one.
                if questObjective.getTrueNextStep() is None:
                    # Assign the next step.
                    if index != lastQuestIndex:
                        questObjective.assignNextStep(index + 1)
                    # If we're at the end, assign the sentinel end.
                    else:
                        questObjective.assignNextStep(END)

    def _calculateLength(self):
        """Calculates the length of the quest chain."""
        initialObjective = self.steps[self.getStartObjectiveId()].getInitialObjective()
        return self.getStepsLeftFromObjective(initialObjective)

    def getStepsLeftFromObjective(self, questObjective: QuestObjective) -> int:
        """Get the steps left from a given objective."""
        if not self.steps:
            return 0

        currentObjective = questObjective
        objectiveCount = 0

        while True:
            # Increment our objective count.
            if not getattr(currentObjective, "fromRandomKudosQuest", False):
                objectiveCount += 1

            # Get the next step.
            nextStep = currentObjective.getNextStep()

            # Break if it's over.
            if nextStep is END:
                return objectiveCount

            # Set next objective.
            currentObjective = self.steps.get(nextStep).getInitialObjective()

            # Break early if we believe something stupid has happened.
            if objectiveCount > 1000:
                raise AttributeError("This QuestChain was defined with an infinite loop!")

    def isExpired(self) -> bool:
        """Determine if the quest chain is expired.
        """
        if self.startDate is not None and self.endDate is not None:
            # This is an event task, are we in the right event?
            currentTime = datetime.now(tz=ToontownTimeZone())
            if self.startDate < currentTime < self.endDate:
                return False

            # We are not in the relevant date (dies of cringe).
            return True
        else:
            # Not an event -- does not expire.
            return False
    
    def validate(self, quester: Quester) -> bool:
        """Validate if the quest can be picked up by the indicated quester.
        """
        # First, check to see if the quest is allowed to be picked up for limited time quests.
        if self.isExpired():
            return False

        # Find out if the quester meets the requirements.
        for req in self.required:
            if not req.check(quester):
                return False

        # This quester can pick up the quest.
        return True

    """
    Modifers
    """

    def addReward(self, reward):
        self.rewards = tuple(list(self.rewards) + [reward])

    def setDeletable(self, mode: bool = True):
        self.deletable = mode

    """
    Getters
    """

    def isDeletable(self):
        """Is this QuestChain deletable?"""
        return self.deletable

    def getStartObjectiveId(self):
        """Returns the starting objective ID."""
        return min(self.steps.keys())
    
    def getInitialObjective(self) -> QuestObjective:
        return self.steps[self.getStartObjectiveId()].getInitialObjective()

    def getNextChainId(self):
        """Gets the next chain id.
        
        :rtype: Optional[int]
        """
        return self.nextChain

    def getQuestObjectivesAtId(self, objectiveId: int) -> MultiObjective:
        """
        Returns the tuple of questObjectives at a given id.
        :param objectiveId: The ID to check for questObjectives.
        """
        assert objectiveId in self.steps, "QuestChain has non-existent objectiveId"
        return self.steps.get(objectiveId)

    def getQuestRewards(self):
        """Returns all QuestRewards.

        :rtype: Tuple[QuestReward]
        """
        return self.rewards

    def getDynamicQuestRewards(self):
        """Returns all dynamic QuestRewards.
        
        :rtype: Tuple[QuestReward]
        """
        return self.dynamicRewards

    def getQuestChainLength(self):
        """Gets the length of the quest chain."""
        return self.questChainLength

    def isEventChain(self) -> bool:
        return bool(self.endDate)

    """
    Repr presentation
    """

    def __repr__(self):
        msg = "QuestChain(\n"
        if self.nextChain:
            msg = msg + '\t' + f'nextChain={self.nextChain},' + '\n'
        if self.rewards:
            msg = msg + '\t' + f'rewards={repr(tuple(self.rewards))},' + '\n'
        if self.dynamicRewards:
            msg = msg + '\t' + f'dynamicRewards={repr(tuple(self.dynamicRewards))},' + '\n'
        if self.startDate:
            msg = msg + '\t' + f'startDate={repr(self.startDate)},' + '\n'
        if self.endDate:
            msg = msg + '\t' + f'endDate={repr(self.endDate)},' + '\n'
        if self.required:
            msg = msg + '\t' + f'required={repr(tuple(self.required))},' + '\n'
        if self.deletable:
            msg = msg + '\t' + f'deletable={repr(self.deletable)},' + '\n'
        msg += '\tsteps={\n'
        for key, obj in self.steps.items():
            msg += '\t\t' + f'{key}: {repr(obj)},' + '\n'
        msg += '\t}\n'
        msg += '),'
        return msg
