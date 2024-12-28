import pygame
from general.globals import *

class Heart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/general/heart.png")
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10
