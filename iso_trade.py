# Global imports
import pygame

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


class IsoTrade:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

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
            draw_isometric_tile(self.screen, 100, 100, ISO_TILE_SIZE)

            # Last stuff in frame
            pygame.display.flip()
            self.clock.tick(60)

        # Quit the game
        pygame.quit()


if __name__ == "__main__":
    game = IsoTrade()
    game.run()
