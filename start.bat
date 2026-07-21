@echo off
cd /d "%~dp0"
echo Starting Stair Calculator...
call venv\Scripts\activate
streamlit run stair.py --server.headless true
