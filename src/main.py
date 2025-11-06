from .game import Game
from .world import world

import time

def main():
    game = Game()

    while True:
        game.update()

def main2():
    world.main()