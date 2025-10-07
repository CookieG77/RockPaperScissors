"""Module for the game menu GUI."""

from typing import Callable, Optional
import random
import math
import pathlib
import pygame
from src.scripts.gui_version.game_state_manager.game_state_manager import \
    StateManager
from src.scripts.gui_version.gpu_graphics.gpu_graphics import GPUBackground
from src.scripts.gui_version.gui_utils.gui_utils import (
    PyGameMenu, render_surface_fullscreen)


class GameMenu(PyGameMenu):
    """Class to handle the game menu."""

    # Class-level cache to avoid loading images multiple times
    _player_hands_cache = None

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

        # Load player hand images with caching to avoid multiple loads
        if GameMenu._player_hands_cache is None:
            repo_root = pathlib.Path(__file__).resolve().parents[4]
            assets_folder = repo_root / 'assets' / 'images'
            player_hands = [
                {
                    "rock": pygame.image.load(assets_folder / "blue_hands" / "blue_rock.png").convert_alpha(),
                    "paper": pygame.image.load(assets_folder / "blue_hands" / "blue_paper.png").convert_alpha(),
                    "scissors": pygame.image.load(assets_folder / "blue_hands" / "blue_scissors.png").convert_alpha()
                }, {
                    "rock": pygame.image.load(assets_folder / "red_hands" / "red_rock.png").convert_alpha(),
                    "paper": pygame.image.load(assets_folder / "red_hands" / "red_paper.png").convert_alpha(),
                    "scissors": pygame.image.load(assets_folder / "red_hands" / "red_scissors.png").convert_alpha()
                }
            ]
            # Resize hands once and store in cache
            for hand_set in player_hands:
                for key in list(hand_set.keys()):
                    surf = hand_set[key]
                    scaled = pygame.transform.scale(surf, (surf.get_width() // 2.5, surf.get_height() // 2.5))
                    hand_set[key] = scaled
            GameMenu._player_hands_cache = player_hands

        # Reuse cached hands (copy references — surfaces are immutable enough for blitting)
        self.player_hands = GameMenu._player_hands_cache
        
        self.animate_hand_idle = True
        self.hands_height = screen.get_height() // 2
        # Animation timing
        self.animation_start_time = None
        self.animation_stage = 0 # 0: hands move to center, 1: move up down 3 times, 2 reveal choices, 3: over

    def _blit_rotate(self, surface: pygame.Surface, image: pygame.Surface, topleft: tuple[int, int], pivot: tuple[int, int], angle: float):
        """Blit `image` on `surface` rotated by `angle` degrees around `pivot`.

        - `topleft` is the world position where the unrotated image's topleft would be.
        - `pivot` is the pivot point relative to the image topleft (x,y).
        - `angle` is in degrees (counter-clockwise).
        """
        # world position of pivot
        pivot_world = pygame.math.Vector2(topleft) + pygame.math.Vector2(pivot)

        # original image center in world coords
        orig_rect = image.get_rect(topleft=topleft)
        orig_center = pygame.math.Vector2(orig_rect.center)

        # vector from pivot to center, rotate it, compute new center
        pivot_to_center = orig_center - pivot_world
        rotated_pivot_to_center = pivot_to_center.rotate(angle)
        new_center = pivot_world + rotated_pivot_to_center

        # rotate the image and blit with new center
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rect = rotated_image.get_rect(center=(int(new_center.x), int(new_center.y)))
        surface.blit(rotated_image, rotated_rect.topleft)

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
                    elif self.game_stage == 4 and self.get_winner() > 0:
                        # Game is over, wait for any key to restart
                        if e.key == pygame.K_RETURN or e.key == pygame.K_SPACE:
                            # Redirect to a new game menu instance
                            self.manager.change(lambda mgr: GameMenu(mgr, self.screen, self.bg, self.is_against_machine, self.back_target))

    def update(self, dt):
        """Update the game menu state."""
        super().update(dt)

        # Handle the animation and then set the game to over
        if self.game_stage == 2:
            # Stop idle animation and start the animation stage
            self.animate_hand_idle = False
            if self.animation_start_time is None:
                self.animation_start_time = pygame.time.get_ticks()
            # switch to animation stage
            self.game_stage = 3
        elif self.game_stage == 4 and self.get_winner() == 0:
            #If a tie happend wait for 2 seconds and restart the game
            
            # Use the animation timer to wait 2 seconds
            if self.animation_start_time is None:
                self.animation_start_time = pygame.time.get_ticks()
            elapsed = pygame.time.get_ticks() - self.animation_start_time
            if elapsed >= 5000:
                # Restart the game
                self.game_stage = 0
                self.player1_menu_choice = None
                self.player2_menu_choice = None
                self.player1_menu_index = 0
                self.player2_menu_index = 0
                self.animate_hand_idle = True
                self.animation_start_time = None
                self.animation_stage = 0

    def draw(self, screen: pygame.Surface):
        """Draw the game menu."""
        # Render GL background first
        self.bg.render()

        # Create a transparent surface for the UI
        ui_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        font = pygame.font.SysFont("Arial", 40)
        player_choice_font = pygame.font.SysFont("Arial", 25)

        # Render the player hands (static for now)
        if self.animate_hand_idle:
            player1_hand_pos = (-45, self.hands_height - self.player_hands[0]["rock"].get_height() // 2)
            player2_hand_pos = (45 + screen.get_width() - self.player_hands[1]["rock"].get_width(), self.hands_height - self.player_hands[1]["rock"].get_height() // 2)
            # small vertical bobbing
            player1_hand_pos_offset = 5 * math.cos(pygame.time.get_ticks() / 200)
            player2_hand_pos_offset = 5 * math.cos(pygame.time.get_ticks() / 200 + 1.62)

            # rotation angles
            t = pygame.time.get_ticks()
            angle_amp = 5.0 # degrees amplitude
            angle1 = angle_amp * math.sin(t / 400)
            angle2 = angle_amp * math.sin(t / 400 + 1.62)

            # image surfaces
            img1 = self.player_hands[0]["rock"]
            img2 = self.player_hands[1]["rock"]

            # compute topleft positions (with bobbing)
            topleft1 = (int(player1_hand_pos[0]), int(player1_hand_pos[1] + player1_hand_pos_offset))
            topleft2 = (int(player2_hand_pos[0]), int(player2_hand_pos[1] + player2_hand_pos_offset))

            # pivot relative to image topleft: center-left for player1, center-right for player2
            pivot1 = (img1.get_width(), img1.get_height() // 2)
            pivot2 = (0, img2.get_height() // 2)

            # blit rotated images around the requested pivots
            self._blit_rotate(ui_surface, img1, topleft1, pivot1, angle1)
            self._blit_rotate(ui_surface, img2, topleft2, pivot2, angle2)


        # Render the player choices depending on the game state
        if self.player1_menu_choice is None:
            text = font.render("Player 1: Choose your move", True, (255, 255, 255))
            ui_surface.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 30))
            for i, (label, _) in enumerate(self.player1_menu_buttons):
                color = (255, 255, 0) if i == self.player1_menu_index else (200, 200, 200)
                # Rendered in bottom left corner
                rect = pygame.Rect(15 + i * 100, screen.get_height() - 70, 90, 50)
                pygame.draw.rect(ui_surface, (0, 0, 0, 150), rect)
                text = player_choice_font.render(label, True, color)
                ui_surface.blit(text, (20 + i * 100, screen.get_height() - 65))
        elif self.player2_menu_choice is None and not self.is_against_machine:
            text = font.render("Player 2: Choose your move", True, (255, 255, 255))
            ui_surface.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 30))
            for i, (label, _) in enumerate(self.player2_menu_buttons):
                color = (255, 255, 0) if i == self.player2_menu_index else (200, 200, 200)
                # Rendered in bottom right corner
                rect = pygame.Rect(screen.get_width() - 15 - (len(self.player2_menu_buttons) - i) * 100, screen.get_height() - 70, 90, 50)
                pygame.draw.rect(ui_surface, (0, 0, 0, 150), rect)
                text = player_choice_font.render(label, True, color)
                ui_surface.blit(text, (screen.get_width() - 10 - (len(self.player2_menu_buttons) - i) * 100, screen.get_height() - 65))
        elif self.game_stage == 3:
            if self.animation_stage == 0:
                # Move hands closer to center
                elapsed = pygame.time.get_ticks() - self.animation_start_time
                duration = 1000  # ms
                if elapsed >= duration:
                    elapsed = duration
                    self.animation_stage = 1
                    self.animation_start_time = pygame.time.get_ticks()
                progress = elapsed / duration
                # Interpolate hand positions
                player1_hand_pos = (-30 * -progress - 15 + (screen.get_width() // 2 - self.player_hands[0]["rock"].get_width() - 50 + 15),
                                    self.hands_height - self.player_hands[0]["rock"].get_height() // 2)
                player2_hand_pos = (30 * -progress + 15 + screen.get_width() - self.player_hands[1]["rock"].get_width() - (screen.get_width() // 2 - self.player_hands[1]["rock"].get_width() - 50 + 15),
                                    self.hands_height - self.player_hands[1]["rock"].get_height() // 2)
                # No rotation during this phase
                img1 = self.player_hands[0]["rock"]
                img2 = self.player_hands[1]["rock"]
                topleft1 = (int(player1_hand_pos[0]), int(player1_hand_pos[1]))
                topleft2 = (int(player2_hand_pos[0]), int(player2_hand_pos[1]))
                pivot1 = (img1.get_width(), img1.get_height() // 2)
                pivot2 = (0, img2.get_height() // 2)
                self._blit_rotate(ui_surface, img1, topleft1, pivot1, 0)
                self._blit_rotate(ui_surface, img2, topleft2, pivot2, 0)
            elif self.animation_stage == 1:
                # Rotate hands up and down 3 times
                elapsed = pygame.time.get_ticks() - self.animation_start_time
                duration = 3000  # ms
                if elapsed >= duration:
                    elapsed = duration
                    self.animation_stage = 2
                    self.animation_start_time = pygame.time.get_ticks()
                progress = elapsed / duration
                # Compute hand positions
                player1_hand_pos = (-15 + (screen.get_width() // 2 - self.player_hands[0]["rock"].get_width() - 50 + 15),
                                    self.hands_height - self.player_hands[0]["rock"].get_height() // 2)
                player2_hand_pos = (15 + screen.get_width() - self.player_hands[1]["rock"].get_width() - (screen.get_width() // 2 - self.player_hands[1]["rock"].get_width() - 50 + 15),
                                    self.hands_height - self.player_hands[1]["rock"].get_height() // 2)
                # Rotation angles (2 and a half full up-down cycles)
                angle1 = 30 * math.sin(progress * 5 * math.pi)  # 2.5 cycles
                angle2 = 30 * math.sin(progress * 5 * math.pi + math.pi + 0.1)  # 2.5 cycles, phase shifted
                # image surfaces
                img1 = self.player_hands[0]["rock"]
                img2 = self.player_hands[1]["rock"]
                topleft1 = (int(player1_hand_pos[0]), int(player1_hand_pos[1]))
                topleft2 = (int(player2_hand_pos[0]), int(player2_hand_pos[1]))
                pivot1 = (img1.get_width(), img1.get_height() // 2)
                pivot2 = (0, img2.get_height() // 2)
                self._blit_rotate(ui_surface, img1, topleft1, pivot1, angle1)
                self._blit_rotate(ui_surface, img2, topleft2, pivot2, angle2)
            elif self.animation_stage == 2:
                # Reveal choices
                elapsed = pygame.time.get_ticks() - self.animation_start_time
                duration = 1000  # ms
                if elapsed >= duration:
                    elapsed = duration
                    self.animation_stage = 3
                    self.game_stage = 4  # Game over
                progress = elapsed / duration
                # Compute hand positions
                player1_hand_pos = ((screen.get_width() // 2 - self.player_hands[0]["rock"].get_width() - 50 + 15),
                                    self.hands_height - self.player_hands[0]["rock"].get_height() // 2)
                player2_hand_pos = (screen.get_width() - self.player_hands[1]["rock"].get_width() - (screen.get_width() // 2 - self.player_hands[1]["rock"].get_width() - 50 + 15),
                                    self.hands_height - self.player_hands[1]["rock"].get_height() // 2)
                # No rotation during this phase
                img1 = self.player_hands[0][self.player1_menu_choice]
                img2 = self.player_hands[1][self.player2_menu_choice]
                topleft1 = (int(player1_hand_pos[0]), int(player1_hand_pos[1]))
                topleft2 = (int(player2_hand_pos[0]), int(player2_hand_pos[1]))
                pivot1 = (img1.get_width(), img1.get_height() // 2)
                pivot2 = (0, img2.get_height() // 2)
                self._blit_rotate(ui_surface, img1, topleft1, pivot1, 0)
                self._blit_rotate(ui_surface, img2, topleft2, pivot2, 0)
                
        else:
            # Both players have chosen; display the result
            
            #Display the hands in the background
            # Compute hand positions
            player1_hand_pos = ((screen.get_width() // 2 - self.player_hands[0]["rock"].get_width() - 50 + 15),
                                self.hands_height - self.player_hands[0]["rock"].get_height() // 2)
            player2_hand_pos = (screen.get_width() - self.player_hands[1]["rock"].get_width() - (screen.get_width() // 2 - self.player_hands[1]["rock"].get_width() - 50 + 15),
                                self.hands_height - self.player_hands[1]["rock"].get_height() // 2)
            # No rotation during this phase
            img1 = self.player_hands[0][self.player1_menu_choice]
            img2 = self.player_hands[1][self.player2_menu_choice]
            topleft1 = (int(player1_hand_pos[0]), int(player1_hand_pos[1]))
            topleft2 = (int(player2_hand_pos[0]), int(player2_hand_pos[1]))
            pivot1 = (img1.get_width(), img1.get_height() // 2)
            pivot2 = (0, img2.get_height() // 2)
            self._blit_rotate(ui_surface, img1, topleft1, pivot1, 0)
            self._blit_rotate(ui_surface, img2, topleft2, pivot2, 0)
            
            # Display the result text
            winner = self.get_winner()
            if winner == 0:
                result_text = "It's a Tie!"
            elif winner == 1:
                result_text = "Player Blue Wins!"
            else:
                result_text = "Player Red Wins!" if not self.is_against_machine else "Machine Wins!"
            text = font.render(result_text, True, (255, 255, 255))
            ui_surface.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 30))

            p1_text = font.render(f"Player Blue chose: {self.player1_menu_choice}", True, (255, 255, 255))
            ui_surface.blit(p1_text, (screen.get_width() // 2 - p1_text.get_width() // 2, 150))

            p2_text = font.render(f"Player Red chose: {self.player2_menu_choice}" if not self.is_against_machine else f"Machine chose: {self.player2_menu_choice}", True, (255, 255, 255))
            ui_surface.blit(p2_text, (screen.get_width() // 2 - p2_text.get_width() // 2, 250))
            
            if winner != 0:
                restart_text = player_choice_font.render("Press Enter or Space to play again", True, (255, 128, 0))
                ui_surface.blit(restart_text, (screen.get_width() // 2 - restart_text.get_width() // 2, screen.get_height() - restart_text.get_height() - 20))
            else:
                tie_text = player_choice_font.render("It's a tie! Restarting in 5 seconds...", True, (255, 128, 0))
                ui_surface.blit(tie_text, (screen.get_width() // 2 - tie_text.get_width() // 2, screen.get_height() - tie_text.get_height() - 20))

        if self.is_paused:
            # Draw pause menu
            text = font.render("Game Paused", True, (255, 255, 255))
            ui_surface.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 30))
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
