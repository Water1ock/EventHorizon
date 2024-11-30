import pygame
import random
class PickItems:
    def __init__(self, x, y, width, height, name):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.picked = False

    def draw(self, screen):
        if not self.picked:
            self.rect = pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
    def redraw(self, screen, player):
        self.x = player.x + 10
        self.y = player.y - 10
        self.rect = pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
