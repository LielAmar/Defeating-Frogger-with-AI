from enum import Enum


class Direction(Enum):
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
        if index == 0:
            return Direction.LEFT
        if index == 1:
            return Direction.RIGHT
        if index == 2:
            return Direction.UP
        if index == 3:
            return Direction.DOWN

        return Direction.NONE
