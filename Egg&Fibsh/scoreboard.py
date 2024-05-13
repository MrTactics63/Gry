import pygame
import pygame.font

class Scoreboard():
    def __init__(self,ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings 
        self.stats = ai_game.stats
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,48)
        self.prep_score()

    def prep_score(self):

        score_str = str(self.stats.score)  
        self.score_image = self.font.render(score_str, True, self.text_color)  
        self.score_rect = self.score_image.get_rect()  
        self.score_rect.right = self.screen_rect.right - 50
        self.score_rect.top = 20

        self.score_text = "Wynik"
        self.score_text_image = self.font.render(self.score_text, True, self.text_color)
        self.score_text_rect = self.score_text_image.get_rect()
        self.score_text_rect.right = self.score_rect.left - 10  # Umieść obrazek "Wynik" obok obrazka punktacji
        self.score_text_rect.centery = self.score_rect.centery  # Wyśrodkuj pionowo

    def update(self):
        pass 

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.score_text_image, self.score_text_rect)