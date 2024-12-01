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
        self.direction = enum.Enum('Direction', 'left right up down')
        self.current_direction = self.direction.right
        self.controls = controls
        self.held_item = None
        self.pick_pressed = False
        self.action = None  # Can be 'pick' or 'drop'

    def move(self, keys):
        # Handle movement
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

        # Handle pick/drop actions
        if keys[self.controls['pick']]:
            if not self.pick_pressed:
                self.pick_pressed = True
                if self.held_item is None:
                    self.action = 'pick'
                else:
                    self.action = 'drop'
        else:
            self.pick_pressed = False

    def apply_gravity(self):
        self.y += self.gravity
        if self.y > self.bounds[3] - self.height:
            self.y = self.bounds[3] - self.height

    def decrease_oxy_level(self):
        self.oxy_level -= 0.5

    def decrease_health(self):
        self.health -= 1

    def draw(self, screen, color):
        self.rect = pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

    def draw_stats(self, screen, position, player_name, color):
        font = pygame.font.Font(pygame.font.get_default_font(), 36)

        # Draw the colored square representing the player
        square_size = 20
        square_x, square_y = position[0], position[1] - 40
        pygame.draw.rect(screen, color, (square_x, square_y, square_size, square_size))

        # Display the player's name next to the colored square
        name_label = font.render(player_name, True, (0, 0, 0))
        screen.blit(name_label, (square_x, square_y-20))

        # Health Bar
        bar_width = 200
        bar_height = 20
        health_bar_x, health_bar_y = position[0], position[1]

        # Draw background of the health bar
        pygame.draw.rect(screen, (139, 69, 19), (health_bar_x, health_bar_y, bar_width, bar_height))  # Dark yellow

        # Draw foreground of the health bar
        health_width = (self.health / 100) * bar_width  # Adjust width based on health percentage
        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_width, bar_height))  # Red