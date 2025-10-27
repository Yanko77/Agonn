from __future__ import annotations
from typing import Callable
from enum import Enum


class Stat:
    """
    Represents a single stat.

    It's defined by its name.
    """

    def __init__(self, 
                 name: str):
        self.name = name


class StatsManager:
    """
    Manages all the Stat object of an entity.
    """

    def __init__(self):
        self._dict: dict[str, Stat] = {}
        self._buffs_dict: dict[str, list[StatBuff]] = {}
        
        self.rel_register = StatsRelRegister()

    
    @property
    def list(self) -> list[Stat]:
        """
        Returns the list of all the Stat.
        Order isn't fixed.
        """
        return self._dict.values()
    
    @property
    def names_list(self) -> list[str]:
        """
        Returns the list of all the Stat names.
        Order isn't fixed.
        """
        return self._dict.keys()
    
    def addStat(self, stat: Stat):
        """
        Adds a Stat to this StatsManager list.
        Raises a ValueError if a stat with the same name as `stat` already exists.
        """
        if self._dict.get(stat.name):
            raise ValueError(f"The Stat called '{stat.name}' already exists in this Manager")

        self._dict[stat.name] = stat

        # Init an empty buff list for this new Stat
        self.setBuffList(stat.name, list())

    def addBuff(self, buff: StatBuff, stat_name: str):
        """
        Adds a Buff to the Stat whose name is `stat_name`.
        Raises a ValueError if the given stat name is unknown.
        """
        buff_list = self.getBuffList(stat_name)

        # Find the index to insert the new buff
        i = 0
        while i < len(buff_list) and buff_list[i].prio >= buff.prio:
            i += 1
        
        # Insert the new buff
        if i == len(buff_list):
            buff_list.append(buff)
        else:
            buff_list = buff_list[:i] + [buff] + buff_list[i:]
        
        # Update the buff list
        self.setBuffList(stat_name, buff_list)
    
    def getValue(self, stat_name: str) -> int:
        """
        Returns the value of the contained stat whose name is `stat_name`.
        Raises a ValueError if it doesn't exist.
        """
        value = self.getObj(stat_name).value

        buffs_list = self.getBuffList(stat_name)

        for buff in buffs_list:
            value = buff.apply(value)

        return value

    def getObj(self, stat_name: str) -> Stat:
        """
        Returns the Stat object whose name is `stat_name`.
        Raises a ValueError if it doesn't exist.
        """
        try:
            res = self._dict[stat_name]
        except KeyError:
            raise ValueError(f"Unknown stat name : {stat_name}")

        return res

    def getBuffList(self, stat_name: str) -> list[StatBuff]:
        """
        Returns the list of all the StatBuff to be applied to the stat whose name is `stat_name`.
        The returned list is ordered by priority order.
        Raises a ValueError is the given stat name is unknown.
        """
        try:
            res = self._buffs_dict[stat_name]
        except KeyError:
            raise ValueError(f"Unknown stat name : {stat_name}")

        return res

    def setBuffList(self, stat_name: str, buff_list: list[StatBuff]):
        """
        Sets the buff list of the Stat whose name is `stat_name`.
        """
        self._buffs_dict[stat_name] = buff_list

class StatsRelRegister:
    """
    Represents a register of all the relationships between Stat objects.
    """

    def __init__(self):
        self._rel_dict: dict[str, set[str]] = {}
    
    def getRelList(self, stat_name: str) -> set[str]:
        """
        Returns the names of all the Stat objects that have a relationship 
            with the Stat whose name is `stat_name`.
        Raises a ValueError if it doesn't exist.
        """
        try:
            res = self._rel_dict[stat_name]
        except KeyError:
            raise ValueError(f"Unknown stat name : {stat_name}")
        return res


class StatBuff:
    """
    Represents a Stat buff.

    A Buff can be temporary.
    Its effect is applied after the Stat value calculation.

    It's defined by:
    - StatBuffType, the type of the buff
    - float, its value
    - int, its priority value
    """

    def __init__(self,
                 type_: StatBuffType,
                 value: float,
                 prio: int):
        self.type = type_
        self.value = value
        self.prio = prio
    
    def apply(self, value: int) -> int:
        """
        Applies this buff to the value `value`.
        Returns the result.
        """
        func = self.type.getFunc()
        return func(value, self.value)

    def __eq__(self, other):
        return isinstance(other, StatBuff) and self.type == other.type and self.value == other.value and self.prio == other.prio

class StatBuffType(Enum):
    """
    Represents a stat buff type.
    """
    FLAT_BONUS = 0
    MULTIPLIER = 1

    def getFunc(self) -> Callable[[int, int], int]:
        """
        Returns the function to use to apply the buff on a value.
        """
        _funcs = [
            self.flatBonusApply,
            self.multiplierApply
        ]
        return _funcs[self.value]
    
    @staticmethod
    def flatBonusApply(stat_value: int, buff_value: int) -> int:
        return round(stat_value + buff_value)
    
    @staticmethod
    def multiplierApply(stat_value: int, buff_value: int) -> int:
        return round(stat_value * buff_value)
