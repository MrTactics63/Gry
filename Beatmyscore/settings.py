import pygame

class Settings():
    def __init__(self):
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_img = pygame.image.load('tlo.png')
        self.gravity = 0.4
        self.fall_speed = 0
        self.platforms = []