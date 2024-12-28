import pygame
import sys
import os
import general.globals
# Import des constantes ou variables globales (assurez-vous qu'elles sont définies quelque part)
from general.globals import *
from general.dialogue import dialogue


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def save_score():
    with open("scores.txt", "a") as file:
        file.write(f"{general.globals.PLAYERNAME} - {general.globals.ACTUALSCORE}\n")

def load_scores():
    if not os.path.exists("scores.txt"):
        return []
    with open("scores.txt", "r") as file:
        scores = file.readlines()
    
    # Convertir les scores en tuples (nom, score)
    scores = [score.strip().split(" - ") for score in scores]
    scores = [(name, int(score)) for name, score in scores]
    
    # Trier les scores par ordre décroissant
    scores.sort(key=lambda x: x[1], reverse=True)
    
    # Retourner les 10 meilleurs scores
    top_scores = scores[:10]
    
    # Convertir les scores en chaînes de caractères
    top_scores = [f"{name} - {score}" for name, score in top_scores]
    
    return top_scores

class Menu:
    def __init__(self, screen, gameStateManager):
        self.screen = screen  # Utilisation de la fenêtre passée depuis Game
        self.gameStateManager = gameStateManager
        self.init_menu()

    def init_menu(self):
        self.WIDTH, self.HEIGHT = self.screen.get_width(), self.screen.get_height()  # Taille de la fenêtre
        pygame.display.set_caption("Atlantis Menu")

        self.WHITE = (255, 255, 255)
        self.GOLD = (255, 215, 0)
        self.DARK_BLUE = (10, 25, 50)

        # Charger le fond
        self.background_image = pygame.image.load("assets/menu/fondmenu.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))

        # Police pour le texte
        self.font_title = pygame.font.SysFont("timesnewroman", 64)
        self.font_menu = pygame.font.SysFont("timesnewroman", 36)

        # Boutons
        self.button_play = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT // 2 - 80, 200, 50)
        self.button_scores = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT // 2, 200, 50)
        self.button_quit = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT // 2 + 80, 200, 50)

    def enter_name(self):
        player_name = ""
        active = False
        input_rect = pygame.Rect(self.WIDTH // 2 - 150, self.HEIGHT // 2 - 25, 300, 50)
        button_next = pygame.Rect(self.WIDTH - 120, self.HEIGHT - 70, 100, 50)
        button_back = pygame.Rect(20, 20, 100, 50)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_back.collidepoint(event.pos):
                        running = False  
                        return
                    if button_next.collidepoint(event.pos) and player_name.strip():
                        running = False
                        # self.gameStateManager.set_state('zonePromenade')
                        dialogue("Je dois me rendre au château afin de terrasser l'être maléfique qui s'y trouve.", 'zonePromenade', self.gameStateManager)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]  
                    else:
                        player_name += event.unicode
                        general.globals.PLAYERNAME = player_name

            self.screen.fill(self.DARK_BLUE)
            draw_text("Enter Your Name", self.font_title, self.GOLD, self.screen, self.WIDTH // 2, 50)

            # Zone de saisie
            pygame.draw.rect(self.screen, self.WHITE, input_rect)
            pygame.draw.rect(self.screen, self.GOLD, input_rect, 2)
            draw_text(player_name, self.font_menu, self.DARK_BLUE, self.screen, input_rect.centerx, input_rect.centery)

            # Boutons
            pygame.draw.rect(self.screen, self.GOLD, button_next)
            draw_text("Next", self.font_menu, self.DARK_BLUE, self.screen, button_next.centerx, button_next.centery)
            pygame.draw.rect(self.screen, self.GOLD, button_back)
            draw_text("Back", self.font_menu, self.DARK_BLUE, self.screen, button_back.centerx, button_back.centery)

            pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_play.collidepoint(event.pos):
                        running = False
                        self.enter_name()  # Aller à l'écran de saisie du nom
                    if self.button_scores.collidepoint(event.pos):
                        self.show_scores()
                    if self.button_quit.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            self.screen.blit(self.background_image, (0, 0))

            draw_text("Atlantis", self.font_title, self.GOLD, self.screen, self.WIDTH // 2, self.HEIGHT // 4)

            pygame.draw.rect(self.screen, self.DARK_BLUE, self.button_play)
            pygame.draw.rect(self.screen, self.DARK_BLUE, self.button_scores)
            pygame.draw.rect(self.screen, self.DARK_BLUE, self.button_quit)
            pygame.draw.rect(self.screen, self.GOLD, self.button_play, 2)
            pygame.draw.rect(self.screen, self.GOLD, self.button_scores, 2)
            pygame.draw.rect(self.screen, self.GOLD, self.button_quit, 2)


            draw_text("Play", self.font_menu, self.WHITE, self.screen, self.button_play.centerx, self.button_play.centery)
            draw_text("Scores", self.font_menu, self.WHITE, self.screen, self.button_scores.centerx, self.button_scores.centery)
            draw_text("Quit", self.font_menu, self.WHITE, self.screen, self.button_quit.centerx, self.button_quit.centery)

            pygame.display.flip()

    def show_scores(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return 

            self.screen.fill(self.DARK_BLUE)

            draw_text("Scores", self.font_title, self.GOLD, self.screen, self.WIDTH // 2, 50)
            scores = load_scores()
            for i, score in enumerate(scores):
                draw_text(score, self.font_menu, self.WHITE, self.screen, self.WIDTH // 2, 150 + i * 50)

            pygame.draw.rect(self.screen, self.GOLD, pygame.Rect(20, 20, 100, 50))
            draw_text("Back", self.font_menu, self.DARK_BLUE, self.screen, 70, 45)

            pygame.display.flip()
