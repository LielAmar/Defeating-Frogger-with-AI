import pygame

from src.constants import CELL_SIZE
from src.entities.player import Player


class NeatPlayer(Player):

    MAX_DISTANCE = 5

    def get_state(self, obstacles: pygame.sprite.Group):
        state = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        # Sensor Left (directly horizontal to the left)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y and obstacle.rect.x < self.rect.x:
                distance = (self.rect.x - obstacle.rect.x) / CELL_SIZE
                if distance <= self.MAX_DISTANCE:
                    state[0] = max(state[0], 1.0 - (distance * (1 / self.MAX_DISTANCE)))

        # Sensor Right (directly horizontal to the right)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y and obstacle.rect.x > self.rect.x:
                distance = (obstacle.rect.x - self.rect.x) / CELL_SIZE
                if distance <= self.MAX_DISTANCE:
                    state[1] = max(state[1], 1.0 - (distance * (1 / self.MAX_DISTANCE)))

        # Sensor Up (directly vertical above)
        for obstacle in obstacles:
            if obstacle.rect.x == self.rect.x and obstacle.rect.y < self.rect.y:
                distance = (self.rect.y - obstacle.rect.y) / CELL_SIZE
                if distance <= self.MAX_DISTANCE:
                    state[2] = max(state[2], 1.0 - (distance * (1 / self.MAX_DISTANCE)))

        # Sensor Down (directly vertical below)
        for obstacle in obstacles:
            if obstacle.rect.x == self.rect.x and obstacle.rect.y > self.rect.y:
                distance = (obstacle.rect.y - self.rect.y) / CELL_SIZE
                if distance <= self.MAX_DISTANCE:
                    state[3] = max(state[3], 1.0 - (distance * (1 / self.MAX_DISTANCE)))

        # Sensor Top-Left (one row above, to the left)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y - CELL_SIZE and obstacle.rect.x < self.rect.x:
                distance = (self.rect.x - obstacle.rect.x) / CELL_SIZE
                if distance <= self.MAX_DISTANCE:
                    state[4] = max(state[2], 1.0 - (distance * (1 / self.MAX_DISTANCE)))

        # Sensor Top-Right (one row above, to the right)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y - CELL_SIZE and obstacle.rect.x > self.rect.x:
                distance = (obstacle.rect.x - self.rect.x) / CELL_SIZE
                if distance <= self.MAX_DISTANCE:
                    state[5] = max(state[3], 1.0 - (distance * (1 / self.MAX_DISTANCE)))

        # Sensor Bottom-Left (one row below, to the left)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y + CELL_SIZE and obstacle.rect.x < self.rect.x:
                distance = (self.rect.x - obstacle.rect.x) / CELL_SIZE
                if distance <= self.MAX_DISTANCE:
                    state[6] = max(state[2], 1.0 - (distance * (1 / self.MAX_DISTANCE)))

        # Sensor Bottom-Right (one row below, to the right)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y + CELL_SIZE and obstacle.rect.x > self.rect.x:
                distance = (obstacle.rect.x - self.rect.x) / CELL_SIZE
                if distance <= self.MAX_DISTANCE:
                    state[7] = max(state[3], 1.0 - (distance * (1 / self.MAX_DISTANCE)))

        # Sensor Top-Top-Left (one row above, to the left)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y - CELL_SIZE * 2 and obstacle.rect.x < self.rect.x:
                distance = (self.rect.x - obstacle.rect.x) / CELL_SIZE
                if distance <= self.MAX_DISTANCE:
                    state[8] = max(state[2], 1.0 - (distance * (1 / self.MAX_DISTANCE)))

        # Sensor Top-Top-Right (one row above, to the right)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y - CELL_SIZE * 2 and obstacle.rect.x > self.rect.x:
                distance = (obstacle.rect.x - self.rect.x) / CELL_SIZE
                if distance <= self.MAX_DISTANCE:
                    state[9] = max(state[3], 1.0 - (distance * (1 / self.MAX_DISTANCE)))

        # Sensor Bottom-Bottom-Left (one row below, to the left)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y + CELL_SIZE * 2 and obstacle.rect.x < self.rect.x:
                distance = (self.rect.x - obstacle.rect.x) / CELL_SIZE
                if distance <= self.MAX_DISTANCE:
                    state[10] = max(state[2], 1.0 - (distance * (1 / self.MAX_DISTANCE)))

        # Sensor Bottom-Bottom-Right (one row below, to the right)
        for obstacle in obstacles:
            if obstacle.rect.y == self.rect.y + CELL_SIZE * 2 and obstacle.rect.x > self.rect.x:
                distance = (obstacle.rect.x - self.rect.x) / CELL_SIZE
                if distance <= self.MAX_DISTANCE:
                    state[11] = max(state[3], 1.0 - (distance * (1 / self.MAX_DISTANCE)))

        # Center Sensor (three squares directly in front of the frog)
        # direction = self.direction
        # if direction == 0:  # Facing Left
        #     for obstacle in obstacles:
        #         if obstacle.rect.y == self.rect.y and 0 < self.rect.x - obstacle.rect.x <= 3 * CELL_SIZE:
        #             sensor_data[6] = 1.0
        #             break
        # elif direction == 1:  # Facing Right
        #     for obstacle in obstacles:
        #         if obstacle.rect.y == self.rect.y and 0 < obstacle.rect.x - self.rect.x <= 3 * CELL_SIZE:
        #             sensor_data[6] = 1.0
        #             break
        # elif direction == 2:  # Facing Up
        #     for obstacle in obstacles:
        #         if obstacle.rect.x == self.rect.x and 0 < self.rect.y - obstacle.rect.y <= 3 * CELL_SIZE:
        #             sensor_data[6] = 1.0
        #             break
        # elif direction == 3:  # Facing Down
        #     for obstacle in obstacles:
        #         if obstacle.rect.x == self.rect.x and 0 < obstacle.rect.y - self.rect.y <= 3 * CELL_SIZE:
        #             sensor_data[6] = 1.0
        #             break

        return state
