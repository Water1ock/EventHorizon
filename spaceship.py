import enum
import pygame
from object import Object
from roomTile import RoomTile
from barrier import Barrier
from door import Door
from ladder import Ladder
from constants import ROOM_TILE_WIDTH, ROOM_TILE_HEIGHT, WALL_FLOOR_DEPTH, WALL_FLOOR_COLOUR, SPACESHIP_PADDING_LEFT, SPACESHIP_PADDING_TOP

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

        # Loop through the level grid and create tiles
        self.barriers = []
        for row in range(len(self.room_tile_grid)):
            for col in range(len(self.room_tile_grid[row])):
                if self.room_tile_grid[row][col]:
                    tile = self.room_tile_grid[row][col]  # If there's a platform
                    x = col * ROOM_TILE_WIDTH + SPACESHIP_PADDING_LEFT
                    y = row * ROOM_TILE_HEIGHT + SPACESHIP_PADDING_TOP
                    if tile.floor:
                        self.barriers.append(Barrier(WALL_FLOOR_COLOUR, x, y + ROOM_TILE_HEIGHT - (WALL_FLOOR_DEPTH // 2), ROOM_TILE_WIDTH, WALL_FLOOR_DEPTH))
                
                    # Draw the ceiling if it exists
                    if tile.ceiling:
                        self.barriers.append(Barrier(WALL_FLOOR_COLOUR, x, y - (WALL_FLOOR_DEPTH // 2), ROOM_TILE_WIDTH, WALL_FLOOR_DEPTH))

                    # Draw the left wall
                    if tile.wall_left == WallType.WALL:
                        self.barriers.append(Barrier(WALL_FLOOR_COLOUR, x - (WALL_FLOOR_DEPTH // 2), y, WALL_FLOOR_DEPTH, ROOM_TILE_HEIGHT))
                    elif tile.wall_left == WallType.DOOR:
                        self.barriers.append(Door(WALL_FLOOR_COLOUR, x - (WALL_FLOOR_DEPTH // 2), y, WALL_FLOOR_DEPTH, ROOM_TILE_HEIGHT))

                    # Draw the right wall
                    if tile.wall_right == WallType.WALL:
                        self.barriers.append(Barrier(WALL_FLOOR_COLOUR, x + ROOM_TILE_WIDTH - (WALL_FLOOR_DEPTH // 2), y, WALL_FLOOR_DEPTH, ROOM_TILE_HEIGHT))
                    elif tile.wall_right == WallType.DOOR:
                        self.barriers.append(Door(WALL_FLOOR_COLOUR, x + ROOM_TILE_WIDTH - (WALL_FLOOR_DEPTH // 2), y, WALL_FLOOR_DEPTH, ROOM_TILE_HEIGHT))

                    # # Draw ladders if present
                    if tile.has_ladder:
                        self.barriers.append(Ladder(x + ROOM_TILE_WIDTH // 2 - 2, y, 30, ROOM_TILE_HEIGHT))

                    # Draw any object in the tile (placeholder logic for visual representation)
                    # if tile.object:
                    #     pygame.draw.circle(screen, (0, 255, 0), (x + ROOM_TILE_WIDTH // 2, y + ROOM_TILE_HEIGHT // 2), 10)

    def draw(self, screen):
        
        ### FOR DEBUGGING UNCOMMENT THIS TO SHOW FULL GRID ###
        # for row in range(len(self.room_tile_grid)):
        #     for col in range(len(self.room_tile_grid[row])):
        #         if self.room_tile_grid[row][col]:
        #             tile = self.room_tile_grid[row][col]  # If there's a platform
        #             x = col * ROOM_TILE_WIDTH + SPACESHIP_PADDING_LEFT
        #             y = row * ROOM_TILE_HEIGHT + SPACESHIP_PADDING_TOP
        #             pygame.draw.rect(screen, (0, 255, 0), (x, y, ROOM_TILE_WIDTH, ROOM_TILE_HEIGHT), 3)
        ### FOR DEBUGGING UNCOMMENT THIS TO SHOW FULL GRID ###
         
        for barrier in self.barriers:
            barrier.draw(screen)

