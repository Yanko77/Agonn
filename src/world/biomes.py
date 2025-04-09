import random
import time

import src.config as config


class _Set:
    """
    This class is a ``set`` implementation of which it's possible to get a random element, remove an element
    and do ``.__countains__()`` with a complexity of O(1).
    """
    def __init__(self, data: list):
        self.data = data
        self.data_map = {self.data[i]: i for i in range(len(self.data))}

    def remove(self, item):
        """
        Remove ``item`` from self.

        Complexity : O(1)
        """
        # Get the last element and the index of the item to remove
        last = self.data[-1]
        index = self.data_map[item]

        # Swap the item to remove and the last
        self.data[index] = last
        self.data[-1] = item

        # Update data_map
        self.data_map[last] = index

        # Pop the last
        self.data.pop()
        # Pop item from data_map. ( O(1) )
        self.data_map.pop(item)

    def random_choice(self):
        """
        Returns a random element from self.

        Complexity : O(1)
        """
        return random.choice(self.data)

    def __contains__(self, item):
        """
        Returns True if ``item`` is in self.

        Complexity : O(1)
        """
        return item in self.data_map

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        for item in self.data:
            yield item


class _GridTile:
    """
    Represents a tile of the biome generation grid.
    """

    def __init__(self, pos, biome, spr):
        self.y, self.x = pos
        self.biome = biome
        self.spr = spr

        self.neighbors = self.init_neighbors()

    def init_neighbors(self):
        """
        Returns the neighbors pos list.
        """
        _neighbors = {(self.y-1, self.x),
                      (self.y+1, self.x),
                      (self.y, self.x-1),
                      (self.y, self.x+1)}
        return _Set([neigh for neigh in _neighbors if _is_in(neigh[1], neigh[0], config.MAP_SIZE)])

    def spread(self, grid):
        """
        Tries to spread its biome to its neighbors.

        If a neighbor does have its attribute ``spr`` up to 100, removes this neighbor from ``self.neighbors``
        """

        _to_remove = set()
        for neigh_pos in self.neighbors:
            neigh = grid.get(neigh_pos, None)

            if neigh is None:
                if random.randint(1, 100) < self.spr:
                    spr_value = random.randint(8, 10) * self.spr // 10
                    grid[neigh_pos] = _GridTile(neigh_pos, self.biome, spr_value)

            elif neigh.biome == self.biome and neigh.spr < 100:
                incr = round(self.spr / 10)
                neigh.incr_spr(incr)

            elif neigh.spr == 100:
                _to_remove.add(neigh_pos)

        for neigh_pos in _to_remove:
            self.neighbors.remove(neigh_pos)

    def incr_spr(self, incr):
        self.spr += incr
        if self.spr > 100:
            self.spr = 100


class Biome:
    """
    Represents a biome.
    """

    def __init__(self,
                 name: str,
                 crossing_cost: int,
                 spawning_chance: int,
                 color: tuple[int, int, int],
                 area_size: int = 5):
        self.name = name
        self.crossing_cost = crossing_cost

        self.spawning_chance = spawning_chance
        self.color = color

        self.area_size = area_size

        self.tiles_list = ()

    def __eq__(self, other):
        return self.name == other.name


def get_random_biome(weights_on: bool = True) -> Biome:
    """
    Returns a random ``Biome`` objects among ``TYPES``.
    If ``weights_on`` is True, considers the spawning chances of the biomes.

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

    return biome_type


def spawn(grid: dict, biome: Biome, x: int, y: int):
    """
    Spawns the ``biome`` on the tile (y, x) of the grid.
    Does edit the grid.

    :param grid: set
    :param biome: Biome
    :param x: int
    :param y: int
    """
    grid[(y, x)] = _GridTile((y, x), biome, 100)


def spawn_all_biomes() -> tuple[tuple, dict[tuple[int, int], _GridTile]]:
    """
    Spawns all biomes on a map.
    Returns the biomes list and the generated grid.

    The complexity of this algo is excellent.

    :returns: tuple[tuple, dict[tuple[int, int], tuple[Biome, int]]], the biomes list and the grid.
        The grid is a dict that countains all the not empty tiles.
    """
    all_biomes = ()
    grid = dict()

    # Biomes spawning
    tiles_pool = _Set([(y, x) for x in range(config.MAP_SIZE[1]) for y in range(config.MAP_SIZE[0])])

    for _ in range(config.NB_BIOMES):
        biome = get_random_biome()

        # Get the random tile
        tile_pos = tiles_pool.random_choice()

        # Spawn the biome
        spawn(grid, biome, tile_pos[1], tile_pos[0])

        # Add it to the biome list
        all_biomes += (biome,)

        # Remove from the pool
        tiles_pool.remove(tile_pos)

        # Remove the tiles in the area from the pool
        for y in range(-biome.area_size, biome.area_size):
            for x in range(-biome.area_size, biome.area_size):
                grid_y, grid_x = tile_pos[0] + y, tile_pos[1] + x

                if (grid_y, grid_x) in tiles_pool:
                    tiles_pool.remove((grid_y, grid_x))

    return all_biomes, grid


def spread_all_biomes(grid):
    """
    grid example:
    {
        (1, 1): (FOREST, 100),
        ...
    }
    """
    t1, t0 = 0, 0

    stop = False
    while not stop:
        grid_copy = grid.copy()

        for tile_pos in grid_copy.keys():

            t0 += time.perf_counter()
            grid[tile_pos].spread(grid)
            t1 += time.perf_counter()

        if len(grid) >= config.MAP_SIZE[0] * config.MAP_SIZE[1]:
            stop = True

    print(f'TEMPS SPREAD : {t1 - t0}')


def init() -> tuple:
    """
    Randomly generates biomes on the map.
    Returns the map grid.
    """

    t0 = time.perf_counter()
    all_biomes, grid = spawn_all_biomes()
    t1 = time.perf_counter()

    print(f"TEMPS SPAWN : {t1 - t0}")

    # Biome spreading
    spread_all_biomes(grid)

    return all_biomes, grid


def _is_in(x: int, y: int, size: tuple[int, int]) -> bool:
    """
    Returns True if the tile (y, x) exists in a grid with a size of 'size'.
    Otherwise, returns False.

    :param x: int
    :param y: int
    :param size: tuple[int, int]
    :returns: bool
    """
    return 0 <= y < size[0] and 0 <= x < size[1]


FOREST = Biome(name='Forest', crossing_cost=2, spawning_chance=60, color=(6, 137, 6))
VOLCANO = Biome(name='Volcano', crossing_cost=4, spawning_chance=15, color=(255, 81, 0))
DESERT = Biome(name='Desert', crossing_cost=4, spawning_chance=30, color=(255, 220, 0))
POND = Biome(name='Pond', crossing_cost=3, spawning_chance=30, color=(12, 72, 14))
FIELD = Biome(name='Field', crossing_cost=1, spawning_chance=100, color=(99, 210, 0))
MOUNTAINS = Biome(name='Mountains', crossing_cost=3, spawning_chance=40, color=(108, 108, 108))
WATER = Biome(name='Water', crossing_cost=5, spawning_chance=41, color=(0, 155, 255))

TYPES = (FOREST, VOLCANO, DESERT, POND, FIELD, MOUNTAINS, WATER)
