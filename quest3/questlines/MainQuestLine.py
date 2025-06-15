"""
This module contains the full QuestLine dictionary.
"""
from toontown.inventory.enums.ItemEnums import BackgroundItemType, HatItemType, BackpackItemType, GlassesItemType, ShirtItemType, FurnitureItemType
from toontown.quest3.QuestEnums import QuestSource, QuestCollectable, QuestItemName
from toontown.quest3.base.QuestChain import QuestChain
from toontown.quest3.base.QuestHistory import QuestHistory
from toontown.quest3.base.QuestLine import QuestLine
from toontown.quest3.base.QuestObjective import MultiObjective
from toontown.quest3.base.QuestReference import QuestId, QuestReference
from toontown.quest3.rewards import *
from toontown.quest3.objectives import *
from toontown.toonbase import ToontownGlobals


class MainQuestLineContainer(QuestLine):
    questSource = QuestSource.MainQuest

    def getStarterQuestData(self, skipTutorial: bool):
        """
        Gets the starter quest data.
        """
        if not skipTutorial:
            # Get the starter quests, from the start of the toontorial.
            startingQuestRef = [
                QuestReference(
                    QuestId(
                        questSource=self.questSource,
                        chainId=1,
                        objectiveId=1,
                    )
                ).toStruct()
            ]
            startingQuestHistory = []
        else:
            # Skip the toontorial, and get the refs/quest history resulting.
            startingQuestRef = [
                QuestReference(
                    QuestId(
                        questSource=self.questSource,
                        chainId=3,
                        objectiveId=1,
                    )
                ).toStruct()
            ]
            startingQuestHistory = [
                QuestHistory(QuestSource.MainQuest, 1).toStruct(),
                QuestHistory(QuestSource.MainQuest, 2).toStruct(),
            ]
        return startingQuestRef, startingQuestHistory


MainQuestLine = MainQuestLineContainer(
    questLine={
        1: QuestChain(
            nextChain=2,
            rewards=(MaxQuestCarryReward(4)),
            steps={
                1: VisitObjective(npc=2001),
            }
        ),
        2: QuestChain(
            nextChain=3,
            rewards=(InventoryReward(BackgroundItemType.PG_TTC), ExpReward(45)),
            dynamicRewards=(ExpReward(45),),
            steps={
                1: VisitObjective(npc=(2001, 2007), rewards=BeanReward(20)),
                2: TrolleyObjective(npc=2007),
                3: DefeatCogObjective(npc=2007, cogCount=2, cogLocation=ToontownGlobals.ToontownCentral,
                                      nextStep=(4, 5, 6, 7, 8)),
                4: DefeatCogObjective(npc=2007, cogCount=3, cogTrack='s', nextStep=9),
                5: DefeatCogObjective(npc=2007, cogCount=3, cogTrack='m', nextStep=9),
                6: DefeatCogObjective(npc=2007, cogCount=3, cogTrack='l', nextStep=9),
                7: DefeatCogObjective(npc=2007, cogCount=3, cogTrack='c', nextStep=9),
                8: DefeatCogObjective(npc=2007, cogCount=3, cogTrack='g', nextStep=9),
                9: VisitObjective(npc=(2007, 2008)),
            }
        ),
        3: QuestChain(
            nextChain=4,
            rewards=(BeanReward(10), ExpReward(234)),
            dynamicRewards=(BeanReward(10), ExpReward(234)),
            steps={
                1: VisitObjective(npc=(2008, 2311)),
                2: RecoverFromCogObjective(npc=2311, cogLocation=ToontownGlobals.ToontownCentral,
                                           recoverItem=QuestItemName.ExerciseSupplies, recoverChance=0.8),
                3: DefeatCogObjective(npc=2311, cogCount=3, cogLocation=ToontownGlobals.ToontownCentral),
                4: VisitObjective(npc=(2311, 2008)),
            }
        ),
        4: QuestChain(
            nextChain=5,
            rewards=(BeanReward(15), ExpReward(260)),
            dynamicRewards=(BeanReward(15), ExpReward(260)),
            steps={
                1: VisitObjective(npc=(2008, 2126)),
                2: RecoverFromCogObjective(npc=2126, cogLocation=ToontownGlobals.ToontownCentral,
                                           recoverItem=QuestItemName.LaughingGas, recoverChance=0.75),
                3: VisitObjective(npc=(2126, 2118)),
                4: RecoverFromCogObjective(npc=2118, cogLocation=ToontownGlobals.ToontownCentral,
                                           recoverItem=QuestItemName.JokeRepairTools, recoverChance=0.65),
                5: DeliverObjective(npc=(2118, 2126), recoverItem=QuestItemName.JokeRepairTools),
                6: VisitObjective(npc=(2126, 2008)),
            }
        ),
        5: QuestChain(
            nextChain=6,
            rewards=(BeanReward(18), ExpReward(279)),
            dynamicRewards=(BeanReward(18), ExpReward(279)),
            steps={
                1: VisitObjective(npc=(2008, 2009)),
                2: VisitObjective(npc=(2009, 2208)),
                3: ObtainObjective(npc=(2208, 2134), recoverItem=QuestItemName.ReservationTicket),
                4: DeliverObjective(npc=(2134, 2208), recoverItem=QuestItemName.ReservationTicket),
                5: RecoverFromCogObjective(npc=2208, cogLocation=ToontownGlobals.ToontownCentral,
                                           recoverItem=QuestItemName.UnstickingObject, recoverChance=0.5),
                6: DeliverObjective(npc=(2208, 2009), recoverItem=QuestItemName.DecorativeGlue),
                7: VisitObjective(npc=(2009, 2208)),
                8: QuestFishObjective(npc=2208, fishType=QuestItemName.GlassJar, fishChance=1.0,
                                      fishLocation=ToontownGlobals.ToontownCentral),
                9: DeliverObjective(npc=(2208, 2009), recoverItem=QuestItemName.Glue),
            }
        ),
        6: QuestChain(
            nextChain=7,
            rewards=(BeanReward(20), ExpReward(280)),
            dynamicRewards=(BeanReward(20), ExpReward(280)),
            steps={
                1: VisitObjective(npc=(2009, 2010)),
                2: VisitObjective(npc=(2010, 2002)),
                3: RecoverFromCogObjective(npc=2002, cogLocation=ToontownGlobals.ToontownCentral, cogType='pp',
                                           recoverItem=QuestItemName.AddingMachine, recoverChance=0.6),
                4: VisitObjective(npc=(2002, 2408)),
                5: RecoverFromCogObjective(npc=2408, cogLocation=ToontownGlobals.ToontownCentral,
                                           recoverItem=QuestItemName.MachineParts, recoverChance=0.85,
                                           recoverRequired=3),
                6: DeliverObjective(npc=(2408, 2002), recoverItem=QuestItemName.AddingMachine),
                7: VisitObjective(npc=(2002, 2010)),
            }
        ),
        7: QuestChain(
            nextChain=8,
            rewards=(BeanReward(20), ExpReward(288)),
            dynamicRewards=(BeanReward(20), ExpReward(288)),
            steps={
                1: VisitObjective(npc=(2010, 2201)),
                2: RecoverFromCogObjective(npc=2201, cogLocation=ToontownGlobals.ToontownCentral, cogType='cc',
                                           recoverItem=QuestItemName.PapercutProofGloves, recoverChance=0.7,
                                           recoverRequired=2),
                3: RecoverFromCogObjective(npc=2201, cogLocation=ToontownGlobals.ToontownCentral, cogType='p',
                                           recoverItem=QuestItemName.MailPackage, recoverChance=0.7),
                4: DeliverObjective(npc=(2201, 2128), recoverItem=QuestItemName.MailPackage),
                5: QuestFishObjective(npc=2128, fishType=QuestItemName.ClownTires, fishCount=4, fishChance=1.0,
                                      fishLocation=ToontownGlobals.ToontownCentral),
                6: VisitObjective(npc=(2128, 2010)),
            }
        ),
        8: QuestChain(
            nextChain=9,
            rewards=(BeanReward(22), ExpReward(316)),
            dynamicRewards=(BeanReward(22), ExpReward(316)),
            steps={
                1: VisitObjective(npc=(2010, 2007)),
                2: VisitObjective(npc=(2007, 2324)),
                3: VisitObjective(npc=(2324, 2315)),
                4: DefeatCogObjective(npc=2315, cogCount=5, cogLevelMin=2, 
                                      cogLocation=ToontownGlobals.ToontownCentral),
                5: VisitObjective(npc=(2315, 2324)),
                6: VisitObjective(npc=(2324, 2316)),
                7: DefeatCogObjective(npc=2316, cogCount=2, cogLocation=ToontownGlobals.ToontownCentral, cogType='cn'),
                8: VisitObjective(npc=(2316, 2324)),
                9: VisitObjective(npc=(2324, 2219)),
                10: DefeatCogObjective(npc=2219, cogCount=4, cogLocation=ToontownGlobals.LoopyLane),
                11: DeliverObjective(npc=(2219, 2324), recoverItem=QuestItemName.BoxOfMeatballProduct),
                12: VisitObjective(npc=(2324, 2007)),
            }
        ),
        9: QuestChain(
            nextChain=10,
            rewards=(BeanReward(20), ExpReward(320)),
            dynamicRewards=(BeanReward(20), ExpReward(320)),
            steps={
                1: VisitObjective(npc=(2007, 2404)),
                2: DefeatCogObjective(npc=2404, cogCount=3, cogLocation=ToontownGlobals.WackyWay),
                3: VisitObjective(npc=(2404, 2007)),
                4: VisitObjective(npc=(2007, 2117)),
                5: RecoverFromCogObjective(npc=2117, cogLocation=ToontownGlobals.ToontownCentral, cogType='p',
                                           recoverItem=QuestItemName.PencilShavings, recoverChance=0.95,
                                           recoverRequired=3),
                6: VisitObjective(npc=(2117, 2007)),
                7: VisitObjective(npc=(2007, 2215)),
                8: RecoverFromCogObjective(npc=2215, cogLocation=ToontownGlobals.ToontownCentral,
                                           recoverItem=QuestItemName.Springs, recoverChance=0.85, recoverRequired=3),
                9: VisitObjective(npc=(2215, 2007)),
            }
        ),
        10: QuestChain(
            nextChain=11,
            rewards=(BeanReward(20), ExpReward(322)),
            dynamicRewards=(BeanReward(20), ExpReward(322)),
            steps={
                1: VisitObjective(npc=(2007, 2001)),
                2: VisitObjective(npc=(2001, 2301)),
                3: VisitObjective(npc=(2301, 2312)),
                4: ObtainObjective(npc=(2312, 2301), recoverItem=QuestItemName.LoveLetter),
                5: RecoverFromCogObjective(npc=2301, cogType='dt', recoverItem=QuestItemName.LoveLetter,
                                           recoverChance=0.9),
                6: QuestFishObjective(npc=2301, fishType=QuestItemName.SupplyOfInk, fishChance=1.0,
                                      fishLocation=ToontownGlobals.ToontownCentral),
                7: DeliverObjective(npc=(2301, 2312), recoverItem=QuestItemName.LoveLetter),
                8: VisitObjective(npc=(2312, 2001)),
            }
        ),
        11: QuestChain(
            nextChain=12,
            rewards=(InventoryReward(BackgroundItemType.PG_BB), BeanReward(22), ExpReward(332)),
            dynamicRewards=(BeanReward(22), ExpReward(332)),
            steps={
                1: VisitObjective(npc=(2001, 2007)),
                2: VisitObjective(npc=(2007, 2402)),
                3: VisitObjective(npc=(2402, 2403)),
                4: InvestigateObjective(npc=(2402, 2403), zoneId=ToontownGlobals.Gagsoline),
                5: RecoverFromCogObjective(npc=(2403, 2007), cogLocation=ToontownGlobals.ToontownCentral, cogTrack='c',
                                           recoverItem=QuestItemName.Keys, recoverChance=0.5,
                                           zoneUnlocks=[ToontownGlobals.Gagsoline]),
                6: InvestigateObjective(npc=2007, zoneId=ToontownGlobals.Gagsoline),
                7: DefeatCogObjective(npc=2007, cogLocation=ToontownGlobals.WackyWay, cogType='derrman', taskManagerBoss=True),
            }
        ),
    }
)
