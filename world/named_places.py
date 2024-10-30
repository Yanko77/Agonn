import pygame
import random

import biomes


class NamedPlace:

    def __init__(self,
                 game,
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
                 game,
                 name: str,
                 tile):

        super().__init__(game=game,
                         name=name,
                         tile=tile)

        self.districts = []  # Liste des quartiers de la ville : Centre-ville, Quartier commercial, Résidentiel


class DistrictType:
    def __init__(self,
                 game,
                 name: str,
                 places_type_pool: list):
        self.game = game

        self.name = name

        # Liste de tous les types d'endroits qui peuvent être dans ce type de quartier
        self.places_type_pool = places_type_pool


class DownTown(DistrictType):

    def __init__(self):
        super().__init__(game=game,
                         name='Downtown',
                         places_type_pool=[]  # TODO: Place du marché, Arène, Ecoles?, Boutiques, Hotel de ville, Eglise
                         )


class CommercialDistrict(DistrictType):
    def __init__(self):
        super().__init__(game=game,
                         name='Commercial district',
                         places_type_pool=[]  # TODO : Boutiques (beaucoup)
                         )


class ResidentialDistrict(DistrictType):

    def __init__(self):
        super().__init__(game=game,
                         name='Residential district',
                         places_type_pool=[]  # TODO :  Maisons, Tavernes, Auberges
                         )


class BadDisctrict(DistrictType):

    def __init__(self):
        super().__init__(game=game,
                         name='Bad district',
                         places_type_pool=[]  # TODO : Boutiques marché noir, arènes illegales, tavernes malfamées
                         )


class District:
    """
    Classe représentant un quartier d'une ville
    """

    def __init__(self,
                 game,
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
                 game,
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
        ((0, 0), (24, 24)),
    )

    def __init__(self,
                 game,
                 name: str):
        self.game = game

        # Nom du type d'endroit
        self.name = name

        # Image du type d'endroit
        self.images_directory = f'../assets/world/places/{name}/'

        # Horaires d'ouverture. Tuple : ((x1, x2), (x3, x4), ...). Est ouvert entre x1 et x2, entre x3 et x4, etc
        self.opening_hours = self.init_opening_hours()

    @property
    def is_open(self):
        for open_h, close_h in self.opening_hours:
            if open_h <= self.game.time.get() <= close_h:
                return True
        return False

    def init_opening_hours(self) -> tuple:
        opening_hours = ()

        for hours_range in self.OPENING_HOURS_RANGES:
            open_min, open_max = hours_range[0]
            close_min, close_max = hours_range[1]

            opening_hours += ((
                random.randint(open_min, open_max),
                random.randint(close_min, close_max)
            ))

        return opening_hours


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
        ((6, 8), (20, 22)),
    )

    def __init__(self,
                 game):
        super().__init__(game=game,
                         name='Food Shop')


class Tavern(PlaceType):

    OPENING_HOURS_RANGES = (
        ((0, 0), (24, 24))
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='Tavern')


class Church(PlaceType):

    OPENING_HOURS_RANGES = (
        ((9, 10), (12, 12)),
        ((14, 15), (17, 19))
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='Church')


class BlacksmithShop(ShopType):

    OPENING_HOURS_RANGES = (
        ((6, 8), (11, 12)),
        ((12, 13), (18, 18))
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='Blacksmith Shop')


class TownHall(PlaceType):

    OPENING_HOURS_RANGES = (
        ((10, 10), (12, 12)),
        ((14, 14), (17, 17))
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='TownHall')


class Arena(PlaceType):

    OPENING_HOURS_RANGES = (
        ((17, 18), (22, 24)),
    )

    def __init__(self,
                 game):
        super().__init__(game=game,
                         name='Arena')


class MarketPlace(PlaceType):

    OPENING_HOURS_RANGES = (
        ((7, 9), (12, 13)),
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='Market Place')


class ArmourerShop(ShopType):

    OPENING_HOURS_RANGES = (
        ((9, 10), (12, 13)),
        ((13, 14), (15, 17))
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='Armourer Shop')


class EnchantingShop(ShopType):

    OPENING_HOURS_RANGES = (
        ((15, 16), (23, 24)),
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='Enchanting Shop')


class WeaponShop(ShopType):

    OPENING_HOURS_RANGES = (
        ((9, 10), (12, 13)),
        ((13, 14), (15, 17))
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='Weapon Shop')


class EquipementShop(ShopType):

    OPENING_HOURS_RANGES = (
        ((8, 10), (11, 13)),
        ((12, 14), (17, 19))
    )

    def __init__(self, game):
        super().__init__(game=game,
                         name='Equipement Shop')


class Inn(PlaceType):
    OPENING_HOURS_RANGES = (
        ((0, 0), (10, 12)),
        ((17, 18), (24, 24))
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
