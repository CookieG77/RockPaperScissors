"""Module for GUI utilities."""

import pygame
from OpenGL.GL import *
from src.scripts.gui_version.game_state_manager.game_state_manager import StateManager

class PyGameMenu:
    """Class to handle PyGame menu operations."""

    def __init__(self, manager: StateManager, screen: pygame.Surface, bg=None):
        """Base menu class.

        Parameters:
        - manager: StateManager that owns this state
        - screen: pygame display surface
        - bg: optional shared GPUBackground instance to render behind the UI
        """
        self.manager = manager
        self.screen = screen
        self.bg = bg
        self.t = 0

    def handle_event(self, event):
        """Handle events."""

    def update(self, dt):
        """Update menu."""
        self.t += dt

    def draw(self, screen: pygame.Surface):
        """Draw menu to the screen."""


def _constrain_to_aspect(w: int, h: int, aspect: float, min_w: int=200, min_h: int=150, max_w: int=3840, max_h: int=2160):
    """Constrain width and height to a given aspect ratio while fitting within max dimensions."""
    # clamp incoming values
    w = max(min_w, min(max_w, int(w)))
    h = max(min_h, min(max_h, int(h)))

    # keep width and fit height => h_from_w
    h_from_w = int(round(w / aspect))
    if h_from_w <= h:
        return w, max(min_h, h_from_w)

    # otherwise fit width to h
    w_from_h = int(round(h * aspect))
    return max(min_w, w_from_h), h

def _blit_surface_to_opengl(surface : pygame.Surface):
    """Convert a pygame surface to an OpenGL texture and return the texture ID.

    Note: use flip=False so we get the raw top-to-bottom ordering from pygame and
    supply texcoords accordingly when drawing.
    """
    # Pygame.image.tostring flip argument controls vertical ordering of rows.
    # Use flip=True so the image rows are flipped on upload — this matches
    # the texcoord layout used in the fullscreen quad and avoids a mirrored UI.
    texture_data = pygame.image.tostring(surface, "RGBA", True)
    width, height = surface.get_size()

    # ensure correct row alignment for tightly packed RGBA data
    try:
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    except Exception:
        pass

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return tex_id

def _draw_texture_fullscreen(tex_id):
    """Draw a fullscreen quad with the given texture ID."""
    # attempt to read GL state, but remain silent on failure
    try:
        vp = glGetIntegerv(GL_VIEWPORT)
        curp = glGetIntegerv(GL_CURRENT_PROGRAM)
    except Exception:
        vp = None
        curp = None

    # We'll use a small textured shader and a cached VAO/VBO to draw the quad
    global _ui_shader_prog, _ui_vao, _ui_vbo, _ui_tex_loc

    def _create_ui_resources():
        # simple textured shader
        vert = b"""
        #version 120
        attribute vec2 position;
        attribute vec2 texcoord;
        varying vec2 v_texcoord;
        void main() {
            v_texcoord = texcoord;
            gl_Position = vec4(position, 0.0, 1.0);
        }
        """
        frag = b"""
        #version 120
        varying vec2 v_texcoord;
        uniform sampler2D tex;
        void main() {
            gl_FragColor = texture2D(tex, v_texcoord);
        }
        """

        # compile shaders
        vs = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vs, vert)
        glCompileShader(vs)
        if not glGetShaderiv(vs, GL_COMPILE_STATUS):
            raise RuntimeError(glGetShaderInfoLog(vs))

        fs = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fs, frag)
        glCompileShader(fs)
        if not glGetShaderiv(fs, GL_COMPILE_STATUS):
            raise RuntimeError(glGetShaderInfoLog(fs))

        prog = glCreateProgram()
        glAttachShader(prog, vs)
        glAttachShader(prog, fs)
        glBindAttribLocation(prog, 0, b'position')
        glBindAttribLocation(prog, 1, b'texcoord')
        glLinkProgram(prog)
        if not glGetProgramiv(prog, GL_LINK_STATUS):
            raise RuntimeError(glGetProgramInfoLog(prog))

        # create VBO/VAO for a fullscreen quad (two triangles)
        # Quad vertices: position.x, position.y, tex.u, tex.v
        # Use texcoords that map the (flipped) pygame image data correctly so
        # top-left in the image maps to top-left on screen.
        # Flip V only (swap the v values) to correct vertical mirroring
        # Texcoords: flip V so the top row of the pygame surface (which is
        # first in the string when flip=False) maps to the top of the screen.
        quad = (GLfloat * 24)(
            # position.x, position.y, tex.u, tex.v
            # bottom-left
            -1.0, -1.0, 0.0, 0.0,
            # bottom-right
             1.0, -1.0, 1.0, 0.0,
            # top-right
             1.0,  1.0, 1.0, 1.0,
            # bottom-left
            -1.0, -1.0, 0.0, 0.0,
            # top-right
             1.0,  1.0, 1.0, 1.0,
            # top-left
            -1.0,  1.0, 0.0, 1.0
        )

        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, sizeof(quad), quad, GL_STATIC_DRAW)

        # position attribute (location 0)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * sizeof(GLfloat), ctypes.c_void_p(0))
        # texcoord attribute (location 1)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * sizeof(GLfloat), ctypes.c_void_p(2 * sizeof(GLfloat)))

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        return prog, vao, vbo

    if '_ui_shader_prog' not in globals():
        _ui_shader_prog, _ui_vao, _ui_vbo = _create_ui_resources()
        try:
            _ui_tex_loc = glGetUniformLocation(_ui_shader_prog, b'tex')
        except Exception:
            _ui_tex_loc = -1

    # save previous program to restore later
    try:
        prev_prog = glGetIntegerv(GL_CURRENT_PROGRAM)
    except Exception:
        prev_prog = 0

    # disable depth and enable blending so UI draws on top
    try:
        glDisable(GL_DEPTH_TEST)
        glDepthMask(GL_FALSE)
    except Exception:
        pass
    try:
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    except Exception:
        pass

    # use the UI shader and draw the quad
    try:
        glUseProgram(_ui_shader_prog)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        if _ui_tex_loc is not None and _ui_tex_loc != -1:
            glUniform1i(_ui_tex_loc, 0)
        glBindVertexArray(_ui_vao)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glBindVertexArray(0)
    except Exception:
        # shader draw failure — suppress detailed debug output in normal runs
        pass

    # restore GL state
    try:
        glDisable(GL_BLEND)
    except Exception:
        pass
    try:
        glDepthMask(GL_TRUE)
    except Exception:
        pass
    try:
        if prev_prog:
            glUseProgram(int(prev_prog))
    except Exception:
        pass

def render_surface_fullscreen(surface: pygame.Surface):
    """Render a pygame surface fullscreen using OpenGL."""
    tex_id = _blit_surface_to_opengl(surface)
    _draw_texture_fullscreen(tex_id)
    glDeleteTextures([tex_id])
