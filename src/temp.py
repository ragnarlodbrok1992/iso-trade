import pygame
import glm
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Global variables to represent the camera position, zoom level, and rotation angle
camera_x = 0.0
camera_y = 0.0
zoom = 1.0
rotation_angle = 0.0

# TODO: move camera values to vector
camera_vector = glm.vec4(camera_x, camera_y, zoom, rotation_angle)
print(camera_vector)

def draw_checkered_pattern(size, num_tiles):
    colors = [(0.0, 0.0, 1.0), (1.0, 1.0, 0.0)]  # Blue and Yellow colors

    for i in range(num_tiles):
        for j in range(num_tiles):
            color_index = (i + j) % 2
            glColor3f(*colors[color_index])  # Use the appropriate color from the list

            x0, y0 = size * (i - num_tiles/2), size * (j - num_tiles/2)
            x1, y1 = size * (i + 1 - num_tiles/2), size * (j + 1 - num_tiles/2)

            glBegin(GL_QUADS)
            glVertex2f(x0, y0)
            glVertex2f(x1, y0)
            glVertex2f(x1, y1)
            glVertex2f(x0, y1)
            glEnd()

def handle_input():
    global camera_x, camera_y, zoom, rotation_angle

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

        # Continous presses
        else:
            keys = pygame.key.get_pressed()

            # Moves
            if keys[pygame.K_a]:
                camera_x -= 1
            elif keys[pygame.K_d]:
                camera_x += 1
            elif keys[pygame.K_w]:
                camera_y -= 1
            elif keys[pygame.K_s]:
                camera_y += 1

            # Rotates
            elif keys[pygame.K_q]:
                rotation_angle -= 1
            elif keys[pygame.K_e]:
                rotation_angle += 1 

            # Zooms
            elif keys[pygame.K_z]:
                zoom *= 1.1
            elif keys[pygame.K_x]:
                zoom /= 1.1


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluOrtho2D(-display[0]/2, display[0]/2, -display[1]/2, display[1]/2)

    while True:
        # TODO: fix first "hiccup" in movement
        # TODO: add moving with mouse
        handle_input()

        glClear(GL_COLOR_BUFFER_BIT)

        # TODO: check what glPushMatrix/glPopMatrix is doing
        glPushMatrix()
        
        # TODO: make camera be super isometric and only move in one plane with zooms
        glTranslatef(camera_x, camera_y, 0)
        glScalef(zoom, zoom, 1.0)
        glRotatef(rotation_angle, 0, 0, 1)  # Apply rotation around the Z-axis

        draw_checkered_pattern(50, 8)

        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
