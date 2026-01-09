"""
AirMenu Configuration
Central configuration for all constants and parameters
"""

# Screen Settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS_TARGET = 30

# Camera Settings
CAMERA_INDEX = 0
FLIP_CAMERA = True  # Flip for mirror effect

# Hand Tracking Settings
HAND_DETECTION_CONFIDENCE = 0.7
HAND_TRACKING_CONFIDENCE = 0.5
MAX_HANDS = 1

# Gesture Parameters
HOVER_THRESHOLD_PX = 50  # Distance to consider hovering
DWELL_TIME_SECONDS = 0.8  # Time to hold for dwell select
PINCH_THRESHOLD = 0.05  # Distance between thumb and index for pinch
INTERACTION_COOLDOWN = 0.3  # Seconds between interactions

# Smoothing Parameters
SMOOTHING_FACTOR = 0.7  # Exponential moving average factor (0-1)
JITTER_THRESHOLD = 5  # Pixels - movement below this is ignored

# Color Scheme (BGR format for OpenCV)
COLOR_PRIMARY = (255, 140, 50)  # Vibrant orange
COLOR_SECONDARY = (100, 200, 255)  # Light blue
COLOR_ACCENT = (180, 100, 255)  # Purple
COLOR_SUCCESS = (100, 255, 100)  # Green
COLOR_WARNING = (80, 180, 255)  # Yellow
COLOR_ERROR = (80, 80, 255)  # Red
COLOR_TEXT = (255, 255, 255)  # White
COLOR_TEXT_DIM = (180, 180, 180)  # Gray
COLOR_BACKGROUND = (20, 20, 30)  # Dark background

# Glassmorphism Parameters
GLASS_BLUR_AMOUNT = 21  # Must be odd number
GLASS_ALPHA = 0.15  # Background transparency
GLASS_BORDER_ALPHA = 0.3  # Border transparency
GLOW_INTENSITY = 0.6  # Glow effect strength

# Animation Settings
ANIMATION_DURATION_FAST = 0.2  # seconds
ANIMATION_DURATION_MEDIUM = 0.4  # seconds
ANIMATION_DURATION_SLOW = 0.6  # seconds

# Transition Settings
TRANSITION_SLIDE_DISTANCE = 300  # pixels
TRANSITION_DURATION = 0.5  # seconds

# UI Element Sizes
BUTTON_HEIGHT = 60
BUTTON_PADDING = 20
CARD_PADDING = 25
CARD_MARGIN = 15
ITEM_HEIGHT = 120
HEADER_HEIGHT = 80

# Font Settings
FONT_FACE = 0  # cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE_LARGE = 1.2
FONT_SCALE_MEDIUM = 0.9
FONT_SCALE_SMALL = 0.7
FONT_THICKNESS = 2
FONT_THICKNESS_THIN = 1

# Billing Settings
GST_RATE = 0.18  # 18% GST
RESTAURANT_NAME = "AirMenu Restaurant"
CURRENCY_SYMBOL = "₹"

# Debug Settings
SHOW_FPS = True
SHOW_HAND_LANDMARKS = False  # Set to True for debugging
SHOW_CURSOR = True
