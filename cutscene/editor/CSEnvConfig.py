"""
The configuration file for the Cutscene Editor.

Run CutsceneEditorStart in order to execute these changes.
"""
import json
from json import JSONDecodeError
import random
from toontown.cutscene.repository.CutsceneLoader import CutsceneLoader
from toontown.cutscene.repository.CutsceneKeyEnum import CutsceneKeyEnum

# The cutscene we are working on.
CutsceneEditKey = CutsceneKeyEnum.Trailer_MajorPlayer


# Are we editing an existing cutscene?
# If this is False, we instead build our cutscene dictionary from the autosave.
EditMode = False


# Category names to hide in the editor.
HiddenCategoryNames = (
    # 'AudioSequence',
    # 'ParticleSequence',
    # 'CogBossSequence',
    # 'GUISequence',
)


def makeCutsceneDict() -> dict:
    if EditMode:
        return {}
    cutsceneLoader = CutsceneLoader.createLoader(key=CutsceneEditKey, editor=True)
    return cutsceneLoader.getCutsceneDict()


def createCutscene(cutsceneDict) -> list:
    """
    Returns the event list to use.

    :param cutsceneDict: Refers to the dict created in makeCutsceneDict.
    """
    if not EditMode:
        try:
            # First, see if there's anything to load.
            success = False
            with open('cutscene_editor_autosave.json', mode='r') as f:
                line = f.readline()
                if line:
                    success = True
            # If so, normal load.
            if success:
                with open('cutscene_editor_autosave.json', mode='r') as f:
                    c = json.load(f)
            # Otherwise, empty dict.
            else:
                c = {}
        except (JSONDecodeError, FileNotFoundError) as e:
            print("Error loading cutscene autosave.")
            raise e
        from toontown.cutscene.editor.CSEditorClasses import Cutscene
        cutscene = Cutscene.fromDict(cutsceneDict=cutsceneDict, cutsceneData=c)
        return cutscene.events
    else:
        # Otherwise, we just create one using the setup func.
        cutsceneLoader = CutsceneLoader.createLoader(key=CutsceneEditKey, editor=True)
        cutsceneDict.update(cutsceneLoader.cutsceneDict)
        return cutsceneLoader.makeCutsceneObject().events
