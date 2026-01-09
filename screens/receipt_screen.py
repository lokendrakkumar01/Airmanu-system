"""
Receipt Screen - Display digital receipt
"""

import cv2
from screens.base_screen import BaseScreen
from ui_framework.glass_card import GlassCard
from ui_framework.glass_button import GlassButton
from ui_framework.rendering_utils import *
from ui_framework.icons import draw_checkmark
from state_manager import ScreenState
from config import *


class ReceiptScreen(BaseScreen):
    def __init__(self, state_manager, cart_manager):
        super().__init__(state_manager, cart_manager)
        
        # New order button
        self.new_order_button = GlassButton(
            (SCREEN_WIDTH - 300) // 2,
            SCREEN_HEIGHT - 80,
            300, BUTTON_HEIGHT,
            "START NEW ORDER",
            callback=self.on_new_order,
            color=COLOR_PRIMARY
        )
    
    def on_new_order(self):
        """Start a new order"""
        self.cart_manager.clear()
        self.state_manager.reset()
    
    def on_enter(self):
        super().on_enter()
    
    def update(self, cursor_pos, current_time):
        """Update receipt screen"""
        self.new_order_button.update_hover_state(cursor_pos)
        
        # Check for dwell on new order button
        is_hovering = self.new_order_button.state == "hover"
        if self.new_order_button.update_dwell(is_hovering, current_time):
            self.on_new_order()
    
    def render(self, frame):
        """Render receipt screen"""
        # Background
        gradient = create_gradient(
            SCREEN_WIDTH, SCREEN_HEIGHT,
            (30, 40, 30), (10, 20, 10), vertical=True
        )
        frame = alpha_blend(gradient, frame, 0.6)
        
        # Success checkmark
        check_y = 60
        draw_checkmark(frame, SCREEN_WIDTH // 2 - 30, check_y, 60, COLOR_SUCCESS)
        
        # Success message
        cv2.putText(
            frame, "Order Complete!",
            (SCREEN_WIDTH // 2 - 150, check_y + 100),
            FONT_FACE, FONT_SCALE_LARGE, COLOR_SUCCESS,
            FONT_THICKNESS, cv2.LINE_AA
        )
        
        # Receipt card
        receipt_card = GlassCard(
            (SCREEN_WIDTH - 500) // 2, 200,
            500, 350,
            border_color=COLOR_SUCCESS
        )
        frame = receipt_card.render(frame)
        
        # Get receipt data
        receipt = self.state_manager.receipt_data
        if receipt:
            content_x, content_y, _, _ = receipt_card.get_content_area()
            
            y_offset = content_y
            
            # Restaurant name
            cv2.putText(
                frame, receipt['restaurant'],
                (content_x + 100, y_offset),
                FONT_FACE, FONT_SCALE_MEDIUM, COLOR_TEXT,
                FONT_THICKNESS, cv2.LINE_AA
            )
            y_offset += 30
            
            # Date and time
            date_time = f"{receipt['date']} {receipt['time']}"
            cv2.putText(
                frame, date_time,
                (content_x + 120, y_offset),
                FONT_FACE, FONT_SCALE_SMALL - 0.1, COLOR_TEXT_DIM,
                FONT_THICKNESS_THIN, cv2.LINE_AA
            )
            y_offset += 40
            
            # Divider
            cv2.line(frame, (content_x, y_offset), (content_x + 450, y_offset), COLOR_TEXT_DIM, 1)
            y_offset += 25
            
            # Items (show max 5 items to fit)
            for i, item in enumerate(receipt['items'][:5]):
                if i >= 5:
                    break
                
                # Item name and quantity
                item_text = f"{item['quantity']}x {item['name']}"
                cv2.putText(
                    frame, item_text,
                    (content_x, y_offset),
                    FONT_FACE, FONT_SCALE_SMALL - 0.1, COLOR_TEXT,
                    FONT_THICKNESS_THIN, cv2.LINE_AA
                )
                
                # Price
                price_text = f"{receipt['currency']}{item['price'] * item['quantity']:.2f}"
                cv2.putText(
                    frame, price_text,
                    (content_x + 350, y_offset),
                    FONT_FACE, FONT_SCALE_SMALL - 0.1, COLOR_TEXT,
                    FONT_THICKNESS_THIN, cv2.LINE_AA
                )
                y_offset += 25
            
            if len(receipt['items']) > 5:
                cv2.putText(
                    frame, f"... and {len(receipt['items']) - 5} more items",
                    (content_x, y_offset),
                    FONT_FACE, FONT_SCALE_SMALL - 0.2, COLOR_TEXT_DIM,
                    FONT_THICKNESS_THIN, cv2.LINE_AA
                )
                y_offset += 25
            
            y_offset += 10
            # Divider
            cv2.line(frame, (content_x, y_offset), (content_x + 450, y_offset), COLOR_TEXT_DIM, 1)
            y_offset += 25
            
            # Subtotal
            cv2.putText(
                frame, "Subtotal:",
                (content_x, y_offset),
                FONT_FACE, FONT_SCALE_SMALL, COLOR_TEXT_DIM,
                FONT_THICKNESS_THIN, cv2.LINE_AA
            )
            cv2.putText(
                frame, f"{receipt['currency']}{receipt['subtotal']:.2f}",
                (content_x + 350, y_offset),
                FONT_FACE, FONT_SCALE_SMALL, COLOR_TEXT_DIM,
                FONT_THICKNESS_THIN, cv2.LINE_AA
            )
            y_offset += 25
            
            # GST
            gst_text = f"GST ({receipt['gst_rate']:.0f}%):"
            cv2.putText(
                frame, gst_text,
                (content_x, y_offset),
                FONT_FACE, FONT_SCALE_SMALL, COLOR_TEXT_DIM,
                FONT_THICKNESS_THIN, cv2.LINE_AA
            )
            cv2.putText(
                frame, f"{receipt['currency']}{receipt['gst_amount']:.2f}",
                (content_x + 350, y_offset),
                FONT_FACE, FONT_SCALE_SMALL, COLOR_TEXT_DIM,
                FONT_THICKNESS_THIN, cv2.LINE_AA
            )
            y_offset += 35
            
            # Total
            cv2.putText(
                frame, "TOTAL:",
                (content_x, y_offset),
                FONT_FACE, FONT_SCALE_MEDIUM, COLOR_SUCCESS,
                FONT_THICKNESS, cv2.LINE_AA
            )
            cv2.putText(
                frame, f"{receipt['currency']}{receipt['total']:.2f}",
                (content_x + 350, y_offset),
                FONT_FACE, FONT_SCALE_MEDIUM, COLOR_SUCCESS,
                FONT_THICKNESS, cv2.LINE_AA
            )
        
        # Thank you message
        cv2.putText(
            frame, "Thank you for your order!",
            (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT - 130),
            FONT_FACE, FONT_SCALE_SMALL, COLOR_TEXT_DIM,
            FONT_THICKNESS_THIN, cv2.LINE_AA
        )
        
        # New order button
        frame = self.new_order_button.render(frame)
        
        return frame
    
    def handle_pinch(self, cursor_pos, current_time):
        """Handle pinch gesture"""
        if self.new_order_button.is_point_inside(*cursor_pos):
            self.on_new_order()
