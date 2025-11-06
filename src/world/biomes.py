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
from typing import TYPE_CHECKING
import random
from enum import Enum

from src.tools.QuickSet import QuickSet

if TYPE_CHECKING:
    from .grid import GridTile


class Biome:

    def __init__(self,
                 type_: BiomeType,
                 tiles: QuickSet[GridTile]):
        self.type: BiomeType = type_
        self._tiles: QuickSet[GridTile] = tiles

    def getTiles(self) -> QuickSet[GridTile]:
        return self._tiles.copy()

    def addTile(self, tile: GridTile):
        self._tiles.add(tile)


class BiomeType:

    def __init__(self,
                 name: str,
                 crossing_cost: int,
                 spawning_chance: int,
                 color: tuple[int, int, int],
                 area_radius: int = 5):
        self.name = name
        self.crossing_cost = crossing_cost

        self.spawning_chance = spawning_chance
        self.color = color

        self.area_radius = area_radius
    

    def __eq__(self, other):
        return isinstance(other, BiomeType) and self.name == other.name
    
    def __repr__(self):
        return f"BiomeType({self.name})"
    

class BiomeTypes(Enum):
    """
    Enumerates all the existing BiomeType instances.
    """
    FOREST = BiomeType(name='Forest', crossing_cost=2, spawning_chance=60, color=(6, 137, 6))
    VOLCANO = BiomeType(name='Volcano', crossing_cost=4, spawning_chance=15, color=(255, 81, 0))
    DESERT = BiomeType(name='Desert', crossing_cost=4, spawning_chance=30, color=(255, 220, 0))
    POND = BiomeType(name='Pond', crossing_cost=3, spawning_chance=30, color=(12, 72, 14))
    FIELD = BiomeType(name='Field', crossing_cost=1, spawning_chance=100, color=(99, 210, 0))
    MOUNTAINS = BiomeType(name='Mountains', crossing_cost=3, spawning_chance=40, color=(108, 108, 108))
    WATER = BiomeType(name='Water', crossing_cost=5, spawning_chance=41, color=(0, 155, 255))

    @classmethod
    def list(cls) -> list[BiomeType]:
        return [e.value for e in cls]


def get_random_type(weights_on: bool = True) -> BiomeType:
    """
    Returns a random BiomeType instance.
    All existing BiomeType are in BiomeTypes.

    If `weights_on` is True, then it considers the spawning chances of each biome type.

    Parameters
    ----------
    weights_on: bool = True
        If it's True, then this function considers each BiomeType spawning chance
        in the random process.
    
    Returns
    -------
    BiomeType
        A random BiomeType.
    """
    biomes_types = BiomeTypes.list()

    weights = None
    if weights_on:
        weights = [biome_type.spawning_chance for biome_type in biomes_types]
    
    return random.choices(
        population=biomes_types,
        weights=weights,
        k=1
    )[0]