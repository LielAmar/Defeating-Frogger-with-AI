import torch
from torch import nn


class DQNModel(nn.Module):
    def __init__(self, state_dim: int = 256, action_dim: int = 5):
        super(DQNModel, self).__init__()

        # 16x16 grid, apply conv with kernel size 5 -> 12x12 grid -> apply conv with kernel size 5 -> 8x8 grid

        self.fc1 = nn.Conv2d(1, 1, kernel_size=5, stride=1).to(device='cpu')
        self.fc2 = nn.Conv2d(1, 1, kernel_size=5, stride=1).to(device='cpu')
        self.fc3 = nn.Linear(64, action_dim).to(device='cpu')

    def forward(self, state):
        # Change the state from batch_size x w x h to batch_size x (w * h)
        # state = state.view(state.size(0), -1)
        # add a channel dimension
        state = state.unsqueeze(1)

        x = torch.relu(self.fc1(state))
        x = torch.relu(self.fc2(x))
        x = x.view(x.size(0), -1)
        return self.fc3(x)
