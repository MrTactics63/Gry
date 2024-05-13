import pygame
import sys
from settings import Settings
from seal import Seal 
from fish import Fish
from octopus import Octopus
from predator import Predator
from predator1 import Predator1
from egg import Egg
from stats import Stats
from scoreboard import Scoreboard

class Menu():

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        pygame.mixer.init()
        pygame.mixer.music.load('Sea-side-Village.wav')
        pygame.mixer.music.play(-1) 
        self.font = pygame.font.SysFont(None, 48)
        self.start_button = pygame.image.load('sandstart.png').convert_alpha()
        self.credits_button = pygame.image.load('sandcredits.png').convert_alpha()
        self.exit_button = pygame.image.load('sandexit.png').convert_alpha()
        self.menu_bg = pygame.image.load('menu1.png').convert_alpha()
        self.start_button_rect = self.start_button.get_rect(
            center=(self.settings.screen_width - 330, self.settings.screen_height - 600))
        self.credits_button_rect = self.credits_button.get_rect(
            center=(self.settings.screen_width - 330, self.settings.screen_height - 400 ))
        self.exit_button_rect = self.exit_button.get_rect(
            center=(self.settings.screen_width - 330, self.settings.screen_height - 200 ))

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
                        pygame.mixer.music.stop()
                        return Gameloop()
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
                    
class Gameloop():
    
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.bg_img = pygame.image.load('Background.png').convert()
        self.bg_img_x = 0
        pygame.display.set_caption('Egg & Fibsh')
        pygame.mixer.init()
        pygame.mixer.music.load('oga_jam_menu_music_loopable.wav')
        pygame.mixer.music.play(-1) 
        self.player = Seal(self)
        self.menu = Menu(self)
        self.stats = Stats(self)
        self.scoreboard = Scoreboard(self)
        self.fishes = pygame.sprite.Group()
        self.octopuses = pygame.sprite.Group()
        self.predators = pygame.sprite.Group()
        self.predators1 = pygame.sprite.Group()
        self.eggs = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.running = True 
        self.create_fish1()
        self.create_fish2()
        self.create_fish3()
        self.create_fish4()
        self.create_octopuses()
        self.create_predators()
        self.create_predators1()
        self.create_eggs()
    
    def run_menu(self):
        pygame.mixer.music.load('Sea-side-Village.wav')
        pygame.mixer.music.play(-1) 
        in_menu = True
        while in_menu:
            self.menu.display_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if self.menu.handle_event():  # Start button clicked
                            in_menu = False
                        else:  # Exit button clicked
                            pygame.quit()
                            sys.exit()

        self.running = True
        self.run_game()

    def run_game(self):
        pygame.mixer.music.load('oga_jam_menu_music_loopable.wav')    
        pygame.mixer.music.play(-1)
        while self.running: 
            self.check_events() 
            self.update_screen()
            self.collision_seal_with_fishes()
            self.collision_seal_with_eggs()
            self.collision_seal_with_octopus()
            self.collision_seal_with_predator()
            self.collision_seal_with_predator1()
            self.clock.tick(200)
            pygame.display.flip()
        
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.player.moving_right = True
                elif event.key == pygame.K_a:
                    self.player.moving_left = True
                elif event.key == pygame.K_w:
                    self.player.moving_up = True
                elif event.key == pygame.K_s:
                    self.player.moving_down = True
                elif event.key == pygame.K_d and event.key == pygame.K_w:
                    self.player.moving_right_up = True
                elif event.key == pygame.K_d and event.key == pygame.K_s:
                    self.player.moving_right_down = True
                elif event.key == pygame.K_a and event.key == pygame.K_w:
                    self.player.moving_left_up = True
                elif event.key == pygame.K_a and event.key == pygame.K_s:
                    self.player.moving_left_down = True
                elif event.key == pygame.K_ESCAPE:
                    self.running = False 
                    sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.player.moving_right = False
                elif event.key == pygame.K_a:
                    self.player.moving_left = False
                elif event.key == pygame.K_w:
                    self.player.moving_up = False
                elif event.key == pygame.K_s:
                    self.player.moving_down = False
                elif event.key == pygame.K_d and event.key == pygame.K_w:
                    self.player.moving_right_up = False
                elif event.key == pygame.K_d and event.key == pygame.K_s:
                    self.player.moving_right_down = False
                elif event.key == pygame.K_a and event.key == pygame.K_w:
                    self.player.moving_left_up = False
                elif event.key == pygame.K_a and event.key == pygame.K_s:
                    self.player.moving_left_down = False

    def _check_menu_events(self):  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.menu.check_button_click(mouse_pos)

    def update_screen(self):
        
        self.bg_img_x -= 2
        if self.bg_img_x <= -self.settings.screen_width:
            self.bg_img_x = 0
        self.screen.blit(self.bg_img, (self.bg_img_x, 0))
        self.screen.blit(self.bg_img, (self.bg_img_x + self.settings.screen_width, 0))
        self.player.update()
        self.player.blitme()
        self.fishes.update()
        self.fishes.draw(self.screen)
        self.octopuses.update()
        self.octopuses.draw(self.screen)
        self.predators.update()
        self.predators.draw(self.screen)
        self.predators1.update()
        self.predators1.draw(self.screen)
        self.eggs.update()
        self.eggs.draw(self.screen)
        self.scoreboard.update()
        self.scoreboard.show_score()

    def create_fish1(self):
        for x, y in [(600, self.settings.screen_height - 700)]:
            fish1 = Fish(self, x, y)
            self.fishes.add(fish1)

    def create_fish2(self):
        for x, y in [(950, self.settings.screen_height - 400),]:
            fish2 = Fish(self, x, y)
            self.fishes.add(fish2)

    def create_fish3(self):
        for x, y in [(1300, self.settings.screen_height - 150)]:
            fish3 = Fish(self, x, y)
            self.fishes.add(fish3)

    def create_fish4(self):
        for x, y in [(1650, self.settings.screen_height - 400)]:
            fish4 = Fish(self, x, y)
            self.fishes.add(fish4)

    def create_octopuses(self):
        for _ in range(1):
            octopus1 = Octopus(self, self.settings.screen_width, self.settings.screen_height - 500)
            self.octopuses.add(octopus1)
    
    def create_predators(self):
        for _ in range(1):
            predator = Predator(self,self.settings.screen_width, self.settings.screen_height)
            self.predators.add(predator)
    
    def create_predators1(self):
        for _ in range(1):
            predator1 = Predator1(self,self.settings.screen_width, self.settings.screen_height)
            self.predators1.add(predator1)
    
    def create_eggs(self):
        for _ in range(1):
            eggs = Egg(self,self.settings.screen_width, self.settings.screen_height)
            self.eggs.add(eggs)

    def collision_seal_with_fishes(self):
        collision_seal_with_fishes = pygame.sprite.spritecollide(self.player, self.fishes, True)
        if collision_seal_with_fishes:
            for fish in collision_seal_with_fishes:
                new_x = fish.original_x
                new_y = fish.original_y
                while pygame.sprite.spritecollideany(Fish(self, new_x, new_y), self.fishes):
                    new_x += 0.9 
                    new_y += 0.9
                new_fish = Fish(self, new_x, new_y)
                new_fish_group = pygame.sprite.GroupSingle(new_fish)
                self.fishes.add(new_fish_group)
                self.stats.score += 10 
                self.scoreboard.prep_score()
                
    def collision_seal_with_eggs(self):
        collision_seal_with_eggs = pygame.sprite.spritecollide(self.player, self.eggs, True)
        if collision_seal_with_eggs:
            for eggs in collision_seal_with_eggs:
                self.create_eggs()
                self.stats.score += 20 
                self.scoreboard.prep_score()

    def collision_seal_with_octopus(self):
        collision_seal_with_octopus = pygame.sprite.spritecollide(self.player, self.octopuses, True)
        if collision_seal_with_octopus:
            for octopus in collision_seal_with_octopus:
                if self.player.rect.bottom > octopus.rect.top:
                    print("Zderzenie z wrogiem!")
                    self.running = False
                    end_game = Endgame(self)
                    end_game.display_endgame()
                    pygame.display.flip()
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            if end_game.end_button_rect.collidepoint(mouse_pos):
                                self.reset_game()
                                self.back_to_menu()  
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                sys.exit()  

    def collision_seal_with_predator(self):
        collision_seal_with_predator = pygame.sprite.spritecollide(self.player, self.predators, True)
        if collision_seal_with_predator:
            for predator in collision_seal_with_predator:
                if self.player.rect.bottom > predator.rect.top:
                    print("Zderzenie z wrogiem!")
                    self.running = False
                    end_game = Endgame(self)
                    end_game.display_endgame()
                    pygame.display.flip()
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            if end_game.end_button_rect.collidepoint(mouse_pos):
                                self.reset_game()
                                self.back_to_menu()  
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                sys.exit()  

    def collision_seal_with_predator1(self):
        collision_seal_with_predator1 = pygame.sprite.spritecollide(self.player, self.predators1, True)
        if collision_seal_with_predator1:
            for predator1 in collision_seal_with_predator1:
                if self.player.rect.bottom > predator1.rect.top:
                    print("Zderzenie z wrogiem!")
                    self.running = False
                    end_game = Endgame(self)
                    end_game.display_endgame()
                    pygame.display.flip()
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            if end_game.end_button_rect.collidepoint(mouse_pos):
                                self.reset_game()
                                self.back_to_menu()  
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                sys.exit()  

    def reset_game(self):
        self.game_over = False

    def back_to_menu(self):
        self.running = False
        self.player.rect.x = 10
        self.player.rect.y = self.settings.screen_height - 384
        self.player.moving_right = False
        self.player.moving_left = False
        self.player.moving_up = False
        self.player.moving_down = False
        self.player.moving_right_up = False
        self.player.moving_right_down = False
        self.player.moving_left_up = False
        self.player.moving_left_down = False
        self.stats.score = 0
        self.fishes.empty()
        self.octopuses.empty()
        self.predators.empty()
        self.predators1.empty()
        self.eggs.empty()
        self.create_fish1()
        self.create_fish2()
        self.create_fish3()
        self.create_fish4()
        self.create_octopuses()
        self.create_predators()
        self.create_predators1()
        self.create_eggs()
        return self.run_menu()

class Endgame():

    def __init__(self,ai_game):
        self.screen = ai_game.screen 
        self.settings = ai_game.settings
        self.end_button = pygame.image.load('sandend.png').convert_alpha()
        self.end_bg = pygame.image.load('endgame.png').convert_alpha()
        self.end_button_rect = self.end_button.get_rect(
            center=(self.settings.screen_width - 650, self.settings.screen_height - 350))
    
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
    ai = Gameloop()
    in_menu = ai.run_menu()
    if not in_menu: 
        ai.run_game()