"""
This module contains the item data for profile backgrounds.
"""
from panda3d.core import NodePath

from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.base.ItemDefinition import ItemDefinition
from typing import Dict, Optional
from enum import IntEnum

from toontown.inventory.enums.ItemEnums import BackgroundItemType
from toontown.inventory.enums.RarityEnums import Rarity
from toontown.toonbase import ProcessGlobals, ToontownGlobals


class ProfileBackgroundDefinition(ItemDefinition):
    """
    The definition structure for profile backgrounds.
    """
    # Need to pre-load the model, or hammerspace item previews get very laggy
    if ProcessGlobals.getCurrentProcess() == ProcessGlobals.Process.Client:
        model = loader.loadModelRaw('phase_3.5/models/gui/profile/background')

    def __init__(self,
                 modelPath: str,
                 **kwargs):
        super().__init__(**kwargs)
        self.modelPath = modelPath

    def getModelPath(self) -> str:
        return self.modelPath

    def getItemTypeName(self):
        return 'Profile Background'

    def getRewardName(self, item: Optional[InventoryItem] = None):
        return f'{self.getName()} Profile Background'

    def makeItemModel(self, item: Optional[InventoryItem] = None, *extraArgs) -> NodePath:
        """
        Returns a nodepath that represents this item.
        """
        background = NodePath('background')
        background = self.model.find(self.getModelPath()).copyTo(background)
        return background


# A dictionary mapping various zones to different background item types.
ZoneToProfileBackground: Dict[int, BackgroundItemType] = {
    ToontownGlobals.ToontownCentral:    BackgroundItemType.PG_Sky_TTC,
    ToontownGlobals.DonaldsDock:        BackgroundItemType.PG_Sky_BB,
    ToontownGlobals.OldeToontown:       BackgroundItemType.PG_Sky_YOTT,
    ToontownGlobals.DaisyGardens:       BackgroundItemType.PG_Sky_DG,
    ToontownGlobals.MinniesMelodyland:  BackgroundItemType.PG_Sky_MML,
    ToontownGlobals.TheBrrrgh:          BackgroundItemType.PG_Sky_TB,
    ToontownGlobals.OutdoorZone:        BackgroundItemType.PG_Sky_AA,
    ToontownGlobals.DonaldsDreamland:   BackgroundItemType.PG_Sky_DDL,
}


# The registry dictionary for profile backgrounds.
ProfileBackgroundRegistry: Dict[IntEnum, ProfileBackgroundDefinition] = {
    ### Default ###
    BackgroundItemType.Default: ProfileBackgroundDefinition(
        name='Default',
        description='The default background for your Toon Profile.',
        modelPath='**/default',
    ),

    ### Sky Backgrounds ###
    BackgroundItemType.PG_Sky_TTC: ProfileBackgroundDefinition(
        name='Toontown Central Sky',
        description='Present your Toon Profile with the skies of Toontown Central.',
        rarity=Rarity.Common,
        modelPath='**/hidden_sky_ttc',
    ),
    BackgroundItemType.PG_Sky_BB: ProfileBackgroundDefinition(
        name='Barnacle Boatyard Sky',
        description='Present your Toon Profile with the skies of Barnacle Boatyard.',
        rarity=Rarity.Common,
        modelPath='**/hidden_sky_bb',
    ),
    BackgroundItemType.PG_Sky_YOTT: ProfileBackgroundDefinition(
        name='Ye Olde Toontowne Sky',
        description='Present your Toon Profile with the skies of Ye Olde Toontowne.',
        rarity=Rarity.Common,
        modelPath='**/hidden_sky_ttc',
    ),
    BackgroundItemType.PG_Sky_DG: ProfileBackgroundDefinition(
        name='Daffodil Gardens Sky',
        description='Present your Toon Profile with the skies of Daffodil Gardens.',
        rarity=Rarity.Common,
        modelPath='**/hidden_sky_dg',
    ),
    BackgroundItemType.PG_Sky_MML: ProfileBackgroundDefinition(
        name='Mezzo Melodyland Sky',
        description='Present your Toon Profile with the skies of Mezzo Melodyland.',
        rarity=Rarity.Common,
        modelPath='**/hidden_sky_mml',
    ),
    BackgroundItemType.PG_Sky_TB: ProfileBackgroundDefinition(
        name='The Brrrgh Sky',
        description='Present your Toon Profile with the skies of The Brrrgh.',
        rarity=Rarity.Common,
        modelPath='**/hidden_sky_tb',
    ),
    BackgroundItemType.PG_Sky_AA: ProfileBackgroundDefinition(
        name='Acorn Acres Sky',
        description='Present your Toon Profile with the skies of Acorn Acres.',
        rarity=Rarity.Common,
        modelPath='**/hidden_sky_aa',
    ),
    BackgroundItemType.PG_Sky_DDL: ProfileBackgroundDefinition(
        name='Drowsy Dreamland Sky',
        description='Present your Toon Profile with the skies of Drowsy Dreamland.',
        rarity=Rarity.Common,
        modelPath='**/hidden_sky_ddl',
    ),
    
    ### Regular PG Backgrounds ###
    BackgroundItemType.PG_TTC: ProfileBackgroundDefinition(
        name='Toontown Central',
        description='Present your Toon Profile with Toontown Central.',
        rarity=Rarity.Common,
        modelPath='**/hidden_pg_ttc',
    ),
    BackgroundItemType.PG_BB: ProfileBackgroundDefinition(
        name='Barnacle Boatyard',
        description='Present your Toon Profile with Barnacle Boatyard.',
        rarity=Rarity.Common,
        modelPath='**/hidden_pg_bb',
    ),
    BackgroundItemType.PG_YOTT: ProfileBackgroundDefinition(
        name='Ye Olde Toontowne',
        description='Present your Toon Profile with Ye Olde Toontowne.',
        rarity=Rarity.Common,
        modelPath='**/hidden_pg_ttc',
    ),
    BackgroundItemType.PG_DG: ProfileBackgroundDefinition(
        name='Daffodil Gardens',
        description='Present your Toon Profile with Daffodil Gardens.',
        rarity=Rarity.Common,
        modelPath='**/hidden_pg_dg',
    ),
    BackgroundItemType.PG_MML: ProfileBackgroundDefinition(
        name='Mezzo Melodyland',
        description='Present your Toon Profile with Mezzo Melodyland.',
        rarity=Rarity.Common,
        modelPath='**/hidden_pg_mml',
    ),
    BackgroundItemType.PG_TB: ProfileBackgroundDefinition(
        name='The Brrrgh',
        description='Present your Toon Profile with The Brrrgh.',
        rarity=Rarity.Common,
        modelPath='**/hidden_pg_tb',
    ),
    BackgroundItemType.PG_AA: ProfileBackgroundDefinition(
        name='Acorn Acres',
        description='Present your Toon Profile with Acorn Acres.',
        rarity=Rarity.Common,
        modelPath='**/hidden_pg_aa',
    ),
    BackgroundItemType.PG_DDL: ProfileBackgroundDefinition(
        name='Drowsy Dreamland',
        description='Present your Toon Profile with Drowsy Dreamland.',
        rarity=Rarity.Common,
        modelPath='**/hidden_pg_ddl',
    ),

    ### HQS ###
    BackgroundItemType.HQ_Sellbot: ProfileBackgroundDefinition(
        name='Sellbot HQ',
        description='Present your Toon Profile with Sellbot HQ.',
        rarity=Rarity.Uncommon,
        modelPath='**/hidden_hq_sbhq',
    ),
    BackgroundItemType.HQ_Cashbot: ProfileBackgroundDefinition(
        name='Cashbot HQ',
        description='Present your Toon Profile with Cashbot HQ.',
        rarity=Rarity.Uncommon,
        modelPath='**/hidden_hq_cbhq',
    ),
    BackgroundItemType.HQ_Lawbot: ProfileBackgroundDefinition(
        name='Lawbot HQ',
        description='Present your Toon Profile with Lawbot HQ.',
        rarity=Rarity.Uncommon,
        modelPath='**/hidden_hq_lbhq',
    ),
    BackgroundItemType.HQ_Bossbot: ProfileBackgroundDefinition(
        name='Bossbot HQ',
        description='Present your Toon Profile with Bossbot HQ.',
        rarity=Rarity.Uncommon,
        modelPath='**/hidden_hq_bbhq',
    ),
    BackgroundItemType.HQ_Boardbot: ProfileBackgroundDefinition(
        name='Boardbot HQ',
        description='Present your Toon Profile with Boardbot HQ.',
        rarity=Rarity.Uncommon,
        modelPath='**/hidden_hq_bdhq',
    ),

    ### ACTIVITIES ###
    BackgroundItemType.Activity_Fishing: ProfileBackgroundDefinition(
        name='Aquarium',
        description='Let your Toon sleep with the fishes!\nObtained through fishing.',
        rarity=Rarity.Common,
        modelPath='**/hidden_aqua_fish',
    ),
    BackgroundItemType.Activity_Golfing: ProfileBackgroundDefinition(
        name='Golfing',
        description='Hole in one!\nObtained after playing golf.',
        rarity=Rarity.Common,
        modelPath='**/hidden_golfing',
    ),
    BackgroundItemType.Activity_Racing: ProfileBackgroundDefinition(
        name='Chequered Flag',
        description='Ready, set, go!\nObtained after participating in a race.',
        rarity=Rarity.Common,
        modelPath='**/hidden_racing',
    ),
    BackgroundItemType.Activity_Trolley: ProfileBackgroundDefinition(
        name='Jellybeans',
        description='Money, money, money!\nObtained after playing a Trolley Game.',
        rarity=Rarity.Common,
        modelPath='**/hidden_trolley',
    ),

    ### TASKS ###
    BackgroundItemType.Tasks_Judy: ProfileBackgroundDefinition(
        name='R.I.D.D.L.E.',
        description='Five across, ten down...\nObtained after completing the "Crossword Crisis" directive.',
        rarity=Rarity.Rare,
        modelPath='**/sidetask_judy',
    ),

    ### EVENT ###
    BackgroundItemType.Event_Winter2018_A: ProfileBackgroundDefinition(
        name='Winter Cabin',
        description='Obtained through playing Present Thief in Toonseltown.',
        rarity=Rarity.Event,
        modelPath='**/event_winter_cabin',
    ),
    BackgroundItemType.Event_Winter2018_B: ProfileBackgroundDefinition(
        name='Fireplace',
        description='Obtained through completing Toonseltown tasks.',
        rarity=Rarity.Event,
        modelPath='**/event_winter_fireplace',
    ),
    BackgroundItemType.Event_NewYears2019: ProfileBackgroundDefinition(
        name='New Years 2019 Fireworks',
        description='Obtained during the New Years 2019 event.',
        rarity=Rarity.Event,
        modelPath='**/event_2019',
    ),
    BackgroundItemType.Event_SkyClan: ProfileBackgroundDefinition(
        name='Sky Clan',
        description='Obtained during the April Toons 2020 event.',
        rarity=Rarity.Event,
        modelPath='**/event_skyclan',
    ),
    BackgroundItemType.Event_Outback: ProfileBackgroundDefinition(
        name='Outback',
        description='Watch out for Kangaroos!',
        rarity=Rarity.Event,
        modelPath='**/event_outback',
    ),
    BackgroundItemType.Event_GoldenCorridor: ProfileBackgroundDefinition(
        name='The Golden Corridor',
        description='Obtained through defeating someone unimportant.',
        rarity=Rarity.Event,
        modelPath='**/event_golden_corridor',
    ),
    BackgroundItemType.Event_NewYears2020: ProfileBackgroundDefinition(
        name='New Years 2020 Fireworks',
        description='Obtained during the New Years 2020 event.',
        rarity=Rarity.Event,
        modelPath='**/event_2020',
    ),
    BackgroundItemType.Event_BTL: ProfileBackgroundDefinition(
        name='Break the Law!',
        description='Obtained during the Break the Law event.',
        rarity=Rarity.Event,
        modelPath='**/event_btl',
    ),
    BackgroundItemType.Event_Valentines2020: ProfileBackgroundDefinition(
        name='Valentine\'s 2020',
        description='Obtained during the Valentine\'s 2020 event.',
        rarity=Rarity.Event,
        modelPath='**/event_valentines',
    ),
    BackgroundItemType.Event_Easter2020: ProfileBackgroundDefinition(
        name='Easter 2020',
        description='Obtained during the Easter 2020 event.',
        rarity=Rarity.Event,
        modelPath='**/event_easter2020',
    ),
    BackgroundItemType.Event_StandIn: ProfileBackgroundDefinition(
        name='Artificial Progeny',
        description='Obtained after defeating the Witness Stand-In.',
        rarity=Rarity.VeryRare,
        modelPath='**/event_standin',
    ),
    BackgroundItemType.Event_FourthJuly2020: ProfileBackgroundDefinition(
        name='Fireworks Show',
        description='Obtained during the Fourth of July 2020 event.',
        rarity=Rarity.Event,
        modelPath='**/firework_background',
    ),
    BackgroundItemType.Event_Halloween2020: ProfileBackgroundDefinition(
        name='Halloween Town',
        description='Obtained during the Halloween 2020 event.',
        rarity=Rarity.Event,
        modelPath='**/event_halloween_town',
    ),
    BackgroundItemType.Event_Electric: ProfileBackgroundDefinition(
        name='Electric',
        description='Obtained by doing something cool probably.',
        rarity=Rarity.Event,
        modelPath='**/event_electric',
    ),

    ### SPECIAL ###
    BackgroundItemType.Special_PaintMixer: ProfileBackgroundDefinition(
        name='Paint Mixer',
        description='Obtained by defeating 5 Unstable Cogs during the Maypril Toons 2023 event.',
        rarity=Rarity.Event,
        modelPath='**/hidden_ocftf',
    ),

    ### KUDOS ###
    BackgroundItemType.Kudos_TTC: ProfileBackgroundDefinition(
        name='Congratulations',
        description='It\'s all thanks to you.\nObtained upon reaching Rank 4 in Toontown Central Kudos.',
        rarity=Rarity.Uncommon,
        modelPath='**/kudos_ttc',
    ),
    BackgroundItemType.Kudos_BB: ProfileBackgroundDefinition(
        name='On the Dock',
        description='Wow, it\'s like you\'re really there!\nObtained upon reaching Rank 4 in Barnacle Boatyard Kudos.',
        rarity=Rarity.Uncommon,
        modelPath='**/kudos_bb',
    ),
    BackgroundItemType.Kudos_YOTT: ProfileBackgroundDefinition(
        name='Hearty Feast',
        description='Tonight, we feast.\nObtained upon reaching Rank 4 in Ye Olde Toontowne Kudos.',
        rarity=Rarity.Uncommon,
        modelPath='**/kudos_yott',
    ),
    BackgroundItemType.Kudos_DG: ProfileBackgroundDefinition(
        name='Tranquil Fountain',
        description='An exotic-aquatic display.\nObtained upon reaching Rank 4 in Daffodil Gardens Kudos.',
        rarity=Rarity.Uncommon,
        modelPath='**/kudos_dg',
    ),
    BackgroundItemType.Kudos_MML: ProfileBackgroundDefinition(
        name='Rock Concert',
        description='You HAD to be there.\nObtained upon reaching Rank 4 in Mezzo Melodyland Kudos.',
        rarity=Rarity.Uncommon,
        modelPath='**/kudos_mml',
    ),
    BackgroundItemType.Kudos_TB: ProfileBackgroundDefinition(
        name='Doodlesledding',
        description='A characteristically adorable means of transportation.\nObtained upon reaching Rank 4 in The Brrrgh Kudos.',
        rarity=Rarity.Uncommon,
        modelPath='**/kudos_tb',
    ),
    BackgroundItemType.Kudos_AA: ProfileBackgroundDefinition(
        name='Light Show',
        description='The party never stops!\nObtained upon reaching Rank 4 in Acorn Acres Kudos.',
        rarity=Rarity.Uncommon,
        modelPath='**/kudos_aa',
    ),
    BackgroundItemType.Kudos_DDL: ProfileBackgroundDefinition(
        name='Sweet',
        description='Sweet treats are made of these.\nObtained upon reaching Rank 4 in Drowsy Dreamland Kudos.',
        rarity=Rarity.Uncommon,
        modelPath='**/kudos_ddl',
    ),
}
