from __future__ import annotations
import time

"""
This module contains the game time manager
"""

class Hour:

    def __init__(self, *args: str | tuple[int, int]):
        self.hours: int = None
        self.minutes: int = None

        # An hour string has been given
        if len(args) == 1 and type(args[0]) is str:
            self._init_from_str(args[0])
        
        # Two integer has been given : hours and minutes values
        elif len(args) == 2 and all([type(arg) is int for arg in args]):
            self._init_from_int(args[0], args[1])
        
        else:
            raise ValueError(f"An Hour object cannot be defined by: args = {args}")
        

    def _init_from_str(self, hour_str: str):
        """
        Initializes this Hour object from an hour string whose format is : "<hour_value>:<minutes_value>".
        
        Examples:
            Hour("12:30")
            = 12h30

            Hour("100:30")
            Raises a ValueError
        """
        try:
            hours, minutes = map(int, hour_str.split(":"))

            assert 0 <= hours <= 23
            assert 0 <= minutes <= 59

            self.hours = hours
            self.minutes = minutes
            
        except:
            raise ValueError(f"An Hour object cannot be defined by: args[0] = {hour_str}")


    def _init_from_int(self, hours: int, minutes: int):
        """
        Initializes this Hour object from two integers : the hour and the minute values.

        Examples:
            Hour(10, 50)
            = 10h50

            Hour(100, 30)
            Raises a ValueError
        """
        try:
            assert 0 <= hours <= 23
            assert 0 <= minutes <= 59
        except:
            raise ValueError(f"An Hour object cannot be defined by: args = ({hours}, {minutes})")

        self.hours = hours
        self.minutes = minutes

    def is_between(self, other1: Hour, other2: Hour) -> bool:
        """
        Returns True if this Hour object is between other1 and other2.
        """
        if other1 == other2:
            return self == other1
        elif other1 < other2:
            return other1 <= self < other2
        else:
            return other1 <= self or self < other2

    def __str__(self):
        return f'{self.hours}:{self.minutes}'

    def __eq__(self, other) -> bool:
        if not isinstance(other, Hour):
            raise TypeError('Can only compare two Hour objects')

        return self.hours == other.hours and self.minutes == other.minutes

    def __lt__(self, other) -> bool:
        if not isinstance(other, Hour):
            raise TypeError('Can only compare two Hour objects')

        return self.hours == other.hours and self.minutes < other.minutes or self.hours < other.hours

    def __le__(self, other) -> bool:
        if not isinstance(other, Hour):
            raise TypeError('Can only compare two Hour objects')

        return self == other or self < other

    def __repr__(self):
        return f'{self.hours}:{self.minutes}'