"""
A utils file containing several methods
to make it easier to use the injector.
"""
from toontown.gui.PositionedGUI import OnscreenPositionData, ScreenCorner, PaddingGUI
from direct.gui import DirectGuiGlobals as DGG
from toontown.gui.TTGui import SizerFrame
from panda3d.otp import CFThought, CFTimeout


if __debug__:
    setattr(base, 'PADDING', [None] * 100)

    def SCREEN_PADDING(marginData: OnscreenPositionData,
                       corner: ScreenCorner = ScreenCorner.TOP_RIGHT,
                       vertical: bool = False,
                       index: int = 0, padId: int = 0):
        """
        Adds GUI padding with respect to MarginData.
        """
        if base.PADDING[padId] is None:
            base.PADDING[padId] = PaddingGUI(
                marginData=OnscreenPositionData(),
                corner=corner,
                vertical=vertical,
            )
        base.PADDING[padId].setMarginData(marginData)
        base.PADDING[padId].moveToIndex(index)

    fieldAdjusters = {
        'guiXAdjuster': (0.1, 0.25),
        'guiZAdjuster': (0.1, 0),
        'guiScaleAdjuster': (0.1, -0.25),

        'guiImgXAdjuster': (-1.2, 0.8),
        'guiImgZAdjuster': (-1.2, 0.6),
        'guiImgXScaleAdjuster': (-1.2, 0.4),
        'guiImgZScaleAdjuster': (-1.2, 0.2),

        'guiGeomXAdjuster': (-1.2, 0),
        'guiGeomZAdjuster': (-1.2, -0.2),
        'guiGeomXScaleAdjuster': (-1.2, -0.4),
        'guiGeomZScaleAdjuster': (-1.2, -0.6),

        'nodeXYZAdjuster': (0, 0.4),
        'nodeHPRAdjuster': (0, 0),
        'nodeScaleAdjuster': (0, -0.4),
    }
    _topNodes = []
    for field in fieldAdjusters:
        setattr(base, field, None)


    def setGuiAdjuster(gui=None):
        """Sets a GUI to be adjusted on-screen."""
        for field in fieldAdjusters:
            f = getattr(base, field)
            if f:
                f.remove()
        global _topNodes
        for node in _topNodes:
            node.removeNode()
        _topNodes = []

        if not gui:
            return

        def moveX(field):
            x, *_ = getattr(base, field).values
            try:
                *_, z = gui['pos'] or (0, 0, 0)
                gui.setPos(x, 0, z)
            except Exception as e:
                print('An exception was caught while using GUI adjusters.')
                print(e)

        def moveZ(field):
            *_, z = getattr(base, field).values
            try:
                x, *_ = gui['pos'] or (0, 0, 0)
                gui.setPos(x, 0, z)
            except Exception as e:
                print('An exception was caught while using GUI adjusters.')
                print(e)

        def scaleGui(field):
            s, *_ = getattr(base, field).values or 1
            gui.setScale(s)

        def moveImgX(field):
            x, *_ = getattr(base, field).values
            try:
                *_, z = gui['image_pos'] or (0, 0, 0)
                gui['image_pos'] = (x, 0, z)
            except Exception as e:
                print('An exception was caught while using GUI adjusters.')
                print(e)

        def moveImgZ(field):
            *_, z = getattr(base, field).values
            try:
                x, *_ = gui['image_pos'] or (0, 0, 0)
                gui['image_pos'] = (x, 0, z)
            except Exception as e:
                print('An exception was caught while using GUI adjusters.')
                print(e)

        def scaleXImgGui(field):
            x, *_ = getattr(base, field).values or (1, 1, 1)
            try:
                *_, z = gui['image_scale']
                gui['image_scale'] = (x, 1, z)
            except Exception as e:
                print('An exception was caught while using GUI adjusters.')
                print(e)

        def scaleZImgGui(field):
            *_, z = getattr(base, field).values or (1, 1, 1)
            try:
                x, *_ = gui['image_scale']
                gui['image_scale'] = (x, 1, z)
            except Exception as e:
                print('An exception was caught while using GUI adjusters.')
                print(e)

        def moveGeomX(field):
            x, *_ = getattr(base, field).values
            try:
                *_, z = gui['geom_pos'] or (0, 0, 0)
                gui['geom_pos'] = (x, 0, z)
            except Exception as e:
                print('An exception was caught while using GUI adjusters.')
                print(e)

        def moveGeomZ(field):
            *_, z = getattr(base, field).values
            try:
                x, *_ = gui['geom_pos'] or (0, 0, 0)
                gui['geom_pos'] = (x, 0, z)
            except Exception as e:
                print('An exception was caught while using GUI adjusters.')
                print(e)

        def scaleXGeomGui(field):
            x, *_ = getattr(base, field).values or (1, 1, 1)
            try:
                *_, z = gui['geom_scale']
                gui['geom_scale'] = (x, 1, z)
            except Exception as e:
                print('An exception was caught while using GUI adjusters.')
                print(e)

        def scaleZGeomGui(field):
            *_, z = getattr(base, field).values or (1, 1, 1)
            try:
                x, *_ = gui['geom_scale']
                gui['geom_scale'] = (x, 1, z)
            except Exception as e:
                print('An exception was caught while using GUI adjusters.')
                print(e)

        # Set up the sizer frames
        def setupFrame(field, title, properties, default, range, func):
            posNode = aspect2d.attachNewNode('posNode')
            _topNodes.append(posNode)
            x, z = fieldAdjusters[field]
            posNode.setPos(x, 0, z)
            setattr(base, field, SizerFrame(
                posNode, title, properties, default, range, func, extraArgs=[field]
            ))

        x, _, z = gui['pos'] or (0, 0, 0)
        setupFrame('guiXAdjuster', 'GUI Xpos', 'x', (x,), (-0.5, 0.5), moveX)
        setupFrame('guiZAdjuster', 'GUI Zpos', 'z', (z,), (-0.5, 0.5), moveZ)

        s = gui.getScale() or 1
        if type(s) not in (int, float):
            s = sum(s)/len(s)
        setupFrame('guiScaleAdjuster', 'GUI Scale', 's', (s,), (0.01, 1.0), scaleGui)

        # image pos
        try:
            x, _, z = gui['image_pos'] or (0, 0, 0)
            setupFrame('guiImgXAdjuster', 'Image Xpos', 'x', (x,), (-0.5, 0.5), moveImgX)
            setupFrame('guiImgZAdjuster', 'Image Zpos', 'z', (z,), (-0.5, 0.5), moveImgZ)

            s = gui['image_scale'] or (1, 1, 1)
            if type(s) in (int, float):
                s = (s, s, s)
            s = (s[0], s[2])
            setupFrame('guiImgXScaleAdjuster', 'Img XScale', 'x', (s[0],), (0.01, 1.0), scaleXImgGui)
            setupFrame('guiImgZScaleAdjuster', 'Img ZScale', 'z', (s[1],), (0.01, 1.0), scaleZImgGui)
        except KeyError:
            pass  # no image

        # Geom pos
        try:
            x, _, z = gui['geom_pos'] or (0, 0, 0)
            setupFrame('guiGeomXAdjuster', 'Geom Xpos', 'x', (x,), (-0.5, 0.5), moveGeomX)
            setupFrame('guiGeomZAdjuster', 'Geom Zpos', 'z', (z,), (-0.5, 0.5), moveGeomZ)

            s = gui['geom_scale'] or (1, 1, 1)
            if type(s) in (int, float):
                s = (s, s, s)
            s = (s[0], s[2])
            setupFrame('guiGeomXScaleAdjuster', 'Geom XScale', 'x', (s[0],), (0.01, 1.0), scaleXGeomGui)
            setupFrame('guiGeomZScaleAdjuster', 'Geom ZScale', 'z', (s[1],), (0.01, 1.0), scaleZGeomGui)
        except KeyError:
            pass  # no image


    def setNodeAdjuster(node=None):
        """Sets a node to be adjusted on-screen."""
        for field in fieldAdjusters:
            f = getattr(base, field)
            if f:
                f.remove()
        global _topNodes
        for n in _topNodes:
            n.removeNode()
        _topNodes = []

        if not node:
            return

        def moveXYZ(field):
            x, y, z = getattr(base, field).values
            try:
                node.setPos(x, y, z)
            except Exception as e:
                print('An exception was caught while using node adjusters.')
                print(e)

        def moveHPR(field):
            x, y, z = getattr(base, field).values
            try:
                node.setHpr(x, y, z)
            except Exception as e:
                print('An exception was caught while using node adjusters.')
                print(e)

        def moveScale(field):
            x, y, z = getattr(base, field).values
            try:
                node.setScale(x, y, z)
            except Exception as e:
                print('An exception was caught while using node adjusters.')
                print(e)

        # Set up the sizer frames
        def setupFrame(field, title, properties, default, range, func):
            posNode = aspect2d.attachNewNode('posNode')
            _topNodes.append(posNode)
            x, z = fieldAdjusters[field]
            posNode.setPos(x, 0, z)
            setattr(base, field, SizerFrame(
                posNode, title, properties, default, range, func, extraArgs=[field]
            ))

        x, y, z = node.getPos()
        setupFrame('nodeXYZAdjuster', 'Node Pos', 'xyz', (x, y, z), (-50, 50), moveXYZ)

        h, p, r = node.getHpr()
        setupFrame('nodeHPRAdjuster', 'Node Hpr', 'hpr', (h, p, r), (-180, 180), moveHPR)

        s = node.getScale() or 1
        if type(s) in (int, float):
            s = (s, s, s)
        setupFrame('nodeScaleAdjuster', 'Node Scale', 'xyz', s, (0.01, 1.0), moveScale)


    def make_xyz_adjuster(name, node):
        """
        Creates an on-screen XYZ adjuster.
        """
        if hasattr(base, name):
            return
        newNode = render.attachNewNode('ParentNode')
        node.wrtReparentTo(newNode)
        def posNode():
            newNode.setPos(getattr(base, name).values)
        setattr(base, name, SizerFrame(
            aspect2d, 'Position', 'xyz', newNode.getPos(), (-3, 3), callback=posNode,
        ))


    setattr(base, 'gui', None)


    def accessOnscreenGui(changeState=False):
        """
        Lets all onscreen GUI selectable with middle-click.
        Upon middle-clicking, the selected GUI can be accessed with `base.gui`
        """

        def printName(gui, _):
            try:
                print(gui.getName())
                if base.localAvatar:
                    if gui.getName():
                        base.localAvatar.setChatAbsolute(f'Selected {gui.getName()}', CFThought | CFTimeout)
                    else:
                        base.localAvatar.setChatAbsolute(f'Selected noname', CFThought | CFTimeout)
                else:
                    if gui.getName():
                        print(f"Selected {gui.getName()}")
                    else:
                        print("Selected noname")
                setattr(base, 'gui', gui)
            except Exception as e:
                base.localAvatar.setChatAbsolute(f'Selection failed :)', CFThought | CFTimeout)
                print(e)

        for gui in base.guiItems.values():
            gui.bind(DGG.B2PRESS, printName, [gui])
            if changeState:
                gui['state'] = DGG.NORMAL
