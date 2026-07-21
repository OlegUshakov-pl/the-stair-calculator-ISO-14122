@echo off
echo Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Failed to create virtual environment. Make sure Python is installed.
    pause
    exit /b 1
)

if exist "venv\Scripts\python.exe" (
    set "VENV_PYTHON=venv\Scripts\python.exe"
) else (
    set "VENV_PYTHON=venv\bin\python.exe"
)

echo Installing dependencies...
%VENV_PYTHON% -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo Installation complete! Run start.bat to launch the app.
pause
