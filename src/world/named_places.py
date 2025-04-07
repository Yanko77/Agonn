import pygame
import random

from src.game import Game
from src import mytime

H = mytime.Hour

# Tags pour les batiments du quartier
NECESSARY = -1  # Le lieu est nécessairement présent dans le quartier.
ANY = -2  # Le lieu n'a pas de nombre prédéfini d'exemplaires.


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
        self.roads.append(road)


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
                 places_type_pool: dict,
                 sites: list):
        self.game = game

        self.name = name

        self.places_type_pool = places_type_pool

        self.sites = sites

    def init_places(self):
        """
        Initialize all district places by determining their location (site).
        """
        # On mélange tous les emplacements.

        # On crée un dict de chaque type de lieu associé à tous les emplacements qui peuvent l'accueillir.
        # On ordonne :
        # -> En premier les lieux nécessaires, ensuite les autres
        # -> Pour les lieux necessaires : on ordonne par ordre croissant de nb d'emplacements
        # -> Pour les autres, on mélange.

        # Pour chaque lieu de cette liste, dans l'ordre, on lui choisit un emplacement s'il en reste.

        random.shuffle(self.sites)

        pool = self.places_type_pool

        necessary_pool = []
        other_pool = []
        for placetype in pool.keys():
            if NECESSARY in pool[placetype]['tags']:
                sites_list = [site for site in self.sites if site.is_place_type_correct(placetype)]
                random.shuffle(sites_list)

                necessary_pool.append({'type': placetype,
                                       'amount': 1,
                                       'sites': sites_list})
                pool[placetype]['amount'] -= 1

            if pool[placetype]['amount'] > 0 or pool[placetype]['amount'] == ANY:
                other_pool.append({'type': placetype,
                                   'amount': pool[placetype]['amount']})

        # Ordonner par ordre croissant de nb d'emplacements
        necessary_pool = sort_by_sites_amount(necessary_pool)

        # On choisit l'emplacement des lieux nécessaires
        for placetype in necessary_pool:
            bool_done = False
            i = 0
            while not bool_done and i < len(placetype['sites']):
                site = placetype['sites'][i]
                if site.is_empty:
                    site.set_place(placetype['type'](self.game))
                    bool_done = True
                else:
                    i += 1

        # On choisit pour les autres lieux
        # On crée une liste des emplacements vides
        empty_sites = [site for site in self.sites if site.is_empty]
        random.shuffle(empty_sites)

        for site in empty_sites:
            # Liste des lieux restants compatibles
            compatibles_places = [placetype for placetype in other_pool
                                  if site.is_place_type_correct(placetype['type']) and placetype['amount'] != 0]

            picked_place = random.choice(compatibles_places)
            site.set_place(picked_place['type'](self.game))

            for i in range(len(other_pool)):
                if other_pool[i]['type'] == picked_place and other_pool[i]['amount'] != ANY:
                    other_pool[i]['amount'] -= 1

                    if other_pool[i]['amount'] == 0:
                        other_pool.pop(i)


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

    @property
    def is_empty(self):
        return self.place is None

    def set_place(self, place):
        assert type(place) in self._place_types, f"{place} n'est pas dans la liste des types de l'emplacement"

        self.place = place

    def is_place_type_correct(self, place_type):
        return place_type in self._place_types


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
                         places_type_pool={
                             Arena: {'tags': (NECESSARY,),
                                     'amount': 1},

                             TownHall: {'tags': (NECESSARY,),
                                        'amount': 1},
                             Church: {'tags': (NECESSARY,),
                                      'amount': 1},
                             MarketPlace: {'tags': (NECESSARY,),
                                           'amount': 1},
                             FoodShop: {'tags': (),
                                        'amount': ANY},
                             BlacksmithShop: {'tags': (),
                                              'amount': ANY},
                             ArmourerShop: {'tags': (),
                                            'amount': ANY},
                             EnchantingShop: {'tags': (),
                                              'amount': ANY},
                             WeaponShop: {'tags': (),
                                          'amount': ANY},
                             EquipmentShop: {'tags': (),
                                             'amount': ANY},
                         },  # Place du marché, Arène, Ecoles?, Boutiques, Hotel de ville, Eglise
                         sites=sites
                         )


class CommercialDistrict(District):
    def __init__(self,
                 game: Game,
                 sites: list):
        super().__init__(game=game,
                         name='Commercial district',
                         places_type_pool={
                             FoodShop: {'tags': (),
                                        'amount': ANY},
                             BlacksmithShop: {'tags': (),
                                              'amount': ANY},
                             ArmourerShop: {'tags': (),
                                            'amount': ANY},
                             EnchantingShop: {'tags': (),
                                              'amount': ANY},
                             WeaponShop: {'tags': (),
                                          'amount': ANY},
                             EquipmentShop: {'tags': (),
                                             'amount': ANY},
                         },  # Boutiques (beaucoup)
                         sites=sites
                         )


class ResidentialDistrict(District):

    def __init__(self,
                 game: Game,
                 sites: list):
        super().__init__(game=game,
                         name='Residential district',
                         places_type_pool={
                             Tavern: {'tags': (NECESSARY,),
                                      'amount': 3},
                             Inn: {'tags': (NECESSARY,),
                                   'amount': 3}
                         },  # Maisons, Tavernes, Auberges
                         sites=sites
                         )


class BadDistrict(District):

    def __init__(self,
                 game: Game,
                 sites: list):
        super().__init__(game=game,
                         name='Bad district',
                         places_type_pool={

                         },  # TODO : Boutiques marché noir, arènes illegales, tavernes malfamées
                         sites=sites
                         )


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
    pass
