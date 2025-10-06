"""Module for GPU-based graphics using shaders."""

import time
import numpy as np
import pygame
from OpenGL.GL import *


class GPUBackground:
    """Class to handle GPU-based animated background using shaders."""
    def __init__(self, width, height, vertex_src, fragment_src, uniforms=None):
        self.width = width
        self.height = height
        self.start_time = time.time()

        # Optional dict of custom uniform name -> python value
        self.uniforms = uniforms or {}

        self.program = self._create_shader(vertex_src, fragment_src)
        glUseProgram(self.program)

        # Create the fullscreen quad
        vertices = np.array([
            -1, -1,  1, -1,  1,  1,
            -1, -1,  1,  1, -1,  1
        ], dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        pos_loc = glGetAttribLocation(self.program, "position")
        glEnableVertexAttribArray(pos_loc)
        glVertexAttribPointer(pos_loc, 2, GL_FLOAT, GL_FALSE, 0, None)

        self.i_time_loc = glGetUniformLocation(self.program, "iTime")
        self.i_resolution_loc = glGetUniformLocation(self.program, "iResolution")
        # cache locations for any custom uniforms provided
        self._uniform_locs = {}
        for name in self.uniforms.keys():
            loc = glGetUniformLocation(self.program, name)
            self._uniform_locs[name] = loc
            if loc == -1:
                print(f"Warning: uniform '{name}' not found in shader (location -1)")

    def _create_shader(self, vertex_src, fragment_src):
        """Compile and link vertex and fragment shaders."""
        # compile vertex
        vs = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vs, vertex_src)
        glCompileShader(vs)
        if not glGetShaderiv(vs, GL_COMPILE_STATUS):
            raise RuntimeError(glGetShaderInfoLog(vs))

        # compile fragment
        fs = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fs, fragment_src)
        glCompileShader(fs)
        if not glGetShaderiv(fs, GL_COMPILE_STATUS):
            raise RuntimeError(glGetShaderInfoLog(fs))

        # link program
        prog = glCreateProgram()
        glAttachShader(prog, vs)
        glAttachShader(prog, fs)
        glLinkProgram(prog)
        if not glGetProgramiv(prog, GL_LINK_STATUS):
            raise RuntimeError(glGetProgramInfoLog(prog))
        return prog

    def render(self):
        """Render the animated background."""
        t = time.time() - self.start_time
        # ensure the viewport matches the stored size so the shader draws to the whole window
        try:
            glViewport(0, 0, int(self.width), int(self.height))
        except Exception:
            pass
        # debug current viewport
        # try to ensure viewport is what we expect; ignore failures
        try:
            vp = glGetIntegerv(GL_VIEWPORT)
        except Exception:
            vp = None
        # Use a neutral clear color (black) in normal runs
        try:
            glClearColor(0.0, 0.0, 0.0, 1.0)
        except Exception:
            pass

        glUseProgram(self.program)
        # debug current program id
        try:
            curp = glGetIntegerv(GL_CURRENT_PROGRAM)
        except Exception:
            curp = None
        glUniform1f(self.i_time_loc, t)
        glUniform2f(self.i_resolution_loc, self.width, self.height)

        # upload custom uniforms
        for name, value in self.uniforms.items():
            loc = self._uniform_locs.get(name, -1)
            if loc == -1:
                continue
            try:
                self._upload_uniform(loc, value)
            except Exception as e:
                print(f"Failed to upload uniform {name}: {e}")

        glClear(GL_COLOR_BUFFER_BIT)
        # ensure our fullscreen quad VAO is bound so the shader has vertex data
        try:
            glBindVertexArray(self.vao)
        except Exception:
            pass
        glDrawArrays(GL_TRIANGLES, 0, 6)
        try:
            glBindVertexArray(0)
        except Exception:
            pass
        # check for GL errors after draw
        try:
            err = glGetError()
            # silently ignore GL errors in normal runs; leave checks for developer diagnostics
        except Exception:
            pass

    def update_size(self, width, height):
        """Update the resolution uniform when the window is resized."""
        self.width = width
        self.height = height
        # update the GL viewport immediately to match new size
        try:
            glViewport(0, 0, int(self.width), int(self.height))
        except Exception:
            pass

    def _upload_uniform(self, loc, value):
        """Upload a Python value to a uniform location.

        Supported types: int, float, bool, tuple/list/numpy array (size 1..4)
        """
        # booleans -> ints
        if isinstance(value, bool):
            glUniform1i(loc, int(value))
            return

        # ints
        if isinstance(value, int):
            glUniform1i(loc, int(value))
            return

        # floats
        if isinstance(value, float):
            glUniform1f(loc, float(value))
            return

        # sequences / numpy arrays
        if isinstance(value, (list, tuple)) or (np and isinstance(value, np.ndarray)):
            arr = np.array(value)
            # integer arrays
            if arr.dtype.kind in ("i", "u"):
                if arr.size == 1:
                    glUniform1i(loc, int(arr.flat[0]))
                elif arr.size == 2:
                    glUniform2i(loc, int(arr.flat[0]), int(arr.flat[1]))
                elif arr.size == 3:
                    glUniform3i(loc, int(arr.flat[0]), int(arr.flat[1]), int(arr.flat[2]))
                elif arr.size == 4:
                    glUniform4i(loc, int(arr.flat[0]), int(arr.flat[1]), int(arr.flat[2]), int(arr.flat[3]))
                else:
                    raise ValueError("Integer uniform arrays >4 not supported")
                return

            # float arrays
            if arr.dtype.kind in ("f", "c", "u"):
                if arr.size == 1:
                    glUniform1f(loc, float(arr.flat[0]))
                elif arr.size == 2:
                    glUniform2f(loc, float(arr.flat[0]), float(arr.flat[1]))
                elif arr.size == 3:
                    glUniform3f(loc, float(arr.flat[0]), float(arr.flat[1]), float(arr.flat[2]))
                elif arr.size == 4:
                    glUniform4f(loc, float(arr.flat[0]), float(arr.flat[1]), float(arr.flat[2]), float(arr.flat[3]))
                else:
                    # try bulk upload as 1fv
                    try:
                        glUniform1fv(loc, arr.astype(np.float32))
                    except Exception:
                        raise ValueError("Float uniform arrays >4 not supported by helper")
                return

        raise TypeError(f"Unsupported uniform type for value: {type(value)}")
