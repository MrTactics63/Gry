import pygame
from settings import Settings
from pygame.sprite import Sprite

class Fish(Sprite):

    def __init__(self,ai_game,x,y):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = Settings()
        self.image = pygame.image.load('Guppy Large Normal.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.x = x
        self.rect.y = self.rect.height
        self.rect.y = y
        self.x = float(self.rect.x)
        self.original_x = x  
        self.original_y = y
    
    def update(self):
        self.rect.x -= 4  # Poruszanie w lewo
        if self.rect.right < 0:
            self.rect.left = self.settings.screen_width
            
