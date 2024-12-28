import pygame
import sys
import time

def dialogue(message, zone, gameStateManager):
    pygame.init()

    # Utiliser la taille de la fenêtre définie dans Game
    screen = pygame.display.get_surface()
    WIDTH, HEIGHT = screen.get_width(), screen.get_height()

    pygame.display.set_caption("Dialogue Scene")

    # Couleurs
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Charger les images
    background_image = pygame.image.load("assets/combat2D/fondfight.png")
    character_image = pygame.image.load("assets/dialogue/mob1.png")
    arrow_image = pygame.image.load("assets/dialogue/arrow_right.png")  # Assurez-vous d'avoir cette image

    # Redimensionner les images si nécessaire
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    # Obtenir les dimensions de l'image du personnage
    character_width, character_height = character_image.get_size()

    # Position du personnage au centre gauche de l'écran
    character_x = -200
    character_y = (HEIGHT - character_height) // 2

    # Font pour le texte
    font = pygame.font.Font(None, 36)

    # Texte à afficher
    dialogue = message

    # Variables pour gérer le défilement du texte
    text_displayed = ""
    text_index = 0
    text_speed = 0.05  # Vitesse du défilement (en secondes par caractère)
    last_update_time = time.time()

    # Position du bouton de la flèche droite
    arrow_width, arrow_height = arrow_image.get_size()
    arrow_x = WIDTH - arrow_width - 30
    arrow_y = HEIGHT - arrow_height - 30
    arrow_rect = pygame.Rect(arrow_x, arrow_y, arrow_width, arrow_height)

    # Boucle principale
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if arrow_rect.collidepoint(event.pos):
                    running = False  # Passe à l'étape suivante
                    gameStateManager.set_state(zone)  # Changer l'état du jeu en fonction de la zone passée

        # Afficher le fond
        screen.blit(background_image, (0, 0))

        # Afficher le personnage à sa taille d'origine
        screen.blit(character_image, (character_x, character_y))

        # Afficher la bulle de dialogue
        bubble_rect = pygame.Rect(20, HEIGHT - 150, WIDTH - 40, 130)
        pygame.draw.rect(screen, WHITE, bubble_rect)
        pygame.draw.rect(screen, BLACK, bubble_rect, 2)  # Bordure noire

        # Gérer le défilement du texte
        current_time = time.time()
        if text_index < len(dialogue) and current_time - last_update_time > text_speed:
            text_displayed += dialogue[text_index]
            text_index += 1
            last_update_time = current_time

        # Diviser le texte en plusieurs lignes si nécessaire
        words = text_displayed.split(" ")
        lines = []
        current_line = words[0]

        for word in words[1:]:
            if font.size(current_line + " " + word)[0] < bubble_rect.width - 20:
                current_line += " " + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)

        # Afficher le texte dans la bulle de dialogue
        y_offset = 0
        for line in lines:
            text_surface = font.render(line, True, BLACK)
            screen.blit(text_surface, (bubble_rect.x + 10, bubble_rect.y + 10 + y_offset))
            y_offset += font.get_height() + 2

        # Afficher la flèche droite
        screen.blit(arrow_image, (arrow_x, arrow_y))

        # Mettre à jour l'écran
        pygame.display.flip()

    # pygame.quit()
    # sys.exit()
