import pygame
import general.globals
from general.globals import ACTUALSCORE

class Timer:
    def __init__(self, total_time):
        self.total_time = total_time  # Temps total en secondes
        self.start_ticks = pygame.time.get_ticks()

    def get_time_left(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_ticks) // 1000
        return max(self.total_time - elapsed_time, 0)

    def add_time_score(self):

        remaining_time = self.get_time_left()

        general.globals.ACTUALSCORE += remaining_time // 10 # 1 point toutes les 10 secondes restantes.

    def draw(self, screen, font, x, y):
        time_left = self.get_time_left()
        timer_surface = font.render(f"Time: {time_left}s", True, (255, 255, 255))
        screen.blit(timer_surface, (x, y))

    def is_time_up(self):
        return self.get_time_left() <= 0
