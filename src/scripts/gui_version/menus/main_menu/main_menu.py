"""Module for the main menu."""

import os
import random

import pygame

from src.scripts.gui_version.game_state_manager.game_state_manager import StateManager
from src.scripts.gui_version.gpu_graphics.gpu_graphics import GPUBackground
from src.scripts.gui_version.gui_utils.gui_utils import PyGameMenu, render_surface_fullscreen


class MainMenu(PyGameMenu):
    """Class to handle the main menu."""

    def __init__(self, manager: StateManager, screen: pygame.Surface):
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
        vertex_src_path = os.path.join(script_dir, "..", "..", "..", "..", "assets", "shaders", "main_menu_background.vert")
        fragment_src_path = os.path.join(script_dir, "..", "..", "..", "..", "assets", "shaders", "main_menu_background.frag")
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

        # font and texture cache for OpenGL-rendered text
        self.font = pygame.font.SysFont("arial", 36)
        # cache: (label, color) -> (texid, w, h)
        self._text_tex_cache = {}


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

    def draw(self, screen):
        # Render GL background first
        self.bg.render()

        # Create a transparent surface for the UI
        ui_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        font = pygame.font.SysFont("Arial", 40)

        # Render debug background to test if ui is drawn over it (transparent)
        # Use alpha=0 so the GL background remains visible under the UI
        ui_surface.fill((0, 0, 0, 0))

        # Render the menu title
        text = font.render("Mon super menu", True, (255, 255, 255))
        ui_surface.blit(text, (50, 50))

        # Render menu options
        for i, (label, _) in enumerate(self.buttons):
            color = (255, 255, 0) if i == self.selected_index else (200, 200, 200)
            rect = pygame.Rect(50, 150 + i * 60, 200, 50)
            pygame.draw.rect(ui_surface, (0, 0, 0, 150), rect)
            text = self.font.render(label, True, color)
            ui_surface.blit(text, (rect.x + 10, rect.y + 10))
        
        

        # Render the UI surface to the screen
        render_surface_fullscreen(ui_surface)

    def update_size(self, width, height):
        """Update the size of the background."""
        self.bg.update_size(width, height)
