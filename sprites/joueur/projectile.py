import pygame
from general.globals import * 

class Projectile(pygame.sprite.Sprite):

    def __init__(self, player, direction):
        super().__init__()
        self.velocity = 5
        self.player = player
        self.image = pygame.image.load(('assets/joueur/boule.png'))
        self.rect = self.image.get_rect()
        if direction == "right":
            self.rect.x = player.rect.x + 60 
        else:
            self.rect.x = player.rect.x - 60 
        self.rect.y = player.rect.y + 12
        self.origine_image = self.image
        self.angle = 0
        self.direction = direction

    def rotate(self):
        self.angle += 12
        self.image = pygame.transform.rotozoom(self.origine_image,self.angle,1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def removeProjectile(self):
        self.player.all_projectiles.remove(self)

    def moveRight(self):
        self.rect.x += self.velocity
        self.rotate()
        
        for monster in self.player.jeuCombat2D.check_collision(self, self.player.jeuCombat2D.all_monster):
            self.removeProjectile()
            monster.damage(self.player.attack)

    def moveLeft(self):
        self.rect.x -= self.velocity
        self.rotate()

        for monster in self.player.jeuCombat2D.check_collision(self, self.player.jeuCombat2D.all_monster):
            self.removeProjectile()
            monster.damage(self.player.attack)
        if self.rect.x > SCREENWIDTH or self.rect.x < 0:
            self.removeProjectile()
