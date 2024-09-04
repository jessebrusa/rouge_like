import pygame
import sys
import os

from data.settings import *
  
TEXT_SPEED = 1.4
INTRO_TEXT_URL = os.path.join(ROOT_DIR, "data", "text", "intro.txt")

class Intro:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.title_font = pygame.font.Font(None, TITLE_FONT_SIZE) 

        with open(INTRO_TEXT_URL) as f:
            self.intro_text = f.read().splitlines() 

    def justify_text(self, lines, max_width):
        justified_lines = []
        for line in lines:
            words = line.split()
            if not words:
                justified_lines.append("")
                continue

            line_surface = self.font.render(line, True, WHITE)
            line_width = line_surface.get_width()

            if line_width <= max_width:
                justified_lines.append(line)
                continue

            justified_line = ""
            current_width = 0
            for word in words:
                word_surface = self.font.render(word + " ", True, WHITE)
                word_width = word_surface.get_width()
                if current_width + word_width <= max_width:
                    justified_line += word + " "
                    current_width += word_width
                else:
                    justified_lines.append(justified_line.strip())
                    justified_line = word + " "
                    current_width = word_width
            justified_lines.append(justified_line.strip())

        return justified_lines

    def scroll_text(self, lines, speed=TEXT_SPEED):
        lines.reverse()

        max_width = SCREEN_WIDTH * 0.8
        justified_lines = self.justify_text(lines, max_width)

        # Create surfaces for each line
        line_surfaces = [self.font.render(line, True, WHITE) for line in justified_lines]
        line_height = line_surfaces[0].get_height()
        total_height = line_height * len(line_surfaces)
        start_y = -total_height  # Start from the top of the screen

        while start_y < SCREEN_HEIGHT:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        return  # Skip the scrolling and go to the menu

            self.screen.fill(BLACK)
            y = start_y
            for line_surface in line_surfaces:
                line_rect = line_surface.get_rect(center=(SCREEN_WIDTH // 2, y))
                self.screen.blit(line_surface, line_rect)
                y += line_height

            start_y += speed  # Move down the text
            pygame.display.flip()
            self.clock.tick(FPS)

    def menu(self):
        options = ["Play", "Quit"]
        selected = 0
        title_lines = GAME_TITLE.split('\n')  # Split the title into lines

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(options)
                    elif event.key == pygame.K_UP:
                        selected = (selected - 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        return options[selected]

            self.screen.fill(BLACK)
            
            # Render the title
            title_start_y = SCREEN_HEIGHT // 4 - 50  # Adjust this value to move the title higher or lower
            for i, line in enumerate(title_lines):
                title_surface = self.title_font.render(line, True, WHITE)
                title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, title_start_y + i * TITLE_FONT_SIZE))
                self.screen.blit(title_surface, title_rect)

            # Render the menu options
            for i, option in enumerate(options):
                color = WHITE if i == selected else (GREY)
                option_surface = self.font.render(option, True, color)
                option_rect = option_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 40))
                self.screen.blit(option_surface, option_rect)

            pygame.display.flip()
            self.clock.tick(FPS)

    def run_intro(self):
        self.scroll_text(self.intro_text, speed=TEXT_SPEED)
        choice = self.menu()
        return choice

if __name__ == "__main__":
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()

    intro = Intro(screen, clock)
    choice = intro.run_intro()
    if choice == "Play":
        print("Starting the game...")
        # Call your game loop here
    elif choice == "Quit":
        pygame.quit()
        sys.exit()