from datetime import timedelta, datetime

import pickle
from time import sleep

import neat
import sys

import pygame

import matplotlib.pyplot as plt

from constants import FPS, HEIGHT, CELL_SIZE, NEAT_GENERATIONS
from frogger_runner import FroggerGame
from neat_player import NeatPlayer


class NeatFroggerGame(FroggerGame):

    def run_game_step(self, nets, players, ge, best_of=3):
        self.clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.cars.update()
        self.players = pygame.sprite.Group(players)

        for x, player in enumerate(players):
            d = ((HEIGHT - player.rect.y) // CELL_SIZE) - 1

            if not player.alive:
                player.fitnesses[player.game_id] += d

                if player.game_id < best_of:
                    player.reset()
                else:
                    ge[x].fitness += len(set(player.action_taken))
                    ge[x].fitness += sum(player.fitnesses) / len(player.fitnesses)

                    players.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                continue

            output = nets[x].activate(player.get_data(self.cars))
            direction = output.index(max(output))
            player.update(direction)

            if pygame.sprite.spritecollideany(player, self.cars):
                player.alive = False

            if player.steps == 0:
                player.alive = False

            if player.rect.y <= 0:
                player.alive = False
                player.won = True

                player.fitnesses[player.game_id] += player.steps / 10

        self._draw()

        return len(players) > 0


# NEATRunner Class
class NEATRunner:
    def __init__(self, config_file):
        self.config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                         config_file)

        self.population = neat.Population(self.config)
        self.population.add_reporter(neat.StdOutReporter(True))
        self.stats = neat.StatisticsReporter()
        self.population.add_reporter(self.stats)

        self.best_fitness = []
        self.average_fitness = []
        self.last_plot_time = datetime.now()
        self.game = NeatFroggerGame()

    def run(self):
        for gen in range(NEAT_GENERATIONS):
            self.population.run(self.eval_genomes, 1)
            self.update_plot(gen)

        winner = self.stats.best_genome()
        print(f'\nBest genome:\n{winner}')

        # Save winner to models folder
        with open('models/winner1.pkl', 'wb') as f:
            pickle.dump(winner, f)

    def test_run(self):
        with open('models/winner1.pkl', 'rb') as f:
            winner = pickle.load(f)

        wins = 0

        for i in range(100):
            nets = []
            players = []
            ge = []

            net = neat.nn.FeedForwardNetwork.create(winner, self.config)
            nets.append(net)
            player = NeatPlayer()
            players.append(player)
            ge.append(winner)

            self.game.cars = self.game.create_cars()

            running = True

            while running:
                running = self.game.run_game_step(nets, players, ge, best_of=1)

            win = player.rect.y <= 0

            print(f'Game {i + 1} finished with {win and "WIN" or "LOSE"}')

            wins += win

    def eval_genomes(self, genomes, config):
        nets = []
        players = []
        ge = []

        for genome_id, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            players.append(NeatPlayer())
            genome.fitness = 0
            ge.append(genome)

        self.game.cars = self.game.create_cars()

        running = True

        while running:
            running = self.game.run_game_step(nets, players, ge)

        fitnesses = [genome.fitness for index, genome in genomes]
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
        plt.pause(0.1)  # Brief pause to update the plot

        self.last_plot_time = datetime.now()
