from toontown.quest3.QuestLocalizer import AuxillaryText_To, HL_Deliver, OBJ_Deliver, SC_Deliver, LevelXGag, Gag, \
    Gags, PROG_Deliver, PFX_DELIVER
from toontown.quest3.base.QuestObjective import *
from toontown.quest3.context.NPCInteractContext import NPCInteractContext
from toontown.quest3.objectives import VisitObjective
from toontown.battle.BattleGlobals import AvPropsNew


class DeliverGagObjective(VisitObjective):

    def __init__(self,
                 npc = 2001,
                 rewards=None,
                 nextStep=None,
                 npcReturnable: bool = False,
                 gagCount: int = 1,
                 gagLevel: int = 0):
        super().__init__(npc=npc, rewards=rewards, nextStep=nextStep, npcReturnable=npcReturnable)
        self.gagCount = gagCount
        self.gagLevel = gagLevel

    def calculateProgress(self, context: NPCInteractContext, questReference: QuestReference, quester: Quester) -> int:
        result = super().calculateProgress(context, questReference, quester)
        if result:
            # Okay so here we're looking to accept any kind of level x gag from the player
            gagLevel = self.gagLevel
            gagsTaken = 0
            progress = questReference.getQuestProgress(self.objectiveIndex)
            amountNeeded = self.gagCount - progress
            av = context.av

            for count, track in enumerate(av.inventory.inventory):
                # We have one or more of the required gag
                if track[gagLevel] > 0:
                    # We have more than needed
                    if track[gagLevel] >= amountNeeded:
                        av.inventory.setItem(
                            count, gagLevel, av.inventory.numItem(count, gagLevel) - amountNeeded
                        )
                        gagsTaken += amountNeeded
                        break
                    # We don't have enough in this track. Go to the next
                    else:
                        gagsAvailable = av.inventory.numItem(count, gagLevel)
                        gagsTaken += gagsAvailable
                        av.inventory.setItem(count, gagLevel, 0)
                        amountNeeded -= gagsAvailable

            if gagsTaken:
                av.b_setInventory(av.inventory.makeNetString())
            return gagsTaken

        return 0

    def getCompletionRequirement(self) -> int:
        return self.gagCount

    def modifyPoster(self, questReference: QuestReference, poster):
        invModel = loader.loadModel('phase_3.5/models/gui/inventory_icons')
        track = random.randint(0, 7)
        lIconGeom = invModel.find('**/' + AvPropsNew[track][self.gagLevel])
        poster.visual_setFrameGeom(poster.LEFT, geom=lIconGeom)
        poster.visual_setFrameColor(poster.LEFT, 'lightGreen')
        poster.visual_setFrameText(
            poster.LEFT,
            PFX_DELIVER + LevelXGag.format(
                amount='A' if self.gagCount == 1 else self.gagCount,
                level=self.gagLevel + 1,
                gag=Gags if self.gagCount > 1 else Gag,
            )
        )
        invModel.removeNode()

        poster.visual_setNpcFrame(poster.RIGHT, self.getToNpcId())
        poster.visual_setFrameColor(poster.RIGHT, 'lightGreen')
        poster.visual_setFrameText(poster.RIGHT, self.getToNpcName())

        poster.visual_setAuxText(AuxillaryText_To)
        poster.label_auxillaryText.show()

        poster.visual_setProgressInfo(
            value=questReference.getQuestProgress(self.objectiveIndex),
            range=self.gagCount,
            textFormat=PROG_Deliver,
        )
        if self.gagCount == 1:
            poster.waitbar_questProgress.hide()

    def getSpeedchatMessages(self, quester, questReference: QuestReference) -> tuple:
        if questReference.isQuestComplete(quester, self.objectiveIndex):
            return tuple()
        msg = SC_Deliver.format(
            LevelXGag.format(
                amount='a' if self.gagCount == 1 else self.gagCount,
                level=self.gagLevel + 1,
                gag=Gags if self.gagCount != 1 else Gag,
            )
        )
        return tuple([msg] + list(self.getFinishToontaskStrings()))

    def getHeadline(self, questReference: QuestReference, objectiveSelected: int = 0) -> str:
        return HL_Deliver
    
    def getObjectiveGoal(self) -> str:
        return OBJ_Deliver % "a Gag"
