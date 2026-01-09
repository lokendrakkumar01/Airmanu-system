"""
Base Component Class for UI Framework
All UI elements inherit from this
"""

from config import *


class BaseComponent:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True
        self.enabled = True
        self.state = "normal"  # normal, hover, active, disabled
    
    def is_point_inside(self, px, py):
        """Check if a point is inside this component"""
        if not self.visible or not self.enabled:
            return False
        return (self.x <= px <= self.x + self.width and 
                self.y <= py <= self.y + self.height)
    
    def update_hover_state(self, cursor_pos):
        """Update hover state based on cursor position"""
        if cursor_pos and self.is_point_inside(*cursor_pos):
            self.state = "hover"
            return True
        else:
            if self.state == "hover":
                self.state = "normal"
            return False
    
    def render(self, frame):
        """Override this method in subclasses"""
        raise NotImplementedError("Subclasses must implement render()")
    
    def handle_click(self):
        """Override this method in subclasses for click handling"""
        pass
