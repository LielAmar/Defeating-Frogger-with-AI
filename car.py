import random

import pygame

from constants import CELL_SIZE, WIDTH, FPS
from utils import crop_image

POSSIBLE_CAR_IMAGES = [
    'assets/car1.png',
    'assets/car2.png',
    'assets/car3.png',
]


class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, grid):
        super().__init__()

        self.image = pygame.transform.scale(
            crop_image(pygame.image.load(random.choice(POSSIBLE_CAR_IMAGES)).convert_alpha()),
            (CELL_SIZE, CELL_SIZE)
        )

        if direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = 3

        self.direction = direction
        self.grid = grid


    def update(self):
        if self.grid:
            self.rect.x += self.direction * CELL_SIZE
        else:
            self.rect.x += self.speed * self.direction


        if self.rect.x > WIDTH and self.direction == 1:
            self.rect.x = -self.rect.width
        elif self.rect.x < -self.rect.width and self.direction == -1:
            self.rect.x = WIDTH
