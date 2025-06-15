"""
This module contains the item data for profile poses.
"""
from panda3d.core import NodePath

from toontown.battle import BattleProps
from toontown.inventory.base.InventoryItem import InventoryItem
from toontown.inventory.base.ItemDefinition import ItemDefinition
from typing import Dict, Optional
from enum import IntEnum, Enum, auto

from toontown.inventory.enums.ItemEnums import ProfilePoseItemType
from toontown.inventory.enums.RarityEnums import Rarity
from toontown.toon import CheesyEffectGlobals
from toontown.toon import ToonDNA
from toontown.toonbase import ToontownGlobals


class PoseValueEnum(Enum):
    Animation = auto()
    Eyes = auto()
    Muzzle = auto()
    AvatarPanelPos = auto()
    Hpr = auto()
    ItemsPagePos = auto()
    Prop = auto()
    PropParent = auto()
    PropPos = auto()
    PropHpr = auto()
    PropScale = auto()
    Scale = auto()
    Species = auto()
    CheesyEffect = auto()


class ProfilePoseDefinition(ItemDefinition):
    """
    The definition structure for profile poses.
    """
    def __init__(self,
                 poseData: dict,
                 **kwargs):
        super().__init__(**kwargs)
        self.poseData = poseData

    def getPoseData(self) -> dict:
        return self.poseData

    def getItemTypeName(self):
        return 'Profile Pose'

    def getRewardName(self, item: Optional[InventoryItem] = None):
        return f'{self.getName()} Profile Pose'

    def getGuiItemModel(self, item: Optional[InventoryItem] = None, *args, **kwargs) -> NodePath:
        """
        Returns a nodepath that is to be used in 2D space.
        """
        return super().getGuiItemModel(item=item, useModel=self.renderTextForGuiModel(item), *args, **kwargs)

    def applyPoseToToon(self, toon, notify, localToonIsReused=False):
        """
        Applies a profile pose to the given toon.
        :param toon:
        :param notify:
        :param localToonIsReused: Whether we should try to clean up aspects of previous profile poses (and it's based on localAvatar).
        :return:
        """
        # TODO: Check to see if we can move all the cleanup code up here, and tie it to localToonIsReused

        # Apply cheesy effect
        cheesyEffect = self.poseData.get(PoseValueEnum.CheesyEffect)
        if cheesyEffect:
            toon.applyCheesyEffect(cheesyEffect)
        else:
            toon.clearCheesyEffect()

        # Change the species of the Toon
        def updateSpecies(species):
            newDna = ToonDNA.ToonDNA()
            newDna.makeFromNetString(toon.style.makeNetString())
            newDna.head = f'{species}{toon.style.head[1:]}'
            toon.updateToonDNA(newDna)
            toon.setBlend(frameBlend=base.wantSmoothAnims)
            toon.setLODAnimation(base.lodMaxRange, base.lodMinRange, base.lodDelayFactor)

        if PoseValueEnum.Species in self.poseData:
            # If the Toon is already this species, give them a big head instead.
            if self.poseData[PoseValueEnum.Species] == toon.style.head[0] and \
                    (not localToonIsReused or self.poseData[PoseValueEnum.Species] == base.localAvatar.style.head[0]):
                toon.applyCheesyEffect(CheesyEffectGlobals.CEBigHead)
            else:
                updateSpecies(self.poseData[PoseValueEnum.Species])
        elif localToonIsReused and base.localAvatar.style.head[0] != toon.style.head[0]:
            # Make sure we represent their true species.
            updateSpecies(base.localAvatar.style.head[0])

        # Pose the Toon
        toon.pose(*self.poseData[PoseValueEnum.Animation])

        # Cleanup Eyes (have to close and open eyes to refresh)
        toon.normalEyes()
        toon.closeEyes()
        toon.openEyes()

        # Set Eye Type of Toon
        if PoseValueEnum.Eyes in self.poseData:
            eyeType = self.poseData[PoseValueEnum.Eyes]
            if eyeType == 'sad':
                toon.sadEyes()
                toon.closeEyes()
                toon.openEyes()
            elif eyeType == 'surprise':
                toon.surpriseEyes()
            elif eyeType == 'angry':
                toon.angryEyes()
                toon.closeEyes()
                toon.openEyes()
            elif eyeType == 'close':
                toon.closeEyes()
            else:
                notify.warning('Requested eye type {} not valid.'.format(eyeType))

        # Cleanup Muzzles
        toon.hideSadMuzzle()
        toon.hideSurpriseMuzzle()
        toon.hideAngryMuzzle()
        toon.hideSmileMuzzle()

        # Set Muzzle Type of Toon
        if PoseValueEnum.Muzzle in self.poseData:
            muzzleType = self.poseData[PoseValueEnum.Muzzle]
            if muzzleType == 'sad':
                toon.showSadMuzzle()
            elif muzzleType == 'surprise':
                toon.showSurpriseMuzzle()
            elif muzzleType == 'angry':
                toon.showAngryMuzzle()
            elif muzzleType == 'smile':
                toon.showSmileMuzzle()
            elif muzzleType == 'laugh':
                toon.showLaughMuzzle()
            else:
                notify.warning('Requested muzzle type {} not valid.'.format(muzzleType))

        # Set Rotation of Toon
        if PoseValueEnum.Hpr in self.poseData:
            toon.setHpr(*self.poseData[PoseValueEnum.Hpr])
        else:
            toon.setHpr(0, 0, 0)

        # Set Scale of Toon
        if PoseValueEnum.Scale in self.poseData:
            toon.setScale(toon.getScale() * self.poseData[PoseValueEnum.Scale])

        # Clear potential lingering props from both hands
        for child in toon.leftHand.getChildren():
            child.removeNode()
        for child in toon.rightHand.getChildren():
            child.removeNode()

        # Attach prop to Toon
        if PoseValueEnum.Prop in self.poseData and PoseValueEnum.PropParent in self.poseData:
            for i in range(len(self.poseData[PoseValueEnum.Prop])):
                if self.poseData[PoseValueEnum.PropParent][i]:
                    propParent = getattr(toon, self.poseData[PoseValueEnum.PropParent][i])
                else:
                    propParent = toon

                # Figure out prop name and if we're extracting a part of it
                propPart = None
                if isinstance(self.poseData[PoseValueEnum.Prop][i], list):
                    propName = self.poseData[PoseValueEnum.Prop][i][0]
                    propPart = self.poseData[PoseValueEnum.Prop][i][1]
                else:
                    propName = self.poseData[PoseValueEnum.Prop][i]

                # Check to see if the prop name is a model path, if so load that model.
                # If not, it should be in the globalPropPool.
                if 'phase_' in propName:
                    prop = loader.loadModel(propName)
                    if propPart:
                        model = prop
                        prop = model.find(propPart)
                        prop.reparentTo(propParent)
                        model.removeNode()
                else:
                    prop = BattleProps.globalPropPool.getProp(propName)

                prop.reparentTo(propParent)

                # Transform the prop
                if PoseValueEnum.PropPos in self.poseData:
                    prop.setPos(self.poseData[PoseValueEnum.PropPos][i])
                if PoseValueEnum.PropHpr in self.poseData:
                    prop.setHpr(self.poseData[PoseValueEnum.PropHpr][i])
                if PoseValueEnum.PropScale in self.poseData:
                    prop.setScale(self.poseData[PoseValueEnum.PropScale][i])

                # Reparent the prop to the toon's right hand so we can make sure it gets cleaned up
                prop.wrtReparentTo(toon.rightHand)

        # Make sure we don't be looking around
        toon.stopLookAroundNow()


# The registry dictionary for profile poses.
# NOTE: When adding hpr, you will likely need to find an appropriate posOffset for the TAP
ProfilePoseRegistry: Dict[IntEnum, ProfilePoseDefinition] = {
    # Default
    ProfilePoseItemType.Neutral: ProfilePoseDefinition(
        name='Neutral',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('neutral', 0)
        }
    ),
    ProfilePoseItemType.Wave: ProfilePoseDefinition(
        name='Wave',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('wave', 50)
        }
    ),
    ProfilePoseItemType.Sit: ProfilePoseDefinition(
        name='Sit',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('sit', 0)
        }
    ),
    ProfilePoseItemType.Applause: ProfilePoseDefinition(
        name='Applause',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('applause', 14)
        }
    ),
    ProfilePoseItemType.Thinking: ProfilePoseDefinition(
        name='Thinking',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('think', 40)
        }
    ),
    ProfilePoseItemType.Greened: ProfilePoseDefinition(
        name='Greened',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('sad-neutral', 0)
        }
    ),
    ProfilePoseItemType.Taunt: ProfilePoseDefinition(
        name='Taunt',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('taunt', 27)
        }
    ),
    ProfilePoseItemType.ImOuttaHere: ProfilePoseDefinition(
        name="I'm Outta Here!",
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('sidestep-left', 11),
            PoseValueEnum.Eyes: 'surprise',
        }
    ),
    ProfilePoseItemType.Casting: ProfilePoseDefinition(
        name='Casting',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('cast', 28),
            PoseValueEnum.AvatarPanelPos: (-0.68, 0, 0),
            PoseValueEnum.Hpr: (-20, 0, 0),
        }
    ),
    ProfilePoseItemType.Yippie: ProfilePoseDefinition(
        name='Yippie!',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('good-putt', 12)
        }
    ),
    ProfilePoseItemType.Selfie: ProfilePoseDefinition(
        name='Selfie',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('battlecast', 20),
            PoseValueEnum.Muzzle: 'smile',
        }
    ),
    ProfilePoseItemType.ResistanceSalute: ProfilePoseDefinition(
        name='Resistance Salute',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('victory', 130)
        }
    ),
    ProfilePoseItemType.Throw: ProfilePoseDefinition(
        name='Throw',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('throw', 55),
            PoseValueEnum.Eyes: 'angry',
            PoseValueEnum.AvatarPanelPos: (0.8, 0, 0),
            PoseValueEnum.Hpr: (20, 0, 0),
        }
    ),
    ProfilePoseItemType.Hypnotizer: ProfilePoseDefinition(
        name='Hypnotizer',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('hypnotize', 23)
        }
    ),
    ProfilePoseItemType.Running: ProfilePoseDefinition(
        name='Running',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('wheelRun', 30),
            PoseValueEnum.AvatarPanelPos: (2.39, 0, 0),
            PoseValueEnum.Hpr: (50, 0, 0),
        }
    ),
    ProfilePoseItemType.Diving: ProfilePoseDefinition(
        name='Diving',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('climb', 115)
        }
    ),
    ProfilePoseItemType.WhatAreYouDoing: ProfilePoseDefinition(
        name='What Are You Doing?!',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('down', 3),
            PoseValueEnum.Eyes: 'surprise',
        }
    ),
    ProfilePoseItemType.Slapped: ProfilePoseDefinition(
        name='Slapped',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('sound', 4),
            PoseValueEnum.Eyes: 'surprise',
            PoseValueEnum.Muzzle: 'sad',
        }
    ),
    ProfilePoseItemType.Surprised: ProfilePoseDefinition(
        name='Surprised',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('conked', 17),
            PoseValueEnum.Eyes: 'surprise',
            PoseValueEnum.Muzzle: 'surprise',
        }
    ),
    ProfilePoseItemType.Presenting: ProfilePoseDefinition(
        name='Presenting...',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('smooch', 120),
            PoseValueEnum.Muzzle: 'smile',
            PoseValueEnum.AvatarPanelPos: (0.35, 0, 0),
            PoseValueEnum.Hpr: (10, 0, 0),
        }
    ),
    ProfilePoseItemType.Victory: ProfilePoseDefinition(
        name='Victory',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('victory', 230)
        }
    ),
    ProfilePoseItemType.Shrug: ProfilePoseDefinition(
        name='Shrug',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('shrug', 132)
        }
    ),
    ProfilePoseItemType.Upset: ProfilePoseDefinition(
        name='Upset',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('confused', 72),
            PoseValueEnum.Eyes: 'angry',
            PoseValueEnum.Muzzle: 'angry',
            PoseValueEnum.AvatarPanelPos: (1.59, 0, 0),
            PoseValueEnum.Hpr: (38, 0, 0),
        }
    ),
    ProfilePoseItemType.ToBeOrNotToBe: ProfilePoseDefinition(
        name='To Be Or Not To Be?',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('right', 9),
            PoseValueEnum.Eyes: 'sad',
            PoseValueEnum.Muzzle: 'sad',
        }
    ),
    ### Halloween ###
    ProfilePoseItemType.Spooky: ProfilePoseDefinition(
        name='Spooky',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('cringe', 18),
            PoseValueEnum.Muzzle: 'surprise',
        }
    ),
    ProfilePoseItemType.Zombie: ProfilePoseDefinition(
        name='Zombie',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('block', 17)
        }
    ),
    ProfilePoseItemType.Yawn: ProfilePoseDefinition(
        name='Yawn',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('victory', 104),
            PoseValueEnum.Eyes: 'close',
            PoseValueEnum.Muzzle: 'surprise',
        }
    ),
    ProfilePoseItemType.Sinking: ProfilePoseDefinition(
        name='Sinking',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('melt', 49),
            PoseValueEnum.Eyes: 'sad',
            PoseValueEnum.Muzzle: 'sad',
            PoseValueEnum.AvatarPanelPos: (0, 0, -0.015),
            PoseValueEnum.ItemsPagePos: (0, 0, 0.228),
        }
    ),
    ### OCLO Directives ###
    ProfilePoseItemType.Megaphone: ProfilePoseDefinition(
        name='Megaphone',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('sound', 23),
            PoseValueEnum.AvatarPanelPos: (1.08, 0, 0),
            PoseValueEnum.Hpr: (30, 0, 0),
            PoseValueEnum.Prop: ['blue-megaphone'],
            PoseValueEnum.PropParent: ['rightHand'],
        }
    ),
    ### Unused ###
    ProfilePoseItemType.UpsideDown: ProfilePoseDefinition(
        name='Upside Down',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('neutral', 0),
            PoseValueEnum.AvatarPanelPos: (0, 0, -0.5),
            PoseValueEnum.ItemsPagePos: (0, 0, 0.4),
            PoseValueEnum.Hpr: (0, 0, 180),
        }
    ),
    ProfilePoseItemType.Sideways: ProfilePoseDefinition(
        name='Sideways',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('neutral', 0),
            PoseValueEnum.AvatarPanelPos: (-0.25, 0, -0.3),
            PoseValueEnum.ItemsPagePos: (0.2, 0, 0.2),
            PoseValueEnum.Hpr: (0, 0, 90),
        }
    ),
    ProfilePoseItemType.Small: ProfilePoseDefinition(
        name='Small',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('neutral', 0),
            PoseValueEnum.Scale: 0.4,
        }
    ),
    ### Gumball Machine ###
    ProfilePoseItemType.SilentTreatment: ProfilePoseDefinition(
        name='Silent Treatment',
        description='Shh!',
        poseData={
            PoseValueEnum.Animation: ('neutral', 0),
            PoseValueEnum.Hpr: (180, 0, 0),
        }
    ),
    ProfilePoseItemType.Banana: ProfilePoseDefinition(
        name='Banana',
        description='Whoops! Who left that there!?',
        poseData={
            PoseValueEnum.Animation: ('toss', 32),
            PoseValueEnum.AvatarPanelPos: (1.09, 0, 0),
            PoseValueEnum.Hpr: (30, 0, 0),
            PoseValueEnum.Eyes: 'angry',
            PoseValueEnum.Muzzle: 'smile',
            PoseValueEnum.Prop: ['banana'],
            PoseValueEnum.PropScale: [0.75],
            PoseValueEnum.PropParent: ['rightHand'],
        }
    ),
    ProfilePoseItemType.SeltzerBottle: ProfilePoseDefinition(
        name='Seltzer Bottle',
        description='Would you like a seltzer, sir?',
        poseData={
            PoseValueEnum.Animation: ('hold-bottle', 24),
            PoseValueEnum.AvatarPanelPos: (1.09, 0, 0),
            PoseValueEnum.Hpr: (30, 0, 0),
            PoseValueEnum.Prop: ['bottle'],
            PoseValueEnum.PropParent: ['rightHand'],
        }
    ),
    ProfilePoseItemType.GagButton: ProfilePoseDefinition(
        name='Gag Button',
        description='Watch your head!',
        poseData={
            PoseValueEnum.Animation: ('pushbutton', 41),
            PoseValueEnum.AvatarPanelPos: (1.09, 0, 0),
            PoseValueEnum.Hpr: (30, 0, 0),
            PoseValueEnum.Prop: ['button-no-actor'],
            PoseValueEnum.PropParent: ['leftHand'],
        }
    ),
    ProfilePoseItemType.PieToss: ProfilePoseDefinition(
        name='Pie Toss',
        description='This one is on the house!',
        poseData={
            PoseValueEnum.Animation: ('toss', 43),
            PoseValueEnum.AvatarPanelPos: (1.13, 0, 0),
            PoseValueEnum.Hpr: (30, 0, 0),
            PoseValueEnum.Muzzle: 'laugh',
            PoseValueEnum.Prop: ['fruitpie'],
            PoseValueEnum.PropParent: ['rightHand'],
        }
    ),
    ### Kudos ###
    ProfilePoseItemType.BecomeDuck: ProfilePoseDefinition(
        name='Become Duck',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('neutral', 0),
            PoseValueEnum.Species: 'f',
        }
    ),
    ProfilePoseItemType.Treasure: ProfilePoseDefinition(
        name='Treasure',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('bank', 50),
            PoseValueEnum.AvatarPanelPos: (2.39, 0, 0),
            PoseValueEnum.Hpr: (50, 0, 0),
            PoseValueEnum.Muzzle: 'smile',
            PoseValueEnum.Prop: ['treasure-chest'],
            PoseValueEnum.PropParent: ['rightHand'],
            PoseValueEnum.PropHpr: [(180, 0, 0)],
            PoseValueEnum.PropScale: [0.8],
        }
    ),
    ProfilePoseItemType.AtTheGate: ProfilePoseDefinition(
        name='At The Gate',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('tickle', 21),
            PoseValueEnum.Eyes: 'angry',
            PoseValueEnum.AvatarPanelPos: (-0.94, 0, 0),
            PoseValueEnum.Hpr: (-25, 0, 0),
            PoseValueEnum.Prop: ['phase_4/models/accessories/tt_m_chr_avt_acc_pac_woodenSword'],
            PoseValueEnum.PropParent: ['rightHand'],
            PoseValueEnum.PropPos: [(0.3, 1.35, 0.1)],
            PoseValueEnum.PropHpr: [(0, 90, 0)],
            PoseValueEnum.PropScale: [0.4],
        }
    ),
    ProfilePoseItemType.Elegance: ProfilePoseDefinition(
        name='Elegance',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('sprinkle-dust', 36),
        }
    ),
    ProfilePoseItemType.PickUpThePhone: ProfilePoseDefinition(
        name='Pick Up The Phone',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('pushbutton', 57),
            PoseValueEnum.Muzzle: 'surprise',
            PoseValueEnum.Prop: ['receiver', 'phone'],
            PoseValueEnum.PropParent: ['rightHand', 'leftHand'],
            PoseValueEnum.PropPos: [(-0.2, -0.37, 0.8), (0, 0, 0)],
            PoseValueEnum.PropHpr: [(90, 180, 0,), (0, 0, 0)],
            PoseValueEnum.PropScale: [1.0, 1.0],
        }
    ),
    ProfilePoseItemType.FireHands: ProfilePoseDefinition(
        name='Fire Hands',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('juggle', 57),
            PoseValueEnum.Eyes: 'surprise',
            PoseValueEnum.Muzzle: 'surprise',
            PoseValueEnum.Prop: [
                ['phase_12/models/char/suits/ttcc_ene_firestarter-zero', '**/fire_seq'],
                ['phase_12/models/char/suits/ttcc_ene_firestarter-zero', '**/fire_seq'],
            ],
            PoseValueEnum.PropParent: ['rightHand', 'leftHand'],
            PoseValueEnum.PropPos: [(-0.5, 0.0, -3.4), (-0.5, 0.0, -3.4)],
            PoseValueEnum.PropHpr: [(90, 0, 0), (90, 0, 0)],
            PoseValueEnum.PropScale: [2.0, 2.0],
        }
    ),
    ProfilePoseItemType.Rolled: ProfilePoseDefinition(
        name='Rolled',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('slip-forward', 75),
            PoseValueEnum.Eyes: 'sad',
            PoseValueEnum.Muzzle: 'sad',
            PoseValueEnum.Prop: ['treekiller_log'],
            PoseValueEnum.PropParent: [None],
            PoseValueEnum.PropPos: [(-0.1, 0.7, 0.8)],
            PoseValueEnum.PropHpr: [(0, 0, 0)],
            PoseValueEnum.PropScale: [1.75],
        }
    ),
    ProfilePoseItemType.Naptime: ProfilePoseDefinition(
        name='Naptime',
        description='Todo!',
        poseData={
            PoseValueEnum.Animation: ('slip-backward', 22),
            PoseValueEnum.Eyes: 'close',
            PoseValueEnum.AvatarPanelPos: (2.34, 0, 0.04),
            PoseValueEnum.Hpr: (50, 0, 0),
            PoseValueEnum.Prop: ['phase_8/models/props/zzz_treasure'],
            PoseValueEnum.PropParent: [None],
            PoseValueEnum.PropPos: [(-1.6, 0.4, 1.5)],
            PoseValueEnum.PropHpr: [(0, 0, -15)],
            PoseValueEnum.PropScale: [0.6],
        }
    ),
}
