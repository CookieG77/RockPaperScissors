"""Starts the Rock-Paper-Scissors game in terminal or GUI mode based on user input."""

from src.scripts.game_booter.game_booter import start_game
from src.scripts.bdd_scripts.dbb_utils.bdd_utils import *
import os

if __name__ == "__main__":
    #start_game()
    db = RPSDatabase()
    db.insert_user("xX_ProGamer69_Xx", "my_secure_password_123", "random_salt_value")
    db.add_victory(1)
    db.print_database_info()
