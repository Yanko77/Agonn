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

from .biomes import Biome
from src.tools.QuickSet import QuickSet


class Grid:

    def __init__(self, tiles_biome: dict[GridPos, Biome]):
        self._content: dict[GridPos, GridTile] = dict()
        self._init_content(tiles_biome)

    def _init_content(self, tiles_biome: dict[GridPos, Biome]):
        """
        Initializes tiles with the generated Biome in this grid content.
        It assumes that `tiles_biome.keys()` contains all this grid tiles positions.
        """
        for tile_pos in tiles_biome:
            tile_biome = tiles_biome[tile_pos]
            self._content[tile_pos] = GridTile(biome=tile_biome)

    def __contains__(self, pos: GridPos):
        """
        Returns True if `pos` is valid in this grid. False otherwise.
        """
        return pos in self._content.keys()

    def __getitem__(self, pos: GridPos) -> GridTile:
        """
        Returns the grid tile whose position are `pos`.
        Raises a ValueError if the position is not valid.
        """
        res = self._content.get(pos)

        if res is None:
            raise ValueError(f'The position is not valid : {pos}')
        return res


class GridPos:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @property
    def above(self) -> GridPos:
        return GridPos(self.x, self.y - 1)
    
    @property
    def below(self) -> GridPos:
        return GridPos(self.x, self.y + 1)
    
    @property
    def left(self) -> GridPos:
        return GridPos(self.x - 1, self.y)
    
    @property
    def right(self) -> GridPos:
        return GridPos(self.x + 1, self.y)
    
    def getNeighbors(self,
                     grid: Grid | QuickSet = None) -> QuickSet['GridPos']:
        """
        Returns the neighbors tiles positions.
        If `grid` is None, then if a neighbor is not in `grid`, then it doesn't appears in the result set.

        Returns
        -------
        QuickSet[GridPos]
        """
        set_ = QuickSet([self.above, self.below, self.left, self.right])

        if grid:
            return set_.filter(lambda el: el in grid)
        else:
            return set_
    
    def area_from_radius(self, grid: Grid | QuickSet, radius: int) -> QuickSet['GridPos']:
        """
        Return a set containing all the tile pos within a radius of `radius`.
        """
        res = QuickSet([])
        for x in range(self.x - radius, self.x + radius):
            for y in range(self.y - radius, self.y + radius):
                res.add(GridPos(x, y))
        
        return res.filter(lambda el: el in grid)

    def __eq__(self, other):
        return isinstance(other, GridPos) and self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __repr__(self):
        return f"GridPos({self.x}, {self.y})"
    

class GridTile:

    def __init__(self,
                 biome: Biome):
        self.biome: Biome = biome
