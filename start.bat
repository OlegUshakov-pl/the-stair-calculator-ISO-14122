@echo off
cd /d "%~dp0"
call venv\Scripts\activate
streamlit run stair.py --server.headless true
pause
