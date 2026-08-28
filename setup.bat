@echo off
REM DocuVerify-Sec Automated Setup Script for Windows
REM Installs all dependencies and initializes the application

setlocal enabledelayedexpansion

echo.
echo ================================================================
echo   DocuVerify-Sec: Automated Setup ^& Initialization (Windows)
echo ================================================================
echo.

REM Check Python installation
echo [1/6] Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python 3 not found. Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%
echo [OK] Python version check passed
echo.

REM Create virtual environment
echo [2/6] Creating virtual environment...
if exist venv\ (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    echo [OK] Virtual environment created
)
echo.

REM Activate virtual environment
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo [4/6] Upgrading pip...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1
echo [OK] pip upgraded
echo.

REM Install dependencies
echo [5/6] Installing dependencies...
if exist requirements.txt (
    pip install -r requirements.txt
    echo [OK] All dependencies installed
) else (
    echo Error: requirements.txt not found!
    pause
    exit /b 1
)
echo.

REM Create uploads directory
echo [6/6] Setting up directories...
if not exist uploads mkdir uploads
echo [OK] Uploads directory created
echo.

REM Check for Tesseract (optional)
echo [Optional] Checking for Tesseract OCR...
where tesseract >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%i in ('tesseract --version 2^>^&1 ^| findstr /R "tesseract"') do set TESS_VERSION=%%i
    echo [OK] Tesseract found: !TESS_VERSION!
) else (
    echo [WARNING] Tesseract not found - EasyOCR will be used as fallback
    echo To install Tesseract:
    echo   Download from: https://github.com/UB-Mannheim/tesseract/wiki
)
echo.

REM Create .gitignore if it doesn't exist
if not exist .gitignore (
    (
        echo venv/
        echo __pycache__/
        echo *.pyc
        echo .DS_Store
        echo .env
        echo uploads/
        echo *.log
        echo .pytest_cache/
        echo dist/
        echo build/
        echo *.egg-info/
    ) > .gitignore
    echo [OK] .gitignore created
)
echo.

echo ================================================================
echo   SETUP COMPLETE!
echo ================================================================
echo.
echo Next steps:
echo.
echo 1. Start the server:
echo    python app.py
echo.
echo 2. Open your browser:
echo    http://localhost:5000
echo.
echo 3. Upload a document for analysis
echo.
echo To stop the server, press Ctrl+C
echo.
echo For more information, see README.md and QUICKSTART.md
echo.
pause
