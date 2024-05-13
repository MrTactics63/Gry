class GameStats():
    
    def __init__(self, ai_game):
        self.settings = ai_game.settings  
        self.level = 1
        self.reset_stats()

    def reset_stats(self):
        self.player_left = self.settings.player_limit
        self.score = 0 
        self.level = 1