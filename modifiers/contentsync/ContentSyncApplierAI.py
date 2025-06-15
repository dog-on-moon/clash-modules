from typing import Optional, List

from toontown.modifiers.contentsync.ContentSyncEnums import ContentSyncType
from toontown.toon.DistributedToonAI import DistributedToonAI


class ContentSyncApplierAI:
    """
    An AI-sided base class to help apply Content Sync onto Toons for various instances.
    self.air must be defined for this to be functional.
    """

    contentSync_listenForZone  = True  # Flag to determine how the ContentSync should clean up.
    contentSync_listenForDeath = True  # Flag to determine how the ContentSync should clean up.

    def getContentSync(self) -> Optional[ContentSyncType]:
        """
        Figures out the ideal content sync to apply.
        Override this method to set the content sync.
        """
        return None

    def contentSync_getForceOldZone(self) -> Optional[int]:
        """
        If we have the contentSync_listenForZone flag, we will attempt to
        listen to THIS zone to attempt to clear the content sync from Toons.
        If set to None, then any zone change will do.
        """
        return None

    def contentSync_getIgnoreThisZone(self) -> Optional[int]:
        """
        If we have the contentSync_listenForZone flag, we will attempt to
        listen to everything BUT this zone to attempt to clear the content sync from Toons.
        If set to None, then any zone change will do.
        """
        return None

    def contentSync_getZoneChangeIsLogical(self) -> bool:
        """
        If we have the contentSync_listenForZone flag, this determines if the zone change event
        is logical or not. If it is logical, we will ignore QuietZone (1) changes and only listen for
        full-fat zone changes.
        """
        return False

    """
    Application Methods
    
    Call these somewhere in the class, ideally after all the
    Toons are loaded and generated in the right zone.
    """

    def applyContentSync(self, *toons: DistributedToonAI) -> None:
        """
        Applies ContentSync onto toons.
        """
        assert hasattr(self, 'air') and self.air, "self.air must be defined for ContentSync."

        # Make sure something is defined.
        contentSync = self.getContentSync()
        if contentSync is None:
            return

        # If so, apply the sync.
        self.air.contentSyncManager.applyContentSync(
            syncType=contentSync,
            toons=toons,
            listenForZone=self.contentSync_listenForZone,
            listenForDeath=self.contentSync_listenForDeath,
            forceOldZone=self.contentSync_getForceOldZone(),
            ignoreThisZone=self.contentSync_getIgnoreThisZone(),
            isLogical=self.contentSync_getZoneChangeIsLogical(),
        )

    def removeContentSync(self, *toons: DistributedToonAI) -> None:
        """
        Removes ContentSync from toons.
        """
        assert hasattr(self, 'air') and self.air, "self.air must be defined for ContentSync."

        # We must have applied a sync before we attempt to remove it.
        if self.getContentSync() is None:
            return

        # Go through each toon and remove their sync.
        for toon in toons:
            self.air.contentSyncManager.removeContentSync(toon)

    """
    Helper methods
    """

    def avIdsToAvs(self, avIds: List[int]) -> List[DistributedToonAI]:
        """Converts a list of avIds into avs."""
        retlist = []
        for toonId in avIds:
            toon = self.air.doId2do.get(toonId)
            if toon:
                retlist.append(toon)
        return retlist
