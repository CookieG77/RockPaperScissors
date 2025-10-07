# 🪨 RockPaperScissors ✂️

A classic **Rock, Paper, Scissors** game built in Python — playable either right in your **terminal** or through a stylised **Pygame UI**.  

Challenge the **computer** or a **friend**, test your reflexes, and enjoy a nostalgic twist on the age-old hand game.


## 🎯 Overview

RockPaperScissors lets players enjoy a simple yet fun match of chance and quick decisions.  
It’s designed to be lightweight and easy to run — whether you’re coding along in the terminal or relaxing with a visual interface.

### 🎮 Game Modes
- **Player vs Computer** — take on an AI opponent that plays randomly
- **Player vs Player** — compete locally with a friend on the same machine  


## ⚙️ Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/CookieG77/RockPaperScissors.git
cd RockPaperScissors
pip install PyOpenGL PyOpenGL_accelerate pygame
````

## 🚀 Usage

You can lauch the game by _**TODO**_

After the launch of the game, you can choose to play the game either **directly in the terminal**, or **launch it in a pygame/OpenGL UI** when prompted by typing "**terminal**" (or "**t**") or "**gui**" (or "**g**").

You can stop the game at any moment in the terminal by typing "**stop**".

## 📁 Project Structure

```python
RockPaperScissors/
├── LISCENCE
├── main.py
├── README.md
└── src/
    ├── assets/
    │   ├── images/
    │   │   ├── blue_hands/
    │   │   └── red_hands/
    │   ├── shaders/
    │   └── test/
    └── scripts/
        ├── game_booter/
        ├── gui_version/
        │   ├── game_state_manager/
        │   ├── gpu_graphics/
        │   ├── gui_game/
        │   ├── gui_utils/
        │   └── menus/
        │       ├── chose_gamemode_menu/
        │       └── main_menu/
        └── terminal_vesion/
            ├── terminal_game/
            └── terminal_utils/
```

## 📜 License

This project is licensed under the
**Creative Commons Attribution-NonCommercial 4.0 International License**.

You are free to use and modify it for **non-commercial purposes** with proper attribution.

## 🙌 Credits

Developed by **CLÉMENT Timothé** and **CORDONNIER MAXIME**.
Special thanks to **localthunk** for the shader **(https://www.playbalatro.com)**.

Enjoy the game and have fun throwing your virtual hands! ✊ 🖐️ ✌️