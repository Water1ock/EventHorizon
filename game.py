import pygame
import sys
from player import Player
from pickables import PickItems

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
        self.picked_map = {}

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
            {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN,'pick': pygame.K_DELETE,'use':pygame.K_END},
            {'left': pygame.K_s, 'right': pygame.K_f, 'up': pygame.K_e, 'down': pygame.K_d,'pick': pygame.K_q,'use':pygame.K_w},
            {'left': pygame.K_j, 'right': pygame.K_l, 'up': pygame.K_i, 'down': pygame.K_k,'pick': pygame.K_y,'use':pygame.K_u},
            {'left': pygame.K_KP4, 'right': pygame.K_KP6, 'up': pygame.K_KP8, 'down': pygame.K_KP5,'pick': pygame.K_KP1,'use':pygame.K_KP0}
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
        
        self.pickables = []
        for i in range(4):
                pickable = PickItems(
                    x=100 + 100 * i,
                    y=100 + i*10,
                    width=10,
                    height=10,
                    name = 'item'+str(i)
                )
                self.pickables.append(pickable)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        keys = pygame.key.get_pressed()
        for player in self.players:
            player.move(keys)
            player.apply_gravity()
        
        self.handle_player_actions()

    def handle_player_actions(self):
        for player in self.players:
            if player.action == 'pick':
                # Try to pick up an item
                for pickable in self.pickables:
                    if player.rect.colliderect(pickable.rect) and not pickable.picked:
                        player.held_item = pickable
                        self.picked_map[player] = pickable
                        pickable.picked = True
                        break
                player.action = None  # Reset action after handling
            elif player.action == 'drop':
                # Drop the held item
                if player in self.picked_map:
                    pickable = self.picked_map.pop(player)
                    pickable.x = 50
                    pickable.y = 50
                    pickable.picked = False
                    player.held_item = None
                player.action = None  # Reset action after handling

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
        
        # Draw pickables
        for pickable in self.pickables:
            if pickable.picked:
                # Draw the pickable at the player's position
                player = None
                for p, item in self.picked_map.items():
                    if item == pickable:
                        player = p
                        break
                if player:
                    pickable.redraw(self.screen, player)
            else:
                # Draw the pickable at its position
                pickable.draw(self.screen)

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
