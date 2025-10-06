"""Starts the Rock-Paper-Scissors game in terminal or GUI mode based on user input."""

from time import sleep
from src.scripts.game import start_terminal_game
from src.scripts.terminal_utils import get_input

if __name__ == "__main__":
    while True:
        playerInput = get_input("What do you want to do ? (play/quit): ")
        if playerInput == "play":
            playerInput = get_input("What version do you want to play (terminal/gui) ? ")
            if playerInput == "terminal":
                print("Starting terminal version...\n")
                sleep(1) # Pause for dramatic effect
                start_terminal_game()
                break
            if playerInput == "gui":
                print("Starting GUI version...\n")
                sleep(1) # Pause for dramatic effect
                # TODO : Implement GUI version here
                break
            print("Invalid input. Please enter 'terminal' or 'gui'.")
        elif playerInput == "quit":
            break
        else:
            print("Invalid input. Please enter 'play' or 'quit'.")
