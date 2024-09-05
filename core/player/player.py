import pygame
import os
from data.settings import *

SYRINGE_URL = os.path.join(ROOT_DIR, "assets", "img", "syringe.png")

RADIUS = 20
COLOR = GREY
SPEED = 5

SYRINGE_SCALE = 3
SYRING_ROTATION = 20
SYRING_OFFSET = 10

class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.radius = RADIUS
        self.color = COLOR
        self.speed = SPEED
        self.direction = "up"
        
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


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

        # Draw the bounding circle around the player
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius, 2)  # Red color with a thickness of 2


    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
            self.x -= self.speed
            self.y -= self.speed
            self.direction = "up_left"
        elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
            self.x += self.speed
            self.y -= self.speed
            self.direction = "up_right"
        elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
            self.x -= self.speed
            self.y += self.speed
            self.direction = "down_left"
        elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
            self.x += self.speed
            self.y += self.speed
            self.direction = "down_right"
        elif keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.direction = "left"
        elif keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.direction = "right"
        elif keys[pygame.K_UP]:
            self.y -= self.speed
            self.direction = "up"
        elif keys[pygame.K_DOWN]:
            self.y += self.speed
            self.direction = "down"
            
    def is_off_screen(self):
        return self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT