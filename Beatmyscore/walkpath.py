import pygame
from settings import Settings

class Platform(pygame.sprite.Sprite):
    def __init__(self,width,height):
        super().__init__()
        self.settings = Settings()
        self.platform_height = 100
        self.platform_width = self.settings.screen_width * 2
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.image.set_alpha(0)  # Przezroczysta
        self.rect = self.image.get_rect(topleft=(0, self.height - 100))  # 100 px od dołu ekranu

    def update(self):
        pass  # Platforma porusza się wraz z ekranem