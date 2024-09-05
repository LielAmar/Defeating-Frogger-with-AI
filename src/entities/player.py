from abc import abstractmethod, ABC
from typing import ClassVar

import pygame

from src.constants import CELL_SIZE, WIDTH, HEIGHT, NEAT_MAX_STEPS
from src.direction import Direction
from src.utils import crop_image


class Player(pygame.sprite.Sprite, ABC):
    PLAYER_IMAGE: ClassVar = 'assets/player.png'

    PLAYER_SIZE: ClassVar = CELL_SIZE

    def __init__(self):
        super().__init__()

        self.image = pygame.transform.scale(
            crop_image(pygame.image.load(self.PLAYER_IMAGE).convert_alpha()),
            (self.PLAYER_SIZE, self.PLAYER_SIZE)
        )

        self.rect = self.image.get_rect()

        self.won = False
        self.alive = True

        self.steps = NEAT_MAX_STEPS

        self.fitnesses = []
        self.action_taken = []

        self.game_id = 0

        self.reset()

    def reset(self):
        self.rect.x = WIDTH // 2 - CELL_SIZE
        self.rect.y = HEIGHT - CELL_SIZE

        self.won = False
        self.alive = True

        self.steps = NEAT_MAX_STEPS

        self.fitnesses.append(0)

        self.game_id = len(self.fitnesses) - 1

    def update(self, direction: Direction):
        self.steps -= 1
        self.action_taken.append(direction)

        self.rect.x = max(0, min(self.rect.x + direction.x * self.PLAYER_SIZE, WIDTH - CELL_SIZE))
        self.rect.y = max(0, min(self.rect.y + direction.y * self.PLAYER_SIZE, HEIGHT - CELL_SIZE))
