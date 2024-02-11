import pygame
from pygame.sprite import Sprite

class Coin(Sprite):

    def __init__(self, dino_game):
        super().__init__()
        self.screen = dino_game.screen
        self.screen_rect = dino_game.screen.get_rect()
        
        # Załaduj obraz monety
        self.image = pygame.image.load('moneta1.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

    def update(self):
        pass
    
    def blitme(self):
        self.screen.blit(self.image, self.rect)
