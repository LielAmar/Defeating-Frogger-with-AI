import pygame

from src.constants import CELL_SIZE
from src.entities.player import Player


class NeatPlayer(Player):

    def get_state(self, cars: pygame.sprite.Group):
        sensor_data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

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

        # Sensor Bottom-Left (one row above, to the left)
        for car in cars:
            if car.rect.y == self.rect.y + CELL_SIZE and car.rect.x < self.rect.x:
                distance = (self.rect.x - car.rect.x) / CELL_SIZE
                if distance <= 4:
                    sensor_data[4] = max(sensor_data[2], 1.0 - (distance * 0.25))

        # Sensor Bottom-Right (one row above, to the right)
        for car in cars:
            if car.rect.y == self.rect.y + CELL_SIZE and car.rect.x > self.rect.x:
                distance = (car.rect.x - self.rect.x) / CELL_SIZE
                if distance <= 4:
                    sensor_data[5] = max(sensor_data[3], 1.0 - (distance * 0.25))

        # Center Sensor (three squares directly in front of the frog)
        direction = self.direction
        if direction == 0:  # Facing Left
            for car in cars:
                if car.rect.y == self.rect.y and 0 < self.rect.x - car.rect.x <= 3 * CELL_SIZE:
                    sensor_data[6] = 1.0
                    break
        elif direction == 1:  # Facing Right
            for car in cars:
                if car.rect.y == self.rect.y and 0 < car.rect.x - self.rect.x <= 3 * CELL_SIZE:
                    sensor_data[6] = 1.0
                    break
        elif direction == 2:  # Facing Up
            for car in cars:
                if car.rect.x == self.rect.x and 0 < self.rect.y - car.rect.y <= 3 * CELL_SIZE:
                    sensor_data[6] = 1.0
                    break
        elif direction == 3:  # Facing Down
            for car in cars:
                if car.rect.x == self.rect.x and 0 < car.rect.y - self.rect.y <= 3 * CELL_SIZE:
                    sensor_data[6] = 1.0
                    break

        return sensor_data
