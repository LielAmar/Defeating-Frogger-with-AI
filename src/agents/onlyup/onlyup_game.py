import pygame

from src.frogger_game import FroggerGame


class OnlyUpGame(FroggerGame):

    def __init__(self, settings):
        super().__init__(settings=settings)

    def update_configuration(self, player):
        self.players.append(player)

    def update_game_frame(self):
        super().update_game_frame()

        for x, player in enumerate(self.players):
            direction = 2  # up

            self.update_player(player, direction)
