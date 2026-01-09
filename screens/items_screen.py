"""
Items Screen - Display menu items for selected category
"""

import cv2
from screens.base_screen import BaseScreen
from ui_framework.glass_card import GlassCard
from ui_framework.rendering_utils import *
from ui_framework.icons import draw_back_arrow, draw_plus_icon, draw_cart_icon
from data.menu_data import get_items_by_category
from state_manager import ScreenState
from config import *


class ItemsScreen(BaseScreen):
    def __init__(self, state_manager, cart_manager):
        super().__init__(state_manager, cart_manager)
        self.items = []
        self.item_cards = []
        self.scroll_offset = 0
        self.back_button_rect = (20, 20, 100, 50)
        self.cart_button_rect = (SCREEN_WIDTH - 200, 20, 180, 50)
    
    def on_enter(self):
        """Load items for selected category"""
        super().on_enter()
        category = self.state_manager.selected_category
        if category:
            self.items = get_items_by_category(category['id'])
            self._create_item_cards()
    
    def _create_item_cards(self):
        """Create cards for each item"""
        self.item_cards = []
        card_width = SCREEN_WIDTH - 100
        card_height = ITEM_HEIGHT
        start_x = 50
        start_y = 120
        spacing = 15
        
        for i, item in enumerate(self.items):
            y = start_y + i * (card_height + spacing)
            card = GlassCard(start_x, y, card_width, card_height, border_color=COLOR_PRIMARY)
            card.item_data = item
            
            # Add button position (on the right side of card)
            card.add_btn_rect = (
                start_x + card_width - 60,
                y + (card_height - 40) // 2,
                50, 40
            )
            
            self.item_cards.append(card)
    
    def update(self, cursor_pos, current_time):
        """Update items screen"""
        # Update card hover states
        for card in self.item_cards:
            # Adjust for scroll
            adjusted_y = cursor_pos[1] + self.scroll_offset if cursor_pos else None
            if adjusted_y:
                card.update_hover_state((cursor_pos[0], adjusted_y))
    
    def render(self, frame):
        """Render items screen"""
        # Background
        gradient = create_gradient(
            SCREEN_WIDTH, SCREEN_HEIGHT,
            (25, 20, 30), (10, 10, 20), vertical=True
        )
        frame = alpha_blend(gradient, frame, 0.6)
        
        # Header with category name
        category = self.state_manager.selected_category
        if category:
            cv2.putText(
                frame, category['name'],
                (SCREEN_WIDTH // 2 - 100, 80),
                FONT_FACE, FONT_SCALE_LARGE, COLOR_TEXT,
                FONT_THICKNESS, cv2.LINE_AA
            )
        
        # Render items (with scroll offset)
        for card in self.item_cards:
            # Check if card is visible
            if card.y - self.scroll_offset < -ITEM_HEIGHT or card.y - self.scroll_offset > SCREEN_HEIGHT:
                continue
            
            # Temporarily adjust y position for rendering
            original_y = card.y
            card.y = card.y - self.scroll_offset
            
            frame = card.render(frame)
            
            # Render item details
            content_x, content_y, content_w, content_h = card.get_content_area()
            
            # Item name
            cv2.putText(
                frame, card.item_data['name'],
                (content_x, content_y + 25),
                FONT_FACE, FONT_SCALE_MEDIUM, COLOR_TEXT,
                FONT_THICKNESS_THIN, cv2.LINE_AA
            )
            
            # Description
            cv2.putText(
                frame, card.item_data['description'],
                (content_x, content_y + 50),
                FONT_FACE, FONT_SCALE_SMALL - 0.1, COLOR_TEXT_DIM,
                FONT_THICKNESS_THIN, cv2.LINE_AA
            )
            
            # Price
            price_text = f"{CURRENCY_SYMBOL}{card.item_data['price']}"
            cv2.putText(
                frame, price_text,
                (content_x, content_y + 80),
                FONT_FACE, FONT_SCALE_MEDIUM, COLOR_ACCENT,
                FONT_THICKNESS, cv2.LINE_AA
            )
            
            # Add button
            btn_x, btn_y, btn_w, btn_h = card.add_btn_rect
            btn_y = btn_y - self.scroll_offset
            
            btn_overlay = frame.copy()
            draw_rounded_rectangle(btn_overlay, btn_x, btn_y, btn_w, btn_h, 8, COLOR_SUCCESS, -1)
            frame = alpha_blend(btn_overlay, frame, 0.7)
            
            draw_plus_icon(frame, btn_x + 10, btn_y + 5, 30, COLOR_TEXT)
            
            # Restore original y
            card.y = original_y
        
        # Back button
        bx, by, bw, bh = self.back_button_rect
        back_overlay = frame.copy()
        draw_rounded_rectangle(back_overlay, bx, by, bw, bh, 10, COLOR_SECONDARY, 2)
        frame = alpha_blend(back_overlay, frame, 0.6)
        draw_back_arrow(frame, bx + 35, by + 10, 30, COLOR_SECONDARY)
        
        # Cart button
        cx, cy, cw, ch = self.cart_button_rect
        cart_overlay = frame.copy()
        draw_rounded_rectangle(cart_overlay, cx, cy, cw, ch, 10, COLOR_PRIMARY, 2)
        frame = alpha_blend(cart_overlay, frame, 0.6)
        
        draw_cart_icon(frame, cx + 10, cy + 10, 30, COLOR_PRIMARY)
        
        # Cart count
        cart_count = self.cart_manager.get_item_count()
        count_text = f"Cart ({cart_count})"
        cv2.putText(
            frame, count_text,
            (cx + 50, cy + 35),
            FONT_FACE, FONT_SCALE_SMALL, COLOR_TEXT,
            FONT_THICKNESS_THIN, cv2.LINE_AA
        )
        
        return frame
    
    def handle_pinch(self, cursor_pos, current_time):
        """Handle pinch gesture"""
        # Check back button
        bx, by, bw, bh = self.back_button_rect
        if bx <= cursor_pos[0] <= bx + bw and by <= cursor_pos[1] <= by + bh:
            self.state_manager.go_back()
            return
        
        # Check cart button
        cx, cy, cw, ch = self.cart_button_rect
        if cx <= cursor_pos[0] <= cx + cw and cy <= cursor_pos[1] <= cy + ch:
            self.state_manager.transition_to(ScreenState.CART)
            return
        
        # Check add buttons
        for card in self.item_cards:
            btn_x, btn_y, btn_w, btn_h = card.add_btn_rect
            btn_y = btn_y - self.scroll_offset
            
            if btn_x <= cursor_pos[0] <= btn_x + btn_w and btn_y <= cursor_pos[1] <= btn_y + btn_h:
                self.cart_manager.add_item(card.item_data['id'], 1)
                break
