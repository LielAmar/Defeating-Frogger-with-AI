import os
from datetime import datetime, timedelta

import torch
from matplotlib import pyplot as plt

from src.agents.dqn.dqn_agent import DQNAgent
from src.agents.dqn.dqn_game import DQNFroggerGame
from src.agents.dqn.dqn_player import DQNPlayer
from src.frogger_runner import FroggerRunner


class DQNRunner(FroggerRunner):
    def __init__(
            self,
            settings
    ):
        super().__init__(
            game=DQNFroggerGame(settings=settings),
            settings=settings
        )

        state_dim = 25
        state_dim += 5 if settings.train else 0
        state_dim += 15 if settings.water else 0

        self.agent = DQNAgent(self.settings, state_dim=state_dim, action_dim=5)

        self.last_plot_time = datetime.now()

    def run(self):
        if self.settings.test is not None:
            return self._run_test()

        self.game.update_configuration(self.agent)

        total_rewards = []
        game_results = []

        for episode in range(self.settings.games):
            self.game.reset()

            player = DQNPlayer(self.settings)
            self.game.players.append(player)

            total_reward = 0

            done = False

            while not done:
                done = not self.game.run_single_game_frame()

                state = self.game.state
                action = self.game.direction.value
                reward = self.game.reward
                next_state = self.game.next_state

                # print(f"Action: {action}, Reward: {reward}, Done: {done}")

                # Remember the experience
                self.agent.remember(state, action, reward, next_state, done)

                total_reward += reward

                # Replay memory to train the agent
                self.agent.replay()

            self.agent.update_target_model()

            print(f"Episode {episode + 1}/{self.settings.games}, Total Reward: {total_reward}. Won: {player.won}")

            total_rewards.append(total_reward)
            game_results.append(1 if player.won else 0)

            # Optionally save the model at intervals
            if (episode + 1) % 50 == 0:
                self.save_model(f"models/dqn/episode_{episode + 1}.pth")

            if (episode + 1) % 10 == 0 and self.settings.plot:
                self.update_plot(total_rewards, game_results)

    def save_model(self, filename):
        torch.save(self.agent.model.state_dict(), filename)

    def _run_test(self):
        models_files = []

        if self.settings.test == '*':
            models_files += [file for file in os.listdir('models/dqn') if file.endswith('.pth')]
        else:
            models_files.append(self.settings.test)

        wins_tracker = dict()

        for model_file in models_files:
            wins_tracker[model_file] = self._run_single_test(model_file)

            print(f'{model_file}: won {wins_tracker[model_file]}% of the games')

            print(f'Total Wins: {sum(wins_tracker.values())}')
            print(f'Win Rate: {sum(wins_tracker.values()) / (len(wins_tracker) * 100)}%')

            best_player = max(wins_tracker, key=wins_tracker.get)

            print(f'Best Player Wins: {wins_tracker[best_player]}')
            print(f'Best Player Win Rate: {wins_tracker[best_player] / 100}%')

        print(f"Best Player: {best_player}")

        return wins_tracker[best_player]

    def _run_single_test(self, model_name: str):
        model_path = f'models/dqn/{model_name}'

        self.agent.model.load_state_dict(torch.load(model_path))
        self.agent.update_target_model()

        self.game.update_configuration(self.agent)

        wins = 0

        for i in range(self.settings.games):
            self.game.reset()

            player = DQNPlayer(self.settings)
            self.game.players.append(player)

            while True:
                if not self.game.run_single_game_frame():
                    break

            win = player.won
            wins += win

            print(f'Player has {win and "WON" or "LOST"} game #{i + 1}')

        print(f"Total number of Wins: {wins}")

        return wins

    def update_plot(self, total_rewards, game_results):
        if datetime.now() - self.last_plot_time < timedelta(seconds=3):
            return

        plt.clf()

        plt.subplot(2, 1, 1)
        plt.title("DDQN Reward & Wins over Episodes")
        plt.xlabel("Episodes")
        plt.ylabel("Reward")
        plt.plot(total_rewards, 'o', label="Reward", markersize=4)
        plt.legend()

        if len(game_results) < 100:
            wins = [sum(game_results[:i]) for i in range(1, len(game_results) + 1)]
            losses = [i - win for i, win in enumerate(wins)]
        else:
            wins = [
                sum(game_results[i - 100:i]) if i >= 100 else sum(game_results[:i])
                for i in range(0, len(game_results))
            ]
            losses = [100 - win if i >= 100 else i - win for i, win in enumerate(wins)]

        plt.subplot(2, 1, 2)
        plt.xlabel("Episodes")
        plt.ylabel("Number of Wins (last 100 games)")
        plt.plot(wins, label="Wins (last 100 games)", color='blue')
        plt.plot(losses, label="Losses (last 100 games)", color='red')
        plt.axhline(y=90, color='g', linestyle='--', label='90%')
        plt.legend()

        plt.tight_layout()
        plt.pause(0.1)

        self.last_plot_time = datetime.now()
