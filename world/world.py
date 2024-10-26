"""
Fichier qui gère la carte du monde avec :
- les Lieux-dits : Villes, Villages, Donjons...
- les routes
- les biomes
"""

import pygame
import random

import biomes

from dataclasses import dataclass
from config import MAP_SIZE, NB_BIOMES
from colorama import Back
import time


class Map:

    def __init__(self):
        self.size = MAP_SIZE

        self.grid = self.init_grid()

        self.biomes = []  # Liste des objets Biomes de la carte.

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    def get_tile(self, irow, icolumn):
        return self.grid[irow][icolumn]

    def init_grid(self) -> list:
        """
        Initialise la grille de la carte.
        """
        grid = [
            [
                Tile(x=column_i,
                     y=row_i,
                     biome=None,
                     place=None)

                for column_i in range(self.width)
            ]

            for row_i in range(self.height)
        ]

        return grid

    def init_biomes(self):
        """
        Méthode qui génére aléatoirement des biomes sur la carte.
        """
        # Liste temporaire : De meme forme que self.grid mais chaque élément est un tuple (Biome, %tage)
        grid = [[(None, 0) for _ in range(MAP_SIZE[0])] for _ in range(MAP_SIZE[1])]

        for i in range(NB_BIOMES):
            # Choose BiomeType
            biome = biomes.get_random_biome()

            x = random.randint(0, MAP_SIZE[0] - 1)
            y = random.randint(0, MAP_SIZE[1] - 1)

            grid = biomes.spawn_biome(grid, biome, x, y)

        stop = False
        while not stop:
            grid_copy = [row.copy() for row in grid]

            stop = True
            for row_i in range(MAP_SIZE[1]):
                for column_i in range(MAP_SIZE[0]):

                    biome_type = grid[row_i][column_i][0]
                    capture_percent = grid[row_i][column_i][1]

                    if biome_type is not None:
                        # Haut
                        if row_i - 1 >= 0:
                            self.spread_biome(grid_copy, row_i - 1, column_i, biome_type, capture_percent)

                        # Bas
                        if row_i + 1 < MAP_SIZE[1]:
                            self.spread_biome(grid_copy, row_i + 1, column_i, biome_type, capture_percent)

                        # Gauche
                        if column_i - 1 >= 0:
                            self.spread_biome(grid_copy, row_i, column_i - 1, biome_type, capture_percent)

                        # Droite
                        if column_i + 1 < MAP_SIZE[0]:
                            self.spread_biome(grid_copy, row_i, column_i + 1, biome_type, capture_percent)

                        '''# Haut-Gauche
                        if row_i - 1 >= 0 and column_i - 1 >= 0:
                            self.spread_biome(grid_copy, row_i - 1, column_i - 1, biome_type, capture_percent/(2**(1/2)))

                        # Haut-Droite
                        if row_i - 1 >= 0 and column_i + 1 < MAP_SIZE[0]:
                            self.spread_biome(grid_copy, row_i - 1, column_i + 1, biome_type, capture_percent/(2**(1/2)))

                        # Bas-Gauche
                        if row_i + 1 < MAP_SIZE[1] and column_i - 1 >= 0:
                            self.spread_biome(grid_copy, row_i + 1, column_i - 1, biome_type, capture_percent/(2**(1/2)))

                        # Bas-Droite
                        if row_i + 1 < MAP_SIZE[1] and column_i + 1 < MAP_SIZE[0]:
                            self.spread_biome(grid_copy, row_i + 1, column_i + 1, biome_type, capture_percent/(2**(1/2)))'''

                    else:
                        stop = False

            grid = grid_copy

        for i_row in range(MAP_SIZE[1]):
            for i_column in range(MAP_SIZE[0]):
                self.grid[i_row][i_column].biome = grid[i_row][i_column][0]

    def spread_biome(self, grid: list, row_i: int, column_i: int, biome_type, chance: int):
        """
        Propage le biome à la case grid[row_i][column_i] avec une certaine probabilité.
        """
        tile = grid[row_i][column_i]

        if tile[0] is None:
            r_value = random.randint(1, 100)
            if r_value < chance:  # Spread réussi
                capture_value = random.randint(85, 100) * chance / 100
                grid[row_i][column_i] = (biome_type, capture_value)

        elif tile[0] == biome_type:
            grid[row_i][column_i] = (tile[0], tile[1] + round(chance * 10 / 100))

            if grid[row_i][column_i][1] > 100:
                grid[row_i][column_i] = (tile[0], 100)


@dataclass
class Tile:
    x: int
    y: int
    biome: biomes.Biome  # Objet Biome auquel il appartient
    place: str


class NamedPlace:

    def __init__(self,
                 name: str,
                 tile: Tile):
        self.name = name

        self.tile = tile  # Tuile sur laquelle le lieu-dit se situe.

    def add_road(self, road):
        self.roads.append(road)


class Town(NamedPlace):

    def __init__(self,
                 name: str,
                 biome: biomes.BiomeType):
        super().__init__(name, biome)

        self.roads = []  # Liste des routes "officielles" sortantes


class Road:

    def __init__(self):
        self.places = ()  # Couple des 2 lieux reliés (uniquement 2, pour faire plus, créer un point d'intersection
        # de Road)
        self.distance = 0  # Distance entre les 2 lieux. Impacte le cout en energie
        self.angle = ()  # L'angle à l'indice i du tuple correspond à l'angle entre places[i] et places[i-1]
        self.cost = 0  # Coût en energie de la traversée de la route. Valeur fixe, le coût réel dépendra d'autres
        # facteurs
        self.biomes = ()  # Tuple de tuple des biomes traversés par la route avec leur proportion.
        # Impacte le cout en energie

    def set(self, place1: NamedPlace, place2: NamedPlace, distance: int, angle: int):
        place1.add_road(self)
        place2.add_road(self)

        self.places = (place1, place2)
        self.distance = distance
        self.angle = (angle, 180 - angle)


class RoadIntersection:

    def __init__(self):
        self.roads = ()  # Tuple des routes sortantes "officielles" de l'intersection


if __name__ == '__main__':

    m = Map()
    t0 = time.perf_counter()
    m.init_biomes()
    t1 = time.perf_counter()

    print(t1 - t0)

    screen = pygame.display.set_mode((MAP_SIZE[0] * 4, MAP_SIZE[1] * 4))

    running = True
    while running:
        for row_i in range(MAP_SIZE[1]):
            for column_i in range(MAP_SIZE[0]):
                tile = m.get_tile(row_i, column_i)
                pygame.draw.rect(screen,
                                 tile.biome.color,
                                 pygame.Rect(4 * column_i, 4 * row_i, 4, 4))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

