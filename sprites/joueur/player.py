import pygame
from general.globals import *
from sprites.joueur.projectile import Projectile
from sprites.decors.heart import Heart


class Player(pygame.sprite.Sprite): 
    def __init__(self, jeuCombat2D):
        super().__init__()
        self.jeuCombat2D = jeuCombat2D
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 3
        self.velocity_y = 10
        self.jump = False
        self.all_projectiles = pygame.sprite.Group()
        self.heart = Heart()
        self.image = pygame.image.load('assets/joueur/persotest.png')
        self.image_right = pygame.image.load('assets/joueur/monsieur_right.png')
        self.image_left = pygame.image.load('assets/joueur/monsieur_left.png')
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = 405

    ########## Promenade #############
    # Movement
    def move_right(self):
        if self.jump: 
            self.rect.x += self.velocity*3
        else:
            self.rect.x += self.velocity

    def move_left(self):
        if self.jump: 
            self.rect.x -= self.velocity*3
        else:
            self.rect.x -= self.velocity

    ########## Combat #############
    # Shoot
    def launch_projectile(self, direction, velocity = 5):
        self.all_projectiles.add(Projectile(self, direction))

    # Movement
    def move_right_cbt(self):
        if not self.jeuCombat2D.check_collision(self, self.jeuCombat2D.all_monster):
            if self.jump: 
                self.rect.x += self.velocity*3
            else:
                self.rect.x += self.velocity

    def move_left_cbt(self):
        if not self.jeuCombat2D.check_collision(self, self.jeuCombat2D.all_monster):
            if self.jump: 
                self.rect.x -= self.velocity*3
            else:
                self.rect.x -= self.velocity
        # hit
    def damage(self, amount):
        self.health -= amount
        
        # maj hp bar
    def update_health_bar(self, surface):
        pygame.draw.rect(surface, (60,63,60), [self.rect.x - 18,self.rect.y - 20,self.max_health,5])
        pygame.draw.rect(surface, (111,210,46), [self.rect.x - 18,self.rect.y - 20,self.health,5])

    def update_pos(self, x, y): 
        self.rect.center = (x, y)






