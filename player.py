import pygame

class Player:
    def __init__(self, x, y, width, height, speed, bounds):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.bounds = bounds  # (x_min, x_max)

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        # Constrain player movement within the bounds
        self.x = max(self.bounds[0], min(self.x, self.bounds[1]))

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
