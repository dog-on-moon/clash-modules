from toontown.gui.EasyManagedItem import EasyManagedItem
from toontown.gui.TTGui import kwargsToOptionDefs
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from direct.gui.DirectGui import *


@DirectNotifyCategory()
class EasyManagedButton(DirectButton, EasyManagedItem):
    """
    Same kwargs as an EasyManagedItem,
    but inherits from DirectButton.
    """

    def __init__(self, parent=aspect2d, **kw):
        optiondefs = kwargsToOptionDefs(
            easyHeight=[0.0, self.easyUpdate],
            easyWidth=[0.0, self.easyUpdate],
            easyPadLeft=[0.0, self.easyUpdate],
            easyPadRight=[0.0, self.easyUpdate],
            easyPadDown=[0.0, self.easyUpdate],
            easyPadUp=[0.0, self.easyUpdate],
            easyXMax=[1.0, self.easyUpdate],
            easyItemCount=[1.0, self.easyUpdate],
            posOffset=[(0, 0, 0), self.updateOffset],
            easyScrolledFrame=[None, self.attachFrame],
        )
        self.defineoptions(kw, optiondefs)
        DirectButton.__init__(self, parent, **kw)
        self.postInitialized = False
        self.postInitialiseFuncList.append(lambda: setattr(self, 'postInitialized', True))
        self.initialiseoptions(EasyManagedButton)

        # Sync with EasyManagedItem's init
        self.oldOffset = self.cget('posOffset')
        self._active = True
