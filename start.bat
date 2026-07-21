@echo off
echo Starting ISO 14122-3 Stair Calculator...
echo.

if not exist venv\Scripts\activate.bat (
    echo Virtual environment not found. Run install.bat first.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
streamlit run stair.py --server.headless true
