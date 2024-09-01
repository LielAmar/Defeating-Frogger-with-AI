from abc import ABC

import random
import pygame

from car import Car
from constants import WIDTH, HEIGHT, BLACK, CARS_PER_ROW, CELL_SIZE


class FroggerGame(ABC):

    CAR_ROWS = [
        (2, 1),
        (3, -1),
        (4, 1),
        (5, -1),

        (9, -1),
        (10, 1),
        (11, -1),
        (12, 1)
    ]

    FINISH_ROWS = [
        0
    ]

    GRASS_ROWS = [
        13,
        14,
        15
    ]

    SIDEWALK_ROWS = [
        1,
        6,
        7,
        8,
    ]

    def __init__(self, grid=False):
        self.grid = grid

        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption("Frogger Game")

        self.clock = pygame.time.Clock()

        self.cars = self.create_cars()
        self.players = pygame.sprite.Group()

        self.road_image = pygame.image.load('assets/road.png')
        self.grass_image = pygame.image.load('assets/grass.png')
        self.finish_image = pygame.image.load('assets/finish.png')
        self.sidewalk_image = pygame.image.load('assets/sidewalk.png')

        # Resize every image to be of height CELL_SIZE and width with respect to the aspect ratio
        self.road_image = pygame.transform.scale(self.road_image, ((CELL_SIZE / self.road_image.get_height()) * self.road_image.get_width(), CELL_SIZE))
        self.grass_image = pygame.transform.scale(self.grass_image, ((CELL_SIZE / self.grass_image.get_height()) * self.grass_image.get_width(), CELL_SIZE))
        self.finish_image = pygame.transform.scale(self.finish_image, ((CELL_SIZE / self.finish_image.get_height()) * self.finish_image.get_width(), CELL_SIZE))
        self.sidewalk_image = pygame.transform.scale(self.sidewalk_image, ((CELL_SIZE / self.sidewalk_image.get_height()) * self.sidewalk_image.get_width(), CELL_SIZE))

    def create_cars(self):
        cars = pygame.sprite.Group()

        for row, direction in self.CAR_ROWS:
            second_offset = random.randint(0, 6)
            offset = random.randint(3, 8)

            for i in range(CARS_PER_ROW):
                car = Car((i * offset + second_offset) * CELL_SIZE, row * CELL_SIZE, direction, self.grid)
                cars.add(car)

        return cars

    def _draw(self):
        self.screen.fill(BLACK)

        # Finish line
        for i in range(0, WIDTH, self.finish_image.get_width()):
            for row in self.FINISH_ROWS:
                self.screen.blit(self.finish_image, (i, row * CELL_SIZE))

        # Grass
        for i in range(0, WIDTH, self.grass_image.get_width()):
            for row in self.GRASS_ROWS:
                self.screen.blit(self.grass_image, (i, row * CELL_SIZE))

        # Road
        for i in range(0, WIDTH, self.road_image.get_width()):
            for row, direction in self.CAR_ROWS:
                self.screen.blit(self.road_image, (i, row * CELL_SIZE))

        # Sidewalk
        for i in range(0, WIDTH, self.sidewalk_image.get_width()):
            for row in self.SIDEWALK_ROWS:
                self.screen.blit(self.sidewalk_image, (i, row * CELL_SIZE))

        self.cars.draw(self.screen)

        for player in self.players:
            if player.alive:
                self.screen.blit(player.image, player.rect.topleft)

        pygame.display.flip()
