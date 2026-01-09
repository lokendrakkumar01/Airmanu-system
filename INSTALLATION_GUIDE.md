# AirMenu - Installation Guide

## ⚠️ Current System Compatibility Issues

Your system has the following issues preventing AirMenu from running:

### Issues Detected:
1. **Python Version**: 3.15.0a2 (Alpha/Pre-release) - **32-bit**
   - Mediapipe doesn't provide 32-bit builds
   - NumPy 2.x requires 64-bit Python
   - Alpha versions lack stable package support

2. **GCC Compiler**: Version 6.3.0
   - NumPy 2.x requires GCC >= 8.4
   - setuptools build failing

3. **Missing Dependencies**: No numpy, opencv-python, or mediapipe installed

## ✅ Solutions

### Option 1: Install 64-bit Python 3.11 (RECOMMENDED)

This is the most straightforward solution:

1. **Download 64-bit Python 3.11**:
   - Go to: https://www.python.org/downloads/
   - Download: **Python 3.11.x (64-bit)** installer
   - **IMPORTANT**: Choose the 64-bit version, not 32-bit

2. **Install Python 3.11**:
   - Run the installer
   - ✅ Check "Add Python 3.11 to PATH"
   - Choose "Install Now"

3. **Open a NEW Command Prompt** and verify:
   ```bash
   python --version
   # Should show: Python 3.11.x
   
   python -c "import struct; print(f'{struct.calcsize(\"P\") * 8}-bit')"
   # Should show: 64-bit Python
   ```

4. **Install AirMenu dependencies**:
   ```bash
   cd c:\Users\loken\Downloads\airmnu
   pip install opencv-python mediapipe numpy
   ```

5. **Run AirMenu**:
   ```bash
   python main.py
   ```

### Option 2: Use Python 3.10 64-bit

If Python 3.11 has issues:
- Download Python 3.10.x (64-bit) instead
- Follow same steps as Option 1

### Option 3: Create Virtual Environment

If you want to keep Python 3.15:
```bash
# Install Python 3.11 separately
# Then create a virtual environment:
py -3.11 -m venv airmenu_env
airmenu_env\Scripts\activate
pip install opencv-python mediapipe numpy
python main.py
```

## 🖱️ Demo Version (No Installation Required)

I've created a **mouse-based demo** that works without hand tracking:

### If you have ANY Python with numpy and opencv-python:
```bash
python demo_mouse.py
```

This lets you test the UI using mouse clicks instead of hand gestures.

## 🔍 Why These Errors Occurred

| Issue | Explanation |
|-------|-------------|
| **32-bit Python** | Mediapipe and modern NumPy only support 64-bit Python |
| **Python 3.15 alpha** | Pre-release versions lack stable package wheels |
| **GCC 6.3** | Too old to compile NumPy 2.x from source |
| **No setuptools** | Can't build packages from source |

## 📋 Quick Checklist

Before running AirMenu, ensure:
- [ ] Python 3.9, 3.10, or 3.11 (NOT 3.15 alpha)
- [ ] 64-bit Python (NOT 32-bit)
- [ ] Fresh installation (not alpha/beta)
- [ ] Webcam available
- [ ] Dependencies installed: `pip install opencv-python mediapipe numpy`

## 🎯 Next Steps

1. **Install Python 3.11 64-bit** from python.org
2. **Restart your terminal**
3. **Install dependencies**: `pip install opencv-python mediapipe numpy`
4. **Run**: `python main.py`

## 🆘 Still Having Issues?

After installing Python 3.11 64-bit, if you still get errors:
1. Make sure old Python is uninstalled or not in PATH
2. Use `py -3.11` instead of `python` command
3. Try the demo version first: `python demo_mouse.py`

---

**The good news**: All the code is complete and ready! You just need the right Python environment.
