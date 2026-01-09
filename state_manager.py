"""
State Manager - Screen State Machine
Manages transitions between different screens
"""

from enum import Enum
from animation_engine import AnimationEngine
from config import TRANSITION_DURATION


class ScreenState(Enum):
    HOME = "home"
    CATEGORY = "category"
    ITEMS = "items"
    CART = "cart"
    RECEIPT = "receipt"


class StateManager:
    def __init__(self):
        self.current_state = ScreenState.HOME
        self.previous_state = None
        self.animator = AnimationEngine()
        self.transitioning = False
        self.transition_progress = 0.0
        self.history_stack = []
        
        # Data passed between screens
        self.selected_category = None
        self.receipt_data = None
    
    def transition_to(self, new_state, data=None):
        """Initiate transition to a new state"""
        if self.current_state == new_state:
            return
        
        self.previous_state = self.current_state
        self.history_stack.append(self.current_state)
        self.current_state = new_state
        self.transitioning = True
        
        # Store any passed data
        if data:
            if 'category' in data:
                self.selected_category = data['category']
            if 'receipt' in data:
                self.receipt_data = data['receipt']
        
        # Create transition animation
        self.animator.clear_all()
        self.transition_anim = self.animator.create_animation(
            TRANSITION_DURATION, 0.0, 1.0, "ease_in_out",
            callback=self._on_transition_complete
        )
    
    def go_back(self):
        """Go back to previous screen"""
        if self.history_stack:
            prev = self.history_stack.pop()
            self.previous_state = self.current_state
            self.current_state = prev
            self.transitioning = True
            
            self.animator.clear_all()
            self.transition_anim = self.animator.create_animation(
                TRANSITION_DURATION, 0.0, 1.0, "ease_in_out",
                callback=self._on_transition_complete
            )
    
    def _on_transition_complete(self):
        """Called when transition animation completes"""
        self.transitioning = False
        self.transition_progress = 0.0
    
    def update(self):
        """Update animations"""
        self.animator.update()
        if self.transitioning:
            self.transition_progress = self.animator.get_value(self.transition_anim) or 0.0
    
    def reset(self):
        """Reset to home screen"""
        self.current_state = ScreenState.HOME
        self.previous_state = None
        self.history_stack = []
        self.selected_category = None
        self.receipt_data = None
        self.transitioning = False
        self.animator.clear_all()
