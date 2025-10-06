"""Module for terminal utilities."""

import os

def get_input(prompt: str) -> str:
    """Helper function to get user input."""
    return input(prompt).strip().lower()

def clear_cmd():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def move_cursor_up(lines: int = 1):
    """
    Moves the cursor up by the specified number of lines in the terminal.
    Used to overwrite previous lines.
    """
    # ANSI sequence to move the cursor up
    print(f"\033[{lines}A", end='')


def clear_line():
    """
    Clears the current line in the terminal.

    Uses ANSI escape sequence to clear the line and carriage return to go to
    the beginning of the line. If the terminal doesn't support ANSI, the
    fallback is to print a newline of spaces (less ideal but portable).
    """
    # ANSI: erase line and return carriage
    try:
        # '\x1b[2K' clears the entire line, '\r' returns carriage
        print('\x1b[2K\r', end='')
    except OSError:
        # Fallback: overwrite with spaces then return carriage
        print(' ' * 80 + '\r', end='')


def clear_previous_line(lines: int = 1):
    """
    Move up `lines` lines and clear them.

    Useful when you just printed something and want to remove it before
    printing a shorter/longer string, avoiding leftover characters.
    """
    move_cursor_up(lines)
    clear_line()

def loading_animation(
    duration: int = 2, 
    interval: float = 0.25, 
    loading_str = "Loading", 
    suffix: str = "", 
    animation_frames: list = [".  ", ".. ", "..."]
    ):
    """Displays a simple loading animation for the specified duration."""
    import time
    start_time = time.time()
    i = 0
    while time.time() - start_time < duration:
        print(f"{loading_str}{animation_frames[i]}{suffix}", end="\r")
        i = (i + 1) % len(animation_frames)
        time.sleep(interval)
    clear_line()
    
def set_text_color(color_code: int, string: str = "") -> str:
    """Sets the terminal text color using ANSI escape codes."""
    return(f"\033[{color_code}m{string}\033[0m")