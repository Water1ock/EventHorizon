import enum
import pygame
from object import Object
from roomTile import RoomTile

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
        room_tile_grid = [
            # top floor
            [
                RoomTile(),
                RoomTile(),

                RoomTile(l=WallType.WALL, f=True, c=True, room_type=RoomType.O2),
                RoomTile(c=True, has_ladder=True, room_type=RoomType.O2),
                RoomTile(r=WallType.DOOR, f=True, c=True, room_type=RoomType.O2, object=Object(RoomType.O2, 100)),

                RoomTile(l=WallType.DOOR, r=WallType.DOOR, f=True, c=True),

                RoomTile(l=WallType.DOOR, f=True, c=True, room_type=RoomType.GRAVITY),
                RoomTile(f=True, c=True, room_type=RoomType.GRAVITY, object=Object(RoomType.GRAVITY, 100)),
                RoomTile(c=True, has_ladder=True, room_type=RoomType.GRAVITY),
                RoomTile(r=WallType.WALL, f=True, c=True, room_type=RoomType.GRAVITY),

                RoomTile(),
                RoomTile(),
                RoomTile(),
            ],
            # middle floor
            [
                RoomTile(l=WallType.WALL, f=True, c=True, room_type=RoomType.ENGINE),
                RoomTile(f=True, c=True, room_type=RoomType.ENGINE, object=Object(RoomType.ENGINE, 100)),
                RoomTile(r=WallType.DOOR, f=True, c=True, room_type=RoomType.ENGINE),

                RoomTile(l=WallType.DOOR, r=WallType.DOOR, has_ladder=True),

                RoomTile(l=WallType.DOOR, f=True, c=True, room_type=RoomType.CARGO),
                RoomTile(f=True, c=True, room_type=RoomType.CARGO, object=Object(RoomType.CARGO, 100)),
                RoomTile(r=WallType.WALL, f=True, c=True, room_type=RoomType.CARGO),

                RoomTile(l=WallType.WALL, f=True, c=True),
                RoomTile(f=True, has_ladder=True),
                RoomTile(r=WallType.DOOR, f=True, c=True),

                RoomTile(l=WallType.DOOR, f=True, c=True, room_type=RoomType.CONTROL),
                RoomTile(f=True, c=True, room_type=RoomType.CONTROL, object=Object(RoomType.CONTROL, 100)),
                RoomTile(r=WallType.WALL, f=True, c=True, room_type=RoomType.CONTROL),
            ],
            # bottom floor
            [
                RoomTile(),
                RoomTile(),

                RoomTile(l=WallType.WALL, f=True, c=True, room_type=RoomType.ARMOURY, object=Object(RoomType.ARMOURY, 100)),
                RoomTile(f=True, room_type=RoomType.ARMOURY),
                RoomTile(r=WallType.DOOR, f=True, c=True, room_type=RoomType.ARMOURY),

                RoomTile(l=WallType.DOOR, f=True, c=True, room_type=RoomType.WORKSHOP),
                RoomTile(f=True, c=True, room_type=RoomType.WORKSHOP, object=Object(RoomType.WORKSHOP, 100)),
                RoomTile(r=WallType.DOOR, f=True, c=True, room_type=RoomType.WORKSHOP),

                RoomTile(l=WallType.DOOR, f=True, c=True, room_type=RoomType.MEDBAY),
                RoomTile(f=True, c=True, room_type=RoomType.MEDBAY),
                RoomTile(r=WallType.WALL, f=True, c=True, room_type=RoomType.MEDBAY, object=Object(RoomType.MEDBAY, 100)),

                RoomTile(),
                RoomTile(),
            ],
        ]

