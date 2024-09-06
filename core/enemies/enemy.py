import pygame
import random
from data.settings import *

RADIUS = 20
COLOR = ORANGE
ENEMY_SPEED = 3
RED = (255, 0, 0)

class Enemy:
    def __init__(self):
        self.x = random.randint(RADIUS, SCREEN_WIDTH - RADIUS - WALL_THICKNESS)
        self.y = random.randint(RADIUS, SCREEN_HEIGHT - RADIUS - WALL_THICKNESS)
        self.radius = RADIUS
        self.color = COLOR
        self.speed = ENEMY_SPEED
        self.direction = random.choice(["up", "down", "left", "right"])
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)
        self.moving = True
        self.stuck_syringe = None  # Add this line to store the reference to the syringe

    def update(self):
        if not self.moving:
            return

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

        # Update the rect attribute to reflect the current position
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)

        # Update the syringe's position if it is stuck to the enemy
        if self.stuck_syringe:
            relative_x, relative_y = self.stuck_syringe.relative_position
            self.stuck_syringe.x = self.x + relative_x
            self.stuck_syringe.y = self.y + relative_y
            self.stuck_syringe.rect = self.stuck_syringe.rotated_image.get_rect(center=(self.stuck_syringe.x, self.stuck_syringe.y))

    def draw(self, screen):
        # Draw the syringe if it is stuck to the enemy
        if self.stuck_syringe:
            screen.blit(self.stuck_syringe.rotated_image, self.stuck_syringe.rect.topleft)
        
        # Draw the enemy as a circle
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        # Draw the outline of the enemy in red
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius, 2)