"""Module for the Rock-Paper-Scissors GUI game logic."""

import pygame

pygame.init()
screen = pygame.display.set_mode((640, 360))
clock = pygame.time.Clock()

def update_display():
    """Update the game display."""
    pygame.display.flip()
    clock.tick(60)


def start_gui_game():
    """
    Placeholder function to start the GUI version of the game.
    """
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill('#FFFFFF')
        update_display()

if __name__ == "__main__":
    start_gui_game()
