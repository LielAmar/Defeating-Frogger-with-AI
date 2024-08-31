import pygame

from constants import RED, CELL_SIZE, WIDTH


class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.x += CELL_SIZE
        if self.rect.x > WIDTH:
            self.rect.x = -self.rect.width
