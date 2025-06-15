from enum import Enum, auto

from panda3d.core import NodePath

from toontown.gui.WorldGUI import WorldGUI
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
from typing import Optional, List, Tuple, Dict, Set, TYPE_CHECKING
if TYPE_CHECKING:
    from toontown.utils.InjectorHelper import *


class WorldInteractionService(WorldGUI):
    """
    A useful class for helping to connect clear, concise interaction confirmations.
    """

    TASK_SPEED = 0.04

    class DisableFlag(Enum):
        DOOR_TRANSITION = auto()

    class NodeData:

        def __init__(self, np, actions: dict[str, tuple[str, callable]], distance: float,
                     enterCallback: callable, exitCallback: callable,
                     targetNode: NodePath | None,
                     screenOffset: tuple[float, float, float] = (0, 0, 0),
                     worldOffset: tuple[float, float, float] = (0, 0, 0)):
            self.np = np
            self.actions = actions
            self.distance = distance
            self.enterCallback = enterCallback
            self.exitCallback = exitCallback
            self.targetNode = targetNode
            self.screenOffset = screenOffset
            self.worldOffset = worldOffset

        def doEnterCallback(self):
            if self.enterCallback:
                self.enterCallback()

        def doExitCallback(self):
            if self.exitCallback:
                self.exitCallback()

    def __init__(self, parent=aspect2d, **kw):
        # GUI boilerplate.
        optiondefs = TTGui.kwargsToOptionDefs(
            relief=None,
            pos=(0, 0, 0),
            scale=1.0,

            text='',
            text_scale=0.07,
            text_fg=(1, 1, 1, 1),
            text_bg=(0, 0, 0, 0.5),
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.postInitialized = False
        self.postInitialiseFuncList.append(lambda: setattr(self, 'postInitialized', True))
        self.initialiseoptions(WorldInteractionService)
        self.hide()

        self.current: WorldInteractionService.NodeData | None = None
        self.collOwns: bool = False

        self.activeNode: NodePath | None = None
        self.activeColl: NodePath | None = None

        self.nodeRegistry: dict[NodePath, WorldInteractionService.NodeData] = {}
        self.collRegistry: dict[NodePath, WorldInteractionService.NodeData] = {}
        self.flags: set[WorldInteractionService.DisableFlag] = set()

        self._startLoop()

        self.accept('zoneChange', self.clear)

    def destroy(self):
        self.ignoreAll()
        self._endLoop()
        del self.current
        del self.nodeRegistry
        del self.collRegistry
        del self.flags
        super().destroy()

    def show(self):
        if self.flags:
            self.hide()
        else:
            super().show()

    def clear(self, *_):
        self.current = None
        self.collOwns = False
        self.activeNode = None
        self.activeColl = None
        self.nodeRegistry = {}
        self.collRegistry = {}
        self.flags = set()

    def addFlag(self, flag: DisableFlag):
        """Adds a flag to the WIS, disabling its functionality."""
        self.flags.add(flag)
        self.show()

    def removeFlag(self, flag: DisableFlag):
        """Removes a flag from the WIS, re-enabling its functionality."""
        self.flags.discard(flag)
        self.show()

    """
    Interface
    """

    def addNode(self, np, actions: dict[str, tuple[str, callable]] = None, distance: float = 5.0,
                enterCallback: callable = None, exitCallback: callable = None,
                targetNode: NodePath | None = None,
                screenOffset: tuple[float, float, float] = (0, 0, 0),
                worldOffset: tuple[float, float, float] = (0, 0, 0)):
        """
        Registers a NodePath in the WIS.

        When the player is within distance of it, GUI will appear at its location,
        providing context for which actions are available.
        """
        if callable(actions):
            actions = actions()
        self.nodeRegistry[np] = self.NodeData(np, actions or {}, distance, enterCallback, exitCallback, targetNode, screenOffset, worldOffset)

    def removeNode(self, np):
        """
        Removes a NodePath from the WIS.
        """
        if np not in self.nodeRegistry:
            return
        if self.activeNode == np:
            del self.nodeRegistry[np]
            self._evaluateClosestNode()
        else:
            self._evaluateClosestNode()

    def addCollision(self, np, actions: dict[str, tuple[str, callable]] = None,
                     enterCallback: callable = None, exitCallback: callable = None,
                     targetNode: NodePath | None = None,
                     screenOffset: tuple[float, float, float] = (0, 0, 0),
                     worldOffset: tuple[float, float, float] = (0, 0, 0)):
        """
        Registers a CollisionNode in the WIS.
        This is similar to adding a node, but with a bit more compatability,
        since any kind of silly collision shape can be used here.
        """
        if callable(actions):
            actions = actions()
        self.collRegistry[np] = self.NodeData(np, actions or {}, 0, enterCallback, exitCallback, targetNode, screenOffset, worldOffset)

        collName = np.getName()
        self.accept(f'enter{collName}', lambda *_: self.__enterCollision(np))
        self.accept(f'exit{collName}', lambda *_: self.__exitCollision(np))

    def removeCollision(self, np):
        """
        Removes a CollisionNode from the WIS.
        """
        if np not in self.collRegistry:
            return
        del self.collRegistry[np]

        collName = np.getName()
        self.ignore(f'enter{collName}')
        self.ignore(f'exit{collName}')
        self.__exitCollision(np)

    """
    Internal logic
    """

    def _startLoop(self):
        taskMgr.add(self._taskLoop, 'worldInteractionService')

    def _endLoop(self):
        taskMgr.remove('worldInteractionService')

    def _taskLoop(self, task=None):
        if self.collOwns:
            if not self.activeColl:
                self.activeColl = None
                self._evaluateClosestNode()
        else:
            self._evaluateClosestNode()
        if task:
            task.delayTime = self.TASK_SPEED
            return task.again

    def _evaluateClosestNode(self):
        oldNode = self.activeNode
        self.activeNode = self.getNearestNode()

        if oldNode == self.activeNode:
            return

        oldData = self.nodeRegistry.get(oldNode)
        if oldData:
            oldData.doExitCallback()
        newData = self.nodeRegistry.get(self.activeNode)
        if newData:
            newData.doEnterCallback()
        self.set(newData)

    def __enterCollision(self, np):
        self.activeColl = np
        self.collOwns = True
        self.activeNode = None
        nodeData = self.collRegistry.get(np)
        nodeData.doEnterCallback()
        self.set(nodeData)

    def __exitCollision(self, np):
        if np == self.activeColl:
            self.activeColl = None
            self.collOwns = False
            self.set(None)
            nodeData = self.collRegistry.get(np)
            nodeData.doExitCallback()
            self._evaluateClosestNode()

    """
    GUI Function
    """

    def set(self, nodeData: NodeData | None):
        # Update data.
        if self.current:
            for key, actions in self.current.actions.items():
                self.ignore(key)
        self.current = nodeData

        # No data => just hide
        if not nodeData:
            # Bye bye!!
            self.setTarget(None)
            self.hide()
            return

        # Set the GUI to match the active nodeData.
        self.setTarget(nodeData.targetNode or nodeData.np)
        if nodeData.actions:
            self.show()
            self['text'] = '\n'.join(f'[{key.upper()}] {actions[0]}' for key, actions in nodeData.actions.items())
            self['screenOffset'] = nodeData.screenOffset
            self['worldOffset'] = nodeData.worldOffset
            for key, actions in nodeData.actions.items():
                self.accept(key, lambda *_: actions[1]())

    """
    Node Searching
    """

    def getNearestNode(self) -> NodePath | None:
        """Hunts for the Node closest to the player."""
        if not hasattr(base, 'localAvatar') or not base.localAvatar:
            return None

        # Find nearest nodes and
        clearNodes = []
        nearestNode = None
        closestDistance = 129837
        for np, nd in self.nodeRegistry.items():
            if not np:
                clearNodes.append(np)
                continue
            distance = np.getDistance(base.localAvatar)
            if distance < closestDistance and distance < nd.distance:
                nearestNode = np
                closestDistance = distance
        for np in clearNodes:
            del self.nodeRegistry[np]
        return nearestNode
