import pygame
from data.settings import *
from core.player.player import Player
from core.room.room import Room

class CollisionHandler:
    def __init__(self):
        pass

    def check_player_room_collision(self, player: Player, room: Room):
        # Check collision with room borders considering room thickness and gaps
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


    def check_player_enemy_collision(self, player: Player, enemies):
        # Check collision with enemies
        for enemy in enemies:
            if pygame.sprite.collide_circle(player, enemy):
                # Handle collision
                pass