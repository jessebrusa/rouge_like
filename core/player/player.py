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
        self.syringe_image = pygame.image.load(SYRINGE_URL)
        self.syringe_image = pygame.transform.scale(self.syringe_image, (self.radius * SYRINGE_SCALE, self.radius * SYRINGE_SCALE))
        
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

        # Rotate the syringe images
        self.update_syringe_images()

    def update_syringe_images(self):
        if self.direction in ["up", "up_right", "up_left"]:
            self.syringe_left = pygame.transform.rotate(self.syringe_image, self.direction_dict[self.direction] - SYRING_ROTATION)
            self.syringe_right = pygame.transform.rotate(self.syringe_image, self.direction_dict[self.direction] + SYRING_ROTATION)
        elif self.direction in ["right"]:
            self.syringe_left = pygame.transform.rotate(self.syringe_image, self.direction_dict[self.direction] - SYRING_ROTATION)
            self.syringe_right = pygame.transform.rotate(self.syringe_image, self.direction_dict[self.direction] + SYRING_ROTATION)
        elif self.direction in ["down", "down_left"]:
            self.syringe_left = pygame.transform.rotate(self.syringe_image, self.direction_dict[self.direction] + SYRING_ROTATION)
            self.syringe_right = pygame.transform.rotate(self.syringe_image, self.direction_dict[self.direction] - SYRING_ROTATION)
        elif self.direction in ["left", "up_left"]:
            self.syringe_left = pygame.transform.rotate(self.syringe_image, self.direction_dict[self.direction] - SYRING_ROTATION)
            self.syringe_right = pygame.transform.rotate(self.syringe_image, self.direction_dict[self.direction] + SYRING_ROTATION)
        elif self.direction == "down_right":
            self.syringe_left = pygame.transform.rotate(self.syringe_image, self.direction_dict[self.direction] + SYRING_ROTATION)
            self.syringe_right = pygame.transform.rotate(self.syringe_image, self.direction_dict[self.direction] - SYRING_ROTATION)

    def draw(self, screen):
        # Draw the player
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

        # Draw the syringes on the left and right sides of the player
        syringe_left_width, syringe_left_height = self.syringe_left.get_size()
        syringe_right_width, syringe_right_height = self.syringe_right.get_size()
        
        if self.direction == "right":  # Facing right
            syringe_left_pos = (self.x - syringe_left_width // 2, self.y - self.radius - syringe_left_height // 2 - SYRING_OFFSET - 2)
            syringe_right_pos = (self.x - syringe_right_width // 2, self.y + self.radius - syringe_right_height // 2 + SYRING_OFFSET)
        elif self.direction == "left":  # Facing left
            syringe_left_pos = (self.x - syringe_left_width // 2, self.y + self.radius - syringe_left_height // 2 + SYRING_OFFSET + 2)
            syringe_right_pos = (self.x - syringe_right_width // 2, self.y - self.radius - syringe_right_height // 2 - SYRING_OFFSET)
        elif self.direction == "down":  # Facing down
            syringe_left_pos = (self.x - self.radius - syringe_left_width // 2 - SYRING_OFFSET, self.y - syringe_left_height // 2)
            syringe_right_pos = (self.x + self.radius - syringe_right_width // 2 + SYRING_OFFSET + 2, self.y - syringe_right_height // 2)
        elif self.direction == "up":  # Facing up
            syringe_left_pos = (self.x - self.radius - syringe_left_width // 2 - SYRING_OFFSET -2, self.y - syringe_left_height // 2)
            syringe_right_pos = (self.x + self.radius - syringe_right_width // 2 + SYRING_OFFSET, self.y - syringe_right_height // 2)
        elif self.direction == "up_right":  # Facing up-right
            syringe_left_pos = (self.x - self.radius - syringe_left_width // 2 - 2, self.y - self.radius - syringe_left_height // 2 - 2)
            syringe_right_pos = (self.x + self.radius - syringe_right_width // 2, self.y + self.radius - syringe_right_height // 2)
        elif self.direction == "up_left":  # Facing up-left
            syringe_left_pos = (self.x - self.radius - syringe_left_width // 2 - 2, self.y + self.radius - syringe_left_height // 2 + 2)
            syringe_right_pos = (self.x + self.radius - syringe_right_width // 2, self.y - self.radius - syringe_right_height // 2)
        elif self.direction == "down_right":  # Facing down-right
            syringe_left_pos = (self.x - self.radius - syringe_left_width // 2, self.y + self.radius - syringe_left_height // 2 + 2)
            syringe_right_pos = (self.x + self.radius - syringe_right_width // 2 + 2, self.y - self.radius - syringe_right_height // 2 - 2)
        elif self.direction == "down_left":  # Facing down-left
            syringe_left_pos = (self.x - self.radius - syringe_left_width // 2 - 7, self.y + self.radius - syringe_left_height // 2 - 30)
            syringe_right_pos = (self.x + self.radius - syringe_right_width // 2 - 5, self.y - self.radius - syringe_right_height // 2 + 45)

        screen.blit(self.syringe_left, syringe_left_pos)
        screen.blit(self.syringe_right, syringe_right_pos)

        # Draw the bounding circle around the player
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius, 2)  # Red color with a thickness of 2

        # Draw the bounding rectangles around the syringes with an additional 20-degree offset
        self.draw_rotated_rect(screen, syringe_left_pos, syringe_left_width, syringe_left_height, self.direction_dict[self.direction])
        self.draw_rotated_rect(screen, syringe_right_pos, syringe_right_width - 50, syringe_right_height, self.direction_dict[self.direction])

    def draw_rotated_rect(self, screen, pos, width, height, angle):
        rect = pygame.Rect(pos[0], pos[1], width, height)
        rotated_image = pygame.transform.rotate(pygame.Surface((width, height), pygame.SRCALPHA), angle)
        rotated_rect = rotated_image.get_rect(center=rect.center)
        pygame.draw.rect(screen, (0, 255, 0), rotated_rect, 2)  # Green color with a thickness of 2

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

        self.update_syringe_images()

    def is_off_screen(self):
        return self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT