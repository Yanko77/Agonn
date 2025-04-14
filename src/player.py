


class Player:

    def __init__(self, game):
        self.game = game

        self.stats = Stats(self, [0, 0, 0, 0, 0, 0, 0])



class Stats:

    def __init__(self, player: Player, stats: list[int]):
        self.player = player

        (self.intelligence,
        self.constitution,
        self.strength,
        self.power,
        self.dexterity,
        self.agility,
        self.perception) = stats

        self.biology = 0.7*self.intelligence + 0.2*self.constitution + 0.1*self.perception
        self.strategy = 0.6*self.intelligence + 0.2*max(self.power, self.strength) + 0.2*self.constitution
        self.crystal_know = 0.8*self.intelligence + 0.2*self.power

        self.jump = 0.7*self.agility + 0.2*self.constitution + 0.1*self.perception
        self.climbing = 0.7*self.agility + 0.3*self.constitution

        self.lock_picking = self.intelligence*0.4 + self.dexterity*0.6
        self.traps = self.intelligence * 0.4 + self.strength*0.3 + self.dexterity*0.3

        self.martial_arts = self.dexterity*0.4 + self.strength*0.3 + self.agility*0.3
        self.stealth = self.agility*0.8 + self.dexterity*0.3 - 0.1*self.constitution
        self.dodging = self.agility*0.9 + self.dexterity*0.3 - self.constitution*0.2
        self.draw_quickly = self.dexterity*0.8 + self.agility*0.1 + self.strength*0.1

        self.balance = self.constitution*0.5 + self.perception*0.5
        self.listen = self.perception
        self.smell = self.perception
        self.see = self.perception
        self.taste = self.perception
        self.chase = self.perception

        self.trading = self.intelligence*0.6 + self.perception*0.2 + self.constitution*0.2
        self.smooth_talk = self.intelligence*0.4 + self.power*0.2 + self.perception*0.2 + self.constitution*0.2


if __name__ == '__main__':
    p = Player('a')
