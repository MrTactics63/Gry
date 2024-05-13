import sys
import pygame 
from time import sleep
from settings import Settings
from player import Player
from bullet import Bullet
from alien import Alien 
from gamestats import GameStats
from scoreboard import Scoreboard

class Menu():

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.font = pygame.font.SysFont(None, 48)
        self.start_button = pygame.image.load('newgame.png').convert_alpha()
        self.credits_button = pygame.image.load('credits.png').convert_alpha()
        self.exit_button = pygame.image.load('exit.png').convert_alpha()
        self.menu_bg = pygame.image.load('menu.png').convert_alpha()
        self.start_button_rect = self.start_button.get_rect(
            center=(self.settings.screen_width - 600, self.settings.screen_height - 550))
        self.credits_button_rect = self.credits_button.get_rect(
            center=(self.settings.screen_width - 600, self.settings.screen_height - 350 ))
        self.exit_button_rect = self.exit_button.get_rect(
            center=(self.settings.screen_width - 600, self.settings.screen_height - 150 ))

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
                        running = False
                        pygame.mixer.music.stop()
                        return Spaceshooter()
                    elif self.credits_button_rect.collidepoint(mouse_pos):
                        self.show_credits()
                    elif self.exit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
    
    def show_credits(self):
        credits_image = pygame.image.load('creditsmenu.png')
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


class Spaceshooter():
    
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Space Shooter')
        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load("background.png")
        self.laser_sound = pygame.mixer.Sound('laser_shooting_sfx.wav')
        self.player = Player(self)
        self.menu = Menu(self)
        self.engame = Endgame(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.running = True
        self.create_fleet()
    
    def run_menu(self):
        pygame.mixer.music.load('b423b42.wav')    
        pygame.mixer.music.play(-1)
        in_menu = True
        while in_menu:
            self.menu.display_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: 
                        if self.menu.handle_event():
                            in_menu = False
                            self.stats.reset_stats()
                        else:  
                            pygame.quit()
                            sys.exit()
        self.running = True
        self.run_game()
        
    def run_game(self):
        pygame.mixer.music.load('magic space.mp3')    
        pygame.mixer.music.play(-1)
        while True:
            self.check_events()
            if self.running == True:
                self.player.update()
                self.update_bullets()
                self.update_aliens()
            self.update_screen()
            self.clock.tick(60)
        
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)

    def check_keydown_events(self,event):
        if event.key == pygame.K_d:
            self.player.moving_right = True
        elif event.key == pygame.K_a:
            self.player.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()
        elif event.key == pygame.K_ESCAPE:
            return self.run_menu()

    def check_keyup_events(self,event):
        if event.key == pygame.K_d:
            self.player.moving_right = False
        elif event.key == pygame.K_a:
            self.player.moving_left = False

    def create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        level = 1
        while current_y <(self.settings.screen_height - 3 * alien_height):
            while current_x <(self.settings.screen_width - alien_width):
                self.create_alien(current_x,current_y,level)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height
            level += 1
    
    def create_alien(self,x_position,y_position,level):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        new_alien.level = level 
        self.aliens.add(new_alien)

    def fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
        self.laser_sound.play()
    def update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self.check_bullet_alien_collision()
    
    def check_bullet_alien_collision(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        
        if collisions:
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()

        if not self.aliens: 
            self.bullets.empty()
            self.create_fleet()
            self.stats.level += 1
            self.settings.increase_speed()

    def check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self.player_hit()
            self.check_aliens_bottom()

    def update_aliens(self):
        self.aliens.update()
        self.check_fleet_edges()
        if pygame.sprite.spritecollideany(self.player, self.aliens):
            self.player_hit()
            
    def check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break
    
    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def player_hit(self):
        self.stats.player_left -= 1
        self.bullets.empty()
        self.aliens.empty()
        self.create_fleet()
        self.player.center_player()
        sleep(0.5)
        
        end_game = Endgame(self)
        end_game.display_endgame()
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if end_game.end_button_rect.collidepoint(mouse_pos):
                        self.stats.reset_stats()
                        self.run_menu() 
                        return 

    def show_level(self):
        level_text = f"Poziom: {self.stats.level}"
        level_font = pygame.font.SysFont(None, 46)
        level_surface = level_font.render(level_text, True, (255, 255, 255))
        level_rect = level_surface.get_rect(topleft=(20, 20))
        self.screen.blit(level_surface, level_rect)

    def update_screen(self):
        self.screen.blit(self.bg,(0,0))
        self.player.blitme()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        self.show_level()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        pygame.display.flip()

class Endgame():

    def __init__(self,ai_game):
        self.screen = ai_game.screen 
        self.settings = ai_game.settings
        self.end_button = pygame.image.load('tryagain.png').convert_alpha()
        self.end_bg = pygame.image.load('endgame.png').convert_alpha()
        self.end_button_rect = self.end_button.get_rect(
            center=(self.settings.screen_width - 600, self.settings.screen_height - 400))
    
    def update(self):
        pass

    def display_endgame(self):
        self.screen.blit(self.end_bg, (0, 0))
        self.screen.blit(self.end_button, self.end_button_rect)
        pygame.display.flip()

    def back_to_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if self.end_button_rect.collidepoint(event.pos):
                            print('123')  # Debugging check
                            return Menu()

if __name__ == '__main__':
    ai = Spaceshooter()
    in_menu = ai.run_menu()
    if not in_menu: 
        ai.run_game()