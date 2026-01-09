"""
Home Screen - Welcome Screen
"""

import cv2
from screens.base_screen import BaseScreen
from ui_framework.glass_button import GlassButton
from ui_framework.rendering_utils import *
from ui_framework.icons import draw_home_icon
from state_manager import ScreenState
from config import *


class HomeScreen(BaseScreen):
    def __init__(self, state_manager, cart_manager):
        super().__init__(state_manager, cart_manager)
        
        # Start button
        btn_width = 300
        btn_height = BUTTON_HEIGHT
        btn_x = (SCREEN_WIDTH - btn_width) // 2
        btn_y = SCREEN_HEIGHT // 2 + 50
        
        self.start_button = GlassButton(
            btn_x, btn_y, btn_width, btn_height,
            "START ORDERING",
            callback=self.on_start_click,
            color=COLOR_PRIMARY
        )
        
        self.components = [self.start_button]
    
    def on_start_click(self):
        """Navigate to category screen"""
        self.state_manager.transition_to(ScreenState.CATEGORY)
    
    def on_enter(self):
        super().on_enter()
    
    def update(self, cursor_pos, current_time):
        """Update home screen"""
        # Update button hover state
        self.start_button.update_hover_state(cursor_pos)
        
        # Check for dwell click
        is_hovering = self.start_button.state == "hover"
        if self.start_button.update_dwell(is_hovering, current_time):
            self.on_start_click()
    
    def render(self, frame):
        """Render home screen"""
        # Background gradient
        gradient = create_gradient(
            SCREEN_WIDTH, SCREEN_HEIGHT,
            (40, 25, 15), (15, 10, 25), vertical=True
        )
        frame = alpha_blend(gradient, frame, 0.7)
        
        # Title with glow
        title = "AirMenu"
        title_y = SCREEN_HEIGHT // 2 - 100
        
        # Glow effect for title
        glow_layer = np.zeros_like(frame)
        cv2.putText(
            glow_layer, title,
            (SCREEN_WIDTH // 2 - 200, title_y),
            FONT_FACE, 2.5, COLOR_PRIMARY,
            8, cv2.LINE_AA
        )
        glow_layer = cv2.GaussianBlur(glow_layer, (25, 25), 0)
        frame = alpha_blend(glow_layer, frame, 0.8)
        
        # Main title
        cv2.putText(
            frame, title,
            (SCREEN_WIDTH // 2 - 200, title_y),
            FONT_FACE, 2.5, COLOR_TEXT,
            3, cv2.LINE_AA
        )
        
        # Subtitle
        subtitle = "Touchless AR Restaurant Menu"
        cv2.putText(
            frame, subtitle,
            (SCREEN_WIDTH // 2 - 280, title_y + 60),
            FONT_FACE, FONT_SCALE_MEDIUM, COLOR_TEXT_DIM,
            FONT_THICKNESS_THIN, cv2.LINE_AA
        )
        
        # Instructions
        instruction = "Hover and hold to select"
        cv2.putText(
            frame, instruction,
            (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 150),
            FONT_FACE, FONT_SCALE_SMALL, COLOR_TEXT_DIM,
            FONT_THICKNESS_THIN, cv2.LINE_AA
        )
        
        # Render button
        frame = self.start_button.render(frame)
        
        return frame
    
    def handle_pinch(self, cursor_pos, current_time):
        """Handle pinch gesture on home screen"""
        if self.start_button.is_point_inside(*cursor_pos):
            self.on_start_click()
