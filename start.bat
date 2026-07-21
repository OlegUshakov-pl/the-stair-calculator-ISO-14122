@echo off
pushd "%~dp0"

if not exist "venv\Scripts\streamlit.exe" (
    echo [ERROR] Virtual environment not found. Run install.bat first.
    pause
    exit /b 1
)

echo Starting ISO 14122-3 Stair Calculator...
echo.

venv\Scripts\streamlit.exe run stair.py

echo.
echo Streamlit exited. Check the output above for details.
pause
popd
