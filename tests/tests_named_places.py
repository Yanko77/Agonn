"""
This module countains all the functions able to test named_places.py file.
"""

from src.world.named_places import CommercialDistrict, ResidentialDistrict, DownTown, BadDistrict, FoodShop, \
    BlacksmithShop, EnchantingShop, EquipmentShop, WeaponShop, ArmourerShop, MarketPlace, Arena, TownHall, Inn, \
    Tavern, Site, Church


def test_district_init_places():

    DISTRICTS = (CommercialDistrict, ResidentialDistrict, DownTown, BadDistrict)
    SITES = (
        [Site('', (FoodShop, BlacksmithShop, EnchantingShop, EquipmentShop, WeaponShop, ArmourerShop), i) for i in range(6)],
        [Site('', (Inn, Tavern), i) for i in range(6)],
        [Site('', (MarketPlace,), 0), Site('', (Arena,), 1),
            Site('', (TownHall,), 2), Site('', (Church,), 3)]
            + [Site('', (FoodShop, BlacksmithShop, ArmourerShop, EnchantingShop, WeaponShop, EquipmentShop), i) for i in range(4, 6)],
        []  # TODO BadDistrict
    )

    for i in range(len(DISTRICTS)):
        district = DISTRICTS[i](game='game', sites=SITES[i])
        district.init_places()

        for site in district.sites:
            # print(type(site.place), site._place_types)
            assert type(site.place) in site._place_types, "Err: Place not in places types"


def exec_tests():
    test_district_init_places()

    print('TESTS OK')
