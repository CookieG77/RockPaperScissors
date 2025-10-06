"""Starts the Rock-Paper-Scissors game in terminal or GUI mode based on user input."""

from src.scripts.game import start_terminal_game

def get_input(prompt: str) -> str:
    """Helper function to get user input."""
    return input(prompt).strip().lower()

if __name__ == "__main__":
    while True:
        playerInput = get_input("What do you want to do ? (play/quit): ")
        if playerInput == "play":
            playerInput = get_input("What version do you want to play (terminal/gui) ? ")
            if playerInput == "terminal":
                print("Starting terminal version...")
                start_terminal_game()
                break
            if playerInput == "gui":
                # TODO : Implement GUI version here
                break
            print("Invalid input. Please enter 'terminal' or 'gui'.")
        elif playerInput == "quit":
            break
        else:
            print("Invalid input. Please enter 'play' or 'quit'.")
