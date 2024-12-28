import pygame, random
from general.globals import *
from sprites.monstre._Monstre import Monstre

class Monster(Monstre):
    def __init__(self, jeuCombat2D):
        super().__init__(jeuCombat2D)
        pygame.init()

        self.health = 100
        self.max_health = 100
        self.attack = 1
        self.attack_card = 5
        self.diceNum = 2
        self.image = pygame.image.load("assets/monstre/monsterTest.png")
        self.rect.x = (SCREENWIDTH - 80) + random.randint(10,400)
        self.rect.y = 405
        self.velocity = random.randint(1,3)