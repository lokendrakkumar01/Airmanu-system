# AirMenu - Touchless AR Restaurant Menu System

A futuristic touchless restaurant menu system using computer vision and hand tracking. Browse menus, select items, and complete orders using only hand gestures — no physical touch required!

## ✨ Features

- **Touchless Interaction**: Navigate entirely using hand gestures
- **Real-time Hand Tracking**: Powered by Mediapipe for precise fingertip detection
- **Vision Pro-Inspired UI**: Glassmorphism effects with blurred backgrounds, soft shadows, and glowing elements
- **Smooth iOS-Style Transitions**: Cubic-easing animations between screens
- **Complete Ordering Flow**: Browse categories → Select items → Manage cart → View receipt
- **Auto-calculated Billing**: Automatic GST calculation and digital receipt generation
- **Gesture Recognition**: 
  - **Hover**: Move your index finger to navigate
  - **Dwell-to-Select**: Hold cursor over buttons to activate
  - **Pinch-to-Click**: Pinch thumb and index finger for instant selection

## 🎯 System Requirements

- **Python**: 3.8 or higher
- **Webcam**: Any standard USB or built-in camera
- **OS**: Windows, macOS, or Linux

## 🚀 Installation

1. **Clone or download** this repository

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python main.py
```

## 🎮 How to Use

### Gesture Controls

1. **Index Finger Cursor**: Point your index finger at the camera - it becomes your cursor
2. **Hover Selection**: Move cursor over any button and hold for 0.8 seconds to select
3. **Pinch to Click**: Bring thumb and index finger together for instant click
4. **Navigate**: Use the back button (←) to return to previous screens

### Ordering Flow

1. **Home Screen**: Start by selecting "START ORDERING"
2. **Categories**: Choose a category (Starters, Main Course, Desserts, Beverages)
3. **Items List**: Browse items and tap (+) to add to cart
4. **Cart**: Adjust quantities (+/-), view billing summary, and checkout
5. **Receipt**: View digital receipt and start a new order

### Keyboard Shortcuts

- **ESC**: Exit application
- **R**: Reset to home screen

## 📁 Project Structure

```
airmnu/
├── main.py                 # Main application entry point
├── config.py               # Central configuration
├── hand_tracker.py         # Mediapipe hand tracking wrapper
├── cart_manager.py         # Shopping cart logic
├── billing_engine.py       # GST calculation & receipts
├── animation_engine.py     # Cubic easing animations
├── state_manager.py        # Screen state machine
├── utils.py                # Utility functions
├── requirements.txt        # Python dependencies
├── ui_framework/           # Custom OpenCV UI components
│   ├── base_component.py
│   ├── rendering_utils.py  # Glassmorphism effects
│   ├── glass_card.py
│   ├── glass_button.py
│   └── icons.py
├── screens/                # Screen modules
│   ├── base_screen.py
│   ├── home_screen.py
│   ├── category_screen.py
│   ├── items_screen.py
│   ├── cart_screen.py
│   └── receipt_screen.py
└── data/                   # Menu data
    └── menu_data.py
```

## 🎨 Architecture

### State Machine Pattern
Each screen is an independent module with its own rendering pipeline and interaction logic. The `StateManager` handles transitions with smooth animations.

### Custom UI Framework
All UI elements are rendered frame-by-frame using OpenCV primitives:
- **Glassmorphism**: Multi-layer Gaussian blur with alpha blending
- **Glow Effects**: Bloom filters for button highlights
- **Soft Shadows**: Blurred overlays for depth
- **Rounded Corners**: Custom shape rendering

### Hand Tracking Pipeline
1. Mediapipe detects 21 hand landmarks
2. Index fingertip (landmark 8) tracked with exponential moving average
3. Jitter reduction filters out micro-movements
4. Pinch detection via thumb-index distance threshold

## ⚙️ Configuration

Edit `config.py` to customize:
- Screen resolution and FPS target
- Hand tracking sensitivity
- Gesture thresholds (hover distance, dwell time, pinch threshold)
- Color scheme and glassmorphism parameters
- GST rate and currency
- Animation timing

## 🍽️ Menu Customization

Edit `data/menu_data.py` to add/modify menu items:
- Categories with custom icons
- Items with name, description, price, and category
- Currently includes 20 sample items across 4 categories

## 🐛 Troubleshooting

**Camera not detected**:
- Check if camera is available and not used by another application
- Modify `CAMERA_INDEX` in `config.py` (try 0, 1, or 2)

**Low FPS**:
- Close other applications
- Reduce `SCREEN_WIDTH` and `SCREEN_HEIGHT` in `config.py`
- Set `GLASS_BLUR_AMOUNT` to a lower value (must be odd number)

**Hand not detected**:
- Ensure good lighting
- Adjust `HAND_DETECTION_CONFIDENCE` in `config.py`
- Keep hand within camera frame

**Gestures too sensitive/not responsive**:
- Adjust `HOVER_THRESHOLD_PX`, `DWELL_TIME_SECONDS`, or `PINCH_THRESHOLD` in `config.py`
- Increase `INTERACTION_COOLDOWN` to prevent accidental rapid clicks

## 🔮 Future Upgrades

- **3D Food Models**: Floating 3D models using OpenGL
- **Multi-hand Gestures**: Two-handed controls for zoom and rotate
- **Voice Ordering**: Natural language processing integration
- **Eye Gaze Tracking**: Alternative input mode for accessibility
- **Physics-based UI**: Momentum scrolling and spring animations
- **AR Spatial Anchoring**: Persistent menu placement in 3D space
- **Multi-language Support**: Internationalization
- **Restaurant Admin Panel**: Live menu editing

## 📄 License

This project is created for educational and demonstration purposes.

## 🙏 Credits

- **OpenCV**: Computer vision and rendering
- **Mediapipe**: Hand tracking ML model
- **Inspiration**: Apple Vision Pro spatial computing interface

---

**Built with ❤️ for the future of touchless interaction**
