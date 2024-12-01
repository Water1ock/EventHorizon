import pygame
import enum

class ToolType(enum.Enum):
    Wrench = "Wrench",
    Weapon = "Weapon"

class Object:
    def __init__(self, room_type, health):
        self.object_type = room_type
        self.health = health