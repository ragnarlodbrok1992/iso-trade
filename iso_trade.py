# Global imports
import pygame
import random

# Local imports
from src.static_entities.iso_map import IsoMap

# Constants
SIZE = [800, 600]
GAME_TITLE = "IsoTrade"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ISO_TILE_SIZE = 25


def draw_isometric_tile(screen, x, y, size):
    pygame.draw.polygon(screen, WHITE,
                        [(x, y), (x + size, y + size / 2), (x, y + size), (x - size, y + size / 2)])


def draw_isometric_tile_color(screen, x, y, size, color):
    pygame.draw.polygon(screen, color,
                        [(x, y), (x + size, y + size / 2), (x, y + size), (x - size, y + size / 2)])


class IsoTrade:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Tweaking variables
        self.num_rows = 10
        self.num_cols = 10

    def run(self):
        while self.running:
            # Checking events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Check for Q key pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

            # Rendering
            self.screen.fill(BLACK)

            # Draw an iso tile
            # pygame.draw.rect(self.screen, WHITE, (100, 100, 50, 25))
            for i in range(self.num_cols):  # Drawing columns
                for j in range(self.num_rows):  # Drawing rows
                    # Prepare random color
                    random_r = random.randint(0, 255)
                    random_g = random.randint(0, 255)
                    random_b = random.randint(0, 255)
                    RANDOM_COLOR = (random_r, random_g, random_b)

                    # Call draw function
                    draw_isometric_tile_color(self.screen,
                                              100 + i * ISO_TILE_SIZE,
                                              100 + j * ISO_TILE_SIZE + (i % 2) * ISO_TILE_SIZE / 2,
                                              ISO_TILE_SIZE,
                                              RANDOM_COLOR)

            # draw_isometric_tile(self.screen, 100, 100, ISO_TILE_SIZE)

            # Last stuff in frame
            pygame.display.flip()
            self.clock.tick(60)

        # Quit the game
        pygame.quit()


if __name__ == "__main__":
    game = IsoTrade()
    game.run()
