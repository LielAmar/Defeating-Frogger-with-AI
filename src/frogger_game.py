import random
import sys
from abc import ABC, abstractmethod
from argparse import Namespace

import pygame

from src.constants import WIDTH, HEIGHT, BLACK, CARS_PER_ROW, CELL_SIZE, LOGS_PER_ROW, CAR_ROWS, WATER_ROWS, \
    SIDEWALK_ROWS, TRAIN_ROWS, GRASS_ROWS, FINISH_ROWS
from src.direction import Direction
from src.entities.car import Car
from src.entities.log import Log
from src.entities.player import Player
from src.entities.train import Train


class FroggerGame(ABC):

    def __init__(self, settings: Namespace):
        self.settings = settings

        self.CAR_ROWS = CAR_ROWS
        self.WATER_ROWS = WATER_ROWS
        self.SIDEWALK_ROWS = SIDEWALK_ROWS
        self.TRAIN_ROWS = TRAIN_ROWS
        self.GRASS_ROWS = GRASS_ROWS
        self.FINISH_ROWS = FINISH_ROWS

        if not settings.water:
            self.CAR_ROWS = self.CAR_ROWS + self.WATER_ROWS
            self.WATER_ROWS = []

        if not settings.train:
            self.SIDEWALK_ROWS = self.SIDEWALK_ROWS + self.TRAIN_ROWS
            self.TRAIN_ROWS = []

        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption("Frogger Game")

        self.clock = pygame.time.Clock()

        self.road_image = self._load_background_asset('assets/road.png')
        self.rail_image = self._load_background_asset('assets/rail.png')
        self.grass_image = self._load_background_asset('assets/grass.png')
        self.finish_image = self._load_background_asset('assets/finish.png')
        self.sidewalk_image = self._load_background_asset('assets/sidewalk.png')
        self.water_image = self._load_background_asset('assets/water.png')

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
                car = Car((i * offset + second_offset) * CELL_SIZE, row * CELL_SIZE, self.settings, direction)
                self.obstacles.add(car)

    def _create_train(self):
        for row, direction in self.TRAIN_ROWS:
            train = Train(0, row * CELL_SIZE, self.settings, direction)
            train.active = False
            train.reset()
            self.obstacles.add(train)

    def _create_logs(self):
        for row, direction in self.WATER_ROWS:
            offset = random.randint(1, 3)

            for i in range(LOGS_PER_ROW):
                log = Log((i * 4 + offset) * CELL_SIZE, row * CELL_SIZE, self.settings, direction)
                self.logs.add(log)

    def _draw(self):
        self.screen.fill(BLACK)

        self._draw_background()

        self.obstacles.draw(self.screen)
        self.logs.draw(self.screen)

        self._draw_players(alive_only=True)

        pygame.display.flip()

    def _draw_background(self):
        self._draw_segment(self.FINISH_ROWS, self.finish_image)
        self._draw_segment(self.GRASS_ROWS, self.grass_image)
        self._draw_segment(self.SIDEWALK_ROWS, self.sidewalk_image)
        self._draw_segment(self.CAR_ROWS, self.road_image)
        self._draw_segment(self.TRAIN_ROWS, self.rail_image)
        self._draw_segment(self.WATER_ROWS, self.water_image)

    def _draw_segment(self, rows, image):
        for row, direction in rows:
            for i in range(0, WIDTH, image.get_width()):
                self.screen.blit(image, (i, row * CELL_SIZE))

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

    def update_player(self, player: Player, direction: Direction):
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
        for water_row, direction in self.WATER_ROWS:
            if player.rect.y == water_row * CELL_SIZE:
                logs_player_on = [
                    log for log in self.logs
                    if log.rect.y == water_row * CELL_SIZE
                    and log.rect.x < player.rect.x < log.rect.x + log.rect.width
                ]

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

    @staticmethod
    def _load_background_asset(asset):
        image = pygame.image.load(asset)

        return pygame.transform.scale(
            image,
            ((CELL_SIZE / image.get_height()) * image.get_width(), CELL_SIZE)
        )
