"""Module for terminal utilities."""

import itertools
import os
import sys
import threading
from time import sleep, time

LOADING_STYLE1 = [".  ", ".. ", "..."]
LOADING_STYLE2 = ["|", "/", "-", "\\"]

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

# def loading_animation(
#     duration: int = 2,
#     interval: float = 0.25,
#     prefix: str = "Loading",
#     suffix: str = "",
#     animation_frames = None
#     ):
#     """
#     Displays a simple loading animation for the specified duration.
    
#     Args:
#         duration (int): Total duration of the animation in seconds.
#         interval (float): Time between frame updates in seconds.
#         prefix (str): String to display before the animation frames.
#         suffix (str): String to display after the animation frames.
#         animation_frames (list[str]): List of strings representing animation frames.
#     """
#     if animation_frames is None:
#         animation_frames = LOADING_STYLE1
#     start_time = time()
#     i = 0
#     while time() - start_time < duration:
#         print(f"{prefix}{animation_frames[i]}{suffix}", end="\r")
#         i = (i + 1) % len(animation_frames)
#         sleep(interval)
#     clear_line()

def set_text_color(color_code: int, string: str = "") -> str:
    """
    Sets the terminal text color using ANSI escape codes.
    
    Args:
        color_code (int): The ANSI color code (e.g., 31 for red, 32 for green).
        string (str): The string to colorize.
        
    Returns:
        str: The colorized string.
        
    Example:
        print(set_text_color(31, "This text is red"))
        print(set_text_color(32, "This text is green"))
        print(set_text_color(34, "This text is blue"))
        print(set_text_color(93, "This text is bright yellow"))
    """
    return f"\033[{color_code}m{string}\033[0m"

class LoadingAnimation:
    """
    Class to handle loading animations in the terminal.
    
    Args:
        frames (list[str]): List of strings representing animation frames.
        delay (float): Time between frame updates in seconds.
    """
    def __init__(self, frames, delay=0.1):
        self.frames = itertools.cycle(frames)
        self.delay = delay
        self.running = False
        self.current_frame = next(self.frames)
        self.thread = None

    def _animate(self):
        while self.running:
            self.current_frame = next(self.frames)
            sleep(self.delay)

    def start(self):
        """
        Starts the loading animation in a separate thread.

        Returns:
            LoadingAnimation: The instance of the loading animation.
        """
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._animate)
            self.thread.start()
        return self

    def stop(self):
        """
        Stops the loading animation and waits for the thread to finish.
        Returns:
            LoadingAnimation: The instance of the loading animation.
        """
        if self.running:
            self.running = False
            self.thread.join(timeout = 0.1)
        return self

    def __str__(self):
        return self.current_frame

class DotsAnimation(LoadingAnimation):
    """Dot animation using LoadingAnimation class."""
    def __init__(self, delay=0.25):
        super().__init__(LOADING_STYLE1, delay)

class SpinnerAnimation(LoadingAnimation):
    """Spinner animation using LoadingAnimation class."""
    def __init__(self, delay=0.1):
        super().__init__(LOADING_STYLE2, delay)

# TODO: Set thread_animation correctly to run animations in a thread to not encumber main thread
def thread_animation(animation_class, duration, *args, **kwargs):
    """
    Runs a loading animation for a specified duration.
    Args:
        animation_class: The class of the animation to run (e.g., DotAnimation).
        duration (int): Duration to run the animation in seconds.
        *args, **kwargs: Arguments to pass to the animation class constructor.
    """
    anim = animation_class(*args, **kwargs).start()

    def auto_stop():
        sleep(duration)
        anim.stop()

    threading.Thread(target=auto_stop).start()

    return anim

def print_animation(template: str, duration, update_interval=0.2, animation_frames=None):
    """
    Print a terminal animation using a provided f-string template for a certain duration.        
    Args:
        template (str): Template string with a placeholder {} for the animation frame.
        duration (int): Duration to run the animation in seconds.
        update_interval (float): Time between frame updates in seconds.
        animation_frames (list[str]): List of animation frames to cycle through.
    """
    if animation_frames is None:
        animation_frames = LOADING_STYLE1

    start_time = time()
    frame_cycle = itertools.cycle(animation_frames)

    while time() - start_time < duration:
        current_frame = next(frame_cycle)
        # Use format() to replace {} placeholder with the current frame
        output = template.format(current_frame)
        sys.stdout.write(f"\r{output}")
        sys.stdout.flush()
        sleep(update_interval)

    # Clear the line and print newline when done
    sys.stdout.write("\r" + " " * len(template.format("...")) + "\r")
    sys.stdout.flush()
