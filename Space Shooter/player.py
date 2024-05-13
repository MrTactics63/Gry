import sys 
import pygame 
from settings import Settings

class Player():
    def __init__(self,ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect() 
        self.image = pygame.image.load("ship3.png")
        self.rect = self.image.get_rect()
        self.animation_frames = self.load_frames()
        self.frame_index = 0
        self.frame_delay = 3
        self.rect.midbottom = self.screen_rect.midbottom
        self.moving_right = False
        self.moving_left = False 
        self.player_speed = 4.0
        self.x = float(self.rect.x)

    def load_frames(self):
        frame_filenames = ['ship3.png', 'ship4.png']
        frames = [pygame.image.load(filename) for filename in frame_filenames]
        return frames
    
    def animate_ship(self):
        if self.frame_delay == 0:
            self.image = self.animation_frames[self.frame_index]
            self.frame_index = (self.frame_index + 1) % len(self.animation_frames)
            self.frame_delay = 30
        else:
            self.frame_delay -= 1

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.player_speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.player_speed
    
    def center_player(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)
        self.animate_ship()