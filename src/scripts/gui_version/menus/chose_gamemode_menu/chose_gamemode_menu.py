"""Module for the menu to choose game mode in the GUI version."""

import pygame


from src.scripts.gui_version.game_state_manager.game_state_manager import StateManager
from src.scripts.gui_version.gpu_graphics.gpu_graphics import GPUBackground
from src.scripts.gui_version.gui_utils.gui_utils import PyGameMenu, render_surface_fullscreen
from src.scripts.gui_version.menus.game_menu.game_menu import GameMenu
from typing import Callable, Optional


class ChoseGameModeMenu(PyGameMenu):
    """Class to handle the game mode selection menu."""

    def __init__(self, manager: StateManager, screen: pygame.Surface, bg: GPUBackground, back_factory: Optional[Callable] = None):
        """Initializes the game mode selection menu."""
        super().__init__(manager, screen, bg)

        # Menu options. The back target is provided by the caller via back_factory.
        back_target = back_factory if back_factory is not None else None
        self.buttons = [
            ("VS Computer", lambda mgr: GameMenu(mgr, screen, self.bg, back_factory=back_target)),
            ("VS Player", lambda mgr: GameMenu(mgr, screen, self.bg, False, back_target)),
            ("Back to Main Menu", back_target),
        ]
        self.selected_index = 0

        # Background info
        self.bg = bg
        # font used for menu rendering
        self.font = pygame.font.SysFont("arial", 36)

    def handle_event(self, event):
        """Handle events specific to the game mode selection menu."""

        for e in event:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP or e.key == pygame.K_z:
                    self.selected_index = (self.selected_index - 1) % len(self.buttons)
                elif e.key == pygame.K_DOWN or e.key == pygame.K_s or e.key == pygame.K_TAB:
                    self.selected_index = (self.selected_index + 1) % len(self.buttons)
                elif e.key == pygame.K_RETURN or e.key == pygame.K_SPACE:
                    _, target = self.buttons[self.selected_index]
                    if target:
                        # target is expected to be a factory that creates a new state
                        self.manager.change(target)
                    else: # If no target is passed, quit the game
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def draw(self, screen: pygame.Surface):
        # Render GL background first
        self.bg.render()

        # Create a transparent surface for the UI
        ui_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        font = pygame.font.SysFont("Arial", 40)

        # Render the menu title
        text = font.render("Choose Game Mode", True, (255, 255, 255))
        ui_surface.blit(text, (50, 50))

        # Render menu options
        for i, (label, _) in enumerate(self.buttons):
            color = (255, 255, 0) if i == self.selected_index else (200, 200, 200)
            rect = pygame.Rect(50, 150 + i * 60, 300, 50)
            pygame.draw.rect(ui_surface, (0, 0, 0, 150), rect)
            text = self.font.render(label, True, color)
            ui_surface.blit(text, (rect.x + 10, rect.y + 10))
        
        # Render the UI surface to the screen
        render_surface_fullscreen(ui_surface)
