import enum
import pygame
from object import Object
from roomTile import RoomTile

ROOM_TILE_WIDTH = 130
ROOM_TILE_HEIGHT = 290

class RoomType(enum.Enum):
    O2 = 'Oxygen'
    GRAVITY = 'Gravity'
    ENGINE = 'Engine'
    ARMOURY = 'Armoury'
    CARGO = 'Cargo'
    CONTROL = 'Control'
    WORKSHOP = 'Workshop'
    MEDBAY = 'Medbay'


class WallType(enum.Enum):
    WALL = 'Wall'
    DOOR = 'Door'


class Spaceship:
    def __init__(self):
        self.room_tile_grid = [
            # top floor
            [
                RoomTile(),
                RoomTile(),

                RoomTile(l=WallType.WALL, f=True, c=True, room_type=RoomType.O2),
                RoomTile(c=True, has_ladder=True, room_type=RoomType.O2),
                RoomTile(r=WallType.DOOR, f=True, c=True, room_type=RoomType.O2, object=Object(RoomType.O2, 100)),

                RoomTile(r=WallType.DOOR, f=True, c=True),

                RoomTile(f=True, c=True, room_type=RoomType.GRAVITY),
                RoomTile(f=True, c=True, room_type=RoomType.GRAVITY, object=Object(RoomType.GRAVITY, 100)),
                RoomTile(c=True, has_ladder=True, room_type=RoomType.GRAVITY),
                RoomTile(r=WallType.WALL, f=True, c=True, room_type=RoomType.GRAVITY),

                RoomTile(),
                RoomTile(),
                RoomTile(),
            ],
            # middle floor
            [
                RoomTile(f=True, c=True, l=WallType.WALL, room_type=RoomType.ENGINE),
                RoomTile(f=True, c=True, room_type=RoomType.ENGINE, object=Object(RoomType.ENGINE, 100)),
                RoomTile(r=WallType.DOOR, room_type=RoomType.ENGINE),

                RoomTile(r=WallType.DOOR, has_ladder=True),

                RoomTile(room_type=RoomType.CARGO),
                RoomTile(room_type=RoomType.CARGO, object=Object(RoomType.CARGO, 100)),
                RoomTile(r=WallType.WALL, room_type=RoomType.CARGO),

                RoomTile(),
                RoomTile(has_ladder=True),
                RoomTile(r=WallType.DOOR),

                RoomTile(c=True, room_type=RoomType.CONTROL),
                RoomTile(f=True, c=True, room_type=RoomType.CONTROL, object=Object(RoomType.CONTROL, 100)),
                RoomTile(f=True, c=True, r=WallType.WALL, room_type=RoomType.CONTROL),
            ],
            # bottom floor
            [
                RoomTile(),
                RoomTile(),

                RoomTile(l=WallType.WALL, f=True, c=True, room_type=RoomType.ARMOURY, object=Object(RoomType.ARMOURY, 100)),
                RoomTile(f=True, room_type=RoomType.ARMOURY, has_ladder=True),
                RoomTile(r=WallType.DOOR, f=True, c=True, room_type=RoomType.ARMOURY),

                RoomTile(f=True, c=True, room_type=RoomType.WORKSHOP),
                RoomTile(f=True, c=True, room_type=RoomType.WORKSHOP, object=Object(RoomType.WORKSHOP, 100)),
                RoomTile(r=WallType.DOOR, f=True, c=True, room_type=RoomType.WORKSHOP),

                RoomTile(f=True, c=True, room_type=RoomType.MEDBAY),
                RoomTile(f=True, c=True, room_type=RoomType.MEDBAY),
                RoomTile(r=WallType.WALL, f=True, c=True, room_type=RoomType.MEDBAY, object=Object(RoomType.MEDBAY, 100)),

                RoomTile(),
                RoomTile(),
            ],
        ]

    def draw(self, screen, SPACESHIP_PADDING_TOP, SPACESHIP_PADDING_LEFT):
         # Loop through the level grid and draw tiles
         for row in range(len(self.room_tile_grid)):
             for col in range(len(self.room_tile_grid[row])):
                 if self.room_tile_grid[row][col]:
                    tile = self.room_tile_grid[row][col]  # If there's a platform
                    x = col * ROOM_TILE_WIDTH + SPACESHIP_PADDING_LEFT
                    y = row * ROOM_TILE_HEIGHT + SPACESHIP_PADDING_TOP
                    #  pygame.draw.rect(screen, (1, 1, 1), (x, y, ROOM_TILE_WIDTH, ROOM_TILE_HEIGHT))
                    #  pygame.draw.rect(screen, (255, 0, 0), (x, y, ROOM_TILE_WIDTH, ROOM_TILE_HEIGHT), 3)  # 3 is the border width
                    if tile.floor:
                        pygame.draw.rect(screen, (150, 75, 0), (x, y + ROOM_TILE_HEIGHT - 5, ROOM_TILE_WIDTH, 5))
                
                    # Draw the ceiling if it exists
                    if tile.ceiling:
                        pygame.draw.rect(screen, (100, 100, 100), (x, y, ROOM_TILE_WIDTH, 5))

                    # Draw the left wall
                    if tile.wall_left == WallType.WALL:
                        pygame.draw.rect(screen, (50, 50, 255), (x, y, 5, ROOM_TILE_HEIGHT))
                    elif tile.wall_left == WallType.DOOR:
                        pygame.draw.rect(screen, (0, 255, 255), (x, y, 5, ROOM_TILE_HEIGHT))

                    # Draw the right wall
                    if tile.wall_right == WallType.WALL:
                        pygame.draw.rect(screen, (50, 50, 255), (x + ROOM_TILE_WIDTH - 5, y, 5, ROOM_TILE_HEIGHT))
                    elif tile.wall_right == WallType.DOOR:
                        pygame.draw.rect(screen, (0, 255, 255), (x + ROOM_TILE_WIDTH - 5, y, 5, ROOM_TILE_HEIGHT))

                    # Draw ladders if present
                    if tile.has_ladder:
                        pygame.draw.rect(screen, (200, 200, 0), (x + ROOM_TILE_WIDTH // 2 - 2, y, 4, ROOM_TILE_HEIGHT))

                    # Draw any object in the tile (placeholder logic for visual representation)
                    if tile.object:
                        pygame.draw.circle(screen, (0, 255, 0), (x + ROOM_TILE_WIDTH // 2, y + ROOM_TILE_HEIGHT // 2), 10)
