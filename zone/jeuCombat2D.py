import pygame
from general.dialogue import dialogue
from sprites.joueur.player import Player
from sprites.monstre.monstreBasic import Monster
from general.menu import save_score
import general.globals

class JeuCombat2D:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.bg_img = pygame.image.load("assets/combat2D/fondfight.png")
        self.all_player = pygame.sprite.Group()
        self.player = Player(self)
        self.all_player.add(self.player)
        self.all_monster = pygame.sprite.Group()
        self.player.update_pos(300 ,460)
        for i in range(8):
            self.spawn_monster()
        self.direction = "left"


    def spawn_monster(self):
        monster = Monster(self)
        self.all_monster.add(monster)

    def check_collision(self, sprite, groupe):
        return pygame.sprite.spritecollide(sprite, groupe, False, pygame.sprite.collide_mask)

    def run(self):
        #background
        self.display.blit(self.bg_img,(0,0))
        #sprite

        self.display.blit(self.player.image,self.player.rect)

        for projectile in self.player.all_projectiles:
            if projectile.direction == "right":
                projectile.moveRight()
            elif projectile.direction == "left":
                projectile.moveLeft()
        self.player.all_projectiles.draw(self.display)
        
        for monster in self.all_monster:
            monster.forward()
            monster.update_health_bar(self.display)

        for player in self.all_player:
            player.update_health_bar(self.display)
        
        self.all_monster.draw(self.display)

        if not self.all_monster:
            self.display_victory_screen()

        if self.player.health <= 0:
            self.display_defeat_screen()

    def display_victory_screen(self):
        # self.display.fill((0, 255, 0)) 
        # pygame.display.flip()
        pygame.time.delay(500)
        dialogue("J'ai vaincu tous les monstres. Le château est juste devant.", 'zonePromenade', self.gameStateManager)
    
    def display_defeat_screen(self):
        # self.display.fill((255, 0, 0))  
        # pygame.display.flip()
        # pygame.time.delay(2000) 
        save_score()
        self.gameStateManager.set_state('gameover', self.bg_img)
