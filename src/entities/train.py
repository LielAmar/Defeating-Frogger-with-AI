import random
from argparse import Namespace
from typing import ClassVar

from src.constants import CELL_SIZE
from src.direction import Direction
from src.entities.lethal_entity import LethalEntity


class Train(LethalEntity):
    """
    A class representing a train entity
    """

    POSSIBLE_TRAIN_IMAGES: ClassVar = [
        'assets/train.png',
    ]

    SPEED: ClassVar = 30
    PROBABILITY: ClassVar = 0.03

    TRAIN_SIZE: ClassVar = CELL_SIZE

    def __init__(self, x: int, y: int, settings: Namespace, direction: Direction):
        super().__init__(
            x=x,
            y=y,
            width=self.TRAIN_SIZE * 5,
            height=self.TRAIN_SIZE,
            possible_images=self.POSSIBLE_TRAIN_IMAGES,
            direction=direction,
            settings=settings,
            speed=self.SPEED
        )

        self.active = True

    def update(self) -> bool:
        """
        Update the position of the train

        If the train is active, update its position
        Otherwise, with a certain probability, activate the train

        :return: True if the train was out of bounds
        """

        if self.active:
            if super().update():
                self.active = False
                return True
        else:
            if random.random() < self.PROBABILITY:
                self.active = True
                self.reset()

        return False
