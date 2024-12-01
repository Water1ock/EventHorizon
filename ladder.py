import pygame
from constants import LADDER_COLOUR

class Ladder:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        # pygame.draw.rect(screen, LADDER_COLOUR, (self.x, self.y, self.width, self.height))

        pass