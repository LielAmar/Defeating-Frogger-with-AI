import random

import pygame

from src.direction import Direction
from src.frogger_game import FroggerGame


class RandomGame(FroggerGame):

    def __init__(self, settings):
        super().__init__(settings=settings)

    def update_configuration(self, player):
        self.players.append(player)

    def update_game_frame(self):
        super().update_game_frame()

        for x, player in enumerate(self.players):
            self.update_player(player, random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]))
