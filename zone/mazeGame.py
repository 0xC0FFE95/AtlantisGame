import pygame
from classesMaze.player import Player
from classesMaze.maze import Maze
from classesMaze.monster import Monster
from classesMaze.artifact import Artifact
from classesMaze.timer import Timer
from classesMaze.scoreMaze import Score
from general.dialogue import dialogue
from general.menu import save_score
import general.globals
from general.globals import *

class MazeGame:
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.running = True

        # Dimensions de l'écran
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = SCREENWIDTH, SCREENHEIGHT

        # Charger les images
        self.player_image = pygame.image.load("images/player.png")
        self.wall_image = pygame.image.load("images/wall.png")
        self.exit_image = pygame.image.load("images/exit.jpg")
        self.monster_image = pygame.image.load("images/monster.jpg")
        self.artifact_image = pygame.image.load("images/artifact.jpg")
        self.heart_image = pygame.image.load("images/heart.png")

        # Charger les sons
        self.artifact_sound = pygame.mixer.Sound("sounds/artifact_collected.wav")
        self.win_sound = pygame.mixer.Sound("sounds/win.wav")
        self.game_over_sound = pygame.mixer.Sound("sounds/game_over.wav")
        self.life_lost_sound = pygame.mixer.Sound("sounds/life_lost.wav")

        # Initialiser le labyrinthe
        rows, cols = 23, 23
        self.maze = Maze(rows, cols, self.wall_image, self.exit_image, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        # Position initiale du joueur
        player_start_x, player_start_y = self.maze.find_free_position()
        self.player = Player(player_start_x, player_start_y, size=20, speed=5, image=self.player_image, lives=3)

        # Initialiser les artefacts et les monstres
        self.artifact = Artifact(self.maze, self.artifact_image)
        self.monsters = [Monster(*self.maze.find_free_position(), size=20, speed=1, image=self.monster_image) for _ in range(3)]

        # Initialiser le timer
        self.timer = Timer(total_time=60)  # 60 secondes

        # Initialiser le score
        self.score = Score()

        # Initialiser la police pour le texte
        self.font = pygame.font.Font(None, 36)

        # Cooldown pour les collisions
        self.collision_cooldown = 0

        # Indicateur pour afficher le menu de victoire
        self.show_victory_menu = False

    def run(self):
        # if self.show_victory_menu:
        #     self.display_victory_screen()
        #     return

        # Démarrer la musique de fond si elle n'est pas déjà en cours
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("sounds/background_music.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

        keys = pygame.key.get_pressed()
        self.player.move(keys, self.maze)

        # Déplacement des monstres
        for monster in self.monsters:
            monster.move(self.maze, (self.player.x, self.player.y))

        # Collecte des artefacts
        if self.artifact.collect(self.player):
            self.artifact_sound.play()
            new_monster_x, new_monster_y = self.maze.find_free_position()
            self.monsters.append(Monster(new_monster_x, new_monster_y, size=20, speed=3, image=self.monster_image))

        # Activer la sortie après avoir collecté tous les artefacts
        if not self.artifact.positions and not self.maze.exit_position:
            self.maze.activate_exit()

        # Vérifier si le joueur atteint la sortie
        if self.maze.exit_position:
            exit_rect = pygame.Rect(
                self.maze.exit_position[0],
                self.maze.exit_position[1],
                self.maze.cell_width,
                self.maze.cell_height,
            )
            if self.player.rect.colliderect(exit_rect):
                pygame.mixer.music.stop()  # Arrêter la musique de fond
                self.win_sound.play()
                self.display_victory_screen()  # Afficher l'écran de victoire

        # Vérifier les collisions avec les monstres
        if self.collision_cooldown == 0:
            for monster in self.monsters:
                if self.player.rect.colliderect(monster.rect):
                    self.player.lives -= 1
                    self.life_lost_sound.play()
                    self.collision_cooldown = 60
                    if self.player.lives <= 0:
                        pygame.mixer.music.stop()  # Arrêter la musique de fond
                        self.game_over_sound.play()
                        self.display_defeat_screen()  # Afficher l'écran de défaite
                    break

        if self.collision_cooldown > 0:
            self.collision_cooldown -= 1

        if self.timer.is_time_up():
            pygame.mixer.music.stop()  # Arrêter la musique de fond
            self.game_over_sound.play()
            self.display_defeat_screen()  # Écran de défaite

        self.draw()

    def draw(self):
        self.screen.fill((0, 0, 0))  # Fond noir
        self.maze.draw(self.screen)
        self.artifact.draw(self.screen)
        self.player.draw(self.screen)
        for monster in self.monsters:
            monster.draw(self.screen)

        # Dessiner les vies
        for i in range(self.player.lives):
            self.screen.blit(pygame.transform.scale(self.heart_image, (30, 30)), (10 + i * 40, 10))

        # Dessiner le timer
        self.timer.draw(self.screen, self.font, self.SCREEN_WIDTH - 150, 10)

        pygame.display.flip()

    def display_victory_screen(self):
        general.globals.AVANCER += 1
        self.timer.add_time_score()
        """
        Gère l'écran de victoire.
        """
        dialogue("J'ai réussi à trouver une sortie. Allons voir où cela mène.", 'zonePromenade', self.gameStateManager)

    def display_defeat_screen(self):
        print('victoire')
        self.timer.add_time_score()
        print('victoire')
        """
        Gère l'écran de défaite.
        """
        save_score()  # Sauvegarder le score
        self.gameStateManager.set_state('gameover')
