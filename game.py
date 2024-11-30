import pygame
import sys
from player import Player

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

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
        pygame.display.set_caption("Big Box with Movable Player")
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize the big box
        self.big_box_x = (SCREEN_WIDTH - BIG_BOX_WIDTH) // 2
        self.big_box_y = (SCREEN_HEIGHT - BIG_BOX_HEIGHT) // 2

        # Player initialization
        player_initial_x = self.big_box_x + (BIG_BOX_WIDTH - PLAYER_WIDTH) // 2
        player_initial_y = self.big_box_y + BIG_BOX_HEIGHT - PLAYER_HEIGHT - 10
        self.player = Player(
            x=player_initial_x,
            y=player_initial_y,
            width=PLAYER_WIDTH,
            height=PLAYER_HEIGHT,
            speed=PLAYER_SPEED,
            bounds=(self.big_box_x, self.big_box_x + BIG_BOX_WIDTH - PLAYER_WIDTH),
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys)

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

        # Draw the player
        self.player.draw(self.screen, BLUE)

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
