from abc import ABC, abstractmethod

from src.frogger_game import FroggerGame


class FroggerRunner(ABC):
    def __init__(self, game: FroggerGame, settings):
        self.game = game

        self.settings = settings

    @abstractmethod
    def run(self):
        """
        Run the game

        :return:
        """

        pass
