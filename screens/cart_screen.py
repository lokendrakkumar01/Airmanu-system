"""
Cart Screen - Shopping cart with quantity controls
"""

import cv2
from screens.base_screen import BaseScreen
from ui_framework.glass_card import GlassCard
from ui_framework.glass_button import GlassButton
from ui_framework.rendering_utils import *
from ui_framework.icons import draw_back_arrow, draw_plus_icon, draw_minus_icon
from billing_engine import BillingEngine
from state_manager import ScreenState
from config import *


class CartScreen(BaseScreen):
    def __init__(self, state_manager, cart_manager):
        super().__init__(state_manager, cart_manager)
        self.item_cards = []
        self.back_button_rect = (20, 20, 100, 50)
        
        # Checkout button
        self.checkout_button = GlassButton(
            (SCREEN_WIDTH - 300) // 2,
            SCREEN_HEIGHT - 100,
            300, BUTTON_HEIGHT,
            "CHECKOUT",
            callback=self.on_checkout,
            color=COLOR_SUCCESS
        )
    
    def on_enter(self):
        """Refresh cart items"""
        super().on_enter()
        self._create_item_cards()
    
    def _create_item_cards(self):
        """Create cards for cart items"""
        self.item_cards = []
        cart_items = self.cart_manager.get_items()
        
        card_width = SCREEN_WIDTH - 100
        card_height = 100
        start_x = 50
        start_y = 120
        spacing = 15
        
        for i, item in enumerate(cart_items):
            y = start_y + i * (card_height + spacing)
            card = GlassCard(start_x, y, card_width, card_height, border_color=COLOR_SECONDARY)
            card.item_data = item
            
            # Control button positions
            controls_x = start_x + card_width - 150
            controls_y = y + (card_height - 40) // 2
            
            card.minus_btn_rect = (controls_x, controls_y, 40, 40)
            card.plus_btn_rect = (controls_x + 85, controls_y, 40, 40)
            
            self.item_cards.append(card)
    
    def on_checkout(self):
        """Proceed to checkout"""
        if not self.cart_manager.is_empty():
            receipt = BillingEngine.generate_receipt(self.cart_manager.get_items())
            self.state_manager.transition_to(ScreenState.RECEIPT, {'receipt': receipt})
    
    def update(self, cursor_pos, current_time):
        """Update cart screen"""
        # Update button states
        self.checkout_button.update_hover_state(cursor_pos)
        
        # Check for dwell on checkout
        is_hovering = self.checkout_button.state == "hover"
        if self.checkout_button.update_dwell(is_hovering, current_time):
            self.on_checkout()
        
        # Update card hover states
        for card in self.item_cards:
            card.update_hover_state(cursor_pos)
    
    def render(self, frame):
        """Render cart screen"""
        # Background
        gradient = create_gradient(
            SCREEN_WIDTH, SCREEN_HEIGHT,
            (30, 25, 20), (15, 10, 20), vertical=True
        )
        frame = alpha_blend(gradient, frame, 0.6)
        
        # Header
        cv2.putText(
            frame, "Your Cart",
            (SCREEN_WIDTH // 2 - 100, 80),
            FONT_FACE, FONT_SCALE_LARGE, COLOR_TEXT,
            FONT_THICKNESS, cv2.LINE_AA
        )
        
        # Check if cart is empty
        if self.cart_manager.is_empty():
            cv2.putText(
                frame, "Cart is empty",
                (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2),
                FONT_FACE, FONT_SCALE_MEDIUM, COLOR_TEXT_DIM,
                FONT_THICKNESS_THIN, cv2.LINE_AA
            )
        else:
            # Render cart items
            for card in self.item_cards:
                frame = card.render(frame)
                
                content_x, content_y, content_w, content_h = card.get_content_area()
                
                # Item name
                cv2.putText(
                    frame, card.item_data['name'],
                    (content_x, content_y + 20),
                    FONT_FACE, FONT_SCALE_SMALL, COLOR_TEXT,
                    FONT_THICKNESS_THIN, cv2.LINE_AA
                )
                
                # Price
                price_text = f"{CURRENCY_SYMBOL}{card.item_data['price']} each"
                cv2.putText(
                    frame, price_text,
                    (content_x, content_y + 45),
                    FONT_FACE, FONT_SCALE_SMALL - 0.1, COLOR_TEXT_DIM,
                    FONT_THICKNESS_THIN, cv2.LINE_AA
                )
                
                # Quantity controls
                minus_x, minus_y, minus_w, minus_h = card.minus_btn_rect
                plus_x, plus_y, plus_w, plus_h = card.plus_btn_rect
                
                # Minus button
                minus_overlay = frame.copy()
                draw_rounded_rectangle(minus_overlay, minus_x, minus_y, minus_w, minus_h, 8, COLOR_WARNING, -1)
                frame = alpha_blend(minus_overlay, frame, 0.6)
                draw_minus_icon(frame, minus_x + 5, minus_y + 5, 30, COLOR_TEXT)
                
                # Quantity display
                qty_text = str(card.item_data['quantity'])
                qty_x = minus_x + minus_w + 15
                qty_y = minus_y + 28
                cv2.putText(
                    frame, qty_text,
                    (qty_x, qty_y),
                    FONT_FACE, FONT_SCALE_MEDIUM, COLOR_TEXT,
                    FONT_THICKNESS, cv2.LINE_AA
                )
                
                # Plus button
                plus_overlay = frame.copy()
                draw_rounded_rectangle(plus_overlay, plus_x, plus_y, plus_w, plus_h, 8, COLOR_SUCCESS, -1)
                frame = alpha_blend(plus_overlay, frame, 0.6)
                draw_plus_icon(frame, plus_x + 5, plus_y + 5, 30, COLOR_TEXT)
            
            # Billing summary
            subtotal = self.cart_manager.get_subtotal()
            gst = BillingEngine.calculate_gst(subtotal)
            total = BillingEngine.calculate_total(subtotal, gst)
            
            summary_y = SCREEN_HEIGHT - 220
            summary_x = SCREEN_WIDTH - 350
            
            # Summary card
            summary_card = GlassCard(summary_x - 20, summary_y - 20, 320, 100, border_color=COLOR_ACCENT)
            frame = summary_card.render(frame)
            
            cv2.putText(frame, f"Subtotal: {CURRENCY_SYMBOL}{subtotal:.2f}",
                       (summary_x, summary_y + 10), FONT_FACE, FONT_SCALE_SMALL,
                       COLOR_TEXT_DIM, FONT_THICKNESS_THIN, cv2.LINE_AA)
            
            cv2.putText(frame, f"GST (18%): {CURRENCY_SYMBOL}{gst:.2f}",
                       (summary_x, summary_y + 35), FONT_FACE, FONT_SCALE_SMALL,
                       COLOR_TEXT_DIM, FONT_THICKNESS_THIN, cv2.LINE_AA)
            
            cv2.putText(frame, f"Total: {CURRENCY_SYMBOL}{total:.2f}",
                       (summary_x, summary_y + 65), FONT_FACE, FONT_SCALE_MEDIUM,
                       COLOR_ACCENT, FONT_THICKNESS, cv2.LINE_AA)
            
            # Checkout button
            frame = self.checkout_button.render(frame)
        
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
        
        # Check checkout button
        if not self.cart_manager.is_empty():
            if self.checkout_button.is_point_inside(*cursor_pos):
                self.on_checkout()
                return
        
        # Check quantity controls
        for card in self.item_cards:
            # Minus button
            mx, my, mw, mh = card.minus_btn_rect
            if mx <= cursor_pos[0] <= mx + mw and my <= cursor_pos[1] <= my + mh:
                new_qty = card.item_data['quantity'] - 1
                self.cart_manager.update_quantity(card.item_data['id'], new_qty)
                self._create_item_cards()  # Refresh
                break
            
            # Plus button
            px, py, pw, ph = card.plus_btn_rect
            if px <= cursor_pos[0] <= px + pw and py <= cursor_pos[1] <= py + ph:
                new_qty = card.item_data['quantity'] + 1
                self.cart_manager.update_quantity(card.item_data['id'], new_qty)
                self._create_item_cards()  # Refresh
                break
