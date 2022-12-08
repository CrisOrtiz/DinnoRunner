from pygame import Surface
from pygame.sprite import Sprite

from dino_runner.utils.constants import SCREEN_WIDTH


class Obstacle(Sprite):
    def __init__(self, images: list[Surface], type):
        self.images = images
        self.type = type
        self.rect = self.images[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self, game_speed, obstacles: list):
        self.rect.x -= game_speed
        if self.rect.x <= -self.rect.width:
            obstacles.pop()

    def draw(self, screen: Surface):
        screen.blit(self.images[self.type], (self.rect.x, self.rect.y))
