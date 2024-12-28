import pygame,sys,random
from zone.zonePromenade import ZonePromenade
from zone.jeuCombat2D import JeuCombat2D
from zone.gameover import GameOver
from zone.donkey import JeuMontee
from general.gameStateManager import GameStateManager
from general.globals import *
from general.menu import Menu
from zone.mazeGame import MazeGame




class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.gameStateManager = GameStateManager('menu')
        self.zonePromenade = ZonePromenade(self.screen, self.gameStateManager)
        self.jeuCombat2D = JeuCombat2D(self.screen, self.gameStateManager)
        self.gameOver = GameOver(self.screen, self.gameStateManager)
        self.jeuMontee = JeuMontee(self.screen, self.gameStateManager)
        self.mazeGame = MazeGame(self.screen, self.gameStateManager)
        self.menu = Menu(self.screen, self.gameStateManager)
        self.pressed = {
            #pour gérer les déplacements fluides
       }
        self.states = {
            'zonePromenade': self.zonePromenade,
            'jeuCombat2D': self.jeuCombat2D,
            'jeumontee': self.jeuMontee,
            'gameover': self.gameOver,
            'menu': self.menu,
            'mazeGame': self.mazeGame,
        }

    def run(self):
        while self.running:
            self.update()
            self.draw()
            #prends la scene de la classe gameStateManager, faire attention a ajouter une def run dans toute les states
            self.states[self.gameStateManager.get_state()].run()

            # Pour pas sortir de l'écran
            if game.pressed.get(pygame.K_d) and self.zonePromenade.player.rect.x + self.zonePromenade.player.rect.width < self.screen.get_width():
                self.zonePromenade.player.move_right()
            elif game.pressed.get(pygame.K_q) and self.zonePromenade.player.rect.x > 0:
                self.zonePromenade.player.move_left()

            if game.pressed.get(pygame.K_d) and self.jeuCombat2D.player.rect.x + self.jeuCombat2D.player.rect.width < self.screen.get_width():
                self.jeuCombat2D.player.move_right_cbt()

            elif game.pressed.get(pygame.K_q) and self.jeuCombat2D.player.rect.x > 0:
                self.jeuCombat2D.player.move_left()


        self.close()

    def update(self):
        if self.jeuCombat2D.player.jump is True:
            self.jeuCombat2D.player.rect.y -= self.jeuCombat2D.player.velocity_y*4
            self.jeuCombat2D.player.velocity_y -= 1
            if self.jeuCombat2D.player.velocity_y < -10:
                self.jeuCombat2D.player.jump = False
                self.jeuCombat2D.player.velocity_y = 10

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            #Pour pouvoir rester appuyer sur une touche
            elif event.type == pygame.KEYDOWN:
                game.pressed[event.key] = True
                if event.key == pygame.K_RIGHT:
                    self.jeuCombat2D.player.launch_projectile("right")
                elif event.key == pygame.K_LEFT:
                    self.jeuCombat2D.player.launch_projectile("left")
                elif self.jeuCombat2D.player.jump is False and event.key == pygame.K_SPACE:
                    self.jeuCombat2D.player.jump = True

            elif event.type == pygame.KEYUP:
              game.pressed[event.key] = False

        pygame.display.update()
        self.clock.tick(FPS)

    def draw(self):
        self.screen.fill('lightblue')

    def close(self):
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()