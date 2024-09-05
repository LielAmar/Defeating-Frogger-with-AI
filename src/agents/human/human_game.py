import sys

import pygame

from src.frogger_game import FroggerGame


class HumanGame(FroggerGame):

    def __init__(self, settings):
        super().__init__(settings=settings)

    def update_configuration(self, player):
        self.players.append(player)

    def run_single_game_frame(self):
        self.clock.tick(self.settings.fps)

        self.obstacles.update()
        self.logs.update()

        self.update_game_frame()

        self._draw()

        return any(player.alive for player in self.players)

    def update_game_frame(self):

        super().update_game_frame()

        direction = 4

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    direction = 0
                elif event.key == pygame.K_d:
                    direction = 1
                elif event.key == pygame.K_w:
                    direction = 2
                elif event.key == pygame.K_s:
                    direction = 3
                else:
                    direction = 4

        for player in self.players:
            self.update_player(player, direction)
