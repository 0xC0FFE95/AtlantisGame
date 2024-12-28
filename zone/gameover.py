import pygame
import numpy as np
from PIL import Image, ImageFilter
from general.menu import save_score
from general.globals import *

class GameOver:
    # Constants for window size, colors, and other settings
    LARGEUR_FENETRE = SCREENWIDTH
    HAUTEUR_FENETRE = SCREENHEIGHT
    FPS = FPS
    COULEUR_FOND = (0, 0, 0)  # Black

    # Wave parameters
    AMPLITUDE_VAGUE = 8  # Wave height
    LONGUEUR_ONDE = 100  # Distance between wave crests
    VITESSE_VAGUE = 0.4  # Wave speed
    FREQUENCE_VAGUE = 0.02  # Wave frequency
    COULEUR_VAGUE = (0, 100, 255, 128)  # Blue with transparency

    # Water rise parameters
    HAUTEUR_DEPART = HAUTEUR_FENETRE / 1.2  # Initial water level
    VITESSE_MONTEE = 10  # Pixels per frame

    VITESSE_MONTEE = 15  # Pixels per frame

    LIMITE_MONTANT = 0  # Limit where the water should stop

    # Blur parameters
    ACTIVER_FLOU = True  # Toggle blur effect
    RAYON_FLOU = 5  # Blur intensity (radius)

    # Background image settings
    CHEMIN_IMAGE_FOND = "assets/combat2D/fondfight.png"  # Default background image path
    IMAGE_FOND_ACTIVE = True  # Toggle background image

    # Game over image settings
    CHEMIN_IMAGE_GAME_OVER = "assets/general/over3.png"  # Game over image path
    IMAGE_GAME_OVER = pygame.image.load(CHEMIN_IMAGE_GAME_OVER)
    IMAGE_GAME_OVER = pygame.transform.scale(IMAGE_GAME_OVER, (300, 300))

    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.bg_img = self.gameStateManager.bg_img if self.gameStateManager.bg_img else pygame.image.load(self.CHEMIN_IMAGE_FOND)
        
        # Initialize the display 
        self.ecran = pygame.display.set_mode((self.LARGEUR_FENETRE, self.HAUTEUR_FENETRE)) 
        pygame.display.set_caption("Defeat") 
        self.surface_temporaire = pygame.Surface((self.LARGEUR_FENETRE, self.HAUTEUR_FENETRE), pygame.SRCALPHA) 
        self.surface_temporaire.fill((0, 0, 0, 0)) 

        if self.IMAGE_FOND_ACTIVE:
            self.image_fond = self.bg_img 
            self.image_fond = pygame.transform.scale(self.image_fond, (self.LARGEUR_FENETRE, self.HAUTEUR_FENETRE)) 
            
        self.clock = pygame.time.Clock() 
        self.temps = 0 
        self.hauteur_base = self.HAUTEUR_DEPART 
        self.game_over = False

    def appliquer_flou(self, surface):
        if not self.ACTIVER_FLOU:
            return surface
        taille = surface.get_size()
        image = pygame.image.tostring(surface, "RGBA")
        img_pillow = Image.frombytes("RGBA", taille, image)
        img_pillow = img_pillow.filter(ImageFilter.GaussianBlur(self.RAYON_FLOU))
        image_floue = pygame.image.fromstring(img_pillow.tobytes(), taille, "RGBA")
        return image_floue

    def dessiner_vague(self):
        for x in range(self.LARGEUR_FENETRE):
            y = int(self.hauteur_base - self.temps * self.VITESSE_MONTEE + self.AMPLITUDE_VAGUE * np.sin((x * self.FREQUENCE_VAGUE) + (self.temps * self.VITESSE_VAGUE)))
            pygame.draw.line(self.surface_temporaire, self.COULEUR_VAGUE, (x, y), (x, self.HAUTEUR_FENETRE))

    def afficher_game_over(self):
        self.ecran.blit(self.IMAGE_GAME_OVER, ((self.LARGEUR_FENETRE - self.IMAGE_GAME_OVER.get_width()) // 2,
                                               (self.HAUTEUR_FENETRE - self.IMAGE_GAME_OVER.get_height()) // 2))

    def run(self):
        # Main game loop
        en_cours = True
        while en_cours:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    en_cours = False

            # Draw background
            if self.IMAGE_FOND_ACTIVE:
                self.ecran.blit(self.image_fond, (0, 0))
            else:
                self.ecran.fill(self.COULEUR_FOND)

            # Create and draw the wave
            self.surface_temporaire.fill((0, 0, 0, 0))  # Reset the surface for each frame
            self.dessiner_vague()

            # Apply blur effect (if enabled)
            if self.ACTIVER_FLOU:
                surface_floue = self.appliquer_flou(self.surface_temporaire)
                self.ecran.blit(surface_floue, (0, 0))
            else:
                self.ecran.blit(self.surface_temporaire, (0, 0))

            # Check if the water level reached the limit
            if self.hauteur_base - self.temps * self.VITESSE_MONTEE < self.LIMITE_MONTANT:
                self.game_over = True

            # If "Game Over", display the Game Over image
            if self.game_over:
                self.afficher_game_over()
                pygame.display.flip()
                pygame.time.delay(2000)
                # pygame.quit()
                self.gameStateManager.set_state('menu')
                break
            # Refresh the screen
            pygame.display.flip()
            self.temps += 1
            self.clock.tick(self.FPS)

    def display(self):
        self.run()

    def set_gameover(self):
        self.gameStateManager.set_state('gameover')
