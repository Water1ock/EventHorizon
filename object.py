import pygame
import enum

class ToolType(enum.Enum):
    WRENCH = "Wrench",
    WEAPON = "Weapon"

class Object:
    def __init__(self, room_type, health):
        self.x = None
        self.y = None
        self.object_type = room_type
        self.health = health

    def update_x(self, x):
        self.x = x

    def update_y(self, y):
        self.y = y
