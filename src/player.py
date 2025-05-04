from entity import Entity


class Player(Entity):

    def __init__(self,
                 game: 'Game'):
        super().__init__(game=game,
                         class_name='player')

        self.name = None  # Player name is undefined at initialization


if __name__ == '__main__':
    p = Player('a')

    for stat in p.stats.list:
        print(stat.name, stat.value)

    print(p.stats['INT'])
    p.stats.get('INT').add(12)
    print(p.stats['INT'])

    for stat in p.stats.list:
        print(stat.name, stat.value)