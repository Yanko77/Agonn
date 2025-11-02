import pygame

from src.mytime import TimeManager


class Game:

    def __init__(self):
        self.time = TimeManager()

    def update(self):
        self.time.update()
        print(self.time.now)