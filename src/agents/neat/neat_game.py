import pygame

from src.constants import HEIGHT, CELL_SIZE
from src.frogger_game import FroggerGame


class NeatFroggerGame(FroggerGame):

    def __init__(self, grid_like: bool = False, with_train: bool = False, lives_per_player: int = 5):
        super().__init__(grid_like=grid_like, with_train=with_train)

        self.lives_per_player = lives_per_player

        self.networks = []
        self.players = []
        self.genomes = []

    def update_configuration(self, networks, players, genomes):
        self.networks = networks
        self.players = players
        self.genomes = genomes

    def update_game_frame(self):
        super().update_game_frame()

        for x, player in enumerate(self.players):
            output = self.networks[x].activate(player.get_state(self.obstacles))
            direction = output.index(max(output))
            player.update(direction)

            # If the player died to a car, kill it
            if pygame.sprite.spritecollideany(player, self.obstacles):
                player.alive = False

            # If the player is out of steps, kill it
            if player.steps == 0:
                player.alive = False

            # If the player reached the top, mark it as won and give it a fitness boost
            if player.rect.y <= 0:
                player.alive = False
                player.won = True

                player.fitnesses[player.game_id] += player.steps / 10

            # If the player had just died in the previous frame, update its fitness
            if not player.alive:
                progress_made = ((HEIGHT - player.rect.y) // CELL_SIZE) - 1

                player.fitnesses[player.game_id] += progress_made

                if player.game_id < self.lives_per_player - 1:
                    player.reset()
                else:
                    unique_actions = len(set(player.action_taken))
                    average_fitness = sum(player.fitnesses) / len(player.fitnesses)

                    self.genomes[x].fitness += unique_actions + average_fitness

                    self.players.pop(x)
                    self.networks.pop(x)
                    self.genomes.pop(x)
