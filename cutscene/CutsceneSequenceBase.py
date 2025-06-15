"""
This module contains the methods that are necessary
in order for defining your own cutscene sequence methods.
"""
from toontown.cutscene.editor.CSEditorClasses import EventArgument
from toontown.cutscene.editor.CSEditorEnums import EventDefinitionEnum
from toontown.cutscene.editor import CSEnvConfig


cutsceneEventUniqueId = 0


def getUniqueCutsceneId():
    """
    Gets a unique ID for cutscene usage
    :return: The unique ID
    """
    global cutsceneEventUniqueId
    cutsceneEventUniqueId += 1
    return cutsceneEventUniqueId


cutsceneMethodDefs = {}


def cutsceneSequence(name: str, enum: EventDefinitionEnum, hidden: bool = False):
    """
    Marks a given function as being a Cutscene Sequence.
    :param name:    The name of the sequence.
    :param enum:    The enum associated with the sequence.
    :param hidden:  Is this function hidden in the editor?
    :return:        A decorator that decorates the sequence appropriately.
    """
    def cutsceneDecorator(f):
        if __debug__:
            # We are in dev, so give this functionality for editor usage.
            methodDict = {
                'name': name,
                'enum': enum,
                'hidden': hidden
            }

            import inspect
            # Crazy lil' inspect line that gets us the name of the current module.
            sequenceName = inspect.currentframe().f_back.f_globals['__name__'].split('.')[-1]
            if sequenceName in CSEnvConfig.HiddenCategoryNames:
                return
            methodDict['category'] = sequenceName

            # Make event arguments.
            argumentList = []
            signature = inspect.signature(f)
            for parameter_name in signature.parameters:
                parameter = signature.parameters[parameter_name]
                if parameter.name == 'cutsceneDict':
                    continue
                argumentList.append(
                    EventArgument(
                        kwarg=parameter.name,
                        name=parameter.name,
                        type=parameter.annotation,
                        default=parameter.default,
                    )
                )

            # Set the arguments.
            methodDict['args'] = argumentList

            # Set this method defintion.
            cutsceneMethodDefs[f] = methodDict
        else:
            # We won't be using inspect, so we skip defining the args and category.
            cutsceneMethodDefs[f] = {
                'name': name,
                'enum': enum,
                'category': '',
                'args': [],
                'hidden': False,
            }
        return f

    # Return our decorator
    return cutsceneDecorator
