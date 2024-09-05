from argparse import Namespace
from typing import ClassVar, Literal

from src.constants import CELL_SIZE
from src.direction import Direction
from src.entities.lethal_entity import LethalEntity


class Car(LethalEntity):
    """
    A class representing a car entity
    """

    POSSIBLE_CAR_IMAGES: ClassVar = [
        'assets/car1.png',
        'assets/car2.png',
        'assets/car3.png',
    ]

    SPEED: ClassVar = 3

    CAR_SIZE: ClassVar = CELL_SIZE

    def __init__(self, x: int, y: int, settings: Namespace, direction: Direction):
        super().__init__(
            x=x,
            y=y,
            width=self.CAR_SIZE,
            height=self.CAR_SIZE,
            possible_images=self.POSSIBLE_CAR_IMAGES,
            direction=direction,
            settings=settings,
            speed=self.SPEED
        )
