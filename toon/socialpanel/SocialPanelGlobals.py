"""
Global definitions for the Social Panel.
"""
from toontown.groups.GroupClasses import GroupBase, GroupType
from toontown.hood import ZoneUtil
from toontown.battle import BattleGlobals
from toontown.toonbase.ToontownGlobals import *

# event enums
TAB_FRIENDS = 0
TAB_GROUPS = 1
# TAB_CLUBS = 3
TAB_FRIENDS_INVITE = 4

# some state names
STATE_BROWSE = 'Browse'
STATE_VIEW = 'View'
STATE_CREATE = 'Create'

# social panel defaults
DEFAULT_TAB = TAB_FRIENDS

# friends tab stuff
friendYOffset = 0.5

# groups tab stuff
groupsPerRow = 1
groupsPerCol = 6

# gui stuff
sp_gui = loader.loadModelRaw('phase_3.5/models/gui/socialpanel/social_panel')
sp_gui_icons = loader.loadModelRaw('phase_3.5/models/gui/socialpanel/social_panel_icons')
sp_gui_bgs = loader.loadModelRaw('phase_3.5/models/gui/socialpanel/social_panel_groupbgs')
tooltipGUI = loader.loadModelRaw('phase_3.5/models/gui/battlegui/info_panels')
gagSelectGui = loader.loadModelRaw('phase_3.5/models/gui/battlegui/gag_selection_panels')

# gag icons
AvPropsNew = BattleGlobals.AvPropsNew
invModel = base.loader.loadModel('phase_3.5/models/gui/inventory_icons')
invModels = []
for track in range(len(AvPropsNew)):
    itemList = []
    for item in range(len(AvPropsNew[track])):
        itemList.append(invModel.find('**/' + AvPropsNew[track][item]))

    invModels.append(itemList)

# some text
waitingForToon = "\x01SlightSlant\x01Waiting for Toon...\x02"


# bg handling
def getSocialPanelGroupBg(group: GroupBase, pgOnly=False):
    """Gets the node to use for the bgs."""
    name = None  # base image

    if not pgOnly:
        # See if we can pick some groups that are not pg-only
        type2BgGroup = {
            'pg_factory':      [GroupType.FrontFactory, GroupType.SideFactory],
            'pg_lawfice':      [GroupType.LawficeA, GroupType.LawficeB, GroupType.LawficeC],
            'pg_cgc':          [GroupType.SilverSprocket, GroupType.GoldenGear, GroupType.DiamondDynamo],
            'bldg_pizzeria':   [GroupType.Pizzeria],
            'bldg_pizzeria_b': [GroupType.Plutocrat],
        }
        for groupName, typeList in type2BgGroup.items():
            if group.groupType in typeList:
                name = groupName
                break

    if not name:
        # If the overrides were not set, at minimum, match it to a playground
        name = {
            ToontownCentral:    'pg_ttc',
            DonaldsDock:        'pg_bb',
            OldeToontown:       'pg_yott',
            DaisyGardens:       'pg_dg',
            MinniesMelodyland:  'pg_mml',
            TheBrrrgh:          'pg_brrrgh',
            OutdoorZone:        'pg_aa',
            DonaldsDreamland:   'pg_ddl',
            GolfZone:           'pg_minigames',
            GoofySpeedway:      'pg_race',
            SellbotHQ:          'pg_sbhq',
            CashbotHQ:          'pg_cbhq',
            LawbotHQ:           'pg_lbhq',
            BossbotHQ:          'pg_bbhq',
            BoardbotHQ:         'pg_boredbot',
        }.get(ZoneUtil.getHoodId(group.zoneId), name)

    # We got it!!
    return sp_gui_bgs.find(f'**/{name or "pg_brrrgh"}')


# dev stuff
def questCard():
    """Gets the questCard image for placeholders."""
    bookModel = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
    questCard = bookModel.find('**/questCard')
    bookModel.removeNode()
    return questCard
