import pygame
from pygame.sprite import Sprite
from settings import Settings

class Enemy(pygame.sprite.Sprite):
    def __init__(self,ai_game,x,y):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = Settings()
        self.image = pygame.image.load('rock-obstacle1.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.x = x
        self.rect.y = self.rect.height
        self.rect.y = y
        self.x = float(self.rect.x)
    
    def update(self):
        self.rect.x -= 7  # Poruszanie w lewo
        if self.rect.right < 0:
            self.rect.left = self.settings.screen_width
            self.rect.centery = self.settings.screen_height - 170