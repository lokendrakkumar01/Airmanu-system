"""
AirMenu - Touchless AR Restaurant Menu System
Main Application Entry Point
"""

import cv2
import time
import numpy as np
from config import *
from hand_tracker import HandTracker
from cart_manager import CartManager
from state_manager import StateManager, ScreenState
from screens.home_screen import HomeScreen
from screens.category_screen import CategoryScreen
from screens.items_screen import ItemsScreen
from screens.cart_screen import CartScreen
from screens.receipt_screen import ReceiptScreen
from utils import setup_logging


class AirMenu:
    def __init__(self):
        self.logger = setup_logging()
        self.logger.info("Initializing AirMenu...")
        
        # Initialize camera
        self.cap = cv2.VideoCapture(CAMERA_INDEX)
        if not self.cap.isOpened():
            self.logger.error("Failed to open camera")
            raise RuntimeError("Could not access camera")
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, SCREEN_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, SCREEN_HEIGHT)
        
        # Initialize hand tracker
        self.hand_tracker = HandTracker()
        
        # Initialize managers
        self.cart_manager = CartManager()
        self.state_manager = StateManager()
        
        # Initialize screens
        self.screens = {
            ScreenState.HOME: HomeScreen(self.state_manager, self.cart_manager),
            ScreenState.CATEGORY: CategoryScreen(self.state_manager, self.cart_manager),
            ScreenState.ITEMS: ItemsScreen(self.state_manager, self.cart_manager),
            ScreenState.CART: CartScreen(self.state_manager, self.cart_manager),
            ScreenState.RECEIPT: ReceiptScreen(self.state_manager, self.cart_manager),
        }
        
        # Set initial screen
        self.current_screen = self.screens[ScreenState.HOME]
        self.current_screen.on_enter()
        self.previous_state = None
        
        # FPS tracking
        self.fps = 0
        self.frame_count = 0
        self.fps_start_time = time.time()
        
        self.logger.info("AirMenu initialized successfully")
    
    def update_fps(self):
        """Calculate FPS"""
        self.frame_count += 1
        elapsed = time.time() - self.fps_start_time
        if elapsed >= 1.0:
            self.fps = self.frame_count / elapsed
            self.frame_count = 0
            self.fps_start_time = time.time()
    
    def handle_screen_transition(self):
        """Handle screen state transitions"""
        if self.state_manager.current_state != self.previous_state:
            # Exit previous screen
            if self.current_screen:
                self.current_screen.on_exit()
            
            # Enter new screen
            self.current_screen = self.screens[self.state_manager.current_state]
            self.current_screen.on_enter()
            self.previous_state = self.state_manager.current_state
    
    def run(self):
        """Main application loop"""
        self.logger.info("Starting main loop...")
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    self.logger.error("Failed to read frame")
                    break
                
                # Flip for mirror effect
                if FLIP_CAMERA:
                    frame = cv2.flip(frame, 1)
                
                # Resize to target resolution
                frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
                
                # Create canvas for double buffering
                canvas = frame.copy()
                
                # Hand tracking
                hand_detected = self.hand_tracker.find_hands(frame)
                cursor_pos = None
                
                if hand_detected:
                    cursor_pos = self.hand_tracker.get_fingertip_position(frame.shape)
                    
                    # Show landmarks if debug enabled
                    if SHOW_HAND_LANDMARKS:
                        self.hand_tracker.draw_landmarks(canvas)
                
                # Update state manager
                self.state_manager.update()
                
                # Handle screen transitions
                self.handle_screen_transition()
                
                # Get current time
                current_time = time.time()
                
                # Update current screen
                self.current_screen.update(cursor_pos, current_time)
                
                # Render current screen
                canvas = self.current_screen.render(canvas)
                
                # Handle pinch gesture
                if hand_detected:
                    pinch_event = self.hand_tracker.get_pinch_event()
                    if pinch_event and cursor_pos:
                        if self.hand_tracker.check_interaction_cooldown(current_time):
                            self.current_screen.handle_pinch(cursor_pos, current_time)
                            self.hand_tracker.mark_interaction(current_time)
                
                # Draw cursor
                if SHOW_CURSOR and cursor_pos:
                    self.hand_tracker.draw_cursor(canvas, cursor_pos)
                
                # Show FPS
                if SHOW_FPS:
                    self.update_fps()
                    fps_text = f"FPS: {self.fps:.1f}"
                    cv2.putText(
                        canvas, fps_text,
                        (10, SCREEN_HEIGHT - 20),
                        FONT_FACE, FONT_SCALE_SMALL - 0.2,
                        COLOR_SUCCESS if self.fps >= 25 else COLOR_WARNING,
                        FONT_THICKNESS_THIN, cv2.LINE_AA
                    )
                
                # Hand tracking status
                status_text = "Hand Detected" if hand_detected else "No Hand"
                status_color = COLOR_SUCCESS if hand_detected else COLOR_ERROR
                cv2.putText(
                    canvas, status_text,
                    (10, 30),
                    FONT_FACE, FONT_SCALE_SMALL - 0.2,
                    status_color,
                    FONT_THICKNESS_THIN, cv2.LINE_AA
                )
                
                # Display frame
                cv2.imshow('AirMenu - Touchless AR Menu', canvas)
                
                # Check for exit (ESC key)
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESC
                    self.logger.info("Exit requested by user")
                    break
                elif key == ord('r'):  # R key to reset
                    self.logger.info("Reset to home screen")
                    self.state_manager.reset()
                    self.cart_manager.clear()
        
        except Exception as e:
            self.logger.error(f"Error in main loop: {e}", exc_info=True)
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.logger.info("Cleaning up...")
        self.cap.release()
        cv2.destroyAllWindows()
        self.logger.info("AirMenu shutdown complete")


def main():
    """Entry point"""
    try:
        app = AirMenu()
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
