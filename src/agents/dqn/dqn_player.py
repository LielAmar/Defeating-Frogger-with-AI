from argparse import Namespace

import pygame

from src.constants import CELL_SIZE
from src.entities.player import Player
from src.entities.train import Train


class DQNPlayer(Player):

    MAX_DISTANCE = 5

    MAX_STEPS = 50

    def __init__(self, settings: Namespace):
        super().__init__()

        self.settings = settings

        self.steps = self.MAX_STEPS

        self.best_progress = 0

    def reset(self):
        super().reset()

        self.steps = self.MAX_STEPS

        self.best_progress = 0

    def get_state(self, obstacles: pygame.sprite.Group = None, logs: pygame.sprite.Group = None) -> list:
        states = 25

        states += 5 if self.settings.train else 0
        states += 15 if self.settings.water else 0

        state = [0.0] * states

        # Left-Side Sensor (directly horizontal to the left)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y and obstacle.rect.x < self.rect.x:
                distance = (self.rect.x - obstacle.rect.x) / CELL_SIZE
                if distance <= self.MAX_DISTANCE:
                    state[0] = max(state[0], 1.0 - (distance * (1 / self.MAX_DISTANCE)))
                    state[13] = obstacle.direction.x

        # Right-Side Sensor (directly horizontal to the right)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y and obstacle.rect.x > self.rect.x:
                distance = (obstacle.rect.x - self.rect.x) / CELL_SIZE
                if distance <= self.MAX_DISTANCE:
                    state[1] = max(state[1], 1.0 - (distance * (1 / self.MAX_DISTANCE)))
                    state[14] = obstacle.direction.x

        # Up-Side Sensor (directly vertical above)
        for obstacle in obstacles:
            if obstacle.rect.x == self.rect.x and obstacle.rect.y < self.rect.y:
                distance = (self.rect.y - obstacle.rect.y) / CELL_SIZE
                if distance <= self.MAX_DISTANCE:
                    state[2] = max(state[2], 1.0 - (distance * (1 / self.MAX_DISTANCE)))
                    state[15] = obstacle.direction.x

        # Down-Side Sensor (directly vertical below)
        for obstacle in obstacles:
            if obstacle.rect.x == self.rect.x and obstacle.rect.y > self.rect.y:
                distance = (obstacle.rect.y - self.rect.y) / CELL_SIZE
                if distance <= self.MAX_DISTANCE:
                    state[3] = max(state[3], 1.0 - (distance * (1 / self.MAX_DISTANCE)))
                    state[16] = obstacle.direction.x

        # Top-Left Sensor (one row above, to the left)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y - CELL_SIZE and obstacle.rect.x < self.rect.x:
                distance = (self.rect.x - obstacle.rect.x) / CELL_SIZE
                if distance <= self.MAX_DISTANCE:
                    state[4] = max(state[4], 1.0 - (distance * (1 / self.MAX_DISTANCE)))
                    state[17] = obstacle.direction.x

        # Top-Right Sensor (one row above, to the right)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y - CELL_SIZE and obstacle.rect.x > self.rect.x:
                distance = (obstacle.rect.x - self.rect.x) / CELL_SIZE
                if distance <= self.MAX_DISTANCE:
                    state[5] = max(state[5], 1.0 - (distance * (1 / self.MAX_DISTANCE)))
                    state[18] = obstacle.direction.x

        # Bottom-Left Sensor (one row below, to the left)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y + CELL_SIZE and obstacle.rect.x < self.rect.x:
                distance = (self.rect.x - obstacle.rect.x) / CELL_SIZE
                if distance <= self.MAX_DISTANCE:
                    state[6] = max(state[6], 1.0 - (distance * (1 / self.MAX_DISTANCE)))
                    state[19] = obstacle.direction.x

        # Bottom-Right Sensor (one row below, to the right)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y + CELL_SIZE and obstacle.rect.x > self.rect.x:
                distance = (obstacle.rect.x - self.rect.x) / CELL_SIZE
                if distance <= self.MAX_DISTANCE:
                    state[7] = max(state[7], 1.0 - (distance * (1 / self.MAX_DISTANCE)))
                    state[20] = obstacle.direction.x

        # Top-Top-Left Sensor (two rows above, to the left)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y - CELL_SIZE * 2 and obstacle.rect.x < self.rect.x:
                distance = (self.rect.x - obstacle.rect.x) / CELL_SIZE
                if distance <= self.MAX_DISTANCE:
                    state[8] = max(state[8], 1.0 - (distance * (1 / self.MAX_DISTANCE)))
                    state[21] = obstacle.direction.x

        # Top-Top-Right Sensor (two rows above, to the right)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y - CELL_SIZE * 2 and obstacle.rect.x > self.rect.x:
                distance = (obstacle.rect.x - self.rect.x) / CELL_SIZE
                if distance <= self.MAX_DISTANCE:
                    state[9] = max(state[9], 1.0 - (distance * (1 / self.MAX_DISTANCE)))
                    state[22] = obstacle.direction.x

        # Bottom-Bottom-Left Sensor (two rows below, to the left)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y + CELL_SIZE * 2 and obstacle.rect.x < self.rect.x:
                distance = (self.rect.x - obstacle.rect.x) / CELL_SIZE
                if distance <= self.MAX_DISTANCE:
                    state[10] = max(state[10], 1.0 - (distance * (1 / self.MAX_DISTANCE)))
                    state[23] = obstacle.direction.x

        # Bottom-Bottom-Right Sensor (two rows below, to the right)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y + CELL_SIZE * 2 and obstacle.rect.x > self.rect.x:
                distance = (obstacle.rect.x - self.rect.x) / CELL_SIZE
                if distance <= self.MAX_DISTANCE:
                    state[11] = max(state[11], 1.0 - (distance * (1 / self.MAX_DISTANCE)))
                    state[24] = obstacle.direction.x

        state[12] = self.MAX_STEPS - self.steps

        if self.settings.water:
            # Top left
            state[25] = 1.0
            for log in logs:
                if log.rect.y == self.rect.y - CELL_SIZE and log.rect.x < self.rect.x:
                    distance = (self.rect.x - log.rect.x) / CELL_SIZE
                    if distance <= self.MAX_DISTANCE:
                        state[25] = min(state[25], (distance * (1 / self.MAX_DISTANCE)))
                        state[26] = log.direction.x

            # Top right
            state[27] = 1.0
            for log in logs:
                if log.rect.y == self.rect.y - CELL_SIZE and log.rect.x > self.rect.x:
                    distance = (log.rect.x - self.rect.x) / CELL_SIZE
                    if distance <= self.MAX_DISTANCE:
                        state[27] = min(state[27], (distance * (1 / self.MAX_DISTANCE)))
                        state[28] = log.direction.x

            # Bottom left
            state[29] = 1.0
            for log in logs:
                if log.rect.y == self.rect.y + CELL_SIZE and log.rect.x < self.rect.x:
                    distance = (self.rect.x - log.rect.x) / CELL_SIZE
                    if distance <= self.MAX_DISTANCE:
                        state[29] = min(state[29], (distance * (1 / self.MAX_DISTANCE)))
                        state[30] = log.direction.x

            # Bottom right
            state[31] = 1.0
            for log in logs:
                if log.rect.y == self.rect.y + CELL_SIZE and log.rect.x > self.rect.x:
                    distance = (log.rect.x - self.rect.x) / CELL_SIZE
                    if distance <= self.MAX_DISTANCE:
                        state[31] = min(state[31], (distance * (1 / self.MAX_DISTANCE)))
                        state[32] = log.direction.x

            # Top
            state[33] = 1.0
            for log in logs:
                if log.rect.x == self.rect.x and log.rect.y < self.rect.y:
                    distance = (self.rect.y - log.rect.y) / CELL_SIZE
                    if distance <= self.MAX_DISTANCE:
                        state[33] = min(state[33], (distance * (1 / self.MAX_DISTANCE)))
                        state[34] = log.direction.x

            # Bottom
            state[35] = 1.0
            for log in logs:
                if log.rect.x == self.rect.x and log.rect.y > self.rect.y:
                    distance = (log.rect.y - self.rect.y) / CELL_SIZE
                    if distance <= self.MAX_DISTANCE:
                        state[35] = min(state[35], (distance * (1 / self.MAX_DISTANCE)))
                        state[36] = log.direction.x

            for log in logs:
                if log.player is not None:
                    state[37] = 1
                    state[38] = (self.rect.x - log.rect.x) / CELL_SIZE
                    state[39] = ((log.rect.x + (log.rect.width - CELL_SIZE)) - self.rect.x) / CELL_SIZE

        if self.settings.train:
            for obstacle in obstacles:
                if isinstance(obstacle, Train):
                    state[40 if self.settings.water else 25] = obstacle.direction.x
                    state[41 if self.settings.water else 26] = obstacle.direction.x
                    state[42 if self.settings.water else 27] = obstacle.rect.x / CELL_SIZE

            state[43 if self.settings.water else 28] = self.rect.x
            state[44 if self.settings.water else 29] = self.rect.y

        return state
