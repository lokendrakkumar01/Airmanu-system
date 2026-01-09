"""
Base Screen Class
All screens inherit from this
"""


class BaseScreen:
    def __init__(self, state_manager, cart_manager):
        self.state_manager = state_manager
        self.cart_manager = cart_manager
        self.components = []
        self.active = False
    
    def on_enter(self):
        """Called when screen becomes active"""
        self.active = True
    
    def on_exit(self):
        """Called when leaving this screen"""
        self.active = False
    
    def update(self, cursor_pos, current_time):
        """Update screen logic and interactions"""
        pass
    
    def render(self, frame):
        """Render screen to frame"""
        pass
    
    def handle_pinch(self, cursor_pos, current_time):
        """Handle pinch gesture"""
        pass
