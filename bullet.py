import pygame
class Bullet:
    prev_direction = 1
    def __init__(self, x, y, width, height, color, direction):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.direction = direction
        self.speed = 3
        
    
    def move(self):
        
        if self.direction == 1:#left
            self.x -= self.speed
            Bullet.prev_direction = 1
        elif self.direction == 2:#right
            self.x += self.speed
            Bullet.prev_direction = 2
        else:
          
            if Bullet.prev_direction == 1:
                self.direction = 1
                self.x -= self.speed
            elif Bullet.prev_direction == 2:
                self.x += self.speed
                self.direction = 2
        
        # elif self.direction == 3:
        #     self.y -= self.speed
        # elif self.direction == 4:
        #     self.y += self.speed
        

    def draw(self, screen):
        self.rect = pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))