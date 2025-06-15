
if __name__ == "__main__":
    from tools.headless.headlessbase import HeadlessStart
    from tools.headless.headlessbase.HeadlessBase import HeadlessBase
    base = HeadlessBase(wantHotkeys=False)
    if __debug__:
        from toontown.utils.DeveloperInjector import startInjector
        startInjector()
    # base.initCR()  # defines base.cr
    # base.startHeadlessShow()

from toontown.gui.AutoCloseButton import AutoCloseButton
from toontown.gui import TTGui
from toontown.gui.GUITemplateSliders import GUITemplateSliders
from toontown.gui.GUINode import GUINode
from toontown.gui.CornerAnchor import CornerAnchor
from toontown.gui import UiHelpers
from toontown.gui.EasyManagedItem import EasyManagedItem
from toontown.gui.EasyManagedButton import EasyManagedButton
from toontown.gui.EasyScrolledFrame import EasyScrolledFrame
from toontown.gui.Bounds import Bounds
from toontown.gui.GUIPositionGlobals import ScreenCorner
from toontown.gui.ScaledFrame import ScaledFrame
from toontown.toon.gui import GuiBinGlobals
from toontown.toonbase import ToontownGlobals

from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.InjectorTarget import InjectorTarget
from toontown.utils import ColorHelper
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase import PythonUtil
from direct.fsm.FSM import FSM
from typing import Optional, List, Tuple, Dict, Set, TYPE_CHECKING
if TYPE_CHECKING:
    from toontown.utils.InjectorHelper import *


@DirectNotifyCategory()
class TabbedScaledFrame(ScaledFrame):
    """
    A scaled frame with native tab support.
    """

    @InjectorTarget
    def __init__(self, parent, **kw):
        # GUI boilerplate.
        self._closeButton = None
        optiondefs = TTGui.kwargsToOptionDefs(
            pos = (0, 0, 0),
            scale = 1.0,
            bin = GuiBinGlobals.TabbedScaleFrameDefault,
            frameSize=(-0.5, 0.5, -0.15, 0.15),

            # Tab definitions
            tabs = [
                (  # tab names must begin with a capital letter
                    ('Tab1', '880000'),
                    ('Tab2', '008800'),
                    ('Tab3', '000088'),
                ),
                self._createTabs,
            ],
            tabDistance = [0.06573, self._replaceTabs],
            selectedTabDistance = [0.03, self._replaceTabs],
            tabOffset = [0.0, self._replaceTabs],
            tabStart = [ScreenCorner.TOP_LEFT, self._replaceTabs],
            tabEnd = [ScreenCorner.TOP_RIGHT, self._replaceTabs],
            tabWidth = [0.22, self._replaceTabs],
            autoTabWidth = [False, self._replaceTabs],
            tabSpacing = [0.00, self._replaceTabs],
            tabTextPos = [(0, 0.01147), self._replaceTabs],
            tabTextScale = [0.05227, self._replaceTabs],
            tabTextColor = [(1, 1, 1, 1), self._replaceTabs],
            defaultFrameSize=[(-0.5, 0.5, -0.15, 0.15), self._replaceTabs],
            tabFrameSizes=[{}, self._replaceTabs],

            hasCloseButton = True,
            closeButtonCmd = self.destroy,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.postInitialized = False
        self.postInitialiseFuncList.append(lambda: setattr(self, 'postInitialized', True))
        self.initialiseoptions(TabbedScaledFrame)
        self.setBin('sorted-gui-popup', self['bin'])
        self['state'] = DGG.NORMAL

        # FSM states.
        self._tabFSM = None
        self._fsmReady: bool = False

        # Create tab objects.
        self._tabs: list[EasyManagedButton] = []
        self._tabNodes: list[GUINode] = []
        self._createTabs()

        # Late gen a close button.
        if self['hasCloseButton']:
            self._closeButton = AutoCloseButton(self, scale=1.5, command=self['closeButtonCmd'])

    def destroy(self):
        self._tabFSM.cleanup()
        self._tabFSM = None
        self._tabs = []
        self._tabNodes = []
        self._closeButton = None
        super().destroy()

    """
    Tab Initialization
    """

    def _createTabs(self):
        if not hasattr(self, '_tabs'):
            return

        # Cleanup old tabs.
        for tab in self._tabs:
            tab.destroy()
        self._tabs = []
        for node in self._tabNodes:
            node.destroy()
        self._tabNodes = []

        # Create new ones.
        self._tabs = [
            EasyManagedButton(
                parent=self,  # relief=None,
                command=self.requestTab,
                extraArgs=[tabName],
                text='',
                text_align=TextNode.ACenter,
            )
            for tabName in self.getTabNames()
        ]
        self._tabNodes = [GUINode(parent=self, frameSize=(0, 0, 0, 0)) for tabName in self.getTabNames()]
        for node in self._tabNodes:
            node.hide()

        # The rest of the setup.
        self.__setupTabFsm()
        if self.getTabNames():
            self.requestTab(self.getInitialTab())
            self.__sortBins()

    def _replaceTabs(self) -> bool:
        if not hasattr(self, '_tabs'):
            return False

        # Set frame size.
        self['frameSize'] = self['tabFrameSizes'].get(self.getActiveTab(), self['defaultFrameSize'])

        # Determine placement constants.
        left, right, down, up = self.getDefinedBounds()
        tabWidth = self['tabWidth'] if not self['autoTabWidth'] else self.getBoundWidth() / self.getTabCount()

        # Place them nowsies.
        if self['tabStart'] == ScreenCorner.TOP_LEFT and self['tabEnd'] == ScreenCorner.TOP_RIGHT:
            for i in range(self.getTabCount()):
                # Set tab attributes.
                tabName, tabCol = self.getTabData(i)
                tab: EasyManagedButton = self._tabs[i]
                tab['easyWidth'] = tabWidth + self['tabSpacing']
                tab['frameSize'] = (0, tabWidth, -self['tabDistance'], self['tabDistance'])
                tab['frameColor'] = ColorHelper.hexToPCol(tabCol)
                tab['text'] = tabName

                x, z = self['tabTextPos']
                tab['text_pos'] = ((tabWidth / 2) + x, z)
                tab['text_scale'] = self['tabTextScale']
                tab['text_fg'] = self['tabTextColor']

            # And position them.
            UiHelpers.fillGridWithElements(
                initialGuiList=self._tabs,
                horizontalCount=self.getTabCount(),
                verticalCount=1,
                startPos=(left + self['tabOffset'], 0, up + self['tabDistance']),
                startCorner=ScreenCorner.TOP_LEFT,
                expandMode=UiHelpers.GridType.HorizontalFirst,
            )

            # Move selected tab up a bit.
            if self._fsmReady:
                activeTab = self._tabs[self.getTabIndex(self.getActiveTab())]
                x, y, z = activeTab.getPos()
                activeTab.setPos(x, y, z + self['selectedTabDistance'])
        elif self['tabStart'] == ScreenCorner.TOP_LEFT and self['tabEnd'] == ScreenCorner.BOTTOM_LEFT:
            for i in range(self.getTabCount()):
                # Set tab attributes.
                tabName, tabCol = self.getTabData(i)
                tab: EasyManagedButton = self._tabs[i]
                tab['easyHeight'] = -tabWidth - self['tabSpacing']
                tab['frameSize'] = (-self['tabDistance'], self['tabDistance'], -tabWidth, 0)
                tab['frameColor'] = ColorHelper.hexToPCol(tabCol)
                tab['text'] = tabName

                x, z = self['tabTextPos']
                tab['text_pos'] = (x, z - (tabWidth / 2))
                tab['text_align'] = TextNode.ARight
                tab['text_scale'] = self['tabTextScale']
                tab['text_fg'] = self['tabTextColor']

            # And position them.
            UiHelpers.fillGridWithElements(
                initialGuiList=self._tabs,
                horizontalCount=1,
                verticalCount=self.getTabCount(),
                startPos=(left, 0, up - self['tabOffset']),
                startCorner=ScreenCorner.TOP_LEFT,
                expandMode=UiHelpers.GridType.HorizontalFirst,
            )

            # if not hasattr(base, 'sadfghj'):
            #     base.sadfghj = True
            #     GUITemplateSliders(
            #         self,
            #         'tabOffset', 'tabDistance', 'selectedTabDistance',
            #         'tabTextPos', 'tabWidth',
            #         scale = 0.25,
            #     )

            # Move selected tab up a bit.
            if self._fsmReady:
                activeTab = self._tabs[self.getTabIndex(self.getActiveTab())]
                x, y, z = activeTab.getPos()
                activeTab.setPos(x - self['selectedTabDistance'], y, z)
        else:
            # Haven't figured out the others yet >:3
            raise NotImplementedError

        for tab in self.getTabNames():
            tabNode = self.getTabNode(tab)
            tabNode['frameSize'] = self['frameSize']

        # Lol
        if self._closeButton:
            self._closeButton.place()

        # Virtual call here
        self.onTabReplace()
        return True

    """
    Tab Actions
    """

    def requestTab(self, tabName: str):
        """
        Requests the scaled frame to transition into a given tab.
        """
        if tabName == self._tabFSM.state:
            return
        self._tabFSM.request(tabName)
        self._fsmReady = True
        self._replaceTabs()

    """
    Tab Virtuals
    """

    def onTabEnter(self, tabName: str):
        pass

    def onTabExit(self, tabName: str):
        pass

    def onTabReplace(self):
        pass

    """
    Tab Internals
    """

    def __setupTabFsm(self):
        def enterFunc(*_):
            self.getTabNode(self._tabFSM.newState).show()
            self.onTabEnter(self._tabFSM.newState)
            self.__setTabStates()

        def exitFunc(*_):
            self.getTabNode(self._tabFSM.oldState).hide()
            self.onTabExit(self._tabFSM.oldState)

        if self._tabFSM:
            self._tabFSM.cleanup()
            self._tabFSM = None

        self._tabFSM = FSM('TabFSM')
        self._fsmReady = False
        for tabName in self.getTabNames():
            setattr(self._tabFSM, f'enter{tabName}', enterFunc)
            setattr(self._tabFSM, f'exit{tabName}', exitFunc)

    def __sortBins(self):
        tabOrder = self._tabs[:]
        mainTab = tabOrder.pop(self.getTabIndex(self.getActiveTab()))
        tabOrder.insert(0, mainTab)
        for i, tab in enumerate(tabOrder):
            tab.setBin('sorted-gui-popup', self['bin'] - 1 - i)
        for tabNode in self._tabNodes:
            tabNode.setBin('sorted-gui-popup', self['bin'] + 1)

    def __setTabStates(self):
        activeTab = self.getActiveTab()
        for i in range(self.getTabCount()):
            self._tabs[i]['state'] = DGG.DISABLED if self.getTabName(i) == activeTab else DGG.NORMAL

    """
    Tab Getters
    """

    def getTabNode(self, tabName: str) -> GUINode:
        """
        Returns a GUINode of a given tabName.
        These are the intended parents for GUI on each tab page.
        """
        return self._tabNodes[self.getTabIndex(tabName)]

    def getAllTabNodes(self) -> list[GUINode]:
        return self._tabNodes

    def getTabIndex(self, tabName: str) -> int:
        for i in range(self.getTabCount()):
            if self.getTabName(i) == tabName:
                return i
        raise KeyError(f'{tabName} not in {self.getTabNames()}')

    def getTabData(self, tabIndex: int) -> tuple:
        assert 0 <= tabIndex < self.getTabCount()
        return self['tabs'][tabIndex]

    def getTabCount(self) -> int:
        return len(self['tabs'])

    def getTabNames(self) -> list[str]:
        return [tabData[0] for tabData in self['tabs']]

    def getTabName(self, tabIndex: int) -> str:
        return self['tabs'][tabIndex][0]

    def getInitialTab(self) -> str:
        return self.getTabNames()[0]

    def getActiveTab(self) -> str:
        return self._tabFSM.state


if __name__ == "__main__":
    gui = TabbedScaledFrame(
        parent=aspect2d,
        # any kwargs go here
    )
    GUITemplateSliders(
        gui,
        'tabDistance', 'tabOffset',
        'tabWidth', 'tabTextPos', 'tabTextScale', 'tabTextColor',
        'selectedTabDistance', 'frameSize',
        scale=0.2,
    )
    base.run()
