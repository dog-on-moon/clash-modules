from typing import TYPE_CHECKING, Tuple

from toontown.quest3.QuestEnums import QuestSource, QuesterType
from toontown.quest3.base.QuestHistory import QuestHistory
from toontown.quest3.base.QuestObjective import QuestObjective, MultiObjective
from toontown.quest3.base.QuestContext import QuestContext
from toontown.quest3.base.QuestLine import QuestLine
from toontown.quest3.base.QuestReference import QuestReference, QuestId
from toontown.quest3.base.Quester import Quester
from toontown.quest3 import questlines  # necessary import for load.
from toontown.quest3.context.NPCInteractContext import NPCInteractContext
from toontown.quest3.questlines.MainQuestLine import MainQuestLine
from toontown.toon.DistributedToonAI import DistributedToonAI
from toontown.toon.ToonStatsGlobals import ToonStats
from toontown.toonbase import ToontownGlobals
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory

if TYPE_CHECKING:
    from toontown.ai.ToontownAIRepository import ToontownAIRepository


@DirectNotifyCategory()
class QuestManagerAI:
    """
    The dedicated Quest Manager class.

    Can progress an objective for a given "Quester" object, given some Objective context.
    """

    def __init__(self, air):
        self.air = air  # type: ToontownAIRepository

    def progressObjective(self, quester: Quester, context: QuestContext, 
                          completeOnlyOne: bool=False, detectProgress: bool=False):
        """
        Given a Quester, all of its quest references are obtained,
        which get dereferenced to individual QuestParts.

        On each QuestPart, a list of QuestObjectives have their calculateProgress
        method called with the context passed in from the messenger call.

        calculateProgress returns an integer of how much the Quester's
        questRef needs to have its progress increment by. It does all of
        this, and then after doing so for each QuestObjective on each
        QuestPart, let the Quester do a sendUpdate to reflect
        the updated objectives on the client. (Optimize by not doing
        this sendUpdate if calculateProgress returns a zero always.)
        """
        completedIds = []
        madeProgress = False

        # First, gather the actual QuestReferences.
        questReferences = quester.getQuestReferences()

        # We'll need to obtain the questObjectives associated with the quest references.
        for questReference in questReferences[:]:
            questReference: QuestReference
            multiObjective: MultiObjective = QuestLine.dereferenceQuestReference(questReference, quester=quester)

            # Figure out how much we need to progress this questReference.
            for index, questObjective in enumerate(multiObjective.getQuestObjectives()):
                # Ignore it if it is complete.
                if questObjective.isComplete(questReference=questReference, objectiveIndex=index, quester=quester):
                    continue

                # How much progress have we made?
                progress = questObjective.calculateProgress(context, questReference, quester)

                # Did we do something?
                if progress:
                    madeProgress = True

                    # Progress the questReference by this amount.
                    questReference.progressObjective(index, progress)

                    # Cache the quest ID that was just completed.
                    if questReference.isQuestComplete(quester, index):
                        completedIds.append(QuestId(
                            questSource=questReference.getQuestSource(),
                            chainId=questReference.getChainId(),
                            objectiveId=questReference.getObjectiveId(),
                            subObjectiveId=index,
                        ))

                # If we have found one, get out of here if we want to.
                if completedIds and completeOnlyOne:
                    break

            # Does the grouping of objectives suggest that we should complete it now?
            # We also check if the quest ref is still in the quester's references.
            # If another quest's rewards happened to progress it into the next step, it won't be here anymore.
            if multiObjective.isComplete(questReference, context=context, quester=quester) and \
                    questReference in quester.getQuestReferences():
                self.completeQuest(quester=quester, questReference=questReference)
                completedIds.append(
                    QuestId(
                        questSource=questReference.getQuestSource(),
                        chainId=questReference.getChainId(),
                        objectiveId=questReference.getObjectiveId(),
                        subObjectiveId=0,
                    )
                )

            # If we have found one, get out of here if we want to.
            if completedIds and completeOnlyOne:
                break

        # If the questReferences have progressed, then tell the quester to update.
        if completedIds or madeProgress:
            quester.updateQuestProgress()

        # Notify the world we're progressing a quester's objective.
        messenger.send('progressObjective', [quester, context])

        # Return the quests that we completed.
        if completeOnlyOne:
            # We only return the single questId if we only want to complete one.
            retval = completedIds[0] if completedIds else None
            # Return if progress was made on any quest if asked.
            if detectProgress:
                return (retval, madeProgress)
            return retval
        else:
            # We return all completed questIds if we completed multiple.
            retval = completedIds
            # Return if progress was made on any quest if asked.
            if detectProgress:
                return (retval, madeProgress)
            return retval

    def completeQuest(self, quester: Quester, questReference: QuestReference, objectiveIndexCompleted: int = 0) -> None:
        """
        Makes a quester's QuestReference complete, and moves it to the next part of its QuestChain.
        Make sure to call quester.updateQuestProgress() externally after.

        :param quester:                 The Quester object.
        :param questReference:          The QuestReference instance.
        :param objectiveIndexCompleted: The index of the objective that was completed. Used for questTypes that
                                        may be able to complete on their own, causing branches (VisitQuests).
        """
        # Ensure this Quester has this questReference.
        questReferences = quester.getQuestReferences()
        if questReference not in questReferences:
            self.notify.error(f'Quester {quester} marked completeQuest for this '
                              f'questReference they did not have: {questReference}. '
                              f'This may lead to a softlock, so shut down ASAP')
            return

        # Get the next QuestId.
        nextQuestId = QuestLine.getNextQuestId(questReference.getQuestId(), quester, objectiveIndexCompleted)

        # We don't need to create a new quest reference if we've reached the end.
        if nextQuestId is None:
            questReferences.remove(questReference)
        else:
            # Make our new QuestReference.
            newQuestReference = QuestReference(questId=nextQuestId)

            # Get the index of the reference we're updating.
            questReferenceIndex = questReferences.index(questReference)

            # Replace it in the quester's questReferences.
            questReferences[questReferenceIndex] = newQuestReference

        # Go ahead and reward the quester for doing a good job.
        self.handleQuestRewards(quester=quester, questReference=questReference, nextQuestId=nextQuestId)

        # Run different methods depending on the quester.
        if quester.questerType == QuesterType.Toon:
            self.completeToonQuest(quester=quester, questReference=questReference)

    @staticmethod
    def handleQuestRewards(quester, questReference: QuestReference, nextQuestId: QuestId):
        """
        Handles quest rewards for a Quester.
        :param quester:         The quester to give quest rewards to.
        :param questReference:  The questReference.
        :param nextQuestId:     The QuestId that comes next.
        :return:                None.
        """
        # Get some properties of the quest reference.
        questId = questReference.getQuestId()
        questObjectives = QuestLine.dereferenceQuestReference(questReference, quester=quester).getQuestObjectives()
        questChain = QuestLine.getQuestChainFromQuestId(questId, quester=quester)

        # First, handle any rewards local to the QuestReference.
        for index, objective in enumerate(questObjectives):
            # Give rewards if this objective is complete.
            if not objective.isComplete(questReference=questReference, objectiveIndex=index, quester=quester):
                continue

            # Get the objective's rewards.
            rewards = objective.getQuestRewards()

            # Iterate over each reward.
            for reward in rewards:
                # Give the reward to the quester.
                reward.handleReward(quester=quester)

        # Next, handle partial objectives within the QuestChain.
        dynamicRewards = questChain.getDynamicQuestRewards()
        rewardMultiplier = 1.0 / max(1, questChain.getQuestChainLength())

        for reward in dynamicRewards:
            # Give the reward to the quester, with the reward multiplier.
            reward.handleReward(quester=quester, multiplier=rewardMultiplier)

        # If we have totally completed the chain, handle those rewards too.
        if nextQuestId is None or questId.getChainId() != nextQuestId.getChainId():
            # We are on the next quest chain.
            rewards = questChain.getQuestRewards()
            for reward in rewards:
                # Give the reward to the quester.
                reward.handleReward(quester=quester)

            # The quester has completed the chain entirely, add that to their history.
            quester.addQuestHistory(QuestHistory.fromQuestId(questId))

    @staticmethod
    def completeToonQuest(quester: DistributedToonAI, questReference: QuestReference):
        """
        Called when a Toon completes a Quest.

        :param quester:         The DistributedToonAI.
        :param questReference:  The quest reference.
        """
        quester.addStat(ToonStats.TASKS)
        # TODO - implement showQuestTip from old quest manager
