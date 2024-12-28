import pygame
from sprites.joueur.player import Player
from sprites.decors.door import Door,BigDoor
from general.dialogue import dialogue

class ZonePromenade:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.bg_img = pygame.image.load("assets/zonePromenade/bg.png")
        self.player = Player(self)
        self.door = Door()
        self.door2 = Door()
        self.door2.rect.x = 380
        self.door3 = Door()
        self.door3.rect.x = 600
        self.bigdoor = BigDoor()
        self.player.rect.y = 455

    def run(self):
        #background
        self.display.blit(self.bg_img,(0,0))
        #sprite
        self.display.blit(self.door.image,self.door.rect)
        self.display.blit(self.door2.image,self.door2.rect)
        self.display.blit(self.door3.image,self.door3.rect)
        self.display.blit(self.bigdoor.image,self.bigdoor.rect)
        self.display.blit(self.player.image,self.player.rect)

        pygame.display.flip()

        keys = pygame.key.get_pressed()

        if self.player.rect.colliderect(self.door.rect):
            if keys[pygame.K_f]:
                self.gameStateManager.set_state(('mazeGame'))

        if self.player.rect.colliderect(self.door2.rect):
            if keys[pygame.K_f]:
                self.gameStateManager.set_state(('jeumontee'))

        if self.player.rect.colliderect(self.door3.rect):
            if keys[pygame.K_f]:
                self.gameStateManager.set_state(('jeuCombat2D'))

        if self.player.rect.colliderect(self.bigdoor.rect):
            if keys[pygame.K_f]:
                dialogue("Mince, je n'ai pas acheté le DLC, je ne peux pas accéder au château.", 'menu', self.gameStateManager)




