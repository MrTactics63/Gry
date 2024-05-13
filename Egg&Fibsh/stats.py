import pygame
from scoreboard import Scoreboard
from seal import Seal

class Stats:
    def __init__(self,ai_game):
        self.game_active = False
        self.score = 0

    def reset_stats(self):
        self.score = 0