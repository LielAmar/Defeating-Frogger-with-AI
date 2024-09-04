import pickle
from datetime import datetime, timedelta

import neat
from matplotlib import pyplot as plt

from src.agents.neat.neat_game import NeatFroggerGame
from src.agents.neat.neat_player import NeatPlayer
from src.frogger_runner import FroggerRunner


class NEATRunner(FroggerRunner):
    def __init__(
            self,
            settings
    ):
        super().__init__(
            game=NeatFroggerGame(settings=settings), settings=settings)

        self.config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                         self.settings.neat_config)

        self.population = neat.Population(self.config)
        self.population.add_reporter(neat.StdOutReporter(True))
        self.stats = neat.StatisticsReporter()
        self.population.add_reporter(self.stats)

        # Plotting configuration
        self.best_fitness = []
        self.average_fitness = []
        self.last_plot_time = datetime.now()

    def run(self):
        if self.settings.test is not None:
            self._run_test()
            return

        for gen in range(self.settings.generations):
            self.population.run(self.eval_genomes, 1)

            if self.settings.plot:
                self.update_plot(gen)

        best_genome = self.stats.best_genome()
        file = f"neat_model_{datetime.now().timestamp()}.pkl"

        print(f'Best genome: {best_genome}. Saving to file {file}')

        # Save best_genome to models folder
        with open(f'models/{file}', 'wb') as f:
            pickle.dump(best_genome, f)

    def _run_test(self):
        models_files = []

        if self.settings.test == '*':
            models_files += [file for file in os.listdir('models') if file.endswith('.pkl')]
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

    def _run_single_test(self, model_name: str):
        # Load model from models folder
        with open(f'models/{model_name}', 'rb') as f:
            model = pickle.load(f)

        wins = 0

        for i in range(self.settings.games):
            networks = []
            players = []
            genomes = []

            network = neat.nn.FeedForwardNetwork.create(model, self.config)
            networks.append(network)

            player = NeatPlayer()
            players.append(player)

            genomes.append(model)

            self.game.reset()
            self.game.update_configuration(networks, players, genomes)

            while True:
                if not self.game.run_single_game_frame():
                    break

            win = player.won
            wins += win

            print(f'Player has {win and "WON" or "LOST"} game #{i + 1}')

        print(f"Total number of Wins: {wins}")

        return wins

    def eval_genomes(self, all_genomes, config):
        networks = []
        players = []
        genomes = []

        for genome_id, genome in all_genomes:
            network = neat.nn.FeedForwardNetwork.create(genome, config)
            networks.append(network)

            player = NeatPlayer()
            players.append(player)

            genome.fitness = 0
            genomes.append(genome)

        self.game.reset()
        self.game.update_configuration(networks, players, genomes)

        while True:
            if not self.game.run_single_game_frame():
                break

        fitnesses = [genome.fitness for index, genome in all_genomes]

        best_fitness = max(fitnesses)
        average_fitness = sum(fitnesses) / len(fitnesses)

        won = [fitness for fitness in fitnesses if fitness >= 15]

        print("Number of winners:", len(won))

        self.best_fitness.append(best_fitness)
        self.average_fitness.append(average_fitness)

    def update_plot(self, generation):
        if datetime.now() - self.last_plot_time < timedelta(seconds=3):
            return

        plt.clf()
        plt.title("NEAT Fitness over Generations")
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.plot(self.best_fitness, label="Best Fitness")
        plt.plot(self.average_fitness, label="Average Fitness")

        plt.axhline(y=15, color='r', linestyle='--', label="Win Threshold")

        plt.legend()
        plt.pause(0.1)

        self.last_plot_time = datetime.now()
