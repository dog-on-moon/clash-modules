"""
This module contains the item data for fishing rods.
"""
from panda3d.core import NodePath

from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.base.ItemDefinition import ItemDefinition
from typing import Dict, Optional
from enum import IntEnum

from toontown.inventory.enums.ItemEnums import FishingRodItemType
from toontown.inventory.enums.ItemTags import ItemTag
from toontown.inventory.enums.RarityEnums import Rarity

from toontown.battle.attacks.base.AttackEnum import AttackEnum

# Higher numbers mean the rare fish are even more rare.
# Note - the rodSubtype is factored into the dice roll too. Now better rods
# will have an easier time catching more rare fish
GlobalRarityDialBase = 4.3


class FishingRodDefinition(ItemDefinition):
    """
    The definition structure for fishing rods.
    """

    def __init__(self,
                 modelPath,
                 fishRarityFactor,
                 castCost=1,
                 weightRange=(0, 4),
                 beanBountyAmount=10,
                 levelMinimum=0,
                 **kwargs):
        super().__init__(**kwargs)
        self.modelPath = modelPath
        # This is how much each rod changes the global rarity dice rolls.
        # These get multiplied into the GlobalRarityDialBase, thus making the rare fish less rare.
        # The rarity curve is controlled by this exponent in the dict below.
        # Making that value smaller (where 1/2 = square root, 1/3 = cube root, etc) will make
        # higher rarity levels even harder to find by making the curve steeper.
        self.fishRarityFactor = fishRarityFactor
        self.castCost = castCost
        self.weightRange = weightRange
        self.beanBountyAmount = beanBountyAmount
        self.levelMinimum = levelMinimum

    def getModelPath(self):
        return self.modelPath

    def getFishRarityFactor(self):
        return self.fishRarityFactor

    def getCastCost(self):
        return self.castCost

    def getWeightRange(self):
        return self.weightRange

    def getMinWeight(self):
        return self.getWeightRange()[0]

    def getMaxWeight(self):
        return self.getWeightRange()[1]

    def getBeanBountyAmount(self):
        return self.beanBountyAmount

    def getLevelMinimum(self):
        return self.levelMinimum

    def getItemTypeName(self):
        return 'Fishing Rod'

    def getTags(self, item: 'InventoryItem') -> set[ItemTag]:
        tags = super().getTags(item)
        tags.add(ItemTag.FishingRod)
        return tags

    def makeItemModel(self, item: Optional[InventoryItem] = None, *extraArgs) -> NodePath:
        """
        Returns a nodepath that represents this item.
        """
        model = loader.loadModel(self.getModelPath())
        return model

    def getItemTypeDescriptionInfo(self, item: Optional[InventoryItem] = None) -> str:
        returnStr = f"\1white\1\5icon_battleProp_{AttackEnum.TOON_DROP}_4\5\2 Weight Range: {self.getMinWeight()}-{self.getMaxWeight()} lbs.\n" \
            f"\1white\1\5reward_beanJarIcon\5\2 Cast Cost: {self.getCastCost()}\n" \
            f"\1white\1\5reward_beanJarIcon\5\2 Bean Bounty: {self.getBeanBountyAmount()}\n" \
            f"\1white\1\5reward_fishieIcon\5\2 Fishing Level Minimum: {self.getLevelMinimum()+1}"
        return returnStr


# The registry dictionary for fishing rods.
FishingRodRegistry: Dict[IntEnum, FishingRodDefinition] = {
    FishingRodItemType.Cardboard: FishingRodDefinition(
        name='Cardboard Fishing Rod',
        description='A flimsy fishing rod made from cardboard.',
        modelPath='phase_4/models/props/pole_plywood-mod',
        fishRarityFactor=1.0 / (GlobalRarityDialBase * 1),
        castCost=1,
        weightRange=(0, 4),
        beanBountyAmount=50,
        levelMinimum=0,
        rarity=Rarity.Common,
    ),
    FishingRodItemType.Twig: FishingRodDefinition(
        name='Twig Fishing Rod',
        description='A rough fishing rod made from the branches of a tree.',
        modelPath='phase_4/models/props/pole_treebranch-mod',
        fishRarityFactor=1.0 / (GlobalRarityDialBase * 0.975),
        castCost=2,
        weightRange=(1, 6),
        beanBountyAmount=100,
        levelMinimum=10-1,
        rarity=Rarity.Common,
    ),
    FishingRodItemType.Bamboo: FishingRodDefinition(
        name='Bamboo Fishing Rod',
        description='A sturdy fishing rod made from bamboo.',
        modelPath='phase_4/models/props/pole_bamboo-mod',
        fishRarityFactor=1.0 / (GlobalRarityDialBase * 0.95),
        castCost=3,
        weightRange=(2, 9),
        beanBountyAmount=175,
        levelMinimum=20-1,
        rarity=Rarity.Uncommon,
    ),
    FishingRodItemType.Hardwood: FishingRodDefinition(
        name='Hardwood Fishing Rod',
        description='A solid fishing rod made from harvested lumber.',
        modelPath='phase_4/models/props/pole_wood-mod',
        fishRarityFactor=1.0 / (GlobalRarityDialBase * 0.9),
        castCost=4,
        weightRange=(3, 12),
        beanBountyAmount=250,
        levelMinimum=30-1,
        rarity=Rarity.Uncommon,
    ),
    FishingRodItemType.Steel: FishingRodDefinition(
        name='Steel Fishing Rod',
        description='A reliable fishing rod made of steel.',
        modelPath='phase_4/models/props/pole_steel-mod',
        fishRarityFactor=1.0 / (GlobalRarityDialBase * 0.85),
        castCost=5,
        weightRange=(4, 15),
        beanBountyAmount=325,
        levelMinimum=40-1,
        rarity=Rarity.Rare,
    ),
    FishingRodItemType.Gold: FishingRodDefinition(
        name='Gold Fishing Rod',
        description='An elegant fishing rod made of gold.',
        modelPath='phase_4/models/props/pole_gold-mod',
        fishRarityFactor=1.0 / (GlobalRarityDialBase * 0.8),
        castCost=6,
        weightRange=(5, 18),
        beanBountyAmount=400,
        levelMinimum=50-1,
        rarity=Rarity.Rare,
    ),
    FishingRodItemType.Platinum: FishingRodDefinition(
        name='Platinum Fishing Rod',
        description='An exquisite fishing rod made of platinum.',
        modelPath='phase_4/models/props/pole_platinum-mod',
        fishRarityFactor=1.0 / (GlobalRarityDialBase * 0.75),
        castCost=7,
        weightRange=(6, 20),
        beanBountyAmount=500,
        levelMinimum=60-1,
        rarity=Rarity.VeryRare,
    ),
}
