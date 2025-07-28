class GameStats:
    def __init__(self, ai_game):
        settings = ai_game.settings
        self.settings = settings
        self.reset_stats()

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        

    