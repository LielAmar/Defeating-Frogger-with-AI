import torch
from torch import nn


class DQNModel(nn.Module):
    def __init__(self, state_dim: int, action_dim: int):
        super(DQNModel, self).__init__()

        self.fc1 = nn.Linear(state_dim, 64).to(device='cuda')
        self.fc2 = nn.Linear(64, 64).to(device='cuda')
        self.fc3 = nn.Linear(64, action_dim).to(device='cuda')

    def forward(self, state):
        x = torch.relu(self.fc1(state))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)
