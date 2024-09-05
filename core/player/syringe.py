import pygame
import os
from data.settings import *

SYRINGE_URL = os.path.join(ROOT_DIR, "assets", "img", "syringe.png")
SYRINGE_SCALE = 5

class Syringe:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.image = pygame.image.load(SYRINGE_URL)
        
        # Scale the image
        self.image = pygame.transform.scale(self.image, 
                                            (self.image.get_width() // SYRINGE_SCALE, 
                                             self.image.get_height() // SYRINGE_SCALE))
        
        self.speed = 10  # Adjust the speed as needed
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.direction_dict = {
            "up": 0,
            "down": 180,
            "right": 270,
            "left": 90,
            "up_right": 315,
            "up_left": 45,
            "down_right": 225,
            "down_left": 135
        }

    def update(self):
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
        rotate_angle = self.direction_dict[self.direction]
        self.rotated_image = pygame.transform.rotate(self.image, rotate_angle)
        self.rect = self.rotated_image.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.rotated_image, self.rect.topleft)