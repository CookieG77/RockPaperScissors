"""Module for GUI utilities."""

import pygame
import os
import random
from src.scripts.gui_version.gpu_graphics.gpu_graphics import GPUBackground


class PyGameMenu:
    """Class to handle PyGame menu operations."""

    def __init__(self, manager, screen):
        self.manager = manager
        self.t = 0
        self.has_animated_bg = False

    def handle_event(self, event):
        """Handle events."""

    def update(self, dt):
        """Update menu."""
        self.t += dt

    def draw(self, screen):
        """Draw menu to the screen."""




class MainMenu(PyGameMenu):
    """Class to handle the main menu."""

    def __init__(self, manager, screen):
        super().__init__(manager, screen)

        # Menu options
        self.buttons = [
            ("Start Game", None),
            ("Quit", None)
        ]
        self.selected_index = 0
        self.has_animated_bg = True

        # Set up background
        w, h = screen.get_size()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        vertex_src_path = os.path.join(script_dir, "..", "..", "..", "assets", "shaders", "background.vert")
        fragment_src_path = os.path.join(script_dir, "..", "..", "..", "assets", "shaders", "background.frag")
        with open(vertex_src_path, 'r', encoding='utf-8') as f:
            vertex_src = f.read()
        with open(fragment_src_path, 'r', encoding='utf-8') as f:
            fragment_src = f.read()

        # Saturated palette to choose from for the background
        main_colors = [
            (1.0, 0.0, 0.0, 1.0),    # red
            (0.0, 1.0, 0.0, 1.0),    # green
            (0.0, 0.0, 1.0, 1.0),    # blue
            (0.5, 0.0, 0.5, 1.0),    # purple
            (1.0, 0.5, 0.0, 1.0),    # orange
            (0.6, 0.0, 1.0, 1.0),    # violet / magenta variant
            (0.0, 1.0, 1.0, 1.0),    # cyan
            (1.0, 1.0, 0.0, 1.0),    # yellow
        ]

        # Pass three main colours to the shader (shader expects vec4)
        # Choose three distinct colours from the palette
        if len(main_colors) >= 3:
            c1, c2, c3 = random.sample(main_colors, 3)
        else:
            # fallback: repeat as needed
            picks = (main_colors * 3)[:3]
            c1, c2, c3 = picks

        uniforms = {
            'colour_1': c1,
            'colour_2': c2,
            'colour_3': c3,
        }
        self.bg = GPUBackground(w, h, vertex_src, fragment_src, uniforms)


    def handle_event(self, event):
        """Handle events specific to the main menu."""
        for e in event:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.buttons)
                elif e.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.buttons)
                elif e.key == pygame.K_RETURN:
                    _, target = self.buttons[self.selected_index]
                    if target:
                        self.manager.change(target)
                    else: # If no target is passed, quit the game
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
                        print("Quitting game...")
        
    def draw(self, screen):
        screen.fill('#FFFFFF')
        self.bg.render()
        
    def update_size(self, width, height):
        """Update the size of the background."""
        self.bg.update_size(width, height) 
