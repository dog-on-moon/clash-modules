"""
The main file of the Cutscene Editor.

Initialize settings in the CutsceneEditorConfig.
Run the Cutscene Editor by running CSEnvStart.py.
"""
from panda3d.core import *
from tools.headless.headlessbase import HeadlessStart
from tools.headless.headlessbase.HeadlessBase import HeadlessBase


class CutsceneEditorBase(HeadlessBase):

    def __init__(self):
        super().__init__(wantHotkeys=False)
        self.initCR()
        self.startHeadlessShow()

    def start(self, _=None):
        # Load audio manager
        self.initSounds()

        # Load editor manager
        from toontown.cutscene.editor.CSEditorManager import CSEditorManager

        self.editor = CSEditorManager()
        taskMgr.doMethodLater(30, self.printRepeat, 'editor-autosave')

        # Load injector as well
        from toontown.utils.DeveloperInjector import startInjector
        startInjector()

        # Accept oobe
        self.accept('f2', self.oobe)

    def printRepeat(self, task):
        self.editor.autosave()
        task.delayTime = 20
        return task.again

    def exitShow(self, errorCode = None):
        self.notify.info('Exiting Toontown: errorCode = %s' % errorCode)
        if self.editor:
            print('Closing Editor! Printing...')
            self.editor.autosave()
            print()
        import sys
        sys.exit()

    def run(self):
        taskMgr.doMethodLater(0.05, self.start, 'start')
        try:
            taskMgr.run()
        except SystemExit:
            self.notify.info('Normal exit.')
            try:
                self.destroy()
            except KeyError:
                # cleanup race condition with the main menu... i guess???
                pass
            raise
        except:
            self.notify.warning('Handling Python exception.')
            if getattr(self, 'cr', None):
                self.cr.flush()
                self.cr.sendDisconnect()
            self.notify.info('Exception exit.\n')

            self.destroy()
            import traceback
            traceback.print_exc()
