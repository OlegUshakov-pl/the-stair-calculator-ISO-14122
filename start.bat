@echo off
pushd "%~dp0"
venv\Scripts\streamlit.exe run stair.py --server.headless true
popd
pause
