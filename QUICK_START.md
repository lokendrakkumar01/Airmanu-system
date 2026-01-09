# AirMenu Quick Start Guide

## Step 1: Install Python 3.11 (64-bit)

### Download
1. **Browser opened**: The Python downloads page should be open in your browser
2. **Look for**: "Download Python 3.11.x" button (the latest 3.11 version)
3. **IMPORTANT**: Download the **Windows installer (64-bit)** - usually labeled as:
   - `Windows installer (64-bit)` or
   - `python-3.11.x-amd64.exe`

### Install
1. **Run** the downloaded installer (`python-3.11.x-amd64.exe`)
2. **✅ CRITICAL**: Check the box "Add Python 3.11 to PATH"
3. Click **"Install Now"**
4. Wait for installation to complete
5. Click **"Close"**

## Step 2: Verify Installation

Open a **NEW** Command Prompt or PowerShell and run:
```bash
python --version
```
Should show: `Python 3.11.x`

```bash
python -c "import struct; print(f'{struct.calcsize(\"P\") * 8}-bit Python')"
```
Should show: `64-bit Python`

## Step 3: Install AirMenu Dependencies

### Option A: Automated (Recommended)
Double-click `setup_airmenu.bat` in the project folder

### Option B: Manual
```bash
cd c:\Users\loken\Downloads\airmnu
pip install -r requirements.txt
```

## Step 4: Run AirMenu

### Hand Tracking Version (Main)
```bash
python main.py
```
- Ensure your **webcam is connected**
- Grant camera permissions if prompted
- Use **hand gestures** to interact with the menu

### Mouse Demo Version
```bash
python demo_mouse.py
```
- Use your **mouse** to click on UI elements
- Good for testing without hand tracking

## Controls

### Hand Tracking Mode (main.py)
- **Hover**: Move your index finger over buttons
- **Click**: Pinch gesture (thumb + index finger)
- **Dwell**: Hold finger over button for 2 seconds
- **Exit**: Press ESC key

### Mouse Mode (demo_mouse.py)
- **Click**: Regular mouse left-click
- **Exit**: Press ESC key

## Troubleshooting

### "No module named 'cv2'" or similar
Run: `pip install -r requirements.txt`

### Camera not detected
- Check if webcam is connected
- Close other apps using the camera
- Check camera permissions in Windows Settings

### Still showing Python 3.15
- Close and reopen terminal
- Or use: `py -3.11 main.py`

---

**Need Help?** Check `INSTALLATION_GUIDE.md` for detailed troubleshooting
