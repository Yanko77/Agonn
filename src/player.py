from stats import Stat


class Player:

    def __init__(self,
                 game: 'Game',
                 age: int = 20):
        self.game = game
        self.name = 'player'

        self.age = age

        self.stats = Stats(self, [0, 0, 0, 0, 0, 0, 0])


class Stats:

    def __init__(self, player: Player, stats: list[int]):
        self.player = player

        (
            self.STR,
            self.DEX,
            self.VIT,
            self.CHA,
            self.INT,
            self.POW,
            self.HEI
        ) = stats

        self.knowledge = Stat(self.player, 'knowledge')
        self.agility = Stat(self.player, 'agility')
        self.accuracy = Stat(self.player, 'accuracy')
        self.perception = Stat(self.player, 'perception')

        self.biology = ...
        self.strategy = ...
        self.crystal_know = ...

        self.jump = ...
        self.climbing = ...

        self.lock_picking = ...
        self.traps = ...

        self.martial_arts = ...
        self.stealth = ...
        self.dodging = ...
        self.draw_quickly = ...

        self.balance = ...
        self.listen = ...
        self.smell = ...
        self.see = ...
        self.taste = ...
        self.chase = ...

        self.trading = ...
        self.smooth_talk = ...

    def __getitem__(self, item):
        local_vars = {}
        code = f'res = {self.__getattribute__(item).formula}'
        exec(code, locals(), local_vars)

        return local_vars['res']


if __name__ == '__main__':
    p = Player('a')

    p.stats.INT = 15

    print(p.stats['agility'])
