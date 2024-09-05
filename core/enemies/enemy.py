import pygame
import random
from data.settings import *


RADIUS = 20
COLOR = ORANGE
ENEMY_SPEED = 3

class Enemy:
    def __init__(self):
        self.x = random.randint(RADIUS, SCREEN_WIDTH - RADIUS - WALL_THICKNESS)
        self.y = random.randint(RADIUS, SCREEN_HEIGHT - RADIUS - WALL_THICKNESS)
        self.radius = RADIUS
        self.color = COLOR
        self.speed = ENEMY_SPEED
        self.direction = random.choice(["up", "down", "left", "right"])

    def update(self):
        if self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed

        # Change direction if the enemy hits the screen border
        if self.x - self.radius < 0 or self.x + self.radius > SCREEN_WIDTH - WALL_THICKNESS:
            self.direction = "left" if self.direction == "right" else "right"
        if self.y - self.radius < 0 or self.y + self.radius > SCREEN_HEIGHT - WALL_THICKNESS:
            self.direction = "up" if self.direction == "down" else "down"

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)