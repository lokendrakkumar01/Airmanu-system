"""
Category Screen - Menu Category Selection
"""

import cv2
from screens.base_screen import BaseScreen
from ui_framework.glass_card import GlassCard
from ui_framework.rendering_utils import *
from ui_framework.icons import draw_category_icon, draw_back_arrow
from data.menu_data import get_categories
from state_manager import ScreenState
from config import *


class CategoryScreen(BaseScreen):
    def __init__(self, state_manager, cart_manager):
        super().__init__(state_manager, cart_manager)
        self.categories = get_categories()
        self.category_cards = []
        self.back_button_rect = (20, 20, 100, 50)
        
        # Create category cards in a 2x2 grid
        card_width = 250
        card_height = 180
        spacing = 30
        start_x = (SCREEN_WIDTH - (2 * card_width + spacing)) // 2
        start_y = 150
        
        for i, category in enumerate(self.categories):
            row = i // 2
            col = i % 2
            x = start_x + col * (card_width + spacing)
            y = start_y + row * (card_height + spacing)
            
            card = GlassCard(x, y, card_width, card_height, border_color=COLOR_PRIMARY)
            card.category_data = category
            self.category_cards.append(card)
    
    def on_enter(self):
        super().on_enter()
    
    def update(self, cursor_pos, current_time):
        """Update category screen"""
        # Update card hover states
        for card in self.category_cards:
            card.update_hover_state(cursor_pos)
    
    def render(self, frame):
        """Render category screen"""
        # Background
        gradient = create_gradient(
            SCREEN_WIDTH, SCREEN_HEIGHT,
            (30, 20, 20), (10, 10, 20), vertical=True
        )
        frame = alpha_blend(gradient, frame, 0.6)
        
        # Header
        cv2.putText(
            frame, "Select Category",
            (SCREEN_WIDTH // 2 - 150, 80),
            FONT_FACE, FONT_SCALE_LARGE, COLOR_TEXT,
            FONT_THICKNESS, cv2.LINE_AA
        )
        
        # Render category cards
        for card in self.category_cards:
            frame = card.render(frame)
            
            # Render category icon and text
            content_x, content_y, content_w, content_h = card.get_content_area()
            
            # Icon
            icon_size = 60
            icon_x = card.x + (card.width - icon_size) // 2
            icon_y = content_y + 10
            draw_category_icon(
                frame, icon_x, icon_y, icon_size,
                COLOR_PRIMARY, card.category_data['icon']
            )
            
            # Category name
            name_y = icon_y + icon_size + 30
            draw_text_centered(
                frame, card.category_data['name'],
                card.x, name_y - 20, card.width, 40,
                COLOR_TEXT, FONT_FACE, FONT_SCALE_MEDIUM, FONT_THICKNESS_THIN
            )
        
        # Back button
        bx, by, bw, bh = self.back_button_rect
        back_overlay = frame.copy()
        draw_rounded_rectangle(back_overlay, bx, by, bw, bh, 10, COLOR_SECONDARY, 2)
        frame = alpha_blend(back_overlay, frame, 0.6)
        draw_back_arrow(frame, bx + 35, by + 10, 30, COLOR_SECONDARY)
        
        return frame
    
    def handle_pinch(self, cursor_pos, current_time):
        """Handle pinch gesture"""
        # Check back button
        bx, by, bw, bh = self.back_button_rect
        if bx <= cursor_pos[0] <= bx + bw and by <= cursor_pos[1] <= by + bh:
            self.state_manager.go_back()
            return
        
        # Check category cards
        for card in self.category_cards:
            if card.is_point_inside(*cursor_pos):
                self.state_manager.transition_to(
                    ScreenState.ITEMS,
                    {'category': card.category_data}
                )
                break
