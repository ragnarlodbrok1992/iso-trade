import pygame
import pyrr
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# Global variables to represent the camera position, zoom level, and rotation angle
camera_x = 0.0
camera_y = 0.0
zoom = 1.0
rotation_angle = 0.0

def create_checkered_pattern(size, num_tiles):
    vertices = []
    colors = [(0.0, 0.0, 1.0), (1.0, 1.0, 0.0)]  # Blue and Yellow colors

    for i in range(num_tiles):
        for j in range(num_tiles):
            color_index = (i + j) % 2
            color = colors[color_index]

            x0, y0 = size * (i - num_tiles/2), size * (j - num_tiles/2)
            x1, y1 = size * (i + 1 - num_tiles/2), size * (j + 1 - num_tiles/2)

            vertices.extend([x0, y0, color[0], color[1], color[2]])
            vertices.extend([x1, y0, color[0], color[1], color[2]])
            vertices.extend([x1, y1, color[0], color[1], color[2]])
            vertices.extend([x0, y1, color[0], color[1], color[2]])

    return np.array(vertices, dtype=np.float32)

def handle_input():
    global camera_x, camera_y, zoom, rotation_angle

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.KEYDOWN:
            # Camera movement keys
            if event.key == pygame.K_LEFT:
                camera_x -= 10
            elif event.key == pygame.K_RIGHT:
                camera_x += 10
            elif event.key == pygame.K_UP:
                camera_y -= 10
            elif event.key == pygame.K_DOWN:
                camera_y += 10

            # Zoom keys
            elif event.key == pygame.K_q:
                zoom *= 1.1
            elif event.key == pygame.K_e:
                zoom /= 1.1

            # Camera rotation keys
            elif event.key == pygame.K_r:
                rotation_angle -= 5
            elif event.key == pygame.K_t:
                rotation_angle += 5

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    vertex_shader = """
    #version 330 core
    in vec2 position;
    in vec3 color;
    out vec3 v_color;

    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;

    void main()
    {
        v_color = color;
        gl_Position = projection * view * model * vec4(position, 0.0, 1.0);
    }
    """

    fragment_shader = """
    #version 330 core
    in vec3 v_color;
    out vec4 FragColor;

    void main()
    {
        FragColor = vec4(v_color, 1.0);
    }
    """

    shader_program = glCreateProgram()
    vertex_shader_object = glCreateShader(GL_VERTEX_SHADER)
    fragment_shader_object = glCreateShader(GL_FRAGMENT_SHADER)

    glShaderSource(vertex_shader_object, vertex_shader)
    glShaderSource(fragment_shader_object, fragment_shader)

    glCompileShader(vertex_shader_object)
    glCompileShader(fragment_shader_object)

    glAttachShader(shader_program, vertex_shader_object)
    glAttachShader(shader_program, fragment_shader_object)

    glLinkProgram(shader_program)
    glUseProgram(shader_program)

    pattern_vao = glGenVertexArrays(1)
    pattern_vbo = glGenBuffers(1)

    glBindVertexArray(pattern_vao)

    pattern_data = create_checkered_pattern(50, 8)

    glBindBuffer(GL_ARRAY_BUFFER, pattern_vbo)
    glBufferData(GL_ARRAY_BUFFER, pattern_data, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(GLfloat), ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(GLfloat), ctypes.c_void_p(2 * sizeof(GLfloat)))
    glEnableVertexAttribArray(1)

    glBindVertexArray(0)

    projection = pyrr.matrix44.create_orthogonal_projection(-display[0]/2, display[0]/2, -display[1]/2, display[1]/2, -1, 1)
    glUniformMatrix4fv(glGetUniformLocation(shader_program, "projection"), 1, GL_FALSE, projection)

    while True:
        handle_input()

        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(shader_program)

        model = pyrr.matrix44.create_from_translation(pyrr.Vector3([camera_x, camera_y, 0.0]))
        glUniformMatrix4fv(glGetUniformLocation(shader_program, "model"), 1, GL_FALSE, model)

        view = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, 0.0]))
        view = pyrr.matrix44.multiply(view, pyrr.matrix44.create_from_z_rotation(rotation_angle))
        glUniformMatrix4fv(glGetUniformLocation(shader_program, "view"), 1, GL_FALSE, view)

        glBindVertexArray(pattern_vao)
        glDrawArrays(GL_QUADS, 0, len(pattern_data) // 5)
        glBindVertexArray(0)

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
