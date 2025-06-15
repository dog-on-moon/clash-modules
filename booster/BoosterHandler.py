"""
This is an AI superclass that you can apply on
various objects to give them booster handling properties.
"""
import datetime
import math
from datetime import timedelta

# from typing import List, Union
import time

from toontown.booster.BoosterBase import BoosterBase
from toontown.inventory.enums.ItemEnums import BoosterItemType
from toontown.inventory.registry.BoosterRegistry import AllStarBoosts, BoosterDefinition, BoostMode, BossRewardBoosts
from toontown.inventory.registry.ItemTypeRegistry import getItemDefinition
from toontown.time import TimeUtil


class BoosterHandler:
    """
    A class with the logic to give various classes the ability to manage local boosts.

    BoosterHandler also has the notion of childBoosterHandlers.
    Any BoosterHandler subclass may associate with it a list of BoosterHandlers,
    which will have the BoosterHandler count for all of its
    child BoosterHandlers when applying boosts.
    """

    def __init__(self, rawBoosters: list = None, boosters: list = None, childBoosterHandlers: list = None):
        """
        Inits the BoosterHandler.
        :param rawBoosters: A 'raw booster' list (ala Astron struct).
        :param boosters: A list of BoosterBases.
        :param childBoosterHandlers: A list of child BoosterHandler classes.
        """
        if rawBoosters is None:
            rawBoosters = []
        if boosters is None:
            boosters = []
        if childBoosterHandlers is None:
            childBoosterHandlers = []
        self._rawBoosters = rawBoosters
        self.boosters = boosters
        self._childBoosterHandlers = childBoosterHandlers

    def b_setRawBoosters(self, boosters):
        """
        Sets the rawBoosters of this class.
        DistributedObjectAI subclasses can use this to properly
        register fields to distribute to a client (like in DistributedToonAI).
        :return: None.
        """
        self._rawBoosters = boosters

    def getRawBoosters(self):
        return self._rawBoosters

    def resetBoosters(self):
        """Resets all boosters."""
        self.b_setRawBoosters([])
        self._updateBoosters()

    def extendRawBoosterDurations(self, seconds: int) -> None:
        """
        Extends the duration of all raw boosters by some duration.

        :param seconds: The seconds to extend by.
        """
        # Build our raw boosters.
        rawBoosters = self.getRawBoosters()
        newRawBoosters = []

        # Go through each boosterType and endTimestamp.
        # When we re-add it, extend the seconds.
        for boosterData in rawBoosters:
            boosterType, endTimestamp, startTimestamp = boosterData
            newRawBoosters.append([boosterType, endTimestamp + seconds, startTimestamp + seconds])

        # Set our raw boosters directly.
        self.b_setRawBoosters(newRawBoosters)

    @staticmethod
    def _getCurrentTimeForBoosterHandler() -> float:
        """
        Gets the current time.
        :return: Float.
        """
        return time.time()

    def _validateRawBoosters(self):
        """
        Validates all of this Toon's rawBoosters to make sure they're active still.
        Cleanliness is always healthy for the mind and soul.
        :return: None.
        """
        # First, let's validate the rawBoosters.
        currentTime = self._getCurrentTimeForBoosterHandler()
        rawBoosters = self.getRawBoosters()
        newRawBoosters = []

        # Go through each boosterType and endTimestamp.
        for boosterData in rawBoosters:
            boosterType, endTimestamp, startTimestamp = boosterData

            # Is this booster expired?
            if currentTime > endTimestamp:
                continue

            # Extend with the new information
            newRawBoosters.append([int(boosterType), endTimestamp, startTimestamp])

        # Make sure we set our raw boosters.
        # We'll set it directly for now. We'll find that there's a booster inconsistency,
        # and then it'll run the b_set method for us.
        self._rawBoosters = newRawBoosters

    def _anyBoosterInconsistencies(self) -> bool:
        """
        Looks for any inconsistencies between the
        raw booster list and the BoosterBase list.
        :return: True if so, False if not.
        """
        # First, let's validate the rawBoosters.
        rawBoosters = self.getRawBoosters()

        # Are the lengths inconsistent?
        if len(self.boosters) != len(rawBoosters):
            return True

        # Go through each boosterType and endTimestamp.
        for i, boosterData in enumerate(rawBoosters):
            boosterType, endTimestamp, startTimestamp = boosterData

            # Has this changed from our current raw boosters?
            booster = self.boosters[i]  # type: BoosterBase
            if booster.getBoostType().value != boosterType or booster.endTimestamp != endTimestamp or booster.startTimestamp != startTimestamp:
                # It has.
                return True

        # There was no difference.
        return False

    def _validateBoosterInstances(self):
        """
        Ensures that this class has properly associated boosterInstances.
        :return: None.
        """
        # Clear out our current booster list.
        self.boosters = []

        # Make new booster instances based off of those in our rawBooster list.
        rawBoosters = self.getRawBoosters()
        for boosterData in rawBoosters:
            boosterType, endTimestamp, startTimestamp = boosterData
            self.boosters.append(BoosterBase(BoosterItemType(boosterType), endTimestamp=endTimestamp, startTimestamp=startTimestamp))

        # If we had to call this, then certainly we need to update the boosts.
        self.b_setRawBoosters(rawBoosters)

    def _boosterInstancesToRaw(self):
        """
        Updates the raw boosters with the instance ones we have.
        Only use this if you have modified booster instances
        BEFORE and AFTER an _updateBoosters call.

        :return: None.
        """
        newRawBoosters = []
        for booster in self.boosters:
            booster: BoosterBase
            newRawBoosters.append([booster.boosterType.value, booster.endTimestamp, booster.startTimestamp])
        self.b_setRawBoosters(newRawBoosters)

    def _updateBoosters(self):
        """
        Updates the Boosters.
        :return: None.
        """
        self._validateRawBoosters()
        if self._anyBoosterInconsistencies():
            # We only need to care about validating the booster instances if
            # found that there were any discrepancies between them and
            # the raw booster data established just above.
            self._validateBoosterInstances()

    def getBoosterOfType(self, boosterType: BoosterItemType):
        """
        Gets a booster instance of a given class.

        :param boosterType: The type of booster to hunt for.
        :return: The class instance, if it exists, or None.
        """
        if boosterType == BoosterItemType.Random:
            return None

        # Make sure our boosters are up to date.
        self._updateBoosters()

        # Search for this booster.
        boosterInstances = [booster for booster in self.boosters if booster.boosterType == boosterType]

        # Return it, if it exists.
        return None if not boosterInstances else boosterInstances[0]

    def addNewBooster(self, boosterType: BoosterItemType, timeDelta: datetime.timedelta = None, startTs: int | None = None):
        """
        Adds a new Booster to this class.

        :param boosterType: Some sort of boosterType class.
        :param timeDelta: A timedelta class.
        :param startTs: Optional start time for the booster.
        :return: None.
        """
        # If there's no time delta set, just put it to be like a minute from now.
        # It's likely being used as a temporary boost for a temporary booster handler.
        if timeDelta is None:
            timeDelta = timedelta(seconds=60)

        # Does a booster of this type already exist?
        existingBooster = self.getBoosterOfType(boosterType)  # type: BoosterBase

        # If no existing booster, then create a new one.
        if not existingBooster:
            # Make a new boosterInstance.
            boosterInstance = BoosterBase(boosterType)
            boosterInstance.setDuration(
                currentTime=startTs or self._getCurrentTimeForBoosterHandler(),
                timeDelta=timeDelta
            )

            # Get its raw struct, and put it in our boosterList.
            self._rawBoosters.append(boosterInstance.toStruct())
        else:
            # If there is, we extend the duration on the existing one.
            existingBooster.extendDuration(timeDelta=timeDelta)

            # Update our raw boosters with our instance ones.
            # This is safe to do since we're updating boosters
            # before (in getBoosterOfType) and after (just below).
            self._boosterInstancesToRaw()

        # Then, update our BoosterList.
        # This will make sure no other boosters are expired,
        # and will additionally confirm that instances are up to date.
        self._updateBoosters()

    def setChildBoosterHandlers(self, childBoosterHandlers) -> None:
        """
        Sets a list of child booster handlers.
        Mainly used for test cases, subclasses may find it
        a bit easier to simply overwrite self._getChildBoosterHandlers().
        """
        self._childBoosterHandlers = childBoosterHandlers  # type: List[BoosterHandler]

    def _getChildBoosterHandlers(self):
        """
        Gets a list of child booster handlers.
        Subclasses can overwrite this directly for them to
        more easily obtain a list of related BoosterHandlers.
        """
        return self._childBoosterHandlers

    def getAllBoosters(self):
        """
        Gets a list of all boosters.

        :return: A list of all boosters.
        """
        self._updateBoosters()
        return self.boosters

    def getBoosters(self, boosterType: BoosterItemType | list[BoosterItemType]) -> list[BoosterBase]:
        """
        Given a boosterType, returns all Booster classes of that type from
        this BoosterHandler and all of its child BoosterHandlers.

        :param boosterType: A boosterType, or list of boosterTypes.
        :return: A list of Booster classes.
        """
        # Ensure our boosters are updated.
        self._updateBoosters()

        # Listify our boosterType.
        if type(boosterType) is not list:
            boosterType = [boosterType]

        # Time to get all of these boosters.
        retBoosters = []
        for bt in boosterType:
            # Check ourselves for this booster.
            for booster in self.boosters:
                booster: BoosterBase
                if booster.boosterType == bt:
                    retBoosters.append(booster)

            # Check our child BoosterHandlers as well.
            for child in self._getChildBoosterHandlers():
                retBoosters.extend(child.getBoosters([bt]))

        # Return our complete list of boosters.
        return retBoosters

    def applyBoosters(self, boosterTypes, value, applyRound: bool = False) -> float | int:
        """
        Given a BoosterType (or list of boosterTypes) and a value,
        it will boost that value (applying all relevant boosts) and then returns it.

        :param boosterTypes: A boosterType, or list of boosterTypes.
        :param value: The value to boost.
        :param applyRound: Do we round this value?
        :return: The boosted value.
        """
        # Listify all of these boosters.
        if type(boosterTypes) is not list:
            boosterTypes = [boosterTypes]

        # Get the boosters of this type.
        boosters: list[BoosterBase] = self.getBoosters(boosterTypes)
        boostedValue = value

        # PREPASS 1: Add additional boosters if need be, based on current boosts.
        for booster in self.getAllBoosters():
            booster: BoosterBase
            boosterType: BoosterItemType = booster.getBoostType()
            itemDef: BoosterDefinition = getItemDefinition(boosterType)

            if itemDef.getBoostMode() == BoostMode.ALL_STAR:
                boosters.extend([
                    BoosterBase(itemType)
                    for itemType in AllStarBoosts
                ])

        # PREPASS 2: Add additional boosters if need be, based on expected boosts.
        for boosterType in boosterTypes:
            itemDef: BoosterDefinition = getItemDefinition(boosterType)
            if itemDef.getBoostMode() == BoostMode.GLOBAL_BOSS_REWARDS:
                # We have a global boss reward booster --
                # add an extra stack of any expected boss reward boosts.
                for searchBoosterType in boosterTypes:
                    if searchBoosterType in BossRewardBoosts:
                        boosters.append(BoosterBase(boosterType))

        # PASS 1: Apply additive boosts, determine multiplicative boosts.
        multBoost = 1
        for booster in boosters:
            booster: BoosterBase
            boosterType: BoosterItemType = booster.getBoostType()
            itemDef: BoosterDefinition = getItemDefinition(boosterType)

            if itemDef.getBoostMode() in (BoostMode.ADDITIVE, BoostMode.ADDITIVE_MULT):
                boostedValue += itemDef.getBoostAmount()
            elif itemDef.getBoostMode() in (BoostMode.ADDITIVE_MULTIPLICATIVE_PERC,):
                multBoost += itemDef.getBoostAmount()

        # PASS 2: Apply multiplicative boosts.
        for booster in boosters:
            booster: BoosterBase
            boosterType: BoosterItemType = booster.getBoostType()
            itemDef: BoosterDefinition = getItemDefinition(boosterType)
            if itemDef.getBoostMode() == BoostMode.MULTIPLICATIVE:
                boostedValue *= itemDef.getBoostAmount()

        # Apply mult boost.
        boostedValue *= multBoost

        # Return our boosted value.
        if applyRound:
            return round(boostedValue)
        return boostedValue


if __debug__:
    # You can set BoosterType enums here to be active on dev.
    debugBoostersToForce = [
        # BoosterItemType.Exp_Activity_Global,
        # BoosterItemType.Jellybeans_Global,
    ]
else:
    debugBoostersToForce = []


def getHolidayBoosterHandler(client=False, ai=False) -> BoosterHandler:
    """Gets a BoosterHandler on the client end."""
    from toontown.toonbase import ToontownGlobals
    holidayToBoostDict = {
        (ToontownGlobals.ACTIVITY_EXPERIENCE_HOLIDAY,
         ToontownGlobals.SILLY_ACTIVITY,): BoosterItemType.Exp_Activity_Global,
        (ToontownGlobals.WEALTHY_WEDNESDAY,
         ToontownGlobals.SILLY_SATURDAY_WEALTHY,): BoosterItemType.Jellybeans_Global,
        (ToontownGlobals.GAG_EXPERIENCE_HOLIDAY,
         ToontownGlobals.SILLY_GAG,
         ToontownGlobals.GAG_EXPERIENCE_HOLIDAY_LTO): BoosterItemType.Exp_Gags_Global,
        (ToontownGlobals.MERIT_HOLIDAY,
         ToontownGlobals.SILLY_MERIT,): BoosterItemType.Merit_Global,
        (ToontownGlobals.BOSS_REWARD_HOLIDAY,
         ToontownGlobals.SILLY_REWARD,): BoosterItemType.Reward_Boss_Global,
        (ToontownGlobals.DEPARTMENT_EXPERIENCE_HOLIDAY,
         ToontownGlobals.SILLY_DEPARTMENT,): BoosterItemType.Exp_Dept_Global,
        ToontownGlobals.NATIONAL_BINGO_DAY_HOLIDAY: BoosterItemType.Jellybeans_Bingo,
        ToontownGlobals.CLASH_BIRTHDAY_DOUBLE_GUMBALLS: BoosterItemType.Gumballs_Global,
    }

    # Add various holiday boosters.
    startTs = TimeUtil.getLastTimestampOfMidnight()
    holidayBoosterHandler = BoosterHandler()
    for holidaySet, booster in holidayToBoostDict.items():
        if type(holidaySet) is not tuple:
            holidaySet = (holidaySet,)

        for holiday in holidaySet:
            if client:
                if not base.cr.newsManager:
                    break
                if base.cr.newsManager.isHolidayRunning(holiday):
                    holidayBoosterHandler.addNewBooster(booster, timeDelta=timedelta(days=1.0), startTs=startTs)
                    break
            elif ai:
                if not simbase.air.holidayManager:
                    break
                if simbase.air.holidayManager.isHolidayRunning(holiday):
                    holidayBoosterHandler.addNewBooster(booster, timeDelta=timedelta(days=1.0), startTs=startTs)
                    break
            else:
                assert client or ai, "you gotta pick one buddy"

    # Add debug boosters, if we so desire.
    if __debug__:
        for booster in debugBoostersToForce:
            holidayBoosterHandler.addNewBooster(booster)

    return holidayBoosterHandler
