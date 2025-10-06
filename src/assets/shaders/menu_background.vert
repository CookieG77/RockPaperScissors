#version 330

// Simple passthrough vertex shader for 2D full-screen quads
layout(location = 0) in vec2 position;
out vec2 uv;

void main() {
    // Map position [-1,1] to uv [0,1]
    uv = position * 0.5 + 0.5;
    gl_Position = vec4(position, 0.0, 1.0);
}
