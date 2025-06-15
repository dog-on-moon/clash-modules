from direct.showbase.DirectObject import DirectObject

from typing import Union, Optional, List, Tuple, Dict
from typing import TYPE_CHECKING

from toontown.modifiers.Modifier import Modifier
from toontown.modifiers.ModifierClasses import ContentSyncModifiers
from toontown.modifiers.contentsync.ContentSyncDefinitions import ContentSyncDefinitions
from toontown.modifiers.contentsync.ContentSyncEnums import ContentSyncType
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.toon.DistributedToonAI import DistributedToonAI

if TYPE_CHECKING:
    from toontown.ai.ToontownAIRepository import ToontownAIRepository


@DirectNotifyCategory()
class ContentSyncManagerAI(DirectObject):
    """
    A manager class to help manage Content Sync for Toons.

    This class can be invoked with a Toon and Content Sync Enum to apply a sync.
    In addition, it can also be used to clear Content Sync status.
    """

    def __init__(self, air):
        self.air = air  # type: ToontownAIRepository
        self.accept('avatarEntered', self.onAvatarEntered)

    def applyContentSync(self,
                         syncType: ContentSyncType,
                         toons: Union[DistributedToonAI, List[DistributedToonAI]],
                         listenForZone: bool = True,
                         listenForDeath: bool = True,
                         forceOldZone: Optional[int] = None,
                         ignoreThisZone: Optional[int] = None,
                         isLogical: bool = False) -> None:
        """
        Applies a Content Sync modifier onto a Toon(s).

        :param syncType: The type of Content Sync to apply.
        :param toons: The toons to manipulate.
        :param listenForZone: Should Content Sync be cleared when the Toon's zone changes?
        :param listenForDeath: Should Content Sync be cleared when the Toon goes sad?
        :param forceOldZone: When clearing ContentSync on zone change, we must exit THIS zone to clear it.
        :param ignoreThisZone: If indicated, this zone won't be accounted for in zone change events.
        :param isLogical: If True, we will listen to logical zone change instead of normal zone change.
        """
        if not toons:
            return

        # Wrap toons in a list if necessary.
        if not isinstance(toons, (list, tuple, set)):
            toons = [toons]

        # Only affect Toons that do not have Content Sync.
        toons = [toon for toon in toons if not toon.hasModifier(*ContentSyncModifiers)]
        if not toons:
            return self.notify.info(f'Attempted to apply ContentSync onto Toons, but they all had sync already.')

        self.notify.info(f'Applying ContentSync [{syncType.name}] onto Toons: {toons}')

        # Clear content sync off of all toons.
        # We disable notify to avoid confusion.
        self.removeContentSync(toons, update=False)

        # For all toons, apply all modifiers.
        for toon in toons:
            modifiers: List[Modifier] = ContentSyncDefinitions.getModifiersOfSyncType(syncType)
            for modifier in modifiers:
                # We'll only update the Toon's modifier fields if it's the last modifier.
                finalModifier = modifier is modifiers[-1]

                # Add the modifier.
                toon.addModifier(
                    modifier=modifier,
                    update=finalModifier,
                )

            # Listen for events to clear content sync.
            if listenForZone:
                self.listenForZone(toon, forceOldZone=forceOldZone, ignoreThisZone=ignoreThisZone, isLogical=isLogical)

            if listenForDeath:
                self.listenForDeath(toon)

            # Give them a contextual toon tip about Content Sync
            toon.showToonTip(78)

    def removeContentSync(self, toons: Union[DistributedToonAI, List[DistributedToonAI]], update: bool = True) -> None:
        """
        Removes the Content Sync effect from Toon(s).

        :param toons: The toons to manipulate.
        :param update: Are we updating this Toon's modifiers instantly?
        """
        if not toons:
            return

        # Wrap toons in a list if necessary.
        if not isinstance(toons, (list, tuple, set)):
            toons = [toons]

        # Only affect Toons that do have Content Sync.
        toons = [toon for toon in toons if toon.hasModifier(*ContentSyncModifiers)]
        if not toons:
            if update:
                self.notify.info(f'Attempted to removing ContentSync from Toons, but they did not have any.')
            return

        if update:
            self.notify.info(f'Removing ContentSync from Toons: {toons}')

        # Clear content sync off of all toons.
        for toon in toons:
            toon.removeModifierOfType(*ContentSyncModifiers, update=update)
            self.clearEventsForToon(toon)

    """
    Event handling
    """

    def onAvatarEntered(self, toon: DistributedToonAI):
        """When a toon spawns, re-initialize the events, in case they didn't get cleaned up."""
        self.clearEventsForToon(toon)

    def clearEventsForToon(self, toon: DistributedToonAI):
        """
        Clears all listening events on a Toon.

        :param toon: The Toon in question.
        """
        self.ignore(toon.getZoneChangeEvent())
        self.ignore(toon.getLogicalZoneChangeEvent())
        self.ignore(toon.getGoneSadMessage())

    def listenForZone(self, toon: DistributedToonAI, forceOldZone: Optional[int] = None, ignoreThisZone: Optional[int] = None, isLogical: bool = False) -> None:
        """
        Listens for a Toon's zone change.
        If the Zone changes, remove Content Sync.

        :param toon: The Toon in question.
        :param forceOldZone: The oldZone must be THIS value to clear the sync.
        :param ignoreThisZone: The newZone must NOT be this value to clear the sync.
        :param isLogical: Will use logicalZoneChangeEvent instead of ZoneChangeEvent.
        """
        def onZoneChange(newZone, oldZone):
            # When the Zone changes, clear content sync.
            if forceOldZone is not None and forceOldZone != oldZone:
                self.notify.info(f'Detected zone change from {toon}. However, it was not the right oldZone.')
                return
            if ignoreThisZone is not None and newZone == ignoreThisZone:
                self.notify.info(f'Detected zone change from {toon}. However, the new zone was the ignore zone.')
                return
            self.notify.info(f'Detected zone change from {toon}. Removing content sync...')
            self.removeContentSync(toon)

        zoneEvent = toon.getLogicalZoneChangeEvent() if isLogical else toon.getZoneChangeEvent()
        # Listen to the event.
        self.accept(zoneEvent, onZoneChange)

    def listenForDeath(self, toon: DistributedToonAI) -> None:
        """
        Listens for a Toon's death.
        If the Zone changes, remove Content Sync.

        :param toon: The Toon in question.
        """
        def onDeath():
            # When the Toon obliterates, clear content sync.
            self.notify.info(f'Detected DEATH from {toon}. Removing content sync...')
            self.removeContentSync(toon)

        # Listen to the event.
        self.acceptOnce(toon.getGoneSadMessage(), onDeath)
