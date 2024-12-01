import enum
import pygame

class Player:
    def __init__(self, x, y, width, height, speed, bounds, controls):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.bounds = bounds  # (x_min, x_max)
        self.gravity = 0.5
        self.health = 100
        self.oxy_level = 100
        self.action = False
        self.direction = enum.Enum('Direction', 'left right up down')
        self.current_direction = self.direction.right
        self.controls = controls  # {'left': key, 'right': key, 'up': key, 'down': key}

    def move(self, keys):
        if keys[self.controls['left']]:
            self.current_direction = self.direction.left
            self.x -= self.speed
        if keys[self.controls['right']]:
            self.current_direction = self.direction.right
            self.x += self.speed
        if keys[self.controls['up']]:
            self.current_direction = self.direction.up
            self.y -= self.speed
        if keys[self.controls['down']]:
            self.current_direction = self.direction.down
            self.y += self.speed

        # Constrain player movement within the bounds
        self.x = max(self.bounds[0], min(self.x, self.bounds[1]))
        self.y = max(self.bounds[2], min(self.y, self.bounds[3]))

    def apply_gravity(self):
        self.y += self.gravity
        if self.y > self.bounds[3] - self.height:
            self.y = self.bounds[3] - self.height

    def decrease_oxy_level(self):
        self.oxy_level -= 0.5

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

    def draw_stats(self, screen, position):
        font = pygame.font.Font(None, 36)

        # Health Bar
        pygame.draw.rect(screen, (255, 0, 0), (position[0], position[1], 200, 20))  # Red background for health
        pygame.draw.rect(screen, (0, 255, 0), (position[0], position[1], self.health * 2, 20))  # Green foreground for health

        # Oxygen Bar
        pygame.draw.rect(screen, (0, 0, 255), (position[0], position[1] + 30, 200, 20))  # Blue background for oxygen
        pygame.draw.rect(screen, (173, 216, 230), (position[0], position[1] + 30, self.oxy_level * 2, 20))  # Cyan foreground for oxygen

        # Display Player Label
        label = font.render(f"Player", True, (0, 0, 0))
        screen.blit(label, (position[0], position[1] - 30))
