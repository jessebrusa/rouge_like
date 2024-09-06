import pygame
import math
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
        player_rect = pygame.Rect(player.x - player.radius, player.y - player.radius, player.radius * 2, player.radius * 2)
        for enemy in enemies:
            if player_rect.colliderect(enemy.rect):
                print("Player Collision detected with enemy!")
                # Handle collision (e.g., reduce player health, remove enemy, etc.)

    def check_syringe_enemy_collision(self, syringes, enemies):
        for syringe in syringes:
            syringe_rect = syringe.rect  # Use the rect attribute directly
            for enemy in enemies:
                if syringe_rect.colliderect(enemy.rect):
                    if syringe.stuck_enemy:
                        return 
                    
                    print("Syringe Collision detected with enemy!")
                    # Reduce enemy speed by 1 until it hits 0
                    enemy.speed = max(0, enemy.speed - 1)

                    # Make the syringe stick to the enemy
                    syringe.moving = False
                    syringe.stuck_enemy = enemy
                    enemy.stuck_syringe = syringe  # Add this line to set the reference to the syringe in the enemy

                    # Calculate the point of collision
                    dx = syringe.x - enemy.x
                    dy = syringe.y - enemy.y
                    distance = math.sqrt(dx**2 + dy**2)
                    if distance != 0:
                        collision_x = enemy.x + (enemy.radius * dx / distance)
                        collision_y = enemy.y + (enemy.radius * dy / distance)
                    else:
                        collision_x, collision_y = enemy.x, enemy.y
                    
                    # Calculate the relative position of the syringe with respect to the enemy
                    relative_x = collision_x - enemy.x
                    relative_y = collision_y - enemy.y
                    
                    # Store the relative position in the syringe
                    syringe.relative_position = (relative_x, relative_y)
                    
                    # Position the syringe at the point of collision
                    syringe.x = collision_x
                    syringe.y = collision_y
                    syringe.rect = syringe.rotated_image.get_rect(center=(syringe.x, syringe.y))

                    syringe.swap_image()
                    