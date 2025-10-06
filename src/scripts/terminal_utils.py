"""Module for terminal utilities."""

import os

def get_input(prompt: str) -> str:
    """Helper function to get user input."""
    return input(prompt).strip().lower()

def clear_cmd():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')
