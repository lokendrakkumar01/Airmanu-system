@echo off
echo ==========================================
echo Python 3.11 Installation Verification
echo ==========================================
echo.

echo Checking Python version...
python --version
echo.

echo Checking Python architecture...
python -c "import struct; print(f'{struct.calcsize(\"P\") * 8}-bit Python')"
echo.

echo Checking pip...
pip --version
echo.

echo ==========================================
echo.
echo If you see:
echo   - Python 3.11.x
echo   - 64-bit Python
echo   - pip version
echo.
echo Then installation is SUCCESSFUL!
echo.
echo Next step: Run setup_airmenu.bat
echo ==========================================
echo.
pause
