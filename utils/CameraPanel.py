"""
A Camera Panel on the GUI to
adjust camera position more precisely.
"""
from direct.gui.DirectGui import *

from toontown.gui.TTGui import SizerFrame


class CameraPanel(DirectFrame):
    """
    A UI element placed on the bottom right to help maneuver the camera around.
    """

    def __init__(self, parent=base.a2dBottomRight, **kw):
        optiondefs = (
            ('frameSize', (-1, 0, 0, 1.2), None),
            ('frameColor', (0.8, 0.8, 0.8, 0.3), None),
        )
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        self.initialiseoptions(CameraPanel)

        self.label_CameraStats = DirectLabel(
            parent=self, pos=(-1, 0, 1.2),
            text_scale=0.04, text='',
            text_align=TextNode.ALeft,
            text_pos=(0, -0.03),
        )
        taskMgr.add(self._updateCameraStats, 'cameraPanelUpdateStats')

        self.cameraPos = (0, 0, 0)
        self.cameraHpr = (0, 0, 0)
        self.cameraFov = 0

        sizerNode = DirectLabel(parent=self, pos=(-0.5, 0, 0))
        self.posSizer = SizerFrame(sizerNode, 'Position', 'xyz', base.camera.getPos(),
                                   (-20, 20), self.updateCamera, 0.875)
        self.hprSizer = SizerFrame(sizerNode, 'Rotation', 'hpr', base.camera.getHpr(),
                                   (0, 360), self.updateCamera, 0.475)
        self.fovSizer = SizerFrame(sizerNode, 'FOV', 'f', [base.camLens.getMinFov()],
                                   (30, 120), self.updateCamera, 0.075)

        self.accept('space-up', self.print)

    def _updateCameraStats(self, task):
        label = self.label_CameraStats
        cameraPos = camera.getPos()
        cameraHpr = camera.getHpr()
        cameraFov = base.camLens.getMinFov()
        if cameraPos != self.cameraPos or cameraHpr != self.cameraHpr or cameraFov != self.cameraFov:
            self.posSizer.setValues(cameraPos, doCallback=False)
            self.hprSizer.setValues(cameraHpr, doCallback=False)
            self.fovSizer.setValues([cameraFov], doCallback=False)
        self.cameraPos = cameraPos
        self.cameraHpr = cameraHpr
        self.cameraFov = cameraFov
        label.setText(f'Camera Position: {cameraPos}\nCamera Hpr: {cameraHpr}\nCamera Fov: {cameraFov}')
        return task.cont

    def updateCamera(self):
        camera.setPos(*self.posSizer.values)
        camera.setHpr(*self.hprSizer.values)
        base.camLens.setMinFov(*self.fovSizer.values)

    def print(self):
        pos = self.posSizer.values
        hpr = self.hprSizer.values
        fov = self.fovSizer.values[0]
        print(
            f'\n'
            f'camSeq.seq_moveCameraPosHpr(seqData=SeqData(\n'
            f'    pos={pos},\n'
            f'    hpr={hpr},\n'
            f'    duration=0,\n'
            f')),\n'
            f'camSeq.seq_changeCameraFov(seqData=SeqData(\n'
            f'    end={fov}, duration=0,\n'
            f'))\n'
        )

