"""
This file is used to generate unique ids.
"""

value = 0

def genId():
    global value
    value += 1
    return value
