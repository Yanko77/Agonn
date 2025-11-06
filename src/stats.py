######################################################################
# Copyright 2025 (c) Yanko Lemoine
#
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
#
# SPDX-License-Identifier: EPL-2.0
######################################################################

from __future__ import annotations
from typing import Callable
import re
from copy import copy
import json

from .id import genId

JSON_FILE = "src/stats.json"

class Stat:
    """
    Represents a single stat.

    It's defined by its name and its formula.
    """

    def __init__(self, 
                 name: str,
                 formula: str = None):
        self.name = name
        
        """
        Example of formula :
        "10 + `charisma` * 2 + `dexterity`"
        This formula is valid if charisma and dexterity both exist.
        """
        if formula is None: 
            formula = "0"
        self.formula: str = formula

    
    def getRequiredRels(self) -> list[str]:
        """
        Returns the name of all the Stats required to evaluate this Stat value.
        """
        return list(map(
            lambda x: x.replace("`", ""),
            re.findall(r"`[a-zA-Z0-9_]*`", self.formula)))
    
    def getValue(self, rel_stats: dict[str, int]) -> int:
        """
        Returns this Stat value (before Buff application).

        Parameters
        ----------
        rel_stats: dict[str, int]
            A dict containing the values of all the Stat objects that are concerned by this evaluation.
            Example:
                If this Stat formula is : ```"10 + `charisma`"```.
                Then `other_stat` has to contain : `{"charisma": <value>}`
        
        Raises
        ------
        ValueError
            if `rel_stats` does not contain all needed Stat objects
        """

        formula = copy(self.formula)

        # Check that formula is evaluable: 
        # All the stat names used in the formula are in `rel_stats`
        for stat_name in self.getRequiredRels():
            if rel_stats.get(stat_name) is None:
                raise ValueError(f"The stat dict doesn't contain the required Stat objects : formula='{self.formula}', rel_stats={rel_stats}")

        # Replace with Stats value
        for stat_name in rel_stats.keys():
            stat_value = rel_stats[stat_name]
            formula = formula.replace(stat_name, str(stat_value))
        
        # Remove "`" characters
        formula = formula.replace("`", "")

        return eval(formula)
    
    def __repr__(self):
        return f"Stat<{self.name}, {self.formula}>"
    
    def __eq__(self, other):
        return isinstance(other, Stat) and (self.name, self.formula) == (other.name, other.formula)


class StatsManager:
    """
    Manages all the Stat object of an entity.
    """

    def __init__(self,
                 entity_name: str = None,
                 _json_file: str = JSON_FILE):
        """
        Builds a StatsManager.
        If `entity_name` is given, it loads the default stats from the json file.
        - If the given entity name is unknown, it builds an empty StatManager.
        """
        self._dict: dict[str, Stat] = {}
        self._buffs_dict: dict[str, list[StatBuff]] = {}
        
        self.rel_register = StatsRelRegister()

        if entity_name:
            try: self._init_from_entity(entity_name, _json_file)
            except ValueError: pass
    
    def _init_from_entity(self, entity_name: str, _file: str) -> None:
        """
        Init stats from a JSON file containing all the stats name for
        entity whose name is `entity_name`.
        By default the used json file path is `JSON_FILE`.
        Raises a ValueError if `entity_name` is unknown.
        """
        with open(_file, 'r') as file:
            data = json.loads(file.read())

        try:
            stats_dict = data[entity_name]
        except ValueError:
            raise ValueError(f'The entity is unknown : {entity_name}')

        for name in stats_dict.keys():
            self.addStat(Stat(name, stats_dict[name]))

    @property
    def list(self) -> list[Stat]:
        """
        Returns the list of all the Stat.
        Order isn't fixed.
        """
        return list(self._dict.values())
    
    @property
    def names_list(self) -> list[str]:
        """
        Returns the list of all the Stat names.
        Order isn't fixed.
        """
        return list(self._dict.keys())
    
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

        # Init an empty rel list for this new Stat
        self.rel_register.addStat(stat.name)

        # Add required rel depending on this new Stat formula
        _required_rels = stat.getRequiredRels()
        for rel_stat_name in _required_rels:
            self.rel_register.addRel(stat.name, rel_stat_name)


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
    
    def removeBuff(self, buff_id: int, stat_name: str):
        """
        Removes the StatBuff whose id is `buff_id` from the Stat whose name is `stat_name`.
        Raises ValueError is the buff id or the stat name is unknown.
        """
        buffs = self.getBuffList(stat_name)

        # Get selected buff index in the list
        i = 0
        while i < len(buffs) and buffs[i].id != buff_id:
            i += 1
        
        # Check that the buff exists
        if i == len(buffs):
            raise ValueError(f"Buff id is unknown : {buff_id}")
     
        buffs.pop(i)

        self.setBuffList(stat_name, buffs)

    
    def getValue(self, stat_name: str) -> int:
        """
        Returns the value of the contained stat whose name is `stat_name`.
        Raises a ValueError if it doesn't exist.
        """

        # Get value
        _stat = self.getObj(stat_name)
        _rel_values = self.getRelValues(stat_name)
        value = _stat.getValue(_rel_values)

        # Get buffs
        buffs_list = self.getBuffList(stat_name)

        # Apply buffs
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
    
    def getRelValues(self, stat_name: str) -> dict[str, int]:
        """
        Return the dict of the values of all the Stat that have a relationship
        with the stat whose name is `stat_name`.
        """
        rels = self.rel_register.getRelList(stat_name)
        res = {}
        for other_stat_name in rels:
            res[other_stat_name] = self.getValue(other_stat_name)
        
        return res
    
    def incrStat(self, stat_name: str, value: int) -> None:
        """
        Adds a flat bonus buff to the stat whose name is `stat_name`.
        The value of this buff is equal to `value`.
        Raises a ValueError if the stat name is unknown.
        """
        buff = StatBuff(StatBuffTypes.FLAT_BONUS, value)

        self.addBuff(buff, stat_name)


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
    
    
    def addStat(self, stat_name: str):
        """
        Adds a Stat to this register.
        It initializes an empty relationships set.
        """
        self._rel_dict[stat_name] = set()

    
    def addRel(self, stat_name1: str, stat_name2: str):
        """
        Adds a new relationship between the stats whose names are `stat_name1` and `stat_name2`.
        `stat_name2` appears in `stat_name1` Stat formula.
        """
        self._rel_dict[stat_name1].add(stat_name2)


class StatBuff:
    """
    Represents a Stat buff.

    A Buff can be temporary.
    Its effect is applied after the Stat value calculation.

    It's defined by:
    - StatBuffType, the type of the buff
    - float, its value
    - int, its priority value

    By default, the used priority value depends on the Buff type.
    """

    def __init__(self,
                 type_: StatBuffType,
                 value: float,
                 prio: int = None):
        self.type = type_
        self.value = value

        if prio is None:
            self.prio = self.type.prio
        else:
            self.prio = prio

        self.id = genId()
    
    def apply(self, value: int) -> int:
        """
        Applies this buff to the value `value`.
        Returns the result.
        """
        func = self.type.getFunc()
        return func(value, self.value)

    def __eq__(self, other):
        return isinstance(other, StatBuff) and self.type == other.type and self.value == other.value and self.prio == other.prio

class StatBuffType:
    """
    Represents a stat buff type.
    """

    def __init__(self,
                 default_prio: int,
                 apply_func: Callable[[int, int], int]
                 ):
        self.prio = default_prio
        self._func = apply_func

    def getFunc(self) -> Callable[[int, int], int]:
        """
        Returns the function to use to apply the buff on a value.
        """
        return self._func
    
    @staticmethod
    def flatBonusApply(stat_value: int, buff_value: int) -> int:
        return round(stat_value + buff_value)
    
    @staticmethod
    def multiplierApply(stat_value: int, buff_value: int) -> int:
        return round(stat_value * buff_value)

class StatBuffTypes:
    """
    Enumerates all the existing StatBuff types
    """
    FLAT_BONUS = StatBuffType(0, StatBuffType.flatBonusApply)
    MULTIPLIER = StatBuffType(10, StatBuffType.multiplierApply)
