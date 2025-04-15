"""
This module countains all the functions able to test named_places.py file.
"""
from typing import assert_type

from src.world.named_places import CommercialDistrict, ResidentialDistrict, DownTown, BadDistrict, FoodShop, \
    BlacksmithShop, EnchantingShop, EquipmentShop, WeaponShop, ArmourerShop, MarketPlace, Arena, TownHall, Inn, \
    Tavern, Site, Church, NECESSARY

from src.mytime import Hour


DISTRICTS = (CommercialDistrict, ResidentialDistrict, DownTown, BadDistrict)
SITES = (
        [Site('', (FoodShop, BlacksmithShop, EnchantingShop, EquipmentShop, WeaponShop, ArmourerShop), i) for i in range(6)],
        [Site('', (Inn, Tavern), i) for i in range(6)],
        [Site('', (MarketPlace,), 0), Site('', (Arena,), 1),
            Site('', (TownHall,), 2), Site('', (Church,), 3)]
            + [Site('', (FoodShop, BlacksmithShop, ArmourerShop, EnchantingShop, WeaponShop, EquipmentShop), i) for i in range(4, 6)],
        []  # TODO BadDistrict
    )
PLACES = (Inn, EquipmentShop, WeaponShop, EnchantingShop,  ArmourerShop, MarketPlace, Arena, TownHall, BlacksmithShop,
          Church, Tavern, FoodShop)


def test_district_init_places():

    for i in range(len(DISTRICTS)):
        district = DISTRICTS[i](game='game', sites=SITES[i])
        district.init_places()

        nec_places = district._split_pools()[0]

        # test if the place type is correct relating to the site where it's situated.
        sites_place_type = []
        for site in district.sites:
            # print(type(site.place), site._place_types)
            assert type(site.place) in site._place_types, "Err: Place not in places types"
            sites_place_type.append(site.place.__class__)

        # test if all necessary places are in the district
        for nec_place in nec_places:
            assert nec_place['type'] in sites_place_type, f"{sites_place_type} {nec_place}"


def test_place_init_hrs():
    a = Inn(game='game')
    assert a.is_always_open is False
    assert a.open_hrs == [((Hour("17:0"), Hour("18:0")), (Hour("10:0"), Hour("12:0")))]

    b = Tavern(game='game')
    assert b.is_always_open is True
    assert b.open_hrs is None

    c = Church(game='game')
    assert c.open_hrs[0] == ((Hour("9:0"), Hour("10:0")), Hour("12:00"))
    assert c.open_hrs[1] == ((Hour("14:0"), Hour("15:0")), (Hour("17:0"), Hour("19:0")))


def exec_tests():
    test_district_init_places()
    test_place_init_hrs()

    print('TESTS OK')
