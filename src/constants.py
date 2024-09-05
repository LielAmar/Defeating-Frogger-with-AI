from typing import Literal

from src.direction import Direction

# Window Configuration
GRID_SIZE = 16
CELL_SIZE = 40

WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE

# Game Configurations
CARS_PER_ROW = 2
LOGS_PER_ROW = 3

NEAT_MAX_STEPS = 50

# Map
CAR_ROWS: list[tuple[int, Direction]] = [
    (9, Direction.LEFT),
    (10, Direction.RIGHT),
    (11, Direction.LEFT),
    (12, Direction.RIGHT)
]

WATER_ROWS: list[tuple[int, Direction]] = [
    (2, Direction.RIGHT),
    (3, Direction.LEFT),
    (4, Direction.RIGHT),
    (5, Direction.LEFT),
]

TRAIN_ROWS: list[tuple[int, Direction]] = [
    (7, Direction.RIGHT)
]

FINISH_ROWS: list[tuple[int, Direction]] = [
    (0, Direction.NONE)
]
GRASS_ROWS: list[tuple[int, Direction]] = [
    (13, Direction.NONE),
    (14, Direction.NONE),
    (15, Direction.NONE)
]
SIDEWALK_ROWS: list[tuple[int, Direction]] = [
    (1, Direction.NONE),
    (6, Direction.NONE),
    (8, Direction.NONE)
]

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
