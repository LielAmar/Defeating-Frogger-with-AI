import random
import sys
from abc import ABC, abstractmethod
from typing import Literal

import pygame

from src.constants import WIDTH, HEIGHT, BLACK, CARS_PER_ROW, CELL_SIZE, LOGS_PER_ROW
from src.entities.car import Car
from src.entities.log import Log
from src.entities.player import Player
from src.entities.train import Train


class FroggerGame(ABC):
    CAR_ROWS: list[tuple[int, Literal[1, -1]]] = [
        (9, -1),
        (10, 1),
        (11, -1),
        (12, 1)
    ]

    LOG_ROWS: list[tuple[int, Literal[1, -1]]] = [
        (2, 1),
        (3, -1),
        (4, 1),
        (5, -1),
    ]

    TRAIN_ROWS: list[tuple[int, Literal[1, -1]]] = [
        (7, 1)
    ]

    FINISH_ROWS: list[tuple[int, Literal[1, -1]]] = [
        (0, -1)
    ]
    GRASS_ROWS: list[tuple[int, Literal[1, -1]]] = [
        (13, -1),
        (14, -1),
        (15, -1)
    ]
    SIDEWALK_ROWS: list[tuple[int, Literal[1, -1]]] = [
        (1, -1),
        (6, -1),
        (8, -1)
    ]

    def __init__(self, settings):
        self.settings = settings

        if not settings.with_water:
            self.CAR_ROWS = self.CAR_ROWS + self.LOG_ROWS
            self.LOG_ROWS = []

        if not settings.with_train:
            self.SIDEWALK_ROWS = self.SIDEWALK_ROWS + self.TRAIN_ROWS
            self.TRAIN_ROWS = []

        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption("Frogger Game")

        self.clock = pygame.time.Clock()

        self.road_image = pygame.image.load('assets/road.png')
        self.rail_image = pygame.image.load('assets/rail.png')
        self.grass_image = pygame.image.load('assets/grass.png')
        self.finish_image = pygame.image.load('assets/finish.png')
        self.sidewalk_image = pygame.image.load('assets/sidewalk.png')
        self.water_image = pygame.image.load('assets/water.png')

        self.road_image = pygame.transform.scale(
            self.road_image,
            ((CELL_SIZE / self.road_image.get_height()) * self.road_image.get_width(), CELL_SIZE)
        )
        self.rail_image = pygame.transform.scale(
            self.rail_image,
            ((CELL_SIZE / self.rail_image.get_height()) * self.rail_image.get_width(), CELL_SIZE)
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
        self.water_image = pygame.transform.scale(
            self.water_image,
            ((CELL_SIZE / self.water_image.get_height()) * self.water_image.get_width(), CELL_SIZE)
        )

        self.obstacles = pygame.sprite.Group()
        self.logs = pygame.sprite.Group()
        self.players = []

        self.reset()

    def reset(self):
        self.obstacles.empty()
        self.logs.empty()

        self._create_cars()
        self._create_train()
        self._create_logs()

        self.players = []

    def _create_cars(self):
        for row, direction in self.CAR_ROWS:
            offset = random.randint(3, 8)
            second_offset = random.randint(0, 6)

            for i in range(CARS_PER_ROW):
                car = Car((i * offset + second_offset) * CELL_SIZE, row * CELL_SIZE, direction, self.settings.grid_like)
                self.obstacles.add(car)

    def _create_logs(self):
        for row, direction in self.LOG_ROWS:
            offset = random.randint(1, 3)

            for i in range(LOGS_PER_ROW):
                log = Log((i * 4 + offset) * CELL_SIZE, row * CELL_SIZE, direction, self.settings.grid_like)
                self.logs.add(log)

    def _create_train(self):
        for row, direction in self.TRAIN_ROWS:
            train = Train(0, row * CELL_SIZE)
            train.active = False
            train.reset()
            self.obstacles.add(train)

    def _draw(self):
        self.screen.fill(BLACK)

        self._draw_background()

        self.obstacles.draw(self.screen)
        self.logs.draw(self.screen)

        self._draw_players(alive_only=True)

        pygame.display.flip()

    def _draw_background(self):
        for row, direction in self.FINISH_ROWS:
            for i in range(0, WIDTH, self.finish_image.get_width()):
                self.screen.blit(self.finish_image, (i, row * CELL_SIZE))

        for row, direction in self.GRASS_ROWS:
            for i in range(0, WIDTH, self.grass_image.get_width()):
                self.screen.blit(self.grass_image, (i, row * CELL_SIZE))

        for row, direction in self.SIDEWALK_ROWS:
            for i in range(0, WIDTH, self.sidewalk_image.get_width()):
                self.screen.blit(self.sidewalk_image, (i, row * CELL_SIZE))

        for row, direction in self.CAR_ROWS:
            for i in range(0, WIDTH, self.road_image.get_width()):
                self.screen.blit(self.road_image, (i, row * CELL_SIZE))

        for row, direction in self.TRAIN_ROWS:
            if self.settings.with_train:
                for i in range(0, WIDTH, self.rail_image.get_width()):
                    self.screen.blit(self.rail_image, (i, row * CELL_SIZE))
            else:
                for i in range(0, WIDTH, self.sidewalk_image.get_width()):
                    self.screen.blit(self.sidewalk_image, (i, row * CELL_SIZE))

        for row, direction in self.LOG_ROWS:
            if self.settings.with_water:
                for i in range(0, WIDTH, self.water_image.get_width()):
                    self.screen.blit(self.water_image, (i, row * CELL_SIZE))
            else:
                for i in range(0, WIDTH, self.road_image.get_width()):
                    self.screen.blit(self.road_image, (i, row * CELL_SIZE))

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

    def update_player(self, player, direction):
        player.update(direction)

        # If the player died to a car, kill it
        if pygame.sprite.spritecollideany(player, self.obstacles):
            player.alive = False

        # If the player is out of steps, kill it
        if player.steps == 0:
            player.alive = False

        # If the player reached the top, mark it as won and give it a fitness boost
        if player.rect.y <= 0:
            player.alive = False
            player.won = True

        # if there isn't a log under the player, kill it
        if self.settings.with_water:
            for water_row, direction in self.LOG_ROWS:
                if player.rect.y == water_row * CELL_SIZE:
                    logs_player_on = [log for log in self.logs if
                                      log.rect.y == water_row * CELL_SIZE and log.rect.x < player.rect.x < log.rect.x + log.rect.width]
                    if not any(logs_player_on):
                        player.alive = False
                    else:
                        for log in logs_player_on:
                            player.rect.x += log.direction * (CELL_SIZE if self.settings.grid_like else Log.SPEED)
                            player.rect.x = max(0, min(player.rect.x, WIDTH - CELL_SIZE))

    def run_single_game_frame(self):
        self.clock.tick(self.settings.fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.obstacles.update()
        self.logs.update()

        self.update_game_frame()

        self._draw()

        return any(player.alive for player in self.players)
