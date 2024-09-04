import pygame
import random
from data.settings import *

THICKNESS = 10
OPENING_SIZE = 150
NUM_OPENINGS = 2
BORDER_COLOR = BLUE

class Room:
    def __init__(self, screen, fixed_opening=None):
        self.screen = screen
        self.thickness = THICKNESS
        self.opening_size = OPENING_SIZE
        self.openings = self.generate_openings(fixed_opening)

    def generate_openings(self, fixed_opening):
        openings = []
        if fixed_opening:
            side, pos = fixed_opening
            if side == 'left':
                openings.append(('right', pos))
            elif side == 'right':
                openings.append(('left', pos))
            elif side == 'top':
                openings.append(('bottom', pos))
            elif side == 'bottom':
                openings.append(('top', pos))
        
        while len(openings) < NUM_OPENINGS:
            side = random.choice(['top', 'bottom', 'left', 'right'])
            if side in ['top', 'bottom']:
                position = random.randint(0, SCREEN_WIDTH - OPENING_SIZE)
            else:
                position = random.randint(0, SCREEN_HEIGHT - OPENING_SIZE)

            # Ensure openings are not directly next to each other
            if not any(existing_side == side and abs(existing_pos - position) < OPENING_SIZE + THICKNESS for existing_side, existing_pos in openings):
                openings.append((side, position))
        return openings

    def draw(self):
        # Draw top border
        for x in range(0, SCREEN_WIDTH, THICKNESS):
            if not any(side == 'top' and pos <= x < pos + OPENING_SIZE for side, pos in self.openings):
                pygame.draw.rect(self.screen, BORDER_COLOR, (x, 0, THICKNESS, THICKNESS))
        # Draw bottom border
        for x in range(0, SCREEN_WIDTH, THICKNESS):
            if not any(side == 'bottom' and pos <= x < pos + OPENING_SIZE for side, pos in self.openings):
                pygame.draw.rect(self.screen, BORDER_COLOR, (x, SCREEN_HEIGHT - THICKNESS, THICKNESS, THICKNESS))
        # Draw left border
        for y in range(0, SCREEN_HEIGHT, THICKNESS):
            if not any(side == 'left' and pos <= y < pos + OPENING_SIZE for side, pos in self.openings):
                pygame.draw.rect(self.screen, BORDER_COLOR, (0, y, THICKNESS, THICKNESS))
        # Draw right border
        for y in range(0, SCREEN_HEIGHT, THICKNESS):
            if not any(side == 'right' and pos <= y < pos + OPENING_SIZE for side, pos in self.openings):
                pygame.draw.rect(self.screen, BORDER_COLOR, (SCREEN_WIDTH - THICKNESS, y, THICKNESS, THICKNESS))