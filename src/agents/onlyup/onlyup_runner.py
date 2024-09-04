from src.agents.onlyup.onlyup_game import OnlyUpGame
from src.agents.onlyup.onlyup_player import OnlyUpPlayer
from src.frogger_runner import FroggerRunner


class OnlyUpRunner(FroggerRunner):
    def __init__(self, settings):
        super().__init__(game=OnlyUpGame(settings=settings), settings=settings)

    def run(self):
        wins = 0

        for i in range(self.settings.games):
            self.game.reset()

            player = OnlyUpPlayer()
            self.game.update_configuration(player=player)

            while True:
                if not self.game.run_single_game_frame():
                    break

            win = player.won
            wins += win

            print(f'Player has {win and "WON" or "LOST"} game #{i + 1}')

        print(f"Total number of Wins: {wins}")

        return wins

    def test_run(self, model_name: str):
        raise NotImplementedError
