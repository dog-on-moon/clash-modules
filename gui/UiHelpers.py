from enum import IntEnum, auto
from typing import TYPE_CHECKING, Optional
from direct.showbase.PythonUtil import lerp
from typing import Tuple, List

from toontown.gui.GUIPositionGlobals import ScreenCorner
from toontown.toonbase import PythonUtil

if TYPE_CHECKING:
    from toontown.gui.EasyManagedItem import EasyManagedItem

from panda3d.core import Vec4


def calculateImageScale(imageWidth: int, imageHeight: int, scale: float = 1):
    """
    Calculates the aspect ratio of an image based on its true width and height
    :rtype: Tuple[float, float, float]
    """
    return scale, 1.0, (imageHeight / imageWidth) * scale


def generateButtonImages(nodePath, prefix, normal="Normal", pressed="Pressed", hover="Hover", disable: Optional[str] = None):
    """Generates the image tuple for DirectGUI buttons"""
    if disable is None:
        disable = normal
    return (
        nodePath.find(f"**/{prefix}{normal}"),
        nodePath.find(f"**/{prefix}{pressed}"),
        nodePath.find(f"**/{prefix}{hover}"),
        nodePath.find(f"**/{prefix}{disable}"),
    )


def darkenColor(inputColor: Vec4 = (1, 1, 1, 1), percent: float = 100) -> Vec4:
    """
    Darkens the input colour by a percentage amount.

    :param inputColor: The colour to darken.
    :param percent: 0-100%
    :return: The darkened colour.
    """
    inversePercentage = 100 - percent
    toDarkenBy = inversePercentage / 100
    return Vec4(inputColor[0] * toDarkenBy, inputColor[1] * toDarkenBy, inputColor[2] * toDarkenBy, inputColor[3])


def generateHoverText(text: str) -> Tuple[str, str, str]:
    """Generates hover text for DirectGUI."""
    return '', text, text


def gui_update(guiElement, **kwargs) -> None:
    """
    Updates a GUI element with a set of kwargs.

    :param guiElement: The element that is being modified.
    :param kwargs: Kwargs to update the GUI with.
    :return: None.
    """
    if type(guiElement) is not list:
        guiElement = [guiElement]
    for key, val in kwargs.items():
        for e in guiElement:
            # handle certain overrides
            if key == 'pos':
                e.setPos(val)
            elif key == 'scale':
                e.setScale(val)
            else:
                e[key] = val


"""
Functions for model load/cleanup
"""


def loadModels(*filepaths):
    if len(filepaths) == 1:
        return loader.loadModel(filepaths[0])
    return tuple(loader.loadModel(fp) for fp in filepaths)


def unloadModels(*models):
    for model in models:
        model.removeNode()


"""
Functions for UI Positioning
"""


class GridType(IntEnum):
    HorizontalFirst = auto()
    VerticalFirst = auto()


def placeElementsInGrid(
        guiList: list,
        bounds: tuple,  # left, right, bottom, top
        horizontalCount: int,
        verticalCount: int,
        gridType: GridType,
        scale: float = None,
    ):
    """
    Places GUI elements in a grid.

    :param guiList:         The GUIs to place in a grid.
    :param bounds:          The bounds for the GUI to be placed within.
    :param horizontalCount: The amount of elements to place horizontally
    :param verticalCount:   The amount of elements to place vertically
    :param gridType:        The order that the grid gets populated in
    :param scale:           Scale override on the GUI
    """
    assert horizontalCount * verticalCount >= len(guiList), "Grid size too small for elements provided."
    left, right, bottom, top = bounds

    for index, gui in enumerate(guiList):
        # Figure out our x and z index.
        xindex = 0
        zindex = 0

        if gridType == GridType.HorizontalFirst:
            # 0 1 2  h=3
            # 3 4 5  v=2
            xindex = index % horizontalCount
            zindex = index // horizontalCount
        elif gridType == GridType.VerticalFirst:
            # 0 2 4  h=3
            # 1 3 5  v=2
            xindex = index // verticalCount
            zindex = index % verticalCount

        # Set the GUI position.
        xpos = lerp(left, right, xindex / (horizontalCount - 1))
        zpos = lerp(top, bottom, zindex / (verticalCount - 1))
        gui.setPos(xpos, 0, zpos)
        if scale is not None:
            gui.setScale(scale)


def fillGridWithElements(initialGuiList: list, horizontalCount: int, verticalCount: int,
                         startPos: tuple = (0, 0, 0),
                         alignCorner: ScreenCorner = None,
                         startCorner: ScreenCorner = ScreenCorner.TOP_LEFT,
                         expandMode: GridType = GridType.HorizontalFirst,
                         centering: bool = False, scale: float = 1.0,
                         centeringOtherAxis: bool = False):
    """
    Fill a grid with GUI elements.

    :param initialGuiList:     A list of EasyManagedGUI.
    :type initialGuiList:      List[EasyManagedItem]
    :param horizontalCount:    The number of elements to place horizontally.
    :param verticalCount:      The number of elements to place vertically.
    :param startPos:           The starting position of the grid.
    :param alignCorner:        On which corner of the GUI elements are things centered upon?
    :param startCorner:        The corner from where GUI is initially placed. (if corner is top left, grid fills to bottom right)
    :param expandMode:         The way items fill the grid from the start corner (i.e. fill horizontally or vertically)
    :param centering:          As items are filling the grid, should centering be applied?
    :param scale:              The scale of the elements being placed.
    :param centeringOtherAxis: Should the elements be center aligned on the other axis?
    """
    assert horizontalCount * verticalCount >= len(initialGuiList), "Grid size too small for elements provided."
    if not initialGuiList:
        return
    initialGuiList: List[EasyManagedItem]

    # Figure out our starting position.
    startX, _, startZ = startPos
    cornerX, cornerZ = initialGuiList[0].getCornerPos(screenCorner=alignCorner)
    startPos = (startX + cornerX, 0, startZ + cornerZ)

    # Subdivide our guiList.
    chunkSize = horizontalCount if startCorner in (ScreenCorner.TOP_LEFT, ScreenCorner.TOP_RIGHT) else verticalCount
    guiMatrix = list(PythonUtil.chunks(initialGuiList, chunkSize))

    # Now, we're going to first start by aligning the first item in each GUI list.
    # If we are:
    # start topleft/topright, expand horizontal: Vertical Align from Top, then Horizontal Align from Left/Right (or centering)
    # start topleft/topright, expand vertical: Horizontal Align from Left, then Vertical Align from Top (or centering)
    # start bottomleft/bottomright, expand horizontal: Vertical Align from Bottom, then Horizontal Align from Left/Right (or centering)
    # start bottomleft/bottomright, expand vertical: Horizontal Align from Right, then Vertical Align from Bottom (or centering)
    initialElements = [guiList[0] for guiList in guiMatrix]
    placementKwargs = {
        'guiList': initialElements,
        'startPos': startPos,
        'scale': scale,
        'alignCenter': centeringOtherAxis,
    }
    if startCorner in (ScreenCorner.TOP_LEFT, ScreenCorner.TOP_RIGHT):
        if expandMode == GridType.HorizontalFirst:
            placeElementsInVerticalLine(**placementKwargs)
        elif expandMode == GridType.VerticalFirst:
            placeElementsInHorizontalLine(**placementKwargs)
    elif startCorner in (ScreenCorner.BOTTOM_LEFT, ScreenCorner.BOTTOM_RIGHT):
        if expandMode == GridType.HorizontalFirst:
            placeElementsInVerticalLine(**placementKwargs)
        elif expandMode == GridType.VerticalFirst:
            placeElementsInHorizontalLine(alignRight=True, **placementKwargs)

    # NOW! After placing the starting elements, we now do another pass of centering on all rows (or columns).
    for guiList in guiMatrix:
        placementKwargs = {
            'guiList': guiList,
            'startPos': guiList[0].getPos(),
            'scale': scale,
            'alignCenter': centering,  # overrides other alignment options
        }
        if startCorner == ScreenCorner.TOP_LEFT:
            if expandMode == GridType.HorizontalFirst:
                placeElementsInHorizontalLine(**placementKwargs)
            elif expandMode == GridType.VerticalFirst:
                placeElementsInVerticalLine(alignTop=True, **placementKwargs)
        elif startCorner == ScreenCorner.TOP_RIGHT:
            if expandMode == GridType.HorizontalFirst:
                placeElementsInHorizontalLine(alignRight=True, **placementKwargs)
            elif expandMode == GridType.VerticalFirst:
                placeElementsInVerticalLine(alignTop=True, **placementKwargs)
        elif startCorner == ScreenCorner.BOTTOM_LEFT:
            if expandMode == GridType.HorizontalFirst:
                placeElementsInHorizontalLine(**placementKwargs)
            elif expandMode == GridType.VerticalFirst:
                placeElementsInVerticalLine(**placementKwargs)
        elif startCorner == ScreenCorner.BOTTOM_RIGHT:
            if expandMode == GridType.HorizontalFirst:
                placeElementsInHorizontalLine(alignRight=True, **placementKwargs)
            elif expandMode == GridType.VerticalFirst:
                placeElementsInVerticalLine(**placementKwargs)


def placeElementsInHorizontalLine(guiList: list, startPos: tuple,
                                  alignCenter: bool = False,
                                  alignRight: bool = False,
                                  scale: float = 1.0) -> None:
    """
    Places a list of elements in center alignment, meaning that as the list
    expands, the GUI elements will expand out to the left and right of the start position.

    :param guiList:     The list of GUIs. Must be EasyManagedItems.
    :type guiList:      List[EasyManagedItem]
    :param startPos:    The starting position to expand the elements outwards from.
    :type startPos:     Tuple[float, float, float]
    :param alignCenter: Center-align the elements.
    :param alignRight:  Right-align the elements.
    :param scale:       The scale to move elements with.
    """
    # Set starting variables.
    xoffset = 0.0
    xstart, _, zstart = startPos
    xplacements = []

    # Get initial placements for all of the GUI.
    for i, gui in enumerate(guiList):
        # If this is not the first element, add the left side of the GUI.
        if i != 0:
            xoffset += gui.getEasyWidth() / 2
            xoffset += gui.getEasyPadLeft()

        # Place this offset.
        xplacements.append(xoffset * scale)

        # Add the right side of the GUI if we are not at the end.
        if i != len(guiList) - 1:
            xoffset += gui.getEasyWidth() / 2
            xoffset += gui.getEasyPadRight()

    # The xoffset is now the total width of the elements.
    # If we're aligning center, subtract the placements by half the width.
    halfWidth = (xoffset / 2) * scale
    if alignCenter:
        xplacements = list(map(lambda x: x - halfWidth, xplacements))
    # If we're aligning right, subtract the placements by the width.
    elif alignRight:
        xplacements = list(map(lambda x: x - xoffset, xplacements))

    # Now, place the GUI.
    for gui, xpos in zip(guiList, xplacements):
        gui.setPos(xstart + xpos, 0, zstart)


def placeElementsInVerticalLine(guiList: list, startPos: tuple,
                                alignCenter: bool = False,
                                alignTop: bool = False,
                                scale: float = 1.0) -> None:
    """
    Places a list of elements in center alignment, meaning that as the list
    expands, the GUI elements will expand out to the top and bottom of the start position.

    :param guiList:     The list of GUIs. Must be EasyManagedItems.
    :type guiList:      List[EasyManagedItem]
    :param startPos:    The starting position to expand the elements outwards from.
    :type startPos:     Tuple[float, float, float]
    :param alignCenter: Center-align the elements.
    :param alignTop:    Top-align the elements.
    :param scale:       The scale to move elements with.
    """
    # Set starting variables.
    zoffset = 0.0
    xstart, _, zstart = startPos
    zplacements = []

    # Get initial placements for all of the GUI.
    for i, gui in enumerate(guiList):
        # If this is not the first element, add the top side of the GUI.
        if i != 0:
            zoffset += (gui.getEasyHeight() / 2)
            zoffset += gui.getEasyPadUp()

        # Place this offset.
        zplacements.append(zoffset * scale)

        # Add the bottom of the GUI if we are not at the end.
        if i != len(guiList) - 1:
            zoffset += gui.getEasyHeight() / 2
            zoffset += gui.getEasyPadDown()

    # The zoffset is now the total height of the elements.
    # Since we're aligning center, subtract the placements by half the height.
    halfheight = (zoffset * scale) / 2
    if alignCenter:
        zplacements = list(map(lambda z: z - halfheight, zplacements))
    # If we're aligning top, move them all up Further.
    elif alignTop:
        zplacements = list(map(lambda z: z - zoffset, zplacements))

    # Now, place the GUI.
    for gui, zpos in zip(guiList, zplacements):
        gui.setPos(xstart, 0, zstart + zpos)
