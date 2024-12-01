import pygame
from constants import DOOR_COLOUR

class Door:
    def __init__(self, colour, x, y, width, height):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, DOOR_COLOUR, (self.x, self.y + (self.height // 2), self.width, (self.height // 2) - 5))
