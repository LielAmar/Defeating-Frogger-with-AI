import pygame

from src.constants import CELL_SIZE
from src.direction import Direction
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
        state = [[0.0] * 16] * 16

        for obstacle in obstacles:
            x = (obstacle.rect.x - self.rect.x) // CELL_SIZE
            y = (obstacle.rect.y - self.rect.y) // CELL_SIZE

            if 0 <= x < 16 and 0 <= y < 16:
                state[y][x] = 1.0 if obstacle.direction == Direction.LEFT else 2.0

        player_x = self.rect.x // CELL_SIZE
        player_y = self.rect.y // CELL_SIZE

        state[player_y][player_x] = 3.0

        # state.append(self.steps)

        return state
