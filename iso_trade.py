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
ISO_TILE_GRID = []


def draw_isometric_tile(screen, x, y, size):
    pygame.draw.polygon(screen, WHITE,
                        [(x, y), (x + size, y + size / 2), (x, y + size), (x - size, y + size / 2)])


def draw_isometric_tile_color(screen, x, y, size, color):
    pygame.draw.polygon(screen, color,
                        [(x, y), (x + size, y + size / 2), (x, y + size), (x - size, y + size / 2)])

def draw_text(screen, text, color, size, x, y):
    pass


class IsoTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (random.randint(0, 255),
                      random.randint(0, 255),
                      random.randint(0, 255))


class IsoTileGrid:

    def __init__(self, num_rows, num_cols):
        self.iso_tile_grid_container = []
        self.iso_tile_x = 100
        self.iso_tile_y = 100

        # Rows and cols
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._prepare_grid(num_rows, num_cols)

    def _prepare_grid(self, num_rows, num_cols):
        for i in range(num_cols):
            for j in range(num_rows):
                self.iso_tile_grid_container.append(IsoTile(i, j))

    def render_grid(self, screen):
        for tile in self.iso_tile_grid_container:
            draw_isometric_tile_color(screen,
                                      self.iso_tile_x + tile.x * ISO_TILE_SIZE,
                                      self.iso_tile_y + tile.y * ISO_TILE_SIZE + (tile.x % 2) * ISO_TILE_SIZE / 2,
                                      ISO_TILE_SIZE,
                                      tile.color)


class IsoTrade:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Tweaking variables
        self.num_rows = 17
        self.num_cols = 25

        # Preparing grid
        self.iso_tile_grid = IsoTileGrid(self.num_rows, self.num_cols)

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

            # Draw grid
            self.iso_tile_grid.render_grid(self.screen)

            # Draw debug test text on screen

            # Last stuff in frame
            pygame.display.flip()
            self.clock.tick(60)

        # Quit the game
        pygame.quit()


if __name__ == "__main__":
    game = IsoTrade()
    game.run()
