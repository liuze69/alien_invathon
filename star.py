import pygame
from pygame.sprite import Sprite

class Star(Sprite):
    def __init__(self, ai_game, x, y):
        super().__init__()
        self.screen = ai_game.screen
        self.image = pygame.image.load('images/cropped(1).png') 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw_star(self):
        self.screen.blit(self.image, self.rect)
