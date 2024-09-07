import pygame

from src.constants import CELL_SIZE
from src.entities.player import Player


class DQNPlayer(Player):

    MAX_DISTANCE = 5

    MAX_STEPS = 50

    def __init__(self):
        super().__init__()

        self.steps = self.MAX_STEPS

        self.best_progress = 0

    def reset(self):
        super().reset()

        self.steps = self.MAX_STEPS

        self.best_progress = 0

    def get_state(self, obstacles: pygame.sprite.Group):
        state = [0.0] * 25

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

        # state[13] = self.rect.x / CELL_SIZE
        # state[14] = self.rect.y / CELL_SIZE

        return state
