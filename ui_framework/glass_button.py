"""
Glass Button Component with Hover and Dwell Interaction
"""

import cv2
import time
from ui_framework.base_component import BaseComponent
from ui_framework.rendering_utils import *
from config import *


class GlassButton(BaseComponent):
    def __init__(self, x, y, width, height, text, callback=None, color=None):
        super().__init__(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = color or COLOR_PRIMARY
        self.dwell_start_time = None
        self.dwell_progress = 0.0
    
    def update_dwell(self, is_hovering, current_time):
        """Update dwell progress for dwell-to-select"""
        if is_hovering:
            if self.dwell_start_time is None:
                self.dwell_start_time = current_time
            
            elapsed = current_time - self.dwell_start_time
            self.dwell_progress = min(elapsed / DWELL_TIME_SECONDS, 1.0)
            
            # Trigger click if dwell complete
            if self.dwell_progress >= 1.0:
                self.dwell_start_time = None
                self.dwell_progress = 0.0
                return True  # Click event
        else:
            self.dwell_start_time = None
            self.dwell_progress = 0.0
        
        return False
    
    def render(self, frame):
        if not self.visible:
            return frame
        
        # Determine button appearance based on state
        bg_alpha = 0.25
        border_thickness = 2
        glow_amount = 0.3
        
        if self.state == "hover":
            bg_alpha = 0.4
            border_thickness = 3
            glow_amount = 0.6
        elif not self.enabled:
            bg_alpha = 0.1
            self.color = COLOR_TEXT_DIM
        
        # Extract and blur background
        y1 = max(0, self.y)
        y2 = min(frame.shape[0], self.y + self.height)
        x1 = max(0, self.x)
        x2 = min(frame.shape[1], self.x + self.width)
        
        if y2 <= y1 or x2 <= x1:
            return frame
        
        bg_roi = frame[y1:y2, x1:x2].copy()
        glass = apply_gaussian_blur(bg_roi, 15)
        frame[y1:y2, x1:x2] = glass
        
        # Background fill
        bg_overlay = frame.copy()
        draw_rounded_rectangle(
            bg_overlay, self.x, self.y, self.width, self.height,
            12, self.color, -1
        )
        frame = alpha_blend(bg_overlay, frame, bg_alpha)
        
        # Add glow on hover
        if self.state == "hover":
            frame = add_glow_effect(
                frame, self.x, self.y, self.width, self.height,
                self.color, glow_amount
            )
        
        # Border
        border_overlay = frame.copy()
        draw_rounded_rectangle(
            border_overlay, self.x, self.y, self.width, self.height,
            12, self.color, border_thickness
        )
        frame = alpha_blend(border_overlay, frame, 0.8)
        
        # Dwell progress indicator
        if self.dwell_progress > 0:
            progress_width = int(self.width * self.dwell_progress)
            progress_overlay = frame.copy()
            draw_rounded_rectangle(
                progress_overlay, self.x, self.y, progress_width, self.height,
                12, COLOR_SUCCESS, -1
            )
            frame = alpha_blend(progress_overlay, frame, 0.3)
        
        # Text
        draw_text_centered(
            frame, self.text,
            self.x, self.y, self.width, self.height,
            COLOR_TEXT, FONT_FACE, FONT_SCALE_SMALL, FONT_THICKNESS_THIN
        )
        
        return frame
    
    def handle_click(self):
        """Execute callback when clicked"""
        if self.enabled and self.callback:
            self.callback()
