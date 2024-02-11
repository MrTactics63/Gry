import sys
import math
import pygame
from pygame.locals import *
from settings import Settings
from dino import Dino
from coin import Coin
from random import randint

class MainMenu:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.font = pygame.font.SysFont(None, 48)
        self.start_button = pygame.image.load('button1.png').convert_alpha()
        self.exit_button = pygame.image.load('button2.png').convert_alpha()
        self.menu_bg = pygame.image.load('junglemenu.png').convert_alpha()
    
    def display_menu(self):
        self.screen.blit(self.menu_bg, (0, 0))
        self.screen.blit(self.start_button, (self.settings.screen_width // 2 - self.start_button.get_width() // 2,
                                             self.settings.screen_height // 2 - 50))
        self.screen.blit(self.exit_button, (self.settings.screen_width // 2 - self.exit_button.get_width() // 2,
                                            self.settings.screen_height // 2 + 50))
        pygame.display.flip()

    def handle_event(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return True  # Return to main menu
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        start_button_rect = self.start_button.get_rect()
                        start_button_rect.center = (self.settings.screen_width // 2, self.settings.screen_height // 2 - 50)
                        exit_button_rect = self.exit_button.get_rect()
                        exit_button_rect.center = (self.settings.screen_width // 2, self.settings.screen_height // 2 + 50)
                        if start_button_rect.collidepoint(event.pos):
                            return False  # Start the game
                        elif exit_button_rect.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()

class Dinorunner:
    
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Dino runner")
        self.clock = pygame.time.Clock()
        self.running = True
        self.main_menu = MainMenu(self.screen, self.settings)
        pygame.mixer.music.load('chill_jungle_ambient.wav')  # Load the music file
        pygame.mixer.music.play(-1)
    
    def run_game(self):
        while self.running:
            if self.show_menu():
                continue  # Go back to main menu
            self.play_game()
    
    def show_menu(self):
        self.main_menu.display_menu()
        return self.main_menu.handle_event()

    def play_game(self):
        bg = pygame.image.load('jungle.png').convert_alpha()
        bg_width = bg.get_width()
        tiles = math.ceil(self.settings.screen_width / bg_width) + 1 
        scroll = 0
        dino = Dino(self)  # Modified here
        coin_manager = CoinManager(self)
        score_frame = pygame.image.load('ramka.png').convert_alpha()  # Ramka na wynik
        score_frame_rect = score_frame.get_rect()
        score_frame_rect.topright = (self.settings.screen_width, 0)  # Prawy górny róg ekranu
        score_font = pygame.font.SysFont(None, 48)  # font dla wyniku monet

        while True:
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        dino.jump()
                    elif event.key == pygame.K_ESCAPE:
                        return  # Return to main menu

            dino.update()
            coin_manager.update(scroll)  # aktualizacja monet
            coin_manager.check_collisions(dino)  # Modified here
            
            scroll -= 5
            if abs(scroll) > bg_width:
                scroll = 0

            self.screen.blit(bg, (scroll, 0))
            self.screen.blit(bg, (scroll + bg_width, 0))
            for i in range(0, tiles):
                self.screen.blit(bg, (i * bg_width + scroll, 0))
            dino.blitme()
            coin_manager.draw()  # Tutaj rysujemy monety
            
            # Wyświetlanie ramki wyniku
            self.screen.blit(score_frame, score_frame_rect)
            
            # Wyświetlanie wyniku w ramce
            score_text = score_font.render(f"Wynik: {coin_manager.coin_score}", True, (255, 255, 255))
            score_rect = score_text.get_rect()
            score_rect.center = score_frame_rect.center
            self.screen.blit(score_text, score_rect)
            
            pygame.display.flip()
            self.clock.tick(60)
            
            
class CoinManager:
    
    def __init__(self, dino_game):
        self.screen = dino_game.screen
        self.screen_rect = self.screen.get_rect()
        self.coins = pygame.sprite.Group()
        self.coin_delay = 100  # opóźnienie w klatkach przed kolejnym pojawieniem się monety
        self.coin_timer = 0
        self.coin_score = 0
        self.coin_font = pygame.font.SysFont(None, 48)  # font dla wyniku monet

    def create_coin(self):
        coin = Coin(self)
        coin.rect.x = randint(0, self.screen_rect.width - coin.rect.width)
        coin.rect.y = randint(0, self.screen_rect.height - coin.rect.height)
        self.coins.add(coin)

    def update(self, scroll):
        self.coins.update()
        if self.coin_timer == self.coin_delay:
            self.create_coin()
            self.coin_timer = 0
        else:
            self.coin_timer += 1

        # Aktualizuj pozycję monet wraz z przesunięciem tła
        for coin in self.coins:
            coin.rect.x += scroll / 80

    def check_collisions(self, dino):
        collisions = pygame.sprite.spritecollide(dino, self.coins, True)
        self.coin_score += len(collisions)

    def draw(self):
        self.coins.draw(self.screen)

if __name__ == "__main__":
    dino_game = Dinorunner()
    dino_game.run_game()
