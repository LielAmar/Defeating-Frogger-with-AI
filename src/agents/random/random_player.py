import pygame

from src.entities.player import Player


class RandomPlayer(Player):

    def get_state(self, cars: pygame.sprite.Group) -> list:
        return []
