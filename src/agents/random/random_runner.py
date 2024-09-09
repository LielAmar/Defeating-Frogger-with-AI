from src.agents.random.random_game import RandomGame
from src.agents.random.random_player import RandomPlayer
from src.frogger_runner import FroggerRunner


class RandomRunner(FroggerRunner):
    def __init__(self, settings):
        super().__init__(game=RandomGame(settings=settings), settings=settings)

    def run(self):
        wins = 0
        remaining_steps = []

        for i in range(self.settings.games):
            self.game.reset()

            player = RandomPlayer()
            self.game.update_configuration(player=player)

            while True:
                if not self.game.run_single_game_frame():
                    break

            win = player.won
            wins += win
            remaining_steps.append(player.steps if win else 0)

            print(f'Player has {win and "WON" or "LOST"} game #{i + 1}')

        average_remaining_steps = sum(remaining_steps) / wins if wins else 0

        print(f"Total number of Wins: {wins}, remaining steps: {average_remaining_steps}")

        return wins, average_remaining_steps
