import pygame
import sys
import random
from player import Player
from enemy import Enemy, EnemyType
#from spaceship import Spaceship

GAME_NAME = 'EventHorizon24'

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0)   # Yellow
]

# Box dimensions
BIG_BOX_WIDTH = 1920
BIG_BOX_HEIGHT = 1080
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_SPEED = 5

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tradership")

        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize the big box boundaries
        self.big_box_x = (SCREEN_WIDTH - BIG_BOX_WIDTH) // 2
        self.big_box_y = (SCREEN_HEIGHT - BIG_BOX_HEIGHT) // 2
        self.bounds = (
            self.big_box_x,
            self.big_box_x + BIG_BOX_WIDTH - PLAYER_WIDTH,
            self.big_box_y,
            self.big_box_y + BIG_BOX_HEIGHT - PLAYER_HEIGHT
        )

        # self.spaceship = Spaceship()

        # Define controls for each player
        self.player_controls = [
            {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN},
            {'left': pygame.K_s, 'right': pygame.K_f, 'up': pygame.K_e, 'down': pygame.K_d},
            {'left': pygame.K_j, 'right': pygame.K_l, 'up': pygame.K_i, 'down': pygame.K_k},
            {'left': pygame.K_KP4, 'right': pygame.K_KP6, 'up': pygame.K_KP8, 'down': pygame.K_KP5}
        ]

        # Initialize players at different positions
        self.players = []
        start_positions = [
            (self.big_box_x + 50, self.big_box_y + 50),
            (self.big_box_x + 150, self.big_box_y + 50),
            (self.big_box_x + 250, self.big_box_y + 50),
            (self.big_box_x + 350, self.big_box_y + 50)
        ]

        for i in range(4):
            player = Player(
                x=start_positions[i][0],
                y=start_positions[i][1],
                width=PLAYER_WIDTH,
                height=PLAYER_HEIGHT,
                speed=PLAYER_SPEED,
                bounds=self.bounds,
                controls=self.player_controls[i]
            )
            self.players.append(player)

        # Initialize enemy list
        self.enemies = []

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def find_closest_player(self, enemy_x, enemy_y):
        """Find the closest player to the given enemy coordinates."""
        closest_player = None
        min_distance = float('inf')

        for player in self.players:
            dx = player.x - enemy_x
            dy = player.y - enemy_y
            distance = (dx ** 2 + dy ** 2) ** 0.5  # Euclidean distance

            if distance < min_distance:
                min_distance = distance
                closest_player = player

        return closest_player

    def update(self):
        keys = pygame.key.get_pressed()
        for player in self.players:
            player.move(keys)
            player.apply_gravity()
            player.decrease_oxy_level()

        # Randomly spawn enemies
        if random.randint(1, 100) <= 5:  # 5% chance of spawning an enemy per frame
            enemy_type = random.choice(list(EnemyType))
            x = random.randint(self.big_box_x, self.big_box_x + BIG_BOX_WIDTH - 40)
            y = random.randint(self.big_box_y, self.big_box_y + BIG_BOX_HEIGHT - 40)

            # Assign closest player as the target for PLAYER_ATTACKING type
            target = None
            if enemy_type == EnemyType.PLAYER_ATTACKING:
                target = self.find_closest_player(x, y)

            new_enemy = Enemy(x=x, y=y, speed=2, enemy_type=enemy_type, target=target)
            self.enemies.append(new_enemy)

    # Update enemy behavior
        for enemy in self.enemies:
            if enemy.type == EnemyType.PLAYER_ATTACKING:
                # Recalculate the closest player for each enemy
                enemy.target = self.find_closest_player(enemy.x, enemy.y)
            enemy.move_towards_target()

    def draw(self):
        # Clear screen
        self.screen.fill(WHITE)

        # Draw the big box
        pygame.draw.rect(
            self.screen,
            BLACK,
            (self.big_box_x, self.big_box_y, BIG_BOX_WIDTH, BIG_BOX_HEIGHT),
            2,
        )

        # Draw each player with a unique color
        for i, player in enumerate(self.players):
            player.draw(self.screen, PLAYER_COLORS[i])

        # Draw each enemy
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Update the display
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        # Quit Pygame
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
