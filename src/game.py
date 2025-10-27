import pygame

from src.mytime import TimeManager


class Game:

    def __init__(self):
        self.time = TimeManager()

        self._id = 0

    def update(self):
        self.time.update()
        print(self.time.now)
        

    def get_unique_id(self) -> int:
        self._id += 1
        return self._id