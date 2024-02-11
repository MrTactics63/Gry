import pygame

class Dino:

    def __init__(self, dino_game):
        self.screen = dino_game.screen
        self.settings = dino_game.settings
        self.screen_rect = dino_game.screen.get_rect()

        self.image = pygame.image.load('Run (1).png')
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.screen_rect.bottomleft

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.moving_right = False
        self.moving_left = False
        self.jump_count = 20
        self.is_jumping = False
        self.jump_velocity = 20

        self.walk_animation_frames_right = self.load_walk_frames('right')
        self.walk_frame_index = 0
        self.frame_delay = 5

    def load_walk_frames(self, direction):
        frame_filenames = ['Run (1).png', 'Run (2).png', 'Run (3).png', 'Run (4).png',
                           'Run (5).png', 'Run (6).png', 'Run (7).png', 'Run (8).png']
        frames = [pygame.image.load(filename) for filename in frame_filenames]
        return frames
    
    def animate_walk(self):
        if self.frame_delay == 0:
            self.image = self.walk_animation_frames_right[self.walk_frame_index]
            self.walk_frame_index = (self.walk_frame_index + 1) % len(self.walk_animation_frames_right)
            self.frame_delay = 5  
        else:
            self.frame_delay -= 1
    
    def jump(self):
        if self.rect.bottom >= 600:
            self.is_jumping = True

    def update(self):
        if self.moving_right:
            self.x += self.settings.dino_speed
        if self.moving_left:
            self.x -= self.settings.dino_speed
        if self.is_jumping:
            self.y -= self.jump_velocity
            self.jump_count -= 1
            if self.jump_count <= 0:
                self.is_jumping = False
                self.jump_count = 20
        else:
            if self.rect.bottom < self.screen_rect.bottom:
                self.y += self.settings.gravity

        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        self.animate_walk()
        self.screen.blit(self.image, self.rect)
