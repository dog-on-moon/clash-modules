"""
This module contains the item data for profile nameplates.
"""
from panda3d.core import NodePath

from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.base.ItemDefinition import ItemDefinition
from typing import Dict, Optional
from enum import IntEnum

from toontown.inventory.enums.ItemEnums import NameplateItemType
from toontown.inventory.enums.RarityEnums import Rarity
from toontown.toonbase import ToontownGlobals, ProcessGlobals


class ProfileNameplateDefinition(ItemDefinition):
    """
    The definition structure for profile nameplates.
    """
    # Need to pre-load the model, or hammerspace item previews get very laggy
    if ProcessGlobals.getCurrentProcess() == ProcessGlobals.Process.Client:
        model = loader.loadModelRaw('phase_3.5/models/gui/profile/nameplates')

    def __init__(self,
                 modelPath: str,
                 scale: tuple = (1.0, 1.0, 1.0),
                 position: tuple = (0, 0, 0.13),
                 **kwargs):
        super().__init__(**kwargs)
        self.modelPath = modelPath
        self.scale = scale
        self.position = position

    def getModelPath(self) -> str:
        return self.modelPath

    def getScale(self) -> tuple:
        return self.scale

    def getPosition(self) -> tuple:
        return self.position

    def getItemTypeName(self):
        return 'Profile Nameplate'

    def getRewardName(self, item: Optional[InventoryItem] = None):
        return f'{self.getName()} Profile Nameplate'

    def makeItemModel(self, item: Optional[InventoryItem] = None, *extraArgs) -> NodePath:
        """
        Returns a nodepath that represents this item.
        """
        nameplate = NodePath('nameplate')
        nameplate = self.model.find(self.getModelPath()).copyTo(nameplate)
        nameplate.setScale((self.getScale()[0], 1, self.getScale()[2]))
        return nameplate


# The registry dictionary for profile backgrounds.
ProfileNameplateRegistry: Dict[IntEnum, ProfileNameplateDefinition] = {
    ### Defaults ###
    NameplateItemType.DefaultBlue: ProfileNameplateDefinition(
        name='Default Blue',
        description='The default nameplate for your Toon Profile, but in blue.',
        modelPath='**/default_med_blue',
    ),
    NameplateItemType.DefaultGreen: ProfileNameplateDefinition(
        name='Default Green',
        description='The default nameplate for your Toon Profile, but in green.',
        modelPath='**/default_green',
    ),
    NameplateItemType.DefaultPurple: ProfileNameplateDefinition(
        name='Default Purple',
        description='The default nameplate for your Toon Profile, but in purple.',
        modelPath='**/default_purple',
    ),
    NameplateItemType.DefaultRed: ProfileNameplateDefinition(
        name='Default Red',
        description='The default nameplate for your Toon Profile, but in red.',
        modelPath='**/default_red',
    ),
    NameplateItemType.DefaultYellow: ProfileNameplateDefinition(
        name='Default Yellow',
        description='The default nameplate for your Toon Profile, but in yellow.',
        modelPath='**/default_yellow',
    ),
    NameplateItemType.DefaultOrange: ProfileNameplateDefinition(
        name='Default Orange',
        description='The default nameplate for your Toon Profile, but in orange.',
        modelPath='**/default_orange',
    ),
    NameplateItemType.DefaultBlueB: ProfileNameplateDefinition(
        name='Default Blue',
        description='The default nameplate for your Toon Profile, but in blue.',
        modelPath='**/default_blue',
    ),
    NameplateItemType.DefaultDarkBlue: ProfileNameplateDefinition(
        name='Default Dark Blue',
        description='The default nameplate for your Toon Profile, but in dark blue.',
        modelPath='**/default_dark_blue',
    ),
    NameplateItemType.DefaultDarkGreen: ProfileNameplateDefinition(
        name='Default Dark Green',
        description='The default nameplate for your Toon Profile, but in dark green.',
        modelPath='**/default_dark_green',
    ),

    ### Hidden Playground nameplates ###
    NameplateItemType.PG_TTC: ProfileNameplateDefinition(
        name='Toontown Central',
        description='A hidden nameplate from Toontown Central.',
        modelPath='**/hidden_pg_ttc',
    ),
    NameplateItemType.PG_BB: ProfileNameplateDefinition(
        name='Barnacle Boatyard',
        description='A hidden nameplate from Barnacle Boatyard.',
        modelPath='**/hidden_pg_bb',
    ),
    NameplateItemType.PG_YOTT: ProfileNameplateDefinition(
        name='Ye Olde Toontowne',
        description='A hidden nameplate from Ye Olde Toontowne.',
        modelPath='**/hidden_pg_yott',
    ),
    NameplateItemType.PG_DG: ProfileNameplateDefinition(
        name='Daffodil Gardens',
        description='A hidden nameplate from Daffodil Gardens.',
        modelPath='**/hidden_pg_dg',
    ),
    NameplateItemType.PG_MML: ProfileNameplateDefinition(
        name='Mezzo Melodyland',
        description='A hidden nameplate from Mezzo Melodyland.',
        modelPath='**/hidden_pg_mml',
    ),
    NameplateItemType.PG_TB: ProfileNameplateDefinition(
        name='The Brrrgh',
        description='A hidden nameplate from The Brrrgh.',
        modelPath='**/hidden_pg_tb',
    ),
    NameplateItemType.PG_AA: ProfileNameplateDefinition(
        name='Acorn Acres',
        description='A hidden nameplate from Acorn Acres.',
        modelPath='**/hidden_pg_aa',
    ),
    NameplateItemType.PG_DDL: ProfileNameplateDefinition(
        name='Drowsy Dreamland',
        description='A hidden nameplate from Drowsy Dreamland.',
        modelPath='**/hidden_pg_ddl',
    ),

    ### Activities ###
    NameplateItemType.Activity_Golfing: ProfileNameplateDefinition(
        name='Golfing',
        description='Rewarded to expert golfers!',
        modelPath='**/hidden_golfing',
    ),
    NameplateItemType.Activity_Trolley: ProfileNameplateDefinition(
        name='The Trolley',
        description='Rewarded to expert trolley enjoyers!',
        modelPath='**/hidden_trolley',
    ),
    NameplateItemType.Activity_Racing: ProfileNameplateDefinition(
        name='Racing',
        description='Rewarded to expert racers!',
        modelPath='**/hidden_racing',
    ),

    ### Sidetasks ###
    NameplateItemType.Tasks_Judy: ProfileNameplateDefinition(
        name='Crocheting Lessons',
        description='Todo!',
        modelPath='**/sidetask_judy',
        position=(0.008, 0, 0.138),
    ),

    ### Misc ###
    NameplateItemType.Special_Stars: ProfileNameplateDefinition(
        name='Stars',
        description="You're a STAR!",
        modelPath='**/hidden_stars',
    ),
    NameplateItemType.Special_UnderTheSea: ProfileNameplateDefinition(
        name='Under the Sea',
        description="Todo!",
        modelPath='**/hidden_underwater',
    ),
    NameplateItemType.Special_Slippin: ProfileNameplateDefinition(
        name='Slippin',
        description="Todo!",
        modelPath='**/hidden_banana',
    ),
    NameplateItemType.Special_UpToEleven: ProfileNameplateDefinition(
        name='Turning It Up To 11',
        description="Todo!",
        modelPath='**/hidden_maxevidence',
    ),
    NameplateItemType.Special_SnowballFight: ProfileNameplateDefinition(
        name='Snowball Fight',
        description="Todo!",
        modelPath='**/hidden_steve',
    ),
    NameplateItemType.Special_SellbotPaint: ProfileNameplateDefinition(
        name='Sellbot Paint',
        description='Obtained by defeating 10 Unstable Cogs during the Maypril Toons 2023 event.',
        modelPath='**/hidden_ocftf',
    ),

    ### Events ###
    NameplateItemType.Event_Tinsel: ProfileNameplateDefinition(
        name='Tinsel',
        description="Todo!",
        modelPath='**/event_tinsel',
    ),
    NameplateItemType.Event_Candy: ProfileNameplateDefinition(
        name='Candy',
        description="Todo!",
        modelPath='**/event_candy',
    ),
    NameplateItemType.Event_Wrapping: ProfileNameplateDefinition(
        name='Wrapping',
        description="Todo!",
        modelPath='**/event_wrapping',
    ),
    NameplateItemType.Event_NightLights: ProfileNameplateDefinition(
        name='Night Lights',
        description="Todo!",
        modelPath='**/event_nightlights',
    ),
    NameplateItemType.Event_NewYears2019: ProfileNameplateDefinition(
        name='New Years 2019 Fireworks',
        description="Todo!",
        modelPath='**/event_2019_fireworks',
    ),
    NameplateItemType.Event_SkyClan: ProfileNameplateDefinition(
        name='Dreams Come True',
        description="Todo!",
        modelPath='**/event_skyclan',
    ),
    NameplateItemType.Event_Outback: ProfileNameplateDefinition(
        name='Outback',
        description="Found this on the side of the road.",
        modelPath='**/event_outback',
    ),
    NameplateItemType.Event_LazyBones: ProfileNameplateDefinition(
        name='Lazy Bones',
        description="Todo!",
        modelPath='**/event_lazy',
    ),
    NameplateItemType.Event_Thanksgiving2019: ProfileNameplateDefinition(
        name='Thanksgiving 2019',
        description="Todo!",
        modelPath='**/event_2019_thanksgiving',
    ),
    NameplateItemType.Event_NewYears2020: ProfileNameplateDefinition(
        name='New Years 2020 Fireworks',
        description="Todo!",
        modelPath='**/event_2020_newyears',
    ),
    NameplateItemType.Event_PinkSlip: ProfileNameplateDefinition(
        name='Pink Slip',
        description="Todo!",
        modelPath='**/event_btl',
    ),
    NameplateItemType.Event_Easter2020: ProfileNameplateDefinition(
        name='Easter 2020',
        description="Todo!",
        modelPath='**/event_easter2020',
    ),
    NameplateItemType.Event_AtticusDesk: ProfileNameplateDefinition(
        name="Atticus' Desk",
        description="Todo!",
        modelPath='**/event_standin',
    ),
    NameplateItemType.Event_FourthJuly2020: ProfileNameplateDefinition(
        name='Prepare for Launch',
        description="Todo!",
        modelPath='**/firework_nameplate',
    ),
    NameplateItemType.Event_Electric: ProfileNameplateDefinition(
        name='Electric',
        description="Todo!",
        modelPath='**/event_electric',
        scale=(1.08, 1, 1.08),
    ),
    NameplateItemType.Halloween_CandyBlue: ProfileNameplateDefinition(
        name='Blue Halloween Candy',
        description="Todo!",
        modelPath='**/event_halloween_candy_blue',
        scale=(1.125, 1, 0.95),
    ),
    NameplateItemType.Halloween_CandyGreen: ProfileNameplateDefinition(
        name='Green Halloween Candy',
        description="Todo!",
        modelPath='**/event_halloween_candy_green',
        scale=(1.125, 1, 0.95),
    ),
    NameplateItemType.Halloween_CandyMagenta: ProfileNameplateDefinition(
        name='Magenta Halloween Candy',
        description="Todo!",
        modelPath='**/event_halloween_candy_magenta',
        scale=(1.125, 1, 0.95),
    ),
    NameplateItemType.Halloween_CandyPurple: ProfileNameplateDefinition(
        name='Purple Halloween Candy',
        description="Todo!",
        modelPath='**/event_halloween_candy_purple',
        scale=(1.125, 1, 0.95),
    ),
    NameplateItemType.Halloween_CandyRed: ProfileNameplateDefinition(
        name='Red Halloween Candy',
        description="Todo!",
        modelPath='**/event_halloween_candy_red',
        scale=(1.125, 1, 0.95),
    ),
    NameplateItemType.Halloween_SpookyBat: ProfileNameplateDefinition(
        name='Spooky Bat',
        description="Todo!",
        modelPath='**/event_halloween_bat',
        scale=(1.125, 1, 1),
        position=(0, 0, 0.1325),
    ),

    ### Kudos ###
    NameplateItemType.Kudos_TTC: ProfileNameplateDefinition(
        name='You Did It',
        description="Great Job. We're very proud of you.\nObtained upon reaching rank 4 in Toontown Central Kudos!",
        modelPath='**/kudos_ttc',
    ),
    NameplateItemType.Kudos_BB: ProfileNameplateDefinition(
        name='Sandcastles',
        description="Obtained upon reaching rank 4 in Barnacle Boatyard Kudos!",
        modelPath='**/kudos_bb',
    ),
    NameplateItemType.Kudos_YOTT: ProfileNameplateDefinition(
        name='The Doodragon',
        description="Obtained upon reaching rank 4 in Ye Olde Toontowne Kudos!",
        modelPath='**/kudos_yott',
    ),
    NameplateItemType.Kudos_DG: ProfileNameplateDefinition(
        name='Gardening',
        description="Obtained upon reaching rank 4 in Daffodil Gardens Kudos!",
        modelPath='**/kudos_dg',
    ),
    NameplateItemType.Kudos_MML: ProfileNameplateDefinition(
        name='Fires n\' Flames',
        description="Obtained upon reaching rank 4 in Mezzo Melodyland Kudos!",
        modelPath='**/kudos_mml',
    ),
    NameplateItemType.Kudos_TB: ProfileNameplateDefinition(
        name='Scarf',
        description="Obtained upon reaching rank 4 in The Brrrgh Kudos!",
        modelPath='**/kudos_tb',
    ),
    NameplateItemType.Kudos_AA: ProfileNameplateDefinition(
        name='Light Show',
        description="Obtained upon reaching rank 4 in Acorn Acres Kudos!",
        modelPath='**/kudos_aa',
    ),
    NameplateItemType.Kudos_DDL: ProfileNameplateDefinition(
        name='Sweet',
        description="Obtained upon reaching rank 4 in Drowsy Dreamland Kudos!",
        modelPath='**/kudos_ddl',
    ),
}
