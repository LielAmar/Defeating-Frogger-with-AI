import math
from datetime import datetime, timedelta
import random
import numpy as np

import pygame
import sys
import os
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

from collections import deque

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 16
CELL_SIZE = 40
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 60
ACTION_SPACE = 4

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frogger Game")

# Clock to control the frame rate
clock = pygame.time.Clock()

CAR_ROWS = [
    (2, 0),
    (3, 2),
    (4, 4),
    (5, 3),
    (6, 1),
    (8, 0),
    (9, 4),
    (10, 3),
    (11, 0),
    (12, 2)
]

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - CELL_SIZE // 2
        self.rect.y = HEIGHT - CELL_SIZE
        self.alive = True
        self.direction = 2  # Default direction is Up
        self.steps = 0  # Initialize step counter

    def update(self, direction):
        self.direction = direction  # Update the direction based on the movement
        self.steps += 1  # Increment the step counter

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

    def get_state(self, cars):
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

        return np.array(sensor_data)


# Car class
class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.x += CELL_SIZE
        if self.rect.x > WIDTH:
            self.rect.x = -self.rect.width


# Define the Q-Network
class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_size, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, action_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)


# Implement Replay Buffer
class ReplayBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = []
        self.position = 0

    def push(self, state, action, reward, next_state, done):
        if len(self.buffer) < self.capacity:
            self.buffer.append(None)
        self.buffer[self.position] = (state, action, reward, next_state, done)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)

    def __len__(self):
        return len(self.buffer)


# DQN Agent
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # Discount factor
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.batch_size = 32
        self.policy_net = self._build_model()
        self.target_net = self._build_model()
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=self.learning_rate)
        self.update_target_network()  # Initialize target net with the same weights as policy net

    def _build_model(self):
        model = nn.Sequential(
            nn.Linear(self.state_size, 24),
            nn.ReLU(),
            nn.Linear(24, 24),
            nn.ReLU(),
            nn.Linear(24, self.action_size)
        )
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        state = torch.FloatTensor(state)
        with torch.no_grad():
            act_values = self.policy_net(state)
        return np.argmax(act_values.numpy())

    def replay(self):
        if len(self.memory) < self.batch_size:
            return

        batch = random.sample(self.memory, self.batch_size)
        state, action, reward, next_state, done = zip(*batch)

        state = torch.FloatTensor(state)
        action = torch.LongTensor(action).unsqueeze(1)
        reward = torch.FloatTensor(reward)
        next_state = torch.FloatTensor(next_state)
        done = torch.FloatTensor(done)

        # Get the current Q-values
        q_values = self.policy_net(state).gather(1, action)

        # Get the max Q-value for the next state from the target network
        next_q_values = self.target_net(next_state).max(1)[0].detach()

        # Compute the target Q-value
        expected_q_values = reward + (self.gamma * next_q_values * (1 - done))

        # Compute loss
        loss = nn.MSELoss()(q_values, expected_q_values.unsqueeze(1))

        # Optimize the model
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Epsilon decay
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_target_network(self):
        self.target_net.load_state_dict(self.policy_net.state_dict())


# Create sprite groups
cars = pygame.sprite.Group()

for row, offset in CAR_ROWS:
    for i in range(3):
        car = Car((i * 6 + offset) * CELL_SIZE, row * CELL_SIZE, 1)
        cars.add(car)


# Main training loop
def train_dqn():
    state_size = 5  # Number of inputs from get_state()
    action_size = ACTION_SPACE  # Number of possible actions (4 directions)
    agent = DQNAgent(state_size, action_size)

    episodes = 1000

    for e in range(episodes):
        player = Player()
        state = player.get_state(cars)
        total_reward = 0
        steps = 0

        while True:
            clock.tick(FPS)  # maybe at last

            # Agent chooses action
            action = agent.act(state)
            player.update(action)

            # Environment updates
            cars.update()
            next_state = player.get_state(cars)

            # Calculate reward
            reward = -1  # Penalize every step taken TODO: change
            if pygame.sprite.spritecollideany(player, cars):
                reward = -100  # Collision with car
                player.alive = False
            elif player.rect.y <= 0:
                reward = 100  # Reached the goal
                player.alive = False

            done = not player.alive
            total_reward += reward
            agent.remember(state, action, reward, next_state, done)

            state = next_state
            steps += 1

            if done or steps > 200:
                print(f"Episode: {e}/{episodes}, Total Reward: {total_reward}, Epsilon: {agent.epsilon:.2f}")
                break

            # Training step
            agent.replay()

        agent.update_target_network()

        if e % 10 == 0:
            plt.clf()
            plt.title("DQN Training")
            plt.xlabel("Episode")
            plt.ylabel("Total Reward")
            plt.plot(total_reward, label="Total Reward")
            plt.pause(0.1)  # Brief pause to update the plot

    plt.show()


if __name__ == "__main__":
    train_dqn()
