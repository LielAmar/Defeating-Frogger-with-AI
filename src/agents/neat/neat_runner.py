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
            grid_like: bool = False,
            config_file: str = 'neat-config.txt',
            number_of_generations: int = 200,
            plot: bool = True
    ):
        super().__init__(game=NeatFroggerGame(grid_like=grid_like), grid_like=grid_like)

        self.config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                         config_file)

        self.population = neat.Population(self.config)
        self.population.add_reporter(neat.StdOutReporter(True))
        self.stats = neat.StatisticsReporter()
        self.population.add_reporter(self.stats)

        self.number_of_generations = number_of_generations
        self.plot = plot

        # Plotting configuration
        self.best_fitness = []
        self.average_fitness = []
        self.last_plot_time = datetime.now()

    def run(self):
        for gen in range(self.number_of_generations):
            self.population.run(self.eval_genomes, 1)

            if self.plot:
                self.update_plot(gen)

        best_genome = self.stats.best_genome()
        file = f"neat_model_{datetime.now().timestamp()}.pkl"

        print(f'Best genome: {best_genome}. Saving to file {file}')

        # Save best_genome to models folder
        with open(f'models/{file}', 'wb') as f:
            pickle.dump(best_genome, f)

    def test_run(self, model_name: str, number_of_games: int = 100):
        # Load model from models folder
        with open(f'models/{model_name}', 'rb') as f:
            model = pickle.load(f)

        wins = 0

        for i in range(number_of_games):
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
