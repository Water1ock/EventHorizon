import pygame
import sys
from player import Player

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

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
BIG_BOX_WIDTH = 600
BIG_BOX_HEIGHT = 400
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

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        keys = pygame.key.get_pressed()
        for player in self.players:
            player.move(keys)
            player.apply_gravity()
            player.decrease_oxy_level()

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
