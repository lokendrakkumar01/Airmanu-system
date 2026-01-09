"""
Glass Card Component with Glassmorphism Effect
"""

import cv2
import numpy as np
from ui_framework.base_component import BaseComponent
from ui_framework.rendering_utils import *
from config import *


class GlassCard(BaseComponent):
    def __init__(self, x, y, width, height, title=None, border_color=None):
        super().__init__(x, y, width, height)
        self.title = title
        self.border_color = border_color or COLOR_PRIMARY
        self.content_y_offset = 40 if title else 0
    
    def render(self, frame):
        if not self.visible:
            return frame
        
        # Extract background region
        y1 = max(0, self.y)
        y2 = min(frame.shape[0], self.y + self.height)
        x1 = max(0, self.x)
        x2 = min(frame.shape[1], self.x + self.width)
        
        if y2 <= y1 or x2 <= x1:
            return frame
        
        bg_roi = frame[y1:y2, x1:x2].copy()
        
        # Create glass effect
        glass = create_glass_effect(bg_roi, GLASS_ALPHA, GLASS_BLUR_AMOUNT)
        
        # Add subtle gradient overlay
        gradient = create_gradient(
            glass.shape[1], glass.shape[0],
            (40, 40, 60), (20, 20, 40), vertical=True
        )
        glass = alpha_blend(gradient, glass, 0.3)
        
        # Place glass back
        frame[y1:y2, x1:x2] = glass
        
        # Add glow if hovered
        if self.state == "hover":
            frame = add_glow_effect(
                frame, self.x, self.y, self.width, self.height,
                self.border_color, GLOW_INTENSITY
            )
        
        # Draw border
        border_alpha = GLASS_BORDER_ALPHA if self.state != "hover" else 0.6
        border_overlay = frame.copy()
        draw_rounded_rectangle(
            border_overlay, self.x, self.y, self.width, self.height,
            15, self.border_color, 2
        )
        frame = alpha_blend(border_overlay, frame, border_alpha)
        
        # Draw title if present
        if self.title:
            title_bg = frame.copy()
            cv2.rectangle(
                title_bg,
                (self.x + CARD_PADDING, self.y + 10),
                (self.x + self.width - CARD_PADDING, self.y + 35),
                self.border_color, -1
            )
            frame = alpha_blend(title_bg, frame, 0.2)
            
            cv2.putText(
                frame, self.title,
                (self.x + CARD_PADDING + 5, self.y + 28),
                FONT_FACE, FONT_SCALE_SMALL, COLOR_TEXT,
                FONT_THICKNESS_THIN, cv2.LINE_AA
            )
        
        return frame
    
    def get_content_area(self):
        """Get the usable content area inside the card"""
        return (
            self.x + CARD_PADDING,
            self.y + CARD_PADDING + self.content_y_offset,
            self.width - 2 * CARD_PADDING,
            self.height - 2 * CARD_PADDING - self.content_y_offset
        )
