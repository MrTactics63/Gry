import pygame
from settings import Settings

class Player(): 

    def __init__(self, ai_game):  
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.settings = Settings()
        self.player_img = pygame.image.load('marshmallow_earphone-01.png')
        self.rect = self.player_img.get_rect()  
        self.rect.midleft = self.screen.get_rect().midleft
        self.initial_player_pos = pygame.Vector2(10, self.settings.screen_height - 100)
        self.player_pos = self.initial_player_pos
        self.moving_right = False
        self.moving_left = False
        self.jump = False
        self.speed = 3
        self.gravity = 0.4
        self.jump_speed = 5
        self.on_ground = False

    def update(self):
        if self.moving_right:
            self.rect.x += self.speed
        elif self.moving_left:
            self.rect.x -= self.speed
        if self.jump:
            if self.on_ground:  
                self.jump_speed = -20
                self.on_ground = False
        self.rect.y += self.jump_speed
        self.jump_speed += self.gravity
        if self.rect.right > self.settings.screen_width:
            self.rect.right = self.settings.screen_width
        elif self.rect.left < 0:
            self.rect.left = 0
        for platform in self.settings.platforms:
            if self.rect.colliderect(platform.rect) and self.jump_speed >= 0:
                self.rect.bottom = platform.rect.top  
                self.jump_speed = 0  
                self.on_ground = True  

    def blitme(self):
        self.screen.blit(self.player_img, self.rect)