from direct.showbase.DirectObject import DirectObject
from direct.directtools.DirectUtil import CLAMP
from panda3d.core import *
from direct.gui.DirectGui import *

from toontown.utils.DGGEventIgnorer import ignore_event
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from enum import Enum, auto

from typing import List, Dict


class ObjectPoint(Enum):
    xMin = auto()
    xMax = auto()
    zMin = auto()
    zMax = auto()
    center = auto()


@DirectNotifyCategory()
class NodeScreenRegionManager(DirectObject):
    """
    A class that manages NodePaths that need to respond being hovered/clicked in world space.
    If the mouse is found to be within the node's bounds region, it will send a within message.
    If the mouse leaves the node's bounds region, it will send a without message.
    """
    WantDebugShowFrame = False

    def __init__(self) -> None:
        self.objects: List[NodePath] = []
        self.objectData: Dict[int, Dict] = {}
        self.withinObjects: List[int] = []
        self.active: bool = False
        self.frames: Dict[int, DirectFrame] = {}

    def cleanup(self) -> None:
        self.removeAllTasks()
        self.objects = []
        self.objectData = {}
        self.withinObjects = []
        for frame in self.frames.values():
            frame.destroy()
        self.frames = []

    def setActive(self, active: bool) -> None:
        self.active = active
        self.ignoreAll()
        for frame in self.frames.values():
            frame.destroy()
        self.frames = {}
        if self.active:
            for obj in self.objects:
                self.createObjRegion(obj)

    def createObjRegion(self, obj: NodePath) -> None:
        temp1 = obj.getParent().attachNewNode('temp1')
        temp1.setPos(self.getNodePoint(obj, ObjectPoint.center))
        temp2 = temp1.attachNewNode('temp2')
        # Get the minimum and maximum points along the x and z axises, converted to screen space
        xMin = self.getNodePointScreenXY(obj, ObjectPoint.xMin, temp2)[0]
        xMax = self.getNodePointScreenXY(obj, ObjectPoint.xMax, temp2)[0]
        zMin = self.getNodePointScreenXY(obj, ObjectPoint.zMin, temp2)[2]
        zMax = self.getNodePointScreenXY(obj, ObjectPoint.zMax, temp2)[2]
        temp2.removeNode()
        temp1.removeNode()

        # Build a DirectGui frame based on the points we got above
        relief = DGG.FLAT if __debug__ and self.WantDebugShowFrame else None
        newFrame = DirectFrame(
            relief=relief, parent=aspect2d, frameSize=(xMin, xMax, zMin, zMax)
        )
        newFrame['state'] = DGG.NORMAL
        self.frames[obj.getKey()] = newFrame

        @ignore_event
        def withinEvent(obj):
            messenger.send(self.getWithinEvent(obj))

        @ignore_event
        def withoutEvent(obj):
            messenger.send(self.getWithoutEvent(obj))

        # Add events for going inside/outside the new gui frame.
        # Those interested can hook into getWithinEvent/getWithoutEvent.
        newFrame.bind(DGG.WITHIN, withinEvent, extraArgs=[obj])
        newFrame.bind(DGG.WITHOUT, withoutEvent, extraArgs=[obj])

    @staticmethod
    def getWithinEvent(obj: NodePath) -> str:
        return f'NodeScreenRegionManager-Within-{obj.getKey()}'

    @staticmethod
    def getWithoutEvent(obj: NodePath) -> str:
        return f'NodeScreenRegionManager-Without-{obj.getKey()}'

    def addObject(self, obj: NodePath) -> None:
        if obj not in self.objects:
            self.objects.append(obj)
            self.computeObjBounds(obj)
            if self.active:
                self.createObjRegion(obj)

    def removeObject(self, obj: NodePath) -> None:
        if obj in self.objects:
            self.objects.remove(obj)
        if obj.getKey() in self.objectData:
            del self.objectData[obj.getKey()]
        if obj.getKey() in self.withinObjects:
            self.withinObjects.remove(obj.getKey())
        if obj.getKey() in self.frames:
            self.frames[obj.getKey()].destroy()
            del self.frames[obj.getKey()]

    def removeAllObjects(self) -> None:
        for obj in self.objects[:]:
            self.removeObject(obj)

    def computeObjBounds(self, obj: NodePath) -> None:
        min, max = Point3(0), Point3(0)
        obj.calcTightBounds(min, max)
        center = (min + max) / 2.0

        xRange = (max[0] - min[0])
        zRange = (max[2] - min[2])
        self.objectData[obj.getKey()] = {
            ObjectPoint.xMin: Point3(-xRange/2, 0, 0),
            ObjectPoint.xMax: Point3(xRange/2, 0, 0),
            ObjectPoint.zMin: Point3(0, 0, -zRange/2),
            ObjectPoint.zMax: Point3(0, 0, zRange/2),
            ObjectPoint.center: center,
        }

    def getNodePoint(self, obj: NodePath, nodePoint: ObjectPoint) -> Point3:
        return self.objectData[obj.getKey()].get(nodePoint)

    def getNearProjectionPoint(self, nodePath) -> Point3:
        # Find the position of the projection of the specified node path on the near plane
        origin = nodePath.getPos(camera)
        # project this onto near plane
        if origin[1] != 0.0:
            return origin * (base.camLens.getNear() / origin[1])
        else:
            # Object is coplanar with camera, just return something reasonable
            return Point3(0, base.camLens.getNear(), 0)

    def getNodePointScreenXY(self, nodePath: NodePath, nodePoint: ObjectPoint, tempNode: NodePath) -> Vec3:
        tempNode.setPos(self.getNodePoint(nodePath, nodePoint))

        # Where does the node path's projection fall on the near plane
        nearVec = self.getNearProjectionPoint(tempNode)
        # Where does this fall on focal plane
        nearVec *= base.camLens.getFocalLength() / base.camLens.getNear()

        # Convert to aspect2d coords (clamping to visible screen)
        render2dX = CLAMP(nearVec[0] / (base.camLens.getFilmSize()[0] / 2.0), -0.9, 0.9)
        aspect2dX = render2dX * base.getAspectRatio()
        aspect2dZ = CLAMP(nearVec[2] / (base.camLens.getFilmSize()[1] / 2.0), -0.9, 0.9)
        # aspect2dZ = render2dZ * min(base.getAspectRatio(), 1)

        # Return the resulting value
        return Vec3(aspect2dX, 0, aspect2dZ)
