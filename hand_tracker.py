"""
Hand Tracking Module using Mediapipe
Provides fingertip tracking with smoothing and gesture detection
"""

import cv2
import mediapipe as mp
import numpy as np
from config import *


class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=MAX_HANDS,
            min_detection_confidence=HAND_DETECTION_CONFIDENCE,
            min_tracking_confidence=HAND_TRACKING_CONFIDENCE
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Smoothing
        self.prev_x = None
        self.prev_y = None
        
        # Gesture state
        self.is_pinching = False
        self.prev_pinch_state = False
        self.hover_start_time = None
        self.last_interaction_time = 0
        
    def find_hands(self, frame):
        """Process frame and detect hands"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_frame)
        return self.results.multi_hand_landmarks is not None
    
    def get_fingertip_position(self, frame_shape):
        """
        Get smoothed index fingertip position
        Returns (x, y) or None if no hand detected
        """
        if not self.results.multi_hand_landmarks:
            self.prev_x = None
            self.prev_y = None
            return None
        
        # Get first hand
        hand_landmarks = self.results.multi_hand_landmarks[0]
        
        # Index finger tip is landmark 8
        index_tip = hand_landmarks.landmark[8]
        
        # Convert normalized coordinates to pixel coordinates
        h, w = frame_shape[:2]
        x = int(index_tip.x * w)
        y = int(index_tip.y * h)
        
        # Apply smoothing
        if self.prev_x is not None:
            # Exponential moving average
            x = int(SMOOTHING_FACTOR * x + (1 - SMOOTHING_FACTOR) * self.prev_x)
            y = int(SMOOTHING_FACTOR * y + (1 - SMOOTHING_FACTOR) * self.prev_y)
            
            # Jitter reduction
            dx = abs(x - self.prev_x)
            dy = abs(y - self.prev_y)
            if dx < JITTER_THRESHOLD and dy < JITTER_THRESHOLD:
                x = self.prev_x
                y = self.prev_y
        
        self.prev_x = x
        self.prev_y = y
        
        return (x, y)
    
    def detect_pinch(self):
        """
        Detect pinch gesture (thumb and index finger close together)
        Returns True if pinching
        """
        if not self.results.multi_hand_landmarks:
            self.is_pinching = False
            return False
        
        hand_landmarks = self.results.multi_hand_landmarks[0]
        
        # Thumb tip is landmark 4, index tip is landmark 8
        thumb = hand_landmarks.landmark[4]
        index = hand_landmarks.landmark[8]
        
        # Calculate distance
        distance = np.sqrt((thumb.x - index.x)**2 + (thumb.y - index.y)**2)
        
        self.is_pinching = distance < PINCH_THRESHOLD
        return self.is_pinching
    
    def get_pinch_event(self):
        """
        Returns True on pinch transition (not pinching -> pinching)
        This gives a single click event rather than continuous
        """
        current_pinch = self.detect_pinch()
        pinch_event = current_pinch and not self.prev_pinch_state
        self.prev_pinch_state = current_pinch
        return pinch_event
    
    def check_interaction_cooldown(self, current_time):
        """Check if enough time has passed since last interaction"""
        if current_time - self.last_interaction_time >= INTERACTION_COOLDOWN:
            return True
        return False
    
    def mark_interaction(self, current_time):
        """Mark that an interaction occurred"""
        self.last_interaction_time = current_time
    
    def draw_landmarks(self, frame):
        """Draw hand landmarks on frame (for debugging)"""
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
    
    def draw_cursor(self, frame, position, radius=15):
        """Draw cursor at fingertip position"""
        if position:
            # Outer glow
            cv2.circle(frame, position, radius + 10, COLOR_PRIMARY, 2)
            cv2.circle(frame, position, radius + 5, COLOR_PRIMARY, 1)
            # Inner circle
            cv2.circle(frame, position, radius, COLOR_PRIMARY, -1)
            # Center dot
            cv2.circle(frame, position, 5, COLOR_TEXT, -1)
            
            # Pinch indicator
            if self.is_pinching:
                cv2.circle(frame, position, radius + 15, COLOR_SUCCESS, 3)
