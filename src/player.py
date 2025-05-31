from entity import Entity
from stats import StatBuff


class Player(Entity):

    def __init__(self,
                 game: 'Game'):
        super().__init__(game=game,
                         class_name='player')

        self.name = None  # Player name is undefined at initialization


if __name__ == '__main__':
    from game import Game
    p = Player(Game())

    for stat in p.stats.list:
        print(stat.name, stat.value)

    p.stats.get('trading').add(10)

    for stat in p.stats.list:
        print(stat.name, stat.value)

