@echo off
echo ==========================================
echo AirMenu Setup Script
echo ==========================================
echo.
echo Checking Python version...
python --version
echo.

echo Checking Python architecture...
python -c "import struct; print(f'{struct.calcsize(\"P\") * 8}-bit Python')"
echo.

echo Installing AirMenu dependencies...
echo This may take a few minutes...
echo.
pip install -r requirements.txt

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo To run AirMenu with hand tracking:
echo   python main.py
echo.
echo To run AirMenu with mouse demo:
echo   python demo_mouse.py
echo.
pause
