import sys
from typing import Optional

import pygame

from src.agents.dqn.dqn_agent import DQNAgent
from src.constants import HEIGHT, CELL_SIZE
from src.direction import Direction
from src.frogger_game import FroggerGame


class DQNFroggerGame(FroggerGame):

    def __init__(self, settings):
        super().__init__(settings=settings)

        self.agent: Optional[DQNAgent] = None

        self.state = None
        self.direction = None
        self.reward = 0
        self.next_state = None

        self.settings.new_fps = self.settings.fps

    def update_configuration(self, agent):
        self.agent = agent

    def reset(self):
        super().reset()

        self.state = None
        self.direction = None
        self.reward = 0
        self.next_state = None

    def update_game_frame(self):
        super().update_game_frame()

        self.reward = 0

        for x, player in enumerate(self.players):
            output = self.agent.act(self.state)
            self.direction = Direction.from_int(output)

            self.update_player(player, self.direction)

            if player.won:
                self.reward += 100 + player.steps * 2

            progress_made = ((HEIGHT - player.rect.y) // CELL_SIZE) - 1

            if self.direction == Direction.UP:
                self.reward += 1
            if self.direction == Direction.DOWN:
                self.reward -= 1

            if self.direction == Direction.UP and player.best_progress < progress_made:
                self.reward += progress_made
                player.best_progress = progress_made

            if not player.alive:
                if not player.won:
                    self.reward -= 50

                if player.game_id < self.settings.lives - 1:
                    player.reset()

    def run_single_game_frame(self):
        """
        Runs a single frame of the game.

        :return: True if the game is still running (any player is alive)
        """

        self.clock.tick(self.settings.new_fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.settings.new_fps = 5 if self.settings.new_fps != 5 else self.settings.fps

        player = self.players[0]

        self.state = player.get_state(self.obstacles)

        self.obstacles.update()
        self.logs.update()

        self.update_game_frame()

        self.next_state = player.get_state(self.obstacles)

        self._draw()

        return any(player.alive for player in self.players)