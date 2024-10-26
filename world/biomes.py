import random


class BiomeType:

    def __init__(self,
                 name: str,
                 crossing_cost: int,
                 spawning_chance: int,
                 color: tuple):
        self.name = name
        self.crossing_cost = crossing_cost  # Valeur représentant la difficulté du biome à être traversé.

        self.spawning_chance = spawning_chance
        self.spawning_pattern = ((0, 0,  0,  0, 0),
                                 (0, 0,  0,  0, 0),
                                 (0, 0, 100, 0, 0),
                                 (0, 0,  0,  0, 0),
                                 (0, 0,  0,  0, 0))
        self.spawning_spreading_chance = 100

        self.color = color

    def set_pattern(self, pattern: tuple):
        self.spawning_pattern = pattern


class Forest(BiomeType):

    def __init__(self):
        super().__init__(name='Forest',
                         crossing_cost=2,
                         spawning_chance=60,
                         color=(6, 137, 6))

        self.set_pattern(
            ((100, 80,  70,  80,  100),
             (80,  100, 100, 100, 80),
             (70,  100, 100, 100, 70),
             (80,  100, 100, 100, 80),
             (100, 80,  70,  80,  100))
        )


class Volcano(BiomeType):

    def __init__(self):
        super().__init__(name='Volcano',
                         crossing_cost=4,
                         spawning_chance=15,
                         color=(255, 81, 0))

        self.set_pattern(
            ((0,  0,   0,   0,  0),
             (0, 50,  100, 50,  0),
             (0, 100, 100, 100, 0),
             (0, 50,  100, 50,  0),
             (0,  0,   0,   0,  0))
        )


class Desert(BiomeType):

    def __init__(self):
        super().__init__(name='Desert',
                         crossing_cost=4,
                         spawning_chance=30,
                         color=(255, 220, 0))

        self.set_pattern(
            ((100, 60, 50, 60, 100),
             (60, 100, 100, 100, 60),
             (50, 100, 100, 100, 50),
             (60, 100, 100, 100, 60),
             (100, 60, 50, 60, 100))
        )


class Pond(BiomeType):

    def __init__(self):
        super().__init__(name='Pond',
                         crossing_cost=3,
                         spawning_chance=30,
                         color=(12, 72, 14))

        self.set_pattern(
            ((40,  0,   0,   0,  40),
             (0,  100, 100, 100, 0),
             (0,  100, 100, 100, 0),
             (0,  100, 100, 100, 0),
             (40,  0,   0,   0,  40))
        )


class Field(BiomeType):

    def __init__(self):
        super().__init__(name='Field',
                         crossing_cost=1,
                         spawning_chance=100,
                         color=(99, 210, 0))

        self.set_pattern(
            ((100, 100, 100, 100, 100),
             (100, 100, 100, 100, 100),
             (100, 100, 100, 100, 100),
             (100, 100, 100, 100, 100),
             (100, 100, 100, 100, 100))
        )


class Mountains(BiomeType):

    def __init__(self):
        super().__init__(name='Mountains',
                         crossing_cost=3,
                         spawning_chance=40,
                         color=(108, 108, 108))

        self.set_pattern(
            ((0,    0,   0,   0,   0),
             (0,    0,   0,   0,   0),
             (100, 100, 100, 100, 100),
             (0,    0,   0,   0,   0),
             (0,    0,   0,   0,   0))
        )


class Biome:
    """
    Objet qui représente un biome.
    Il possède un type (si c'est une foret, un étang, un désert, etc) et concerne une liste de tuiles.
    """

    def __init__(self,
                 biome_type: BiomeType):
        self.type = biome_type
        self.tiles_list = ()


def get_random_biome(weights_on: bool = True) -> BiomeType:
    if weights_on:
        return random.choices(
            population=TYPES,
            weights=[TYPES[i].spawning_chance for i in range(len(TYPES))],
            k=1
        )[0]
    else:
        return random.choice(TYPES)[0]


def spawn_biome(grid: list, biome: BiomeType, x: int, y: int) -> list:
    """
    Fait apparaitre le biome en fonction de son pattern de génération avec pour centre du pattern les coordonnées x, y.
    Renvoie la grille modifiée.
    """
    grid_copy = [grid[i].copy() for i in range(len(grid))]

    width = len(grid)
    height = len(grid[0])

    pattern = biome.spawning_pattern
    pattern_midpoint = (len(pattern) // 2, len(pattern[0]) // 2)
    for irow in range(len(pattern)):
        for icolumn in range(len(pattern[0])):
            tile_percent = pattern[irow][icolumn]

            grid_x = x - pattern_midpoint[1] + icolumn
            grid_y = y - pattern_midpoint[0] + irow

            if 0 <= grid_x < width and 0 <= grid_y < height:
                if tile_percent > 0:
                    grid_copy[grid_y][grid_x] = (biome, tile_percent)

    return grid_copy


TYPES = (Forest(), Volcano(), Desert(), Pond(), Field(), Mountains())