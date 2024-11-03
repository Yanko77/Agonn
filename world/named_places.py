import pygame
import random

import biomes
from game import Game
import mytime

H = mytime.Hour


class NamedPlace:

    def __init__(self,
                 game: Game,
                 name: str,
                 tile):
        self.game = game

        self.name = name

        self.tile = tile  # Tuile sur laquelle le lieu-dit se situe.

        self.roads = []  # Liste des routes "officielles" sortantes

        self.size = 1  # Taille du lieu-dit. Valeur forcément impaire.

    def add_road(self, road):
        self.roads.append(road)


class Town(NamedPlace):

    def __init__(self,
                 game: Game,
                 name: str,
                 tile):

        super().__init__(game=game,
                         name=name,
                         tile=tile)

        self.districts = []  # Liste des quartiers de la ville : Centre-ville, Quartier commercial, Résidentiel


class DistrictType:
    def __init__(self,
                 game: Game,
                 name: str,
                 places_type_pool: list):
        self.game = game

        self.name = name

        # Liste de tous les types d'endroits qui peuvent être dans ce type de quartier
        self.places_type_pool = places_type_pool


class DownTown(DistrictType):

    def __init__(self, game: Game):
        super().__init__(game=game,
                         name='Downtown',
                         places_type_pool=[]  # TODO: Place du marché, Arène, Ecoles?, Boutiques, Hotel de ville, Eglise
                         )


class CommercialDistrict(DistrictType):
    def __init__(self, game: Game):
        super().__init__(game=game,
                         name='Commercial district',
                         places_type_pool=[]  # TODO : Boutiques (beaucoup)
                         )


class ResidentialDistrict(DistrictType):

    def __init__(self, game: Game):
        super().__init__(game=game,
                         name='Residential district',
                         places_type_pool=[]  # TODO :  Maisons, Tavernes, Auberges
                         )


class BadDisctrict(DistrictType):

    def __init__(self, game: Game):
        super().__init__(game=game,
                         name='Bad district',
                         places_type_pool=[]  # TODO : Boutiques marché noir, arènes illegales, tavernes malfamées
                         )


class District:
    """
    Classe représentant un quartier d'une ville
    """

    def __init__(self,
                 game: Game,
                 district_type: DistrictType,
                 sites: list):
        self.game = game

        self.type = district_type

        self.sites = sites

    def init_places(self):
        """
        Fonction qui initialise tous les lieux du quartier en leur déterminant un emplacement.
        """

        for site in self.sites:
            # liste de tous les types d'endroits qui peuvent être sur cet emplacement ET dans ce quartier
            site_pool = [place_type for place_type in self.type.places_pool if site.is_place_type_correct(place_type)]
            print(site_pool)

            # Choix aléatoire du type d'endroit qui spawn sur cet emplacement
            place_type = random.choice(site_pool)

            # On fait spawn l'endroit
            site.set_place(place_type())


class Site:
    """
    Classe représentant un emplacement de lieu d'un quartier / lieu-dit
    """
    def __init__(self,
                 game: Game,
                 place_types: tuple,
                 rect: pygame.Rect):
        self.game = game

        self._place_types = place_types

        self.rect = rect
        self.place = None

    def set_place(self, place):
        assert place.type in self._place_types

        self.place = place

    def is_place_type_correct(self, place_type):
        return place_type in self._place_types


class PlaceType:
    """
    Classe représentant le type d'un endroit.
    Exemple : Eglise est un type d'endroit. Il hérite donc des propriétés de PlaceType.
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


class ShopType(PlaceType):
    """
    Classe représentant le type d'une boutique (quelconque).
    """

    def __init__(self,
                 game,
                 name: str):
        super().__init__(game=game,
                         name=name)
        self.selling_items_pools = []  # TODO quand on aura la classe Item


class FoodShop(ShopType):

    OPENING_HOURS_RANGES = (
        ((H("06 30"), H("08 00")), (H("20 00"), H("22 00"))),
    )

    def __init__(self,
                 game):
        super().__init__(game=game,
                         name='Food Shop')


class Tavern(PlaceType):

    OPENING_HOURS_RANGES = (
        (
            (H("00 00"), H("00 00")),
            (H("24 00"), H("24 00"))
        ),
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='Tavern')


class Church(PlaceType):

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


class BlacksmithShop(ShopType):

    OPENING_HOURS_RANGES = (
        ((H("06 00"), H("07 30")), (H("11 00"), H("12 00"))),
        ((H("12 30"), H("13 30")), (H("18 00"), H("18 00")))
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='Blacksmith Shop')


class TownHall(PlaceType):

    OPENING_HOURS_RANGES = (
        ((H("10 00"), H("10 00")), (H("12 00"), H("12 00"))),
        ((H("14 00"), H("14 00")), (H("17 00"), H("17 00")))
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='TownHall')


class Arena(PlaceType):

    OPENING_HOURS_RANGES = (
        ((H("17 00"), H("18 00")), (H("22 00"), H("24 00"))),
    )

    def __init__(self,
                 game):
        super().__init__(game=game,
                         name='Arena')


class MarketPlace(PlaceType):

    OPENING_HOURS_RANGES = (
        ((H("06 30"), H("07 00")), (H("12 00"), H("13 00"))),
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='Market Place')


class ArmourerShop(ShopType):

    OPENING_HOURS_RANGES = (
        ((H("09 00"), H("10 00")), (H("12 00"), H("13 00"))),
        ((H("13 00"), H("14 00")), (H("15 00"), H("17 00"))),
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='Armourer Shop')


class EnchantingShop(ShopType):

    OPENING_HOURS_RANGES = (
        ((H("15 00"), H("16 00")), (H("00 00"), H("02 30"))),
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='Enchanting Shop')


class WeaponShop(ShopType):

    OPENING_HOURS_RANGES = (
        ((H("09 00"), H("10 00")), (H("12 00"), H("13 00"))),
        ((H("13 00"), H("14 00")), (H("15 00"), H("17 00"))),
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='Weapon Shop')


class EquipementShop(ShopType):

    OPENING_HOURS_RANGES = (
        ((H("08 00"), H("10 00")), (H("11 00"), H("13 00"))),
        ((H("12 00"), H("14 00")), (H("17 00"), H("19 00"))),
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='Equipement Shop')


class Inn(PlaceType):

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


if __name__ == '__main__':
    pass