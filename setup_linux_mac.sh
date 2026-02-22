#!/bin/bash

# Regime-Based Trading App - macOS/Linux Setup Script
# This script sets up the environment and runs the application

echo ""
echo "=============================================================================="
echo "  REGIME-BASED TRADING APP - macOS/LINUX SETUP"
echo "=============================================================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.8+ using:"
    echo "  macOS: brew install python3"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip python3-venv"
    echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
    exit 1
fi

echo "✅ Python found:"
python3 --version
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "⚠️  Warning: pip upgrade had issues"
fi
echo ""

# Install basic dependencies
echo "Installing required packages..."
pip install streamlit plotly pandas numpy yfinance hmmlearn scikit-learn
if [ $? -ne 0 ]; then
    echo "❌ Failed to install required packages"
    exit 1
fi
echo "✅ Required packages installed"
echo ""

# Optional: Install TA-Lib
echo ""
echo "TA-Lib is optional but recommended for better performance"
echo ""
read -p "Do you want to install TA-Lib? (y/n): " install_talib

if [[ $install_talib == "y" || $install_talib == "Y" ]]; then
    echo "Installing TA-Lib..."
    
    # Install dependencies based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        echo "Installing TA-Lib dependencies for macOS..."
        if ! command -v brew &> /dev/null; then
            echo "Homebrew not found. Please install from https://brew.sh"
        else
            brew install ta-lib
        fi
    else
        # Linux
        echo "Installing TA-Lib dependencies for Linux..."
        # Assuming Ubuntu/Debian
        sudo apt-get install build-essential wget -y 2>/dev/null || \
        sudo yum install gcc gcc-c++ autoconf automake -y 2>/dev/null || \
        echo "Please manually install build tools"
        
        # Download and install TA-Lib
        cd /tmp
        wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz 2>/dev/null
        if [ -f "ta-lib-0.4.0-src.tar.gz" ]; then
            tar -xzf ta-lib-0.4.0-src.tar.gz
            cd ta-lib/
            ./configure --prefix=/usr
            make
            sudo make install
            cd /tmp
            rm -rf ta-lib ta-lib-0.4.0-src.tar.gz
            echo "✅ TA-Lib installed"
        fi
        cd - >/dev/null
    fi
    
    # Install Python binding
    pip install TA-Lib
    if [ $? -eq 0 ]; then
        echo "✅ TA-Lib installed successfully"
    else
        echo "⚠️  TA-Lib installation failed (this is optional, app will still work)"
    fi
else
    echo "ⓘ TA-Lib skipped - using manual indicator calculations"
fi
echo ""

# Run setup check
echo "Running setup verification..."
python setup_check.py
echo ""

# Ask user what to do
echo ""
echo "=============================================================================="
echo "Setup complete! What would you like to do?"
echo "=============================================================================="
echo "1) Run the Streamlit dashboard (myPortfolioapp.py)"
echo "2) Run examples (example.py)"
echo "3) Check configuration (config.py)"
echo "4) Exit"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "Starting Streamlit dashboard..."
        echo "The app will open in your browser at http://localhost:8501"
        echo ""
        streamlit run myPortfolioapp.py
        ;;
    2)
        echo ""
        echo "Running examples..."
        echo ""
        python example.py
        ;;
    3)
        echo ""
        echo "Configuration details:"
        echo ""
        python config.py
        ;;
    4)
        echo "Exiting..."
        ;;
    *)
        echo "Invalid choice"
        ;;
esac
