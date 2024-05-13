import pygame
from pygame.sprite import Sprite
from settings import Settings

class Coin(Sprite):
    def __init__(self, ai_game, x, y):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.settings = Settings()
        self.image = pygame.image.load('piece.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = float(self.rect.x)
    
    def update(self):
        self.rect.x -= 4  # Move left
        if self.rect.right < 0:
            self.rect.left = self.settings.screen_width
            self.rect.centery = self.settings.screen_height - 600