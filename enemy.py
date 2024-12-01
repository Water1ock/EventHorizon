import enum
import pygame
import random


class EnemyType(enum.Enum):
    PLAYER_ATTACKING = "Player Attacking"
    OBJECT_ATTACKING = "Object Attacking"


class Enemy:
    def __init__(self, x, y, speed, enemy_type: EnemyType, target=None):
        """
        Initialize the enemy.

        :param x: Initial x-coordinate
        :param y: Initial y-coordinate
        :param speed: Movement speed of the enemy
        :param enemy_type: Type of enemy (Player Attacking or Object Attacking)
        :param target: Target of the enemy (Player instance or Room instance)
        """
        self.x = x
        self.y = y
        self.speed = speed
        self.type = enemy_type
        self.target = target  # Target will depend on enemy type
        self.width = 40
        self.height = 40
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

    def move_towards_target(self):
        """
        Moves the enemy towards its target (player or room).
        If no target is assigned, the enemy will not move.
        """
        if not self.target:
            return

        # Get the target's position
        target_x, target_y = self.target.x, self.target.y

        # Calculate direction
        dx, dy = target_x - self.x, target_y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5  # Euclidean distance

        if distance > 0:
            # Normalize the direction and move
            self.x += self.speed * (dx / distance)
            self.y += self.speed * (dy / distance)

    def draw(self, screen):
        """
        Draw the enemy on the screen.
        """
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
