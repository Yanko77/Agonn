from stats import Stat


class Player:

    def __init__(self,
                 game: 'Game'):
        self.game = game
        self.name = 'player'

        self.stats = Stats(self)



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

    def __init__(self, owner: Player):
        self.owner = owner

        self.age = Stat(self)
        self.level = Stat(self)

        self.STR = Stat(self)
        self.DEX = Stat(self)
        self.VIT = Stat(self)
        self.CHA = Stat(self)
        self.INT = Stat(self)
        self.POW = Stat(self)
        self.HEI = Stat(self)

        self.knowledge = Stat(self)
        self.agility = Stat(self)
        self.accuracy = Stat(self)
        self.perception = Stat(self)
        self.communication = Stat(self)
        self.flexibility = Stat(self)

        self.criminology = Stat(self)
        self.biology = Stat(self)
        self.strategy = Stat(self)
        self.crystal_knowledge = Stat(self)

        self.jump = Stat(self)
        self.climbing = Stat(self)
        self.swimming = Stat(self)
        self.acrobatics = Stat(self)

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
        self.smooth_talk = Stat(self)

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

    @property
    def list(self) -> tuple:
        return tuple(attr for attr in self.__dict__.values() if isinstance(attr, Stat))


if __name__ == '__main__':
    p = Player('a')

    print(p.stats.jump.formula)

    p.stats.jump.edit_formula("* 2")

    print(p.stats.jump.formula)

    p.stats.jump.edit_formula('- 1')

    print(p.stats.jump.formula)

    p.stats.jump.back_to_previous_formula()

    print(p.stats.jump.formula)

    p.stats.jump.back_to_previous_formula()

    print(p.stats.jump.formula)

    p.stats.jump.back_to_previous_formula()

    print(p.stats.jump.formula)