from src.entities.player import Player


class HumanPlayer(Player):

    def __init__(self):
        super().__init__()

        self.steps = 10000
