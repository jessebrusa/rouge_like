import pygame
import os
import time

from data.settings import *

from core.player.syringe import Syringe

RADIUS = 20
COLOR = GREY
PLAYER_SPEED = 5

class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.rect = pygame.Rect(self.x - RADIUS, self.y - RADIUS, 2 * RADIUS, 2 * RADIUS)
        self.radius = RADIUS
        self.color = COLOR
        self.speed = PLAYER_SPEED
        self.direction = "up"
        self.last_shot_time = 0
        self.shoot_interval = 0.25
        self.syringes = []
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

        # Draw syringes
        for syringe in self.syringes:
            syringe.draw(screen)


    def shoot_syringe(self):
        current_time = time.time()
        if current_time - self.last_shot_time >= self.shoot_interval:
            self.last_shot_time = current_time
            syringe = Syringe(self.x, self.y, self.direction)
            self.syringes.append(syringe)
            return syringe
        return None

    def update(self):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_UP] or keys[pygame.K_w]):
            self.x -= self.speed
            self.y -= self.speed
            self.direction = "up_left"
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (keys[pygame.K_UP] or keys[pygame.K_w]):
            self.x += self.speed
            self.y -= self.speed
            self.direction = "up_right"
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            self.x -= self.speed
            self.y += self.speed
            self.direction = "down_left"
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            self.x += self.speed
            self.y += self.speed
            self.direction = "down_right"
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
            self.direction = "left"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
            self.direction = "right"
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
            self.direction = "up"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
            self.direction = "down"

        if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
            self.shoot_syringe()

        # Update syringes
        for syringe in self.syringes:
            syringe.update()

    def update_rect(self):
        self.rect.topleft = (self.x - self.radius, self.y - self.radius)

    def is_off_screen(self):
        return self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT
    
    def clear_syringes(self):
        self.syringes = []