"""Module for the Rock-Paper-Scissors terminal game logic."""

import random
import os

from src.scripts.terminal_utils.terminal_utils import loading_animation, set_text_color

try:
    # normal import (package context)
    from ..terminal_utils.terminal_utils import (
        get_input,
        clear_cmd,
        move_cursor_up,
        clear_previous_line,
    )
except ImportError:
    # fallback for direct execution (not for production use)
    import sys
    import pathlib

    repo_root = pathlib.Path(__file__).resolve().parents[2]  # go up to the project root
    sys.path.insert(0, str(repo_root))
    from src.scripts.terminal_utils.terminal_utils import (
        get_input,
        clear_cmd,
        move_cursor_up,
        clear_previous_line,
    )


choices = ["rock", "paper", "scissors"]
shortcut_choices = {"r": "rock", "p": "paper", "s": "scissors"}

# Get the absolute path to the welcome.txt file
script_dir = os.path.dirname(os.path.abspath(__file__))
welcome_file_path = os.path.join(script_dir, "..", "..", "assets", "text", "welcome.txt")


def start_terminal_game():
    """>
    Description:
    Starts a terminal version of the Rock-Paper-Scissors game.
    The game continues until the player types 'stop'.
    The player is prompted to choose between rock, paper, or scissors.
    The computer randomly selects one of the three options.
    The winner is determined based on the classic rules of the game.
    ```
        1. Rock crushes scissors.
        2. Scissors cut paper.
        3. Paper covers rock.
    ```
    If the player inputs an invalid choice, they are prompted to try again.

    Returns: None

    Example:
    ```
    startTerminalGame()
    # Output:
    # Choose rock, paper, or scissors: rock
    # Computer chose scissors.
    # You win!
    #
    # Choose rock, paper, or scissors: paper
    # Computer chose rock.
    # You win!
    #
    # Choose rock, paper, or scissors: scissors
    # Computer chose scissors.
    # It's a tie!
    #
    # Choose rock, paper, or scissors: stop
    # Game stopped.
    ```
    Note: The game is case-insensitive and ignores leading/trailing whitespace.
    But it does not account for typos or alternative spellings.
    """
    playing_against_machine: bool = False
    scores: list[int] = [0, 0]  # [player, computer]
    # Read and display the welcome message
    clear_cmd()
    try:
        with open(welcome_file_path, "r", encoding="utf-8") as f:
            print(set_text_color(92, f.read()))
    except OSError:
        print(set_text_color(92, "Welcome to Rock-Paper-Scissors!"))  # Fallback message

    while True:
        player_input = get_input(
            "Do you want to play against the computer or another player? (machine/player): "
        )
        if player_input == "machine" or player_input == "m":
            playing_against_machine = True
            break
        if player_input == "player" or player_input == "p":
            playing_against_machine = False
            break
        print("Invalid input. Please enter 'machine' or 'player'.")
    clear_cmd()

    # Start the game loop
    print("Type 'stop' to end the game at any time.\n")
    while True:
        first_player_choice = get_input(
            f"{set_text_color(34, 'First player')}: choose rock, paper, or scissors: "
        )
        if first_player_choice == "stop":
            print("Game stopped.\n")
            break
        if first_player_choice in shortcut_choices:
            first_player_choice = shortcut_choices[first_player_choice]
        while first_player_choice not in choices:
            clear_previous_line()
            first_player_choice = get_input("Invalid choice. Please try again: ")
        if not playing_against_machine:
            move_cursor_up(1)
            print(
                f"{set_text_color(34, 'First player')}: choose rock, paper, or scissors: ********"
            )
        if not playing_against_machine:
            second_player_choice = get_input(
                f"{set_text_color(31, 'Second player')}: choose rock, paper, or scissors: "
            )
            if second_player_choice == "stop":
                print("Game stopped.\n")
                break
            if second_player_choice in shortcut_choices:
                second_player_choice = shortcut_choices[second_player_choice]
            while second_player_choice not in choices:
                clear_previous_line()
                second_player_choice = get_input("Invalid choice. Please try again: ")
            clear_previous_line(2)
            print(
                f"{set_text_color(34, 'First player')}: choose rock, paper, or scissors: {first_player_choice}"
            )
            print(
                f"{set_text_color(31, 'Second player')}: choose rock, paper, or scissors: {second_player_choice}"
            )
        else:
            second_player_choice = random.choice(choices)
        if playing_against_machine:
            print(f'{set_text_color(31, "Computer")} chose {second_player_choice}.')
        if first_player_choice == second_player_choice:
            print(set_text_color(33, "It's a tie!"))
            continue
        if (
            choices.index(first_player_choice) - choices.index(second_player_choice)
        ) % 3 == 1:
            scores[0] += 1
            if playing_against_machine:
                print(
                    f"{set_text_color(93, 'Scores')}: {set_text_color(94, 'Player')} {scores[0]} - {set_text_color(91, 'Computer')} {scores[1]}"
                )
                print(
                    loading_animation(
                        duration=5,
                        prefix=f"{set_text_color(94, 'You win!')} (Restarting in 5 seconds",
                        suffix=")",
                    )
                )
            else:
                print(
                    f"{set_text_color(93, 'Scores')}: {set_text_color(94, 'First player')} {scores[0]} - {set_text_color(91, 'Second player')} {scores[1]}"
                )
                print(
                    loading_animation(
                        duration=5,
                        prefix=f"{set_text_color(94, 'First player wins!')} (Restarting in 5 seconds",
                        suffix=")",
                    )
                )
        else:
            scores[1] += 1
            if playing_against_machine:
                print(
                    f"{set_text_color(93, 'Scores')}: {set_text_color(94, 'Player')} {scores[0]} - {set_text_color(91, 'Computer')} {scores[1]}"
                )
                print(
                    loading_animation(
                        duration=5,
                        prefix=f"{set_text_color(91, 'Computer wins!')} (Restarting in 5 seconds",
                        suffix=")",
                    )
                )
            else:
                print(
                    f"{set_text_color(93, 'Scores')}: {set_text_color(94, 'First player')} {scores[0]} - {set_text_color(91, 'Second player')} {scores[1]}"
                )
                print(
                    loading_animation(
                        duration=5,
                        prefix=f"{set_text_color(91, 'Second player wins!')} (Restarting in 5 seconds",
                        suffix=")",
                    )
                )
        clear_cmd()
        print("Type 'stop' to end the game at any time.\n")


if __name__ == "__main__":
    start_terminal_game()
