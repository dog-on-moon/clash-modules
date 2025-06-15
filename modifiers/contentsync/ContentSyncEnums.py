"""
Enums for Content Sync.
"""
from enum import IntEnum, auto


class ContentSyncType(IntEnum):
    """
    Used to define a type of ContentSync for some sort of instanced content.
    """
    # Generic Cog HQ definitions
    SBHQ = auto()
    CBHQ = auto()
    LBHQ = auto()
    BBHQ = auto()
    BDHQ = auto()

    # Minibosses
    TASKLINE_TTC  = auto()
    TASKLINE_BB   = auto()
    TASKLINE_YOTT = auto()
    TASKLINE_DG   = auto()
    TASKLINE_MML  = auto()
    TASKLINE_TB   = auto()
    TASKLINE_AA   = auto()
    TASKLINE_DDL  = auto()

    STREET_TTC  = auto()
    STREET_BB   = auto()
    STREET_YOTT = auto()
    STREET_DG   = auto()
    STREET_MML  = auto()
    STREET_TB   = auto()
    STREET_AA   = auto()
    STREET_DDL  = auto()

    KUDOS_TTC  = auto()
    KUDOS_BB   = auto()
    KUDOS_YOTT = auto()
    KUDOS_DG   = auto()
    KUDOS_MML  = auto()
    KUDOS_TB   = auto()
    KUDOS_AA   = auto()
    KUDOS_DDL  = auto()

    # Misc
    OCLO = auto()
    EVENT_HIGH_ROLLER = auto()
