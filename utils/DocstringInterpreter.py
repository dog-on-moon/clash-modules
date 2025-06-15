"""
Functions to help read docstrings.
"""

import re


# SubEventEnum Regex
# Detects:
#   """
#   Enum: {stuff}
#   """
# Outputs:
#   The enum value (can make an enum with it after)

subEventEnumRegex = re.compile(r"(?:Enum: )(.*?)\n")


def getEnumFromDocstring(docstring):
    return subEventEnumRegex.search(docstring).groups()[0]
