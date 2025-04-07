from src.world.named_places import *


def test_district_init_places():

    DISTRICTS = (CommercialDistrict, ResidentialDistrict, DownTown, BadDistrict)
    SITES = (
        [Site('', (FoodShop, BlacksmithShop, EnchantingShop, EquipmentShop, WeaponShop, ArmourerShop), i) for i in range(6)],
        [Site('', (Inn, Tavern), i) for i in range(6)],
        [Site('', (MarketPlace,), 0), Site('', (Arena,), 1), Site('', (TownHall,), 2), Site('', (Church,), 3)] + [Site('', (FoodShop, BlacksmithShop, ArmourerShop, EnchantingShop, WeaponShop, EquipmentShop), i) for i in range(4, 6)],
        []  # TODO BadDistrict
    )

    for i in range(len(DISTRICTS)):
        district = DISTRICTS[i](game='game', sites=SITES[i])
        district.init_places()

        for site in district.sites:
            assert type(site.place) in site._place_types, "Err: Place not in places types"


if __name__ == '__main__':
    test_district_init_places()

    print('OK')
