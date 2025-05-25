@echo off
setlocal enabledelayedexpansion

echo 🚀 Setting up Sodh - Solana Dashboard Helper
echo ====================================

:: Check if Python 3.8+ is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python is not installed or not in PATH. Please install Python 3.8 or higher.
    exit /b 1
)

for /f "tokens=2" %%a in ('python -c "import sys; print('.'.join(map(str, sys.version_info[:2])))"') do set PYTHON_VERSION=%%a
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    if %%a LSS 3 (
        echo ❌ Python 3.8 or higher is required. Found Python %PYTHON_VERSION%
        exit /b 1
    )
    if %%a EQU 3 if %%b LSS 8 (
        echo ❌ Python 3.8 or higher is required. Found Python %PYTHON_VERSION%
        exit /b 1
    )
)

echo ✅ Found Python %PYTHON_VERSION%

:: Check if pip is installed
python -m pip --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ pip is not installed. Please install pip first.
    exit /b 1
)

for /f "tokens=2" %%a in ('python -m pip --version ^| findstr /i "pip"') do set PIP_VERSION=%%a
echo ✅ Found pip !PIP_VERSION!

:: Create virtual environment
echo.
echo 🔧 Setting up virtual environment...
if not exist "venv" (
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Using existing virtual environment
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Upgrade pip
echo.
echo 🔄 Upgrading pip...
python -m pip install --upgrade pip

:: Install Poetry
echo.
echo 📦 Installing Poetry...
python -m pip install --user poetry
set PATH=%APPDATA%\Python\Scripts;%PATH%

:: Install project dependencies
echo.
echo 📦 Installing project dependencies...
poetry install --no-interaction --no-ansi

:: Set up pre-commit hooks
echo.
echo 🔧 Setting up pre-commit hooks...
poetry run pre-commit install

:: Create .env file if it doesn't exist
if not exist ".env" (
    echo.
    echo 📝 Creating .env file from .env.example...
    copy /y .env.example .env >nul
    echo ✅ .env file created. Please update it with your configuration.
) else (
    echo.
    echo ✅ .env file already exists
)

echo.
echo ✨ Setup complete! ✨
echo.
echo To activate the virtual environment, run:
echo    call venv\Scripts\activate.bat
echo.
echo To run the application, use:
echo    poetry run streamlit run sodh\app.py
echo.
echo Or with Docker:
echo    docker-compose up --build

exit /b 0
