from entity import Entity
from stats import StatBuff


class Player(Entity):

    def __init__(self,
                 game: 'Game'):
        super().__init__(game=game,
                         class_name='player')

        self.name = None  # Player name is undefined at initialization


if __name__ == '__main__':
    p = Player('a')

    print(p.stats.get('knowledge').buffs)
    print(p.stats.get('knowledge').value)

    buff1 = StatBuff('100%', formula='(formula) * 2')
    buff1.id = 1

    p.stats.get('knowledge').add_buff(buff1)

    print(p.stats.get('knowledge').buffs)
    print(p.stats.get('knowledge').value)

    p.stats.get('knowledge').add_buff(StatBuff('-100%', formula='(formula) / 2'))

    print(p.stats.get('knowledge').buffs)
    print(p.stats.get('knowledge').value)

