import pygame
import random
import json
import pprint

from src.game import Game
from src import mytime

H = mytime.Hour

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

    OPENING_HOURS_RANGES = (
        (
            (H("00 00"), H("00 00")),
            (H("24 00"), H("24 00"))
        ),
    )

    def __init__(self,
                 game: Game,
                 name: str):
        self.game = game

        # Nom du type d'endroit
        self.name = name

        # Image du type d'endroit
        self.images_directory = f'../assets/world/places/{name}/'

        # Horaires d'ouverture. Tuple : ((h1, h2), (h3, h4), ...). Est ouvert entre h1 et h2, entre h3 et h4, etc
        self.opening_hours = self.init_opening_hours()

    @property
    def is_open(self):
        for opening_hour, closing_hour in self.opening_hours:
            if self.game.time.hour.is_between(opening_hour, closing_hour):
                return True
        return False

    def init_opening_hours(self) -> tuple:

        opening_hour_tuple = ()

        for hours_range in self.OPENING_HOURS_RANGES:
            opening_hour_min, opening_hour_max = hours_range[0]
            closing_hour_min, closing_hour_max = hours_range[1]

            opening_hour = mytime.random_hour(opening_hour_min, opening_hour_max)
            closing_hour = mytime.random_hour(closing_hour_min, closing_hour_max)

            opening_hour = mytime.round_to_quarter(opening_hour)
            closing_hour = mytime.round_to_quarter(closing_hour)

            opening_hour_tuple += ((
                                       opening_hour,
                                       closing_hour
                                   ),)

        return opening_hour_tuple


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
    OPENING_HOURS_RANGES = (
        ((H("06 30"), H("08 00")), (H("20 00"), H("22 00"))),
    )

    def __init__(self,
                 game):
        super().__init__(game=game,
                         name='Food Shop')


class Tavern(Place):
    OPENING_HOURS_RANGES = (
        (
            (H("00 00"), H("00 00")),
            (H("24 00"), H("24 00"))
        ),
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='Tavern')


class Church(Place):
    OPENING_HOURS_RANGES = (
        (
            (H("09 00"), H("10 00")),
            (H("12 00"), H("12 00"))
        ),
        (
            (H("14 00"), H("15 00")),
            (H("17 00"), H("19 00"))
        )
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='Church')


class BlacksmithShop(Shop):
    OPENING_HOURS_RANGES = (
        ((H("06 00"), H("07 30")), (H("11 00"), H("12 00"))),
        ((H("12 30"), H("13 30")), (H("18 00"), H("18 00")))
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='Blacksmith Shop')


class TownHall(Place):
    OPENING_HOURS_RANGES = (
        ((H("10 00"), H("10 00")), (H("12 00"), H("12 00"))),
        ((H("14 00"), H("14 00")), (H("17 00"), H("17 00")))
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='TownHall')


class Arena(Place):
    OPENING_HOURS_RANGES = (
        ((H("17 00"), H("18 00")), (H("22 00"), H("24 00"))),
    )

    def __init__(self,
                 game):
        super().__init__(game=game,
                         name='Arena')


class MarketPlace(Place):
    OPENING_HOURS_RANGES = (
        ((H("06 30"), H("07 00")), (H("12 00"), H("13 00"))),
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='Market Place')


class ArmourerShop(Shop):
    OPENING_HOURS_RANGES = (
        ((H("09 00"), H("10 00")), (H("12 00"), H("13 00"))),
        ((H("13 00"), H("14 00")), (H("15 00"), H("17 00"))),
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='Armourer Shop')


class EnchantingShop(Shop):
    OPENING_HOURS_RANGES = (
        ((H("15 00"), H("16 00")), (H("00 00"), H("02 30"))),
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='Enchanting Shop')


class WeaponShop(Shop):
    OPENING_HOURS_RANGES = (
        ((H("09 00"), H("10 00")), (H("12 00"), H("13 00"))),
        ((H("13 00"), H("14 00")), (H("15 00"), H("17 00"))),
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='Weapon Shop')


class EquipmentShop(Shop):
    OPENING_HOURS_RANGES = (
        ((H("08 00"), H("10 00")), (H("11 00"), H("13 00"))),
        ((H("12 00"), H("14 00")), (H("17 00"), H("19 00"))),
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='Equipment Shop')


class Inn(Place):
    OPENING_HOURS_RANGES = (
        ((H("17 00"), H("18 00")), (H("10 00"), H("12 00"))),
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='Inn')


# TODO: Tavern (Taverne) X
#       Church (Eglise) X
#       TownHall (Hotel de ville) X
#       Arena (Arene) X
#       MarketPlace (Place du marché) X
#       FoodShop (Magasin : Nourriture) X
#       BlacksmithShop (Magasin : Forgeron) X
#       ArmourerShop (Magasin : Armurier) X
#       EnchantingShop (Magasin : Enchanteur) X
#       WeaponShop (Magasin : Vendeur d'armes) X
#       EquipmentShop (Magasin : Vendeur d'armures) X
#       Inn (Auberge) X


def get_district_places_type_pool(name: str) -> dict[str: dict]:
    """
    Returns the places types dict of the district.

    :param name: str
    :returns: dict[str: dict]
    """

    with open('districts.json', 'r') as file:
        return json.load(file)[name]['pool']


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
