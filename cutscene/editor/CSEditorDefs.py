"""
Definitions for the CS Editor.
"""
from typing import List, Set

from toontown.cutscene.CutsceneSequenceBase import cutsceneMethodDefs
from toontown.cutscene.editor.CSEditorClasses import *
from toontown.cutscene.editor.CSEditorEnums import *

# Important initialization import
from toontown.cutscene.sequences import (
    AudioSequence,
    CameraSequence,
    CogBattleSequence,
    GeneralSequence,
    ParticleSequence,
    SuitSequence,
    ToonSequence,
    CogBossSequence,
    GUISequence,
    EnvironmentSequence,
    ToonExpressionSequence,
)

# This is a useful debug list that can be used to exclude certain event enums
# from actually generating any sequences within a cutscene. Used for figuring out
# where something is going wrong.
EventExcludeList: Set[EventDefinitionEnum] = {
    # EventDefinitionEnum.reparentCamera,
    # EventDefinitionEnum.moveCameraPosHpr,
    # EventDefinitionEnum.animateAllToons,
    # EventDefinitionEnum.particleSystemRun,
    # EventDefinitionEnum.moveParticleSystemPos,
    # EventDefinitionEnum.turnToonsToPoint,
    # EventDefinitionEnum.rotateNode,
    # EventDefinitionEnum.hideNode,
    # EventDefinitionEnum.reparentNode,
    # EventDefinitionEnum.moveNode,
    # EventDefinitionEnum.pingpongAllToons,
    # EventDefinitionEnum.doScreenFade,
    # EventDefinitionEnum.moveToonsToBattlePos,
    # EventDefinitionEnum.showNode,
    # EventDefinitionEnum.nodePosHprScale,
    # EventDefinitionEnum.timeSleep,
}


# A kept-up list of all EventDefinitions.
# EventDefinitions are defined in the docstrings
# of the sequenceClasses defined above.
eventDefinitions = {}  # type: Dict[EventDefinitionEnum, EventDefinition]


# The ordered list of event definitions.
# Has strings for the names.
orderedEventDefinitionList = []  # type: List[Union[EventDefinition, str]]

"""
Small Comprehension Below
"""


# We'll go through all of the sequenceClasses now to check
# all of their methods and see which ones qualify
# for becoming Event Definitions.


categorizedEventDefinitions = {}
for method, methodDef in cutsceneMethodDefs.items():
    methodEnum = methodDef['enum']
    newEventDef = EventDefinition(
        name=methodDef['name'],
        method=method,
        arguments=methodDef['args'],
        enum=methodEnum,
        category=methodDef['category'],
    )
    eventDefinitions[methodEnum] = newEventDef
    if methodDef['category'] not in categorizedEventDefinitions:
        categorizedEventDefinitions[methodDef['category']] = []
    if not methodDef['hidden']:
        categorizedEventDefinitions[methodDef['category']].append(newEventDef)

# Add these categories to the ordered event definition list.
for categoryName, methodDefList in categorizedEventDefinitions.items():
    orderedEventDefinitionList.append(categoryName)
    # Add the sorted list to the event def list.
    methodDefList.sort(key=lambda x: x.name)
    orderedEventDefinitionList.extend(methodDefList)


# Some editor defaults.
firstEvent = Event(
    name='Initialization',
    time=0.0,
    subEvents=[]
)
