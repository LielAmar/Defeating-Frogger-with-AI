from argparse import Namespace
from typing import ClassVar

from src.constants import CELL_SIZE
from src.direction import Direction
from src.entities.lethal_entity import LethalEntity


class Log(LethalEntity):
    """
    A class representing a log entity
    """

    POSSIBLE_LOG_IMAGES: ClassVar = [
        'assets/log.png'
    ]

    SPEED: ClassVar = 3

    LOG_SIZE: ClassVar = CELL_SIZE

    def __init__(self, x: int, y: int, settings: Namespace, direction: Direction):
        super().__init__(
            x=x,
            y=y,
            width=self.LOG_SIZE * 3,
            height=self.LOG_SIZE,
            possible_images=self.POSSIBLE_LOG_IMAGES,
            direction=direction,
            settings=settings,
            speed=self.SPEED
        )
