import pygame
import sys
import os

from data.settings import *

class GameOver:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
        self.options = ["Play Again", "Quit"]
        self.selected_option = 0

    def run_game_over(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return self.options[self.selected_option]
                    elif event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)

            self.screen.fill(BLACK)
            self.draw_text("GAME OVER", self.title_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
            for i, option in enumerate(self.options):
                color = WHITE if i == self.selected_option else GREY
                self.draw_text(option, self.font, color, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50)

            pygame.display.flip()
            self.clock.tick(FPS)

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()

    game_over = GameOver(screen, clock)
    choice = game_over.run_game_over()
    if choice == "Play Again":
        print("Restarting the game...")
        # Call your game loop here
    elif choice == "Quit":
        pygame.quit()
        sys.exit()