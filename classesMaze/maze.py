import pygame
import random

class Maze:
    def __init__(self, rows, cols, wall_image, exit_image, screen_width, screen_height):
        self.rows = rows
        self.cols = cols
        self.cell_width = screen_width // cols
        self.cell_height = screen_height // rows
        self.wall_image = pygame.transform.scale(wall_image, (self.cell_width, self.cell_height))
        self.exit_image = pygame.transform.scale(exit_image, (self.cell_width, self.cell_height))
        self.maze_layout = self.generate_maze()
        self.exit_position = None  # La sortie est inactive au début

    def generate_maze(self):
        maze_layout = [
            ["1" if (i == 0 or j == 0 or i == self.rows - 1 or j == self.cols - 1) else "0" for j in range(self.cols)]
            for i in range(self.rows)
        ]
        for _ in range(self.rows * self.cols // 5):
            row = random.randint(1, self.rows - 2)
            col = random.randint(1, self.cols - 2)
            maze_layout[row][col] = "1"
        return maze_layout

    def find_free_position(self):
        while True:
            row = random.randint(1, self.rows - 2)
            col = random.randint(1, self.cols - 2)
            if self.maze_layout[row][col] == "0":
                x = col * self.cell_width
                y = row * self.cell_height
                return x, y

    def is_wall(self, x, y, size):
        col = x // self.cell_width
        row = y // self.cell_height
        if 0 <= col < self.cols and 0 <= row < self.rows:
            return self.maze_layout[row][col] == "1"
        return True

    def is_valid_area(self, x, y, size):
        return (
            not self.is_wall(x, y, size) and
            not self.is_wall(x + size - 1, y, size) and
            not self.is_wall(x, y + size - 1, size) and
            not self.is_wall(x + size - 1, y + size - 1, size)
        )

    def activate_exit(self):
        """
        Active la porte de sortie à une position libre dans le labyrinthe.
        """
        self.exit_position = self.find_free_position()
        print(f"Exit activated at {self.exit_position}")

    def get_exit_rect(self):
        """
        Retourne un rectangle pour la porte de sortie si elle est activée.
        """
        if self.exit_position:
            return pygame.Rect(self.exit_position[0], self.exit_position[1], self.cell_width, self.cell_height)
        return None

    def draw(self, screen):
        """
        Dessine le labyrinthe et la porte de sortie (si activée).
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.maze_layout[row][col] == "1":
                    screen.blit(self.wall_image, (col * self.cell_width, row * self.cell_height))
        if self.exit_position:
            screen.blit(self.exit_image, self.exit_position)
