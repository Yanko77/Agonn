"""
Fichier qui gère la carte du monde avec :
- les Lieux-dits : Villes, Villages, Donjons
- les routes
- les biomes
"""

import random
from dataclasses import dataclass
from config import MAP_SIZE

# BIOMES
FOREST = Biome('Forêt', 2)
VOLCANO = Biome('Volcan', 4)
DESERT = Biome('Désert', 4)
POND = Biome('Étang', 3)
FIELD = Biome('Champs', 1)
MOUNTAINS = Biome('Montagnes', 3)

BIOMES = (FOREST, VOLCANO, DESERT, POND, FIELD, MOUNTAINS)  # Tous les biomes existants


class NamedPlace:

    def __init__(self,
                 name: str,
                 biome: Biome):
        self.name = name

        self.biome = biome

    def add_road(self, road):
        self.roads.append(road)


class Town(NamedPlace):

    def __init__(self,
                 name: str,
                 biome: Biome):
        super().__init__(name, biome)

        self.roads = []  # Liste des routes "officielles" sortantes


class Road:

    def __init__(self):
        self.places = ()   # Couple des 2 lieux reliés (uniquement 2, pour faire plus, créer un point d'intersection
                           # de Road)
        self.distance = 0  # Distance entre les 2 lieux. Impacte le cout en energie
        self.angle = ()    # L'angle à l'indice i du tuple correspond à l'angle entre places[i] et places[i-1]
        self.cost = 0      # Coût en energie de la traversée de la route. Valeur fixe, le coût réel dépendra d'autres
                           # facteurs
        self.biomes = ()   # Tuple de tuple des biomes traversés par la route avec leur proportion.
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


class Biome:

    def __init__(self,
                 name: str,
                 crossing_cost: int):
        self.name = name
        self.crossing_cost = crossing_cost  # Valeur représentant la difficulté du biome à être traversé.


class Map:

    def __init__(self):
        self.grid = [
            [
                Tile(x=column_i,
                     y=row_i,
                     biome=None,
                     place=None)
                for column_i in range(MAP_SIZE[0])
            ]
            for row_i in range(MAP_SIZE[1])
        ]


@dataclass
class Tile:
    x: int
    y: int
    biome: Biome
    place: NamedPlace
