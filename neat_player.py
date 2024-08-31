import pygame

from constants import CELL_SIZE, WIDTH, HEIGHT, NEAT_MAX_STEPS
from utils import crop_image


class NeatPlayer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.game_id = 0
        self.fitnesses = []

        # Load player image from assets/player.png to be of size CELL_SIZE x CELL_SIZE and crop using utils.crop
        self.image = pygame.transform.scale(
            crop_image(pygame.image.load(f'assets/player.png').convert_alpha()),
            (CELL_SIZE, CELL_SIZE)
        )

        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.x = WIDTH // 2 - CELL_SIZE // 2
        self.rect.y = HEIGHT - CELL_SIZE
        self.alive = True
        self.direction = 2  # Default direction is Up
        self.steps = NEAT_MAX_STEPS

    def update(self, direction):
        self.direction = direction  # Update the direction based on the movement
        self.steps -= 1  # Increment the step counter

        if direction == 0:  # Move Left
            self.rect.x -= CELL_SIZE
        elif direction == 1:  # Move Right
            self.rect.x += CELL_SIZE
        elif direction == 2:  # Move Up
            self.rect.y -= CELL_SIZE
        elif direction == 3:  # Move Down
            self.rect.y += CELL_SIZE

        # Keep the player within bounds
        self.rect.x = max(0, min(self.rect.x, WIDTH - CELL_SIZE))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - CELL_SIZE))

    def get_data(self, cars):
        # Initialize sensor data with default values
        sensor_data = [0.0, 0.0, 0.0, 0.0, 0.0]  # Left, Right, Top-Left, Top-Right, Center

        # Sensor Left (directly horizontal to the left)
        for car in cars:
            if car.rect.y == self.rect.y and car.rect.x < self.rect.x:
                distance = (self.rect.x - car.rect.x) / CELL_SIZE
                if distance <= 4:
                    sensor_data[0] = max(sensor_data[0], 1.0 - (distance * 0.25))

        # Sensor Right (directly horizontal to the right)
        for car in cars:
            if car.rect.y == self.rect.y and car.rect.x > self.rect.x:
                distance = (car.rect.x - self.rect.x) / CELL_SIZE
                if distance <= 4:
                    sensor_data[1] = max(sensor_data[1], 1.0 - (distance * 0.25))

        # Sensor Top-Left (one row above, to the left)
        for car in cars:
            if car.rect.y == self.rect.y - CELL_SIZE and car.rect.x < self.rect.x:
                distance = (self.rect.x - car.rect.x) / CELL_SIZE
                if distance <= 4:
                    sensor_data[2] = max(sensor_data[2], 1.0 - (distance * 0.25))

        # Sensor Top-Right (one row above, to the right)
        for car in cars:
            if car.rect.y == self.rect.y - CELL_SIZE and car.rect.x > self.rect.x:
                distance = (car.rect.x - self.rect.x) / CELL_SIZE
                if distance <= 4:
                    sensor_data[3] = max(sensor_data[3], 1.0 - (distance * 0.25))

        # Center Sensor (three squares directly in front of the frog)
        direction = self.direction
        if direction == 0:  # Facing Left
            for car in cars:
                if car.rect.y == self.rect.y and 0 < self.rect.x - car.rect.x <= 3 * CELL_SIZE:
                    sensor_data[4] = 1.0
                    break
        elif direction == 1:  # Facing Right
            for car in cars:
                if car.rect.y == self.rect.y and 0 < car.rect.x - self.rect.x <= 3 * CELL_SIZE:
                    sensor_data[4] = 1.0
                    break
        elif direction == 2:  # Facing Up
            for car in cars:
                if car.rect.x == self.rect.x and 0 < self.rect.y - car.rect.y <= 3 * CELL_SIZE:
                    sensor_data[4] = 1.0
                    break
        elif direction == 3:  # Facing Down
            for car in cars:
                if car.rect.x == self.rect.x and 0 < car.rect.y - self.rect.y <= 3 * CELL_SIZE:
                    sensor_data[4] = 1.0
                    break

        return sensor_data