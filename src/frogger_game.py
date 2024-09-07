import random
import sys
from abc import ABC, abstractmethod
from argparse import Namespace

import pygame

from src.agents.dqn.dqn_player import DQNPlayer
from src.constants import WIDTH, HEIGHT, BLACK, CARS_PER_ROW, CELL_SIZE, LOGS_PER_ROW, CAR_ROWS, WATER_ROWS, \
    SIDEWALK_ROWS, TRAIN_ROWS, GRASS_ROWS, FINISH_ROWS
from src.direction import Direction
from src.entities.car import Car
from src.entities.log import Log
from src.entities.player import Player
from src.entities.train import Train


class FroggerGame(ABC):
    """
    Abstract class for the Frogger Game
    """

    def __init__(self, settings: Namespace):
        self.settings = settings

        self.settings.new_fps = self.settings.fps

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
            self.GRASS_ROWS = self.GRASS_ROWS + self.TRAIN_ROWS
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
        """
        Reset the game.
        """

        self.obstacles.empty()
        self.logs.empty()

        self._create_cars()
        self._create_train()
        self._create_logs()

        self.players = []

    def _create_cars(self):
        """
        Create all the cars in the game
        """

        for row, direction in self.CAR_ROWS:
            offset = random.randint(3, 8)
            second_offset = random.randint(0, 6)

            for i in range(CARS_PER_ROW):
                car = Car((i * offset + second_offset) * CELL_SIZE, row * CELL_SIZE, self.settings, direction)
                self.obstacles.add(car)

    def _create_train(self):
        """
        Create all the trains in the game
        """

        for row, direction in self.TRAIN_ROWS:
            train = Train(0, row * CELL_SIZE, self.settings, direction)
            train.active = False
            train.reset()
            self.obstacles.add(train)

    def _create_logs(self):
        """
        Create all the logs in the game
        """

        for row, direction in self.WATER_ROWS:
            offset = random.randint(1, 3)

            for i in range(LOGS_PER_ROW):
                log = Log((i * 4 + offset) * CELL_SIZE, row * CELL_SIZE, self.settings, direction)
                self.logs.add(log)

    def _draw(self):
        """
        Draw the game
        """

        self.screen.fill(BLACK)

        self._draw_background()

        self.obstacles.draw(self.screen)
        self.logs.draw(self.screen)

        self._draw_players(alive_only=True)

        if self.settings.debug:
            state = self.players[0].get_state(self.obstacles)

            def calc_dist(dist):
                if abs(dist - 1) <= 0.01:
                    return 1

                if abs(dist - 0.8) <= 0.01:
                    return 2

                if abs(dist - 0.6) <= 0.01:
                    return 3

                if abs(dist - 0.4) <= 0.01:
                    return 4

                if abs(dist - 0.2) <= 0.01:
                    return 5

                return 0

            # take self.next_state and draw it on the screen
            left_side = calc_dist(state[0]) * CELL_SIZE
            right_side = calc_dist(state[1]) * CELL_SIZE
            up_side = calc_dist(state[2]) * CELL_SIZE
            down_side = calc_dist(state[3]) * CELL_SIZE
            top_left = calc_dist(state[4]) * CELL_SIZE
            top_right = calc_dist(state[5]) * CELL_SIZE
            bottom_left = calc_dist(state[6]) * CELL_SIZE
            bottom_right = calc_dist(state[7]) * CELL_SIZE
            top_top_left = calc_dist(state[8]) * CELL_SIZE
            top_top_right = calc_dist(state[9]) * CELL_SIZE
            bottom_bottom_left = calc_dist(state[10]) * CELL_SIZE
            bottom_bottom_right = calc_dist(state[11]) * CELL_SIZE
            steps = state[12]

            player_x = self.players[0].rect.x
            player_y = self.players[0].rect.y

            rect_width = CELL_SIZE
            rect_height = CELL_SIZE

            if left_side != 0:
                pygame.draw.rect(self.screen, (255, 0, 0), (player_x + left_side, player_y, rect_width, rect_height))

            if right_side != 0:
                pygame.draw.rect(self.screen, (0, 255, 0), (player_x + right_side, player_y, rect_width, rect_height))

            if up_side != 0:
                pygame.draw.rect(self.screen, (0, 0, 255), (player_x, player_y - up_side, rect_width, rect_height))

            if down_side != 0:
                pygame.draw.rect(self.screen, (255, 255, 0), (player_x, player_y + down_side, rect_width, rect_height))

        pygame.display.flip()

    def _draw_background(self):
        """
        Draw the background of the game
        """

        self._draw_segment(self.FINISH_ROWS, self.finish_image)
        self._draw_segment(self.GRASS_ROWS, self.grass_image)
        self._draw_segment(self.SIDEWALK_ROWS, self.sidewalk_image)
        self._draw_segment(self.CAR_ROWS, self.road_image)
        self._draw_segment(self.TRAIN_ROWS, self.rail_image)
        self._draw_segment(self.WATER_ROWS, self.water_image)

    def _draw_segment(self, rows, image):
        """"
        Draw a specific segment of the game background
        """

        for row, direction in rows:
            for i in range(0, WIDTH, image.get_width()):
                self.screen.blit(image, (i, row * CELL_SIZE))

    def _draw_players(self, alive_only: bool = True):
        """
        Draw the players

        :param alive_only: Whether to draw only the alive players
        """

        for player in self.players:
            if not alive_only or player.alive:
                self.screen.blit(player.image, player.rect.topleft)

    @abstractmethod
    def update_configuration(self, *args, **kwargs):
        """
        Update the configuration of the game

        :param args:
        :param kwargs:
        :return:
        """

        pass

    @abstractmethod
    def update_game_frame(self):
        """
        A method that can be used to update additional sprites in the game.

        :return:
        """

        pass

    def update_player(self, player: Player, direction: Direction):
        """
        Update a single player.
        This method is called by the game loop to update the player's position.
        It also checks if the player has reached the top of the screen or if it had died.

        :param player: Player to update
        :param direction: Direction to move the player
        """

        prev_x, prev_y = player.rect.x, player.rect.y

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

        for log in self.logs:
            log.player = None

        # if there isn't a log under the player, kill it
        for water_row, direction in self.WATER_ROWS:
            # If player in water
            if player.rect.y == water_row * CELL_SIZE:
                logs_player_on = [
                    log for log in self.logs if pygame.sprite.collide_rect(player, log)
                ]

                for log in logs_player_on:
                    log.player = player

                if not any(logs_player_on):
                    player.alive = False

    def run_single_game_frame(self):
        """
        Runs a single frame of the game.

        :return: True if the game is still running (any player is alive)
        """

        self.clock.tick(self.settings.new_fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.settings.new_fps = 5 if self.settings.new_fps != 5 else self.settings.fps

        self.obstacles.update()
        self.logs.update()

        self.update_game_frame()

        self._draw()

        return any(player.alive for player in self.players)

    @staticmethod
    def _load_background_asset(asset_file):
        """
        Load and scale a background asset

        :param asset_file: Path to the asset
        :return: Scaled asset
        """

        image = pygame.image.load(asset_file)

        return pygame.transform.scale(
            image,
            ((CELL_SIZE / image.get_height()) * image.get_width(), CELL_SIZE)
        )
