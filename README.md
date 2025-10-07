# 🪨 RockPaperScissors ✂️

A classic **Rock, Paper, Scissors** game built in Python — playable either right in your **terminal** or through a stylised **Pygame UI**.  

Challenge the **computer** or a **friend**, test your reflexes, and enjoy a nostalgic twist on the age-old hand game.


## 🎯 Overview

RockPaperScissors lets players enjoy a simple yet fun match of chance and quick decisions.  
It’s designed to be lightweight and easy to run — whether you’re coding along in the terminal or relaxing with a visual interface.

### 🎮 Game Modes
- **Player vs Computer** — take on an AI opponent that plays randomly
- **Player vs Player** — compete locally with a friend on the same machine  

## Requirements

- Python 3.10
- OpenGL 3.3
- Windows 11 (other OS not tested)

## ⚙️ Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/CookieG77/RockPaperScissors.git
cd RockPaperScissors
pip install PyOpenGL PyOpenGL_accelerate pygame
````

## 🚀 Usage

You can lauch the game by launching "**launch.cmd**" or, from a terminal copy and paste `py main.py` from the root folder of the project.

After the launch of the game, you can choose to play the game either **directly in the terminal**, or **launch it in a pygame/OpenGL UI** when prompted by typing "**terminal**" (or "**t**") or "**gui**" (or "**g**").

In the **terminal version**, you can stop the game at any moment in the terminal by typing "**stop**".
In the **PyGame** version, you can simply close the window.
## 📁 Project Structure

```python
RockPaperScissors/
├── LICENCE                                 # Project license
├── main.py                                 # Game entry point
├── launch.cmd                              # Shortcut to launch the game
├── README.md
└── src/
    ├── assets/                             # Folder containing the various assets for the game
    │   ├── images/                         # Folder containing the image assets for the game
    │   ├── shaders/                        # Folder containing the shader assets for the game
    │   └── text/                           # Folder containing the text assets for the game
    └── scripts/                            # Folder containing the project's scripts
        ├── game_booter/                    # Folder containing the function to lauch either version of the game
        ├── gui_version/                    # Folder containing the various modules for the GUI version
        │   ├── game_state_manager/         # Folder conatining two classes allowing to change between menus
        │   ├── gpu_graphics/               # Folder conatining various functions handling the graphic display (mainly OpenGL)
        │   ├── gui_game/                   # Folder conteining the main GUI game module.
        │   ├── gui_utils/                  # Folder containing various functions for the GUI version
        │   └── menus/                      # Folder containing the various game menus
        │       ├── main_menu/              # Folder containing the main menu module
        │       ├── chose_gamemode_menu/    # Folder containing the game mode choice menu module
        │       └── game_menu/              # Folder containing the main game module
        └── terminal_vesion/                # Folder containing the various modules for the terminal version
            ├── terminal_game/              # Folder conteining the main terminal game module.
            └── terminal_utils/             # Folder containing various functions for terminal formating and styling
```

## 📜 License

This project is licensed under the
**Creative Commons Attribution-NonCommercial 4.0 International License**.

You are free to use and modify it for **non-commercial purposes** with proper attribution.

## 🙌 Credits

Developed by **CLÉMENT Timothé** and **CORDONNIER MAXIME**.
Special thanks to **localthunk** for the shader **(https://www.playbalatro.com)**.

Enjoy the game and have fun throwing your virtual hands! ✊ 🖐️ ✌️