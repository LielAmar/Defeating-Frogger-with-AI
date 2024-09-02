from abc import abstractmethod, ABC
from typing import ClassVar

import pygame

from src.constants import CELL_SIZE, WIDTH, HEIGHT, NEAT_MAX_STEPS
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

        self.direction = 2
        self.steps = NEAT_MAX_STEPS

        self.game_id = -1
        self.fitnesses = []
        self.action_taken = []

        self.reset()

    def reset(self):
        self.rect.x = WIDTH // 2 - CELL_SIZE // 2
        self.rect.y = HEIGHT - CELL_SIZE

        self.won = False
        self.alive = True

        self.direction = 2
        self.steps = NEAT_MAX_STEPS

        self.fitnesses.append(0)
        self.game_id = len(self.fitnesses) - 1

    def update(self, direction: int):
        self.direction = direction

        self.steps -= 1
        self.action_taken.append(direction)

        if direction == 0:
            self.rect.x -= CELL_SIZE
        elif direction == 1:
            self.rect.x += CELL_SIZE
        elif direction == 2:
            self.rect.y -= CELL_SIZE
        elif direction == 3:
            self.rect.y += CELL_SIZE

        self.rect.x = max(0, min(self.rect.x, WIDTH - CELL_SIZE))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - CELL_SIZE))

    @abstractmethod
    def get_state(self, cars: pygame.sprite.Group) -> list:
        ...
