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
    """
    To read a stat:
        Use __getitem__ method

        Example:
            ```
            stats = Stats(..., ...)
            stats['knowledge']
            ```

    To increment a stat:
        Use __getattribute__ method and Stat.__add__ method

        Example:
            ```
            stats = Stats(..., ...)
            stats.knowledge += 10  # Increments knowledge stat by 10
            ```
    """

    def __init__(self, owner: Player, stats: list[int]):
        self.owner = owner

        (
            self.STR,
            self.DEX,
            self.VIT,
            self.CHA,
            self.INT,
            self.POW,
            self.HEI
        ) = stats

        self.knowledge = Stat(self)
        self.agility = Stat(self)
        self.accuracy = Stat(self)
        self.perception = Stat(self)

        '''self.biology = Stat(self)
        self.strategy = Stat(self)
        self.crystal_know = Stat(self)

        self.jump = Stat(self)
        self.climbing = Stat(self)

        self.lock_picking = Stat(self)
        self.traps = Stat(self)

        self.martial_arts = Stat(self)
        self.stealth = Stat(self)
        self.dodging = Stat(self)
        self.draw_quickly = Stat(self)

        self.balance = Stat(self)
        self.listen = Stat(self)
        self.smell = Stat(self)
        self.see = Stat(self)
        self.taste = Stat(self)
        self.chase = Stat(self)

        self.trading = Stat(self)
        self.smooth_talk = Stat(self)'''

    def __getitem__(self, item):
        """
        Returns the value of item in self.
        """
        return self.__getattribute__(item).value

    def locals(self):
        """
        Returns locals variables of the class.
        """
        return locals()


if __name__ == '__main__':
    p = Player('a')

    print(p.stats['knowledge'])
    p.stats.knowledge += 1
    print(p.stats['knowledge'])
    p.stats.INT += 1
    print(p.stats['knowledge'])
    p.age += 2
    print(p.stats['knowledge'])
