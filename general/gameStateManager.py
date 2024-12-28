import pygame

class GameStateManager:
    def __init__(self, initial_state):
        self.state = initial_state
        self.bg_img = None  # Initialize background image as None

    def get_state(self):
        return self.state

    def set_state(self, new_state, bg_img=None):
        self.state = new_state
        self.bg_img = bg_img 
