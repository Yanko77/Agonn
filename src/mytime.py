from __future__ import annotations
import time
import random

"""
This module contains the game time manager
"""

class Hour:
    """
    Represents an hour on 24h format.
    
    Example:
        Hour("10:30") and Hour(10, 30) both represent 10h30
    """

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
    

class Date:
    """
    Represents a Date on format <nth day><hour>.

    Example:
        Date(3, Hour(10, 30)) represents the 3th day at 10h30
    """

    def __init__(self,
                 days: int,
                 hour: Hour):
        
        if days < 0:
            raise ValueError(f"Date object cannot be defined with `days`={days}")

        self.days = days
        self.hour = hour
    
    def is_between(self, other1: Date, other2: Date) -> bool:
        """
        Returns True if this Date objects is between other1 and other2.
        """
        if other1 == other2:
            return self == other1
        elif other1 < other2:
            return other1 <= self < other2
        else:
            return other1 <= self or self < other2

    def __str__(self):
        return f'{self.days} {self.hour}'

    def __eq__(self, other) -> bool:
        if not isinstance(other, Date):
            raise TypeError('Can only compare two Date objects')

        return self.days == other.days and self.hour == other.hour

    def __lt__(self, other) -> bool:
        if not isinstance(other, Date):
            raise TypeError('Can only compare two Date objects')

        return self.days == other.days and self.hour < other.hour or self.days < other.days

    def __le__(self, other) -> bool:
        if not isinstance(other, Date):
            raise TypeError('Can only compare two Date objects')

        return self == other or self < other
    

class TimeManager:

    """
    Manages the game time.
    """

    TIME_RATIO = 60  # 1 hour in real time equals to TIME_RATIO seconds ingame

    def __init__(self):
        self.clock = Clock()

        self._time = 0  # Time value. Elapsed time in 10E-9 seconds since the game start.
    
    def update(self):
        incr = self.clock.tick()
        self.incr_time(incr)

    def incr_time(self, value: int):
        self._time += value

    
    def get(self) -> int:
        """
        Returns the elapsed time in seconds since the game start.
        """
        return ns_to_s(self._time)

    @property
    def day(self) -> int:
        """
        Returns the current day.
        """
        return self.get() // (self.TIME_RATIO * 24)

    @property
    def hour(self) -> Hour:
        """
        Returns the current hour.
        """

        current_daytime = self.get() % (self.TIME_RATIO * 24)

        hours = current_daytime // self.TIME_RATIO
        minutes = current_daytime % self.TIME_RATIO

        return Hour(hours, minutes)

    @property
    def now(self) -> Date:
        """
        Returns current date.
        """
        return Date(self.day, self.hour)


class Clock:
    def __init__(self):
        self.speed = 100

        self.initial_time = time.perf_counter_ns()
        self._prev_time = self.initial_time
    
    @property
    def elapsed_time(self) -> int:
        """
        Returns the real elapsed time in ns since the start of the game
        """
        return time.perf_counter_ns() - self.initial_time
    
    def tick(self) -> int:
        """
        Updates this clock and returns the value to add to game current time value.
        """
        _time = self.elapsed_time

        raw_incr = _time - self._prev_time

        self._prev_time = _time

        return raw_incr * self.speed // 100

def ns_to_s(value: int) -> int:
    """
    `value` is a time value in 10E-9 seconds.
    Returns `value` after conversion in seconds (floor value).
    """
    return value // 10**9

def s_to_ns(value: int) -> int:
    """
    `value` is a time value in seconds.
    Returns `value` after conversion in 10E-9 seconds (floor value).
    """
    return value * 10**9


def random_hour(hour1: Hour, hour2: Hour) -> Hour:
    """
    Returns a random Hour object between hour1 and hour2.
    """
    if hour1.hours <= hour2.hours:
        hours_digit = random.randint(hour1.hours, hour2.hours)
    else:
        hours_digit = random.choice((
            random.randint(hour1.hours, 23),
            random.randint(0, hour2.hours)
        ))

    if hours_digit == hour1.hours:
        minutes_digit = random.randint(hour1.minutes, 59)
    elif hours_digit == hour2.hours:
        minutes_digit = random.randint(0, hour2.minutes)
    else:
        minutes_digit = random.randint(0, 59)

    return Hour(hours_digit, minutes_digit)


def round_to_quarter(hour: Hour) -> Hour:
    """
    Rounds an Hour object to the nearest quarter-hour.
    """

    quarter = 0

    while not -7 <= hour.minutes - quarter <= 7 and quarter < 60:
        quarter += 15

    return Hour(
        hour.hours + quarter // 60,
        quarter
    )