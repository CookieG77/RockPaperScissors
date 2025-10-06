"""Bootstraps the Rock-Paper-Scissors game by starting the desired version (terminal or GUI)."""

from time import sleep
from src.scripts.game import start_terminal_game
from src.scripts.terminal_utils import get_input, clear_cmd

def start_game():
    """
    Starts the Rock-Paper-Scissors game in terminal or GUI mode based on user input.
    """
    clear_cmd()
    print("Welcome to Rock-Paper-Scissors!\n")
    while True:
        user_input = get_input("What do you want to do ? (play/quit): ")
        if user_input == "play" or user_input == "p":
            user_input = get_input("What version do you want to play (terminal/gui) ? ")
            if user_input == "terminal" or user_input == "t":
                print("Starting terminal version...\n")
                sleep(1) # Pause for dramatic effect
                start_terminal_game()
                break
            if user_input == "gui" or user_input == "g":
                print("Starting GUI version...\n")
                sleep(1) # Pause for dramatic effect
                # TODO : Implement GUI version here
                break
            print("Invalid input. Please enter 'terminal' or 'gui'.")
        elif user_input == "quit" or user_input == "q":
            break
        else:
            print("Invalid input. Please enter 'play' or 'quit'.")
    print("\rGoodbye!")
