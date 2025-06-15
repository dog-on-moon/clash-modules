from typing import Optional

from toontown.groups.GroupClasses import GroupClient
from toontown.toonbase import TTLocalizer

if __name__ == "__main__":
    from tools.headless.headlessbase import HeadlessStart
    from tools.headless.headlessbase.HeadlessBase import HeadlessBase
    base = HeadlessBase(wantHotkeys=False)
    if __debug__:
        from toontown.utils.DeveloperInjector import startInjector
        startInjector()
    base.initCR()  # defines base.cr
    # base.startHeadlessShow()

from toontown.gui.TTGui import kwargsToOptionDefs
from toontown.gui.GUITemplateSliders import GUITemplateSliders
from toontown.gui.GUINode import GUINode
from toontown.gui import UiHelpers
from toontown.toon.socialpanel.SocialPanelGlobals import sp_gui, sp_gui_icons
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.InjectorTarget import InjectorTarget
from direct.gui.DirectGui import *


@DirectNotifyCategory()
class SocialPanelGroupSubtext(DirectFrame):
    """
    Subtext info that appears on the friends list button.
    """

    GROUP_ICONS = {
        'leader': sp_gui_icons.find('**/star'),
        'ready': sp_gui_icons.find('**/thumbsup_green'),
        'not-here': sp_gui_icons.find('**/thumbsup_grey'),
    }

    taskName = 'sp-group-subtext-update'

    @InjectorTarget
    def __init__(self, parent, friendsListButtons, **kw):
        # GUI boilerplate.
        optiondefs = kwargsToOptionDefs(
            pos=(0.37458, 0.0, -0.36418),
            scale=0.26644,
            relief = None,
            text='',
            text_align=TextNode.ARight,
            text_pos=(0.38499, -1.22111),
            text_scale=0.69825,
            text_fg=(1, 1, 1, 1), text_bg=(0, 0, 0, 0.45),
            # image=self.GROUP_ICONS['leader'],
            # image_scale=1.0,
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.initialiseoptions(self.__class__)
        self.group: Optional[GroupClient] = None
        self.friendsListButtons = friendsListButtons

        # i love panda3d
        self.accept('groupUpdate', self.onGroupUpdate)
        self.accept('groupLeaveResponse', self.onGroupLeft)
        if base.cr:
            self.onGroupUpdate(base.cr.groupManager.group)
        taskMgr.add(self.onCasualUpdate, self.getTaskName())

    def show(self):
        super().show()
        for button in self.friendsListButtons:
            button['text_fg'] = (1, 1, 1, 0)
            button['text_shadow'] = (0, 0, 0, 0)

    def hide(self):
        super().hide()
        for button in self.friendsListButtons:
            button['text_fg'] = (1, 1, 1, 1)
            button['text_shadow'] = (0, 0, 0, 1)

    def destroy(self):
        self.ignoreAll()
        del self.group
        del self.friendsListButtons
        taskMgr.remove(self.getTaskName())
        super().destroy()

    def getTaskName(self):
        return self.uniqueName(self.taskName)

    """
    Updates
    """

    def onCasualUpdate(self, task):
        """Update every second casually when we are visible."""
        if not self.isHidden():
            self.update()
        task.delayTime = 1.0
        return task.again

    def onGroupLeft(self, _=None):
        self.onGroupUpdate(None)

    def onGroupUpdate(self, group: Optional[GroupClient]):
        """Called whenever our group status updates whatsoever."""
        self.group = group

        # If there is no group, just hide.
        if group is None:
            self.hide()
            return

        # Otherwise, become visible, and do general update.
        self.show()
        self.update()

    def update(self):
        """Updates the subtext with context of nearby Toons & group status."""
        if self.group is None:
            return

        # Some group constants
        groupName = self.group.getName()
        groupSize = self.group.groupSize
        subtext = ''
        icon = 'leader' if self.group.localAvIsOwner() else 'ready'

        # Check if we are in the right area.
        localAvNotHere = (not base.localAvatar) or (not self.group.validateZoneId(base.localAvatar.zoneId))
        if localAvNotHere:
            subtext += '\nWaiting for You'
            icon = 'not-here'

        if self.group.groupDefinition.allowFullHood:
            if self.group.announcedBattle and not base.cr.doId2do.get(self.group.avatarThatEncountered):
                subtext += '\nJoin the Battle!'
        else:
            # Is the owner nearby?
            if not localAvNotHere and not base.cr.doId2do.get(self.group.owner):
                subtext += '\nLeader Missing'

            # If the group is full, figure out who we are waiting on.
            elif self.group.isFull:
                toonsPresent = len([toon for toon in map(base.cr.doId2do.get, self.group.avIds) if toon is not None])
                toonsWaiting = groupSize - toonsPresent
                if toonsWaiting > 0:
                    # We are still waiting on people.
                    subtext += f'\n{toonsWaiting} Not Nearby'
                else:
                    # Everyone is here!
                    subtext += '\nAll Present'

        # Add the toon count.
        subtext += f'\n{len(self.group.avIds)}/{groupSize} Toons'

        # With our text formatted, update the GUI text.
        self['text'] = f'{groupName}\1TextSmaller\1{subtext}\2'

        # And the icon.
        # self['image'] = self.GROUP_ICONS[icon]


if __name__ == "__main__":
    bFriendsList = DirectButton(
        image=(sp_gui.find('**/Icon_N'),
               sp_gui.find('**/Icon_P'),
               sp_gui.find('**/Icon_H')),
        relief=None,
        parent=aspect2d,
        scale=0.5,
    )
    gui = SocialPanelGroupSubtext(
        parent=bFriendsList,
        # any kwargs go here
    )
    GUITemplateSliders(
        gui,
        'pos', 'scale'
    )
    base.run()
