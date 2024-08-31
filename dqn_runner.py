import sys

import pygame

from constants import FPS
from dqn_player import DQNPlayer
from frogger_runner import FroggerGame


class DQNFroggerGame(FroggerGame):

    def __init__(self):
        super().__init__()

        self.players.add(DQNPlayer(5, 4))

    def run_game_step(self):
        self.clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player = self.players.sprites()[0]

        state = player.get_state(self.cars)

        action = player.get_action(state)

        player.update(action)

        reward = -1

        if player.rect.y <= 0:
            reward = 100

        elif pygame.sprite.spritecollideany(player, self.cars) or player.steps == 0:
            reward = -100
            player.alive = False

        next_state = player.get_state(self.cars)
        player.remember(state, action, reward, next_state, not player.alive)

        player.replay()

        self.cars.update()

        self._draw()

        return player.alive


class DQNRunner:
    def __init__(self):
        self.game = DQNFroggerGame()

    def run(self):
        while True:
            if not self.game.run_game_step():
                self.game = DQNFroggerGame()
