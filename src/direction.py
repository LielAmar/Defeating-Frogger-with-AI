from enum import Enum

import pygame


class Direction(Enum):
    """"
    Enum class for directions
    """

    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    NONE = 4

    def __str__(self):
        return self.name

    @property
    def x(self):
        return self.to_vector()[0]

    @property
    def y(self):
        return self.to_vector()[1]

    def to_vector(self):
        if self == Direction.LEFT:
            return -1, 0
        if self == Direction.RIGHT:
            return 1, 0
        if self == Direction.UP:
            return 0, -1
        if self == Direction.DOWN:
            return 0, 1
        return 0, 0

    @staticmethod
    def from_int(index):
        for direction in Direction:
            if direction.value == index:
                return direction

    @staticmethod
    def from_key(key):
        if key == pygame.K_a:
            return Direction.LEFT
        elif key == pygame.K_d:
            return Direction.RIGHT
        elif key == pygame.K_w:
            return Direction.UP
        elif key == pygame.K_s:
            return Direction.DOWN

        return Direction.NONE
