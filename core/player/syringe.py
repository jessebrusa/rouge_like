import pygame
import os
from data.settings import *

SYRINGE_URL = os.path.join(ROOT_DIR, "assets", "img", "syringe.png")
SYRINGE_PUSH_URL = os.path.join(ROOT_DIR, "assets", "img", "syringe_push.png")
SYRINGE_SCALE = 5
SYRINGE_SPEED = 10

class Syringe:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.image = pygame.image.load(SYRINGE_URL)
        self.rotated_image = self.image

        self.moving = True
        self.stuck_enemy = None
        self.relative_position = (0, 0)  # Add this line to initialize relative_position

        
        # Scale the image
        self.image = pygame.transform.scale(self.image, 
                                            (self.image.get_width() // SYRINGE_SCALE, 
                                             self.image.get_height() // SYRINGE_SCALE))
        
        self.speed = SYRINGE_SPEED 
        self.rect = self.image.get_rect(center=(self.x, self.y))


    def update(self):
        if self.stuck_enemy:
            self.x = self.stuck_enemy.x
            self.y = self.stuck_enemy.y
            self.rect = None
        elif self.moving:
            if self.direction == "up":
                self.y -= self.speed
            elif self.direction == "down":
                self.y += self.speed
            elif self.direction == "left":
                self.x -= self.speed
            elif self.direction == "right":
                self.x += self.speed
            elif self.direction == "up_right":
                self.x += self.speed
                self.y -= self.speed
            elif self.direction == "up_left":
                self.x -= self.speed
                self.y -= self.speed
            elif self.direction == "down_right":
                self.x += self.speed
                self.y += self.speed
            elif self.direction == "down_left":
                self.x -= self.speed
                self.y += self.speed

        # Rotate the image
        rotate_angle = DIRECTION_DICT[self.direction]
        self.rotated_image = pygame.transform.rotate(self.image, rotate_angle)
        self.rect = self.rotated_image.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        if self.rect:
            screen.blit(self.rotated_image, self.rect.topleft)
        else:
            # Draw the syringe at its current position if rect is None
            screen.blit(self.rotated_image, (self.x, self.y))

    def swap_image(self):
        self.image = pygame.image.load(SYRINGE_PUSH_URL)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() // SYRINGE_SCALE), int(self.image.get_height() // SYRINGE_SCALE)))
        rotate_angle = DIRECTION_DICT[self.direction]
        self.rotated_image = pygame.transform.rotate(self.image, rotate_angle)
        self.rect = self.rotated_image.get_rect(center=(self.x, self.y))