import random
from typing import ClassVar, Literal

import pygame

from src.constants import CELL_SIZE, WIDTH
from src.utils import crop_image


class Log(pygame.sprite.Sprite):

    POSSIBLE_LOG_IMAGES: ClassVar = [
        'assets/log.png'
    ]

    SPEED: ClassVar = 3

    LOG_SIZE: ClassVar = CELL_SIZE

    def __init__(self, x: int, y: int, direction: Literal[1, -1], grid_like: bool = False):
        super().__init__()

        self.image = pygame.transform.scale(
            crop_image(pygame.image.load(random.choice(self.POSSIBLE_LOG_IMAGES)).convert_alpha()),
            (3 * self.LOG_SIZE, self.LOG_SIZE)
        )

        if direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.direction = direction
        self.grid_like = grid_like

    def update(self):
        self.rect.x += self.direction * (CELL_SIZE if self.grid_like else self.SPEED)

        if self.rect.x > WIDTH and self.direction == 1:
            self.rect.x = -self.rect.width
        elif self.rect.x < -self.rect.width and self.direction == -1:
            self.rect.x = WIDTH
