import pygame

class RoomTile:
    def __init__(self, l=None, r=None, f=False, c=False, has_ladder=None, room_type=None, object=None): # object hold the optional item in the room tile, i.e. ladder or workbench
        """
        wall_left and wall_right are of enum type 'WallType'
        ceiling and floor are bools (can they be passed through)
        object is of an object class like 'steering wheel' which has actions players can do when interacting with them
        """
        self.wall_left = l
        self.wall_right = r
        self.ceiling = c
        self.floor = f
        self.has_ladder = has_ladder
        self.roomType = room_type
        self.object = object


        

