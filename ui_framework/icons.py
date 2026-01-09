"""
Icon Rendering using OpenCV Primitives
"""

import cv2
import numpy as np
from config import *


def draw_cart_icon(frame, x, y, size, color):
    """Draw a shopping cart icon"""
    # Cart body
    pts = np.array([
        [x + size//4, y + size//3],
        [x + size//4, y + size//2],
        [x + 3*size//4, y + size//2],
        [x + 3*size//4 + size//6, y + size//3]
    ], np.int32)
    cv2.polylines(frame, [pts], False, color, 2)
    
    # Handle
    cv2.ellipse(frame, (x + size//2, y + size//6), 
                (size//6, size//6), 0, 180, 360, color, 2)
    
    # Wheels
    cv2.circle(frame, (x + size//3, y + 3*size//4), size//10, color, -1)
    cv2.circle(frame, (x + 2*size//3, y + 3*size//4), size//10, color, -1)


def draw_category_icon(frame, x, y, size, color, icon_type="food"):
    """Draw category icons"""
    if icon_type == "food":
        # Plate with fork and knife
        cv2.circle(frame, (x + size//2, y + size//2), size//3, color, 2)
        cv2.line(frame, (x + size//6, y + size//6), 
                (x + size//6, y + 5*size//6), color, 2)
        cv2.line(frame, (x + 5*size//6, y + size//6), 
                (x + 5*size//6, y + 5*size//6), color, 2)
    
    elif icon_type == "drinks":
        # Cup
        pts = np.array([
            [x + size//3, y + size//3],
            [x + size//4, y + 3*size//4],
            [x + 3*size//4, y + 3*size//4],
            [x + 2*size//3, y + size//3]
        ], np.int32)
        cv2.polylines(frame, [pts], True, color, 2)
        cv2.line(frame, (x + 2*size//3, y + size//2), 
                (x + 5*size//6, y + size//2), color, 2)
    
    elif icon_type == "dessert":
        # Ice cream cone
        cv2.circle(frame, (x + size//2, y + size//3), size//4, color, 2)
        pts = np.array([
            [x + size//2, y + size//2],
            [x + size//4, y + 5*size//6],
            [x + 3*size//4, y + 5*size//6]
        ], np.int32)
        cv2.polylines(frame, [pts], True, color, 2)
    
    elif icon_type == "starters":
        # Star
        center = (x + size//2, y + size//2)
        outer_r = size//3
        inner_r = size//6
        points = []
        for i in range(10):
            angle = i * 36 - 90
            r = outer_r if i % 2 == 0 else inner_r
            px = int(center[0] + r * np.cos(np.radians(angle)))
            py = int(center[1] + r * np.sin(np.radians(angle)))
            points.append([px, py])
        pts = np.array(points, np.int32)
        cv2.polylines(frame, [pts], True, color, 2)


def draw_plus_icon(frame, x, y, size, color):
    """Draw a plus (+) icon"""
    cv2.line(frame, (x + size//2, y + size//4), 
            (x + size//2, y + 3*size//4), color, 2)
    cv2.line(frame, (x + size//4, y + size//2), 
            (x + 3*size//4, y + size//2), color, 2)


def draw_minus_icon(frame, x, y, size, color):
    """Draw a minus (-) icon"""
    cv2.line(frame, (x + size//4, y + size//2), 
            (x + 3*size//4, y + size//2), color, 2)


def draw_back_arrow(frame, x, y, size, color):
    """Draw a back arrow <-"""
    # Arrow head
    pts = np.array([
        [x + size//3, y + size//2],
        [x + size//2, y + size//4],
        [x + size//2, y + 3*size//4]
    ], np.int32)
    cv2.polylines(frame, [pts], False, color, 2)
    # Arrow line
    cv2.line(frame, (x + size//3, y + size//2), 
            (x + 2*size//3, y + size//2), color, 2)


def draw_checkmark(frame, x, y, size, color):
    """Draw a checkmark icon"""
    pts = np.array([
        [x + size//4, y + size//2],
        [x + 2*size//5, y + 2*size//3],
        [x + 3*size//4, y + size//3]
    ], np.int32)
    cv2.polylines(frame, [pts], False, color, 3)


def draw_home_icon(frame, x, y, size, color):
    """Draw a home icon"""
    # Roof
    pts = np.array([
        [x + size//2, y + size//4],
        [x + size//6, y + size//2],
        [x + 5*size//6, y + size//2]
    ], np.int32)
    cv2.polylines(frame, [pts], True, color, 2)
    # House body
    cv2.rectangle(frame, (x + size//4, y + size//2), 
                 (x + 3*size//4, y + 5*size//6), color, 2)
    # Door
    cv2.rectangle(frame, (x + 2*size//5, y + 3*size//5), 
                 (x + 3*size//5, y + 5*size//6), color, -1)
