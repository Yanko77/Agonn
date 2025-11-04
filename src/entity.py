from .stats import Stats


class Entity:
    """
    An entity is a character of the game.
    The player or all mobs are entities.
    """
    def __init__(self,
                 game: 'Game',
                 class_name: str):
        self.game = game
        self.class_name = class_name

        self.stats = Stats(self)
