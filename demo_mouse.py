"""
AirMenu Demo - Mouse-based Version (No Hand Tracking Required)
This demo version uses mouse clicks instead of hand gestures to test the UI
"""

import cv2
import time
import numpy as np
from config import *
from cart_manager import CartManager
from state_manager import StateManager, ScreenState
from screens.home_screen import HomeScreen
from screens.category_screen import CategoryScreen
from screens.items_screen import ItemsScreen
from screens.cart_screen import CartScreen
from screens.receipt_screen import ReceiptScreen
from utils import setup_logging


# Global mouse position
mouse_pos = None
mouse_clicked = False


def mouse_callback(event, x, y, flags, param):
    """Mouse callback for OpenCV window"""
    global mouse_pos, mouse_clicked
    mouse_pos = (x, y)
    if event == cv2.EVENT_LBUTTONDOWN:
        mouse_clicked = True


class AirMenuDemo:
    def __init__(self):
        self.logger = setup_logging()
        self.logger.info("Initializing AirMenu Demo (Mouse-based)...")
        
        # Create a blank camera feed
        self.frame_width = SCREEN_WIDTH
        self.frame_height = SCREEN_HEIGHT
        
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
        
        # Setup mouse callback
        cv2.namedWindow('AirMenu Demo - Mouse Control')
        cv2.setMouseCallback('AirMenu Demo - Mouse Control', mouse_callback)
        
        self.logger.info("AirMenu Demo initialized successfully")
    
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
        global mouse_clicked
        self.logger.info("Starting demo loop...")
        
        try:
            while True:
                # Create a dark gradient background
                frame = np.zeros((self.frame_height, self.frame_width, 3), dtype=np.uint8)
                
                # Create canvas for rendering
                canvas = frame.copy()
                
                # Update state manager
                self.state_manager.update()
                
                # Handle screen transitions
                self.handle_screen_transition()
                
                # Get current time
                current_time = time.time()
                
                # Update current screen with mouse position
                self.current_screen.update(mouse_pos, current_time)
                
                # Render current screen
                canvas = self.current_screen.render(canvas)
                
                # Handle mouse click
                if mouse_clicked and mouse_pos:
                    self.current_screen.handle_pinch(mouse_pos, current_time)
                    mouse_clicked = False
                
                # Draw mouse cursor
                if mouse_pos:
                    cv2.circle(canvas, mouse_pos, 15, COLOR_PRIMARY, -1)
                    cv2.circle(canvas, mouse_pos, 5, COLOR_TEXT, -1)
                
                # Show FPS
                self.update_fps()
                fps_text = f"FPS: {self.fps:.1f}"
                cv2.putText(
                    canvas, fps_text,
                    (10, self.frame_height - 20),
                    FONT_FACE, FONT_SCALE_SMALL - 0.2,
                    COLOR_SUCCESS if self.fps >= 25 else COLOR_WARNING,
                    FONT_THICKNESS_THIN, cv2.LINE_AA
                )
                
                # Instruction text
                cv2.putText(
                    canvas, "Mouse Control Mode - Click to interact",
                    (10, 30),
                    FONT_FACE, FONT_SCALE_SMALL - 0.2,
                    COLOR_ACCENT,
                    FONT_THICKNESS_THIN, cv2.LINE_AA
                )
                
                # Display frame
                cv2.imshow('AirMenu Demo - Mouse Control', canvas)
                
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
        cv2.destroyAllWindows()
        self.logger.info("AirMenu Demo shutdown complete")


def main():
    """Entry point"""
    print("="*60)
    print("AirMenu Demo - Mouse Control Version")
    print("="*60)
    print("This is a demo version that uses mouse instead of hand tracking")
    print("\nControls:")
    print("  - Move mouse to navigate")
    print("  - Click to interact with buttons")
    print("  - Hover over buttons to see dwell animation")
    print("  - Press ESC to exit")
    print("  - Press R to reset to home")
    print("="*60)
    print()
    
    try:
        app = AirMenuDemo()
        app.run()
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
