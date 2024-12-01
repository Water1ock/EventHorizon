import enum
import pygame
from bullet import Bullet

class Player:
    def __init__(self, x, y, width, height, speed, bounds, controls):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.bounds = bounds  # (x_min, x_max)
        self.gravity = 1
        self.health = 100
        self.oxy_level = 100
        self.direction = enum.Enum('Direction', 'left right up down')
        self.current_direction = self.direction.right
        self.controls = controls
        self.held_item = "gun"
        self.pick_pressed = False
        self.action = None  # Can be 'pick' or 'drop'
        self.player_bullets = []
        self.use_flag = False
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def move(self, keys, screen, barriers):
        # Store original position to revert if collision occurs
        original_x, original_y = self.x, self.y        # Handle movement
        if keys[self.controls['left']]:
            self.current_direction = self.direction.left
            self.x -= self.speed
            self.rect.x = self.x
        if keys[self.controls['right']]:
            self.current_direction = self.direction.right
            self.x += self.speed
            self.rect.x = self.x
        if keys[self.controls['up']]:
            self.current_direction = self.direction.up
            self.y -= self.speed
            self.rect.y = self.y
        if keys[self.controls['down']]:
            self.current_direction = self.direction.down
            self.y += self.speed
            self.rect.y = self.y
        if keys[self.controls['use']] and not self.use_flag:
            self.use_flag=True
        if not keys[self.controls['use']] and self.use_flag:
            self.use_item(screen)
            self.use_flag=False
            # print("move pressed")
       
        
            

        # Collision checks
        # Check barriers
        if self.check_collisions(barriers):
            # Revert position if collision detected
            self.x, self.y = original_x, original_y

        # Constrain player movement within the bounds
        self.x = max(self.bounds[0], min(self.x, self.bounds[1]))
        self.y = max(self.bounds[2], min(self.y, self.bounds[3]))

        # Handle pick/drop actions
        if keys[self.controls['pick']]:
            if not self.pick_pressed:
                self.pick_pressed = True
                if self.held_item is None:
                    self.action = 'pick'
                else:
                    self.action = 'drop'
        else:
            self.pick_pressed = False

    def apply_gravity(self, barriers):
        new_y = self.y + self.gravity

        # Check if the player will collide with any barrier at the new position
        player_rect = pygame.Rect(self.x, new_y, self.width, self.height)  # Player's new rectangle
        
        if self.check_collisions(barriers):
                self.y = self.y - self.gravity
                return  # Exit the method since the gravity application is complete
    
        # If no collision is found, apply gravity (fall down normally)
        self.y = new_y

        # Check if the player falls out of bounds (for bottom boundary)
        if self.y > self.bounds[3] - self.height:
            self.y = self.bounds[3] - self.height

    def decrease_oxy_level(self):
        self.oxy_level -= 0.5

    def decrease_health(self):
        self.health -= 0.15

    def draw(self, screen, color, sprite):
        # self.rect = pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        if self.direction == 1:
            self.rect = screen.blit(sprite, (self.x, self.y))
        elif self.direction == 2:
            image = pygame.transform.flip(sprite, True, False)
            self.rect = screen.blit(image, (self.x, self.y))

        if len(self.player_bullets)!=0:
            self.draw_bullets(screen)
    
    def fire_bullet(self):
        
            bullet = Bullet(self.x, self.y, 10, 10, (255, 0, 0), self.current_direction.value)
            self.player_bullets.append(bullet)
            # print(len(self.player_bullets),self.current_direction, self.current_direction.value)
    
    def draw_bullets(self, screen):
        for bullet in self.player_bullets:
            bullet.move()
            bullet.draw(screen)
            if bullet.x < 0 or bullet.x > 1920 or bullet.y < 0 or bullet.y > 1080:
                self.player_bullets.remove(bullet)
    def use_item(self,screen):
        if self.held_item is not None:
            if self.held_item == 'gun':
                self.fire_bullet()

    def collision_with_enemy(self, enemies,screen):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                self.health -= 10
        if len(self.player_bullets)!=0:
            self.draw_bullets(screen)
            for bullet in self.player_bullets:
                for enemy in enemies:
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.health -= 10
                        enemies.remove(enemy)
                        # if enemy.health <= 0:
                        #     enemies.remove(enemy)
                        self.player_bullets.remove(bullet)
                        break
                    
        return enemies
        
                
    
    

    def draw_stats(self, screen, position, player_name, color):
        font = pygame.font.Font(pygame.font.get_default_font(), 36)

        # Draw the colored square representing the player
        square_size = 20
        square_x, square_y = position[0], position[1] - 40
        pygame.draw.rect(screen, color, (square_x, square_y, square_size, square_size))

        # Display the player's name next to the colored square
        name_label = font.render(player_name, True, (0, 0, 0))
        screen.blit(name_label, (square_x, square_y-20))

        # Health Bar
        bar_width = 200
        bar_height = 20
        health_bar_x, health_bar_y = position[0], position[1]

        # Draw background of the health bar
        pygame.draw.rect(screen, (139, 69, 19), (health_bar_x, health_bar_y, bar_width, bar_height))  # Dark yellow

        # Draw foreground of the health bar
        health_width = (self.health / 100) * bar_width  # Adjust width based on health percentage
        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_width, bar_height))  # Red
    
    def check_collisions(self, collision_objects):
        """
        Check if the player collides with any objects in the list.
        
        :param collision_objects: List of objects with a rect attribute
        :return: True if collision detected, False otherwise
        """
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        for obj in collision_objects:
            # Skip checking collision with self
            if obj == self:
                continue

            barrier_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            
            # Check for rectangle intersection
            if player_rect.colliderect(barrier_rect):
                return True
        return False