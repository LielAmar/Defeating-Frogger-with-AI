from src.agents.random.random_game import RandomGame
from src.agents.random.random_player import RandomPlayer
from src.frogger_runner import FroggerRunner


class RandomRunner(FroggerRunner):
    def __init__(self, grid_like: bool = False, games_to_play: int = 3):
        super().__init__(game=RandomGame(grid_like=grid_like), grid_like=grid_like)

        self.games_to_play = games_to_play

    def run(self):
        wins = 0

        for i in range(self.games_to_play):
            self.game.reset()

            player = RandomPlayer()
            self.game.update_configuration(player=player)

            while True:
                if not self.game.run_single_game_frame():
                    break

            win = player.won
            wins += win

            print(f'Player has {win and "WON" or "LOST"} game #{i + 1}')

        print(f"Total number of Wins: {wins}")

        return wins

    def test_run(self, model_name: str, number_of_games: int = 100):
        raise NotImplementedError
