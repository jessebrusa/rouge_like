import pygame
import math
import time
from data.settings import *
from core.player.player import Player
from core.room.room import Room

class CollisionHandler:
    def __init__(self):
        pass

    def check_player_room_collision(self, player: Player, room: Room):
        if player.x - player.radius < room.thickness:
            if not any(side == 'left' and pos <= player.y <= pos + room.opening_size for side, pos in room.openings):
                player.x = room.thickness + player.radius
        if player.x + player.radius > SCREEN_WIDTH - room.thickness:
            if not any(side == 'right' and pos <= player.y <= pos + room.opening_size for side, pos in room.openings):
                player.x = SCREEN_WIDTH - room.thickness - player.radius
        if player.y - player.radius < room.thickness:
            if not any(side == 'top' and pos <= player.x <= pos + room.opening_size for side, pos in room.openings):
                player.y = room.thickness + player.radius
        if player.y + player.radius > SCREEN_HEIGHT - room.thickness:
            if not any(side == 'bottom' and pos <= player.x <= pos + room.opening_size for side, pos in room.openings):
                player.y = SCREEN_HEIGHT - room.thickness - player.radius

        for syringe in player.syringes:
            room_rect = pygame.Rect(room.thickness, room.thickness, 
                                    SCREEN_WIDTH - 2 * room.thickness, 
                                    SCREEN_HEIGHT - 2 * room.thickness)
            if not room_rect.contains(syringe.rect):
                player.syringes.remove(syringe)


        player_rect = pygame.Rect(player.x - player.radius, player.y - player.radius, player.radius * 2, player.radius * 2)
        for door in room.doors:
            if door.check_collision(player_rect):
                if door.side == 'top':
                    player.y = room.thickness + player.radius
                elif door.side == 'bottom':
                    player.y = SCREEN_HEIGHT - room.thickness - player.radius
                elif door.side == 'left':
                    player.x = room.thickness + player.radius
                elif door.side == 'right':
                    player.x = SCREEN_WIDTH - room.thickness - player.radius
            

    def check_player_off_screen(self, player: Player, room: Room):
        if player.is_off_screen():
            for side, pos in room.openings:
                if side == 'left' and player.x < 0:
                    return 'right', pos
                if side == 'right' and player.x > SCREEN_WIDTH:
                    return 'left', pos
                if side == 'top' and player.y < 0:
                    return 'bottom', pos
                if side == 'bottom' and player.y > SCREEN_HEIGHT:
                    return 'top', pos
        return None, None


    def check_player_enemy_collision(self, player, enemies):
        current_time = time.time()
        if current_time - player.last_collision_time < 1:
            return False  # Skip collision check if 1 second has not passed

        player_rect = pygame.Rect(player.x - player.radius, player.y - player.radius, player.radius * 2, player.radius * 2)
        for enemy in enemies:
            if player_rect.colliderect(enemy.rect):
                player.last_collision_time = current_time  # Update the last collision time
                if player.health > 1:
                    player.health -= 1
                    print(f"Player Health: {player.health}")
                else:
                    return True  # Indicate that the game should end
        return False  # Indicate that the game should continue

    def check_syringe_enemy_collision(self, syringes, enemies):
        for syringe in syringes:
            if syringe.rect is None:
                continue  # Skip syringes that are stuck to enemies
            syringe_rect = syringe.rect  # Use the rect attribute directly
            for enemy in enemies:
                if syringe_rect.colliderect(enemy.rect):
                    if syringe.stuck_enemy:
                        continue  # Continue to check other enemies
                    
                    # Call the hit method on the enemy
                    enemy.hit()

                    # Make the syringe stick to the enemy
                    syringe.moving = False
                    syringe.stuck_enemy = enemy
                    enemy.stuck_syringe = syringe  # Add this line to set the reference to the syringe in the enemy

                    # Calculate the angle between the syringe and the enemy
                    dx = syringe.x - enemy.x
                    dy = syringe.y - enemy.y
                    angle = math.atan2(dy, dx)
                    
                    # Position the syringe at the edge of the enemy's radius
                    syringe.x = enemy.x + enemy.radius * math.cos(angle)
                    syringe.y = enemy.y + enemy.radius * math.sin(angle)
                    syringe.rect = None  # Remove the rect to prevent further collisions

                    syringe.swap_image()
                    