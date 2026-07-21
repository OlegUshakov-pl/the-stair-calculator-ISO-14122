@echo off
cd /d "%~dp0"
echo Starting ISO 14122-3 Stair Calculator...
echo.
venv\Scripts\streamlit.exe run stair.py --server.headless true
pause
