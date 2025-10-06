"""Module to manage different game states."""

class State:
    """Base class for all game states."""
    def __init__(self, manager):
        self.manager = manager

    def handle_event(self, event):
        """Handle events."""

    def update(self):
        """Update state."""

    def draw(self, screen):
        """Draw state to the screen."""




class StateManager:
    """Class to manage game states."""

    def __init__(self, current_state):
        self.current_state = current_state

    def change(self, new_state):
        """Change the current state."""
        self.current_state = new_state(self)

    def handle_event(self, events):
        """Handle events for the current state."""
        self.current_state.handle_event(events)

    def update(self, dt):
        """Update the current state."""
        self.current_state.update(dt)

    def draw(self, screen):
        """Draw the current state to the screen."""
        self.current_state.draw(screen)
        
    def update_size(self, width, height):
        """Update the size of the current state."""
        if hasattr(self.current_state, 'update_size'):
            self.current_state.update_size(width, height)
