import pygame
from OpenGL.GL import *
import OpenGL.GL.shaders as shaders
import numpy as np

# Some constants

ASPECT_RATIO = 4/3
FOV = 90  # In degrees

vertex_shader = """
#version 330

in vec3 position;
in vec3 color;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 frag_color;

void main()
{
    gl_Position = projection * view * model * vec4(position, 1.0);
    frag_color = color;
}
"""

fragment_shader = """
#version 330

in vec3 frag_color;

out vec4 FragColor;

void main()
{
    FragColor = vec4(frag_color, 1.0);
}
"""

# Functions for MVP matrix for perspective projection
def perspective(fov_degrees=FOV, aspect_ratio=ASPECT_RATIO, near=0.1, far=1000.0):
    fov_rad = np.radians(fov_degrees)
    f = 1.0 / np.tan(fov_rad / 2.0)
    z_range = near - far

    perspective_matrix = np.array([
        [f / aspect_ratio, 0.0,                         0.0,                          0.0],
        [0.0,              f,                           0.0,                          0.0],
        [0.0,              0.0,                     (far + near) / z_range,          (2.0 * far * near) / z_range],
        [0.0,              0.0,                        -1.0,                          0.0]
    ])

    return perspective_matrix

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.OPENGL | pygame.DOUBLEBUF)

    vertices = np.array([
        [-5.0, -5.0, 0.0,  1.0, 0.0, 0.0], # Red
        [5.0, -5.0, 0.0,  0.0, 1.0, 0.0], # Green
        [0.0,  5.0, 0.0,  0.0, 0.0, 1.0], # Blue
    ], dtype=np.float32)

    vertex_shader_id = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader_id, vertex_shader)
    glCompileShader(vertex_shader_id)

    fragment_shader_id = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader_id, fragment_shader)
    glCompileShader(fragment_shader_id)

    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader_id)
    glAttachShader(shader_program, fragment_shader_id)
    glLinkProgram(shader_program)

    glDeleteShader(vertex_shader_id)
    glDeleteShader(fragment_shader_id)

    # projection = np.array([
    #     [2.0 / display[0], 0, 0, 0],
    #     [0, 2.0 / display[1], 0, 0],
    #     [0, 0, -1, 0],
    #     [-1, -1, 0, 1],
    # ], dtype=np.float32)

    # projection_location = glGetUniformLocation(shader_program, "projection")
    # glUniformMatrix4fv(projection_location, 1, GL_FALSE, projection)

    model = np.identity(4, dtype=np.float32)
    view = np.identity(4, dtype=np.float32)

    # Something is wrong with projection array I think
    projection = np.array([
        [2.0 / display[0], 0, 0, 0],
        [0, 2.0 / display[1], 0, 0],
        [0, 0, -1, 0],
        [-1, -1, 0, 1]
    ], dtype=np.float32)

    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)

    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * np.dtype(np.float32).itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * np.dtype(np.float32).itemsize, ctypes.c_void_p(3 * np.dtype(np.float32).itemsize))
    glEnableVertexAttribArray(1)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    # Get location of uniform variables in the shader program
    model_location = glGetUniformLocation(shader_program, "model")
    view_location = glGetUniformLocation(shader_program, "view")
    projection_location = glGetUniformLocation(shader_program, "projection")

    # DEBUG prints
    print("Perspective matrix:", perspective())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(shader_program)

        glUniformMatrix4fv(model_location, 1, GL_FALSE, model)
        glUniformMatrix4fv(view_location, 1, GL_FALSE, view)
        glUniformMatrix4fv(projection_location, 1, GL_FALSE, projection)

        glBindVertexArray(vao)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glBindVertexArray(0)

        pygame.display.flip()


if __name__ == "__main__":
    main()
