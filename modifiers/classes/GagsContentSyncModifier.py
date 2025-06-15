from typing import Any, Optional, List

from toontown.battle import BattleGlobals
from toontown.modifiers.Modifier import Modifier
from toontown.modifiers.ModifierEnums import ModifierType

from toontown.toon.GagInventoryBase import GagInventoryBase

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from toontown.toon.DistributedToonAI import DistributedToonAI
    from toontown.modifiers.ModifiableDOBase import ModifiableDOBase


class GagsContentSyncModifier(Modifier):
    def __init__(self, maxGagLevel: int = 7, maxTrackAccLevel: Optional[int] = None,
                 forceMaxed: bool = False, clearInventory: bool = False):
        super().__init__([maxGagLevel, int(forceMaxed)])

        # We cache the Toon's old and new inventory.
        self.oldInventory: Optional[GagInventoryBase] = None
        self.newInventory: Optional[GagInventoryBase] = None
        self.excessGags: List[int] = [0] * len(BattleGlobals.Tracks)
        self.maxTrackAccLevel: Optional[int] = maxTrackAccLevel
        self.clearInventory = clearInventory

    def modify(self, value: Any, do, context: Optional[int] = None) -> Any:
        """
        Given an inventory (as value), we perform an operation to content-sync the gags down to level.
        :type do: DistributedToonAI
        """

        # Some type hinting.
        value: GagInventoryBase

        # Get some useful constants.
        maxGagLevel = self.getMaxGagLevel()

        # First, zero out this inventory. Bye.
        value.zeroInv()

        if self.clearInventory:
            # Their inventory will remain cleared.
            return value

        # Now, take our old inventory, and move over ALL unrestricted tracks.
        for track in range(len(BattleGlobals.Tracks)):
            for level in range(maxGagLevel + 1):
                carryLimit = BattleGlobals.CarryLimits[track][maxGagLevel][level]
                # Take the items in the old inventory...
                amount = self.oldInventory.numItem(track=track, level=level)

                # ... and move them into the new.
                value.setItem(track=track, level=level, amount=min(amount, carryLimit))

        # Now, let's go ahead and go through the restricted tracks.
        # We'll restock tracks at-level with all gags in the higher levels.
        for track in range(len(BattleGlobals.Tracks)):
            # First, figure out how many gags we can restock.
            amount = sum(
                self.oldInventory.numItem(track=track, level=level)
                for level in range(maxGagLevel + 1, BattleGlobals.LAST_REGULAR_GAG_LEVEL + 1)
            )

            # With this, we tell the inventory to restock up to the gag level.
            leftovers = value.restockTrack(
                track=track,
                maxLevel=maxGagLevel,
                amount=amount,
                reduceCarryLimits=True,
                removeExcess=True,
            )

            # Keep track of the leftovers.
            self.excessGags[track] = leftovers

        # Return our new inventory.
        return value

    def getMaxGagLevel(self) -> int:
        return self.arguments[0]

    def getForceMaxed(self) -> bool:
        return bool(self.arguments[1])

    def getMaxTrackAccLevel(self) -> int:
        if self.maxTrackAccLevel:
            return self.maxTrackAccLevel
        return self.getMaxGagLevel()

    """
    Static methods
    """

    @staticmethod
    def capGagLevel(do, cap=BattleGlobals.MAX_LEVEL_INDEX) -> int:
        """
        Given a ModifiableDO, caps the gag level.
        :type do: ModifiableDOBase
        :type cap: The cap to be reduced.
        """
        for inventoryModifier in do.getModifiersOfType(ModifierType.GagsContentSync):
            if inventoryModifier.getForceMaxed():
                # The max gag level is being forced to be maxed.
                return BattleGlobals.MAX_LEVEL_INDEX
            else:
                # Set the cap to be either our current gag level or the one the modifier wants to be.
                cap = min(cap, inventoryModifier.getMaxGagLevel())
        return cap

    @staticmethod
    def capTrackAccuracyLevel(do, cap=BattleGlobals.MAX_LEVEL_INDEX) -> int:
        """
        Given a ModifiableDO, caps the track accuracy.
        :type do: ModifiableDOBase
        :type cap: The cap to be reduced.
        """
        for inventoryModifier in do.getModifiersOfType(ModifierType.GagsContentSync):
            cap = min(cap, inventoryModifier.getMaxTrackAccLevel())
        return cap

    """
    Some state stuff
    """

    def onModifierPostAddAI(self, do) -> None:
        """:type do: DistributedToonAI"""
        # Cache the toon's inventory in our sync modifier.
        # Make a new object -- we need a different inventory for sure.
        self.oldInventory = do.inventory.duplicate()

        # Now, update the DO's inventory with a modified variant.
        do.b_setInventory(self.modify(value=do.inventory, do=do).makeNetString())

        # Cache a new inventory for reference later.
        self.newInventory = do.inventory.duplicate()

    def onModifierPostRemoveAI(self, do) -> None:
        """:type do: DistributedToonAI"""
        # We need to do a lot of crazy stuff here.
        # We'll have to compare the gags used from the current inventory to the new inventory,
        # and then use that to calculate what gags we take away from the old inventory,
        # and then give *that* old inventory back to the toon.
        if not hasattr(do, 'inventory') or not do.inventory:
            # Inventory cleaned up? Avoid district reset
            return
        if not self.oldInventory:
            return
        currentInventory = do.inventory  # type: GagInventoryBase
        self.oldInventory.calcTotalProps()

        # If we originally cleared their inventory for this sync,
        # just give them back their regular inventory.
        if self.clearInventory:
            do.b_setInventory(self.oldInventory.makeNetString())

        # Only do this if the Toon has gags (i.e. they didn't go sad).
        elif currentInventory.totalProps != 0:
            # Modify the old inventory and remove the expected items.
            # Accumulate total gags we have to remove over the whole inventory.
            gagsToRemove = 0
            for track in range(len(BattleGlobals.Tracks)):
                if not do.hasGagTrack(track):
                    continue

                # If we had excess gags in this track, we won't have to remove as many.
                # gagsToRemove -= self.excessGags[track]

                # Now, go through every single level.
                for level in range(BattleGlobals.LAST_REGULAR_GAG_LEVEL):
                    # Figure out how many gags we'll need to remove here.
                    startItems = self.newInventory.numItem(track=track, level=level)
                    finalItems = currentInventory.numItem(track=track, level=level)
                    gagsToRemove += (startItems - finalItems)

                    # Remove as many gags as possible at this current
                    # track & level from the old inventory.
                    while True:
                        # Break if we are out of gags.
                        if gagsToRemove <= 0:
                            break

                        else:
                            # Use an item. If we couldn't remove it, break.
                            result = self.oldInventory.useItem(track=track, level=level, fullRecalcProps=False)
                            if result != 1:
                                break

                            # Decrement the amount of gags we have to remove.
                            gagsToRemove -= 1

                # If we have excess gags, give them back from top going down.
                # if gagsToRemove < 0:
                #     leftovers = self.oldInventory.restockTrack(
                #         track=track,
                #         amount=-gagsToRemove,
                #     )
                #     gagsToRemove = -leftovers

            # Give the old inventory back to the Toon.
            do.b_setInventory(self.oldInventory.makeNetString())

        # Cleanup our state.
        self.oldInventory = None
        self.newInventory = None
        self.excessGags: List[int] = [0] * len(BattleGlobals.Tracks)
