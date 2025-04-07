import pygame

from src.mytime import Time


class Game:

    def __init__(self):
        self.time = Time()

    def update(self):
        self.time.update()
