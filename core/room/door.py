import pygame
from data.settings import *

DOOR_EXTRA_LENGTH = 10

class Door:
    def __init__(self, side, pos, size, color):
        self.side = side
        self.pos = pos
        self.size = size + DOOR_EXTRA_LENGTH
        self.color = color
        self.rect = self.create_rect()
        self.open = False

    def create_rect(self):
        if self.side == 'top':
            return pygame.Rect(self.pos, 0, self.size, WALL_THICKNESS)
        elif self.side == 'bottom':
            return pygame.Rect(self.pos, SCREEN_HEIGHT - WALL_THICKNESS, self.size, WALL_THICKNESS)
        elif self.side == 'left':
            return pygame.Rect(0, self.pos, WALL_THICKNESS, self.size)
        elif self.side == 'right':
            return pygame.Rect(SCREEN_WIDTH - WALL_THICKNESS, self.pos, WALL_THICKNESS, self.size)

    def draw(self, screen):
        if not self.open:  # Only draw the door if it is not open
            pygame.draw.rect(screen, self.color, self.rect)

    def check_collision(self, player_rect):
        if self.open:
            return False  # No collision if the door is open
        return self.rect.colliderect(player_rect)