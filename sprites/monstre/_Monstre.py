import pygame, random
from general.globals import *
import general.globals
from sprites.decors.heart import Heart

class Monstre(pygame.sprite.Sprite):
    def __init__(self, jeuCombat2D):
        super().__init__()
        pygame.init()

        " Attributs a redefinir excepte rect"
        self.image = pygame.image.load("assets/monstre/monsterTest.png")

        self.rect = self.image.get_rect()
        self.health = 0
        self.max_health = 0
        self.attack = 0
        self.attack_card = 0 
        self.rect.x = 0
        self.rect.y = 0
        self.velocity = 0

        " Attributs par defaut "
        self.jeuCombat2D = jeuCombat2D
        self.heart = Heart()
        self.direction = "left"


    def forward(self):
        if not self.jeuCombat2D.check_collision(self, self.jeuCombat2D.all_player):
            if self.direction == "left":
                self.rect.x -= self.velocity
                if self.rect.x <= 0:
                    self.direction = "right"

            elif self.direction == "right":
                self.rect.x += self.velocity
                if self.rect.x >= SCREENWIDTH:
                    self.direction = "left"
        else:
            self.jeuCombat2D.player.damage(self.attack)
        return self.jeuCombat2D.direction


    def damage(self, amount):
        self.health -= amount

        if self.health <= 0:
            addScore()
            self.kill()
    
    def update_health_bar(self, surface):
        pygame.draw.rect(surface, (60,63,60), [self.rect.x - 18,self.rect.y - 20,self.max_health,5])
        pygame.draw.rect(surface, (111,210,46), [self.rect.x - 18,self.rect.y - 20,self.health,5])

def addScore():
    general.globals.ACTUALSCORE +=500