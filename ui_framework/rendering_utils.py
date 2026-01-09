"""
Rendering Utilities for Custom OpenCV UI
Provides alpha blending, blur effects, gradients, shadows, and glow
"""

import cv2
import numpy as np


def alpha_blend(foreground, background, alpha):
    """
    Blend foreground onto background with alpha transparency
    alpha: 0.0 (transparent) to 1.0 (opaque)
    """
    return cv2.addWeighted(foreground, alpha, background, 1 - alpha, 0)


def apply_gaussian_blur(image, kernel_size=21):
    """Apply Gaussian blur for glassmorphism effect"""
    if kernel_size % 2 == 0:
        kernel_size += 1  # Must be odd
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)


def create_gradient(width, height, color1, color2, vertical=True):
    """
    Create a gradient image
    vertical: True for top-to-bottom, False for left-to-right
    """
    gradient = np.zeros((height, width, 3), dtype=np.uint8)
    
    if vertical:
        for y in range(height):
            ratio = y / height
            color = [
                int(color1[i] * (1 - ratio) + color2[i] * ratio)
                for i in range(3)
            ]
            gradient[y, :] = color
    else:
        for x in range(width):
            ratio = x / width
            color = [
                int(color1[i] * (1 - ratio) + color2[i] * ratio)
                for i in range(3)
            ]
            gradient[:, x] = color
    
    return gradient


def create_radial_gradient(width, height, center_color, edge_color):
    """Create a radial gradient from center to edges"""
    gradient = np.zeros((height, width, 3), dtype=np.uint8)
    center_x, center_y = width // 2, height // 2
    max_distance = np.sqrt(center_x**2 + center_y**2)
    
    for y in range(height):
        for x in range(width):
            distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            ratio = min(distance / max_distance, 1.0)
            color = [
                int(center_color[i] * (1 - ratio) + edge_color[i] * ratio)
                for i in range(3)
            ]
            gradient[y, x] = color
    
    return gradient


def add_soft_shadow(frame, x, y, w, h, offset=10, blur=15, alpha=0.3):
    """Add a soft shadow behind a rectangle"""
    shadow = np.zeros_like(frame)
    cv2.rectangle(
        shadow,
        (x + offset, y + offset),
        (x + w + offset, y + h + offset),
        (0, 0, 0),
        -1
    )
    shadow = cv2.GaussianBlur(shadow, (blur, blur), 0)
    return alpha_blend(shadow, frame, alpha)


def add_glow_effect(frame, x, y, w, h, color, intensity=0.6):
    """Add a glow effect around a rectangle"""
    glow = np.zeros_like(frame)
    
    # Multiple layers for soft glow
    for i in range(3):
        thickness = 3 - i
        offset = i * 5
        cv2.rectangle(
            glow,
            (x - offset, y - offset),
            (x + w + offset, y + h + offset),
            color,
            thickness
        )
    
    glow = cv2.GaussianBlur(glow, (25, 25), 0)
    return alpha_blend(glow, frame, intensity)


def safe_overlay(background, overlay, x, y):
    """
    Safely overlay an image onto background at position (x, y)
    Handles boundary clipping
    """
    bg_h, bg_w = background.shape[:2]
    ov_h, ov_w = overlay.shape[:2]
    
    # Calculate valid region
    x1_bg = max(0, x)
    y1_bg = max(0, y)
    x2_bg = min(bg_w, x + ov_w)
    y2_bg = min(bg_h, y + ov_h)
    
    x1_ov = max(0, -x)
    y1_ov = max(0, -y)
    x2_ov = x1_ov + (x2_bg - x1_bg)
    y2_ov = y1_ov + (y2_bg - y1_bg)
    
    # Check if there's any overlap
    if x2_bg <= x1_bg or y2_bg <= y1_bg:
        return background
    
    # Overlay the valid region
    background[y1_bg:y2_bg, x1_bg:x2_bg] = overlay[y1_ov:y2_ov, x1_ov:x2_ov]
    return background


def create_glass_effect(background_roi, alpha=0.15, blur_amount=21):
    """
    Create glassmorphism effect on a region of interest
    Returns the glassy version of the ROI
    """
    # Blur the background
    blurred = apply_gaussian_blur(background_roi, blur_amount)
    
    # Lighten slightly
    brightened = cv2.addWeighted(blurred, 1.0, blurred, 0, 30)
    
    # Blend with original for subtle effect
    glass = alpha_blend(brightened, background_roi, alpha)
    
    return glass


def draw_rounded_rectangle(frame, x, y, w, h, radius, color, thickness=-1):
    """Draw a rectangle with rounded corners"""
    # Top-left
    cv2.ellipse(frame, (x + radius, y + radius), (radius, radius), 180, 0, 90, color, thickness)
    # Top-right  
    cv2.ellipse(frame, (x + w - radius, y + radius), (radius, radius), 270, 0, 90, color, thickness)
    # Bottom-right
    cv2.ellipse(frame, (x + w - radius, y + h - radius), (radius, radius), 0, 0, 90, color, thickness)
    # Bottom-left
    cv2.ellipse(frame, (x + radius, y + h - radius), (radius, radius), 90, 0, 90, color, thickness)
    
    # Rectangles to fill
    if thickness == -1:
        cv2.rectangle(frame, (x + radius, y), (x + w - radius, y + h), color, -1)
        cv2.rectangle(frame, (x, y + radius), (x + w, y + h - radius), color, -1)
    else:
        # Top, bottom, left, right lines
        cv2.line(frame, (x + radius, y), (x + w - radius, y), color, thickness)
        cv2.line(frame, (x + radius, y + h), (x + w - radius, y + h), color, thickness)
        cv2.line(frame, (x, y + radius), (x, y + h - radius), color, thickness)
        cv2.line(frame, (x + w, y + radius), (x + w, y + h - radius), color, thickness)


def measure_text(text, font_face, font_scale, thickness):
    """Measure text dimensions"""
    (text_width, text_height), baseline = cv2.getTextSize(
        text, font_face, font_scale, thickness
    )
    return text_width, text_height, baseline


def draw_text_centered(frame, text, x, y, w, h, color, font_face, font_scale, thickness):
    """Draw text centered in a rectangle"""
    text_w, text_h, baseline = measure_text(text, font_face, font_scale, thickness)
    
    text_x = x + (w - text_w) // 2
    text_y = y + (h + text_h) // 2
    
    cv2.putText(
        frame, text, (text_x, text_y),
        font_face, font_scale, color, thickness, cv2.LINE_AA
    )
