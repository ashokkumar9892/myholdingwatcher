# INSTALLATION GUIDE - Complete Instructions

## System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: 4 GB minimum (8 GB recommended)
- **Disk Space**: 500 MB for code + dependencies
- **Internet**: Required for data download (yfinance)

---

## Installation Methods

### Method 1: Automated Setup (RECOMMENDED)

#### Windows
1. Right-click `setup_windows.bat`
2. Select "Run as administrator"
3. Follow the on-screen prompts
4. The script will:
   - Create a virtual environment
   - Install all dependencies
   - Verify the installation
   - Offer to run the app

#### macOS/Linux
1. Open Terminal
2. Navigate to the project folder:
   ```bash
   cd /path/to/EtradeMyPortfolioClaudeAI
   ```
3. Make the script executable:
   ```bash
   chmod +x setup_linux_mac.sh
   ```
4. Run it:
   ```bash
   ./setup_linux_mac.sh
   ```
5. Follow the on-screen prompts

---

### Method 2: Manual Setup

#### Step 1: Create Virtual Environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 2: Upgrade pip

**Windows:**
```cmd
python -m pip install --upgrade pip
```

**macOS/Linux:**
```bash
python3 -m pip install --upgrade pip
```

#### Step 3: Install Core Dependencies

```bash
pip install streamlit plotly pandas numpy yfinance hmmlearn scikit-learn
```

#### Step 4: Optional - Install TA-Lib

**Windows:**
```cmd
pip install TA-Lib
```

If that fails, download a pre-compiled wheel from:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib

Then install it:
```cmd
pip install TA-Lib‑0.4.28‑cp311‑cp311‑win_amd64.whl
```

**macOS:**
```bash
brew install ta-lib
pip install TA-Lib
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install build-essential wget
cd /tmp
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib
./configure --prefix=/usr
make
sudo make install
cd /tmp
rm -rf ta-lib ta-lib-0.4.0-src.tar.gz
pip install TA-Lib
```

**Linux (CentOS/RHEL):**
```bash
sudo yum install gcc gcc-c++ autoconf automake wget
cd /tmp
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib
./configure --prefix=/usr
make
sudo make install
cd /tmp
rm -rf ta-lib ta-lib-0.4.0-src.tar.gz
pip install TA-Lib
```

---

## Verification

After installation, verify everything is working:

```bash
python setup_check.py
```

You should see:
```
✅ Python version compatible
✅ All required packages installed
✅ All project files present
✅ All modules can be imported
```

Run the test suite:
```bash
python test_suite.py
```

You should see 80%+ tests passing.

---

## Running the App

### Option 1: Using Automated Script
- Windows: Run `setup_windows.bat` and select option 1
- macOS/Linux: Run `./setup_linux_mac.sh` and select option 1

### Option 2: Manual Command
```bash
streamlit run myPortfolioapp.py
```

The app will automatically open in your browser at:
```
http://localhost:8501
```

---

## Troubleshooting Installation

### "Python not found"
- Install Python 3.8+: https://www.python.org/downloads/
- Windows: Check "Add Python to PATH" during installation
- Then restart your terminal

### "pip: command not found"
- Reinstall Python with pip included
- Or use: `python -m pip install ...`

### "Permission denied" (macOS/Linux)
- Make script executable: `chmod +x setup_linux_mac.sh`
- Or use: `bash setup_linux_mac.sh`

### "hmmlearn not found"
```bash
pip install --upgrade hmmlearn
```

### "pandas/numpy not found"
```bash
pip install --upgrade pandas numpy
```

### "TA-Lib installation fails"
- It's OPTIONAL - the app works without it
- Skip installation and use manual indicators
- If you must install it, download pre-compiled wheel

### "Virtual environment won't activate"
**Windows:**
```cmd
# Try this
py -m venv venv
venv\Scripts\activate

# Or use this
python -m venv venv
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### "Streamlit not found after installing"
```bash
# Verify it's installed
pip show streamlit

# If not listed, reinstall
pip install --force-reinstall streamlit

# Or run with python module
python -m streamlit run myPortfolioapp.py
```

---

## Post-Installation

1. **Run Setup Check**
   ```bash
   python setup_check.py
   ```

2. **Run Tests**
   ```bash
   python test_suite.py
   ```

3. **View Configuration**
   ```bash
   python config.py
   ```

4. **Run Examples**
   ```bash
   python example.py
   ```

5. **Start Dashboard**
   ```bash
   streamlit run myPortfolioapp.py
   ```

---

## Virtual Environment Management

### Activate Environment

**Windows:**
```cmd
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Deactivate Environment

**Windows/macOS/Linux:**
```bash
deactivate
```

### Delete Environment
```bash
# Windows
rmdir /s venv

# macOS/Linux
rm -rf venv
```

---

## Package Versions

**Required packages:**
- streamlit >= 1.28.0
- plotly >= 5.17.0
- pandas >= 2.0.0
- numpy >= 1.24.0
- yfinance >= 0.2.32
- hmmlearn >= 0.3.0
- scikit-learn >= 1.3.0

**Optional packages:**
- ta-lib >= 0.4.28 (recommended, not required)

---

## Dependency Explanations

| Package | Purpose | Why Needed |
|---------|---------|-----------|
| streamlit | Dashboard UI | Interactive web interface |
| plotly | Charts/Plots | Interactive candlestick charts |
| pandas | Data frames | Working with OHLCV data |
| numpy | Numerical arrays | Scientific computations |
| yfinance | Data source | Downloading historical price data |
| hmmlearn | HMM model | Hidden Markov Model implementation |
| scikit-learn | Machine learning | Feature scaling and utilities |
| ta-lib | Technical indicators | Faster indicator calculations |

---

## Network Requirements

The app requires internet access to:
- ✅ Download historical price data from Yahoo Finance
- ✅ Check for package updates (optional)
- ✅ Render Streamlit cloud (optional)

No data is sent to external servers except to Yahoo Finance for data download.

---

## Uninstallation

To completely remove the app:

```bash
# Windows
cd d:\Ashok\ETrade
rmdir /s EtradeMyPortfolioClaudeAI
rmdir /s venv

# macOS/Linux
cd ~
rm -rf EtradeMyPortfolioClaudeAI
rm -rf venv
```

To remove just the virtual environment:
```bash
# Keep the code, delete only venv
rmdir /s venv  # Windows
rm -rf venv    # macOS/Linux
```

---

## Support Resources

1. **Quick Start**: See QUICKSTART.md
2. **Full Documentation**: See README.md
3. **Technical Details**: See PROJECT_SUMMARY.md
4. **Verification**: Run `setup_check.py`
5. **Examples**: Run `python example.py`

---

## Next Steps After Installation

1. ✅ Verify installation with `python setup_check.py`
2. ✅ Run tests with `python test_suite.py`
3. ✅ Review QUICKSTART.md for first usage
4. ✅ Start the app with `streamlit run myPortfolioapp.py`
5. ✅ Test with a popular ticker (AAPL, MSFT, GOOGL)
6. ✅ Review documentation while app loads

---

## Last Resort: Fresh Installation

If everything fails, try a complete fresh installation:

```bash
# 1. Remove everything
rmdir /s venv  # Windows: rmdir /s venv
rm -rf venv    # macOS/Linux

# 2. Create new virtual environment
python -m venv venv

# 3. Activate it
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Install core packages
pip install streamlit plotly pandas numpy yfinance hmmlearn scikit-learn

# 6. Verify
python setup_check.py

# 7. Run
streamlit run myPortfolioapp.py
```

---

**Installation Last Updated**: February 2024
**Compatible Python Versions**: 3.8, 3.9, 3.10, 3.11, 3.12
**Supported Operating Systems**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+, CentOS 7+)
