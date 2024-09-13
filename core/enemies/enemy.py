import pygame
import random
import time
from data.settings import *

RADIUS = 20
RANDOM_RANGE = 50

class Enemy:
    def __init__(self, speed):
        self.x = random.randint(RADIUS, SCREEN_WIDTH - RADIUS - WALL_THICKNESS)
        self.y = random.randint(RADIUS, SCREEN_HEIGHT - RADIUS - WALL_THICKNESS)
        self.radius = RADIUS
        self.color = ORANGE
        self.initial_speed = speed  
        self.speed = speed
        self.direction = random.choice(["up", "down", "left", "right"])
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)
        self.moving = True
        self.stuck_syringe = None  # Add this line to store the reference to the syringe
        self.hit_count = 0 # Add this line to track the number of hits
        self.dead = False
        self.hit_time = None
        self.random_direction = None

    def update(self, player):
        if not self.moving:
            return

        if self.dead:
            return

        current_time = time.time()

        if self.hit_time and current_time - self.hit_time < 3:
            # Move in a random direction for 3 seconds
            if not self.random_direction:
                self.random_direction = (random.uniform(-1, 1), random.uniform(-1, 1))
            dx, dy = self.random_direction
        else:
            # Reset hit state and move towards the player
            self.hit_time = None
            self.random_direction = None

            # Calculate direction towards a random position around the player
            target_x = player.x + random.randint(-RANDOM_RANGE, RANDOM_RANGE)
            target_y = player.y + random.randint(-RANDOM_RANGE, RANDOM_RANGE)
            dx = target_x - self.x
            dy = target_y - self.y
            distance = (dx**2 + dy**2)**0.5

            if distance != 0:
                dx /= distance
                dy /= distance

        # Move towards the target position or in a random direction
        self.x += dx * self.speed
        self.y += dy * self.speed

        # Boundary checks to keep the enemy within the screen considering WALL_THICKNESS
        if self.x - self.radius < WALL_THICKNESS:
            self.x = WALL_THICKNESS + self.radius
        if self.x + self.radius > SCREEN_WIDTH - WALL_THICKNESS:
            self.x = SCREEN_WIDTH - WALL_THICKNESS - self.radius
        if self.y - self.radius < WALL_THICKNESS:
            self.y = WALL_THICKNESS + self.radius
        if self.y + self.radius > SCREEN_HEIGHT - WALL_THICKNESS:
            self.y = SCREEN_HEIGHT - WALL_THICKNESS - self.radius

        # Update the rect attribute to reflect the current position
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)

        # Update the syringe's position if it is stuck to the enemy
        if self.stuck_syringe:
            relative_x, relative_y = self.stuck_syringe.relative_position
            self.stuck_syringe.x = self.x + relative_x
            self.stuck_syringe.y = self.y + relative_y
            self.stuck_syringe.rect = self.stuck_syringe.rotated_image.get_rect(center=(self.stuck_syringe.x, self.stuck_syringe.y))

    def hit(self):
        self.hit_count += 1
        if self.hit_count >= 3:
            self.speed = 0
        else:
            self.speed = max(0, self.initial_speed - (self.initial_speed / 3) * self.hit_count)

        if self.speed == 0: 
            self.dead = True
        else:
            self.hit_time = time.time()  # Record the time when the enemy was hit


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        if self.stuck_syringe:
            self.stuck_syringe.draw(screen)