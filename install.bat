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

echo Upgrading pip...
%VENV_PYTHON% -m pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org

echo Installing dependencies...
%VENV_PYTHON% -m pip install --prefer-binary -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo Retrying with trusted hosts...
    %VENV_PYTHON% -m pip install --prefer-binary --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
)
if %errorlevel% neq 0 (
    echo Failed to install dependencies. Check your internet connection or SSL certificates.
    pause
    exit /b 1
)

echo.
echo Installation complete! Run start.bat to launch the app.
pause
