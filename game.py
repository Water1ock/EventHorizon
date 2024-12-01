import pygame
import sys
import random
from player import Player
from spaceship import Spaceship, ROOM_TILE_HEIGHT, ROOM_TILE_WIDTH
from pickables import PickItems
from enemy import Enemy, EnemyType

GAME_NAME = 'EventHorizon24'

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

SPACESHIP_PADDING_TOP = (SCREEN_HEIGHT - (3*ROOM_TILE_HEIGHT)) // 2 
SPACESHIP_PADDING_LEFT = (SCREEN_WIDTH - (13*ROOM_TILE_WIDTH)) // 2 

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
BIG_BOX_WIDTH = SCREEN_WIDTH
BIG_BOX_HEIGHT = SCREEN_HEIGHT
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

        self.spaceShip = Spaceship()

        self.picked_map = {}
        self.distance = 0
        self.fuel = 100
        self.damage = 0

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

        # Initialize enemy list
        self.enemies = []

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def find_closest_player(self, enemy_x, enemy_y):
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
    
    def healthbar(self, value,color,x,y,text):
        self.draw_text(f'{text}: {round(value,1)}', x, y-20)
        pygame.draw.rect(self.screen, (199, 144, 0 ), (x, y, 100, 20))
        pygame.draw.rect(self.screen, color, (x, y, 100*value/100, 20))

    def update(self):
        keys = pygame.key.get_pressed()
        for player in self.players:
            player.move(keys)
            player.apply_gravity()
        
        self.handle_player_actions()
    
    def draw_text(self, text, x, y, font_size=15):
        font = pygame.font.Font(pygame.font.get_default_font(), font_size)
        text = font.render(text, True, BLACK)
        self.screen.blit(text, (x, y))

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

        self.spaceShip.draw(self.screen, SPACESHIP_PADDING_LEFT, SPACESHIP_PADDING_TOP)

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

        # Draw player health bars (top-left, top-right, bottom-left, bottom-right)
        for i, player in enumerate(self.players):
            # Calculate positions for player health bars
            if i == 0:
                # Top-left
                player.decrease_oxy_level()
                player.draw_stats(self.screen, (20, 70), player_name='Player 1', color=(255, 255, 0))
            elif i == 1:
                # Top-right
                player.decrease_oxy_level()
                player.draw_stats(self.screen, (SCREEN_WIDTH - 210, 70), player_name='Player 2', color=(255, 0, 0))
            elif i == 2:
                # Bottom-left
                player.decrease_oxy_level()
                player.draw_stats(self.screen, (10, SCREEN_HEIGHT - 70), player_name='Player 3', color=(0, 255, 0))
            elif i == 3:
                # Bottom-right
                player.decrease_oxy_level()
                player.draw_stats(self.screen, (SCREEN_WIDTH - 210, SCREEN_HEIGHT - 70), player_name='Player 4', color=(0, 0, 255))

        # Draw each enemy
        for enemy in self.enemies:
            enemy.draw(self.screen)
        self.healthbar(self.fuel, (0,255,0), SCREEN_WIDTH//2-270, 50, 'Fuel')
        self.healthbar(self.distance, (0,255,0), SCREEN_WIDTH//2-20, 50, 'Distance')
        self.healthbar(self.damage, (255,0,0), SCREEN_WIDTH//2+250-20, 50, 'Damage')

        # Update the display
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
            
            self.fuel -= 0.001

        # Quit Pygame
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
