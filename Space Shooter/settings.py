import sys

class Settings():
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.alien_speed = 2.0 
        self.fleet_drop_speed = 2.0
        self.fleet_direction = 1
        self.player_speed = 4.0
        self.player_limit = 3
        self.speedup_scale = 1.1 
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.alien_speed = 2.0
        self.alien_points = 50 

    def increase_speed(self):
        self.alien_speed *= self.speedup_scale
        self.fleet_drop_speed *= self.speedup_scale