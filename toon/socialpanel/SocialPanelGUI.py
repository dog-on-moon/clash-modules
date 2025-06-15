"""
Helper UI classes for various Social Panel GUI elements.
"""
from enum import IntEnum

from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from direct.gui.DirectGuiGlobals import FLAT
from direct.gui.DirectGui import *
from direct.fsm.FSM import FSM
from toontown.groups.GroupGlobals import *

from typing import List

from toontown.gui.TTGui import ContextFrame, kwargsToOptionDefs, ExtendedOnscreenText, ContextDropdown
from toontown.toon.socialpanel.SocialPanelGlobals import sp_gui, sp_gui, sp_gui, sp_gui_icons
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory


@DirectNotifyCategory()
class SelectorButton(DirectFrame):

    BUTTON_ACTIVE = (0.906, 0.843, 0.125, 1.0)
    BUTTON_INACTIVE = (0.184, 0.192, 0.212, 1.0)

    def __init__(self, parent, pos, width=0.6, height=0.07, title='', callback=None, disabled=False, scale=0.6, darkTheme: bool = False, **kwargs):
        self.width = width
        self.height = height
        self.callback = callback

        self.lightCol = kwargs.pop('lightCol', (1, 1, 1, 1))
        self.darkCol = kwargs.pop('darkCol', (0.361, 0.361, 0.361, 1.0))

        if darkTheme:
            self.lightCol, self.darkCol = self.darkCol, self.lightCol

        DirectFrame.__init__(self, parent=parent, relief=None, pos=pos, scale=scale,
                             text_pos=(0, -0.014), text_scale=0.05,
                             text_fg=(0, 0, 0, 1), text="Test choice",
                             geom=sp_gui.find('**/SmoothTextBox'),
                             geom_color=self.darkCol, **kwargs)
        self.initialiseoptions(SelectorButton)
        self.setWidth(width=width)

        # Create the title text on top.
        self.titleText = DirectLabel(
            parent=self, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1),
            text_pos=(0, 0.085), text_scale=0.065, text='',
        )
        if title:
            self.setTitleText(title)
        if darkTheme:
            self.titleText['text_fg'] = (0, 0, 0, 1)
            self.titleText['text_shadow'] = (0, 0, 0, 0)
            self['text_fg'] = (1, 1, 1, 1)
            self['text_shadow'] = (0, 0, 0, 1)

        # Creates the buttons on the side.
        self.button_left = DirectButton(
            self, pos=(-(width/2) - 0.04, 0, 0),
            relief=None,  # frameSize=(-0.04, 0.04, -0.04, 0.04),
            # frameColor=self.BUTTON_ACTIVE,
            text='<', text_scale=0.05,
            command=self.changeOption, extraArgs=[-1],
            image=(
                sp_gui.find('**/Arrow_N'),
                sp_gui.find('**/Arrow_P'),
                sp_gui.find('**/Arrow_H'),
                sp_gui.find('**/Arrow_D'),
            ), image_scale=(-(30 / 42), 1, 1), scale=0.08,
        )
        self.button_right = DirectButton(
            self, pos=((width/2) + 0.04, 0, 0),
            relief=None,  # frameSize=(-0.04, 0.04, -0.04, 0.04),
            # frameColor=self.BUTTON_ACTIVE,
            text='>', text_scale=0.05,
            command=self.changeOption, extraArgs=[1],
            image=(
                sp_gui.find('**/Arrow_N'),
                sp_gui.find('**/Arrow_P'),
                sp_gui.find('**/Arrow_H'),
                sp_gui.find('**/Arrow_D'),
            ), image_scale=((30 / 42), 1, 1), scale=0.08,
        )
        self.button_left.hide()
        self.button_right.hide()

        # Sets our options.
        self.options = []           # A list of values we want to associate as options.
        self.option2Text = {None: ''}       # Text associated with each of our option values.
        self.wraparound = False     # Do we want the selector arrows to wraparound multiple options?
        self.currentIndex = 0       # Our current selected index in the options list.

        # Set the disabled mode.
        self.disabled = disabled
        self.setDisabled()

    def setDisabled(self):
        """
        Sets the disabled mode on this GUI.
        :return: None.
        """
        if self.disabled:
            self.button_left.show()
            self.button_right.show()
            self.setButtonState(False)
            self.setText('')
            self['geom_color'] = self.darkCol
        else:
            self.setButtonState(True)
            self['geom_color'] = self.lightCol

    def setWidth(self, width):
        self['geom_scale']=((0.18333 * width) * (327 / 62), 1, 0.11)

    def setTitleText(self, text):
        self.titleText.setText(text)

    def enterDisable(self):
        self.disabled = True
        self.setDisabled()

    def exitDisable(self):
        self.disabled = False
        self.setDisabled()

    def setButtonState(self, state: bool):
        state = DGG.NORMAL if state else DGG.DISABLED
        self.button_left['state'] = state
        self.button_right['state'] = state

    def setOptions(self, values: list = None, texts: list = None,
                   wraparound: bool = False, setIndex: int = -1, canDisable: bool = True):
        """Sets the options on this GUI."""
        if canDisable and not (values or texts):
            self.enterDisable()
        else:
            self.exitDisable()
        if not values:
            values = [None]
        if not texts:
            texts = ['']
        self.options = values
        self.option2Text = dict(zip(values, texts))
        self.wraparound = wraparound
        self.currentIndex = setIndex if setIndex != -1 else len(values) - 1
        self.updateButtons()

    def getChoice(self):
        if not self.options:
            return None
        return self.options[self.currentIndex]

    def changeOption(self, direction):
        self.currentIndex += direction
        # We can check like this, since wraparound is implied to be true
        # if the button state is active at this point.
        if self.currentIndex < 0:
            self.currentIndex = len(self.options) - 1
        elif self.currentIndex >= len(self.options):
            self.currentIndex = 0
        # Run the callback.
        if self.callback is not None:
            self.callback(self.getChoice())
        # Update the buttons.
        self.updateButtons()

    def updateButtons(self):
        self.setText(str(self.option2Text[self.getChoice()]))
        if len(self.options) <= 1:
            self.button_left.hide()
            self.button_right.hide()
            return
        self.button_left.show()
        self.button_right.show()
        if not self.wraparound:
            active = ()
            self.button_left['state'] = DGG.NORMAL if self.currentIndex != 0 else DGG.DISABLED
            self.button_left['frameColor'] = self.BUTTON_ACTIVE if self.currentIndex != 0 else self.BUTTON_INACTIVE
            self.button_right['state'] = DGG.NORMAL if self.currentIndex != len(self.options) - 1 else DGG.DISABLED
            self.button_right['frameColor'] = self.BUTTON_ACTIVE if self.currentIndex != len(self.options) - 1 else self.BUTTON_INACTIVE
        else:
            self.setButtonState(True)

    @property
    def frameSize(self):
        width = self.width
        height = self.height
        return -width/2, width/2, -height/2, height


class CheckboxButton(DirectButton):
    """
    A button that's designed to appear as a simple checkbox.
    Has logic to maintain its checkbox appearance.

    Apologies that the keywords are hacked together.
    """

    CHECKBOX_STATE = IntEnum("CheckboxState", ("BASE", "EMPTY", "DOT", "CHECK"))
    SCALE = 0.45
    C_SCALE = 0.45

    def __init__(self, parent, **kw):
        """
        Creates a CheckboxButton.

        Optional defs:
        - checked: Does this Checkbox start in a checked state?
        - baseState: The state to use for a base image.
        - checkedState: What state should the Checkbox be in when checked?
        - uncheckedState: What state should the Checkbox be in when unchecked?
        - checkboxGroup: Does this Checkbox control a group of other Checkboxes?
        - partialCheckedState: Partial image state to use, if a checkboxGroup is defined,
                               and not all of the checkboxes in the group are clicked.
        - value: Some associated value. Can be grabbed from a getter, but
                 the getter will return None if the box is not checked.
                 If this checkbox has a checkboxGroup, it will instead return
                 a list of all associated values from the checkboxGroup.
        - checkCallableOnCheck: Given a callable, this checkbox can only enter the checked state
                                if the result from this callable is True.
        - checkCallableOnUncheck: Given a callable, this checkbox can only enter the unchecked state
                                  if the result from this callable is True.
        - checkboxGroupSelectAllPartialHandlerCallable: If this is defined, then this callable
                                                        decides how to handle tiebreakers for a select all
                                                        mechanic (i.e. if 2/4 items in the group are selected,
                                                        callable returns True if it should select all,
                                                        or callable returns False if it should unselect all)
        :param parent: The parent of the GUI element.
        :param kw: Any associated kwargs.
        """
        optiondefs = (
            ('checked', False, None),
            ('baseState', self.CHECKBOX_STATE.BASE, None),
            ('checkedState', self.CHECKBOX_STATE.CHECK, None),
            ('uncheckedState', self.CHECKBOX_STATE.EMPTY, None),
            ('checkboxGroup', None, None),
            ('partialCheckedState', self.CHECKBOX_STATE.DOT, None),
            ('value', None, None),
            ('scale', 1.0, None),
            ('checkCallableOnCheck', None, None),
            ('checkCallableOnUncheck', None, None),
            ('checkboxGroupSelectAllPartialHandlerCallable', None, None),
            ('frameColor', (0, 0, 0, 0), None),
        )
        self.callback = kw.pop('command', None)
        self.defineoptions(kw, optiondefs)

        # create the overlay button
        super().__init__(
            parent=parent, image=self._getImageFromState(self.cget('baseState')),
            command=self.onClick, **kw
        )
        self.initialiseoptions(CheckboxButton)

        # create the base image
        self.checkImage = DirectButton(
            parent=parent, image=self._getImageFromState(self.cget('baseState')),
            pos=kw.get('pos', (0, 0, 0)), scale=kw.get('scale', 1),
            frameColor=(0, 0, 0, 0), frameSize=(0, 0, 0, 0),
            image_scale=kw.get('image_scale', (1, 1, 1)),
        )
        # self.checkImage.bind(DGG.B1PRESS, self.onClickWrapper)

        # update image
        self.setScale(self.cget('scale') * self.SCALE)
        self.checkImage.setScale(self.cget('scale') * self.C_SCALE)
        self['image'] = self._getImageFromState(self.cget('baseState'))
        self.checkImage['image'] = self.getCurrentCheckedImage()

        # a list of checkbox groups that we are in
        self.parentGroups = []
        if self.cget('checkboxGroup'):
            self.defineCheckboxGroup()
        # self.bind(DGG.B1PRESS, self.onClickWrapper)

    def destroy(self):
        """
        Special destroy call to clean up hanging references.
        """
        self['checkboxGroup'] = None
        del self.parentGroups
        super().destroy()

    def bindToScroll(self, scrollPanel):
        # Binds this checkbox to the scroll wheel.
        scrollPanel.bindToScroll(self)
        scrollPanel.bindToScroll(self.checkImage)

    def _getImageFromState(self, checkboxState: IntEnum):
        """
        Gets the image to use for rendering from an IntEnum checkboxState.
        :param checkboxState: The state to get.
        :return: The image node, or None.
        """
        imagePath = {
            self.CHECKBOX_STATE.BASE: None,
            self.CHECKBOX_STATE.EMPTY: '**/CIRCLE1',
            self.CHECKBOX_STATE.DOT: '**/CIRCLE2',
            self.CHECKBOX_STATE.CHECK: '**/CIRCLE3',
        }.get(checkboxState, None)

        # return it if we found anything
        if imagePath is not None:
            return sp_gui_icons.find(imagePath)
        return None

    def getCurrentCheckedImage(self):
        """
        Returns the image node for our current checked state.
        :return: Image node, or None.
        """
        checkboxGroup = self.checkboxGroup  # type: List[CheckboxButton]
        if not self.isGroup():
            return self._getImageFromState(
                self.cget('checkedState' if self.cget('checked') else 'uncheckedState')
            )
        else:
            checkedRatio = len([checkbox for checkbox in checkboxGroup if checkbox.checked]) / len(checkboxGroup)
            if checkedRatio >= 1.0:
                # all checkboxes are checked
                return self._getImageFromState(self.cget('checkedState'))
            elif checkedRatio <= 0.0:
                # no checkboxes are checked
                return self._getImageFromState(self.cget('uncheckedState'))
            else:
                # some checkboxes are checked
                return self._getImageFromState(self.cget('partialCheckedState'))

    def defineCheckboxGroup(self, checkboxGroup: List['CheckboxButton'] = None):
        """
        Defines an associated checkboxGroup for this checkbox.
        :param checkboxGroup: A list of CheckboxButtons to associate. If None, it's already defined.
        :return: None.
        """
        if checkboxGroup is not None:
            self['checkboxGroup'] = checkboxGroup
        else:
            checkboxGroup = self['checkboxGroup']
        for checkbox in checkboxGroup:
            checkbox.parentGroups.append(self)
        self.updateImage()

    def getValue(self, ignoreGroupNones=False):
        """
        Gets the value of this CheckboxButton, or a list of values from its CheckboxGroup.
        :param ignoreGroupNones: If this CheckboxButton has a group, remove all of the Nones from its group.
        :return: A value, or list of values.
        """
        if not self.isGroup():
            # singleton checkbox, return its value if it is checked
            return self.cget('value') if self.checked else None
        else:
            # has a checkbox group, return a list
            retList = [checkbox.getValue() for checkbox in self.checkboxGroup]
            if not ignoreGroupNones:
                # return this raw list
                return retList
            else:
                # return this list, with all of the Nones removed
                return [val for val in retList if val is not None]

    def reset(self, setMode: bool = False) -> None:
        """
        Marks the Checkbox Button as being unclicked.
        :return:
        """
        self['checked'] = setMode
        self.updateImage()
        self.updateParentGroups()

    def onClick(self) -> None:
        """
        Called when the Checkbox Button is clicked.
        :return: None.
        """
        if not self._canSwitchStates():
            # we can't switch states, so don't even bother.
            return

        # flip checked state
        self['checked'] = not self['checked']
        self.clickChildren()
        self.updateImage()
        self.updateParentGroups()

        # run our callback, if defined
        if self.callback is not None:
            self.callback()

    def getClickCallable(self):
        """
        Gets the function of the Checkbox on click.
        :return: Callable.
        """
        return self.onClick

    def clickChildren(self):
        """
        Clicks the child checkboxes.
        :return: None.
        """
        if not self.isGroup():
            return
        checkboxGroup = self.checkboxGroup  # type: List[CheckboxButton]
        checkedRatio = len([checkbox for checkbox in checkboxGroup if checkbox.checked]) / len(checkboxGroup)
        if checkedRatio >= 1.0:
            # all checkboxes are checked, so uncheck all
            self['checked'] = False
            for checkbox in checkboxGroup:
                checkbox.requestCheckMode(False)
        elif checkedRatio <= 0.0:
            # no checkboxes are checked, so check all
            # or some checkboxes are checked, so check all
            self['checked'] = True
            for checkbox in checkboxGroup:
                checkbox.requestCheckMode(True)
        else:
            # some checkboxes are checked.
            # prefer checking all, but be prepared for trouble.
            partialHandlerCallable = self.cget('checkboxGroupSelectAllPartialHandlerCallable')
            if partialHandlerCallable:
                # let the partialHandlerCallable tell us what to do.
                result = partialHandlerCallable()
                self['checked'] = result
                for checkbox in checkboxGroup:
                    checkbox.requestCheckMode(result)
                return

            # we don't have a callable handler,
            # so prefer to select all.
            self['checked'] = True
            for checkbox in checkboxGroup:
                checkbox.requestCheckMode(True)

    def _canSwitchStates(self) -> bool:
        """
        Checks to see if this Checkbox can switch checked states.
        :return: True if we can, False if we can't.
        """
        # see if we can use the transition callable
        transitionCallable = self.cget('checkCallableOnCheck' if not self['checked'] else 'checkCallableOnUncheck')
        if transitionCallable:
            # use its result instead, if it exists
            return transitionCallable()
        # otherwise, we're safe to transition checked states
        return True

    def forceCheckMode(self, mode, callback=True):
        """Forces this checkbox to enter a given state."""
        self['checked'] = mode
        self.updateImage()
        self.updateParentGroups()

        if callback and self.callback is not None:
            self.callback()

    def requestCheckMode(self, mode):
        """Requests a check mode."""
        if mode != self['checked']:
            self.onClick()

    def updateImage(self):
        """
        Updates the image of this checkbox.
        :return: None.
        """
        # self['image'] = self.getCurrentCheckedImage()
        self.checkImage['image'] = self.getCurrentCheckedImage()

    def updateParentGroups(self):
        """
        Updates the status of a parent group.
        :return: None.
        """
        for checkbox in self.parentGroups:
            checkbox.updateImage()

    def isGroup(self) -> bool:
        return bool(self.checkboxGroup)

    @property
    def checkboxGroup(self) -> List['CheckboxButton']:
        return self.cget('checkboxGroup')

    @property
    def checked(self) -> bool:
        return self.cget('checked')


@DirectNotifyCategory()
class SocialPanelContextDropdown(ContextDropdown):
    """
    Context Dropdown specific for the Social Panel.
    """

    def __init__(self, parent, **kw):
        optiondefs = kwargsToOptionDefs(
            xmax=1 - (settings['social-panel-scale'] * 0.17),
            scale=settings['social-panel-scale'] / 10,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.initialiseoptions(SocialPanelContextDropdown)

        # Handle various destroy events.
        destroyEvents = (
            'open-social-panel', 'close-social-panel',
            'unload-social-panel', 'change-tab-social-panel',
            'social-panel-friend-context-close'
        )
        for event in destroyEvents:
            self.accept(event, self.destroy)
