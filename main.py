import math
import os
import sys
from abc import abstractmethod, ABC
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import neat
import pygame

from car import Car
from constants import WIDTH, HEIGHT, CELL_SIZE, FPS, BLACK, CARS_PER_ROW
from neat_player import NeatPlayer


class FroggerGame(ABC):
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption("Frogger Game")

        self.clock = pygame.time.Clock()

        self.cars = self._create_cars()
        self.players = pygame.sprite.Group()

    def _create_cars(self):
        cars = pygame.sprite.Group()
        car_rows = [
            (2, 0),
            (3, 2),
            (4, 4),
            (5, 3),
            (6, 1),

            (8, 0),
            (9, 4),
            (10, 3),
            (11, 0),
            (12, 2)
        ]

        for row, offset in car_rows:
            for i in range(CARS_PER_ROW):
                car = Car((i * 6 + offset) * CELL_SIZE, row * CELL_SIZE, 1)
                cars.add(car)

        return cars

    @abstractmethod
    def run_game_step(self, nets, players, ge):
        ...

    def _draw(self):
        self.screen.fill(BLACK)

        self.cars.draw(self.screen)

        for player in self.players:
            self.screen.blit(player.image, player.rect.topleft)

        pygame.display.flip()


class NeatFroggerGame(FroggerGame):

    def run_game_step(self, nets, players, ge):
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
                ge[x].fitness += d
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
                ge[x].fitness += (player.steps / 10)

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

    def run(self, generations=200):
        for gen in range(generations):
            self.population.run(self.eval_genomes, 1)
            self.update_plot(gen)

        winner = self.stats.best_genome()
        print(f'\nBest genome:\n{winner}')

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
        plt.plot(self.best_fitness, label="Best Fitness (Logged)")
        plt.plot(self.average_fitness, label="Average Fitness")
        plt.legend()
        plt.pause(0.1)  # Brief pause to update the plot

        self.last_plot_time = datetime.now()


# Main Function
def main():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat-config.txt")
    runner = NEATRunner(config_path)
    runner.run()


if __name__ == "__main__":
    main()
