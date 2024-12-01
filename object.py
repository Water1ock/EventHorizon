import pygame
import enum

class ToolType(enum.Enum):
    WRENCH = "Wrench",
    WEAPON = "Weapon"

class Object:
    def __init__(self, room_type, health):
        self.object_type = room_type
        self.health = health