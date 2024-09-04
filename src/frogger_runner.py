from abc import ABC, abstractmethod

from src.frogger_game import FroggerGame


class FroggerRunner(ABC):
    def __init__(self, game: FroggerGame, settings):
        self.game = game

        self.settings = settings

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def test_run(self, model_name: str):
        pass
