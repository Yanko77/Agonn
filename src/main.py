from .game import Game
from . import stats

import time

def main():
    game = Game()

    while True:
        game.update()
    
def main2():
    stats.main()
