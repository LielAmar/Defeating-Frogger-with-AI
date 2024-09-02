import random
import sys
from abc import ABC, abstractmethod
from typing import ClassVar, Literal

import pygame

from src.constants import WIDTH, HEIGHT, BLACK, CARS_PER_ROW, CELL_SIZE, FPS
from src.entities.car import Car
from src.entities.player import Player


class FroggerGame(ABC):

    CAR_ROWS: ClassVar[list[tuple[int, Literal[1, -1]]]] = [
        (2, 1),
        (3, -1),
        (4, 1),
        (5, -1),
        (9, -1),
        (10, 1),
        (11, -1),
        (12, 1)
    ]

    FINISH_ROWS: ClassVar = [0]
    GRASS_ROWS: ClassVar = [13, 14, 15]
    SIDEWALK_ROWS: ClassVar = [1, 6, 7, 8]

    def __init__(self, grid_like: bool = False):
        self.grid_like = grid_like

        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Frogger Game")

        self.clock = pygame.time.Clock()

        self.road_image = pygame.image.load('assets/road.png')
        self.grass_image = pygame.image.load('assets/grass.png')
        self.finish_image = pygame.image.load('assets/finish.png')
        self.sidewalk_image = pygame.image.load('assets/sidewalk.png')

        self.road_image = pygame.transform.scale(
            self.road_image,
            ((CELL_SIZE / self.road_image.get_height()) * self.road_image.get_width(), CELL_SIZE)
        )
        self.grass_image = pygame.transform.scale(
            self.grass_image,
            ((CELL_SIZE / self.grass_image.get_height()) * self.grass_image.get_width(), CELL_SIZE)
        )
        self.finish_image = pygame.transform.scale(
            self.finish_image,
            ((CELL_SIZE / self.finish_image.get_height()) * self.finish_image.get_width(), CELL_SIZE)
        )
        self.sidewalk_image = pygame.transform.scale(
            self.sidewalk_image,
            ((CELL_SIZE / self.sidewalk_image.get_height()) * self.sidewalk_image.get_width(), CELL_SIZE)
        )

        self.cars = None
        self.players = None

        self.reset()

    def reset(self):
        self.cars = self.create_cars()
        self.players = []

    def create_cars(self) -> pygame.sprite.Group:
        cars = pygame.sprite.Group()

        for row, direction in self.CAR_ROWS:
            offset = random.randint(3, 8)
            second_offset = random.randint(0, 6)

            for i in range(CARS_PER_ROW):
                car = Car((i * offset + second_offset) * CELL_SIZE, row * CELL_SIZE, direction, self.grid_like)
                cars.add(car)

        return cars

    def register_player(self, player: Player):
        self.players.add(player)

    def _draw(self):
        self.screen.fill(BLACK)

        self._draw_background()

        self.cars.draw(self.screen)

        self._draw_players(alive_only=True)

        pygame.display.flip()

    def _draw_background(self):
        for row in self.FINISH_ROWS:
            for i in range(0, WIDTH, self.finish_image.get_width()):
                self.screen.blit(self.finish_image, (i, row * CELL_SIZE))

        for row in self.GRASS_ROWS:
            for i in range(0, WIDTH, self.grass_image.get_width()):
                self.screen.blit(self.grass_image, (i, row * CELL_SIZE))

        for row, direction in self.CAR_ROWS:
            for i in range(0, WIDTH, self.road_image.get_width()):
                self.screen.blit(self.road_image, (i, row * CELL_SIZE))

        for row in self.SIDEWALK_ROWS:
            for i in range(0, WIDTH, self.sidewalk_image.get_width()):
                self.screen.blit(self.sidewalk_image, (i, row * CELL_SIZE))

    def _draw_players(self, alive_only: bool = True):
        for player in self.players:
            if not alive_only or player.alive:
                self.screen.blit(player.image, player.rect.topleft)

    @abstractmethod
    def update_configuration(self, *args, **kwargs):
        pass

    @abstractmethod
    def update_game_frame(self):
        pass

    def run_single_game_frame(self):
        self.clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.cars.update()

        self.update_game_frame()

        self._draw()

        return any(player.alive for player in self.players)
