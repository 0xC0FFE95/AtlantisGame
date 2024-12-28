import pygame
import random
from general.dialogue import dialogue
from general.gameStateManager import GameStateManager
from general.globals import *
from assets.jeumontee import *
from general.menu import save_score
import general.globals

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre

fenetre = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Jeu de Montée")


# Couleurs
BLANC = (255, 255, 255)
BLEU = (0, 0, 255)
ROUGE = (255, 0, 0)
NOIR = (0, 0, 0)
GRIS = (200, 200, 200)

# Charger une image de fond
CHEMIN_IMAGE_FOND = "assets/jeumontee/fond.png"
IMAGE_FOND_ACTIVE = True

# Constantes
LARGEUR_PERSONNAGE = 50
HAUTEUR_PERSONNAGE = 50
HAUTEUR_SURFACE = 40
LARGEUR_ECHELLE = 40
HAUTEUR_ECHELLE = 200
SEUIL_DEFILEMENT = SCREENHEIGHT // 3
VITESSE_DEFILEMENT = 2.4
ESPACE_ENTRE_PLATEFORMES = 200
VITESSE_PIEGES = 5
gravite = 5
DISTANCE_MINIMALE_ECHELLES = 200
LARGEUR_FENETRE = SCREENWIDTH 
HAUTEUR_FENETRE = SCREENHEIGHT
MIDDLE_THIRD_START = SCREENWIDTH // 3 
MIDDLE_THIRD_END = (SCREENWIDTH * 2) // 3
SEUIL_SCORE = 1000  #
police = pygame.font.SysFont(None, 36)

# Images
personnage_img = pygame.image.load("assets/jeumontee/mob1.png")
personnage_img = pygame.transform.scale(personnage_img, (LARGEUR_PERSONNAGE, HAUTEUR_PERSONNAGE))

echelle_img = pygame.image.load("assets/jeumontee/echell-removebg-preview.png")
echelle_img = pygame.transform.scale(echelle_img, (LARGEUR_ECHELLE, HAUTEUR_ECHELLE))

sol_img = pygame.image.load("assets/jeumontee/mur.jpg")
sol_img = pygame.transform.scale(sol_img, (SCREENWIDTH, HAUTEUR_SURFACE))

piege_img = pygame.image.load("assets/jeumontee/mob2.png")
piege_img = pygame.transform.scale(piege_img, (20, 20))

porte_img = pygame.image.load("assets/jeumontee/porte.png")
porte_img = pygame.transform.scale(porte_img, (80, 140))
porte_img_active = pygame.image.load("assets/jeumontee/porteActive.png")
porte_img_active = pygame.transform.scale(porte_img_active, (80, 140))

game_over_img = pygame.image.load("assets/jeumontee/over3.png")
game_over_img = pygame.transform.scale(game_over_img, (300, 100))

def addScore():
    general.globals.ACTUALSCORE += 1


class JeuMontee:
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.initialiser_jeu()

    def initialiser_son(self):
        self.soundgame = pygame.mixer.Sound("assets/jeumontee/soundgame.mp3")
        self.soundgame.set_volume(0.5)
        self.soundgame.play(loops=-1)

    def initialiser_jeu(self):
        # Charger les sons
        self.personnage = pygame.Rect(LARGEUR_FENETRE // 2 - LARGEUR_PERSONNAGE // 2, HAUTEUR_FENETRE - HAUTEUR_SURFACE - HAUTEUR_PERSONNAGE, LARGEUR_PERSONNAGE, HAUTEUR_PERSONNAGE)
        self.vies = 3
        self.score = 0
        self.jeu_termine = False
        self.jeu_demarre = False
        self.game_over = False
        self.sur_echelle = False
        self.collision_active = False  # Indique si la collision avec la porte est active
        self.temps_collision = 0  # Temps restant pour permettre la collision
        self.surfaces = [pygame.Rect(0, HAUTEUR_FENETRE - HAUTEUR_SURFACE, LARGEUR_FENETRE, HAUTEUR_SURFACE)]
        self.echelles = []
        self.pieges = []
        self.portes = []
        dernier_x_echelle = random.randint(MIDDLE_THIRD_START, MIDDLE_THIRD_END - LARGEUR_ECHELLE)
        self.echelles.append(pygame.Rect(dernier_x_echelle, self.surfaces[0].y - HAUTEUR_ECHELLE, LARGEUR_ECHELLE, HAUTEUR_ECHELLE))
        self.texte_score = police.render(f"Score : {self.score}", True, NOIR)
        self.texte_vies = police.render(f"Vies : {self.vies}", True, NOIR)
        for i in range(1, 5):
            hauteur_surface = self.surfaces[i - 1].y - ESPACE_ENTRE_PLATEFORMES
            self.surfaces.append(pygame.Rect(0, hauteur_surface, LARGEUR_FENETRE, HAUTEUR_SURFACE))

            while True:
                nouveau_x_echelle = random.randint(MIDDLE_THIRD_START, MIDDLE_THIRD_END - LARGEUR_ECHELLE)
                if abs(nouveau_x_echelle - dernier_x_echelle) >= DISTANCE_MINIMALE_ECHELLES:
                    break
            dernier_x_echelle = nouveau_x_echelle
            self.echelles.append(pygame.Rect(nouveau_x_echelle, hauteur_surface - HAUTEUR_ECHELLE, LARGEUR_ECHELLE, HAUTEUR_ECHELLE))

        if IMAGE_FOND_ACTIVE:
            self.image_fond = pygame.image.load(CHEMIN_IMAGE_FOND)
            self.image_fond = pygame.transform.scale(self.image_fond, (LARGEUR_FENETRE, HAUTEUR_FENETRE))

    def update(self):
        if not self.jeu_termine:
            touches = pygame.key.get_pressed()
            if touches[pygame.K_q] and self.personnage.x > 0:
                self.personnage.x -= 5
            if touches[pygame.K_d] and self.personnage.x < LARGEUR_FENETRE - LARGEUR_PERSONNAGE:
                self.personnage.x += 5

            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load("assets/jeumontee/soundgame.mp3")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)

            if self.score % SEUIL_SCORE == 0 and self.score != 0 and not self.collision_active:
                self.collision_active = True
                self.temps_collision = 300  # 5 secondes à 30 FPS (150 frames)
            if self.collision_active:
                self.temps_collision -= 1
                if self.temps_collision <= 0:
                    self.collision_active = False
            if self.collision_active:
                for porte in self.portes:
                    if self.personnage.colliderect(porte):
                        self.jeu_termine = True

            if self.collision_active:
                texte_collision = police.render("Collision possible !", True, (255, 0, 0))
                self.screen.blit(texte_collision, (LARGEUR_FENETRE // 2 - texte_collision.get_width() // 2, 10))

            if not self.sur_echelle:
                self.personnage.y += gravite

            self.sur_echelle = False
            for echelle in self.echelles:
                if self.personnage.colliderect(echelle):
                    self.sur_echelle = True
                    if touches[pygame.K_z]:
                        self.personnage.y -= 5
                    if touches[pygame.K_s]:
                        self.personnage.y += 5
                    break

            sur_surface = False
            for surface in self.surfaces:
                if self.personnage.colliderect(surface) and self.personnage.bottom <= surface.bottom + 5:
                    sur_surface = True
                    self.personnage.y = surface.y - HAUTEUR_PERSONNAGE
                    break
#Quand le personnage n'est plus sur la premiere plateforme le jeu demarre
            if self.personnage.bottom < self.surfaces[0].y and not self.jeu_demarre:
                self.jeu_demarre = True

            if self.jeu_demarre:
                for surface in self.surfaces:
                    surface.y += VITESSE_DEFILEMENT
                for echelle in self.echelles:
                    echelle.y += VITESSE_DEFILEMENT
                for porte in self.portes:
                    porte.y += VITESSE_DEFILEMENT
                self.score += 1 # augmente le score
                general.globals.ACTUALSCORE += 1

            if random.randint(1, 100) <= 5:
                nouveau_piege = pygame.Rect(random.randint(0, LARGEUR_FENETRE - 20), -20, 20, 20)
                self.pieges.append(nouveau_piege)

            for piege in self.pieges[:]:
                piege.y += VITESSE_PIEGES
                if piege.top > HAUTEUR_FENETRE:
                    self.pieges.remove(piege)

            for piege in self.pieges:
                if self.personnage.colliderect(piege):
                    self.vies -= 1
                    self.pieges.remove(piege)
                    if self.vies <= 0:
                        self.game_over = True
                    break

            while self.surfaces[-1].y > 0:
                nouvelle_surface = pygame.Rect(0, self.surfaces[-1].y - ESPACE_ENTRE_PLATEFORMES, LARGEUR_FENETRE, HAUTEUR_SURFACE)
                self.surfaces.append(nouvelle_surface)
                dernier_x_echelle = random.randint(MIDDLE_THIRD_START, MIDDLE_THIRD_END - LARGEUR_ECHELLE)
                nouvelle_echelle = pygame.Rect(dernier_x_echelle, nouvelle_surface.y - HAUTEUR_ECHELLE, LARGEUR_ECHELLE, HAUTEUR_ECHELLE)
                self.echelles.append(nouvelle_echelle)
                nouvelle_porte = pygame.Rect(1225, nouvelle_surface.y - HAUTEUR_SURFACE - 85, 65, 80)

                self.portes.append(nouvelle_porte)

            if self.personnage.top > HAUTEUR_FENETRE:
                self.game_over = True

    def draw(self):
        if IMAGE_FOND_ACTIVE:
            self.screen.blit(self.image_fond, (0, 0))
        else:
            self.screen.fill(NOIR)

        for surface in self.surfaces:
            self.screen.blit(sol_img, surface)

        for echelle in self.echelles:
            self.screen.blit(echelle_img, echelle)

        for piege in self.pieges:
            self.screen.blit(piege_img, (piege.x, piege.y))

        if self.score >= 10:
            for porte in self.portes:
                if self.collision_active:
                    self.screen.blit(porte_img_active, (porte.x, porte.y))
                else:
                    self.screen.blit(porte_img, (porte.x, porte.y))

        self.screen.blit(personnage_img, (self.personnage.x, self.personnage.y))

        police = pygame.font.SysFont(None, 36)
        texte_score = police.render(f"Score : {self.score}", True, NOIR)
        texte_vies = police.render(f"Vies : {self.vies}", True, NOIR)
        self.screen.blit(texte_score, (10, 10))
        self.screen.blit(texte_vies, (10, 50))

        if self.jeu_termine:
            pygame.mixer.music.stop()
            pygame.time.delay(500)
            dialogue("Le château n'est plus très loin. Je touche au but.", 'zonePromenade', self.gameStateManager)


        if self.game_over:
            pygame.mixer.music.stop()
            self.initialiser_jeu()
            save_score()
            self.gameStateManager.set_state('gameover', game_over_img)
            general.globals.ACTUALSCORE = 0


    def run(self):
        self.update()
        self.draw()
        pygame.display.flip()

       # if self.jeu_termine and pygame.mouse.get_pressed()[0]:
#            if bouton_recommencer.collidepoint(pygame.mouse.get_pos()):
              #  self.initialiser_jeu()

