import numpy as np
import pygame
from pygame.sprite import Sprite
from constants import WIDTH, HEIGHT, CELL_SIZE, NEAT_MAX_STEPS
from dqn_agent import DQNAgent
import random

class DQNPlayer(Sprite):
    def __init__(self, state_size, action_size):
        super().__init__()

        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - CELL_SIZE // 2
        self.rect.y = HEIGHT - CELL_SIZE
        self.state_size = state_size
        self.action_size = action_size
        self.agent = DQNAgent(state_size, action_size)
        self.alive = True

        self.steps = NEAT_MAX_STEPS

    def get_state(self, cars):
        state = np.zeros(self.state_size)
        state[0] = self.rect.x / WIDTH
        state[1] = self.rect.y / HEIGHT
        for i, car in enumerate(cars):
            if i < (self.state_size - 2) // 2:
                state[2 + 2 * i] = car.rect.x / WIDTH
                state[3 + 2 * i] = car.rect.y / HEIGHT
        return state

    def get_action(self, state):
        return random.randint(0, self.action_size - 1)
        # action = self.agent.act(state)

    def update(self, action):
        if not self.alive:
            return

        self.steps -= 1

        if action == 0:  # Left
            self.rect.x -= CELL_SIZE
        elif action == 1:  # Right
            self.rect.x += CELL_SIZE
        elif action == 2:  # Up
            self.rect.y -= CELL_SIZE
        elif action == 3:  # Down
            self.rect.y += CELL_SIZE

        # Keep player within bounds
        self.rect.x = max(0, min(self.rect.x, WIDTH - CELL_SIZE))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - CELL_SIZE))

    def remember(self, state, action, reward, next_state, done):
        self.agent.remember(state, action, reward, next_state, done)

    def replay(self):
        self.agent.replay()
