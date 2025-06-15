from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from direct.gui.DirectGui import *
from panda3d.core import *
from toontown.menu.MainMenuGui import MainMenuButton
from toontown.quest3 import QuestDialogue
from toontown.quest3.base.QuestText import QuestText
from toontown.toon.LocalToon import LocalToon
from toontown.toon import ToonDNA, AccessoryGlobals
from toontown.toonbase import TTLocalizer
import copy
import random

# Page Vars
from toontown.gui.TTGui import SizerFrame

itemFrameXorigin = -0.237
listXorigin = -0.02
listFrameSizeX = 0.67
listZorigin = -0.96
listFrameSizeZ = 1.04
title_text_scale = 0.12
arrowButtonScale = 1.3
rightSideItemsX = 0.36
maxCommandNameLength = 21
maxCommandNameLengthList = 16
textRolloverColor = Vec4(1, 1, 0, 1)
textDownColor = Vec4(0.5, 0.9, 1, 1)
textDisabledColor = Vec4(0.4, 0.8, 0.4, 1)

HATS = 0
GLASSES = 1
BACKPACK = 2


@DirectNotifyCategory()
class ToonAccessoryPlacementPanel:

    def __init__(self):
        self.leftPanel = DirectFrame(
            parent=base.aspect2d, relief=None, geom=DGG.getDefaultDialogGeom(),
            pos=(-1.2, 0, 0), geom_scale=(1, 1, 1.5)
        )
        self.rightPanel = DirectFrame(
            parent=base.aspect2d, relief=None, geom=DGG.getDefaultDialogGeom(),
            pos=(1.2, 0, 0), geom_scale=(1, 1, 1.5)
        )
        self.middlePanel = DirectFrame(
            parent=base.aspect2d, relief=None, geom=DGG.getDefaultDialogGeom(),
            pos=(0, 0, 0.85), geom_scale=(0.9, 1, 0.25)
        )

        self.accessoryMode = HATS
        self.accessorySelected = None
        self.accessoryFrames = {}
        self.copiedTuple = ()

        self.frozen = False
        self.funMode = True

        self.placementButtons = []

        self.load()

    def load(self):
        gui = loader.loadModel("phase_3/models/gui/ttcc_menu_buttons")
        friendsGui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        buttons = loader.loadModel('phase_3/models/gui/ttcc_gui_generalButtons')
        eraserGui = loader.loadModel('phase_3.5/models/gui/optionspage/keybinds_gui.bam')
        genericGui = loader.loadModel('phase_3.5/models/gui/optionspage/options_page')
        self.title = DirectLabel(parent=self.middlePanel, relief=None, text='N/A', text_scale=0.1,
                                 textMayChange=1, pos=(0, 0, -0.04), text_pos=(0, 0.09),)
        self.updateTitle()

        # Left Page
        # region Accessory change buttons
        self.modeHat = MainMenuButton(parent=self.leftPanel, relief=None, text="Hats",
                                          text_scale=0.05, image_scale=(.3, .09, .09), image1_scale=(.3, .09, .09),
                                          image2_scale=(.3, .09, .09), image3_scale=(.3, .09, .09),
                                          image3_color=(.75, .75, .75, 1), text_align=TextNode.ACenter,
                                          image=(gui.find('**/menubtn'), gui.find('**/menubtn-press'),
                                                 gui.find('**/menubtn')), text_pos=(0, -0.02),
                                          text_fg=Vec4(1, 1, 1, 1), text_style=3, command=self.changeMode,
                                          pos=(-0.3, 0, 0.7), extraArgs=[HATS])
        self.modeGlasses = MainMenuButton(parent=self.leftPanel, relief=None, text="Glasses",
                                      text_scale=0.05, image_scale=(.3, .09, .09), image1_scale=(.3, .09, .09),
                                          image2_scale=(.3, .09, .09), image3_scale=(.3, .09, .09),
                                      image3_color=(.75, .75, .75, 1), text_align=TextNode.ACenter,
                                      image=(gui.find('**/menubtn'), gui.find('**/menubtn-press'),
                                             gui.find('**/menubtn')), text_pos=(0, -0.02),
                                      text_fg=Vec4(1, 1, 1, 1), text_style=3, command=self.changeMode,
                                      pos=(0, 0, 0.7), extraArgs=[GLASSES])
        self.modeBackpack = MainMenuButton(parent=self.leftPanel, relief=None, text="Backpacks",
                                      text_scale=0.05, image_scale=(.3, .09, .09), image1_scale=(.3, .09, .09),
                                          image2_scale=(.3, .09, .09), image3_scale=(.3, .09, .09),
                                      image3_color=(.75, .75, .75, 1), text_align=TextNode.ACenter,
                                      image=(gui.find('**/menubtn'), gui.find('**/menubtn-press'),
                                             gui.find('**/menubtn')), text_pos=(0, -0.02),
                                      text_fg=Vec4(1, 1, 1, 1), text_style=3, command=self.changeMode,
                                      pos=(0.3, 0, 0.7), extraArgs=[BACKPACK])
        # endregion
        # region Accessory List
        buttonXstart = 0.16
        itemFrameZorigin = 0.96
        backgroundvOffset = 0.395
        self.accessoryList = DirectScrolledList(parent=self.leftPanel, relief=None, pos=(-0.173, 0, -0.1),
                                                itemFrame_pos=(-0.237 , 0, 0.565),
                                                itemFrame_scale=1.0, itemFrame_relief=DGG.SUNKEN,
                                                itemFrame_frameSize=(-0.02, -0.02 + 0.87, -0.96 + backgroundvOffset , -0.96 + 0.64 + backgroundvOffset),
                                                itemFrame_frameColor=(0.85, 0.95, 1, 1),
                                                itemFrame_borderWidth=(0.01, 0.01), numItemsVisible=9, forceHeight=0.065,
                                                incButton_image = (friendsGui.find('**/FndsLst_ScrollUp'),
                                                                 friendsGui.find('**/FndsLst_ScrollDN'),
                                                                 friendsGui.find('**/FndsLst_ScrollUp_Rllvr'),
                                                                 friendsGui.find('**/FndsLst_ScrollUp')),
                                                incButton_relief = None,
                                                incButton_scale = (arrowButtonScale,
                                                                 arrowButtonScale,
                                                                 -arrowButtonScale),
                                                incButton_pos = (buttonXstart, 0,itemFrameZorigin - 0.999),
                                                incButton_image3_color = Vec4(1, 1, 1, 0.2),
                                                decButton_image = (friendsGui.find('**/FndsLst_ScrollUp'),
                                                                 friendsGui.find('**/FndsLst_ScrollDN'),
                                                                 friendsGui.find('**/FndsLst_ScrollUp_Rllvr'),
                                                                 friendsGui.find('**/FndsLst_ScrollUp')),
                                                decButton_relief = None,
                                                decButton_scale = (arrowButtonScale,
                                                                 arrowButtonScale,
                                                                 arrowButtonScale),
                                                decButton_pos = (buttonXstart, 0, itemFrameZorigin - 0.28),
                                                decButton_image3_color = Vec4(1, 1, 1, 0.2))
        self.leftPanel['state'] = DGG.NORMAL
        self.leftPanel.bind(DGG.WHEELUP, lambda _: self.scroll(1), [])
        self.leftPanel.bind(DGG.WHEELDOWN, lambda _: self.scroll(-1), [])
        self.accessoryList.bind(DGG.WHEELUP, lambda _: self.scroll(1), [])
        self.accessoryList.bind(DGG.WHEELDOWN, lambda _: self.scroll(-1), [])
        self.accessoryList.incButton.bind(DGG.WHEELUP, lambda _: self.scroll(1), [])
        self.accessoryList.incButton.bind(DGG.WHEELDOWN, lambda _: self.scroll(-1), [])
        self.accessoryList.decButton.bind(DGG.WHEELUP, lambda _: self.scroll(1), [])
        self.accessoryList.decButton.bind(DGG.WHEELDOWN, lambda _: self.scroll(-1), [])
        # endregion
        # region Search bar
        searchXOffset = 0.36
        searchYOffset = 0.5

        self.searchBar = DirectEntry(parent=self.leftPanel, relief=DGG.SUNKEN, initialText=TTLocalizer.FriendsListSearchBarDefaultText,
                                     scale=0.07, pos=(-0.74 + searchXOffset, 0, -0.7625 + searchYOffset), width=9, numLines=1, focus=0, cursorKeys=1,
                                     command=self.finishSearch)
        self.searchBar.bind(DGG.B1PRESS, self.updateSearch)

        self.eraser = DirectButton(parent=self.leftPanel, pos=(-0.02 + searchXOffset , 0, -0.74+ searchYOffset), image=eraserGui.find('**/eraser'),
                                   scale=(0.6, 1, 0.32), relief=None, frameSize=(0.1, -0.085, 0.175, -0.175),
                                   command=self.resetSearch)

        # endregion
        # region Accessory change buttons
        self.copyButton = MainMenuButton(parent=self.leftPanel, relief=None, text="Copy",
                                      text_scale=0.05, image_scale=(0.25, 0.15, 0.10), image1_scale=(0.25, 0.15, 0.10),
                                      image2_scale=(0.25, 0.15, 0.10), image3_scale=(0.25, 0.15, 0.10),
                                      image3_color=(.75, .75, .75, 1), text_align=TextNode.ACenter,
                                      image=(gui.find('**/menubtn'), gui.find('**/menubtn-press'),
                                             gui.find('**/menubtn')), text_pos=(0, -0.02),
                                      text_fg=Vec4(1, 1, 1, 1), text_style=3, command=self.copy,
                                      pos=(0.07, 0, -0.37), extraArgs=[])
        self.pasteButton = MainMenuButton(parent=self.leftPanel, relief=None, text="Paste",
                                          text_scale=0.05, image_scale=(0.25, 0.15, 0.10), image1_scale=(0.25, 0.15, 0.10),
                                          image2_scale=(0.25, 0.15, 0.10), image3_scale=(0.25, 0.15, 0.10),
                                          image3_color=(.75, .75, .75, 1), text_align=TextNode.ACenter,
                                          image=(gui.find('**/menubtn'), gui.find('**/menubtn-press'),
                                                 gui.find('**/menubtn')), text_pos=(0, -0.02),
                                          text_fg=Vec4(1, 1, 1, 1), text_style=3, command=self.paste,
                                          pos=(0.32, 0, -0.37), extraArgs=[])
        self.clipboardButton = MainMenuButton(parent=self.leftPanel, relief=None, text="Paste into Logs",
                                          text_scale=0.05, image_scale=(0.5, 0.15, 0.12), image1_scale=(0.5, 0.15, 0.12),
                                          image2_scale=(0.5, 0.15, 0.12), image3_scale=(0.5, 0.15, 0.12),
                                          image3_color=(.75, .75, .75, 1), text_align=TextNode.ACenter,
                                          image=(gui.find('**/menubtn'), gui.find('**/menubtn-press'),
                                                 gui.find('**/menubtn')), text_pos=(0, -0.02),
                                          text_fg=Vec4(1, 1, 1, 1), text_style=3, command=self.copyToClipboard,
                                          pos=(0.195, 0, -0.62), extraArgs=[])
        self.freezeButton = MainMenuButton(parent=self.leftPanel, relief=None, text="Freeze Toon",
                                              text_scale=0.05, image_scale=(0.5, 0.15, 0.12), image1_scale=(0.5, 0.15, 0.12),
                                              image2_scale=(0.5, 0.15, 0.12), image3_scale=(0.5, 0.15, 0.12),
                                              image3_color=(.75, .75, .75, 1), text_align=TextNode.ACenter,
                                              image=(gui.find('**/menubtn'), gui.find('**/menubtn-press'),
                                                     gui.find('**/menubtn')), text_pos=(0, -0.02),
                                              text_fg=Vec4(1, 1, 1, 1), text_style=3, command=self.toggleFrozen,
                                              pos=(0.195, 0, -0.50), extraArgs=[])
        self.resetButton = MainMenuButton(parent=self.leftPanel, relief=None, text="Reset to Defaults",
                                              text_scale=0.05, image_scale=(0.5, 0.15, 0.12), image1_scale=(0.5, 0.15, 0.12),
                                              image2_scale=(0.5, 0.15, 0.12), image3_scale=(0.5, 0.15, 0.12),
                                              image3_color=(.75, .75, .75, 1), text_align=TextNode.ACenter,
                                              image=(gui.find('**/menubtn'), gui.find('**/menubtn-press'),
                                                     gui.find('**/menubtn')), text_pos=(0, -0.02),
                                              text_fg=Vec4(1, 1, 1, 1), text_style=3, command=self.resetToDefaults,
                                              pos=(0.195, 0, -0.74), extraArgs=[], image_color=(1.0, 0, 0, 1.0),)
        self.funModeButton = MainMenuButton(parent=self.middlePanel, relief=None, text="Turn off Fun Mode",
                                              text_scale=0.05, image_scale=(0.5, 0.15, 0.12),
                                              image1_scale=(0.5, 0.15, 0.12), image2_scale=(0.5, 0.15, 0.12),
                                              image3_scale=(0.5, 0.15, 0.12), image3_color=(.75, .75, .75, 1),
                                              text_align=TextNode.ACenter, image=(gui.find('**/menubtn'),
                                                                                  gui.find('**/menubtn-press'),
                                                                                  gui.find('**/menubtn')),
                                              text_pos=(0, -0.02), text_fg=Vec4(1, 1, 1, 1), text_style=3,
                                              command=self.toggleFunMode, pos=(0.705, 0, 0.085), extraArgs=[],)
        # endregion
        # region Toon change buttons
        # self.speciesChange = DirectMiniSelect(ToonDNA.toonSpeciesTypes, 'Species', parent=self.leftPanel,
        #                                       pos=(-0.26, 0, -0.45), text_scale=0.07)
        self.headChange = DirectMiniSelect(ToonDNA.toonHeadTypes, 'Head Type', parent=self.leftPanel,
                                              pos=(-0.26, 0, -0.6), text_scale=0.07, callback=self.updateToon)
        self.torsoChange = DirectMiniSelect(ToonDNA.toonTorsoTypes[3:6], 'Torso Type', parent=self.leftPanel,
                                              pos=(-0.26, 0, -0.75), text_scale=0.07, callback=self.updateToon)
        # endregion
        # region Misc
        self.exitButton = DirectButton(parent=self.leftPanel, relief=None, scale=1.55, text=('', 'Exit', 'Exit'),
                                       text_align=TextNode.ACenter, text_scale=0.075, text_fg=Vec4(1, 1, 1, 1),
                                       text_shadow=Vec4(0, 0, 0, 1), text_pos=(-0.0125, -0.09), pos=(2.49, 0, 0.9),
                                       textMayChange=0, image=(buttons.find('**/CloseBtn_UP'),
                                                               buttons.find('**/CloseBtn_DN'),
                                                               buttons.find('**/CloseBtn_Rllvr')), command=self.destroy)
        # endregion

        gui.removeNode()
        friendsGui.removeNode()
        buttons.removeNode()
        eraserGui.removeNode()
        genericGui.removeNode()

        # Begin populating everything with our available commands.
        hatIndices      = [[ToonDNA.HatStyles[name][0],         HATS,       name] for name in ToonDNA.HatStyles]
        glassesIndices  = [[ToonDNA.GlassesStyles[name][0],     GLASSES,    name] for name in ToonDNA.GlassesStyles]
        backpackIndices = [[ToonDNA.BackpackStyles[name][0],    BACKPACK,   name] for name in ToonDNA.BackpackStyles]

        fullIndices = hatIndices + backpackIndices + glassesIndices
        fullIndices.sort(key=lambda x: x[0], reverse=True)  # sort by clothing id

        for accessoryPair in fullIndices:
            if accessoryPair[2] == 'none':
                continue
            accessoryButton = self.createAccessoryButton(*accessoryPair)
            self.accessoryList.addItem(accessoryButton)

        self.__updateAll()
        self.updateToon()

    def copy(self):
        if self.accessorySelected:
            self.copiedTuple = self.getPlacements()

    def paste(self):
        if self.copiedTuple and self.accessorySelected:
            self.makePlacementButtons(forcePlacements=self.copiedTuple)

    def copyToClipboard(self):
        print(repr(self))

    def toggleFunMode(self):
        self.funMode = not self.funMode
        self.funModeButton.setText(f"Turn {'off' if self.funMode else 'on'} Fun Mode")

    def russianRoulette(self):
        """
        Picks a random word from quest dialogue.
        """
        allQuestDialogue = [text for source in QuestDialogue.QuestTextGigaDict.values() \
            for textDict in source.values() for text in textDict.values()]

        words = []
        for _ in range(4):
            chosenString: QuestText = random.choice(allQuestDialogue)
            word: str = random.choice(chosenString.getDialogue())
            if 'avName' in word:
                word = base.localAvatar.getName()
            if '\x07' in word and not self.funMode:  # Anti-fun mechanism
                word = random.choice(word.split('\x07'))
            words.append(word)
        a, b, c, d = words
        self.title['text'] = f"{a} {b} {c} {d}"
        from toontown.utils.text import fitLabelTextToBounds
        fitLabelTextToBounds(0.87, 0.24, self.title, 'text0', keepTopOfTextAligned=True)

    def toggleFrozen(self):
        self.frozen = not self.frozen
        self.freezeToon()

    def freezeToon(self):
        if self.frozen:
            base.localAvatar.stopLookAround()
            base.localAvatar.disableSleeping()
            base.localAvatar.pose('neutral', 0)

    def resetToDefaults(self):
        if self.accessorySelected is None:
            return
        accessoryId = self.accessoryName2Id(self.accessorySelected)
        if self.accessoryMode == HATS:
            dna = self.headChange.value[:2]
            self.placement = copy.deepcopy(AccessoryGlobals.HatTransTable[dna])
            AccessoryGlobals.ExtendedHatTransTable[accessoryId][dna] = self.placement
        elif self.accessoryMode == GLASSES:
            dna = self.headChange.value[:2]
            self.placement = copy.deepcopy(AccessoryGlobals.GlassesTransTable[dna])
            AccessoryGlobals.ExtendedGlassesTransTable[accessoryId][dna] = self.placement
        elif self.accessoryMode == BACKPACK:
            dna = self.torsoChange.value[0]
            self.placement = copy.deepcopy(AccessoryGlobals.BackpackTransTable[dna])
            AccessoryGlobals.ExtendedBackpackTransTable[accessoryId][dna] = self.placement
        self.makePlacementButtons()
        self.updatePlacements()

    def updateTitle(self):
        """Update the title string to be emotionally relevant."""
        self.russianRoulette()

    def scroll(self, amount):
        self.accessoryList.scrollTo(self.accessoryList.index - amount)

    def updateSearch(self, _=None):
        base.localAvatar.lockControlsForEntry()
        if self.searchBar.get() == TTLocalizer.FriendsListSearchBarDefaultText:  # Lets remove the search prompt if it's there
            self.searchBar.set('')

    def finishSearch(self, _=None):
        self.searchBar['focus'] = 0  # Unfocus the search bar just in case it is focused when we are entering
        base.localAvatar.unlockControlsForEntry()
        self.__updateAll(self.searchBar.get())

    def changeMode(self, mode):
        self.accessoryMode = mode
        self.accessorySelected = None
        self.normalizeAllAccessoryButtons()
        self.cleanPlacementButtons()
        self.__updateAll()

    def __updateAll(self, searchedText=""):
        self.__removeAllInList()
        for accessoryTuple in list(self.accessoryFrames.values()):
            accessoryButton, accessoryType, accessoryName = accessoryTuple
            searchResult = True
            if searchedText:
                parse = searchedText.lower().replace(" ", "")
                realName = self.getRealName(accessoryType, accessoryName).lower().replace(" ", "")
                result = realName.find(parse)
                if result == -1:
                    searchResult = False
            if searchResult and accessoryButton not in self.accessoryList['items'] and accessoryType == self.accessoryMode:
                self.accessoryList.addItem(accessoryButton, refresh=0)
                accessoryButton.show()
        self.accessoryList.refresh()

    def __removeAllInList(self):
        if not hasattr(self, 'accessoryFrames'):
            return
        # prevent failfast
        iterateList = self.accessoryList['items'][:]
        for accessoryButton in iterateList:
            self.accessoryList.removeItem(accessoryButton, refresh=0)
            accessoryButton.hide()
        # for accessoryTuple in list(self.accessoryFrames.values()):
        #     accessoryButton = accessoryTuple[0]
        #     if accessoryButton in self.accessoryList['items']:
        #         self.accessoryList.removeItem(accessoryButton, refresh=0)
        #         accessoryButton.hide()
        self.accessoryList.refresh()

    def resetSearch(self):
        self.searchBar.set('')
        self.finishSearch()
        self.searchBar.set(TTLocalizer.FriendsListSearchBarDefaultText)

    def destroy(self):
        if hasattr(base, 'apPanel') and base.apPanel:
            del base.apPanel

        self.finishSearch()
        self.leftPanel.destroy()
        self.rightPanel.destroy()
        self.middlePanel.destroy()
        self.cleanPlacementButtons()
        del self.accessoryFrames

    """
    Left Page
    All of these methods handle the left hand side of the page.
    This includes
    - Updating the list
    - Handling command select events
    """

    def getRealName(self, accessoryType, accessoryName):
        realName = 'UNDEFINED_NAME'
        if accessoryType == HATS and accessoryName in TTLocalizer.HatStylesDescriptions:
            realName = TTLocalizer.HatStylesDescriptions[accessoryName]
        elif accessoryType == GLASSES and accessoryName in TTLocalizer.GlassesStylesDescriptions:
            realName = TTLocalizer.GlassesStylesDescriptions[accessoryName]
        elif accessoryType == BACKPACK and accessoryName in TTLocalizer.BackpackStylesDescriptions:
            realName = TTLocalizer.BackpackStylesDescriptions[accessoryName]
        return realName

    def createAccessoryButton(self, accessoryIndex, accessoryType, accessoryName):
        """
        Generates an accessory button.
        """

        realName = self.getRealName(accessoryType, accessoryName)

        # Generate the buttons
        accessoryButton = DirectButton(relief = None,
                                       text = realName, text_scale = 0.06,
                                       text_align = TextNode.ALeft, text1_bg = textDownColor,
                                       text2_bg = textRolloverColor, text3_fg = textDisabledColor, textMayChange = 1,
                                       command = self.selectAccessory, extraArgs = [accessoryName])
        accessoryButton.bind(DGG.WHEELUP, lambda _: self.scroll(1), [])
        accessoryButton.bind(DGG.WHEELDOWN, lambda _: self.scroll(-1), [])

        # Now get it ready for the big return
        accessoryTuple = (accessoryButton, accessoryType, accessoryName)
        self.accessoryFrames[accessoryName] = accessoryTuple
        return accessoryButton

    def normalizeAllAccessoryButtons(self):
        for tuple in self.accessoryFrames.values():
            button = tuple[0]
            button['state'] = DGG.NORMAL

    def updateAccessoryButtonState(self, accessoryName, selected):
        """
        Updates the provide shard button state
        """
        buttons = self.accessoryFrames[accessoryName]
        if selected:
            state = DGG.DISABLED
        else:
            state = DGG.NORMAL
        buttons[0]['state'] = state

    def selectAccessory(self, accessoryName):
        """
        Updates both the left and the right page to display the selected commands information.
        """
        if self.accessorySelected:  # Enable the currently disabled button
            self.updateAccessoryButtonState(self.accessorySelected, False)

        # Update the scroll list (Left Page)
        self.updateAccessoryButtonState(accessoryName, True)
        self.accessorySelected = accessoryName

        self.updateTitle()

        # Update the toon.
        accessoryButton, accessoryType, accessoryName = self.accessoryTuple
        if accessoryType == HATS:
            aid, tex, col = ToonDNA.HatStyles[accessoryName]
            base.localAvatar.setHat(aid, tex, col)
        elif accessoryType == GLASSES:
            aid, tex, col = ToonDNA.GlassesStyles[accessoryName]
            base.localAvatar.setGlasses(aid, tex, col)
        elif accessoryType == BACKPACK:
            aid, tex, col = ToonDNA.BackpackStyles[accessoryName]
            base.localAvatar.setBackpack(aid, tex, col)

        self.makePlacementButtons()
        self.updatePlacements()
        # Update the Right Page
        # self.updateCommandInformation(accessoryId)

    @property
    def accessoryTuple(self):
        accessoryButton, accessoryType, accessoryName = self.accessoryFrames[self.accessorySelected]
        return accessoryButton, accessoryType, accessoryName

    def __repr__(self):
        if self.accessorySelected is None:
            return "Error copying string: Make sure you select an accessory!"
        accessoryButton, accessoryType, accessoryName = self.accessoryTuple
        realName = self.getRealName(accessoryType, accessoryName)
        accessoryId = self.accessoryName2Id(self.accessorySelected)
        prefix = str(accessoryId)
        pre = '{'
        post = '},'
        suffix = ''
        if self.accessoryMode == HATS:
            type = 'Hat'
            search = AccessoryGlobals.ExtendedHatTransTable
        elif self.accessoryMode == GLASSES:
            type = 'Glasses'
            search = AccessoryGlobals.ExtendedGlassesTransTable
        elif self.accessoryMode == BACKPACK:
            type = 'Backpack'
            search = AccessoryGlobals.ExtendedBackpackTransTable
        for dna in search[accessoryId]:
            suffix += f'"{dna}": {repr(search[accessoryId][dna])},\n     '
        return f" # {type} - {realName} - {accessoryName} \n {prefix}: {pre}{suffix}{post}\n"

    """
    Right Page
    Handles the right hand side of the page, who would have guessed...
    This includes
    - Updating the Command title.
    - Updating the "Say it" button.
    """

    def makePlacementButtons(self, forcePlacements=None):
        self.cleanPlacementButtons()
        if self.accessorySelected is None:
            return
        if forcePlacements is None:
            self.placement = self.getPlacements()
        else:
            self.placement = forcePlacements
        offset = 0.05
        self.posSizer = SizerFrame(self.rightPanel, 'Positions', 'xyz', self.xyz(),
                                   (-1, 1), self.updatePlacements, 0.50 + offset)
        self.hprSizer = SizerFrame(self.rightPanel, 'Rotations', 'hpr', self.hpr(),
                                   (0, 360), self.updatePlacements, 0.00 + offset)
        self.sizeSizer = SizerFrame(self.rightPanel, 'Scale', 'xyz', self.size(),
                                    (0.1, 0.3), self.updatePlacements, -0.5 + offset)
        self.placementButtons.append(self.posSizer)
        self.placementButtons.append(self.hprSizer)
        self.placementButtons.append(self.sizeSizer)

    def cleanPlacementButtons(self):
        for ui in self.placementButtons:
            ui.remove()
        self.placementButtons = []

    def getPlacements(self):
        """Gets the placements for the current placing accessory."""
        accessoryId = self.accessoryName2Id(self.accessorySelected)
        if self.accessoryMode == HATS:
            dna = self.headChange.value[:2]
            if accessoryId not in AccessoryGlobals.ExtendedHatTransTable:
                AccessoryGlobals.ExtendedHatTransTable[accessoryId] = copy.deepcopy(AccessoryGlobals.HatTransTable)
            if dna not in AccessoryGlobals.ExtendedHatTransTable[accessoryId]:
                AccessoryGlobals.ExtendedHatTransTable[accessoryId][dna] = copy.deepcopy(
                    AccessoryGlobals.HatTransTable[dna])
            return AccessoryGlobals.ExtendedHatTransTable[accessoryId][dna]
        elif self.accessoryMode == GLASSES:
            fullDna = self.headChange.value
            dna = self.headChange.value[:2]
            if accessoryId not in AccessoryGlobals.ExtendedGlassesTransTable:
                AccessoryGlobals.ExtendedGlassesTransTable[accessoryId] = copy.deepcopy(AccessoryGlobals.GlassesTransTable)
            if fullDna in AccessoryGlobals.ExtendedGlassesTransTable[accessoryId]:
                return AccessoryGlobals.ExtendedGlassesTransTable[accessoryId][fullDna]
            if dna not in AccessoryGlobals.ExtendedGlassesTransTable[accessoryId]:
                AccessoryGlobals.ExtendedGlassesTransTable[accessoryId][dna] = copy.deepcopy(
                    AccessoryGlobals.GlassesTransTable[dna])
            return AccessoryGlobals.ExtendedGlassesTransTable[accessoryId][dna]
        elif self.accessoryMode == BACKPACK:
            dna = self.torsoChange.value[0]
            if accessoryId not in AccessoryGlobals.ExtendedBackpackTransTable:
                AccessoryGlobals.ExtendedBackpackTransTable[accessoryId] = copy.deepcopy(AccessoryGlobals.BackpackTransTable)
            if dna not in AccessoryGlobals.ExtendedBackpackTransTable[accessoryId]:
                AccessoryGlobals.ExtendedBackpackTransTable[accessoryId][dna] = copy.deepcopy(
                    AccessoryGlobals.BackpackTransTable[dna])
            return AccessoryGlobals.ExtendedBackpackTransTable[accessoryId][dna]

    def updatePlacements(self, forcePlacement=None):
        """Updates the placements."""
        if not self.placementButtons:
            return
        if forcePlacement is None:
            xyz = self.posSizer.values
            hpr = self.hprSizer.values
            size = self.sizeSizer.values
            self.placement = (xyz, hpr, size)
        else:
            self.placement = forcePlacement
        geom = None
        accessoryId = self.accessoryName2Id(self.accessorySelected)
        if self.accessoryMode == HATS:
            geom = base.localAvatar.toonHat
            dna = self.headChange.value[:2]
            AccessoryGlobals.ExtendedHatTransTable[accessoryId][dna] = copy.deepcopy(self.placement)
        elif self.accessoryMode == GLASSES:
            geom = base.localAvatar.toonGlasses
            fullDna = self.headChange.value
            if fullDna in AccessoryGlobals.ExtendedGlassesTransTable[accessoryId]:
                AccessoryGlobals.ExtendedGlassesTransTable[accessoryId][fullDna] = copy.deepcopy(self.placement)
            else:
                dna = self.headChange.value[:2]
                AccessoryGlobals.ExtendedGlassesTransTable[accessoryId][dna] = copy.deepcopy(self.placement)
        elif self.accessoryMode == BACKPACK:
            geom = base.localAvatar.toonBackpack
            dna = self.torsoChange.value[0]
            AccessoryGlobals.ExtendedBackpackTransTable[accessoryId][dna] = copy.deepcopy(self.placement)
        geom.forcePlace()

    def setXyz(self, x, y, z):
        self.placement[0] = [x, y, z]
        self.updatePlacements()

    def setHpr(self, h, p, r):
        self.placement[1] = [h, p, r]
        self.updatePlacements()

    def setSize(self, sx, sy, sz):
        self.placement[2] = [sx, sy, sz]
        self.updatePlacements()

    def xyz(self):
        return self.placement[0]

    def hpr(self):
        return self.placement[1]

    def size(self):
        return self.placement[2]

    """
    Various misc methods.
    """

    def updateToon(self):
        """Updates the local avatar."""
        av: LocalToon = base.localAvatar
        dna = ToonDNA.ToonDNA(type='t', dna=av.style)
        dna.updateToonProperties(
            head=self.headChange.value,
            torso=self.torsoChange.value,
        )
        dnaNet = dna.makeNetString()
        av.setDNAString(dnaNet)
        self.updateTitle()
        self.freezeToon()
        self.makePlacementButtons()

    def accessoryName2Id(self, name):
        if self.accessoryMode == HATS:
            return ToonDNA.HatStyles[name][0]
        elif self.accessoryMode == GLASSES:
            return ToonDNA.GlassesStyles[name][0]
        elif self.accessoryMode == BACKPACK:
            return ToonDNA.BackpackStyles[name][0]


class DirectMiniSelect(DirectFrame):
    """
    Makes a small box with a few values that can be swapped between.
    """

    def __init__(self, values: list, label: str, callback=None, parent=None, **kw):
        super().__init__(parent, **kw)
        self.values = values[:]
        self.setText(values[0])

        self.index = 0
        self.callback = callback

        self.label = DirectLabel(
            parent=self, pos=(0, 0, 0.07), text=label, text_scale=0.07, relief=None
        )
        self.left = DirectButton(
            parent=self, pos=(-0.1, 0, 0), text='<', text_scale=0.07, relief=None,
            command=self.update, extraArgs=[-1]
        )
        self.right = DirectButton(
            parent=self, pos=(0.1, 0, 0), text='>', text_scale=0.07, relief=None,
            command=self.update, extraArgs=[1]
        )
        self.superleft = DirectButton(
            parent=self, pos=(-0.16, 0, 0), text='<', text_scale=0.07, relief=None,
            command=self.update, extraArgs=[-100]
        )
        self.superright = DirectButton(
            parent=self, pos=(0.16, 0, 0), text='>', text_scale=0.07, relief=None,
            command=self.update, extraArgs=[100]
        )

        self.updateButtonColors()

    def update(self, val):
        self.index += val
        self.index = max(0, min(self.index, len(self.values) - 1))
        self.setText(self.values[self.index])

        self.updateButtonColors()

        # run callback, pass our value
        if self.callback is not None:
            self.callback()

    def updateButtonColors(self):
        """updates the button colors to look not bad"""
        self.left['text_fg']  = (0, 0, 0, 1) if self.index != 0 else (0.65, 0.65, 0.65, 1)
        self.superleft['text_fg'] = (0, 0, 0, 1) if self.index != 0 else (0.65, 0.65, 0.65, 1)
        self.right['text_fg'] = (0, 0, 0, 1) if self.index != len(self.values) - 1 else (0.65, 0.65, 0.65, 1)
        self.superright['text_fg'] = (0, 0, 0, 1) if self.index != len(self.values) - 1 else (0.65, 0.65, 0.65, 1)

    @property
    def value(self):
        return self.values[self.index]
