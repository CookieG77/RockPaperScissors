from src.scripts import game

if __name__ == "__main__":
    while True:
        playerInput = input("What do you want to do ? (play/quit): ").strip().lower()
        if playerInput == "play":
            playerInput = input("What version do you want to play (terminal/gui) ? ").strip().lower()
            if playerInput == "terminal":
                print("Starting terminal version...")
                # TODO : Implement terminal version here
                break
            elif playerInput == "gui":
                # TODO : Implement GUI version here
                break
            else:
                print("Invalid input. Please enter 'terminal' or 'gui'.")
        elif playerInput == "quit":
            break
        else:
            print("Invalid input. Please enter 'play' or 'quit'.")