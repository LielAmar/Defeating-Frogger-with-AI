import pygame

from src.frogger_game import FroggerGame


class OnlyUpGame(FroggerGame):

    def __init__(self, grid_like: bool = False):
        super().__init__(grid_like=grid_like)

    def update_configuration(self, player):
        self.players.append(player)

    def update_game_frame(self):
        super().update_game_frame()

        for x, player in enumerate(self.players):
            up_direction = 2

            player.update(up_direction)

            if pygame.sprite.spritecollideany(player, self.cars):
                player.alive = False

            if player.steps == 0:
                player.alive = False

            if player.rect.y <= 0:
                player.alive = False
                player.won = True
