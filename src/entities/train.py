import random
from typing import ClassVar

import pygame

from src.constants import CELL_SIZE, WIDTH
from src.utils import crop_image


class Train(pygame.sprite.Sprite):
    POSSIBLE_TRAIN_IMAGES: ClassVar = [
        'assets/train.png',
    ]

    SPEED: ClassVar = 30
    PROBABILITY: ClassVar = 0.03

    TRAIN_SIZE: ClassVar = CELL_SIZE

    def __init__(self, x: int, y: int):
        super().__init__()

        self.image = pygame.transform.scale(
            crop_image(pygame.image.load(random.choice(self.POSSIBLE_TRAIN_IMAGES)).convert_alpha()),
            (self.TRAIN_SIZE * 10, self.TRAIN_SIZE)
        )

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.active = True
        self.time_since_death = -1

    def update(self):
        if self.active:
            self.rect.x += self.SPEED
        else:
            if random.random() < self.PROBABILITY:
                self.active = True
                self.reset()

        if self.rect.x > WIDTH:
            self.active = False
            self.time_since_death = pygame.time.get_ticks()

    def reset(self):
        self.rect.x = -self.rect.width
