import pygame
import sys
from settings import Settings
from pygame.math import Vector2

class Seal():
    
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = Settings()
        self.seal_image = pygame.image.load("foka.png")
        self.rect = self.seal_image.get_rect()
        self.rect.midleft = self.screen.get_rect().midleft
        self.animation_frames = self.load_frames()
        self.initial_seal_pos = pygame.Vector2(10,self.settings.screen_height - 384)
        self.seal_pos = self.initial_seal_pos
        self.frame_index = 0
        self.frame_delay = 6
        self.speed = 3.5
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.moving_left_down = False
        self.moving_left_up = False
        self.moving_right_down = False
        self.moving_right_up = False

    def load_frames(self):
        frame_filenames = ['foka.png', 'foka1.png']
        frames = [pygame.image.load(filename) for filename in frame_filenames]
        return frames

    def animate_seal(self):
        if self.frame_delay == 0:
            self.seal_image = self.animation_frames[self.frame_index]
            self.frame_index = (self.frame_index + 1) % len(self.animation_frames)
            self.frame_delay = 30
        else:
            self.frame_delay -= 1

    def update(self):
        movement_vector = Vector2(0, 0)

        if self.moving_right:
            movement_vector.x += self.speed
        if self.moving_left:
            movement_vector.x -= self.speed
        if self.moving_up:
            movement_vector.y -= self.speed
        if self.moving_down:
            movement_vector.y += self.speed

        if self.moving_right_down:
            movement_vector += Vector2(self.speed, self.speed)
        if self.moving_right_up:
            movement_vector += Vector2(self.speed, -self.speed)
        if self.moving_left_down:
            movement_vector += Vector2(-self.speed, self.speed)
        if self.moving_left_up:
            movement_vector += Vector2(-self.speed, -self.speed)

        self.rect.move_ip(movement_vector)

        if self.rect.right > self.settings.screen_width:
            self.rect.right = self.settings.screen_width
        elif self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > self.settings.screen_height:
            self.rect.bottom = self.settings.screen_height
        elif self.rect.top < 0:
            self.rect.top = 0

    def blitme(self):
        self.animate_seal()
        self.screen.blit(self.seal_image, self.rect)
        