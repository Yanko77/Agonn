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

        self.districts = list()  # Town districts list : Centre-ville, Quartier commercial, Résidentiel
        self.init_districts()

    def init_districts(self):
        """
        Initialize all the districts:
        - add them to ``self.districts``
        - initialize all their sites
        - initialize all their places
        """
        districts_infos = get_town_district_sites(self.name)

        for district_name in districts_infos:
            self.districts.append(
                globals()[district_name](game=self.game)
            )

        self._init_district_sites(districts_infos)

        self._init_district_places()

    def _init_district_sites(self, districts_infos) -> None:
        """
        Initialize the sites of all the districts.

        Effect: add the site list to each district
        """
        for district in self.districts:
            infos = districts_infos[district.__class__.__name__]['sites']
            for site_dict in infos:
                site_obj = Site(game=self.game,
                                place_types=[globals()[place_cls_name] for place_cls_name in site_dict["places_types"]],
                                rect=pygame.Rect(site_dict["rect"]))
                district.add_site(site_obj)

    def _init_district_places(self):
        """
        Initialize all the districts places
        """
        for district in self.districts:
            district.init_places()


class District:
    """
    Represents a town district.
    """

    def __init__(self,
                 game: Game,
                 name: str):
        self.game = game

        self.name = name

        self._places_type_pool = self.init_places_type_pool()

        self.sites = list()

    def add_site(self, site: 'Site'):
        self.sites.append(site)

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
        # Split the pool
        necessary_pool, other_pool = self._split_pools()

        # Sort the sites list (Necessary first)
        self.sites = sort_sites(self.sites, self._places_type_pool)

        for site in self.sites:

            # Try to put a necessary place
            nec_compatible_list = [placetype for placetype in necessary_pool if site.is_place_type_correct(placetype)]
            if nec_compatible_list:
                chosen_nec_place = random.choice(nec_compatible_list)

                necessary_pool.remove(chosen_nec_place)

                site.set_place(chosen_nec_place(self.game))

            # Else put another place
            else:
                other_compatible_list = {placetype: other_pool[placetype] for placetype in other_pool.keys()
                                         if site.is_place_type_correct(placetype)}

                chosen_other_place = random.choice(tuple(other_compatible_list.keys()))

                if other_compatible_list[chosen_other_place] == 1:
                    del other_compatible_list[chosen_other_place]
                elif other_compatible_list[chosen_other_place] != ANY:
                    other_compatible_list[chosen_other_place] -= 1

                site.set_place(chosen_other_place(self.game))

    def _split_pools(self) -> tuple[list['Place'], dict['Place', int]]:
        """
        Splits the places type pool into 2 different pools:
        - a necessary pool : it contains all necessary places. Those places will be placed first
        - another pool : it contains all the other places.

        :returns: tuple[list[dict], list[dict]]
        """

        pool = self._places_type_pool

        necessary_pool = list()
        other_pool = dict()

        for place in pool.keys():
            if NECESSARY in pool[place]['tags']:
                necessary_pool.append(place)

                if pool[place]['amount'] != ANY:
                    pool[place]['amount'] -= 1

            if pool[place]['amount'] > 0 or pool[place]['amount'] == ANY:
                other_pool[place] = pool[place]['amount']

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
        return f"Site({self.place.__class__.__name__}, {self.rect})"

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

    @property
    def place_types(self):
        return self._place_types


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
                 game: Game):
        super().__init__(game=game,
                         name='Downtown')


class CommercialDistrict(District):
    def __init__(self,
                 game: Game):
        super().__init__(game=game,
                         name='Commercial district')


class ResidentialDistrict(District):

    def __init__(self,
                 game: Game):
        super().__init__(game=game,
                         name='Residential district')


class BadDistrict(District):

    def __init__(self,
                 game: Game):
        super().__init__(game=game,
                         name='Bad district')


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


def get_town_district_sites(name: str) -> list[dict[str, list]]:
    """
    Returns the list of dict which contains the site infos.

    :returns: list[dict[str, list]]
    """
    with open('towns.json', 'r') as file:
        file_content = json.load(file)[name]

        return file_content


def get_place_hours(name: str) -> tuple[list[tuple[tuple[Hour]]], bool]:
    """
    Returns the place open hour ranges and the always open bool value of the place ``name``.

    :returns: tuple
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


def sort_place_by_sites_amount(type_pool: list[dict]):
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


def is_site_necessary(site: Site, district_pool_infos: dict[Place, dict]):
    """
    Returns True if ``site._places_types`` only contains necessary place types.
    """
    return all([NECESSARY in district_pool_infos[place_cls]['tags'] for place_cls in site.place_types])


def sort_sites(sites_list, district_pool_infos) -> list[Site]:
    """
    Sorts and returns the sites list:
    - the necessary sites first (``is_site_necessary(site) is True``)
    - Then the others
    """

    nec_part, other_part = [], []

    for site in sites_list:
        if is_site_necessary(site, district_pool_infos):
            nec_part.append(site)
        else:
            other_part.append(site)

    random.shuffle(nec_part)
    random.shuffle(other_part)

    return nec_part + other_part


TOWNS_NAME = ('Hanovre',)

if __name__ == '__main__':
    from tests.tests_named_places import exec_tests
    exec_tests()

    HANOVRE = Town(game='game',
                   name='Hanovre',
                   tile='')

    print(HANOVRE.name)
    print(HANOVRE.districts)
    downtown = HANOVRE.districts[0]

    print(downtown.sites)