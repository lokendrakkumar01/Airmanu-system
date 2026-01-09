"""
Utility Functions for AirMenu
"""

import logging
from datetime import datetime


def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger('AirMenu')


def format_timestamp():
    """Format current timestamp"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def clamp(value, min_value, max_value):
    """Clamp value between min and max"""
    return max(min_value, min(value, max_value))


def lerp(a, b, t):
    """Linear interpolation between a and b"""
    return a + (b - a) * t
