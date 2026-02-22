@echo off
REM Regime-Based Trading App - Windows Setup Script
REM This script sets up the environment and runs the application

setlocal enabledelayedexpansion

echo.
echo ==============================================================================
echo   REGIME-BASED TRADING APP - WINDOWS SETUP
echo ==============================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✅ Python found:
python --version
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ⚠️  Warning: pip upgrade had issues
)
echo.

REM Install basic dependencies
echo Installing required packages...
pip install streamlit plotly pandas numpy yfinance hmmlearn scikit-learn
if errorlevel 1 (
    echo ❌ Failed to install required packages
    pause
    exit /b 1
)
echo ✅ Required packages installed
echo.

REM Optional: Install TA-Lib
echo.
echo TA-Lib is optional but recommended for better performance
echo.
set /p install_talib="Do you want to install TA-Lib? (y/n): "
if /i "!install_talib!"=="y" (
    echo Installing TA-Lib...
    pip install TA-Lib
    if errorlevel 1 (
        echo ⚠️  TA-Lib installation failed (this is optional, app will still work)
    ) else (
        echo ✅ TA-Lib installed successfully
    )
) else (
    echo ⓘ TA-Lib skipped - using manual indicator calculations
)
echo.

REM Run setup check
echo Running setup verification...
python setup_check.py
echo.

REM Ask user what to do
echo.
echo ==============================================================================
echo Setup complete! What would you like to do?
echo ==============================================================================
echo 1) Run the Streamlit dashboard (myPortfolioapp.py)
echo 2) Run examples (example.py)
echo 3) Check configuration (config.py)
echo 4) Exit
echo.

set /p choice="Enter your choice (1-4): "

if "!choice!"=="1" (
    echo.
    echo Starting Streamlit dashboard...
    echo The app will open in your browser at http://localhost:8501
    echo.
    streamlit run myPortfolioapp.py
) else if "!choice!"=="2" (
    echo.
    echo Running examples...
    echo.
    python example.py
    pause
) else if "!choice!"=="3" (
    echo.
    echo Configuration details:
    echo.
    python config.py
    pause
) else (
    echo Exiting...
)

endlocal
