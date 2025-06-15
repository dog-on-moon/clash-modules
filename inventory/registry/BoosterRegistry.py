"""
This module contains the item data for estate styles.
"""
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import NodePath

from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.base.ItemDefinition import ItemDefinition
from typing import Dict, Optional
from enum import IntEnum, auto

from toontown.inventory.enums.ItemEnums import BoosterItemType


AllStarBoosts: list[BoosterItemType] = [
    BoosterItemType.Exp_Gags_Power,
    BoosterItemType.Jellybeans_Global,
    BoosterItemType.Merit_Global,
    BoosterItemType.Reward_Boss_Global,
    BoosterItemType.Exp_Dept_Global,
]
BossRewardBoosts: list[BoosterItemType] = [
    BoosterItemType.Reward_Boss_Sellbot,
    BoosterItemType.Reward_Boss_Cashbot,
    BoosterItemType.Reward_Boss_Lawbot,
    BoosterItemType.Reward_Boss_Bossbot,
    BoosterItemType.Reward_Boss_Boardbot,
]


class BoostMode(IntEnum):
    ADDITIVE = auto()                      # +a,  boost gets flat increase
    ADDITIVE_MULTIPLICATIVE_PERC = auto()  # +a%, boost gets multiplicative increase, stacks additively
    ADDITIVE_MULT = auto()                 # +ax, boost gets flat increase
    MULTIPLICATIVE = auto()                # +ax, boost gets multiplicative increase, stacks multiplicatively

    # Special Cases
    GLOBAL_BOSS_REWARDS = auto()
    ALL_STAR = auto()
    RANDOM = auto()


class BoosterDefinition(ItemDefinition):
    """
    The definition structure for boosters.
    """

    def __init__(self,
                 texturePath: str,
                 boostAmount: int | float,
                 boostMode: BoostMode,
                 randomWeight: float,
                 **kwargs):
        super().__init__(**kwargs)
        self.texturePath = texturePath
        self.boostAmount = boostAmount
        self.boostMode = boostMode
        self.randomWeight = randomWeight

    def getDescription(self) -> str:
        return self.formatBoosterText('This gumball grants {boost}{duration}.')

    def getBoostText(self, cullNewLines: bool = False) -> str:
        text = self.description.format(boost=self.getBoostSubtext())
        if cullNewLines:
            text = text.replace('\n', ', ')
        return text

    def getBoostSubtext(self):
        if self.getBoostMode() == BoostMode.ADDITIVE:
            return f'+{round(self.getBoostAmount())}'
        elif self.getBoostMode() == BoostMode.ADDITIVE_MULTIPLICATIVE_PERC:
            return f'+{round(self.getBoostAmount() * 100)}%'
        elif self.getBoostMode() == BoostMode.ADDITIVE_MULT:
            return f'+{self.getBoostAmount()}x'
        elif self.getBoostMode() == BoostMode.MULTIPLICATIVE:
            return f'x{self.getBoostAmount()}'
        elif self.getBoostMode() == BoostMode.ALL_STAR:
            return '\n'.join([
                BoosterRegistry[itemType].getBoostSubtext()
                for itemType in AllStarBoosts
            ])
        else:
            return f'{self.getBoostAmount()}'

    def getDurationText(self) -> str:
        return ' for 2 hours'

    def formatBoosterText(self, s: str) -> str:
        return s.format(boost=self.getBoostText(cullNewLines=True), duration=self.getDurationText())

    def getRandomWeight(self) -> float:
        return self.randomWeight

    def getBoostMode(self) -> BoostMode:
        return self.boostMode

    def getBoostAmount(self) -> int | float:
        return self.boostAmount

    def getItemTypeName(self):
        return 'Booster'

    def makeItemModel(self, item: Optional[InventoryItem] = None, *extraArgs) -> NodePath:
        from toontown.gui.OnscreenBooster import OnscreenBooster
        model = OnscreenImage(image=OnscreenBooster.getBoosterImage(self.itemSubtype))
        return model


# The registry dictionary for boosters.
BoosterRegistry: Dict[BoosterItemType, BoosterDefinition] = {

    ### Jellybeans ###

    BoosterItemType.Jellybeans_Global: BoosterDefinition(
        name='Jellybean Booster',
        description='{boost} Jellybeans',
        texturePath='jellybean2',
        boostAmount=0.25,
        boostMode=BoostMode.ADDITIVE_MULTIPLICATIVE_PERC,
        randomWeight=1.0,
    ),
    BoosterItemType.Jellybeans_Bingo: BoosterDefinition(
        name='Fish Bingo Booster',
        description='{boost} Jellybeans from Fish Bingo',
        texturePath='jellybean2',
        boostAmount=2,
        boostMode=BoostMode.MULTIPLICATIVE,
        randomWeight=0.0,
    ),

    ### Gumballs ###

    BoosterItemType.Gumballs_Global: BoosterDefinition(
        name='Gumball Booster',
        description='{boost} Gumballs',
        texturePath='mainwashere',
        boostAmount=2,
        boostMode=BoostMode.MULTIPLICATIVE,
        randomWeight=0.0,
    ),

    ### Gag Boosters ###

    BoosterItemType.Exp_Gags_Global: BoosterDefinition(
        name='Universal Gag Booster',
        description='{boost} Gag Experience',
        texturePath='gag_all',
        boostAmount=1,
        boostMode=BoostMode.ADDITIVE_MULT,
        randomWeight=0.5,
    ),
    BoosterItemType.Exp_Gags_Support: BoosterDefinition(
        name='Support Gag Booster',
        description='{boost} Gag Experience for Squirt, Sound, Toon-Up and Lure',
        texturePath='gag_support',
        boostAmount=1,
        boostMode=BoostMode.ADDITIVE_MULT,
        randomWeight=1.0,
    ),
    BoosterItemType.Exp_Gags_Power: BoosterDefinition(
        name='Power Gag Booster',
        description='{boost} Gag Experience for Trap, Zap, Throw, and Drop',
        texturePath='gag_power',
        boostAmount=1,
        boostMode=BoostMode.ADDITIVE_MULT,
        randomWeight=1.0,
    ),

    ### Activity Experience ###

    BoosterItemType.Exp_Activity_Global: BoosterDefinition(
        name='Activity XP Booster',
        description='{boost} Activity Experience',
        texturePath='jellybean',
        boostAmount=0.25,
        boostMode=BoostMode.ADDITIVE_MULTIPLICATIVE_PERC,
        randomWeight=0.5,
    ),
    BoosterItemType.Exp_Activity_Racing: BoosterDefinition(
        name='Racing XP Booster',
        description='{boost} Racing Experience',
        texturePath='racing',
        boostAmount=0.25,
        boostMode=BoostMode.ADDITIVE_MULTIPLICATIVE_PERC,
        randomWeight=1.0,
    ),
    BoosterItemType.Exp_Activity_Trolley: BoosterDefinition(
        name='Trolley XP Booster',
        description='{boost} Trolley Experience',
        texturePath='trolley',
        boostAmount=0.25,
        boostMode=BoostMode.ADDITIVE_MULTIPLICATIVE_PERC,
        randomWeight=1.0,
    ),
    BoosterItemType.Exp_Activity_Golf: BoosterDefinition(
        name='Golf XP Booster',
        description='{boost} Golf Experience',
        texturePath='golf',
        boostAmount=0.25,
        boostMode=BoostMode.ADDITIVE_MULTIPLICATIVE_PERC,
        randomWeight=1.0,
    ),
    BoosterItemType.Exp_Activity_Fishing: BoosterDefinition(
        name='Fishing XP Booster',
        description='{boost} Fishing Experience',
        texturePath='fishing',
        boostAmount=0.25,
        boostMode=BoostMode.ADDITIVE_MULTIPLICATIVE_PERC,
        randomWeight=1.0,
    ),

    ### Fishing ###

    BoosterItemType.Fish_Rarity: BoosterDefinition(
        name='Fish Rarity Booster',
        description='{boost} Fish Rarity',
        texturePath='fishing',
        boostAmount=0.5,
        boostMode=BoostMode.ADDITIVE,
        randomWeight=0.0,
    ),

    ### Merits ###

    BoosterItemType.Merit_Global: BoosterDefinition(
        name='Universal Merit Booster',
        description='{boost} to all Merits',
        texturePath='merit',
        boostAmount=0.25,
        boostMode=BoostMode.ADDITIVE_MULTIPLICATIVE_PERC,
        randomWeight=0.5,
    ),
    BoosterItemType.Merit_Sellbot: BoosterDefinition(
        name='Invoice Booster',
        description='{boost} Invoices',
        texturePath='merit_sell',
        boostAmount=0.25,
        boostMode=BoostMode.ADDITIVE_MULTIPLICATIVE_PERC,
        randomWeight=0.5,
    ),
    BoosterItemType.Merit_Cashbot: BoosterDefinition(
        name='Cogbuck Booster',
        description='{boost} Cogbucks',
        texturePath='merit_cash',
        boostAmount=0.25,
        boostMode=BoostMode.ADDITIVE_MULTIPLICATIVE_PERC,
        randomWeight=0.5,
    ),
    BoosterItemType.Merit_Lawbot: BoosterDefinition(
        name='Patent Booster',
        description='{boost} Patents',
        texturePath='merit_law',
        boostAmount=0.25,
        boostMode=BoostMode.ADDITIVE_MULTIPLICATIVE_PERC,
        randomWeight=0.5,
    ),
    BoosterItemType.Merit_Bossbot: BoosterDefinition(
        name='Stock Option Booster',
        description='{boost} Stock Options',
        texturePath='merit_boss',
        boostAmount=0.25,
        boostMode=BoostMode.ADDITIVE_MULTIPLICATIVE_PERC,
        randomWeight=0.5,
    ),
    BoosterItemType.Merit_Boardbot: BoosterDefinition(
        name='Boardbot Merit Booster',
        description='+20 Charisma, +30 Chutzpah',
        texturePath='merit_board',
        boostAmount=0.25,
        boostMode=BoostMode.ADDITIVE_MULTIPLICATIVE_PERC,
        randomWeight=0.5,
    ),

    ### Department Experience ###

    BoosterItemType.Exp_Dept_Global: BoosterDefinition(
        name='Department XP Booster',
        description='{boost} Department XP',
        texturePath='cog',
        boostAmount=0.25,
        boostMode=BoostMode.ADDITIVE_MULTIPLICATIVE_PERC,
        randomWeight=0.5,
    ),
    BoosterItemType.Exp_Dept_Sellbot: BoosterDefinition(
        name='Sellbot XP Booster',
        description='{boost} Sellbot Department XP',
        texturePath='sellbot',
        boostAmount=0.25,
        boostMode=BoostMode.ADDITIVE_MULTIPLICATIVE_PERC,
        randomWeight=0.5,
    ),
    BoosterItemType.Exp_Dept_Cashbot: BoosterDefinition(
        name='Cashbot XP Booster',
        description='{boost} Cashbot Department XP',
        texturePath='cashbot',
        boostAmount=0.25,
        boostMode=BoostMode.ADDITIVE_MULTIPLICATIVE_PERC,
        randomWeight=0.5,
    ),
    BoosterItemType.Exp_Dept_Lawbot: BoosterDefinition(
        name='Lawbot XP Booster',
        description='{boost} Lawbot Department XP',
        texturePath='lawbot',
        boostAmount=0.25,
        boostMode=BoostMode.ADDITIVE_MULTIPLICATIVE_PERC,
        randomWeight=0.5,
    ),
    BoosterItemType.Exp_Dept_Bossbot: BoosterDefinition(
        name='Bossbot XP Booster',
        description='{boost} Bossbot Department XP',
        texturePath='bossbot',
        boostAmount=0.25,
        boostMode=BoostMode.ADDITIVE_MULTIPLICATIVE_PERC,
        randomWeight=0.5,
    ),
    BoosterItemType.Exp_Dept_Boardbot: BoosterDefinition(
        name='Boardbot XP Booster',
        description='{boost} Boardbot Department XP',
        texturePath='boardbot',
        boostAmount=0.25,
        boostMode=BoostMode.ADDITIVE_MULTIPLICATIVE_PERC,
        randomWeight=0.5,
    ),

    ### Boss Rewards ###

    BoosterItemType.Reward_Boss_Global: BoosterDefinition(
        name='Boss Reward Booster',
        description='+1 Boss Rewards (Excluding Unites)',
        texturePath='eyes',
        boostAmount=1,
        boostMode=BoostMode.GLOBAL_BOSS_REWARDS,
        randomWeight=0.5,
    ),
    BoosterItemType.Reward_Boss_Sellbot: BoosterDefinition(
        name='V.P. Reward Booster',
        description='{boost} IOU from the V.P.',
        texturePath='sellboss',
        boostAmount=1,
        boostMode=BoostMode.ADDITIVE,
        randomWeight=1.0,
    ),
    BoosterItemType.Reward_Boss_Cashbot: BoosterDefinition(
        name='C.F.O. Reward Booster',
        description='{boost} Counterfeits from the C.F.O.',
        texturePath='cashboss',
        boostAmount=1,
        boostMode=BoostMode.ADDITIVE,
        randomWeight=1.0,
    ),
    BoosterItemType.Reward_Boss_Lawbot: BoosterDefinition(
        name='C.L.O. Reward Booster',
        description='{boost} Cease and Desists from the C.L.O.',
        texturePath='lawboss',
        boostAmount=1,
        boostMode=BoostMode.ADDITIVE,
        randomWeight=1.0,
    ),
    BoosterItemType.Reward_Boss_Bossbot: BoosterDefinition(
        name='C.E.O. Reward Booster',
        description='{boost} Pink Slips from the C.E.O.',
        texturePath='bossboss',
        boostAmount=1,
        boostMode=BoostMode.ADDITIVE,
        randomWeight=1.0,
    ),
    BoosterItemType.Reward_Boss_Boardbot: BoosterDefinition(
        name='Boardbot Reward Booster',
        description='Please drink more water',
        texturePath='boardboss',
        boostAmount=1,
        boostMode=BoostMode.ADDITIVE,
        randomWeight=1.0,
    ),

    ### Special ###

    BoosterItemType.AllStar: BoosterDefinition(
        name='All-Star Booster',
        description='{boost}',
        texturePath='mainwashere',
        boostAmount=1,
        boostMode=BoostMode.ALL_STAR,
        randomWeight=0.4,
    ),
    BoosterItemType.Random: BoosterDefinition(
        name='Random Booster',
        description='It could be anything!',
        texturePath='random',
        boostAmount=1,
        boostMode=BoostMode.RANDOM,
        randomWeight=0.4,
    ),
}
