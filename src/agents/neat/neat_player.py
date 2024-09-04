import pygame

from src.constants import CELL_SIZE
from src.entities.player import Player
from src.entities.train import Train


class NeatPlayer(Player):

    def get_state(self, obstacles: pygame.sprite.Group):
        sensor_data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        # Sensor Left (directly horizontal to the left)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y and obstacle.rect.x < self.rect.x:
                distance = (self.rect.x - obstacle.rect.x) / CELL_SIZE
                if distance <= 4:
                    sensor_data[0] = max(sensor_data[0], 1.0 - (distance * 0.25))

        # Sensor Right (directly horizontal to the right)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y and obstacle.rect.x > self.rect.x:
                distance = (obstacle.rect.x - self.rect.x) / CELL_SIZE
                if distance <= 4:
                    sensor_data[1] = max(sensor_data[1], 1.0 - (distance * 0.25))

        # Sensor Top-Left (one row above, to the left)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y - CELL_SIZE and obstacle.rect.x < self.rect.x:
                distance = (self.rect.x - obstacle.rect.x) / CELL_SIZE
                if distance <= 4:
                    sensor_data[2] = max(sensor_data[2], 1.0 - (distance * 0.25))

        # Sensor Top-Right (one row above, to the right)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y - CELL_SIZE and obstacle.rect.x > self.rect.x:
                distance = (obstacle.rect.x - self.rect.x) / CELL_SIZE
                if distance <= 4:
                    sensor_data[3] = max(sensor_data[3], 1.0 - (distance * 0.25))

        # Sensor Bottom-Left (one row above, to the left)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y + CELL_SIZE and obstacle.rect.x < self.rect.x:
                distance = (self.rect.x - obstacle.rect.x) / CELL_SIZE
                if distance <= 4:
                    sensor_data[4] = max(sensor_data[2], 1.0 - (distance * 0.25))

        # Sensor Bottom-Right (one row above, to the right)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y + CELL_SIZE and obstacle.rect.x > self.rect.x:
                distance = (obstacle.rect.x - self.rect.x) / CELL_SIZE
                if distance <= 4:
                    sensor_data[5] = max(sensor_data[3], 1.0 - (distance * 0.25))

        # Center Sensor (three squares directly in front of the frog)
        direction = self.direction
        if direction == 0:  # Facing Left
            for obstacle in obstacles:
                if obstacle.rect.y == self.rect.y and 0 < self.rect.x - obstacle.rect.x <= 3 * CELL_SIZE:
                    sensor_data[6] = 1.0
                    break
        elif direction == 1:  # Facing Right
            for obstacle in obstacles:
                if obstacle.rect.y == self.rect.y and 0 < obstacle.rect.x - self.rect.x <= 3 * CELL_SIZE:
                    sensor_data[6] = 1.0
                    break
        elif direction == 2:  # Facing Up
            for obstacle in obstacles:
                if obstacle.rect.x == self.rect.x and 0 < self.rect.y - obstacle.rect.y <= 3 * CELL_SIZE:
                    sensor_data[6] = 1.0
                    break
        elif direction == 3:  # Facing Down
            for obstacle in obstacles:
                if obstacle.rect.x == self.rect.x and 0 < obstacle.rect.y - self.rect.y <= 3 * CELL_SIZE:
                    sensor_data[6] = 1.0
                    break

        for obstacle in obstacles:
            if isinstance(obstacle, Train) and obstacle.active:
                sensor_data[7] = 1.0
                sensor_data[8] = abs((obstacle.rect.y - self.rect.y) / CELL_SIZE)
                sensor_data[9] = pygame.time.get_ticks() - obstacle.time_since_death

        return sensor_data
