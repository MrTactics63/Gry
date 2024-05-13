import sys
import pygame
from player import Player
from enemy import Enemy
from settings import Settings
from walkpath import Platform
from coin import Coin
from stats import Stats
from gamestats import Scoreboard
from pygame.locals import QUIT, MOUSEBUTTONDOWN

class Menu():
    
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.font = pygame.font.SysFont(None, 48)
        self.start_button = pygame.image.load('button1.png').convert_alpha()
        self.credits_button = pygame.image.load('button4.png').convert_alpha()
        self.exit_button = pygame.image.load('button2.png').convert_alpha()
        self.menu_bg = pygame.image.load('tlomenu.png').convert_alpha()
        self.start_button_rect = self.start_button.get_rect(
            center=(self.settings.screen_width // 2, self.settings.screen_height // 3.4))
        self.credits_button_rect = self.credits_button.get_rect(
            center=(self.settings.screen_width // 2, self.settings.screen_height // 2 - 50 ))
        self.exit_button_rect = self.exit_button.get_rect(
            center=(self.settings.screen_width // 2, self.settings.screen_height // 2 + 50))
    
    def display_menu(self):
        self.screen.blit(self.menu_bg, (0, 0))
        self.screen.blit(self.start_button, self.start_button_rect)
        self.screen.blit(self.credits_button, self.credits_button_rect)
        self.screen.blit(self.exit_button, self.exit_button_rect)
        pygame.display.flip()

    def handle_event(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.start_button_rect.collidepoint(mouse_pos):
                        self.menu_displayed = False
                        running = False
                        return Beatmyscore()
                    elif self.credits_button_rect.collidepoint(mouse_pos):
                        self.show_credits()
                    elif self.exit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

    def show_credits(self):
        credits_image = pygame.image.load('credits.png')
        self.screen.blit(credits_image,(0,0))
        pygame.display.flip()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return self.display_menu()
                    
class Beatmyscore:
    
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Beat my score')
        self.coin_sound = pygame.mixer.Sound('coin.mp3')
        self.clock = pygame.time.Clock()
        self.player = Player(self)
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.stats = Stats(self)
        self.scoreboard = Scoreboard(self)
        self.menu = Menu(self)
        self.bg_img = pygame.image.load('tlo.png').convert()
        self.bg_img_x = 0 
        self.running = True
        self._create_enemies()
        self._create_platform()
        self._create_coins()

    def run_menu(self):
        in_menu = True
        while in_menu:
            self.menu.display_menu()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if self.menu.handle_event():  # Start button clicked
                            in_menu = False
                        else:  # Exit button clicked
                            pygame.quit()
                            sys.exit()

        self.running = True
        self.run_game()

    def run_game(self):
        pygame.mixer.music.load('8bit attempt.mp3')  # Ładujemy plik muzyki
        pygame.mixer.music.play(-1)
        while self.running: 
            self._check_events() 
            self._update_screen()
            self._update_entities()
            self._update_entities2()
            self.clock.tick(60)
            pygame.display.flip()

    def _check_menu_events(self):  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.menu.check_button_click(mouse_pos)

    def _check_events(self):  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.player.moving_right = True
                elif event.key == pygame.K_a:
                    self.player.moving_left = True
                elif event.key == pygame.K_SPACE:
                    self.player.jump = True
                elif event.key == pygame.K_ESCAPE:
                    self.stats.game_active = False  
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.player.moving_right = False
                elif event.key == pygame.K_a:
                    self.player.moving_left = False
                elif event.key == pygame.K_SPACE:
                    self.player.jump = False

    def _update_screen(self):
        self.bg_img_x -= 2
        if self.bg_img_x <= -self.settings.screen_width:
            self.bg_img_x = 0

        self.screen.blit(self.bg_img, (self.bg_img_x, 0))
        self.screen.blit(self.bg_img, (self.bg_img_x + self.settings.screen_width, 0))

        self.player.blitme()
        self.enemies.draw(self.screen)
        self.coins.draw(self.screen)
        self.scoreboard.show_score()
   
        pygame.display.flip()

    def _create_enemies(self):
        for _ in range(2):
            enemy = Enemy(self, 600, self.settings.screen_height - 240)
            enemy2 = Enemy(self, 1300, self.settings.screen_height - 240)
            self.enemies.add(enemy, enemy2)

    def _create_platform(self):
        for _ in range(2):
            platform_width = self.settings.screen_width
            platform_height = 100
            platform = Platform(platform_width, platform_height)
            platform.rect.x = _ * self.settings.screen_width
            platform.rect.y = self.settings.screen_height - platform_height
            self.platforms.add(platform)  
            self.all_sprites.add(platform) 
    
    def _create_coins(self):
        for _ in range(1):
            coin = Coin(self, 1000, self.settings.screen_height - 600)
            self.coins.add(coin)

    def _update_entities(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
        platform_collisions = pygame.sprite.spritecollide(self.player, self.platforms, False)
        if platform_collisions:
            self.player.on_ground = True
            self.player.rect.bottom = platform_collisions[0].rect.top 
        else:
            self.player.on_ground = False
        enemy_collisions = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if enemy_collisions:
            for enemy in enemy_collisions:
                if self.player.rect.bottom < enemy.rect.centery: # Dodajemy warunek dotykania od góry
                    self.stats.score += 10
                    self.scoreboard.prep_score()
                    print("Przeskok nad wrogiem!")
                if self.player.rect.bottom > enemy.rect.top:
                    print("Zderzenie z wrogiem!")
                    self.running = False
                    end_game = Endgame(self)
                    end_game.draw_endgame_screen()
                    pygame.display.flip()
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            if end_game.restart_button_rect.collidepoint(mouse_pos):
                                self._reset_game()
                                self.return_to_menu()  # Return to the menu
                            waiting = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                sys.exit()  # Możesz dodać obsługę innych klawiszy
    
    def _update_entities2(self):
        self.player.update()
        for coin in self.coins:
            coin.update()
        platform_collisions = pygame.sprite.spritecollide(self.player, self.platforms, False)
        if platform_collisions:
            self.player.on_ground = True
            self.player.rect.bottom = platform_collisions[0].rect.top 
        else:
            self.player.on_ground = False
        coin_collisions = pygame.sprite.spritecollide(self.player, self.coins, True)
        if coin_collisions:
            for coin in coin_collisions:
                self.stats.score += 10   
                self._create_coins()
                self.scoreboard.prep_score()
                self.coin_sound.play()
                print('Zebrano monetę')

    def _reset_game(self):
        self.game_over = False
    
    def return_to_menu(self):
        self.running = False  
        self.stats.score = 0
        self.player.rect.x = 50  
        self.player.rect.y = self.settings.screen_height - 150
        self.enemies.empty()
        self.coins.empty()  
        self._create_enemies()  
        self._create_platform()  
        self._create_coins()  
        self.run_menu()

class Endgame():
    
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.eg_bg_img = pygame.image.load('endgame.png')
        self.restart_button = pygame.image.load('button3.png')
        self.restart_button_rect = self.restart_button.get_rect(
            center=(self.settings.screen_width // 2, self.settings.screen_height // 2 - 50))

    def update(self):
        pass

    def draw_endgame_screen(self):
        self.screen.blit(self.eg_bg_img, (0, 0))
        self.screen.blit(self.restart_button, self.restart_button_rect)
    
    def back_to_main_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if self.restart_button_rect.collidepoint(event.pos):
                            print('123')  # Debugging check
                            return Menu()
                        
if __name__ == '__main__':
    ai = Beatmyscore()
    in_menu = ai.run_menu()
    if not in_menu:  # Jeśli użytkownik wybrał rozpoczęcie gry
        ai.run_game()