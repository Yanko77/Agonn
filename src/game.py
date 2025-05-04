import pygame

from src.mytime import Time


class Game:

    def __init__(self):
        self.time = Time()

        self._id = 0

    def update(self):
        self.time.update()

    def get_unique_id(self) -> int:
        self._id += 1
        return self._id


if __name__ == '__main__':
    game = Game()

    print(game.get_unique_id())
    print(game.get_unique_id())