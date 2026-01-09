"""
Animation Engine with Cubic Easing
"""

import time
import numpy as np


class AnimationEngine:
    def __init__(self):
        self.active_animations = []
    
    def ease_in_out_cubic(self, t):
        """Cubic ease-in-out easing function"""
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 3) / 2
    
    def ease_out_cubic(self, t):
        """Cubic ease-out easing function"""
        return 1 - pow(1 - t, 3)
    
    def ease_in_cubic(self, t):
        """Cubic ease-in easing function"""
        return t * t * t
    
    def interpolate(self, start, end, progress, easing="ease_in_out"):
        """Interpolate between start and end values with easing"""
        if easing == "ease_in_out":
            t = self.ease_in_out_cubic(progress)
        elif easing == "ease_out":
            t = self.ease_out_cubic(progress)
        elif easing == "ease_in":
            t = self.ease_in_cubic(progress)
        else:
            t = progress  # Linear
        
        return start + (end - start) * t
    
    def create_animation(self, duration, start_value, end_value, 
                        easing="ease_in_out", callback=None):
        """
        Create a new animation
        Returns animation ID
        """
        animation = {
            'id': len(self.active_animations),
            'start_time': time.time(),
            'duration': duration,
            'start_value': start_value,
            'end_value': end_value,
            'easing': easing,
            'callback': callback,
            'current_value': start_value,
            'complete': False
        }
        self.active_animations.append(animation)
        return animation['id']
    
    def update(self):
        """Update all active animations"""
        current_time = time.time()
        
        for anim in self.active_animations[:]:
            if anim['complete']:
                continue
            
            elapsed = current_time - anim['start_time']
            progress = min(elapsed / anim['duration'], 1.0)
            
            anim['current_value'] = self.interpolate(
                anim['start_value'],
                anim['end_value'],
                progress,
                anim['easing']
            )
            
            if progress >= 1.0:
                anim['complete'] = True
                anim['current_value'] = anim['end_value']
                if anim['callback']:
                    anim['callback']()
        
        # Clean up completed animations
        self.active_animations = [a for a in self.active_animations if not a['complete']]
    
    def get_value(self, animation_id):
        """Get current value of an animation"""
        for anim in self.active_animations:
            if anim['id'] == animation_id:
                return anim['current_value']
        return None
    
    def is_complete(self, animation_id):
        """Check if animation is complete"""
        for anim in self.active_animations:
            if anim['id'] == animation_id:
                return anim['complete']
        return True  # Not found = already removed = complete
    
    def clear_all(self):
        """Clear all animations"""
        self.active_animations = []
