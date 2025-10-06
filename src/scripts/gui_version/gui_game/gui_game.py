"""Module for the Rock-Paper-Scissors GUI game logic."""

import pygame
try:
    # normal import (package context)
    from ..gui_utils.gui_utils import MainMenu
    from ..game_state_manager.game_state_manager import StateManager
except ImportError:
    # fallback for direct execution (not for production use)
    import sys
    import pathlib

    repo_root = pathlib.Path(__file__).resolve().parents[4]  # go up to the project root
    sys.path.insert(0, str(repo_root))
    from src.scripts.gui_version.gui_utils.gui_utils import MainMenu
    from src.scripts.gui_version.game_state_manager.game_state_manager import StateManager

# Define global constants
global SCREEN_H, SCREEN_W
SCREEN_H, SCREEN_W = 360, 640

def start_gui_game():
    """
    Placeholder function to start the GUI version of the game.
    """
    # Initialize Pygame and create an OpenGL-capable display
    pygame.init()
    # Request an OpenGL context so PyOpenGL functions are available
    flags = pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), flags)
    clock = pygame.time.Clock()

    # Create the state manager
    manager = StateManager(MainMenu(None, screen))
    manager.state_manager = manager

    # Main game loop
    running : bool = True
    while running:
        dt = clock.tick(60) / 1000.0 
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), flags)
                manager.state_manager.update_size(event.w, event.h)
        manager.handle_event(events)
        manager.update(dt)
        manager.draw(screen)
        pygame.display.flip()
    pygame.quit()
    

if __name__ == "__main__":
    start_gui_game()
