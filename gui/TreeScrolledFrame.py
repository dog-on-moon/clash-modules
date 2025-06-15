from toontown.utils.ColorHelper import hexToPCol

if __name__ == "__main__":
    from tools.headless.headlessbase import HeadlessStart
    from tools.headless.headlessbase.HeadlessBase import HeadlessBase
    base = HeadlessBase(wantHotkeys=False)
    if __debug__:
        from toontown.utils.DeveloperInjector import startInjector
        startInjector()
    # base.initCR()  # defines base.cr
    # base.startHeadlessShow()

from toontown.gui.TTGui import kwargsToOptionDefs
from toontown.gui.GUITemplateSliders import GUITemplateSliders
from toontown.gui.EasyScrolledFrame import EasyScrolledFrame
from toontown.gui.EasyManagedButton import EasyManagedButton
from toontown.gui.GUINode import GUINode
from toontown.gui import UiHelpers
from toontown.utils.DirectNotifyCategory import DirectNotifyCategory
from toontown.utils.InjectorTarget import InjectorTarget
from direct.gui.DirectGui import *

from typing import List, Any, Union


class TreeItem:
    """
    A generic tree item for use in the TreeDictionary.
    """

    def __init__(self, value: Any, name: str = 'none', callback: callable = None, extraArgs: list = None, baseColor: str = 'ffffff'):
        self.value = value
        self.name = name
        self.callback = callback
        self.extraArgs = extraArgs
        self.baseColor = baseColor

    def getValue(self) -> Any:
        return self.value

    def performCallback(self) -> bool:
        if self.callback is None:
            return False
        extraArgs = self.extraArgs or []
        self.callback(*extraArgs)
        return True


class TreeList(list):
    """
    A list of items in a Tree.
    """

    def __init__(self, name: str = 'base', baseColor: str = 'ffffff', **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.baseColor = baseColor


class TreeDictionary(dict):
    """
    A dictionary class to help organize and build a dictionary
    for usage in a TreeScrolledFrame.
    """

    def __init__(self, name: str = 'base', baseColor: str = 'ffffff', **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.baseColor = baseColor

    def setCategory(self, item: TreeItem, categories: List[Any], validate: bool = True):
        """Sets a value at a category depth."""
        categories = categories[:]
        if validate:
            self.validateCategories(categories)
        nextCategory = categories.pop(0)

        # If there are still categories to go through, keep scanning recursively.
        if categories:
            return self[nextCategory].setCategory(item, categories, validate=False)

        # Otherwise, set the value directly -- this is the right category.
        else:
            if nextCategory not in self:
                self[nextCategory] = TreeList(name=nextCategory, baseColor=item.baseColor)
            self[nextCategory].append(item)

    def getCategory(self, categories: List[Any], validate: bool = True):
        """Gets a value at a category depth."""
        categories = categories[:]
        if validate:
            self.validateCategories(categories)
        nextCategory = categories.pop(0)

        # If there are still categories to go through, keep scanning recursively.
        if categories:
            return self[nextCategory].getCategory(categories, validate=False)

        # Otherwise, check the value at this point.
        else:
            return self[nextCategory]

    def validateCategories(self, categories: List[Any]):
        """
        Given a list of categories, ensure that their entries are in the TreeDictionary.

        ```
        treeDict = TreeDictionary()
        treeDict.validateCategories(['planets', 'mountains', 'trees'])
        print(treeDict)
        > {'planets': {'mountains': 'trees': {}}}
        ```

        :param categories: The category order to ensure exists.
        """
        categories = categories[:]
        nextCategory = categories.pop(0)
        if categories and nextCategory not in self:
            self[nextCategory] = TreeDictionary(name=nextCategory)
            self[nextCategory].validateCategories(categories)


class TreeScrolledFrame(EasyScrolledFrame):
    """
    A ScrolledFrame that supports building tree-like structures from a dictionary.
    """

    @InjectorTarget
    def __init__(self, parent, **kw):
        # GUI boilerplate.
        optiondefs = kwargsToOptionDefs(
            frameSize=(-0.4, 0.4, -0.7, 0.7),
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.initialiseoptions(TreeScrolledFrame)
        self.treeDict = None
        self.openCategories = []

    def setTree(self, treeDict: TreeDictionary = None):
        """
        Builds the TreeScrolledFrame entries out of a TreeDictionary.
        """
        self.removeAllItems()
        if treeDict is not None:
            self.treeDict = treeDict

        def addTree(tree: TreeDictionary, depth: int = 0):
            if isinstance(tree, TreeList):
                for item in tree:
                    item = TreeScrolledItem(
                        tsf=self,
                        item=item,
                        depth=depth,
                    )
                    self.addItem(item=item)
            else:
                for key, subTreeDict in tree.items():
                    item = TreeScrolledItem(
                        tsf=self,
                        item=subTreeDict,
                        depth=depth,
                    )
                    self.addItem(item=item)
                    if subTreeDict in self.openCategories:
                        addTree(subTreeDict, depth=depth + 1)

        addTree(self.treeDict)
        self.updateItemPositions()

    def updateItemPositions(self):
        super().updateItemPositions()
        for item in self.canvasItems:
            item.updateItemColor()

    def openItem(self, item: Union[TreeItem, TreeDictionary, TreeList]):
        """Opens an item."""
        if isinstance(item, (TreeDictionary, TreeList)):
            # Time to recursively dig into this!!
            if item in self.openCategories:
                self.openCategories.remove(item)
            else:
                self.openCategories.append(item)
            self.setTree()

        elif isinstance(item, TreeItem):
            # Call this item's callback.
            item.performCallback()


class TreeScrolledItem(EasyManagedButton):

    @InjectorTarget
    def __init__(self, tsf: TreeScrolledFrame, item: Union[TreeItem, TreeDictionary], parent=aspect2d, **kw):
        # GUI boilerplate.
        optiondefs = kwargsToOptionDefs(
            relief=DGG.FLAT,
            frameSize=(0, 1.0, -0.1, 0),
            easyHeight=-0.1,
            text=self.getName(item),
            text_pos=(0.01411, -0.06526),
            text_scale=0.06,
            text_align=TextNode.ALeft,
            command=self.openItem,
            depth=[0, self.updateItemColor],
        )
        self.defineoptions(kw, optiondefs)
        super().__init__(parent, **kw)
        self.tsf = tsf
        self.item = item
        self.initialiseoptions(TreeScrolledItem)

        if isinstance(item, (TreeDictionary, TreeList)):
            self.extraText = DirectFrame(
                parent=self, relief=None,
                text='v',
                text_pos=(0.68195, -0.06467),
                text_scale=0.06,
            )

    def destroy(self):
        super().destroy()
        del self.tsf
        del self.item

    def getName(self, item):
        if isinstance(item, (TreeDictionary, TreeList, TreeItem)):
            return str(item.name)
        return 'none'

    def getItemIndex(self):
        frame = self['easyScrolledFrame'] or self.tsf
        if not frame:
            return 0
        filteredItems = [item for item in frame.canvasItems if item['depth'] == self['depth']]
        if self not in filteredItems:
            return 0
        return filteredItems.index(self)

    def updateItemColor(self):
        color = 1.0
        if self.getItemIndex() % 2:
            color *= 0.9
        color *= (0.8 ** self['depth'])
        r, g, b, _ = hexToPCol(self.item.baseColor)
        self['frameColor'] = (color * r, color * g, color * b, 1.0)

    def openItem(self):
        self.tsf.openItem(self.item)


if __name__ == "__main__":
    gui = TreeScrolledFrame(
        parent=aspect2d,
        # any kwargs go here
    )
    treeDict = TreeDictionary()
    for i in range(5):
        treeDict.setCategory(
            item=TreeItem(value=i, name=f'test {i}', callback=print, extraArgs=[f'pressed test {i}']),
            categories=['spaghetti', 'meatballs', 'problems'],
        )
        treeDict.setCategory(
            item=TreeItem(value=i, name=f'power {i}', callback=print, extraArgs=[f'pressed power {i}']),
            categories=['spaghetti', 'meatballs', 'problems'],
        )
        treeDict.setCategory(
            item=TreeItem(value=i, name=f'problems {i}', callback=print, extraArgs=[f'pressed problems {i}']),
            categories=['spaghetti', 'soup'],
        )
    gui.setTree(treeDict)
    GUITemplateSliders(
        gui.canvasItems[0].extraText,
        'text_pos', 'text_scale'
    )
    base.run()
