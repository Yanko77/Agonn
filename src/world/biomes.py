import random
from src import config


class BiomeType:
    """
    Represents a type of biome.

    It's defined  by:
    - name: str, its name ('forest' for example)
    - crossing_cost: int, a relative value representing how hard it is to cross this biome
    - spawning_chance: int, the rarety of the biome
    - color: tuple[int, int, int]
    """

    def __init__(self,
                 name: str,
                 crossing_cost: int,
                 spawning_chance: int,
                 color: tuple):
        self.name = name
        self.crossing_cost = crossing_cost  # Valeur représentant la difficulté du biome à être traversé.

        self.spawning_chance = spawning_chance
        self.spawning_pattern = ((0, 0, 0, 0,  0,  0, 0, 0, 0),
                                 (0, 0, 0, 0,  0,  0, 0, 0, 0),
                                 (0, 0, 0, 0,  0,  0, 0, 0, 0),
                                 (0, 0, 0, 0,  0,  0, 0, 0, 0),
                                 (0, 0, 0, 0, 100, 0, 0, 0, 0),
                                 (0, 0, 0, 0,  0,  0, 0, 0, 0),
                                 (0, 0, 0, 0,  0,  0, 0, 0, 0),
                                 (0, 0, 0, 0,  0,  0, 0, 0, 0),
                                 (0, 0, 0, 0,  0,  0, 0, 0, 0))
        self.spawning_spreading_chance = 100
        self.area_size = 5  # Area around the central point where no other biome is able to spawn.

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
            ((80, 60,  30,  20,  10,  20,  30, 60, 80),
             (60, 90,  70,  50,  30,  50,  70, 90, 60),
             (30, 70, 100,  80,  70,  80, 100, 70, 30),
             (20, 50,  80, 100, 100, 100,  80, 50, 20),
             (10, 30,  70, 100, 100, 100,  70, 30, 10),
             (20, 50,  80, 100, 100, 100,  80, 50, 20),
             (30, 70, 100,  80,  70,  80, 100, 70, 30),
             (60, 90,  70,  50,  30,  50,  70, 90, 60),
             (80, 60,  30,  20,  10,  20,  30, 60, 80))
        )
        self.area_size = 9


class Volcano(BiomeType):

    def __init__(self):
        super().__init__(name='Volcano',
                         crossing_cost=4,
                         spawning_chance=15,
                         color=(255, 81, 0))

        self.set_pattern(
            ((0, 0, 0,   0,   0,   0, 0, 0, 0),
             (0, 0, 0,   0,   0,   0, 0, 0, 0),
             (0, 0, 0,   0,   0,   0, 0, 0, 0),
             (0, 0, 0, 100,  50, 100, 0, 0, 0),
             (0, 0, 0,  50, 100,  50, 0, 0, 0),
             (0, 0, 0, 100,  50, 100, 0, 0, 0),
             (0, 0, 0,   0,   0,   0, 0, 0, 0),
             (0, 0, 0,   0,   0,   0, 0, 0, 0),
             (0, 0, 0,   0,   0,   0, 0, 0, 0))
        )
        self.area_size = 4


class Desert(BiomeType):

    def __init__(self):
        super().__init__(name='Desert',
                         crossing_cost=4,
                         spawning_chance=30,
                         color=(255, 220, 0))
        self.set_pattern(
            ((70, 35,  15,   5,   1,   5,  15, 35, 70),
             (35, 80,  80,  40,  10,  40,  80, 80, 35),
             (15, 80, 100,  60,  50,  60, 100, 80, 15),
             (5,  40,  60, 100, 100, 100,  60, 40,  5),
             (1,  10,  50, 100, 100, 100,  50, 10,  1),
             (5,  40,  60, 100, 100, 100,  60, 40,  5),
             (15, 80, 100,  60,  50,  60, 100, 80, 15),
             (35, 80,  80,  40,  10,  40,  80, 80, 35),
             (70, 35,  15,   5,   1,   5,  15, 35, 70))
            )
        self.area_size = 9


class Pond(BiomeType):  # Marais

    def __init__(self):
        super().__init__(name='Pond',
                         crossing_cost=3,
                         spawning_chance=30,
                         color=(12, 72, 14))

        self.set_pattern(

            ((0,   0,   0,   0,   0,   0,   0,   0,   0),
             (0,  20,  40,   0,   0,   0,  40,  20,   0),
             (0,  40,  40, 100, 100, 100,  40,  40,   0),
             (0,   0, 100, 100, 100, 100, 100,   0,   0),
             (0,   0, 100, 100, 100, 100, 100,   0,   0),
             (0,   0, 100, 100, 100, 100, 100,   0,   0),
             (0,  40,  40, 100, 100, 100,  40,  40,   0),
             (0,  20,  40,   0,   0,   0,  40,  20,   0),
             (0,   0,   0,   0,   0,   0,   0,   0,   0))
        )
        self.area_size = 8


class Field(BiomeType):

    def __init__(self):
        super().__init__(name='Field',
                         crossing_cost=1,
                         spawning_chance=100,
                         color=(99, 210, 0))

        self.set_pattern(
            (
                (0,    0,  100, 100, 100, 100, 100,   0,    0),
                (0,   100, 100, 100, 100, 100, 100,  100,   0),
                (100, 100, 100, 100, 100, 100, 100,  100, 100),
                (100, 100, 100, 100, 100, 100, 100,  100, 100),
                (100, 100, 100, 100, 100, 100, 100,  100, 100),
                (100, 100, 100, 100, 100, 100, 100,  100, 100),
                (100, 100, 100, 100, 100, 100, 100,  100, 100),
                (0,   100, 100, 100, 100, 100, 100,  100,   0),
                (0,    0,  100, 100, 100, 100, 100,   0,    0),

            )
        )

        self.area_size = 9


class Mountains(BiomeType):

    def __init__(self):
        super().__init__(name='Mountains',
                         crossing_cost=3,
                         spawning_chance=40,
                         color=(108, 108, 108))

        self.set_pattern(
            (
                (0,   0,   0,   0,   0,   0,   0,   0,   0),
                (0,   5,   5,   5,   5,   5,   5,   5,   0),
                (5,   50,  100, 100, 100, 100, 100, 50,  5),
                (50,  100, 100, 100, 100, 100, 100, 100, 50),
                (100, 100, 100, 100, 100, 100, 100, 100, 100),
                (50,  100, 100, 100, 100, 100, 100, 100, 50),
                (5,   50,  100, 100, 100, 100, 100, 50,  5),
                (0,   5,   5,   5,   5,   5,   5,   5,   0),
                (0,   0,   0,   0,   0,   0,   0,   0,   0),
            )
        )

        self.area_size = 9


class Water(BiomeType):
    def __init__(self):
        super().__init__(name='Water',
                         crossing_cost=5,
                         spawning_chance=41,
                         color=(0, 155, 255))
        self.set_pattern(
            ((100,  1,   0,   0,   0,   0,   0,   0,   0),
             (1,  100,   1,   0,   0,   0,   0,   0,   0),
             (0,    1, 100,   1,   0,   0,   0,   0,   0),
             (0,    0,   1, 100,  66,  33,   0,   0,   0),
             (0,    0,   0,  66, 100,  66,   0,   0,   0),
             (0,    0,   0,  33,  66, 100,   1,   0,   0),
             (0,    0,   0,   0,   0,   1, 100,   1,   0),
             (0,    0,   0,   0,   0,   0,   1, 100,   1),
             (0,    0,   0,   0,   0,   0,   0,   1, 100))
        )
        self.area_size = 9


class Biome:
    """
    Represents a biome.

    It's defined by:
    - biome_type: BiomeType, the biome type (forest, desert, pond, ...)

    It concerns a list of tiles.
    """

    def __init__(self,
                 biome_type: BiomeType):
        self.type = biome_type
        self.tiles_list = ()

        self.generator_tiles_pos_list = ()

    def add(self, tile):
        self.tiles_list += tile

    def add_generator(self, tile_pos: tuple):
        self.generator_tiles_pos_list += (tile_pos,)


def get_random_biome(weights_on: bool = True) -> Biome:
    """
    Returns a random Biome objects among TYPES.
    If 'weights_on' is True, considers the spawning chances of the biomes.

    :param weights_on: bool
    :returns : Biome
    """
    if weights_on:
        biome_type = random.choices(
            population=TYPES,
            weights=[TYPES[i].spawning_chance for i in range(len(TYPES))],
            k=1
        )[0]

    else:
        biome_type = random.choice(TYPES)[0]

    return Biome(biome_type)


def spawn(grid: list, biome: Biome, x: int, y: int) -> list:
    """
    Spawns the 'biome' on the tile 'grid[y][x]'.
    Does edit the grid.

    :param grid: list[list[Tile]]
    :param biome: Biome
    :param x: int
    :param y: int

    :returns : list[list[Tile]], the edited grid
    """

    width = len(grid[0])
    height = len(grid)

    # Pattern spawning
    pattern = biome.type.spawning_pattern
    pattern_midpoint = (len(pattern) // 2, len(pattern[0]) // 2)
    for irow in range(len(pattern)):
        for icolumn in range(len(pattern[0])):
            tile_percent = pattern[irow][icolumn]

            grid_x = x - pattern_midpoint[1] + icolumn
            grid_y = y - pattern_midpoint[0] + irow

            if _is_in_grid(grid, grid_x, grid_y):
                if tile_percent > 0:
                    grid[grid_y][grid_x] = (biome, tile_percent)
                    biome.add_generator((grid_y, grid_x))

    # Modification des chances d'apparition des autres biomes autour
    for i_row in range(-1 * biome.type.area_size, biome.type.area_size):
        for i_column in range(-1 * biome.type.area_size, biome.type.area_size):
            grid_x = x + i_column
            grid_y = y + i_row

            if _is_in_grid(grid, grid_x, grid_y):
                tile = grid[grid_y][grid_x]
                if tile[0] is None:
                    new_tile = (tile[0], 0)
                    grid[grid_y][grid_x] = new_tile


def spread(grid: list[list['Tile']], row_i: int, column_i: int, biome: Biome, chance: int) -> list:
    """
    Tries to spread the 'biome' to the tile 'grid[row_i][column_i]' with a probability of 'chance' to success.
    Returns the edited grid.

    :param grid: list[list[Tile]]
    :param row_i: int
    :param column_i: int
    :param biome: Biome, the Biome to spread
    :param chance: int, 0 <= chance <= 100

    :returns : list[list[Tile]]
    """

    tile_biome = grid[row_i][column_i][0]
    tile_spreading_value = grid[row_i][column_i][1]

    if tile_biome is None:
        r_value = random.randint(1, 100)
        if r_value < chance:  # Successful spread
            spreading_value = random.randint(80, 100) * chance / 100
            grid[row_i][column_i] = (biome, spreading_value)
            biome.add_generator((row_i, column_i))

    elif tile_biome == biome and tile_spreading_value < 100:
        tile_spreading_value += round(chance * 10 / 100)

        if tile_spreading_value > 100:
            tile_spreading_value = 100

        grid[row_i][column_i] = (
            tile_biome,
            tile_spreading_value
        )


def init() -> tuple:
    """
    Randomly generates biomes on the map.
    Returns all the Biomes objects generated like this.
    """
    all_biomes = ()
    grid = [[(None, 100) for _ in range(config.MAP_SIZE[0])] for _ in range(config.MAP_SIZE[1])]

    # Spawn des biomes
    for _ in range(config.NB_BIOMES):
        spawning_biome = get_random_biome()

        empty_tiles_pos = _get_empty_tiles_pos(grid)

        weights = [grid[row_i][column_i][1] for row_i, column_i in empty_tiles_pos]
        y, x = random.choices(empty_tiles_pos, weights)[0]

        spawn(grid, spawning_biome, x, y)
        all_biomes += (spawning_biome,)

    # Propagation des biomes
    stop = False
    while not stop:

        grid_copy = [row.copy() for row in grid]

        for biome in all_biomes:
            for row_i, column_i in biome.generator_tiles_pos_list:
                spreading_value = grid[row_i][column_i][1]

                # Haut
                if row_i - 1 >= 0:
                    spread(grid_copy, row_i - 1, column_i, biome, spreading_value)

                # Bas
                if row_i + 1 < len(grid):
                    spread(grid_copy, row_i + 1, column_i, biome, spreading_value)

                # Gauche
                if column_i - 1 >= 0:
                    spread(grid_copy, row_i, column_i - 1, biome, spreading_value)

                # Droite
                if column_i + 1 < len(grid[0]):
                    spread(grid_copy, row_i, column_i + 1, biome, spreading_value)

        grid = grid_copy

        # Vérification que les listes des biomes sont correctes
        tiles_counter = 0
        for biome in all_biomes:
            new_tuple = ()

            for i in range(len(biome.generator_tiles_pos_list)):
                y = biome.generator_tiles_pos_list[i][0]
                x = biome.generator_tiles_pos_list[i][1]

                if grid[y][x][0] == biome:
                    new_tuple += ((y, x),)
                    tiles_counter += 1

            biome.generator_tiles_pos_list = new_tuple

        if tiles_counter >= len(grid) * len(grid[0]):
            stop = True

    return all_biomes


def _get_empty_tiles_pos(grid: list[list['Tile']]) -> list[tuple[int, int]]:
    """
    Returns the list all the empty grid tiles locations.

    :param grid: list[list[Tile]]
    :returns : tuple[tuple[int, int]]
    """
    empty_tiles_pos_list = []

    for row_i in range(len(grid)):
        for column_i in range(len(grid[0])):
            if grid[row_i][column_i][0] is None:
                empty_tiles_pos_list.append((row_i, column_i))

    return empty_tiles_pos_list


def _is_in_grid(grid, x, y):
    """
    Returns True if gris[y][x] exists.
    Otherwise, returns False.

    :param grid: list[list[Tile]]
    :param x: int
    :param y: int
    """
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])


TYPES = (Forest(), Volcano(), Desert(), Pond(), Field(), Mountains(), Water())
