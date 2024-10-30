import pygame
import random

import biomes


class NamedPlace:

    def __init__(self,
                 name: str,
                 tile):
        self.name = name

        self.tile = tile  # Tuile sur laquelle le lieu-dit se situe.

        self.roads = []  # Liste des routes "officielles" sortantes

        self.size = 1  # Taille du lieu-dit. Valeur forcément impaire.

    def add_road(self, road):
        self.roads.append(road)


class Town(NamedPlace):

    def __init__(self,
                 name: str,
                 biome: biomes.BiomeType):
        super().__init__(name, biome)

        self.districts = []  # Liste des quartiers de la ville : Centre-ville, Quartier commercial, Résidentiel


class DistrictType:
    def __init__(self,
                 name: str,
                 places_type_pool: list):
        self.name = name

        # Liste de tous les types d'endroits qui peuvent être dans ce type de quartier
        self.places_type_pool = places_type_pool


class DownTown(DistrictType):

    def __init__(self):
        super().__init__(name='Downtown',
                         places_type_pool=[]  # TODO: Place du marché, Arène, Ecoles?, Boutiques, Hotel de ville, Eglise
                         )


class CommercialDistrict(DistrictType):
    def __init__(self):
        super().__init__(name='Commercial district',
                         places_type_pool=[]  # TODO : Boutiques (beaucoup)
                         )


class ResidentialDistrict(DistrictType):

    def __init__(self):
        super().__init__(name='Residential district',
                         places_type_pool=[]  # TODO :  Maisons, Tavernes, Auberges
                         )


class BadDisctrict(DistrictType):

    def __init__(self):
        super().__init__(name='Bad district',
                         places_type_pool=[]  # TODO : Boutiques marché noir, arènes illegales, tavernes malfamées
                         )


class District:
    """
    Classe représentant un quartier d'une ville
    """

    def __init__(self,
                 district_type: DistrictType,
                 sites: list):
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
                 place_types: tuple,
                 rect: pygame.Rect):

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

    def __init__(self,
                 name: str):

        # Nom du type d'endroit
        self.name = name

        # Image du type d'endroit
        self.images_directory = f'../assets/world/places/{name}/'


class ShopType(PlaceType):
    """
    Classe représentant le type d'une boutique (quelconque).
    """

    def __init__(self,
                 opening_hours: tuple = (0, 24)
                 ):
        super().__init__(name='shop')

        # Horaires d'ouverture. Tuple : (x1, x2). Ouvre à x1 heure et ferme à x2 heure.
        self.opening_hours = opening_hours


if __name__ == '__main__':
    pass
