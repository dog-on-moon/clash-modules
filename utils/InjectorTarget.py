"""
This decorator can make any class a target on the injector.
Example below:

class MyClass:

    @InjectorTarget
    def __init__(self, value: int):
        self.value: int = value

MyClass(value=3)

print(base.myClass.value)
> 3
print(base.l_myClass[0].value)
> 3
"""


def InjectorTarget(initFunc):
    """
    A decorator to make a class an injector target.
    These -- obviously -- are memory leaks, but are only present on dev.
    """

    def wrapper(self, *args, **kwargs):
        # Run the init function.
        initFunc(self, *args, **kwargs)

        # Add references onto base.
        if __debug__:
            # Add the single target.
            name = self.__class__.__name__
            setattr(base, name, self)

            # Add the list target.
            listName = 'l_' + name
            if not hasattr(base, listName):
                setattr(base, listName, [])
            objList = getattr(base, listName)
            if self not in objList:
                objList.append(self)

    return wrapper
