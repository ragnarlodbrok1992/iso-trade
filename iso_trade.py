# Global imports
import pygame

# Local imports
from src.static_entities.iso_map import IsoMap

# Constants
SIZE = [800, 600]
GAME_TITLE = "IsoTrade"


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

            # Rendering
            self.screen.fill((255, 255, 255))
            pygame.display.flip()
            self.clock.tick(60)

        # Quit the game
        pygame.quit()


if __name__ == "__main__":
    game = IsoTrade()
    game.run()
