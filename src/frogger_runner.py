from abc import ABC, abstractmethod

from src.frogger_game import FroggerGame


class FroggerRunner(ABC):
    def __init__(self, game: FroggerGame, grid_like: bool = False):
        self.game = game

        self.grid_like = grid_like

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def test_run(self, model_name: str, number_of_games: int = 100):
        pass
