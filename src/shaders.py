VERTEX_SHADER = """
#version 330 core
in vec2 position;
in vec3 color;
out vec3 v_color;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {

}
"""

FRAGMENT_SHADER = """
#version 330 core
in vec3 v_color;
out vec4 FragColor;

void main() {
    FragColor = vec4(v_color, 1.0);
}
"""


class UniformShaderProgram():

    def __init__(self, vertex_source, fragment_source):
        self.shader_program = None

        self.shader_program = None
        self.vertex_shader_object = None
        self.fragment_shader_object = None

