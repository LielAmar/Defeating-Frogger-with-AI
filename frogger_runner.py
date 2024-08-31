from abc import ABC

import random
import pygame

from car import Car
from constants import WIDTH, HEIGHT, BLACK, CARS_PER_ROW, CELL_SIZE


class FroggerGame(ABC):
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption("Frogger Game")

        self.clock = pygame.time.Clock()

        self.cars = self.create_cars()
        self.players = pygame.sprite.Group()

    @staticmethod
    def create_cars():
        cars = pygame.sprite.Group()
        car_rows = [
            (2, 1),
            (3, -1),
            (4, 1),
            (5, -1),

            (9, -1),
            (10, 1),
            (11, -1),
            (12, 1)
        ]

        for row, direction in car_rows:
            second_offset = random.randint(0, 6)
            offset = random.randint(3, 6)

            for i in range(CARS_PER_ROW):
                car = Car((i * offset + second_offset) * CELL_SIZE, row * CELL_SIZE, direction)
                cars.add(car)

        return cars

    def _draw(self):
        self.screen.fill(BLACK)

        self.cars.draw(self.screen)

        for player in self.players:
            if player.alive:
                self.screen.blit(player.image, player.rect.topleft)

        pygame.display.flip()
