import pygame
import sys

# Initialize Pygame
pygame.init()

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

# Movement speed
PLAYER_SPEED = 5

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Big Box with Movable Player")

# Big box position
big_box_x = (SCREEN_WIDTH - BIG_BOX_WIDTH) // 2
big_box_y = (SCREEN_HEIGHT - BIG_BOX_HEIGHT) // 2

# Player initial position
player_x = big_box_x + (BIG_BOX_WIDTH - PLAYER_WIDTH) // 2
player_y = big_box_y + BIG_BOX_HEIGHT - PLAYER_HEIGHT - 10  # Slight offset from bottom

# Main loop flag
running = True

# Clock to control the frame rate
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player_x += PLAYER_SPEED

    # Constrain player movement within the big box
    player_x = max(big_box_x, min(player_x, big_box_x + BIG_BOX_WIDTH - PLAYER_WIDTH))

    # Clear screen
    screen.fill(WHITE)

    # Draw the big box
    pygame.draw.rect(screen, BLACK, (big_box_x, big_box_y, BIG_BOX_WIDTH, BIG_BOX_HEIGHT), 2)

    # Draw the player
    pygame.draw.rect(screen, BLUE, (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
