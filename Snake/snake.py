import pygame
from random import randrange
import sys

class SnakeSegment(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.apple_image = pygame.image.load('jablko.png').convert_alpha()
        self.background_image = pygame.image.load('tlo.png').convert()
        self.snake_image = pygame.image.load('wonsz.png').convert_alpha()
        self.snake_segments = []
        self.apple_rect = self.apple_image.get_rect(topleft=(randrange(0, self.screen_width - 50, 50),
                                                             randrange(0, self.screen_height - 50, 50)))
        self.score = 0
        self.lives = 3
        self.font = pygame.font.SysFont(None, 36)
        self.snake_dir = (0, 0)
        self.game_over = False
        self.menu_displayed = True
        self.high_scores = []  
        self.game_over_text_shown = False  

    def run_game(self):
        while True:
            if self.menu_displayed:
                self.show_start_screen()
            else:
                self.start_new_game()

    def show_start_screen(self):
        self.start_button = pygame.image.load('nowagra.png')
        self.score_button = pygame.image.load('tablica.png')
        self.quit_button = pygame.image.load('wyjscie.png')
        self.logo = pygame.image.load('pygame_logo.png')
        button_width = self.start_button.get_width()
        button_height = self.start_button.get_height()
        button_x = (self.screen_width - button_width) / 2
        button_y = (self.screen_height - 3 * button_height) / 2
        start_button_rect = self.start_button.get_rect(topleft=(button_x, button_y))
        score_button_rect = self.score_button.get_rect(topleft=(button_x, button_y + button_height + 20))
        quit_button_rect = self.quit_button.get_rect(topleft=(button_x, button_y + 2 * (button_height + 20)))
        # Ustawienia logo
        logo_x = (self.screen_width - self.logo.get_width()) / 2
        logo_y = 50  
        logo_rect = self.logo.get_rect(topleft=(logo_x, logo_y))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button_rect.collidepoint(mouse_pos):
                        self.menu_displayed = False
                        running = False
                    elif score_button_rect.collidepoint(mouse_pos):
                        self.show_high_scores()
                    elif quit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.logo, logo_rect)
            self.screen.blit(self.start_button, start_button_rect)
            self.screen.blit(self.score_button, score_button_rect)
            self.screen.blit(self.quit_button, quit_button_rect)

            pygame.display.flip()

    def show_high_scores(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            self.screen.blit(self.background_image, (0, 0))
            text_y = 50
            title_font = pygame.font.SysFont(None, 48)
            title_text = title_font.render("Najlepsze wyniki", True, (255, 255, 255))
            self.screen.blit(title_text, ((self.screen_width - title_text.get_width()) / 2, 10))
            for player, score in self.high_scores:
                score_text = self.font.render(f"{player}: {score}", True, (255, 255, 255))
                self.screen.blit(score_text, ((self.screen_width - score_text.get_width()) / 2, text_y))
                text_y += 40
            pygame.display.flip()

    def start_new_game(self):
        self.menu_displayed = False  
        self.snake_segments = [SnakeSegment(150, 100, pygame.image.load('wonsz.png').convert_alpha())]
        self.game_over_text_shown = False  
        self.game_over = False
        self.score = 0
        self.lives = 3
        self.snake_dir = (0, 0)
        self.apple_rect.x = randrange(0, self.screen_width - 50, 50)
        self.apple_rect.y = randrange(0, self.screen_height - 50, 50)
        self.run_game_loop()

    def run_game_loop(self):
        while not self.game_over:
            self.handle_events()
            self.update_snake()
            self.check_collisions()
            self.update_screen()
            self.clock.tick(6)

    def show_game_over_screen(self):
        
        game_over_font = pygame.font.SysFont('Arial', 48)
        game_over_text = game_over_font.render("Koniec gry! Podaj swoje imię:", True, (255, 255, 255))
        game_over_text_rect = game_over_text.get_rect(center=(self.screen_width // 2, 200)) 
        self.screen.blit(game_over_text, game_over_text_rect)
        pygame.display.flip()
        self.game_over_text_shown = True
        player_name = self.get_player_name()
        self.high_scores.append((player_name, self.score))
        self.high_scores.sort(key=lambda x: x[1], reverse=True)
        self.menu_displayed = True
        
    def get_player_name(self):
        
        input_box = pygame.Rect((self.screen_width - 200) / 2, (self.screen_height - 32) / 2, 200, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Set input box active when player clicks on it
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    # Change input box color
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            running = False
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
            self.screen.blit(self.background_image, (0, 0))
            pygame.draw.rect(self.screen, color, input_box, 2)
            font = pygame.font.Font(None, 32)
            text_surface = font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
            pygame.display.flip()
        return text

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and self.snake_dir != (0, 50):  # Poprawka: Wąż nie może iść w dół, jeśli porusza się w górę
                    self.snake_dir = (0, -50)
                elif event.key == pygame.K_s and self.snake_dir != (0, -50):  # Poprawka: Wąż nie może iść w górę, jeśli porusza się w dół
                    self.snake_dir = (0, 50)
                elif event.key == pygame.K_a and self.snake_dir != (50, 0):  # Poprawka: Wąż nie może iść w prawo, jeśli porusza się w lewo
                    self.snake_dir = (-50, 0)
                elif event.key == pygame.K_d and self.snake_dir != (-50, 0):  # Poprawka: Wąż nie może iść w lewo, jeśli porusza się w prawo
                    self.snake_dir = (50, 0)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def update_snake(self):

        new_head = SnakeSegment(self.snake_segments[0].rect.x + self.snake_dir[0],
                                self.snake_segments[0].rect.y + self.snake_dir[1],
                                self.snake_image)
        self.snake_segments.insert(0, new_head)
        if self.snake_segments[0].rect.colliderect(self.apple_rect):
            self.score += 1
            self.apple_rect.x = randrange(0, self.screen_width - 50, 50)
            self.apple_rect.y = randrange(0, self.screen_height - 50, 50)
        else:
            self.snake_segments.pop()
    
    def check_collisions(self):
        
        head_rect = self.snake_segments[0].rect
        if (head_rect.left < 0 or head_rect.right > self.screen_width - 50 or
            head_rect.top < 0 or head_rect.bottom > self.screen_height - 50 or
            any(segment.rect.colliderect(head_rect) for segment in self.snake_segments[1:])):
            self.lives -= 1
            if self.lives == 0:
                self.game_over = True
                self.show_game_over_screen()
            else:
                self.snake_segments = [SnakeSegment(150, 100, pygame.image.load('wonsz.png').convert_alpha())]
                self.snake_dir = (0, 0)
                self.apple_rect.x = randrange(0, self.screen_width - 50, 50)
                self.apple_rect.y = randrange(0, self.screen_height - 50, 50)

    def update_screen(self):

        self.screen.blit(self.background_image, (0, 0))
        for segment in self.snake_segments:
            self.screen.blit(segment.image, segment.rect)
        self.screen.blit(self.apple_image, self.apple_rect)
        score_text = self.font.render(f"Wynik: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        heart_x = self.screen_width - 70
        heart_y = 20
        for _ in range(self.lives):
            self.screen.blit(pygame.image.load('heart.png').convert_alpha(), (heart_x, heart_y))
            heart_x -= 40

        pygame.display.flip()

if __name__ == "__main__":
    game = SnakeGame()
    game.run_game()
