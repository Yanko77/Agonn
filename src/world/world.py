"""
File managing the world map.
"""

import pygame

from dataclasses import dataclass
import time

import biomes
from src.config import MAP_SIZE


class Map:

    def __init__(self):
        self.size = MAP_SIZE

        t0, t1 = 0, 0
        t0 += time.perf_counter()
        self.biomes, _biomes_grid = biomes.init()  # Liste des objets Biomes de la carte.
        t1 += time.perf_counter()

        self.grid = self.init_grid(_biomes_grid)
        print(f"TEMPS BIOMES INIT: {t1 - t0}")

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    def get_tile(self, irow, icolumn):
        return self.grid[irow][icolumn]

    def init_grid(self, biomes_grid) -> list:
        """
        Initialize the map grid.
        """

        # Création de la grille
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

        for y, x in biomes_grid.keys():
            grid[y][x].biome = biomes_grid[(y, x)].biome

        return grid


@dataclass
class Tile:
    x: int
    y: int
    biome: biomes.Biome  # Objet Biome auquel il appartient
    place: str


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

    def set(self, place1: 'NamedPlace', place2: 'NamedPlace', distance: int, angle: int):
        place1.add_road(self)
        place2.add_road(self)

        self.places = (place1, place2)
        self.distance = distance
        self.angle = (angle, 180 - angle)


class RoadIntersection:

    def __init__(self):
        self.roads = ()  # Tuple des routes sortantes "officielles" de l'intersection


if __name__ == '__main__':

    t0 = time.perf_counter()
    m = Map()
    t1 = time.perf_counter()

    print(f"TEMPS TOTAL: {t1 - t0}")

    screen = pygame.display.set_mode((MAP_SIZE[0]*4, MAP_SIZE[1]*4))

    running = True
    while running:
        for row_i in range(MAP_SIZE[1]):
            for column_i in range(MAP_SIZE[0]):
                tile = m.get_tile(row_i, column_i)
                pygame.draw.rect(screen,
                                 tile.biome.color if tile.biome is not None else (0, 0, 0),
                                 pygame.Rect(column_i*4, row_i*4, 4, 4))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
