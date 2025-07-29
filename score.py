import pygame.font
from pathlib import Path
import json
class Scoreboard:
    def __init__(self,ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
 
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()
        self.prep_high_score()


    def prep_high_score(self):
        high_score = round(self.stats.high_score)
        high_score_str = f'{high_score}'
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top


    def prep_score(self):
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # 将得分图像放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)

    def zero_score(self):
        """将得分重置为零"""
        self.stats.score = 0
        self.prep_score()


    def check_high_score(self):
        """检查并更新最高分"""
        number = json.loads(Path('high_score.json').read_text())
        if self.stats.score > number:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

        if self.stats.score < number:
            self.stats.high_score = number
            self.prep_high_score()


        number = json.loads(Path('high_score.json').read_text())
        if self.stats.high_score > number:
            path = Path('high_score.json')
            contents = json.dumps(self.stats.high_score)
            path.write_text(contents)
        
        
       