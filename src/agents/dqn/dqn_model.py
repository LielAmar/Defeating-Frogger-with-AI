import torch
from torch import nn


class DQNModel(nn.Module):
    def __init__(self, state_dim: int = 25, action_dim: int = 5):
        super(DQNModel, self).__init__()

        self.fc1 = nn.Linear(state_dim, 64).to(device='cpu')
        self.fc2 = nn.Linear(64, 64).to(device='cpu')
        self.fc3 = nn.Linear(64, action_dim).to(device='cpu')

    def forward(self, state):
        x = torch.relu(self.fc1(state))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)
