"""Module for the main menu."""

import pygame

from src.scripts.gui_version.game_state_manager.game_state_manager import StateManager
from src.scripts.gui_version.gui_utils.gui_utils import PyGameMenu, render_surface_fullscreen
from src.scripts.gui_version.menus.chose_gamemode_menu.chose_gamemode_menu import ChoseGameModeMenu
from src.scripts.gui_version.gpu_graphics.gpu_graphics import GPUBackground


class MainMenu(PyGameMenu):
    """Class to handle the main menu."""

    def __init__(self, manager: StateManager, screen: pygame.Surface, bg : GPUBackground):
        super().__init__(manager, screen, bg)

        # Background info
        self.selected_index = 0

        # Set up background
        self.bg = bg

        # Menu buttons with factories that need self.bg
        self.buttons = [
            ("Start Game", lambda mgr: ChoseGameModeMenu(mgr, screen, self.bg, back_factory=lambda m: MainMenu(m, screen, self.bg))),
            ("Quit", None)
        ]
        # font and texture cache for OpenGL-rendered text
        self.font = pygame.font.SysFont("arial", 36)
        # cache: (label, color) -> (texid, w, h)
        self._text_tex_cache = {}


    def handle_event(self, event):
        """Handle events specific to the main menu."""

        for e in event:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP or e.key == pygame.K_z:
                    self.selected_index = (self.selected_index - 1) % len(self.buttons)
                elif e.key == pygame.K_DOWN or e.key == pygame.K_s or e.key == pygame.K_TAB:
                    self.selected_index = (self.selected_index + 1) % len(self.buttons)
                elif e.key == pygame.K_RETURN or e.key == pygame.K_SPACE:
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
