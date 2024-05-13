import pygame
from settings import Settings
from pygame.sprite import Sprite

class Predator(Sprite):
    def __init__(self,ai_game,x,y):
        super().__init__()
        self.screen = ai_game.screen 
        self.settings = Settings()
        self.image = pygame.image.load('Predator Sick.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.x = self.rect.width + 200
        self.x = float(self.rect.x)
        self.rect.y = y
        self.rect.y = self.rect.height + 510

    def update(self):
        self.rect.x -= 3
        if self.rect.right < 0:
            self.rect.left = self.settings.screen_width