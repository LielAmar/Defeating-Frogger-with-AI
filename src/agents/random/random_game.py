import random

import pygame

from src.frogger_game import FroggerGame


class RandomGame(FroggerGame):

    def __init__(self, grid_like: bool = False):
        super().__init__(grid_like=grid_like)

    def update_configuration(self, player):
        self.players.append(player)

    def update_game_frame(self):
        super().update_game_frame()

        for x, player in enumerate(self.players):
            direction = random.randint(0, 4)

            player.update(direction)

            if pygame.sprite.spritecollideany(player, self.obstacles):
                player.alive = False

            if player.steps == 0:
                player.alive = False

            if player.rect.y <= 0:
                player.alive = False
                player.won = True
