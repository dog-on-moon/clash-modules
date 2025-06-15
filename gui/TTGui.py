"""
Contains GUI-related utilities for making placement easier.
"""
import math

from toontown.toon.gui import GuiBinGlobals
from toontown.toon.socialpanel.SocialPanelGlobals import sp_gui
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.InjectorTarget import InjectorTarget

guiButton = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui.bam')
btnUp = guiButton.find('**/tt_t_gui_mat_shuffleUp')
btnDn = guiButton.find('**/tt_t_gui_mat_shuffleDown')
btnRlvr = guiButton.find('**/tt_t_gui_mat_shuffleUp')
# Use for buttons: image = (btnUp, btnDn, btnRlvr), image_color = (1, 1, 1, 1), image1_color = (0.8, 0.8, 0, 1), image2_color = (0.15, 0.82, 1.0, 1),

guiButtonClassic = loader.loadModel('phase_3/models/gui/quit_button')
btnUpClassic = guiButtonClassic.find('**/QuitBtn_UP')
btnDnClassic = guiButtonClassic.find('**/QuitBtn_DN')
btnRlvrClassic = guiButtonClassic.find('**/QuitBtn_RLVR')

from panda3d.core import *
from direct.gui.DirectGuiBase import DirectGuiWidget
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.gui import DirectGuiGlobals


class LockingEntry(DirectEntry):
    """
    A DirectEntry, but with the added bonus of locking
    the player's controls when focused.

    Very helpful for general input entries that may
    end up having general headaches from hotkeys.

    Responsive to left-clicks taking away focus from the entry.
    Also supports right-click to clear.
    """

    def __init__(self, parent, supportClear=True, **kw):
        optiondefs = (
            ('clearOnFocus', False, None),
            ('canUnlockAv', True, None),
            ('funcOnAccept', None, None)
        )
        self.defineoptions(kw, optiondefs)
        DirectEntry.__init__(self, parent, **kw)
        self.initialiseoptions(LockingEntry)

        self.locked = False
        self.accept('mouse1', self._onAccept)
        self.bind(DGG.B1PRESS, self.lockAvatar)
        self.accept(self.guiItem.getFocusInEvent(), self.lockAvatar)
        self.accept(self.guiItem.getFocusOutEvent(), self._onAccept)
        self.bind(DGG.ACCEPT, self._onAccept)
        self.bind(DGG.ACCEPTFAILED, self._onAccept)
        if supportClear:
            self.bind(DGG.B3PRESS, lambda _: self.clear())

    def destroy(self):
        self.unlockAvatar()
        DirectEntry.destroy(self)

    def clear(self):
        self.set('')
        self.unlockAvatar()

    def lockAvatar(self, _=None):
        if self.locked:
            return
        if base.localAvatar:
            base.localAvatar.lockControlsForEntry()
            base.localAvatar.disableHotkeys()
        self.locked = True
        if self.cget('clearOnFocus'):
            self.clearSearchBar()
        self.acceptOnce('mouse1-up', self.acceptOnce, extraArgs=['mouse1-up', self.unlockAvatar])

    def unlockAvatar(self, _=None):
        if not self.locked:
            return
        if self.cget('canUnlockAv') and base.localAvatar:
            base.localAvatar.unlockControlsForEntry()
            base.localAvatar.enableHotkeys()
        self.locked = False
        self.guiItem.setFocus(0)

    def _onAccept(self, _=None):
        self.unlockAvatar()
        funcOnAccept = self.cget('funcOnAccept')
        if funcOnAccept:
            funcOnAccept()

    def clearSearchBar(self):
        """
        Clears the text off the search bar.
        """
        self.set('')


class LiveLockingEntry(LockingEntry):
    """
    A locking entry with bindings to support reading live entries.
    """

    def __init__(self, parent, supportClear=True, **kw):
        optiondefs = (
            ('callback', None, None),
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, supportClear=supportClear, **kw)
        self.initialiseoptions(LiveLockingEntry)

        self.cachedText = None
        self._startReadTask()

    def destroy(self):
        super().destroy()
        self._endReadTask()

    def _startReadTask(self):
        taskMgr.add(self._readTask, self.uniqueName('entryReadTask'))

    def _endReadTask(self):
        taskMgr.remove(self.uniqueName('entryReadTask'))

    def _readTask(self, task):
        if hasattr(self, 'guiItem'):
            if self.get() != self['initialText']:
                text = self.get()
                if type(text) is str and self.cachedText != text:
                    self.cachedText = text
                    self._doCallback(text)
        else:
            return task.done
        return task.cont

    def _doCallback(self, text):
        if self['callback']:
            self['callback'](text)


class ExtendedOnscreenText(OnscreenText):
    """
    OnscreenText with some extra useful methods.
    """

    def getTextY(self):
        return self.getTextPos()[1]

    def getYScale(self):
        return self.getScale()[1]

    def getLineCount(self):
        return self.textNode.getHeight()

    def _shiftYPosByLineCount(self, lineCount, yScale=None):
        """
        Shifts the text ypos by some amount of lines.
        """
        if self['text'] == '':
            # Empty string has no lines.
            return

        if not lineCount:
            # no lines, no change
            return

        # Each line, we move down half a yscale.
        offsetYScale = (yScale or self.getYScale()) / 2

        # Move down that much.
        xpos, ypos = self['pos']
        self['pos'] = (xpos, ypos + (offsetYScale * lineCount))

    def setTextWithVerticalAlignment(self, text):
        """
        Sets the text of the OnscreenText with respect to
        keeping it vertically aligned.
        :param text: The text to set it to.
        :return: None.
        """
        # Shift the text down, then set new text, and then back up again.
        if self['text'] != '':
            oldLineCount = self.sanity(self.getLineCount()) or 1
        else:
            oldLineCount = 1
        self['text'] = text
        newLineCount = self.getLineCount()
        self._shiftYPosByLineCount(newLineCount - oldLineCount)

    def capTextToLineCount(self, lines=2):
        iterations = 0
        while self.textNode.getNumRows() > lines:
            currTextScale = self['scale']
            self['scale'] = (currTextScale[0] * 0.97, currTextScale[1] * 0.97)
            self['wordwrap'] = self['wordwrap'] / 0.97

            # break early if this operation takes too long
            iterations += 1
            if iterations > 60:
                break

    def multPos(self, x_mult=1.0, y_mult=1.0):
        """Multiplies the text's pos by a given amount."""
        x, y = self.getPos()
        self.setPos(x * x_mult, y * y_mult)

    def move(self, x: float = 0.0, y: float = 0.0):
        """Moves the text by a given amount."""
        _x, _y = self.getPos()
        self.setPos(_x + x, _y + y)

    @staticmethod
    def sanity(x):
        """
        makes numbers sane.
        context: i used self.getLineCount() and it returned 2.297e+31 for the text's height.
        the text node had literally just generated.
        """
        x = round(x, 4)
        if not (0 <= x <= 20):
            return 0
        return x


class OnscreenTextOutline(ExtendedOnscreenText):
    """
    Version of OnscreenText which supports outlines.
    """

    def __init__(self, text_dist=0.011, precision=12, *args, **kwargs):
        """
        Creates an OnscreenTextOutline instance.
        If you want to have arguments that affect specifically the outline,
        begin the kwargs with `outline_` (e.g. set fg=x, outline_fg=x)

        :param text_dist: The distance from the outline to the text.
        :param precision: How strong you want the outline to be. You really want to keep this low.
        :param args: Args to pass for the OnscreenText.
        :param kwargs: Kwargs to pass for the OnscreenText.
        """
        # Create the base onscreen text.
        super().__init__(*args, **self.getBaseTextArgs(**kwargs))
        self._precision = precision

        # Make the outline text.
        self.outlineText = [
            OnscreenText(*args, **self.getOutlineTextArgs(**kwargs)) for _ in range(self._precision)
        ]
        self.text_dist = text_dist
        self.setOutlineTextDist(text_dist=text_dist)

        # Create the text on the very top as well.
        self.topText = OnscreenText(*args, **self.getBaseTextArgs(**kwargs))

    def __setitem__(self, key, value):
        """Make sure to __setitem__ on the children as well."""
        super().__setitem__(key, value)

        # Set it on the outline children too.
        for outlineText in self.outlineText:
            if key == 'pos':
                self.setOutlineTextDist()
            else:
                outlineText.__setitem__(key, value)

        # And the top text (finally).
        self.topText.__setitem__(key, value)

    def show(self):
        super().show()
        for outlineText in self.outlineText:
            outlineText.show()
        self.topText.show()

    def hide(self):
        super().hide()
        for outlineText in self.outlineText:
            outlineText.hide()
        self.topText.hide()

    def setAttribute(self, key, value):
        super().__setitem__(key, value)
        self.topText.__setitem__(key, value)

    def setOutlineAttribute(self, key, value):
        for outlineText in self.outlineText:
            outlineText.__setitem__(key, value)

    @staticmethod
    def getBaseTextArgs(**kwargs):
        """Gets all of the args for the base OnscreenText."""
        return {key: value for key, value in kwargs.items() if 'outline_' not in key}

    def getOutlineTextArgs(self, **kwargs):
        """Gets all of the args for the outlined OnscreenText."""
        outlineArgs = kwargs.copy()
        for key in outlineArgs.keys():
            # If it starts with outline_, ignore.
            if 'outline_' in key:
                continue

            # If it doesn't, see if there's an outline_ to override it.
            else:
                if f"outline_{key}" in outlineArgs:
                    outlineArgs[key] = outlineArgs[f"outline_{key}"]

        # Outline text args Obtained. Make sure we clear the outlines too.
        return self.getBaseTextArgs(**outlineArgs)

    def setOutlineTextDist(self, text_dist=None):
        """Sets the distance for the outline to set from the text."""
        if text_dist is None:
            text_dist = self.text_dist
        self.text_dist = text_dist
        for i in range(self._precision):
            z, x = divmod(i, self._precision)
            real_x, real_z = self['pos']
            xDist = math.cos(math.radians((i / self._precision) * 360))
            yDist = math.sin(math.radians((i / self._precision) * 360))
            self.outlineText[i].setPos(
                real_x + (xDist * text_dist),
                real_z + (yDist * text_dist),
            )

    def setPos(self, x, y):
        super().setPos(x, y)
        self.setOutlineTextDist()

    def setBin(self, bin, height):
        super().setBin(bin, height)
        for text in self.outlineText:
            text.setBin(bin, height - 1)


class ContextFrame(DirectFrame):
    """
    This is a version of the DirectFrame that
    appears directly at the cursor.
    """
    def __init__(self, _=None, **kw):
        optiondefs = (
            ('xmin', -1.0, None),       # Describes the boundary
            ('xmax', 1.0, None),        # where this frame can spawn
            ('zmin', -1.0, None),       # relative to the borders of
            ('zmax', 1.0, None),        # aspect2d.
            ('y', 0.0, None),           # Sets the panel's yposition.
            ('pop-in', True, None),     # Does the pop-in animation.
            ('fragile', True, None),    # Kills the frame if mouse1-up is triggered.
            ('survive', False, None),   # Survives the next mouse1-up.
        )
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, aspect2d, **kw)
        self.initialiseoptions(ContextFrame)
        self['state'] = DirectGuiGlobals.NORMAL
        self.setPos(getMousePositionWithAspect2d(
            y=self.cget('y'),
            xmin=self.cget('xmin'), xmax=self.cget('xmax'),
            zmin=self.cget('zmin'), zmax=self.cget('zmax'),
        ))

        self.setBin('sorted-gui-popup', GuiBinGlobals.ContextFrameBin)

        # Creates the pop-in interval.
        self.hoverInterval = None
        if self.cget('pop-in') and not settings['reduce-gui-movement']:
            self.hoverInterval = Sequence(
                LerpScaleInterval(self, .1, self.cget('scale')*1.1, blendType='easeInOut', startScale=0.01),
                LerpScaleInterval(self, .1, self.cget('scale')*1.0, blendType='easeInOut'),
            ).start()

        # Fragile.
        if self.cget('fragile'):
            self.accept('mouse1-up', self.onMouseUp)

    def onMouseUp(self):
        if self.cget('survive'):
            self['survive'] = False
            return
        self.destroy()

    def destroy(self):
        self.ignoreAll()
        if hasattr(self.hoverInterval, 'finish'):
            self.hoverInterval.finish()
            del self.hoverInterval
        super().destroy()


def getMousePositionWithAspect2d(y=0, xmin=-1.0, xmax=1.0, zmin=-1.0, zmax=1.0) -> tuple:
    """
    Gets the mouse position with respect to aspect2d.

    You can parent GUIs to render2d,
    but guis parented to render2d get stretched,
    and aspect2d prevents the stretchiness.

    xmin/xmax/ymin/ymax can be set to help constrain
    the distance from the border. This is also helpful
    for guis, in case you want them to not go off screen.
    """
    ratio = base.getAspectRatio()
    x = max(xmin, min(base.mouseWatcherNode.getMouseX(), xmax)) * max(ratio, 1)
    z = max(zmin, min(base.mouseWatcherNode.getMouseY(), zmax)) / min(max(0.001, ratio), 1)
    return x, y, z


@DirectNotifyCategory()
class ContextDropdown(ContextFrame):
    """
    A context-based dropdown menu, stylized a bit after the Social Panel.
    Appears at the cursor when created.

    Has methods to contextually append buttons to the menu,
    supporting simple callback functionality.
    """

    @InjectorTarget
    def __init__(self, parent, **kw):
        # GUI boilerplate.
        optiondefs = kwargsToOptionDefs(
            relief=None,
            labelText='Label',
            image=sp_gui.find('**/POPUPBAR'),
            geom=sp_gui.find('**/POPUPBAR_TITLEAREA'),
            buttonGeom=(
                sp_gui.find('**/OrangeButton_N'),
                sp_gui.find('**/OrangeButton_P'),
                sp_gui.find('**/OrangeButton_H'),
            ),
            redButtonGeom=(
                sp_gui.find('**/RedButton_N'),
                sp_gui.find('**/RedButton_P'),
                sp_gui.find('**/RedButton_H'),
            ),
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.initialiseoptions(ContextDropdown)

        # Define objects of this GUI.
        self.buttons = []
        self.text = ExtendedOnscreenText(
            parent=self,
            text='',
            wordwrap=8,
            pos=(-0.0301, -0.57),
            scale=0.32,
            fg=(0, 0, 0, 1),
            shadow=(0, 0, 0, 0),
        )
        self.text.setTextWithVerticalAlignment(self.cget('labelText'))

    """
    Loading methods
    """

    def destroy(self):
        self.buttons = []
        super().destroy()

    """
    Button accessors
    """

    def getButtonCount(self) -> int:
        return len(self.buttons)

    def addButton(self, text: str, callback: callable, red: bool = False, extraArgs: list = None) -> None:
        """Adds a button on the dropdown."""
        if extraArgs is None:
            extraArgs = []

        # Create our button object.
        button = self._makeButton(callback, red, extraArgs=extraArgs)

        # Text is attached to this button.
        t = self._makeOnscreenText(button)
        t.setTextWithVerticalAlignment(text)

        # Position the button correctly.
        buttonIndex = len(self.buttons)
        button.setPos(*self._getButtonPos(buttonIndex))

        # Add the button to our button list.
        self.buttons.append(button)

        # Reposition accordingly
        self._reposition()

    def _makeButton(self, callback: callable, red: bool, extraArgs: list = None) -> DirectButton:
        if extraArgs is None:
            extraArgs = []
        return DirectButton(
            parent=self,
            relief=None,
            frameSize=(-1.4, 1.4, -0.45, 0.45),
            command=callback,
            extraArgs=extraArgs,
            geom=self.cget('buttonGeom' if not red else 'redButtonGeom'),
            geom_scale=(2.72, 1, 0.9),
        )

    def _makeOnscreenText(self, parent) -> ExtendedOnscreenText:
        return ExtendedOnscreenText(
            parent=parent,
            wordwrap=7,
            pos=(-0.0501, -0.1),
            scale=0.37,
            fg=(1, 1, 1, 1.0),
            shadow=(0, 0, 0, 1),
        )

    @staticmethod
    def _getButtonPos(i: int) -> tuple:
        return 0, 0, -1.4 + (i * -0.9)

    """
    Repositioning
    """

    def _reposition(self):
        """Ensures the context panel is placed correctly."""
        # header geom
        self['geom_scale'] = (165 / 39 * 0.63, 1, 0.76)
        self['geom_pos'] = (0, 0, -0.5)

        # back panel
        buttonCount = len(self.buttons)
        dist = 0.9
        start = 1.88
        zpos = start + (dist * (buttonCount - 1))
        self['image_scale'] = ((170 / 304) * 5, 1, zpos)
        self['image_pos'] = (0, 0, -zpos / 2)

        # frame positioning
        self['frameSize'] = (-1.45, 1.45, -zpos, 0)


class SizerFrame:
    """
    Sizer frames for complicated number adjustment.
    """
    def __init__(self, parent, name, shortNames, property, defaultRange, callback=None, heightOffset=0, extraArgs=None):
        if extraArgs is None:
            extraArgs = []
        self.parent = parent
        self.name = name
        self.shortNames = [letter for letter in shortNames]
        self.values = list(property)
        for i, val in enumerate(self.values):
            self.values[i] = round(val, 5)
        self.values = tuple(self.values)
        self.defaultRange = defaultRange
        self.min, self.max = defaultRange
        self.callback = callback if callback else lambda: None
        self.heightOffset = heightOffset
        self.extraArgs = extraArgs
        self.ui = []
        self.size = len(self.values)
        self.cleanedUp = False

        for value in self.values:
            if value < self.min:
                self.min = value
            if self.max < value:
                self.max = value

        self.buildUI()

    def buildUI(self):
        txtScale = 0.08
        self.label = DirectLabel(parent=self.parent, text=self.name, text_scale=txtScale,
                                 relief=None, pos=(-0.25, 0, self.heightOffset + 0.08))

        frameSize = (-0.02, 0.02, -0.02, 0.02)

        self.minButton = DirectEntry(parent=self.parent, initialText=str(self.min), text_scale=txtScale,
                                     frameSize=frameSize, frameColor=(0, 0, 0, 0.25),
                                     pos=(0, 0, self.heightOffset + 0.08), command=self.updateMin,
                                     scale=1)
        self.maxButton = DirectEntry(parent=self.parent, initialText=str(self.max), text_scale=txtScale,
                                     frameSize=frameSize, frameColor=(0, 0, 0, 0.25),
                                     pos=(0.25, 0, self.heightOffset + 0.08), command=self.updateMax,
                                     scale=1)
        self.minButton.bind(DirectGuiGlobals.WHEELUP, self.minScrolled, [1])
        self.minButton.bind(DirectGuiGlobals.WHEELDOWN, self.minScrolled, [-1])
        self.maxButton.bind(DirectGuiGlobals.WHEELUP, self.maxScrolled, [1])
        self.maxButton.bind(DirectGuiGlobals.WHEELDOWN, self.maxScrolled, [-1])

        sliderOffset = -0.09
        self.sliders = [None] * self.size
        self.sliderLabels = [None] * self.size
        self.sliderEntries = [None] * self.size
        for i in range(len(self.sliders)):
            self.sliders[i] = DirectSlider(
                parent=self.parent, range=(0, 1), value=(self.values[i] - self.min) / (self.max - self.min),
                pageSize=0, orientation=DGG.HORIZONTAL,
                pos=(0, 0, (i * sliderOffset) + self.heightOffset),
                scale=0.34, command=self.updateSlider,
            )
            self.sliderLabels[i] = DirectLabel(
                parent=self.parent, text_scale=txtScale,
                scale=1.5, text=self.shortNames[i],
                pos=(-0.4, 0, (i * sliderOffset) + self.heightOffset - 0.013),
                frameColor=(0, 0, 0, 0),
            )
            self.sliderEntries[i] = DirectEntry(
                parent=self.parent, text_scale=1,
                scale=0.05, initialText=str(self.values[i]),
                pos=(0.4, 0, (i * sliderOffset) + self.heightOffset - 0.013),
                frameColor=(0, 0, 0, 0), command=self.updateSliderButton,
                extraArgs=[i]
            )
            self.ui.append(self.sliders[i])
            self.ui.append(self.sliderLabels[i])
            self.ui.append(self.sliderEntries[i])

        self.ui.append(self.label)
        self.ui.append(self.minButton)
        self.ui.append(self.maxButton)

    def bindScroll(self, scrollWheelFrame: ScrollWheelFrame):
        """
        Binds this class to a scrollWheelFrame.
        """
        scrollWheelFrame.bindToScroll(self.label)
        scrollWheelFrame.bindToScroll(self.minButton)
        scrollWheelFrame.bindToScroll(self.maxButton)
        for ui in self.ui:
            scrollWheelFrame.bindToScroll(ui)

    def hide(self):
        for ui in self.ui:
            ui.hide()

    def show(self):
        for ui in self.ui:
            ui.show()

    def updateMin(self, newMin):
        try:
            oldMin = self.min
            if float(newMin) < self.max:
                self.min = float(newMin)
            for button in self.sliderEntries:
                if float(button.get()) < self.min:
                    self.min = float(button.get())
            for slider in self.sliders:
                val = slider.getValue()
                val = (val * (self.max - oldMin)) + oldMin
                slider.setValue((val - self.min) / (self.max - self.min))
        except ValueError:
            pass
        self.minButton.set(str(round(self.min, 3)))
        self.minButton['focus'] = 0
        if hasattr(base, 'localAvatar') and base.localAvatar is not None:
            base.localAvatar.unlockControlsForEntry()

    def updateMax(self, newMax):
        try:
            oldMax = self.max
            if float(newMax) > self.min:
                self.max = float(newMax)
            for button in self.sliderEntries:
                if float(button.get()) > self.max:
                    self.max = float(button.get())
            for slider in self.sliders:
                val = slider.getValue()
                val = (val * (oldMax - self.min)) + self.min
                slider.setValue((val - self.min) / (self.max - self.min))
        except ValueError:
            pass
        self.maxButton.set(str(round(self.max, 3)))
        self.maxButton['focus'] = 0
        if hasattr(base, 'localAvatar') and base.localAvatar is not None:
            base.localAvatar.unlockControlsForEntry()

    def minScrolled(self, direction, _=None):
        distance = self.max - self.min
        dist_delta = (distance / 50) * direction
        self.updateMin(round(self.min + round(dist_delta, 3), 3))

    def maxScrolled(self, direction, _=None):
        distance = self.max - self.min
        dist_delta = (distance / 50) * direction
        self.updateMax(round(self.max + round(dist_delta, 3), 3))

    def updateSlider(self, doCallback=True):
        if self.cleanedUp:
            return
        for i in range(len(self.sliders)):
            if not (self.sliders[i] and self.sliderEntries[i]):
                return
            val = self.sliders[i].getValue()
            val = round((val * (self.max - self.min)) + self.min, 4)
            self.sliderEntries[i].set(str(val))
        if doCallback:
            self.prepCallback()

    def updateSliderButton(self, value, sliderIndex):
        try:
            val = float(value)
            if val > self.max:
                self.updateMax(val)
            if val < self.min:
                self.updateMin(val)
            val = (val - self.min) / (self.max - self.min)
            self.sliders[sliderIndex].setValue(val)
        except ValueError:
            pass
        self.sliderEntries[sliderIndex]['focus'] = 0
        if hasattr(base, 'localAvatar') and base.localAvatar is not None:
            base.localAvatar.unlockControlsForEntry()
        self.prepCallback()

    def setValues(self, newValues, doCallback=True):
        self.values = newValues
        for i, val in enumerate(self.values):
            if val < self.min:
                self.min = val
            if self.max < val:
                self.max = val
            self.sliders[i].setValue((val - self.min) / (self.max - self.min))
        self.updateSlider(doCallback=doCallback)

    def prepCallback(self):
        self.values: list = []
        for slider in self.sliders:
            val = slider.getValue()
            val = (val * (self.max - self.min)) + self.min
            self.values.append(val)
        for i in range(len(self.values)):
            self.values[i] = round(self.values[i], 5)
        self.values = tuple(self.values)
        self.callback(*self.extraArgs)

    def getValues(self):
        self.prepCallback()
        return self.values

    def remove(self):
        self.cleanedUp = True
        for ui in self.ui:
            ui.remove()


class CheckboxButton(DirectButton):
    """
    A button that's just a lame checkbox.

    TODO: Move to the cutscene editor code. CheckboxButton from SocialPanelGUI is a better version of this class
    """

    def __init__(self, parent, callback, labelText, extraArgs=None, boundCheckboxes=None, **kw):
        optiondefs = (
            ('frameSize', (-0.03, 0.03, -0.03, 0.03), None),
            ('frameColor', (0.765, 0.765, 0.765, 1.0), None),
            ('command', self.onClick, None),
            ('text', ' ', None),
            ('text_scale', 0.06, None),
            ('text_pos', (0, -0.01), None),
        )
        self.defineoptions(kw, optiondefs)
        DirectButton.__init__(self, parent, **kw)
        self.initialiseoptions(CheckboxButton)
        self.callback = callback if callback else lambda _: None
        self.extraArgs = extraArgs if extraArgs else []
        self.boundCheckboxes = boundCheckboxes
        self.checked = False
        self.label = None
        if labelText:
            self.label = DirectLabel(
                parent=self, text=labelText,
                text_scale=0.05, text_pos=(0, -0.02),
                text_bg=(0,0,0,0),
                frameColor=(0,0,0,0),
                pos=(0.05, 0, 0),
                text_align=TextNode.ALeft,
            )

    def setBoundCheckboxes(self, boundCheckboxes):
        self.boundCheckboxes = boundCheckboxes

    def onClick(self):
        if self.boundCheckboxes:
            # handle stuff differently if we're bound to other checkboxes
            if self.checked:
                return  # only work on not checked
            for checkbox in self.boundCheckboxes:
                checkbox.setCheck(False)
            self.callback(self, *self.extraArgs)
            self.setCheck(True)
        else:
            # standard boolean
            self.setCheck(not self.checked)
            self.callback(self, *self.extraArgs)

    def setCheck(self, mode):
        self.checked = mode
        self.setText('x' if mode else ' ')


"""
Various functions on gui
"""


def kwargsToOptionDefs(**kwargs):
    """Converts kwargs to option definitions."""
    retList = []
    for key, val in kwargs.items():
        if type(val) is not list:
            retList.append(
                (key, val, None)
            )
        else:
            val, func = val
            retList.append(
                (key, val, func)
            )
    return tuple(retList)


"""
Animation functions on gui
"""


def moveWidgetFrameTop(widget: DirectGuiWidget, duration: float, y: float, startY: float, delay: float = 0.0, blendType: str = 'easeOut'):
    """Moves the top of a widget frame to a given position."""
    if not hasattr(widget, '_optionInfo'):
        return Sequence()

    def setWidgetTop(newy, seqWidget):
        if not hasattr(seqWidget, '_optionInfo'):
            return
        listFrameSize = list(seqWidget['frameSize'])
        listFrameSize[3] = newy
        seqWidget['frameSize'] = tuple(listFrameSize)
        messenger.send(widget.uniqueName('moveWidgetFrameTop'))

    return Sequence(
        Wait(delay),
        LerpFunctionInterval(
            function=setWidgetTop,
            duration=duration,
            fromData=startY,
            toData=y,
            extraArgs=[widget],
            blendType=blendType,
        ),
        Func(messenger.send, widget.uniqueName('moveWidgetFrameTop-end')),
    )


def moveWidgetFrameBottom(widget: DirectGuiWidget, duration: float, y: float, startY: float, delay: float = 0.0, blendType: str = 'easeOut'):
    """Moves the bottom of a widget frame to a given position."""
    if not hasattr(widget, '_optionInfo'):
        return Sequence()

    def setWidgetBottom(newy, seqWidget):
        if not hasattr(seqWidget, '_optionInfo'):
            return
        listFrameSize = list(seqWidget['frameSize'])
        listFrameSize[2] = newy
        seqWidget['frameSize'] = tuple(listFrameSize)
        messenger.send(widget.uniqueName('moveWidgetFrameBottom'))

    return Sequence(
        Wait(delay),
        LerpFunctionInterval(
            function=setWidgetBottom,
            duration=duration,
            fromData=startY,
            toData=y,
            extraArgs=[widget],
            blendType=blendType,
        ),
        Func(messenger.send, widget.uniqueName('moveWidgetFrameBottom-end')),
    )


def fadeFrameText(frame: DirectFrame, duration: float, before: float, after: float, rgb: tuple = (0, 0, 0), delay: float = 0.0, blendType: str = 'noBlend'):
    """Fades a frame text to X percent."""
    if not hasattr(frame, '_optionInfo'):
        return Sequence()

    def setFrameTextFg(x, seqFrame):
        r, g, b = rgb
        seqFrame['text_fg'] = (r, g, b, x)

    return Sequence(
        Wait(delay),
        LerpFunctionInterval(
            function=setFrameTextFg,
            duration=duration,
            fromData=before,
            toData=after,
            extraArgs=[frame],
            blendType=blendType,
        ),
        Func(messenger.send, frame.uniqueName('fadeFrameText-end')),
    )


def fadeFrameGeom(frame: DirectFrame, duration: float, before: float, after: float,
                  rgb: tuple = (1, 1, 1), delay: float = 0.0, blendType: str = 'noBlend'):
    """Fades a frame's geom to X percent."""
    if not hasattr(frame, '_optionInfo'):
        return Sequence()

    def setGeomAlpha(x, seqFrame):
        if not hasattr(seqFrame, '_optionInfo'):
            return
        r, g, b = rgb
        seqFrame['geom_color'] = (r, g, b, x)

    return Sequence(
        Wait(delay),
        LerpFunctionInterval(
            function=setGeomAlpha,
            duration=duration,
            fromData=before,
            toData=after,
            extraArgs=[frame],
            blendType=blendType,
        ),
        Func(messenger.send, frame.uniqueName('fadeFrameGeom-end')),
    )


def widgetImageZScale(widget: DirectGuiWidget, duration: float, z: float, startZ: float, delay: float = 0.0, blendType: str = 'easeOut'):
    """Scale's the Z coordinate of a widget's image scale."""
    if not hasattr(widget, '_optionInfo'):
        return Sequence()

    def setWidgetImageZScale(newz, seqWidget):
        if not hasattr(seqWidget, '_optionInfo'):
            return
        listImageScale = list(seqWidget['image_scale'])
        listImageScale[2] = newz
        seqWidget['image_scale'] = tuple(listImageScale)

    return Sequence(
        Wait(delay),
        LerpFunctionInterval(
            function=setWidgetImageZScale,
            duration=duration,
            fromData=startZ,
            toData=z,
            extraArgs=[widget],
            blendType=blendType,
        ),
        Func(messenger.send, widget.uniqueName('widgetImageZScale-end')),
    )


class CheckboxButton(DirectButton):
    """
    A button that's just a lame checkbox.
    """

    def __init__(self, parent, callback, labelText, extraArgs=None, boundCheckboxes=None, **kw):
        optiondefs = (
            ('frameSize', (-0.03, 0.03, -0.03, 0.03), None),
            ('frameColor', (0.765, 0.765, 0.765, 1.0), None),
            ('command', self.onClick, None),
            ('text', ' ', None),
            ('text_scale', 0.06, None),
            ('text_pos', (0, -0.01), None),
        )
        self.defineoptions(kw, optiondefs)
        DirectButton.__init__(self, parent, **kw)
        self.initialiseoptions(CheckboxButton)
        self.callback = callback if callback else lambda _: None
        self.extraArgs = extraArgs if extraArgs else []
        self.boundCheckboxes = boundCheckboxes
        self.checked = False
        self.label = None
        if labelText:
            self.label = DirectLabel(
                parent=self, text=labelText,
                text_scale=0.05, text_pos=(0, -0.02),
                text_bg=(0,0,0,0),
                frameColor=(0,0,0,0),
                pos=(0.05, 0, 0),
                text_align=TextNode.ALeft,
            )

    def setBoundCheckboxes(self, boundCheckboxes):
        self.boundCheckboxes = boundCheckboxes

    def onClick(self):
        if self.boundCheckboxes:
            # handle stuff differently if we're bound to other checkboxes
            if self.checked:
                return  # only work on not checked
            for checkbox in self.boundCheckboxes:
                checkbox.setCheck(False)
            self.callback(self, *self.extraArgs)
            self.setCheck(True)
        else:
            # standard boolean
            self.setCheck(not self.checked)
            self.callback(self, *self.extraArgs)

    def setCheck(self, mode):
        self.checked = mode
        self.setText('x' if mode else ' ')


"""
Various translation sequences
"""


def getPopInSequence(gui, toScale, duration = 0.29) -> Sequence:
    # Does a pop-in sequence on the GUI.
    enterDuration = duration * 0.6897
    exitDuration = duration * 0.310345
    return Sequence(
        LerpScaleInterval(gui, enterDuration, toScale * 1.1, startScale=0.01,
                          blendType='easeInOut'),
        LerpScaleInterval(gui, exitDuration, toScale, blendType='easeInOut')
    )
