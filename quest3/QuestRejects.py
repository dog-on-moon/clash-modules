"""
Module for NPC reject dialogue and all associated functions.
"""

from copy import deepcopy
import random

from toontown.battle import SuitBattleGlobals
from toontown.hood import ZoneUtil
from toontown.toon.npc import NPCToons
from toontown.toonbase import ToontownGlobals


QuestsRejectDefault = (
    'Heya, _avName_!',
    'Whatcha need?',
    'Hello! How are you doing?',
    'Hi there.',
    "How's it going?",
    "Sorry _avName_, I'm a bit busy right now.",
    'Yes?',
    'Howdy, _avName_!',
    'Welcome, _avName_!',
    "Hey, _avName_! How's it hanging?",
    "Need any help?",
    "Hi _avName_, what brings you here?"
)

QuestsRejectDefined = {
    # Cog HQs
}


def getNpcInfo(npcId):
    npcName = NPCToons.getNPCName(npcId)
    npcZone = NPCToons.getNPCZone(npcId)
    hoodId = ZoneUtil.getCanonicalHoodId(npcZone)
    hoodName = base.cr.hoodMgr.getFullnameFromId(hoodId)
    buildingName = NPCToons.getBuildingTitle(npcZone)
    branchId = ZoneUtil.getCanonicalBranchZone(npcZone)
    streetName = ToontownGlobals.StreetNames[branchId][-1]
    isInPlayground = ZoneUtil.isPlayground(branchId)
    return (npcName, hoodName, buildingName, streetName, isInPlayground)


def getNpcLocationDialog(fromNpcId, toNpcId):
    if not toNpcId:
        return (None, None, None, None)
    fromNpcZone = None
    fromBranchId = None
    if fromNpcId:
        fromNpcZone = NPCToons.getNPCZone(fromNpcId)
        fromBranchId = ZoneUtil.getCanonicalBranchZone(fromNpcZone)
    toNpcZone = NPCToons.getNPCZone(toNpcId)
    toBranchId = ZoneUtil.getCanonicalBranchZone(toNpcZone)
    toNpcName, toHoodName, toBuildingName, toStreetName, isInPlayground = getNpcInfo(toNpcId)
    if fromBranchId == toBranchId:
        if isInPlayground:
            streetDesc = 'in this playground'
            street = 'in this playground'
        else:
            streetDesc = 'on this street'
            street = 'on this street'
    elif isInPlayground:
        streetDesc = 'in the %s playground' % toHoodName
        street = 'in the %s playground' % toHoodName
    else:
        streetDesc = 'on %(toStreetName)s in %(toHoodName)s' % {
            'toStreetName': toStreetName,
            'toHoodName': toHoodName
        }
        street = 'on %(toStreetName)s' % {'toStreetName': toStreetName}

    paragraph = '\x07%(building)s "%(buildingName)s"...\x07...%(buildingVerb)s %(street)s.' % {
        'building': "%s's building is called" % toNpcName,
        'buildingName': toBuildingName,
        'buildingVerb': 'which is',
        'street': streetDesc
    }

    return (paragraph, toBuildingName, streetDesc, street)


def fillInQuestNames(text: str, avName: str=None, fromNpcId: int=None, toNpcId: int=None, av=None):
    text = deepcopy(text)
    toNpcName = ''
    fromNpcName = ''
    where = ''
    buildingName = ''
    streetDesc = ''
    street = ''

    if avName is not None:
        text = text.replace('_avName_', avName)
    if av is not None:
        if hasattr(av, 'suit'):
            suitName = SuitBattleGlobals.SuitAttributes[av.suit.style.name]['name']
        else:
            suitName = avName
        text = text.replace('_suitName_', suitName)
    if toNpcId:
        toNpcName = str(NPCToons.getNPCName(toNpcId))
        where, buildingName, streetDesc, street = getNpcLocationDialog(fromNpcId, toNpcId)
    if fromNpcId:
        fromNpcName = str(NPCToons.getNPCName(fromNpcId))

    replacements = {
        '_toNpcName_':    toNpcName,
        '_fromNpcName_':  fromNpcName,
        '_where_':        where,
        '_buildingName_': buildingName,
        '_streetDesc_':   streetDesc,
        '_street_':       street,
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text
