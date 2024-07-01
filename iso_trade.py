# Global imports
import pygame
import random

# Local imports
from src.static_entities.iso_map import IsoMap

# DEBUG
DEBUG = True

# Constants
RATIO_X = 16.0
RATIO_Y = 9.0
RESOLUTION_FACTOR = 100.0  # 100.0 for 1600x900
SIZE = [int(RESOLUTION_FACTOR * RATIO_X), int(RESOLUTION_FACTOR * RATIO_Y)]
print(f"SIZE: {SIZE}")
GAME_TITLE = "IsoTrade"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ISO_TILE_SIZE = 25  # Same as width (x coordinate dimension)
ISO_TILE_HEIGHT = int(ISO_TILE_SIZE / 2)  # Same as height (y coordinate dimension)
if DEBUG:
    print(f"ISO_TILE_HEIGHT: {ISO_TILE_HEIGHT}")


def draw_bounding_box(grid, screen, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
    grid.update_grid_bounding_box()
    pygame.draw.rect(screen, WHITE, (top_left_x, top_left_y,
                                     bottom_right_x - top_left_x,
                                     bottom_right_y - top_left_y), 1)


def draw_isometric_tile(screen, x, y, size):
    pygame.draw.polygon(screen, WHITE,
                        [(x, y), (x + size, y + size / 2), (x, y + size), (x - size, y + size / 2)])


def draw_isometric_tile_color(screen, x, y, size, color):
    pygame.draw.polygon(screen, color,
                        [(x, y), (x + size, y + size / 2), (x, y + size), (x - size, y + size / 2)])


def draw_text(screen, text, color, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


class IsoTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (random.randint(0, 255),
                      random.randint(0, 255),
                      random.randint(0, 255))


class IsoTileGrid:

    def __init__(self, screen, num_rows, num_cols):
        self.iso_tile_grid_container = []
        # This two variables are offsets for the grid
        self.iso_tile_x = 100
        self.iso_tile_y = 100

        # Camera offsets for the grid rendering
        self.camera_x = 0
        self.camera_y = 0

        # Rows and cols
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._prepare_grid(num_rows, num_cols)

        # Grid bounding box
        self.top_left_x = None
        self.top_left_y = None
        self.bottom_right_x = None
        self.bottom_right_y = None
        self.update_grid_bounding_box()

    def update_grid_bounding_box(self):
        self.top_left_x = self.iso_tile_x + self.camera_x - ISO_TILE_SIZE
        self.top_left_y = self.iso_tile_y + self.camera_y
        self.bottom_right_x = self.top_left_x + self.num_cols * ISO_TILE_SIZE + ISO_TILE_SIZE
        self.bottom_right_y = self.top_left_y + self.num_rows * ISO_TILE_SIZE + (ISO_TILE_SIZE / 2)

    def _prepare_grid(self, num_rows, num_cols):
        for i in range(num_cols):
            for j in range(num_rows):
                self.iso_tile_grid_container.append(IsoTile(i, j))

    def _is_grid_clicked(self, screen_x, screen_y) -> bool:
        self.update_grid_bounding_box()

        if self.top_left_x < screen_x < self.bottom_right_x:
            if self.top_left_y < screen_y < self.bottom_right_y:
                return True

        return False

    def render_grid(self, screen):
        for tile in self.iso_tile_grid_container:
            draw_isometric_tile_color(screen,
                                      self.camera_x + self.iso_tile_x + tile.x * ISO_TILE_SIZE,
                                      self.camera_y + self.iso_tile_y + tile.y * ISO_TILE_SIZE + (tile.x % 2) * ISO_TILE_SIZE / 2,
                                      ISO_TILE_SIZE,
                                      tile.color)

    def _get_clicked_tile(self, screen_x, screen_y) -> IsoTile:
        return None

    def select_tile(self, screen_x, screen_y) -> IsoTile:
        if self._is_grid_clicked(screen_x, screen_y):
            print(f"Grid clicked: {screen_x}, {screen_y}")
        # TODO(ragnar): Implement this method
        # This requires transformation from "normal" grid to isometric grid
        return self._get_clicked_tile(screen_x, screen_y)


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
        self.iso_tile_grid = IsoTileGrid(self.screen, self.num_rows, self.num_cols)

    def run(self):
        # Main game loop
        # Control variables
        selected_tile = None
        is_mouse_dragging = False
        has_mouse_dragged = False
        dragging_offset_per_frame = (0, 0)
        dragging_previous_mouse_pos = (0, 0)

        while self.running:
            # Checking events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Keyboard presses
                # Check for Q key pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                # Mouse events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Left mouse button
                    if event.button == 1:
                        # Check where the mouse is clicked
                        button_down_pos = pygame.mouse.get_pos()
                        dragging_previous_mouse_pos = button_down_pos
                        is_mouse_dragging = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    # Left mouse button
                    if event.button == 1:
                        button_up_pos = pygame.mouse.get_pos()
                        is_mouse_dragging = False

                        # Clicking on the grid - on release action
                        if not has_mouse_dragged:
                            selected_tile = self.iso_tile_grid.select_tile(button_up_pos[0], button_up_pos[1])

                        has_mouse_dragged = False

            # Mouse dragging
            # FIXME: Dragging should be only acknowledged when user dragged something - not just clicked
            # in this case the behaviour will be different
            if is_mouse_dragging:
                dragging_offset_per_frame = pygame.mouse.get_pos()
                # TODO implement or use numpy for vector operations
                dragging_difference = (dragging_offset_per_frame[0] - dragging_previous_mouse_pos[0],
                                       dragging_offset_per_frame[1] - dragging_previous_mouse_pos[1])
                # TODO implement vector operation?
                if dragging_difference[0] != 0 or dragging_difference[1] != 0:
                    has_mouse_dragged = True
                    self.iso_tile_grid.camera_x += dragging_difference[0]
                    self.iso_tile_grid.camera_y += dragging_difference[1]

                dragging_previous_mouse_pos = pygame.mouse.get_pos()

            # Rendering
            self.screen.fill(BLACK)

            # Draw grid
            self.iso_tile_grid.render_grid(self.screen)
            # DEBUG renders
            if DEBUG:
                draw_bounding_box(self.iso_tile_grid, self.screen,
                                  self.iso_tile_grid.top_left_x, self.iso_tile_grid.top_left_y,
                                  self.iso_tile_grid.bottom_right_x, self.iso_tile_grid.bottom_right_y)

            # Draw debug test text on screen
            title_text = f"IsoTrade - FPS {int(self.clock.get_fps())}"
            pygame.display.set_caption(title_text)

            # draw_text(self.screen, debug_text, WHITE, 16, 10, 10)
            if selected_tile is not None:
                draw_text(self.screen,
                          f"Selected tile: {selected_tile.x},{selected_tile.y}",
                          WHITE, 16, 10, 30)

            # Last stuff in frame
            pygame.display.flip()
            self.clock.tick(60)

        # Quit the game
        pygame.quit()


if __name__ == "__main__":
    game = IsoTrade()
    game.run()
