import math

from toontown.quest3.base.QuestObjective import *
from toontown.quest3.context.NPCInteractContext import NPCInteractContext
from toontown.quest3.objectives import VisitObjective
from toontown.quest3.QuestLocalizer import (AuxillaryText_To, HL_Deliver, OBJ_Deliver,
                                            PROG_Deliver, QuestProgress_Complete, SC_DeliverJbs, PFX_DELIVER)
from toontown.toon.npc.NPCToonConstants import NPCToonEnum


class DeliverJellybeanObjective(VisitObjective):

    def __init__(self,
                 npc = 2001,
                 rewards=None,
                 nextStep=None,
                 npcReturnable: bool = False,
                 jellybeans: int=1):
        super().__init__(npc=npc, rewards=rewards, nextStep=nextStep, npcReturnable=npcReturnable)
        self.jellybeans = jellybeans

    def calculateProgress(self, context: NPCInteractContext, questReference: QuestReference, quester: Quester) -> int:
        result = super().calculateProgress(context, questReference, quester)
        if result:
            progress = questReference.getQuestProgress(self.objectiveIndex)
            amountNeeded = self.jellybeans - progress
            av = context.av

            currentMoney = av.getTotalMoney()

            if currentMoney > 0:
                # Clamp the value. The amount we take should never be above
                # their current money or the amount they need to pay.
                takenMoney = min(max(currentMoney - amountNeeded, currentMoney), amountNeeded)

                # We succeeded in robbing them, return the amount.
                if av.takeMoney(takenMoney):
                    return takenMoney

        return 0
    
    @staticmethod
    def getDifficultyRange(questerType: QuesterType, questSource: QuestSource, **extraArgs):
        """
        Returns the difficulty range required to use this objective in random quest generation.

        :return: Any of the following:
                 A) Two floats, for a lower and upper bound
                 B) A float and None, for a lower bound and no upper bound
                 C) None and a float, for no lower bound and an upper bound
                 D) Two nones, for no difficulty bound
                 E) One none, for "cannot be used"
        """
        if questSource == QuestSource.KudosQuest:
            return 1, 45
        return None

    @staticmethod
    def getObjectiveWeight(questerType: QuesterType) -> int:
        """
        The likelihood for this objective to be chosen in a pool.
        The de facto amount is 100.
        """
        return 1

    @classmethod
    def generateFromDifficulty(cls, rng, difficulty: float, questSource: QuestSource, **extraArgs):
        """
        Given an arbitrary difficulty value, generate a QuestObjective.
        For more info, seek QuestGenerator.py.

        :param rng:        A seeded Random instance. Use this for .random() or .randint() calculations.
        :param difficulty: The arbitrary difficulty of the task.
        :return:           This QuestObjective, set with values to match the arbitrary difficulty.
        """
        jellybeans = 25 * difficulty ** 1.8
        jellybeans += ((jellybeans * 0.1) * rng.choice((-1, 1)))

        # Determine a recipient for delivery tasks
        toNpcId = extraArgs.get("npc")
        if not toNpcId:
            zoneId = extraArgs.get("zoneId")
            potentialNpcIds = [  # Cleanse our list of candidates to make sure we're being reasonable
                npcId for npcId, npcToon in NPCToons.NPCToonDict.items() if ZoneUtil.getHoodId(npcToon.zoneId) == zoneId
                and ZoneUtil.getBranchZone(npcToon.zoneId) != zoneId  # Make sure they're on a street in our PG
                and npcToon.npcType == NPCToonEnum.REGULAR  # Validate the NPC type
                and NPCToons.getBuildingTitle(npcToon.zoneId) not in ['', 'Toon HQ', TTLocalizer.GlobalStreetNames.get(
                    ZoneUtil.getBranchZone(npcToon.zoneId), "Unknown Location")[2]]  # Validate their zone id
            ] or [2001]  # Fall back to Flippy if we somehow kill everyone else
            toNpcId = potentialNpcIds[
                int(extraArgs.get("chainId", 1)*difficulty*zoneId) % len(potentialNpcIds)]  # Select a candidate based on various immutable factors

        if toNpcId in NPCToons.getNPCByNPCType(NPCToonEnum.HQRANGER):
            jellybeans *= 1.25
        elif toNpcId in NPCToons.getNPCByNPCType(NPCToonEnum.HQ_INTERN):
            jellybeans *= 0.75
        
        # Round off our jellybean count so that it is pretty.
        jellybeans = math.ceil(jellybeans)
        if jellybeans < 1:
            jellybeans = 1
        elif jellybeans < 10:
            pass
        elif jellybeans < 20:
            jellybeans = round(round(jellybeans / 2) * 2)
        elif jellybeans < 50:
            jellybeans = round(round(jellybeans / 5) * 5)
        elif jellybeans < 100:
            jellybeans = round(round(jellybeans / 10) * 10)
        elif jellybeans < 200:
            jellybeans = round(round(jellybeans / 20) * 20)
        else:
            jellybeans = round(round(jellybeans / 25) * 25)

        # It's robbing time
        return cls(
            jellybeans=jellybeans,
            npcReturnable=False,
            npc=toNpcId,
        )

    def modifyPoster(self, questReference: QuestReference, poster):
        lIconGeom = loader.loadModel('phase_3.5/models/gui/jar_gui')
        poster.visual_setFrameGeom(poster.LEFT, geom=lIconGeom, scale=0.25)
        poster.visual_setFrameColor(poster.LEFT, 'lightGreen')
        poster.visual_setFrameText(poster.LEFT, PFX_DELIVER + f"{self.jellybeans} Jellybeans")

        poster.visual_setNpcFrame(poster.RIGHT, self.getToNpcId())
        poster.visual_setFrameColor(poster.RIGHT, 'lightGreen')
        poster.visual_setFrameText(poster.RIGHT, self.getToNpcName())

        poster.visual_setAuxText(AuxillaryText_To)
        poster.label_auxillaryText.show()

        complete = questReference.isQuestComplete(base.localAvatar, self.objectiveIndex)
        
        if not complete:
            value, range, textFormat = self.getProgressFormat(questReference)
            poster.visual_setProgressInfo(value=value, range=range, textFormat=textFormat)

        lIconGeom.removeNode()

    def getProgressFormat(self, questReference):
        return questReference.getQuestProgress(self.objectiveIndex), self.jellybeans, PROG_Deliver

    def getSpeedchatMessages(self, quester, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(quester, self.objectiveIndex):
            return tuple()
        return tuple([SC_DeliverJbs] + list(self.getFinishToontaskStrings()))

    def getHeadline(self, questReference: QuestReference, objectiveSelected: int = 0) -> str:
        return HL_Deliver
    
    def getCompletionRequirement(self) -> int:
        return self.jellybeans
    
    def getObjectiveGoal(self) -> str:
        return OBJ_Deliver % "Jellybeans"
    
    def getProgressString(self, questReference: QuestReference, progress: int) -> str:
        if questReference.isQuestComplete(base.localAvatar, self.objectiveIndex):
            return QuestProgress_Complete
        elif self.jellybeans == 1:
            return ''
        return PROG_Deliver.format(value=min(progress, self.jellybeans), range=self.jellybeans)

    def _getKwargStr(self):
        kwargstr = super()._getKwargStr()
        if self.jellybeans != 1:
            kwargstr += f'jellybeans={self.jellybeans}, '
        return kwargstr

    def __repr__(self):
        return f'DeliverJellybeanObjective({self._getKwargStr()[:-2]})'
