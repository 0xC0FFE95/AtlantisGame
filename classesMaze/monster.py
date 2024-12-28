import pygame
import random

class Monster:
    def __init__(self, x, y, size, speed, image):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.image = pygame.transform.scale(image, (self.size, self.size))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])

    def move(self, maze, player_position):
        distance_to_player = ((self.x - player_position[0]) ** 2 + (self.y - player_position[1]) ** 2) ** 0.5

        if distance_to_player < 200:  # Si le joueur est proche
            self.follow_player(maze, player_position)
        else:
            self.random_move(maze)

    def random_move(self, maze):
        dx, dy = self.direction[0] * self.speed, self.direction[1] * self.speed
        new_x, new_y = self.x + dx, self.y + dy

        # Vérifie les collisions
        if maze.is_valid_area(new_x, self.y, self.size):
            self.x = new_x
        else:
            self.change_direction()

        if maze.is_valid_area(self.x, new_y, self.size):
            self.y = new_y
        else:
            self.change_direction()

        self.rect.topleft = (self.x, self.y)

    def follow_player(self, maze, player_position):
        dx = player_position[0] - self.x
        dy = player_position[1] - self.y

        if abs(dx) > abs(dy):  # Priorité aux déplacements horizontaux
            new_x = self.x + self.speed if dx > 0 else self.x - self.speed
            if maze.is_valid_area(new_x, self.y, self.size):
                self.x = new_x
            else:
                self.change_direction()
        else:  # Déplacement vertical
            new_y = self.y + self.speed if dy > 0 else self.y - self.speed
            if maze.is_valid_area(self.x, new_y, self.size):
                self.y = new_y
            else:
                self.change_direction()

        self.rect.topleft = (self.x, self.y)

    def change_direction(self):
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
