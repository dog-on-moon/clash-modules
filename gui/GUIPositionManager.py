"""
A class to finely monitor the positions of all on-screen GUI.
"""
from direct.showbase.DirectObject import DirectObject
from toontown.gui.GUIPositionGlobals import *
from panda3d.core import NodePath

from toontown.gui.PositionedGUI import OnscreenPositionData


class GUIPositionManager(DirectObject):
    """
    A class that can be given various GUI elements.
    With them, it will attempt to make sure that their positions onscreen are
    good/valid/rational (as expected).
    """

    MOVE_SPEED = 0.0

    def __init__(self):
        # GUI containers.
        self.managedGui = {screenCorner: [] for screenCorner in ScreenCorner}
        self.activeMovementSequences = {screenCorner: [] for screenCorner in ScreenCorner}

        # Accept calls asking to update.
        self.accept(MSG_UPDATE_POSITION_MANAGER, self.__updateCorner)

        # Task to ensure we update when aspect ratio changes.
        self.lastAspectRatio = base.getAspectRatio()
        taskMgr.add(self.checkAspectRatio, 'gui-position-mgr-check-aspect-ratio')

    @staticmethod
    def getScreenCornerParents():
        return {
            ScreenCorner.TOP_LEFT: base.a2dTopLeft,
            ScreenCorner.TOP_RIGHT: base.a2dTopRight,
            ScreenCorner.BOTTOM_LEFT: base.a2dBottomLeft,
            ScreenCorner.BOTTOM_RIGHT: base.a2dBottomRight,
        }

    def checkAspectRatio(self, task):
        if task.time % 50:
            # don't oversaturate
            yield task.cont
        ratio = base.getAspectRatio()
        if ratio != self.lastAspectRatio:
            self.updateAll(instant=True)
            self.lastAspectRatio = ratio
        return task.cont

    """
    Accessors
    """

    def __findGui(self, gui):
        """
        Looks for a GUI currently being managed.
        :param gui: The GUI element to hunt for.
        :return:    The corner that it is at, or None.
        """
        for corner, guiList in self.managedGui.items():
            for managedGuiTuple in guiList:
                managedGui = managedGuiTuple[1]
                if gui is managedGui:
                    return corner
        return None

    def __findGuiIndex(self, gui):
        """Gets the GUI corner and index."""
        corner = self.__findGui(gui)
        if not corner:
            return None, None
        for i, managedGuiTuple in enumerate(self.managedGui[corner]):
            managedGui = managedGuiTuple[1]
            if gui is managedGui:
                return corner, i
        return corner, None

    """
    Adding and removing GUI
    """

    def manageGui(self, gui, index: int = 0,
                  corner: ScreenCorner = ScreenCorner.TOP_RIGHT,
                  sequence: callable = ManagedGUIEnterSequence.instant,
                  sequenceArgs: list = None,
                  callback: callable = None) -> None:
        """
        Starts managing a GUI element on-screen.

        :param gui:          The GUI element to manage.
        :param index:        The GUI index to insert into.
        :param corner:       The corner where the GUI belongs.
        :param sequence:     The way the GUI should enter upon being managed.
        :param sequenceArgs: Arguments for the sequence.
        :param callback:     Once the sequence finishes, performs this callback.
        :return: None.
        """
        if not sequenceArgs:
            sequenceArgs = []

        # No double manage
        if self.__findGui(gui):
            return

        # Start managing this GUI. Place it on a given node.
        guiElement = gui.getGuiElement()
        guiNode = self.getScreenCornerParents().get(corner).attachNewNode(f'managed-gui-node-{guiElement.getName()}')
        guiElement.reparentTo(guiNode)
        self.managedGui[corner].insert(index, (guiNode, gui))

        # Update this corner.
        self.__cleanupSequencesAtCorner(corner=corner)
        self.__updateCorner(corner, instantGui=gui)

        # Perform the movement sequence for this GUI.
        callbackFunc = Sequence()
        if callback:
            callbackFunc = Func(callback)
        guiMovementSeq = Sequence(
            sequence(gui=gui, args=sequenceArgs),
            callbackFunc,
        )
        self.activeMovementSequences[corner].append(guiMovementSeq)
        guiMovementSeq.start()

    def unmanageGui(self, gui,
                    sequence: callable = ManagedGUIExitSequence.instant,
                    sequenceArgs: list = None,
                    callback: callable = None) -> None:
        """
        Stops managing a GUI element on-screen.

        :param gui:          The GUI element to stop managing.
        :param sequence:     The way the GUI should leave before unmanaging.
        :param sequenceArgs: Arguments for the sequence.
        :param callback:     Once the sequence finishes, performs this callback.
        :return:             None.
        """
        if not sequenceArgs:
            sequenceArgs = []

        # Figure out where this GUI is.
        corner, i = self.__findGuiIndex(gui)
        if corner is None:
            return

        # Perform the movement sequence for this GUI.
        self.__cleanupSequencesAtCorner(corner=corner)

        callbackFunc = Sequence()
        if callback:
            callbackFunc = Func(callback)
        guiMovementSeq = Sequence(
            sequence(gui=gui, args=sequenceArgs),
            callbackFunc,
            Func(self.__updateGUIStatus),
        )
        self.activeMovementSequences[corner].append(guiMovementSeq)
        guiMovementSeq.start()

        # Remove GUI from management.
        # Do a sanity check in case of race conditions (game close)
        if 0 <= i < len(self.managedGui[corner]):
            self.managedGui[corner].pop(i)

        # Update this corner.
        self.__updateCorner(corner, ignoreGui=gui)

    def moveGuiToIndex(self, gui, index: int) -> None:
        """
        Moves some GUI to a given index.
        :param gui:   The GUI to move.
        :param index: The index to move the GUI to.
        :return: None.
        """
        # Get the GUI's current position.
        corner, currentIndex = self.__findGuiIndex(gui)

        # Make sure they are real.
        if corner is None or currentIndex is None:
            return

        # Do a lil' list schmovin.
        guiList = self.managedGui[corner]
        managedGuiTuple = guiList.pop(currentIndex)
        guiList.insert(index, managedGuiTuple)

        # Update the GUI if they're active.
        if gui.onscreenPositionActive():
            self.__updateCorner(corner)

    """
    GUI updating
    """

    def updateAll(self, instant=True):
        """
        Called when we want to update all the GUI positions.
        """
        for corner in ScreenCorner:
            self.__updateCorner(corner, instant=instant)

    def __updateCorner(self, corner: ScreenCorner,
                       ignoreGui=None, instantGui=None,
                       instant: bool = False) -> None:
        """
        Validates the positions of all on-screen GUI.
        :param corner:     The corner to update all GUI within.
        :param ignoreGui:  If we're adding/removing GUI, we should not position it quite yet.
        :param instantGui: Does this GUI get placed instantly?
        :param instant:    Do all GUIs get placed instantly?
        """
        # For all the GUI at this corner, we sit and figure out
        # where it all is supposed to be.
        guiNodePlacements = {}
        instantNode = None

        # Placement constants.
        # h_* represents where this GUI belongs scaling horizontally.
        # v_* represents where this GUI belongs scaling vertically.
        h_xpos = 0.0
        h_ypos = 0.0
        v_xpos = 0.0
        v_ypos = 0.0

        # We only care about active gui.
        activeGui = []
        for guiTuple in self.managedGui[corner]:
            gui = guiTuple[1]
            if gui.onscreenPositionActive():
                activeGui.append(guiTuple)

        # If we have GUI here, we should sort it.
        initialGui = []
        horizontalGui = []
        verticalGui = []
        if activeGui:
            # Begin sorting the GUI.
            # First, we take the GUI at the 0th index and leave it at the 0th index.
            # It is important that it stays there.
            initialGui.append(activeGui[0])

            # Now, we're gonna go ahead and add the
            # horizontal and vertical GUI elements.
            for guiTuple in activeGui[1:]:
                gui = guiTuple[1]
                listToAdd = verticalGui if gui.extendsVertical() else horizontalGui
                listToAdd.append(guiTuple)

        # Add all of the horizontal GUI elements.
        for node, gui in initialGui + horizontalGui:
            # When debugging, we ask the GUI to render themselves for testing
            gui.renderDebugMargins()

            # Is this one moving instantly?
            if gui is instantGui:
                instantNode = node

            # Get the bounds.
            bounds: OnscreenPositionData = gui.onscreenPositionBounds()

            # We account for GUI scale too.
            xscale, yscale = gui.getXYScale()

            # Get the xpos/ypos before placing if necessary.
            if corner == ScreenCorner.TOP_LEFT:
                h_xpos += bounds.left * xscale
                h_ypos = -bounds.top * yscale
            elif corner == ScreenCorner.TOP_RIGHT:
                h_xpos -= bounds.right * xscale
                h_ypos = -bounds.top * yscale
            elif corner == ScreenCorner.BOTTOM_LEFT:
                h_xpos += bounds.left * xscale
                h_ypos = bounds.down * yscale
            elif corner == ScreenCorner.BOTTOM_RIGHT:
                h_xpos -= bounds.right * xscale
                h_ypos = bounds.down * yscale

            # This node goes here.
            if gui is not ignoreGui:
                guiNodePlacements[node] = (h_xpos, h_ypos)

            # Shift the xpos/ypos now as necessary.
            if corner == ScreenCorner.TOP_LEFT:
                h_xpos += bounds.width * xscale
                h_xpos += bounds.right * xscale
            elif corner == ScreenCorner.TOP_RIGHT:
                h_xpos -= bounds.width * xscale
                h_xpos -= bounds.left * xscale
            elif corner == ScreenCorner.BOTTOM_LEFT:
                h_xpos += bounds.width * xscale
                h_xpos += bounds.right * xscale
            elif corner == ScreenCorner.BOTTOM_RIGHT:
                h_xpos -= bounds.width * xscale
                h_xpos -= bounds.left * xscale

        # Add all of the vertical GUI elements.
        for node, gui in initialGui + verticalGui:
            # When debugging, we ask the GUI to render themselves for testing
            gui.renderDebugMargins()

            # Is this one moving instantly?
            if gui is instantGui:
                instantNode = node

            # Get the bounds.
            bounds: OnscreenPositionData = gui.onscreenPositionBounds()

            # We account for GUI scale too.
            xscale, yscale = gui.getXYScale()

            # Get the xpos/ypos before placing if necessary.
            if corner == ScreenCorner.TOP_LEFT:
                v_xpos = bounds.left * xscale
                v_ypos -= bounds.top * yscale
            elif corner == ScreenCorner.TOP_RIGHT:
                v_xpos = -bounds.right * xscale
                v_ypos -= bounds.top * yscale
            elif corner == ScreenCorner.BOTTOM_LEFT:
                v_xpos = bounds.left * xscale
                v_ypos += bounds.down * yscale
            elif corner == ScreenCorner.BOTTOM_RIGHT:
                v_xpos = -bounds.right * xscale
                v_ypos += bounds.down * yscale

            # This node goes here.
            if gui is not ignoreGui:
                guiNodePlacements[node] = (v_xpos, v_ypos)

            # Shift the xpos/ypos now as necessary.
            if corner == ScreenCorner.TOP_LEFT:
                v_ypos -= bounds.height * yscale
                v_ypos -= bounds.down * yscale
            elif corner == ScreenCorner.TOP_RIGHT:
                v_ypos -= bounds.height * yscale
                v_ypos -= bounds.down * yscale
            elif corner == ScreenCorner.BOTTOM_LEFT:
                v_ypos += bounds.height * yscale
                v_ypos += bounds.top * yscale
            elif corner == ScreenCorner.BOTTOM_RIGHT:
                v_ypos += bounds.height * yscale
                v_ypos += bounds.top * yscale

        # Perform the sequences to move them into position.
        self.__moveGuiToPositions(corner, guiNodePlacements, instant=instant, instantNode=instantNode)

    def __moveGuiToPositions(self, corner: ScreenCorner, guiNodePlacements: dict,
                             instant: bool = False, instantNode=None) -> None:
        """
        Given a dict of GUI nodes, move them to their value positions.
        :param corner:            The corner to move with respect to.
        :param guiNodePlacements: The positions to move GUI nodes to.
        :param instant:           Do these move instantly?
        :param instantNode:       One node to move instantly
        :return: None.
        """
        # Let's move the nodes!
        for node, posTuple in guiNodePlacements.items():
            # Get position references for the nodes now.
            new_x, new_y = posTuple
            cur_x, _, cur_y = node.getPos()

            # Get the sequence to move this node.
            moveSequence = LerpPosInterval(
                node, self.MOVE_SPEED, (new_x, 0, new_y), blendType='easeOut'
            )
            self.activeMovementSequences[corner].append(moveSequence)
            moveSequence.start()

            if instant or node is instantNode or settings['reduce-gui-movement']:
                moveSequence.finish()

    """
    Maintenance
    """

    def __updateGUIStatus(self) -> None:
        """
        Curates the managedGui lists, removing any cleaned up GUI.
        :return: None.
        """
        for corner, guiList in self.managedGui.items():
            newList = []
            for guiNode, gui in guiList:
                if gui:
                    # Ensure this GUI is referenced.
                    newList.append((guiNode, gui))
                else:
                    # Kill the references for this gui.
                    guiNode.removeNode()
            self.managedGui[corner] = newList

    def __cleanupSequencesAtCorner(self, corner: ScreenCorner) -> None:
        """
        Finishes all the sequences at a given corner.
        :param corner:        The corner to clear sequences at.
        :param ignoreGuiNode: The GUI node to ignore.
        :return:              None.
        """
        # Get nodes current positions.
        nodePos = []
        for node, _ in self.managedGui[corner]:
            nodePos.append(node.getPos())

        # Cleanup all sequences.
        for seq in self.activeMovementSequences[corner]:
            if seq:
                try:
                    seq.finish()
                except AssertionError:
                    # This is ONLY EVER likely to happen if the game crashes,
                    # because it is trying to move nodes that are cleaned up.
                    # So, to avoid this appearing in crashlogs, we skip it.
                    continue
        self.activeMovementSequences[corner] = []

        # Move nodes back.
        for i, nodeTuple in enumerate(self.managedGui[corner]):
            node = nodeTuple[0]
            node.setPos(nodePos[i])

    def __finishSequences(self) -> None:
        """
        Finishes all actively playing movement sequences.
        :return: None.
        """
        for seq in self.activeMovementSequences.values():
            if seq:
                seq.finish()
        self.activeMovementSequences = {screenCorner: [] for screenCorner in ScreenCorner}

    def finishSequencesAtCorner(self, corner: ScreenCorner):
        """Finishes movement sequences at the given corner."""
        for seq in self.activeMovementSequences[corner]:
            if seq:
                seq.finish()
        self.activeMovementSequences[corner] = []
