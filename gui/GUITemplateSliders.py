"""
A side-module for GUITemplate.
This creates on-screen sliders for GUIs to use for simple modification.
"""
if __name__ == "__main__":
    from tools.headless.headlessbase import HeadlessStart
    from tools.headless.headlessbase.HeadlessBase import HeadlessBase
    base = HeadlessBase(wantHotkeys=False)
    if __debug__:
        from toontown.utils.DeveloperInjector import startInjector
        startInjector()

from toontown.gui.TTGui import kwargsToOptionDefs
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.InjectorTarget import InjectorTarget
from toontown.toon.gui import GuiBinGlobals
from direct.gui.DirectGui import *


@DirectNotifyCategory()
class GUITemplateSliders(DirectButton):
    """
    A container class for managing and creating several sliders for a single GUI element.
    Define a GUI to effect, the specific keys to modify, and a label text if so desired.
    """

    def __init__(self, guiAffected=None, *guiKeys, **kw):
        # GUI boilerplate.
        parent = base.a2dTopLeft
        optiondefs = kwargsToOptionDefs(
            # Visual button aesthetic
            relief = DGG.RAISED,
            frameSize=(-0.8, 0.8, -0.092, 0.248),
            frameColor=(0.773, 0.251, 0.18, 1.0),
            borderWidth=(0.04, 0.04),

            # Default positioning to put it on the left of the screen.
            # This can be overriden, of course.
            pos=(0.55, 0, -0.2),
            scale=0.42,

            # The GUI to affect, and which keys to modify.
            guiAffected=guiAffected,
            guiKeys=guiKeys,
            rounding=5,

            # Text label settings.
            text='',
            text_fg=(1, 1, 1, 1),
            text_shadow=(0, 0, 0, 1),
            text_pos=(0, 0),
            text_scale=0.25,

            # Callback stuff.
            command=self.print,
            callbacks=(),
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.initialiseoptions(self.__class__)

        # Make this object accessible through the injector on dev.
        if __debug__:
            if hasattr(base, 'GUITemplateSliders') and base.GUITemplateSliders:
                # Let only one of these exist simultaneously
                base.GUITemplateSliders.destroy()
            setattr(base, self.__class__.__name__, self)

        # Sanity check on our keys.
        if type(self.cget('guiKeys')) is str:
            self['guiKeys'] = [self['guiKeys']]

        # Define objects of this GUI.
        self.sliders = []

        # Load elements of this GUI.
        self.load()

        # Set bin for debug.
        self.setBin('sorted-gui-popup', GuiBinGlobals.DebugSliders + 1)

    """
    Loading methods
    """

    def load(self):
        # Get the values.
        guiAffected = self.cget('guiAffected')
        guiKeys = self.cget('guiKeys')
        text = self.cget('text')

        if isinstance(guiAffected, OnscreenText):
            return

        if guiAffected:
            # We are modifying a GUI.
            # If we have no text set, use the GUI's text.
            if not text:
                self.setText(guiAffected.__class__.__name__)

            # Create a slider per key.
            for key in guiKeys:
                values = guiAffected.cget(key)
                # Do certain overrides.
                if key in ('pos', 'image_pos', 'geom_pos') and values is None:
                    values = (0, 0, 0)
                    guiAffected.setPos(*values)

                if key in ('hpr', 'image_hpr', 'geom_hpr') and values is None:
                    values = (0, 0, 0)
                    guiAffected.setHpr(*values)

                if key == 'scale' and values is None:
                    values = 1.0
                    guiAffected.setScale(values)

                if key in ('image_scale', 'geom_scale') and values is None:
                    values = (1, 1, 1)
                    guiAffected[key] = values

                if key == 'frameSize' and values is None:
                    values = (-1, 1, -1, 1)
                    guiAffected[key] = values

                if values is None:
                    self.notify.debug(f'No values found for {key}, skipping!')
                    continue

                if type(values) not in (tuple, list) and not isinstance(values, LVecBase3f):
                    # Wrap value in a tuple or list if necessary.
                    values = (values,)

                if isinstance(values[0], LVecBase4f):
                    r, g, b, a = values[0]
                    values = [r, g, b, a]
                else:
                    # Tupliefy
                    values = tuple([*values])

                # Iterate over these values.
                for index in range(len(values)):
                    # Build the text suffix.
                    suffix = ''
                    if key in ('pos', 'image_pos', 'geom_pos',
                               'hpr', 'image_hpr', 'geom_hpr',
                               'scale', 'image_scale', 'geom_scale'):
                        if index == 0:
                            suffix = '-x'
                        elif index == 1:
                            # unused value, just skip it
                            continue
                        elif index == 2:
                            suffix = '-z'
                    elif key == 'frameSize':
                        suffix = {
                            0: '-left',
                            1: '-right',
                            2: '-down',
                            3: '-up',
                        }.get(index)
                    elif key in ('frameColor', 'image_color', 'geom_color'):
                        suffix = {
                            0: '-red',
                            1: '-green',
                            2: '-blue',
                            3: '-alpha',
                        }.get(index)
                    elif len(values) != 1:
                        suffix = f'-{index}'

                    sliderIndex = len(self.sliders) + 1
                    slider = GUITemplateSlider(
                        parent=self,
                        pos=(0, 0, sliderIndex * GUITemplateSlider.height),

                        guiAffected=guiAffected,
                        guiKey=key,
                        guiKeyIndex=index,
                        rounding=self.cget('rounding'),

                        text = f'{key}{suffix}',
                        callbacks=self['callbacks']
                    )
                    self.sliders.append(slider)

    def destroy(self):
        self.sliders = []
        super().destroy()

    def print(self):
        # Get the values.
        guiAffected = self.cget('guiAffected')
        guiKeys = self.cget('guiKeys')
        rounding = self.cget('rounding')

        if not guiAffected:
            print("No GUI affected, no kwargs here.")
        else:
            print(f"Kwargs for {self['text']}:")
            for key in guiKeys:
                try:
                    if key == 'pos':
                        value = tuple(guiAffected.getPos())
                    elif key == 'hpr':
                        value = tuple(guiAffected.getHpr())
                    elif key == 'scale':
                        value = tuple(guiAffected.getScale())
                    else:
                        value = guiAffected.cget(key)
                    if type(value) in (tuple, list) or isinstance(value, LVecBase3f):
                        value = list(value)
                        for i, val in enumerate(value):
                            value[i] = round(val, rounding)
                        value = tuple(value)
                        if key in ('scale', 'text_scale', 'image_scale', 'geom_scale'):
                            # If all of the values are the same, use only one
                            if all(val == value[0] for val in value):
                                value = value[0]
                    if value:
                        print(f'{key}={value},')
                except KeyError:
                    print(f'{key}=???  # KeyError raised')


@DirectNotifyCategory()
class GUITemplateSlider(DirectSlider):
    """
    A slider for modifying a single value of a GUI.
    """

    height = -0.5

    @InjectorTarget
    def __init__(self, parent, **kw):
        # GUI boilerplate.
        optiondefs = kwargsToOptionDefs(
            guiAffected=None,
            guiKey=None,
            guiKeyIndex=None,
            rounding=3,

            # Can set text as a name.
            text='Slider',
            text_fg=(1, 1, 1, 1),
            text_shadow=(0, 0, 0, 1),
            text_scale=0.15,
            text_pos=(0, 0.22),

            callbacks=(),

            # Do not change the below!
            command=self.callback,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.initialiseoptions(self.__class__)

        # Define objects of this GUI.
        self.entry_currentValue = None
        self.entry_minValue = None
        self.entry_maxValue = None

        # Load elements of this GUI.
        self.load()

        # Set initial value if necessary.
        gui = self.cget('guiAffected')
        key = self.cget('guiKey')
        # Override certain values.
        if gui is not None and key is not None:
            keyIndex = self.cget('guiKeyIndex')
            val = gui[key]
            if type(val) not in (list, tuple) and not isinstance(val, (LVecBase3f, LVecBase4f)):
                self['guiKeyIndex'] = None
                keyIndex = None
            if keyIndex is None:
                # Update our value with this value.
                minVal, maxVal = self['range']
                rngValue = max(abs(min(val, minVal)), abs(max(val, maxVal)))
                self['range'] = (-rngValue, rngValue)
                self.setValue(val)
            else:
                # Update our value iwth the index of this value.
                if key in ('pos', 'image_pos', 'geom_pos'):
                    guiPos = gui.getPos() if key == 'pos' else gui[key]
                    guiVal = guiPos[keyIndex]
                    minVal, maxVal = self['range']
                    rngValue = max(abs(min(guiVal, minVal)), abs(max(guiVal, maxVal)))
                    self['range'] = (-rngValue, rngValue)
                    self.setValue(guiVal)
                    self['value'] = guiVal
                elif key in ('hpr', 'image_hpr', 'geom_hpr'):
                    guiHpr = gui.getHpr() if key == 'hpr' else gui[key]
                    guiVal = guiHpr[keyIndex]
                    minVal, maxVal = self['range']
                    rngValue = max(abs(min(guiVal, minVal)), abs(max(guiVal, maxVal)))
                    self['range'] = (-rngValue, rngValue)
                    self.setValue(guiVal)
                    self['value'] = guiVal
                elif key in ('scale', 'image_scale', 'geom_scale'):
                    scale = gui.getScale() if key == 'scale' else gui[key]
                    if type(scale) in (list, tuple) or isinstance(scale, LVecBase3f):
                        val = scale[keyIndex]
                        minVal, maxVal = self['range']
                        rngValue = max(abs(min(val, minVal)), abs(max(val, maxVal)))
                        self['range'] = (0, rngValue)
                        self.setValue(val)
                        self['value'] = val
                    else:
                        self['guiKeyIndex'] = None
                        minVal, maxVal = self['range']
                        rngValue = max(abs(min(scale, minVal)), abs(max(scale, maxVal)))
                        self['range'] = (0, rngValue)
                        self.setValue(scale)
                        self['value'] = scale
                elif key in ('text_pos', 'text_scale'):
                    guiVal = gui[key][keyIndex]
                    minVal, maxVal = (-0.1, 0.1)
                    rngValue = max(abs(min(guiVal, minVal)), abs(max(guiVal, maxVal)))
                    self['range'] = (-rngValue, rngValue)
                    self.setValue(guiVal)
                    self['value'] = guiVal
                else:
                    if isinstance(gui[key][0], LVecBase4f):
                        val = gui[key][0][keyIndex]
                    else:
                        val = gui[key][keyIndex]
                    minVal, maxVal = self['range']
                    rngValue = max(abs(min(val, minVal)), abs(max(val, maxVal)))
                    self['range'] = (-rngValue, rngValue)
                    self.setValue(val)
                    self['value'] = val

        # Set bin for debug.
        self.setBin('sorted-gui-popup', GuiBinGlobals.DebugSliders)

    """
    Loading methods
    """

    def load(self):
        self.entry_currentValue = DirectEntry(
            parent=self, relief=None,
            pos=(1.05, 0, -0.08),
            scale=0.25,
            frameSize=(-0.1, 2.5, -0.1, 0.7),
            initialText='',
            text_fg=(1, 1, 1, 1),
            text_shadow=(0, 0, 0, 1),
            text_align=TextNode.ALeft,
            command=self.typedCallback,
        )
        self.entry_minValue = DirectEntry(
            parent=self, relief=None,
            pos=(-0.9, 0, 0.2),
            scale=0.25,
            frameSize=(-0.8, 0.9, -0.1, 0.7),
            initialText='',
            text_fg=(1, 1, 1, 1),
            text_shadow=(0, 0, 0, 1),
            text_align=TextNode.ACenter,
            command=self.typedMinCallback,
        )
        self.entry_maxValue = DirectEntry(
            parent=self, relief=None,
            pos=(0.9, 0, 0.2),
            scale=0.25,
            frameSize=(-0.8, 0.9, -0.1, 0.7),
            initialText='',
            text_fg=(1, 1, 1, 1),
            text_shadow=(0, 0, 0, 1),
            text_align=TextNode.ACenter,
            command=self.typedMaxCallback,
        )

    """
    Slider functions
    """

    def callback(self):
        # Get values.
        rounding = self.cget('rounding')
        value = round(self.cget('value'), rounding)
        minVal, maxVal = self.cget('range')

        # Update our GUI.
        self.entry_currentValue.set(str(round(value, rounding)))
        self.entry_minValue.set(str(round(minVal, rounding)))
        self.entry_maxValue.set(str(round(maxVal, rounding)))

        # Update the connected GUI.
        gui = self.cget('guiAffected')
        key = self.cget('guiKey')
        if gui is not None and key is not None:
            keyIndex = self.cget('guiKeyIndex')
            if keyIndex is None:
                # Change the GUI's value directly.
                if key == 'pos':
                    gui.setPos(value)
                elif key == 'hpr':
                    gui.setHpr(value)
                elif key == 'scale':
                    gui.setScale(value)
                else:
                    gui[key] = value
            else:
                # Chance an index in the GUI's value directly.
                if key in ('pos', 'image_pos', 'geom_pos'):
                    keyData = list(gui.getPos()) if key == 'pos' else gui[key]
                    keyData[keyIndex] = value
                    if key == 'pos':
                        gui.setPos(tuple(keyData))
                    else:
                        gui[key] = tuple(keyData)
                elif key in ('hpr', 'image_hpr', 'geom_hpr'):
                    keyData = list(gui.getHpr()) if key == 'hpr' else gui[key]
                    keyData[keyIndex] = value
                    if key == 'hpr':
                        gui.setHpr(tuple(keyData))
                    else:
                        gui[key] = tuple(keyData)
                elif key in ('scale', 'image_scale', 'geom_scale'):
                    scale = gui.getScale() if key == 'scale' else gui[key]
                    if type(scale) in (list, tuple) or isinstance(scale, LVecBase3f):
                        keyData = list(scale)
                        keyData[keyIndex] = value
                        if key == 'scale':
                            gui.setScale(tuple(keyData))
                        else:
                            gui[key] = tuple(keyData)
                    else:
                        if key == 'scale':
                            gui.setScale(value)
                        else:
                            gui[key] = value
                else:
                    keyData = list(gui[key])
                    keyData[keyIndex] = value
                    gui[key] = tuple(keyData)

        for callback in self['callbacks']:
            callback()

    def typedCallback(self, val):
        try:
            # Is the value valid?
            val = float(val)

            # Update range if necessary.
            minVal, maxVal = self.cget('range')
            self['range'] = (min(val, minVal), max(val, maxVal))

            # Set the value on the slider.
            self.setValue(float(val))
            self.notify.debug(f'Slider {self.cget("text")} updated value successfully: {self["value"]}')
        except ValueError:
            # Value was invalid, don't do anything
            self.notify.debug(f'Slider {self.cget("text")} typedCallback caught ValueError!')

        # Update everything.
        self.callback()

    def typedMinCallback(self, val):
        try:
            # Is the value valid?
            val = float(val)

            # Update the range.
            value = self.cget('value')
            minVal, maxVal = self.cget('range')
            if minVal == maxVal:
                minVal -= 0.01
            self['range'] = (min(val, value), maxVal)
            self.notify.debug(f'Slider {self.cget("text")} updated min range successfully: {self["range"]}')
        except ValueError:
            self.notify.debug(f'Slider {self.cget("text")} typedMinCallback caught ValueError!')

        # Update everything.
        self.callback()

    def typedMaxCallback(self, val):
        try:
            # Is the value valid?
            val = float(val)

            # Update the range.
            value = self.cget('value')
            minVal, maxVal = self.cget('range')
            if minVal == maxVal:
                maxVal += 0.01
            self['range'] = (minVal, max(val, value))
            self.notify.debug(f'Slider {self.cget("text")} updated max range successfully: {self["range"]}')
        except ValueError:
            self.notify.debug(f'Slider {self.cget("text")} typedMaxCallback caught ValueError!')

        # Update everything.
        self.callback()


if __name__ == "__main__":
    randomGui = DirectFrame(
        parent=aspect2d,
        relief=DGG.FLAT,
        frameSize=(-0.3, 0.3, -0.3, 0.3),
    )
    base.gui = GUITemplateSliders(
        guiAffected = randomGui,
        guiKeys = ('frameSize', 'pos', 'scale'),
        rounding=1,
    )
    base.run()

