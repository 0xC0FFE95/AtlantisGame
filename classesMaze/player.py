import pygame

class Player:
    def __init__(self, x, y, size, speed, image, lives):
        """
        Initialise le joueur.
        """
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.image = pygame.transform.scale(image, (self.size, self.size))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.lives = lives

    def move(self, keys, maze):
        """
        Déplace le joueur tout en respectant les murs.
        """
        dx, dy = 0, 0
        if keys[pygame.K_q]:
            dx -= self.speed
        if keys[pygame.K_d]:
            dx += self.speed
        if keys[pygame.K_z]:
            dy -= self.speed
        if keys[pygame.K_s]:
            dy += self.speed

        # Calcul des nouvelles positions
        new_x = self.x + dx
        new_y = self.y + dy

        # Vérification des collisions avec les murs
        if maze.is_valid_area(new_x, self.y, self.size):  # Déplacement horizontal
            self.x = new_x
        if maze.is_valid_area(self.x, new_y, self.size):  # Déplacement vertical
            self.y = new_y

        # Mettre à jour la position du rectangle
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        """
        Dessine le joueur à l'écran.
        """
        screen.blit(self.image, (self.x, self.y))
