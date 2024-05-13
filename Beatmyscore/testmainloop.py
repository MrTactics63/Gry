import unittest
import pygame
import sys
from beatmyscore import Beatmyscore

class TestGame(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.game = Beatmyscore()

    def test_run_game(self):
        self.game.run_game()
        self.assertTrue(self.game.running)  # Sprawdzamy czy gra jest uruchomiona

    def test_run_menu(self):
        self.game.run_menu()
        self.assertTrue(self.game.running)  # Sprawdzamy czy menu jest uruchomione

    def test_check_menu_events(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        with self.assertRaises(SystemExit):  # Oczekujemy wyjścia z programu po wywołaniu sys.exit()
            self.game._check_menu_events()

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()