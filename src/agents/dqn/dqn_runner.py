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

        self.agent = DQNAgent(self.settings)

        self.last_plot_time = datetime.now()

    def run(self):
        if self.settings.test is not None:
            self._run_test()
            return

        self.game.update_configuration(self.agent)

        total_rewards = []

        for episode in range(self.settings.games):
            self.game.reset()

            player = DQNPlayer()
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

                # Update target model periodically
                if player.steps % 10 == 0:
                    self.agent.update_target_model()

            print(f"Episode {episode + 1}/{self.settings.games}, Total Reward: {total_reward}")

            # Optionally save the model at intervals
            if (episode + 1) % 10 == 0:
                self.save_model(f"models/dqn/3_model_episode_{episode + 1}.pth")

            if episode == self.settings.games / 2:
                self.agent.update_learning_rate()

            if self.settings.plot:
                total_rewards.append(total_reward)
                self.update_plot(total_rewards)

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

    def _run_single_test(self, model_name: str):
        model_path = f'models/dqn/{model_name}'

        self.agent.model.load_state_dict(torch.load(model_path))
        self.agent.update_target_model()

        self.game.update_configuration(self.agent)

        wins = 0

        for i in range(self.settings.games):
            self.game.reset()

            player = DQNPlayer()
            self.game.players.append(player)

            while True:
                if not self.game.run_single_game_frame():
                    break

            win = player.won
            wins += win

            print(f'Player has {win and "WON" or "LOST"} game #{i + 1}')

        print(f"Total number of Wins: {wins}")

        return wins

    def update_plot(self, total_rewards):
        if datetime.now() - self.last_plot_time < timedelta(seconds=3):
            return

        plt.clf()
        plt.title("DQN Reward over Episodes")
        plt.xlabel("Episodes")
        plt.ylabel("Reward")
        plt.plot(total_rewards, label="Reward")

        plt.legend()
        plt.pause(0.1)

        self.last_plot_time = datetime.now()
