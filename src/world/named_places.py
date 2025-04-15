import pygame
import random
import json

from src.game import Game
from src.mytime import Hour

NECESSARY = -1
ANY = -2


class NamedPlace:
    """
    Represents a named place.

    It's defined by:
    - game
    - name, the place name
    - tile: Tile, where the place is located
    """

    def __init__(self,
                 game: Game,
                 name: str,
                 tile):
        self.game = game

        self.name = name
        self.tile = tile
        self.roads = set()  # officials roads set
        self.size = 1  # place size. (has to be odd)

    def add_road(self, road):
        """
        Adds a leaving road to the place.

        :param road: Road
        """
        self.roads.add(road)


class Town(NamedPlace):
    """
    Represents a town.

    A Town object is a type of NamedPlace.
    It's defined by:
    - game
    - name: str, the town name
    - tile: Tile, where the town is located
    """

    def __init__(self,
                 game: Game,
                 name: str,
                 tile):
        super().__init__(game=game,
                         name=name,
                         tile=tile)

        self.districts = set()  # Town districts list : Centre-ville, Quartier commercial, Résidentiel


class District:
    """
    Represents a town district.
    """

    def __init__(self,
                 game: Game,
                 name: str,
                 sites: list):
        self.game = game

        self.name = name

        self._places_type_pool = self.init_places_type_pool()

        self.sites = sites

    def init_places_type_pool(self) -> dict['Place', dict]:
        """
        Returns the places type pool of the district.
        The place type pool infos are written in 'districts.json' file.
        """
        res = dict()

        pool_dict = get_district_places_type_pool(self.name)

        for class_name in pool_dict.keys():
            class_ = globals()[class_name]

            res[class_] = pool_dict[class_name]

        return res

    def init_places(self):
        """
        Initialize all district places by determining their location (site).
        """

        # Shuffle all the sites
        random.shuffle(self.sites)

        # Split the pool
        necessary_pool, other_pool = self._split_pools()

        # Sort the necessary pool by available sites amount
        necessary_pool = sort_by_sites_amount(necessary_pool)

        # Choose the location of the necessary
        for place_infos in necessary_pool:
            place = place_infos['type'](self.game)
            sites = place_infos['sites']

            for site in sites:
                if site.is_empty:
                    site.set_place(place)
                    break

        # Choose the location of the other
        empty_sites = [site for site in self.sites if site.is_empty]

        for site in empty_sites:
            compatibles_places = [placetype for placetype in other_pool
                                  if site.is_place_type_correct(placetype['type']) and placetype['amount'] != 0]

            picked_place = random.choice(compatibles_places)
            site.set_place(picked_place['type'](self.game))

            if picked_place['amount'] != ANY:
                picked_place['amount'] -= 1

    def _split_pools(self) -> tuple[list[dict], list[dict]]:
        """
        Splits the places type pool into 2 different pools:
        - a necessary pool : it contains all necessary places. Those places will be placed first
        - another pool : it contains all the other places.

        :returns: tuple[list[dict], list[dict]]
        """
        pool = self._places_type_pool

        necessary_pool = list()
        other_pool = list()

        for place in pool.keys():
            if NECESSARY in pool[place]['tags']:
                necessary_pool.append({'type': place,
                                       'sites': [site for site in self.sites if site.is_place_type_correct(place)]})

                pool[place]['amount'] -= 1

            if pool[place]['amount'] > 0 or pool[place]['amount'] == ANY:
                other_pool.append({'type': place,
                                   'amount': pool[place]['amount']})

        return necessary_pool, other_pool


class Site:
    """
    Represents a site of a district or a named place
    """

    def __init__(self,
                 game: Game,
                 place_types: tuple,
                 rect: pygame.Rect):
        self.game = game

        self._place_types = place_types

        self.rect = rect
        self.place = None

    def __repr__(self):
        return f"Site({self.place.__class__.__name__})"

    @property
    def is_empty(self):
        return self.place is None

    def set_place(self, place):
        assert type(place) in self._place_types, f"{place} isn't in the list of types of this site"

        self.place = place

    def is_place_type_correct(self, place: object) -> bool:
        """
        Returns True if the place can be placed on this site.

        :param place: Place class
        :returns: bool
        """
        return place in self._place_types


class Place:
    """
    Represents a town place.

    All place types inherit from
    """

    def __init__(self,
                 game: Game,
                 name: str):
        self.game = game

        self.name = name

        self.images_directory = f'../assets/world/places/{name}/'

        _open_hours_infos = get_place_hours(self.name)
        self.open_hrs = _open_hours_infos[0]
        self.is_always_open = _open_hours_infos[1]


class Shop(Place):
    """
    Represents a shop place.
    All the shops inherit this class
    """

    def __init__(self,
                 game,
                 name: str):
        super().__init__(game=game,
                         name=name)
        self.selling_items_pools = []  # TODO quand on aura la classe Item


class DownTown(District):

    def __init__(self,
                 game: Game,
                 sites: list):
        super().__init__(game=game,
                         name='Downtown',
                         sites=sites)


class CommercialDistrict(District):
    def __init__(self,
                 game: Game,
                 sites: list):
        super().__init__(game=game,
                         name='Commercial district',
                         sites=sites)


class ResidentialDistrict(District):

    def __init__(self,
                 game: Game,
                 sites: list):
        super().__init__(game=game,
                         name='Residential district',
                         sites=sites)


class BadDistrict(District):

    def __init__(self,
                 game: Game,
                 sites: list):
        super().__init__(game=game,
                         name='Bad district',
                         sites=sites)


class FoodShop(Shop):

    def __init__(self,
                 game):
        super().__init__(game=game,
                         name='Food Shop')


class Tavern(Place):

    def __init__(self, game):
        super().__init__(game=game,
                         name='Tavern')


class Church(Place):

    def __init__(self, game):
        super().__init__(game=game,
                         name='Church')


class BlacksmithShop(Shop):
    def __init__(self, game):
        super().__init__(game=game,
                         name='Blacksmith Shop')


class TownHall(Place):

    def __init__(self, game):
        super().__init__(game=game,
                         name='TownHall')


class Arena(Place):
    def __init__(self,
                 game):
        super().__init__(game=game,
                         name='Arena')


class MarketPlace(Place):

    def __init__(self, game):
        super().__init__(game=game,
                         name='Market Place')


class ArmourerShop(Shop):

    def __init__(self, game):
        super().__init__(game=game,
                         name='Armourer Shop')


class EnchantingShop(Shop):

    def __init__(self, game):
        super().__init__(game=game,
                         name='Enchanting Shop')


class WeaponShop(Shop):

    def __init__(self, game):
        super().__init__(game=game,
                         name='Weapon Shop')


class EquipmentShop(Shop):

    def __init__(self, game):
        super().__init__(game=game,
                         name='Equipment Shop')


class Inn(Place):

    def __init__(self, game):
        super().__init__(game=game,
                         name='Inn')


def get_district_places_type_pool(name: str) -> dict[str: dict]:
    """
    Returns the places types dict of the district.

    :param name: str
    :returns: dict[str: dict]
    """

    with open('districts.json', 'r') as file:
        return json.load(file)[name]['pool']


def get_place_hours(name: str) -> tuple[list[tuple[tuple[Hour]]], bool]:
    """
    Returns the place open hour ranges and the always open bool value of the place ``name``.

    :return: tuple
    """

    with open('places.json', 'r') as file:
        file_content = json.load(file)[name]

        # Always open bool
        bool_always_open = file_content['always_open']

        # Hours range
        if bool_always_open:
            hrs_range_list = None
        else:

            hrs_dicts_list = file_content['hrs']

            hrs_range_list = []
            for hrs_dict in hrs_dicts_list:

                words = ('open', 'close')

                open_range = tuple()
                for w in words:
                    if type(hrs_dict[w]) is list:
                        open_range += (tuple(Hour(h) for h in hrs_dict[w]),)
                    else:
                        open_range += (Hour(hrs_dict[w]),)

                hrs_range_list.append(open_range)

        return hrs_range_list, bool_always_open


def sort_by_sites_amount(type_pool: list[dict]):
    """
    Sorts the place type list by amount of sites (ascending order)
    """

    new_list = []
    while len(type_pool) > 0:
        mini_i = 0
        for i in range(len(type_pool) - 1):
            if len(type_pool[i + 1]['sites']) < len(type_pool[mini_i]['sites']):
                mini_i = i + 1
        new_list.append(type_pool[mini_i])
        type_pool.pop(mini_i)

    return new_list


if __name__ == '__main__':
    from tests.tests_named_places import exec_tests
    exec_tests()
