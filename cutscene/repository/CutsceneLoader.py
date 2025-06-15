"""
The class, CutsceneLoader, is a special class that
will help you to organize CutsceneDicts, along with
producing a CutsceneDict from a json file.
"""
from typing import List, Optional

from direct.interval.FunctionInterval import Func
from direct.interval.MetaInterval import Parallel, Sequence

from toontown.cutscene.CutsceneParticles import getCutsceneParticleSystems
from toontown.cutscene.editor.CSEditorClasses import Cutscene

import json
from json import JSONDecodeError
from panda3d.core import VirtualFileSystem, Filename, AudioSound, NodePath

from toontown.cutscene.repository.CutsceneKeyEnum import CutsceneKeyEnum
from toontown.distributed import DelayDelete


class ExistingCutsceneKeyError(Exception):
    pass


CutsceneKeyMap = {}
CutsceneSetupFuncMap = {}


# Use this to define new cutscene data entries
def addCutsceneDataEntry(key, filePath):
    if key in CutsceneKeyMap:
        raise ExistingCutsceneKeyError(f"Key {key} already in cutscene map.")

    if not filePath.startswith('/'):
        filePath = '/' + filePath
    CutsceneKeyMap[key] = filePath


# Decorator for cutscene setup functions
def cutsceneSetup(key):
    def wrapper(func):
        # Given the key and func, add it to the cutscene setup func map.
        CutsceneSetupFuncMap[key] = func
        return func
    return wrapper


class CutsceneLoader:
    """
    A dedicated class for loading cutscene data.
    """

    def __init__(self, cutsceneKey: CutsceneKeyEnum = None, affectsCamera: bool = True):
        """
        Loads a cutscene into the CutsceneLoader.
        :param cutsceneKey: A key in the CutsceneKeyMap to read from.
        :param affectsCamera: A bool to determine whether or not Camera-related functions should play.
        """
        if cutsceneKey is not None:
            assert cutsceneKey in CutsceneKeyMap, f"Invalid cutsceneKey '{cutsceneKey}' used."
        self.cutsceneKey = cutsceneKey
        self.cutsceneDict = {
            'nodes': [render, hidden, camera],
            'affectsCamera': affectsCamera,
        }
        self.doCallback = None
        self.track = None

    def cleanup(self):
        """It's always healthy to cleanup after yourself."""
        del self.cutsceneKey
        del self.cutsceneDict
        del self.track

    @classmethod
    def createLoader(cls, key, editor: bool = False, affectsCamera: bool = True, maxPlayers: int = 4, **kwargs) -> 'CutsceneLoader':
        """
        Sets up and creates an entire cutscene loader.
        A setup function must exist for this to be sufficient.

        :param key: The key to reference the cutscene with.
        :param editor: Should the setup funcs use the editor flag?
                       (Don't set this to True unless you know what you're doing)
        :param affectsCamera: A bool to determine whether or not Camera-related functions should play.
        :param maxPlayers: Max number of players in this cutscene, used for Toon sequences
        :param kwargs: Any kwargs to be passed into the setup funcs.
        :return: The entire cutscene sequence.
        """
        # Attempt to setup the cutscene.
        setupFunc = CutsceneSetupFuncMap.get(key)
        if not setupFunc:
            raise KeyError(f"Setup function not made for key {key}.")

        # A setup function exists. Use it to create our cutscene loader.
        cutsceneLoader = setupFunc(editor=editor, **kwargs)  # type: CutsceneLoader
        cutsceneLoader.cutsceneKey = key
        cutsceneLoader.cutsceneDict['affectsCamera'] = affectsCamera
        cutsceneLoader.cutsceneDict['maxPlayers'] = maxPlayers
        return cutsceneLoader

    """
    Methods to populate the cutscene dict
    """

    def addToonsToCutscene(self, toonList: list, maxToonCount: int = None):
        """
        Adds Toons to the Cutscene Dict.
        :param toonList: A list of Toons to add.
        :param maxToonCount: The maximum potential toons in the cutscene. Usually optional.
        """
        toonList = toonList[:]
        if maxToonCount is not None:
            # Add Nones to the end of the toon list to pad space.
            if maxToonCount > len(toonList):
                toonList = toonList + ([None] * (maxToonCount - len(toonList)))

        # Now add to cutscene dict.
        self.cutsceneDict['toons'] = toonList

    def addSuitsToCutscene(self, suitList: list, maxSuitCount: int = None):
        """
        Adds Suits to the Cutscene Dict.
        :param suitList: A list of Suits to add.
        :param maxSuitCount: The maximum potential suits in the cutscene. Usually optional.
        """
        suitList = suitList[:]
        if maxSuitCount is not None:
            # Add Nones to the end of the suit list to pad space.
            if maxSuitCount > len(suitList):
                suitList = suitList + ([None] * (maxSuitCount - len(suitList)))

        # Now add to cutscene dict.
        self.cutsceneDict['suits'] = suitList

    def addBossesToCutscene(self, bossList: list, maxBossCount: int = None):
        """
        Adds Boss Cogs to the Cutscene Dict.
        :param bossList: A list of Cog Bosses to add.
        :param maxBossCount: The maximum potential Cog Bosses in the cutscene. Usually optional.
        """
        bossList = bossList[:]
        if maxBossCount is not None:
            # Add Nones to the end of the boss list to pad space.
            if maxBossCount > len(bossList):
                bossList = bossList + ([None] * (maxBossCount - len(bossList)))

        # Now add to cutscene dict.
        self.cutsceneDict['bosses'] = bossList

    def addActorsToCutscene(self, actorList: list):
        """Adds a list of actors to the cutscene dict."""
        self.cutsceneDict['actors'] = actorList

    def addNodesToCutscene(self, nodeList: list):
        """Adds a list of nodes to the cutscene dict."""
        self.cutsceneDict['nodes'] = self.cutsceneDict['nodes'] + nodeList

    def getNodeIndex(self, index: int):
        return self.cutsceneDict['nodes'][index]

    def addElevatorsToCutscene(self, elevatorList: list):
        """Adds a list of elevators to the cutscene dict."""
        self.cutsceneDict['elevators'] = elevatorList

    def addDialogueToCutscene(self, dialogueList: list):
        """Adds a list of dialogue to the cutscene dict."""
        self.cutsceneDict['messages'] = dialogueList

    def addSoundsToCutscene(self, soundList: list):
        """
        Adds a list of sounds to the cutscene dict.
        Takes file paths as strings or sound objects.
        """
        # If strings are passed in, load in sounds and replace them on the list.
        for i in range(len(soundList)):
            if isinstance(soundList[i], str):
                soundList[i] = base.loader.loadSfx(soundList[i])
        self.cutsceneDict['sounds'] = soundList

    def addMusicToCutscene(self, musicList: list):
        """
        Adds a list of music codes to the cutscene dict.
        Takes file paths as strings or sound objects.
        """
        self.cutsceneDict['music'] = musicList

    def addParticleSystemsToCutscene(self, cutscenePsNameList: list):
        """Adds a list of cutscene particles to the cutscene dict."""
        self.cutsceneDict['particles'] = getCutsceneParticleSystems(cutscenePsNameList)

    def addFunctionsToCutscene(self, functions: list):
        """Adds a list of functions to the cutscene dict."""
        self.cutsceneDict['functions'] = functions

    def addArgumentsToCutscene(self, arguments: list):
        """
        Adds a list of arguments to the cutscene dict.
        Can be individual arguments (special case for lists, see the note) or lists of arguments.

        Note: Due to the unwrapping process, lists that are intended as individual arguments are
        interpreted as multiple arguments. To prevent this, wrap them in an extra list.
        """
        self.cutsceneDict['arguments'] = arguments

    def addStuffToCutscene(self, *stuff,
                           music: List[str] = None,
                           particleNames: List[str] = None,
                           arguments: list = None,
                           expectedToonCount: Optional[int] = 4,
                           expectedSuitCount: Optional[int] = 4):
        """
        General stuff-adding function. Useful for the lazy.
        - stuff: Anything goes, but specifically:
            - Toons: Will be included in the Toon and Actor and Node list.
            - Suits: Will be included in the Suit and Actor and Node list.
            - Bosses: Will be included in the Boss and Node list.
            - Other actors: Will be included in the Actor and Node list.
            - Visual Effect Enums: Will be included in the Visual Effect Enum list.
            - Any AudioSound (loader.loadSfx): Will be included in the Sound list.
            - Any DistributedElevator: Will be included in the Elevator list.
            - Any Callable: Will be included in the Functions list.
            - Any NodePath: Will be included in the Node list.
            - Strings: Will be included in the Dialogue list.
        - music: A list of all music code strings to include in the Music list.
        - particleNames: A list of all particle names to include in the Particles list.
        - arguments: A list of all arguments to include in the arguments list.

        Other flags:
        - expectedToonCount: The anticipated Toon count. It's good to keep this accurate to the cutscene.
        - expectedSuitCount: The anticipated Suit count. It's good to keep this accurate to the cutscene.
        """
        if music is None:
            music = []
        if particleNames is None:
            particleNames = []
        if arguments is None:
            arguments = []

        toons = []
        suits = []
        bosses = []
        actors = []
        visualEffects = []
        sounds = []
        elevators = []
        callables = []
        nodes = []
        strings = []

        from toontown.toon.Toon import Toon
        from direct.actor.Actor import Actor
        from toontown.suit.BossCog import BossCog
        from toontown.suit.Suit import Suit
        from toontown.battle.visuals.VisualEffectEnums import VisualEffectEnum
        from toontown.building.DistributedElevator import DistributedElevator
        TYPE_MATCH = {
            Toon: (toons, actors, nodes),
            Suit: (suits, actors, nodes),
            BossCog: (bosses, nodes),
            Actor: actors,
            VisualEffectEnum: visualEffects,
            AudioSound: sounds,
            DistributedElevator: elevators,
            type(lambda: 0): callables,
            NodePath: nodes,
            str: strings,
        }

        # Over everything we're trying to add...
        for thing in stuff:

            # ...compare it to where it SHOULD go.
            thingsAdded = 0
            for objectType, objectLists in TYPE_MATCH.items():

                # Is this a thing?
                if isinstance(thing, objectType):
                    # Add to the list.
                    thingsAdded += 1

                    if type(objectLists) is not tuple:
                        objectLists.append(thing)
                    else:
                        for objectList in objectLists:
                            objectList.append(thing)

            if thing is None:
                # Technically, None is a valid thing because of how cutscene items get built with Toons and Suits.
                thingsAdded += 1

            # Exception if it is a bad item.
            if not thingsAdded:
                raise AttributeError(f'Cutscene item {thing} does not belong ANYWHERE!')

        # Add everything.
        if toons:
            self.addToonsToCutscene(toonList=toons, maxToonCount=expectedToonCount)
        if suits:
            self.addSuitsToCutscene(suitList=suits, maxSuitCount=expectedSuitCount)
        if bosses:
            self.addBossesToCutscene(bosses)
        if actors:
            self.addActorsToCutscene(actors)
        if sounds:
            self.addSoundsToCutscene(sounds)
        if elevators:
            self.addElevatorsToCutscene(elevators)
        if callables:
            self.addFunctionsToCutscene(callables)
        if nodes:
            self.addNodesToCutscene(nodes)
        if strings:
            self.addDialogueToCutscene(strings)
        if music:
            self.addMusicToCutscene(music)
        if particleNames:
            self.addParticleSystemsToCutscene(particleNames)
        if arguments:
            self.addArgumentsToCutscene(arguments)

    def getCutsceneDict(self):
        return self.cutsceneDict

    def getParticleSystems(self):
        return self.cutsceneDict['particles']

    """
    Methods to finally build the cutscene track
    """

    def buildCutscene(self, callback=None, delayDeleteToons=False, cleanupParticles: bool = True) -> Parallel:
        """
        Builds a cutscene from the CutsceneLoader.
        :return: A Parallel, containing all Cutscene events and happenings.
        """
        assert self.cutsceneKey is not None, "Cutscene key for this CutsceneLoader was not defined."
        self.doCallback = callback
        self.track = self.makeCutsceneObject().toTrack(callback=self.delayDeleteCallback)
        # If not in the editor, add cleanups to these particles
        if not self.cutsceneDict.get('isEditor', False) and cleanupParticles:
            particleCleanup = Parallel()
            for particles in self.cutsceneDict.get('particles', []):
                particleCleanup.append(Func(particles.cleanup))
            self.track = Sequence(self.track, particleCleanup)
        self.track.delayDeletes = []
        if delayDeleteToons:
            self.initDelayDeletes()
        return self.track

    def makeCutsceneObject(self):
        return Cutscene.fromDict(cutsceneDict=self.cutsceneDict, cutsceneData=self._loadJsonData())

    def _loadJsonData(self):
        # First, we need to actually do some re-formatting to the data,
        # so that json can load the string.
        jsonDataPath = self.cutsceneJsonPath
        if __debug__:
            jsonDataPath = '../resources' + jsonDataPath
        jsonDataPath = Filename(jsonDataPath)

        vfs = VirtualFileSystem.getGlobalPtr()

        return json.loads(vfs.readFile(jsonDataPath, True))

    @property
    def cutsceneJsonPath(self):
        return CutsceneKeyMap[self.cutsceneKey]

    """
    Cutscenes involving the delaydelete wrapper
    """

    def initDelayDeletes(self):
        """Inits DelayDeletes on a scene."""
        for toon in self.cutsceneDict.get('toons', []):
            if toon:
                self.track.delayDeletes.append(DelayDelete.DelayDelete(toon, f'Cutscene-{self.cutsceneKey}'))

    def delayDeleteCallback(self):
        """Wrapped version of the cutscene callback to support delaydeletes."""
        if self.doCallback:
            self.doCallback()
        DelayDelete.cleanupDelayDeletes(self.track)
        self.cleanup()
