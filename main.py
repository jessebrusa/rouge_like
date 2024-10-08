import pygame
import sys

from data.settings import *

from core.intro.intro import Intro
from core.game_over.game_over import GameOver

from core.room.room import Room

from core.player.player import Player

from core.collision.collision import CollisionHandler

# Initialize the game
pygame.init()
pygame.display.set_caption(GAME_TITLE)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

def intro_screen():
    intro = Intro(screen, clock)
    choice = intro.run_intro()
    if choice == "Play":
        return True
    elif choice == "Quit":
        pygame.quit()
        sys.exit()

def game_loop():
    player = Player()
    room_counter = 1  # Initialize room_counter
    room = Room(screen, room_counter)
    collision_handler = CollisionHandler()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        # Update
        player.update()
        for enemy in room.enemies:
            enemy.update(player)
        collision_handler.check_player_room_collision(player, room)

        # Check if player moves off-screen through an opening
        side, pos = collision_handler.check_player_off_screen(player, room)
        if side:
            if side == 'left':
                player.x = player.radius
                player.y = pos + room.opening_size // 2
                new_opening = ('right', pos)
            elif side == 'right':
                player.x = SCREEN_WIDTH - player.radius
                player.y = pos + room.opening_size // 2
                new_opening = ('left', pos)
            elif side == 'top':
                player.y = player.radius
                player.x = pos + room.opening_size // 2
                new_opening = ('bottom', pos)
            elif side == 'bottom':
                player.y = SCREEN_HEIGHT - player.radius
                player.x = pos + room.opening_size // 2
                new_opening = ('top', pos)
            room_counter += 1  # Increment room counter
            room = Room(screen, room_counter, fixed_opening=new_opening)
            player.clear_syringes()  # Clear syringes when entering a new room

        # Check for collisions
        if collision_handler.check_player_enemy_collision(player, room.enemies):
            return False  # End the game loop if the player's health is 1 and a collision occurs
        collision_handler.check_syringe_enemy_collision(player.syringes, room.enemies)

        # Draw
        room.draw()
        player.draw(screen)
        for enemy in room.enemies:
            enemy.draw(screen)
        for syringe in player.syringes:
            syringe.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

def game_over():
    game_over_screen = GameOver(screen, clock)
    choice = game_over_screen.run_game_over()
    if choice == "Play Again":
        return True
    elif choice == "Quit":
        pygame.quit()
        sys.exit()

def main():
    # play = intro_screen()
    # if not play:
    #     return

    while True:
        play_again = game_loop()
        if not play_again:
            play_again = game_over()
            if not play_again:
                break

    pygame.quit()

if __name__ == "__main__":
    main()