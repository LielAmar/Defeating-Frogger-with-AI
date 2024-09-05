import random
from argparse import Namespace

import pygame

from src.constants import CELL_SIZE, WIDTH
from src.direction import Direction
from src.utils import crop_image


class LethalEntity(pygame.sprite.Sprite):

    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            possible_images: list[str],
            direction: Direction,
            settings: Namespace,
            speed: int
    ):
        super().__init__()

        self.image = pygame.transform.scale(
            crop_image(pygame.image.load(random.choice(possible_images)).convert_alpha()),
            (width, height)
        )

        if direction == Direction.LEFT:
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.direction = direction
        self.speed = speed
        self.settings = settings

    def update(self) -> bool:
        """
        Update the position of the entity

        :return: True if the entity was out of bounds
        """

        self.rect.x += self.direction.x * (CELL_SIZE if self.settings.grid_like else self.speed)

        if self.rect.x > WIDTH and self.direction == Direction.RIGHT:
            self.rect.x = -self.rect.width
            return True
        elif self.rect.x < -self.rect.width and self.direction == Direction.LEFT:
            self.rect.x = WIDTH
            return True

        return False

    def reset(self):
        """
        Reset the position of the entity
        """

        if self.direction == Direction.RIGHT:
            self.rect.x = -self.rect.width
        elif self.direction == Direction.LEFT:
            self.rect.x = WIDTH
