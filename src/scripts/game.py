"""Module for the Rock-Paper-Scissors terminal game logic."""

import random
import os

choices = ['rock', 'paper', 'scissors']

# Get the absolute path to the welcome.txt file
script_dir = os.path.dirname(os.path.abspath(__file__))
welcome_file_path = os.path.join(script_dir, '..', 'assets', 'text', 'welcome.txt')
def start_terminal_game():
    """
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
    # Read and display the welcome message
    try:
        with open(welcome_file_path, 'r', encoding='utf-8') as f:
            print(f.read())
    except:
        print("Welcome to Rock-Paper-Scissors!")  # Fallback message
    
    while True:
        computer_choice = random.choice(choices)
        player_choice = input('Choose rock, paper, or scissors:').lower().strip()
        if player_choice == 'stop':
            print('Game stopped.\n')
            break
        if player_choice not in choices:
            player_choice = input('Invalid choice. Please try again.').lower().strip()
            continue
        print(f'Computer chose {computer_choice}.')
        if player_choice == computer_choice:
            print('It\'s a tie!')
        elif (player_choice == 'rock' and computer_choice == 'scissors') or (player_choice == 'paper' and computer_choice == 'rock') or (player_choice == 'scissors' and computer_choice == 'paper'):
            print('You win!')
        else:
            print('Computer wins!')
