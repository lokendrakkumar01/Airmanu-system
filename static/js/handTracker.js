/**
 * AirMenu - Hand Tracking Module
 * Uses MediaPipe Hands for browser-based hand tracking
 */

class HandTracker {
    constructor() {
        this.hands = null;
        this.camera = null;
        this.videoElement = null;
        this.canvas = null;
        this.ctx = null;
        this.isConnected = false;
        this.handDetected = false;
        
        // Cursor state
        this.cursorPos = { x: 0, y: 0 };
        this.smoothedPos = { x: 0, y: 0 };
        this.prevPos = { x: 0, y: 0 };
        
        // Gesture state
        this.isPinching = false;
        this.wasPinching = false;
        this.pinchEvent = false;
        
        // Config
        this.smoothingFactor = 0.7;
        this.pinchThreshold = 0.08;
        this.jitterThreshold = 3;
        
        // Callbacks
        this.onHandUpdate = null;
        this.onPinch = null;
        this.onStatusChange = null;
    }
    
    async init() {
        this.videoElement = document.getElementById('camera');
        this.canvas = document.getElementById('cursor-canvas');
        this.ctx = this.canvas.getContext('2d');
        
        // Set canvas size
        this.resizeCanvas();
        window.addEventListener('resize', () => this.resizeCanvas());
        
        // Initialize MediaPipe Hands
        this.hands = new Hands({
            locateFile: (file) => {
                return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
            }
        });
        
        this.hands.setOptions({
            maxNumHands: 1,
            modelComplexity: 1,
            minDetectionConfidence: 0.7,
            minTrackingConfidence: 0.5
        });
        
        this.hands.onResults((results) => this.onResults(results));
        
        // Start camera
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { 
                    width: 1280, 
                    height: 720,
                    facingMode: 'user'
                }
            });
            
            this.videoElement.srcObject = stream;
            await this.videoElement.play();
            
            // Start processing
            this.isConnected = true;
            this.updateStatus('connected', 'Camera Ready - Show your hand');
            this.processFrame();
            
        } catch (error) {
            console.error('Camera access error:', error);
            this.updateStatus('error', 'Camera access denied');
        }
    }
    
    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    async processFrame() {
        if (!this.isConnected) return;
        
        if (this.videoElement.readyState >= 2) {
            await this.hands.send({ image: this.videoElement });
        }
        
        requestAnimationFrame(() => this.processFrame());
    }
    
    onResults(results) {
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
            const landmarks = results.multiHandLandmarks[0];
            
            if (!this.handDetected) {
                this.handDetected = true;
                this.updateStatus('connected', 'Hand Detected ✓');
            }
            
            // Get index fingertip (landmark 8)
            const indexTip = landmarks[8];
            const thumbTip = landmarks[4];
            
            // Convert to screen coordinates (mirror horizontally)
            const rawX = (1 - indexTip.x) * this.canvas.width;
            const rawY = indexTip.y * this.canvas.height;
            
            // Apply smoothing
            this.smoothedPos.x = this.smoothingFactor * this.smoothedPos.x + 
                                 (1 - this.smoothingFactor) * rawX;
            this.smoothedPos.y = this.smoothingFactor * this.smoothedPos.y + 
                                 (1 - this.smoothingFactor) * rawY;
            
            // Jitter reduction
            const dx = Math.abs(this.smoothedPos.x - this.prevPos.x);
            const dy = Math.abs(this.smoothedPos.y - this.prevPos.y);
            
            if (dx > this.jitterThreshold || dy > this.jitterThreshold) {
                this.cursorPos.x = this.smoothedPos.x;
                this.cursorPos.y = this.smoothedPos.y;
                this.prevPos.x = this.cursorPos.x;
                this.prevPos.y = this.cursorPos.y;
            }
            
            // Detect pinch gesture
            const pinchDistance = this.getDistance(indexTip, thumbTip);
            this.wasPinching = this.isPinching;
            this.isPinching = pinchDistance < this.pinchThreshold;
            
            // Pinch event (on pinch start)
            if (this.isPinching && !this.wasPinching) {
                this.pinchEvent = true;
                if (this.onPinch) {
                    this.onPinch(this.cursorPos);
                }
            } else {
                this.pinchEvent = false;
            }
            
            // Draw cursor
            this.drawCursor();
            
            // Callback
            if (this.onHandUpdate) {
                this.onHandUpdate(this.cursorPos, this.isPinching);
            }
            
        } else {
            if (this.handDetected) {
                this.handDetected = false;
                this.updateStatus('no-hand', 'No Hand - Show your hand');
            }
            
            if (this.onHandUpdate) {
                this.onHandUpdate(null, false);
            }
        }
    }
    
    getDistance(p1, p2) {
        return Math.sqrt(
            Math.pow(p1.x - p2.x, 2) + 
            Math.pow(p1.y - p2.y, 2) +
            Math.pow(p1.z - p2.z, 2)
        );
    }
    
    drawCursor() {
        const { x, y } = this.cursorPos;
        
        // Outer glow
        const gradient = this.ctx.createRadialGradient(x, y, 0, x, y, 40);
        gradient.addColorStop(0, this.isPinching ? 'rgba(78, 205, 196, 0.4)' : 'rgba(255, 107, 107, 0.3)');
        gradient.addColorStop(1, 'transparent');
        
        this.ctx.fillStyle = gradient;
        this.ctx.beginPath();
        this.ctx.arc(x, y, 40, 0, Math.PI * 2);
        this.ctx.fill();
        
        // Inner circle
        this.ctx.fillStyle = this.isPinching ? '#4ECDC4' : '#FF6B6B';
        this.ctx.beginPath();
        this.ctx.arc(x, y, 12, 0, Math.PI * 2);
        this.ctx.fill();
        
        // White center
        this.ctx.fillStyle = 'white';
        this.ctx.beginPath();
        this.ctx.arc(x, y, 5, 0, Math.PI * 2);
        this.ctx.fill();
        
        // Pinch indicator ring
        if (this.isPinching) {
            this.ctx.strokeStyle = '#4ECDC4';
            this.ctx.lineWidth = 3;
            this.ctx.beginPath();
            this.ctx.arc(x, y, 25, 0, Math.PI * 2);
            this.ctx.stroke();
        }
    }
    
    updateStatus(state, text) {
        const statusEl = document.getElementById('hand-status');
        statusEl.className = 'status-indicator ' + state;
        statusEl.querySelector('.status-text').textContent = text;
        
        if (this.onStatusChange) {
            this.onStatusChange(state, text);
        }
    }
    
    getCursorPosition() {
        return this.handDetected ? this.cursorPos : null;
    }
    
    isHandDetected() {
        return this.handDetected;
    }
    
    getPinchEvent() {
        return this.pinchEvent;
    }
}

// Export for use in app.js
window.HandTracker = HandTracker;
