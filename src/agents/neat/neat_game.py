from src.constants import HEIGHT, CELL_SIZE
from src.direction import Direction
from src.frogger_game import FroggerGame


class NeatFroggerGame(FroggerGame):

    def __init__(self, settings):
        super().__init__(settings=settings)

        self.networks = []
        self.genomes = []

    def update_configuration(self, networks, players, genomes):
        self.networks = networks
        self.players = players
        self.genomes = genomes

    def update_game_frame(self):
        super().update_game_frame()

        for x, player in enumerate(self.players):
            output = self.networks[x].activate(player.get_state(self.obstacles))
            direction_index = output.index(max(output))
            direction = Direction.from_int(direction_index)

            self.update_player(player, direction)

            if player.won:
                player.fitnesses[player.game_id] += player.steps / 10

            if not player.alive:
                progress_made = ((HEIGHT - player.rect.y) // CELL_SIZE) - 1

                player.fitnesses[player.game_id] += progress_made

                if player.game_id < self.settings.lives - 1:
                    player.reset()
                else:
                    unique_actions = len(set(player.action_taken))
                    average_fitness = sum(player.fitnesses) / len(player.fitnesses)

                    self.genomes[x].fitness += unique_actions + average_fitness

                    self.players.pop(x)
                    self.networks.pop(x)
                    self.genomes.pop(x)
