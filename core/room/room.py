import pygame
import random
from data.settings import *
from core.enemies.enemy import Enemy
from core.room.door import Door  

NUM_OPENINGS = 2
BORDER_COLOR = BLUE
RED_COLOR = RED 

class Room:
    def __init__(self, screen, room_counter, fixed_opening=None):
        self.screen = screen
        self.thickness = WALL_THICKNESS
        self.opening_size = WALL_OPENING_SIZE
        self.rect = pygame.Rect(self.thickness, self.thickness, SCREEN_WIDTH - 2 * self.thickness, SCREEN_HEIGHT - 2 * self.thickness)
        self.room_counter = room_counter
        self.fixed_opening = fixed_opening
        self.openings = self.generate_openings(fixed_opening)
        self.enemies = self.generate_enemies(self.room_counter) 
        self.doors = self.create_doors()
        self.door_opened = False  # Track if the door is opened

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
        else:
            # Ensure the first room has only one door
            side = random.choice(['top', 'bottom', 'left', 'right'])
            if side in ['top', 'bottom']:
                position = random.randint(0, SCREEN_WIDTH - self.opening_size)
            else:
                position = random.randint(0, SCREEN_HEIGHT - self.opening_size)
            openings.append((side, position))
            return openings  # Return immediately to ensure only one door
        
        while len(openings) < NUM_OPENINGS:
            side = random.choice(['top', 'bottom', 'left', 'right'])
            if side in ['top', 'bottom']:
                position = random.randint(0, SCREEN_WIDTH - self.opening_size)
            else:
                position = random.randint(0, SCREEN_HEIGHT - self.opening_size)

            if not any(existing_side == side and abs(existing_pos - position) < self.opening_size + WALL_THICKNESS for existing_side, existing_pos in openings):
                openings.append((side, position))

        return openings
    
    def generate_enemies(self, num_enemies):
        enemies = []
        for _ in range(num_enemies):
            enemies.append(Enemy())
        return enemies

    def create_doors(self):
        doors = []
        self.fixed_door = None
        self.random_door = None
    
        for side, pos in self.openings:
            door = Door(side, pos, self.opening_size + 10, RED_COLOR)
            doors.append(door)
            if self.fixed_opening and (side, pos) == self.fixed_opening:
                self.fixed_door = door
            else:
                self.random_door = door
    
        return doors

    def draw(self):
        # Draw top border
        for x in range(0, SCREEN_WIDTH, WALL_THICKNESS):
            if not any(side == 'top' and pos <= x < pos + self.opening_size for side, pos in self.openings):
                pygame.draw.rect(self.screen, BORDER_COLOR, (x, 0, WALL_THICKNESS, WALL_THICKNESS))
        # Draw bottom border
        for x in range(0, SCREEN_WIDTH, WALL_THICKNESS):
            if not any(side == 'bottom' and pos <= x < pos + self.opening_size for side, pos in self.openings):
                pygame.draw.rect(self.screen, BORDER_COLOR, (x, SCREEN_HEIGHT - WALL_THICKNESS, WALL_THICKNESS, WALL_THICKNESS))
        # Draw left border
        for y in range(0, SCREEN_HEIGHT, WALL_THICKNESS):
            if not any(side == 'left' and pos <= y < pos + self.opening_size for side, pos in self.openings):
                pygame.draw.rect(self.screen, BORDER_COLOR, (0, y, WALL_THICKNESS, WALL_THICKNESS))
        # Draw right border
        for y in range(0, SCREEN_HEIGHT, WALL_THICKNESS):
            if not any(side == 'right' and pos <= y < pos + self.opening_size for side, pos in self.openings):
                pygame.draw.rect(self.screen, BORDER_COLOR, (SCREEN_WIDTH - WALL_THICKNESS, y, WALL_THICKNESS, WALL_THICKNESS))

        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Draw doors
        for door in self.doors:
            door.draw(self.screen)

        # Check if all enemies are dead and open the random door
        if not self.door_opened and all(enemy.dead for enemy in self.enemies):
            self.open_a_door()
            self.door_opened = True

    def open_a_door(self):
        # Ensure the fixed door remains closed
        if self.fixed_door:
            self.fixed_door.open = False
        
        # Open the random door
        if self.random_door:
            self.random_door.open = True