"""Module for the Rock-Paper-Scissors GUI game logic."""

import pygame
import random
try:
    # normal import (package context)
    from ..gui_utils.gui_utils import _constrain_to_aspect
    from ..game_state_manager.game_state_manager import StateManager
    from ..menus.main_menu.main_menu import MainMenu
    from ..gpu_graphics.gpu_graphics import GPUBackground
except ImportError:
    # fallback for direct execution (not for production use)
    import sys
    import pathlib

    repo_root = pathlib.Path(__file__).resolve().parents[4]  # go up to the project root
    sys.path.insert(0, str(repo_root))
    from src.scripts.gui_version.gui_utils.gui_utils import _constrain_to_aspect
    from src.scripts.gui_version.game_state_manager.game_state_manager import StateManager
    from src.scripts.gui_version.menus.main_menu.main_menu import MainMenu
    from src.scripts.gui_version.gpu_graphics.gpu_graphics import GPUBackground

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

    # Create the state manager and initial state
    manager = StateManager(None)

    # Create a single shared GPUBackground for all menus
    import pathlib
    # compute repository root (same logic as fallback imports earlier)
    repo_root = pathlib.Path(__file__).resolve().parents[4]
    vertex_src_path = repo_root / 'src' / 'assets' / 'shaders' / 'main_menu_background.vert'
    fragment_src_path = repo_root / 'src' / 'assets' / 'shaders' / 'main_menu_background.frag'
    with open(vertex_src_path, 'r', encoding='utf-8') as f:
        vertex_src = f.read()
    with open(fragment_src_path, 'r', encoding='utf-8') as f:
        fragment_src = f.read()

    w, h = screen.get_size()
    # choose a random saturated theme for the shared background
    color_themes = [
        ((1.0, 0.41, 0.38, 1.0), (0.39, 0.58, 0.93, 1.0), (1.0, 1.0, 0.0, 1.0)),
        ((0.13, 0.55, 0.13, 1.0), (0.0, 0.5, 0.5, 1.0), (0.27, 0.51, 0.71, 1.0)),
        ((1.0, 0.65, 0.0, 1.0), (1.0, 0.27, 0.0, 1.0), (1.0, 0.75, 0.8, 1.0)),
        ((0.54, 0.17, 0.89, 1.0), (0.0, 0.5, 0.0, 1.0), (0.94, 0.97, 1.0, 1.0)),
        ((0.68, 0.85, 0.9, 1.0), (1.0, 0.87, 0.83, 1.0), (0.74, 0.99, 0.79, 1.0))
    ]
    chosen_color_theme = random.choice(color_themes)
    uniforms = {
        'colour_1': chosen_color_theme[0],
        'colour_2': chosen_color_theme[1],
        'colour_3': chosen_color_theme[2],
    }
    shared_bg = None
    try:
        shared_bg = GPUBackground(w, h, vertex_src, fragment_src, uniforms)
    except Exception:
        shared_bg = None

    main_menu = MainMenu(manager, screen, bg=shared_bg)
    manager.current_state = main_menu

    # Main game loop
    running : bool = True
    while running:
        dt = clock.tick(60) / 1000.0 
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                new_w, new_h = event.w, event.h
                w, h = _constrain_to_aspect(new_w, new_h, SCREEN_W / SCREEN_H, SCREEN_W, SCREEN_H)
                screen = pygame.display.set_mode((w, h), flags)
                manager.update_size(w, h)
        manager.handle_event(events)
        manager.update(dt)
        manager.draw(screen)
        pygame.display.flip()
    pygame.quit()
    

if __name__ == "__main__": # Start the GUI game (for direct execution and debugging)
    start_gui_game()
