@echo off
pushd "%~dp0"

if exist "venv\Scripts\streamlit.exe" (
    set "STREAMLIT=venv\Scripts\streamlit.exe"
) else if exist "venv\bin\streamlit.exe" (
    set "STREAMLIT=venv\bin\streamlit.exe"
) else (
    echo [ERROR] Virtual environment not found. Run install.bat first.
    pause
    exit /b 1
)

echo Starting ISO 14122-3 Stair Calculator...
echo.

%STREAMLIT% run stair.py

echo.
echo Streamlit exited. Check the output above for details.
pause
popd
