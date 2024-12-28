import pygame
from general.globals import *

class Door(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/zonePromenade/door.png")
        self.rect = self.image.get_rect()
        self.rect.x = 150
        self.rect.y = 415

class BigDoor(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/zonePromenade/bigdoor.png")
        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = 275
