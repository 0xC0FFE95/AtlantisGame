import pygame
import general.globals
from general.globals import ACTUALSCORE

class Artifact:
    def __init__(self, maze, image):
        """
        Initialise les artefacts dans le labyrinthe.
        """
        self.positions = []
        self.image = pygame.transform.scale(image, (20, 20))

        # Générer 5 artefacts au hasard
        for _ in range(5):
            x, y = maze.find_free_position()
            self.positions.append((x, y))

    def collect(self, player):
        """
        Vérifie si le joueur ramasse un artefact.
        :param player: Instance de la classe Player.
        :return: True si un artefact est collecté, False sinon.
        """
        for pos in self.positions:
            artifact_rect = pygame.Rect(pos[0], pos[1], 20, 20)
            if player.rect.colliderect(artifact_rect):  # Collision entre le joueur et l'artefact
                self.positions.remove(pos)  # Retirer l'artefact
                addScore()  # Ajouter des points pour l'artefact
                return True
        return False

    def draw(self, screen):
        """
        Dessine les artefacts à l'écran.
        :param screen: Surface de l'écran.
        """
        for pos in self.positions:
            screen.blit(self.image, pos)



def addScore():
    general.globals.ACTUALSCORE += 500
