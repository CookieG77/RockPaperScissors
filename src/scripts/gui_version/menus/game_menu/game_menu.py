"""Module for the game menu GUI."""

from typing import Callable, Optional

import pygame
import random

from src.scripts.gui_version.game_state_manager.game_state_manager import \
    StateManager
from src.scripts.gui_version.gpu_graphics.gpu_graphics import GPUBackground
from src.scripts.gui_version.gui_utils.gui_utils import (
    PyGameMenu, render_surface_fullscreen)


class GameMenu(PyGameMenu):
    """Class to handle the game menu."""

    def __init__(
        self,
        manager: StateManager,
        screen: pygame.Surface,
        bg: GPUBackground,
        is_against_machine : bool = True ,
        back_factory: Optional[Callable] = None
        ):
        """Initialize the main game menu."""
        super().__init__(manager, screen, bg)

        # Set up background
        self.bg = bg

        # Set the game mode
        self.is_against_machine = is_against_machine

        # Menu options. The back target is provided by the caller via back_factory.
        self.back_target = back_factory if back_factory is not None else None
        # Pause menu options
        self.pause_menu_buttons = [
            ("Resume", None),
            ("Restart", lambda mgr: GameMenu(mgr, screen, self.bg, self.is_against_machine, self.back_target)),
            ("Quit to Main Menu", self.back_target),
        ]
        self.is_paused = False
        self.pause_menu_selected_index = 0

        # Game player 1 options
        self.player1_menu_buttons = [
            ("Rock", "rock"),
            ("Paper", "paper"),
            ("Scissors", "scissors"),
        ]
        self.player1_menu_index = 0
        self.player1_menu_choice = None

        # Game player 2 options
        self.player2_menu_buttons = [
            ("Rock", "rock"),
            ("Paper", "paper"),
            ("Scissors", "scissors"),
        ]
        self.player2_menu_index = 0
        self.player2_menu_choice = None

        self.game_stage = 0 # 0: ongoing, 1: player1 chosed, 2: player2 chosed, 3: in animation, 4: game over

        self.player_hands = [
            {
                "rock": pygame.image.load("assets/images/rock_hand.png").convert_alpha(),
                "paper": pygame.image.load("assets/images/paper_hand.png").convert_alpha(),
                "scissors": pygame.image.load("assets/images/scissors_hand.png").convert_alpha()
            }, {
                "rock": pygame.image.load("assets/images/rock_hand_flipped.png").convert_alpha(),
                "paper": pygame.image.load("assets/images/paper_hand_flipped.png").convert_alpha(),
                "scissors": pygame.image.load("assets/images/scissors_hand_flipped.png").convert_alpha()
            }
        ]
        self.animate_hand_idle = True
        self.hands_height = screen.get_height() // 2

    def handle_event(self, event):
        """Handle events specific to the game menu."""

        for e in event:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    # Toggle pause menu
                    self.is_paused = not self.is_paused
                    print("Pause toggled:", self.is_paused)
                if self.is_paused:
                    # Handle pause menu input
                    if e.key == pygame.K_UP or e.key == pygame.K_z:
                        self.pause_menu_selected_index = (self.pause_menu_selected_index - 1) % len(self.pause_menu_buttons)
                    elif e.key == pygame.K_DOWN or e.key == pygame.K_s or e.key == pygame.K_TAB:
                        self.pause_menu_selected_index = (self.pause_menu_selected_index + 1) % len(self.pause_menu_buttons)
                    elif e.key == pygame.K_RETURN or e.key == pygame.K_SPACE:
                        _, target = self.pause_menu_buttons[self.pause_menu_selected_index]
                        if target:
                            # target is expected to be a factory that creates a new state
                            self.manager.change(target)
                        else: # If no target is passed, resume the game
                            self.is_paused = False
                else:
                    # No event handling when game is paused or in animation
                    if self.game_stage <= 1: # If the game is not in animation or over
                        # Handle game input
                        if self.game_stage == 0 and self.player1_menu_choice is None:
                            # Player 1 turn
                            if e.key == pygame.K_LEFT or e.key == pygame.K_q:
                                self.player1_menu_index = (self.player1_menu_index - 1) % len(self.player1_menu_buttons)
                            elif e.key == pygame.K_RIGHT or e.key == pygame.K_d or e.key == pygame.K_TAB:
                                self.player1_menu_index = (self.player1_menu_index + 1) % len(self.player1_menu_buttons)
                            elif e.key == pygame.K_RETURN or e.key == pygame.K_SPACE:
                                _, choice = self.player1_menu_buttons[self.player1_menu_index]
                                self.player1_menu_choice = choice
                                print("Player 1 chose:", choice)
                                self.game_stage = 1
                                if self.is_against_machine:
                                    self.player2_menu_choice = random.choice([btn[1] for btn in self.player2_menu_buttons])
                                    print("Machine chose:", self.player2_menu_choice)
                                    self.game_stage = 2
                        elif self.game_stage == 1 and self.player2_menu_choice is None and not self.is_against_machine:
                            # Player 2 turn (if not against machine)
                            if e.key == pygame.K_LEFT or e.key == pygame.K_q:
                                self.player2_menu_index = (self.player2_menu_index - 1) % len(self.player2_menu_buttons)
                            elif e.key == pygame.K_RIGHT or e.key == pygame.K_d or e.key == pygame.K_TAB:
                                self.player2_menu_index = (self.player2_menu_index + 1) % len(self.player2_menu_buttons)
                            elif e.key == pygame.K_RETURN or e.key == pygame.K_SPACE:
                                _, choice = self.player2_menu_buttons[self.player2_menu_index]
                                self.player2_menu_choice = choice
                                print("Player 2 chose:", choice)
                                self.game_stage = 2
                    elif self.game_stage == 3:
                        # Game is over, wait for any key to restart
                        if e.key == pygame.K_RETURN or e.key == pygame.K_SPACE:
                            # Redirect to a new game menu instance
                            self.manager.change(lambda mgr: GameMenu(mgr, self.screen, self.bg, self.is_against_machine, self.back_target))

    def update(self, dt):
        """Update the game menu state."""
        super().update(dt)

        # Handle the animation and then set the game to over
        if self.game_stage == 2:
            self.animate_hand_idle = False # Stop idle animation to play the hand animation
            #TODO : Add animation here
            self.game_stage = 4
            print("Animation stage skipped")



    def draw(self, screen: pygame.Surface):
        """Draw the game menu."""
        # Render GL background first
        self.bg.render()

        # Create a transparent surface for the UI
        ui_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        font = pygame.font.SysFont("Arial", 40)
        player_choice_font = pygame.font.SysFont("Arial", 25)

        # Render the player hands (static for now)
        


        # Render the player choices depending on the game state
        if self.player1_menu_choice is None:
            text = font.render("Player 1: Choose your move", True, (255, 255, 255))
            ui_surface.blit(text, (50, 50))
            for i, (label, _) in enumerate(self.player1_menu_buttons):
                color = (255, 255, 0) if i == self.player1_menu_index else (200, 200, 200)
                # Rendered in bottom left corner
                rect = pygame.Rect(15 + i * 100, screen.get_height() - 70, 90, 50)
                pygame.draw.rect(ui_surface, (0, 0, 0, 150), rect)
                text = player_choice_font.render(label, True, color)
                ui_surface.blit(text, (20 + i * 100, screen.get_height() - 65))
        elif self.player2_menu_choice is None and not self.is_against_machine:
            text = font.render("Player 2: Choose your move", True, (255, 255, 255))
            ui_surface.blit(text, (50, 50))
            for i, (label, _) in enumerate(self.player2_menu_buttons):
                color = (255, 255, 0) if i == self.player2_menu_index else (200, 200, 200)
                # Rendered in bottom right corner
                rect = pygame.Rect(screen.get_width() - 15 - (len(self.player2_menu_buttons) - i) * 100, screen.get_height() - 70, 90, 50)
                pygame.draw.rect(ui_surface, (0, 0, 0, 150), rect)
                text = player_choice_font.render(label, True, color)
                ui_surface.blit(text, (screen.get_width() - 10 - (len(self.player2_menu_buttons) - i) * 100, screen.get_height() - 65))
        else:
            # Both players have chosen; display the result
            winner = self.get_winner()
            if winner == 0:
                result_text = "It's a Tie!"
            elif winner == 1:
                result_text = "Player 1 Wins!"
            else:
                result_text = "Player 2 Wins!" if not self.is_against_machine else "Machine Wins!"
            text = font.render(result_text, True, (255, 255, 255))
            ui_surface.blit(text, (50, 50))

            p1_text = font.render(f"Player 1 chose: {self.player1_menu_choice}", True, (255, 255, 255))
            ui_surface.blit(p1_text, (50, 150))

            p2_text = font.render(f"Player 2 chose: {self.player2_menu_choice}" if not self.is_against_machine else f"Machine chose: {self.player2_menu_choice}", True, (255, 255, 255))
            ui_surface.blit(p2_text, (50, 250))

        if self.is_paused:
            # Draw pause menu
            text = font.render("Game Paused", True, (255, 255, 255))
            ui_surface.blit(text, (50, 50))
            for i, (label, _) in enumerate(self.pause_menu_buttons):
                color = (255, 255, 0) if i == self.pause_menu_selected_index else (200, 200, 200)
                rect = pygame.Rect(50, 150 + i * 60, 300, 50)
                pygame.draw.rect(ui_surface, (0, 0, 0, 150), rect)
                text = font.render(label, True, color)
                ui_surface.blit(text, (60, 160 + i * 60))

        # Render the UI surface to the screen
        render_surface_fullscreen(ui_surface)
        
    def get_winner(self) -> int:
        """
        Determine the winner of the game.
        
        Returns:
            0 if it's a tie,
            1 if player 1 wins,
            2 if player 2 wins,
            -1 if the game is not yet decided.
        """

        if self.player1_menu_choice is None or self.player2_menu_choice is None:
            return -1  # Game not yet decided

        if self.player1_menu_choice == self.player2_menu_choice:
            return 0  # Tie

        winning_combinations = {
            "rock": "scissors",
            "scissors": "paper",
            "paper": "rock"
        }

        if winning_combinations[self.player1_menu_choice] == self.player2_menu_choice:
            return 1  # Player 1 wins
        return 2  # Player 2 wins
