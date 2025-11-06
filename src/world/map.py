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
import random

from src.tools.QuickSet import QuickSet
from .biomes import Biome, BiomeTypes, get_random_type
from .grid import Grid, GridPos
from src.tools.timeit import timeit


class Map:

    def __init__(self, 
                 size: tuple[int, int],
                 biome_amount_ratio: float):
        tiles_biome = self.generate(size, biome_amount_ratio)
        self.grid: Grid = Grid(tiles_biome)


    def generate(self,
                 size: tuple[int, int],
                 biome_amount_ratio: float
                 ) -> dict[GridPos, Biome]:
        """
        It generates this map so each tile belongs to a Biome.
        This generation is random and as natural as possible.

        The amount of generated biomes depends on the map size.
        The proportion is `biome_amount_ratio`.

        Algorithm
        ---------
        - 1. Spawn biomes roots on random tiles.
        - 2. Make those roots spread randomly to the neighbor tiles.
        - 3. Return a dict matching a tile position and the Biome it belongs to.

        Parameters
        ----------
        size: tuple[int, int]
            This map expected size :
            - size[0] is the number of columns
            - size[1] is the number of rows
        biome_amount_ratio: float
            It's a percentage representing the ratio between the amount of biomes and the
            number of tiles in the map.

            > Example: biome_amount_ratio = 20 and map_nb_tiles = 1000. 
            > Then this function will spawn 1000*0.2=20 biomes.

        Returns
        -------
        dict[GridPos, Biome]
            The dict matching each tile position in the grid with the Biome it belongs to.
        """
        # Amount of biomes to spawn
        nb_tiles = size[0] * size[1]
        nb_biomes = round(biome_amount_ratio / 100 * nb_tiles)

        # Biomes roots spawning
        biomes, gen_grid = self._spawnBiomes(nb_biomes, size)

        res = dict()
        for pos in gen_grid.keys():
            res[pos] = gen_grid[pos][0]

        # Biomes spreading
        neighbors = dict()
        for iCol in range(size[0]):
            for iRow in range(size[1]):
                pos = GridPos(iCol, iRow)
                neighs = pos.getNeighbors()
                neighs = [n for n in neighs if 0 <= n.x < size[0] and 0 <= n.y < size[1]]

                neighbors[pos] = QuickSet(neighs)

        gen_grid = self._spreadBiomes(gen_grid, neighbors, nb_tiles)

        res = dict()
        for pos in gen_grid.keys():
            res[pos] = gen_grid[pos][0]

        return res

    @timeit
    def _spawnBiomes(self, 
                        nb_biomes: int, 
                        size: tuple[int, int]) -> tuple[set[Biome], dict[GridPos, tuple[Biome, int]]]:
        """
        Spawns randomly `nb_biomes` biome roots through the map.

        Parameters
        ----------
        nb_biomes: int
            The amount of Biome instances to create
        size: tuple[int, int]
            This map expected size :
            - size[0] is the number of columns
            - size[1] is the number of rows

        Returns
        -------
        tuple
            The result tuple contains 2 elements:
            - set[Biome]
                - The set contains all the created Biome instances
            - dict[GridPos, tuple[Biome, int]]
                - The dictionnary matching a GridPos with the Biome instance it belongs to and its spreading value.
                The spreading value is by default 100 and is used in the spreading process. It represents the percentage
                of absorbtion of the Biome by the tile.
        
        Raises
        ------
        ValueError
            if `nb_biomes` is too big for the map size depending on `BiomeType.area_radius`.
        """
        # Check that nb_biomes value is not too big
        worst_area_radius = max([type_.area_radius for type_ in BiomeTypes.list()])
        if ((worst_area_radius*2+1)**2 * nb_biomes > size[0]*size[1]):
            raise ValueError(f"The amount of Biomes to spawn is too big for this map size:\n" \
                             f"nb_biomes={nb_biomes}, size={size}")


        all_biomes = tuple()
        gen_grid = dict()

        tiles_pool = QuickSet([GridPos(x, y) for x in range(size[0]) for y in range(size[1])])

        # Biomes spawning
        for _ in range(nb_biomes):
            # Pick random biome
            biome_type = get_random_type()

            # Pick random tile pos
            tile_pos: GridPos = tiles_pool.random_choice()

            # Add new biome to biomes list
            all_biomes += (biome_type,)

            # Remove all the tile pos in the radius defined by the biome type
            tiles_to_rm = tile_pos.area_from_radius(tiles_pool, biome_type.area_radius)
            for tile_to_rm in tiles_to_rm:
                tiles_pool.remove(tile_to_rm)

            # Spawn the biome on the tile
            gen_grid[tile_pos] = (biome_type, 100)

        return all_biomes, gen_grid

    def _spread(self, 
                pos: GridPos,
                gen_grid: dict[GridPos, tuple[Biome, int]],
                neighbors: QuickSet[GridPos]):
        """
        Tries to spread the biome of the tile at `pos` to all its neighbors.

        """
        neigh_to_rm = set()

        biome, spr = gen_grid[pos]
        for neigh_pos in neighbors:
            neigh = gen_grid.get(neigh_pos)

            if not neigh:
                if random.randint(1, 100) < spr:
                    neigh_spr = random.randint(8, 10) * spr // 10
                    gen_grid[neigh_pos] = (biome, neigh_spr)
            elif neigh[0] == biome and neigh[1] < 100:
                incr = round(spr / 10)
                neigh_spr = neigh[1] + incr
                if neigh_spr > 100:
                    neigh_spr = 100

                gen_grid[neigh_pos] = (biome, neigh_spr)
            else:
                neigh_to_rm.add(neigh_pos)
        
        # Remove useless neighbors
        for neigh_pos in neigh_to_rm:
            neighbors.remove(neigh_pos)

    def _spreadBiomesAux(self,
                         gen_grid: dict[GridPos, tuple[Biome, int]],
                         neighbors: dict[GridPos, QuickSet[GridPos]],
                         nb_tiles: int
                         ) -> dict[GridPos, tuple[Biome, int]]:
        if len(gen_grid.keys()) == nb_tiles:
            return gen_grid
        else:
            frozen_keys = set(gen_grid.keys())
            for pos in frozen_keys:
                self._spread(pos, gen_grid, neighbors[pos])
            
            return self._spreadBiomesAux(gen_grid, neighbors, nb_tiles)
    
    @timeit
    def _spreadBiomes(self,
                      gen_grid: dict[GridPos, tuple[Biome, int]],
                      neighbors: dict[GridPos, QuickSet[GridPos]],
                      nb_tiles: int
                      ) -> dict[GridPos, tuple[Biome, int]]:
        return self._spreadBiomesAux(gen_grid, neighbors, nb_tiles)

def main():
    import pygame

    # SCREEN/MAP has to be an integer
    MAP_WIDTH = 250
    MAP_HEIGHT = 250

    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 1000

    m = Map((MAP_WIDTH, MAP_HEIGHT), 0.5)
    g = m.grid

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    running = True
    while running:
        for iRow in range(MAP_HEIGHT):
            for iCol in range(MAP_WIDTH):
                try:
                    biome = g[GridPos(iCol, iRow)].biome
                except ValueError:
                    biome = None
                pygame.draw.rect(
                    screen,
                    biome.color if biome else (0, 0, 0),
                    pygame.Rect(SCREEN_WIDTH/MAP_WIDTH*iCol,
                                SCREEN_HEIGHT/MAP_HEIGHT*iRow,
                                SCREEN_WIDTH/MAP_WIDTH,
                                SCREEN_HEIGHT/MAP_HEIGHT)
                )
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
