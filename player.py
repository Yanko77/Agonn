from dataclasses import dataclass


class Player:

    def __init__(self, game):
        self.game = game

        self.stats = Stats()


@dataclass
class Stats:
    intelligence: int = 0
    constitution: int = 0
    charisma: int = 0
    dexterity: int = 0
    agility: int = 0
    perception: int = 0


if __name__ == '__main__':
    p = Player('a')
