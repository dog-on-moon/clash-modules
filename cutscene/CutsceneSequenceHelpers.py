"""
A module containing various helper methods for cutscene sequence types.
"""
from panda3d.core import Point3, NodePath


class NodePathWithState(NodePath):
    """
    A wrapper class to let you setattr/getattr on NodePaths.
    """
    pass


def getHprBetweenPoints(a: Point3, b: Point3) -> Point3:
    """
    Gets the HPR between two points.
    Assumption is that they're both relative to the same point.

    :param a: Point A in 3D space
    :param b: Point B in 3D space
    """
    # Get two temporary nodes.
    x, y, z = a
    tempA = render.attachNewNode('tempA')
    tempA.setPos(x, y, z)

    x, y, z = b
    tempB = render.attachNewNode('tempB')
    tempB.setPos(x, y, z)

    # Have one node face the other.
    tempA.lookAt(tempB)
    goalHpr = tempA.getHpr()

    # Cleanup.
    tempA.removeNode()
    tempB.removeNode()

    # We're done here.
    return goalHpr

