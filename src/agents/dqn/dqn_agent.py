import random
from argparse import Namespace
from collections import deque

import numpy as np
import torch
from torch import optim, nn

from src.agents.dqn.dqn_model import DQNModel


class DQNAgent:
    def __init__(self, settings: Namespace, state_dim: int = 256, action_dim: int = 5):
        self.settings = settings

        self.state_dim = state_dim
        self.action_dim = action_dim

        self.memory = deque(maxlen=20000)

        self.gamma = 0.99  # Discount factor
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.999

        self.batch_size = 128
        self.learning_rate = 0.0001

        self.model = DQNModel(state_dim, action_dim)
        self.target_model = DQNModel(state_dim, action_dim)
        self.update_target_model()

        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        self.criterion = nn.MSELoss()

    def update_learning_rate(self):
        for param_group in self.optimizer.param_groups:
            param_group['lr'] = param_group['lr'] / 10

    def update_target_model(self):
        self.target_model.load_state_dict(self.model.state_dict())

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state) -> int:
        if self.settings.test is None:
            if random.random() <= self.epsilon:
                return random.randint(0, self.action_dim - 1)

        state = torch.FloatTensor(state).unsqueeze(0).to(device='cpu')

        with torch.no_grad():
            q_values = self.model(state)

        return np.argmax(q_values.cpu().data.numpy())

    def replay(self):
        if len(self.memory) < self.batch_size:
            return

        minibatch = random.sample(self.memory, self.batch_size)

        for state, action, reward, next_state, done in minibatch:
            state = torch.FloatTensor(state).unsqueeze(0).to(device='cpu')
            next_state = torch.FloatTensor(next_state).unsqueeze(0).to(device='cpu')

            target = reward

            if not done:
                target = reward + self.gamma * torch.max(self.target_model(next_state)[0])

            # TODO - check with debug
            target_f = self.model(state)
            target_f[0][action] = target

            self.optimizer.zero_grad()

            loss = self.criterion(target_f, self.model(state))
            loss.backward()

            self.optimizer.step()

        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
