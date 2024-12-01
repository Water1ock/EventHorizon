import pygame
import sys
import random
from player import Player
from spaceship import Spaceship
from pickables import PickItems
from enemy import Enemy, EnemyType
from constants import ROOM_TILE_HEIGHT, ROOM_TILE_WIDTH, GAME_NAME, SCREEN_WIDTH, SCREEN_HEIGHT, SPACESHIP_PADDING_TOP, SPACESHIP_PADDING_LEFT, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED
import enum
import os

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PLAYER_COLOURS = [
    (116,147,216), #blue   
    (156,216,116), #green
    (234,234,54), #yellow
    (223,100,78) #red
]

# base_path = os.path.join('sprites', 'players')

# PLAYER_SPRITE = [
#     pygame.image.load(os.path.join(base_path, 'char-blue-left.png')),
#     pygame.image.load(os.path.join(base_path, 'char-green-left.png')),
#     pygame.image.load(os.path.join(base_path, 'char-yellow-left.png')),
#     pygame.image.load(os.path.join(base_path, 'char-red-left.png'))
# ]

directory_path = os.path.dirname(__file__)

PLAYER_SPRITES = [
    pygame.image.load('char-red-left.png'),
    pygame.image.load('char-red-left.png'),
    pygame.image.load('char-red-left.png'),
    pygame.image.load('char-red-left.png')
]



class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tradership")

        self.clock = pygame.time.Clock()
        self.running = True

        self.spaceShip = Spaceship()
        self.spaceShip.update_object_coordinates(SPACESHIP_PADDING_LEFT, SPACESHIP_PADDING_TOP)

        self.picked_map = {}
        self.distance = 0
        self.fuel = 100
        self.damage = 0

        # Initialize the big box boundaries
        self.big_box_x = 0
        self.big_box_y = 0
        self.bounds = (
            self.big_box_x,
            self.big_box_x + SCREEN_WIDTH - PLAYER_WIDTH,
            self.big_box_y,
            self.big_box_y + SCREEN_HEIGHT - PLAYER_HEIGHT
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
            (self.big_box_x + 700, self.big_box_y + 550),
            (self.big_box_x + 775, self.big_box_y + 550),
            (self.big_box_x + 850, self.big_box_y + 550),
            (self.big_box_x + 925, self.big_box_y + 550)
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
        self.difficulty = 100  # Starting difficulty (you can tweak this starting value)
        self.max_difficulty = 10000  # Maximum difficulty cap (you can tweak this)
        self.difficulty_increase_rate = 1  # Rate at which difficulty increases (adjust as needed)
        self.enemies = []  # List to hold enemies in the game

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
        
        # Combine barriers and players for collision detection
        collision_barriers = self.spaceShip.barriers
        
        for player in self.players:
            player.apply_gravity(self.spaceShip.barriers)
            player.move(keys,None, collision_barriers)
            self.enemies = player.collision_with_enemy(self.enemies,self.screen)
            other_players = [p for p in self.players if p != player]
        
        self.handle_player_actions()

        player_rooms = {
            player: self.spaceShip.get_room_type_at_position(
                player.x,
                player.y,
                SPACESHIP_PADDING_TOP,
                SPACESHIP_PADDING_LEFT
            ) for player in self.players
        }

        enemy_rooms = {
            enemy: self.spaceShip.get_room_type_at_position(
                enemy.x,
                enemy.y,
                SPACESHIP_PADDING_TOP,
                SPACESHIP_PADDING_LEFT
            ) for enemy in self.enemies
        }

        # Apply damage to players if they're in the same room as an enemy
        for player, player_room in player_rooms.items():
            for enemy, enemy_room in enemy_rooms.items():
                if player_room and player_room == enemy_room:
                    player.decrease_health()
    
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
                        # player.held_item = pickable
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
        if self.difficulty < self.max_difficulty:
                self.difficulty += self.difficulty_increase_rate
        if random.randint(1, max((self.max_difficulty - self.difficulty),200)) <= 50:  # % chance of spawning an enemy per frame
            # enemy_type = random.choice(list(EnemyType))
            enemy_type = EnemyType.PLAYER_ATTACKING
            x = random.randint(self.big_box_x, self.big_box_x + SCREEN_WIDTH - 40)
            y = random.randint(self.big_box_y, self.big_box_y + SCREEN_HEIGHT - 40)

            # Assign closest player as the target for PLAYER_ATTACKING type
            # target = None
            # if enemy_type == EnemyType.PLAYER_ATTACKING:
            target = self.find_closest_player(x, y)
            # if enemy_type == EnemyType.OBJECT_ATTACKING:
            #     target = self.spaceShip.find_closest_object(x, y, SPACESHIP_PADDING_TOP, SPACESHIP_PADDING_LEFT)

            new_enemy = Enemy(x=x, y=y, speed=2, enemy_type=enemy_type, target=target)
            self.enemies.append(new_enemy)

    # Update enemy behavior
        for enemy in self.enemies:
            if enemy.type == EnemyType.PLAYER_ATTACKING:
                # Recalculate the closest player for each enemy
                enemy.target = self.find_closest_player(enemy.x, enemy.y)
            if enemy.type == EnemyType.OBJECT_ATTACKING:
                enemy.target = self.spaceShip.find_closest_object(enemy.x, enemy.y, SPACESHIP_PADDING_TOP, SPACESHIP_PADDING_LEFT)
            enemy.move_towards_target()

    def draw(self):
        # Clear screen
        self.screen.fill(WHITE)

        # Draw the big box
        pygame.draw.rect(
            self.screen,
            BLACK,
            (self.big_box_x, self.big_box_y, SCREEN_WIDTH, SCREEN_HEIGHT),
            2,
        )

        self.spaceShip.draw(self.screen)

        # Draw each player with a unique color
        for i, player in enumerate(self.players):
            player.draw(self.screen, PLAYER_COLOURS[i], PLAYER_SPRITES[i])
        
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
                player.draw_stats(self.screen, (20, 70), player_name='Player 1', color=PLAYER_COLOURS[0])
            elif i == 1:
                # Top-right
                player.decrease_oxy_level()
                player.draw_stats(self.screen, (SCREEN_WIDTH - 210, 70), player_name='Player 2', color=PLAYER_COLOURS[3])
            elif i == 2:
                # Bottom-left
                player.decrease_oxy_level()
                player.draw_stats(self.screen, (10, SCREEN_HEIGHT - 70), player_name='Player 3', color=PLAYER_COLOURS[1])
            elif i == 3:
                # Bottom-right
                player.decrease_oxy_level()
                player.draw_stats(self.screen, (SCREEN_WIDTH - 210, SCREEN_HEIGHT - 70), player_name='Player 4', color=PLAYER_COLOURS[2])
        
        # Draw each enemy
        for enemy in self.enemies:
            enemy.draw(self.screen)
        self.healthbar(int(((self.difficulty/self.max_difficulty)*100)), (0,255,0), SCREEN_WIDTH//2-270, 50, 'Difficulty')
        self.healthbar(self.distance, (0,255,0), SCREEN_WIDTH//2-20, 50, 'Points')
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
