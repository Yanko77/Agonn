from world.named_places import *

district = District('game',
                    ResidentialDistrict('game'),
                    [
                        Site('game',
                             (Inn, Tavern),
                             1),
                        Site('game',
                             (Inn, Tavern),
                             2),
                        Site('game',
                             (Inn, Tavern),
                             3),
                        Site('game',
                             (Inn, Tavern),
                             4),
                        Site('game',
                             (Inn, Tavern),
                             5),
                        Site('game',
                             (Inn, Tavern),
                             6)
                    ])

district.init_places()

for site in district.sites:
    print(site.rect, site.place, site._place_types)