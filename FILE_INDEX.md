# File Index & Documentation Map

## 📋 Complete File Structure

### Core Application Files (14 files)

```
EtradeMyPortfolioClaudeAI/
│
├─ 🔧 CORE MODULES (5 files)
│  ├─ data_loader.py              [~400 lines] Data fetching & feature engineering
│  ├─ indicators.py               [~200 lines] Technical indicators (RSI, MACD, ADX, etc.)
│  ├─ hmm_engine.py               [~250 lines] HMM regime detection engine
│  ├─ myPortfoliobacktester.py    [~400 lines] Backtesting engine with trading logic
│  └─ config.py                   [~250 lines] Centralized configuration
│
├─ 💻 APPLICATION (1 file)
│  └─ myPortfolioapp.py           [~350 lines] Streamlit dashboard (main UI)
│
├─ 🛠️ SETUP & UTILITIES (4 files)
│  ├─ setup_windows.bat           Automated setup for Windows
│  ├─ setup_linux_mac.sh          Automated setup for macOS/Linux
│  ├─ setup_check.py              [~200 lines] Installation verification
│  ├─ test_suite.py               [~350 lines] Comprehensive test suite
│  └─ example.py                  [~200 lines] Usage examples
│
└─ 📚 DOCUMENTATION (8 files)
   ├─ README.md                   [~300 lines] Full documentation
   ├─ QUICKSTART.md               [~200 lines] 5-minute quick start
   ├─ INSTALLATION.md             [~400 lines] Complete installation guide
   ├─ PROJECT_SUMMARY.md          [~600 lines] Technical architecture
   ├─ FILE_INDEX.md               This file
   ├─ requirements.txt            Python package dependencies
   ├─ .gitignore                  Git ignore rules
   └─ __init__.py                 Package initialization
```

**Total**: ~3,500 lines of Python code + ~1,500 lines of documentation

---

## 📚 Documentation Guide

### For First-Time Users
1. **START HERE**: [QUICKSTART.md](QUICKSTART.md)
   - 5-minute setup and first run
   - Fastest way to get started

2. **THEN READ**: [INSTALLATION.md](INSTALLATION.md)
   - Detailed setup instructions
   - Troubleshooting guide
   - All operating systems covered

3. **BEFORE TRADING**: [README.md](README.md)
   - Full documentation
   - Strategy explanation
   - Configuration guide

### For Developers & Researchers
1. **Architecture**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
   - Technical details
   - Algorithm explanations
   - Performance expectations

2. **Code Examples**: [example.py](example.py)
   - How to use modules programmatically
   - API usage patterns

3. **Configuration**: [config.py](config.py)
   - All tunable parameters
   - What each parameter does

### For Troubleshooting
1. **Setup Issues**: [INSTALLATION.md](INSTALLATION.md) → Troubleshooting section
2. **Runtime Issues**: [README.md](README.md) → Troubleshooting Guide
3. **Verification**: Run `python setup_check.py`
4. **Testing**: Run `python test_suite.py`

---

## 🔍 File Descriptions

### Core Modules

#### `data_loader.py` (Data Management)
**Purpose**: Fetch and process financial data
**Key Functions**:
- `fetch_hourly_data()` - Download hourly OHLCV from yfinance
- `calculate_features()` - Calculate HMM training features
- `get_training_features()` - Extract feature matrix

**Dependencies**: yfinance, pandas, numpy
**Supported**: 28+ stocks, 730-day history, hourly interval

---

#### `hmm_engine.py` (Regime Detection)
**Purpose**: Hidden Markov Model for market regime detection
**Key Classes**:
- `RegimeDetector` - 7-component GaussianHMM
  - `train()` - Train on historical features
  - `predict_regime()` - Predict states
  - `get_current_regime()` - Get current market regime

**Regimes Identified**:
- Bull: Highest positive returns
- Bear: Lowest returns
- Neutral: 5 Other states

**Dependencies**: hmmlearn, scikit-learn, numpy, pandas

---

#### `indicators.py` (Technical Indicators)
**Purpose**: Calculate technical indicators for trading signals
**Indicators Implemented**:
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- ADX (Average Directional Index)
- EMA/SMA (Moving Averages)
- Momentum
- Volatility

**Fallback**: Manual implementations if TA-Lib not installed

**Dependencies**: pandas, numpy, [optional: talib]

---

#### `myPortfoliobacktester.py` (Backtesting Engine)
**Purpose**: Simulate trading strategy on historical data
**Key Classes**:
- `TradeLogger` - Log all trades and metrics
- `RegimeBasedBacktester` - Main backtesting engine
  - `check_entry_conditions()` - Verify 8 conditions
  - `should_enter()` - Check entry criteria
  - `should_exit()` - Check exit criteria
  - `run_backtest()` - Execute backtest simulation

**Logic**:
- Entry: Regime=Bull AND 7/8 conditions AND outside cooldown
- Exit: Regime flips to Bear/Crash
- Cooldown: 48 hours mandatory after exit

**Dependencies**: data_loader, indicators, hmm_engine, pandas, numpy

---

#### `config.py` (Configuration)
**Purpose**: Centralized configuration management
**Key Settings**:
- HMM_COMPONENTS = 7
- MIN_CONDITIONS_FOR_ENTRY = 7
- DEFAULT_LEVERAGE = 2.5
- COOLDOWN_HOURS = 48
- 36 stock list (28 primary + 8 popular)

**Functions**:
- `validate_config()` - Check parameter validity
- `print_config()` - Display current settings
- `get_stock_list()` - Get all available stocks

---

### Application

#### `myPortfolioapp.py` (Streamlit Dashboard)
**Purpose**: Interactive web-based trading dashboard
**Sections**:
- **Configuration Panel** (Sidebar)
  - Stock selection
  - Historical data period
  - Capital & leverage settings

- **Results Display**
  - Current regime & signal
  - Interactive candlestick chart
  - Performance metrics
  - Trade log
  - Regime distribution

**Features**:
- Real-time regime coloring (Green=Bull, Red=Bear)
- Interactive Plotly charts
- Automatic model training
- Backtesting engine integration

**Dependencies**: streamlit, plotly, pandas, yfinance, all core modules

---

### Setup & Utilities

#### `setup_windows.bat` (Windows Setup)
**Purpose**: Automated environment setup for Windows
**Actions**:
1. Check Python installation
2. Create virtual environment
3. Activate venv
4. Install dependencies
5. Optional: Install TA-Lib
6. Run verification
7. Offer to start app

**Usage**: Double-click the file

---

#### `setup_linux_mac.sh` (macOS/Linux Setup)
**Purpose**: Automated environment setup for Unix-like systems
**Actions**:
1. Check Python 3
2. Create virtual environment
3. Activate venv
4. Install dependencies
5. Optional: Install TA-Lib (with system dependencies)
6. Run verification
7. Offer to start app

**Usage**: `chmod +x setup_linux_mac.sh && ./setup_linux_mac.sh`

---

#### `setup_check.py` (Installation Verification)
**Purpose**: Verify installation correctness
**Checks**:
- Python version >= 3.8
- All required packages
- All project files
- Module imports

**Usage**: `python setup_check.py`

---

#### `test_suite.py` (Automated Testing)
**Purpose**: Comprehensive test coverage
**Tests**:
1. Module imports
2. Configuration validation
3. Data loader functions
4. HMM engine
5. Technical indicators
6. Backtester logic

**Usage**: `python test_suite.py`

**Expected**: 80%+ tests passing

---

#### `example.py` (Code Examples)
**Purpose**: Show how to use the API
**Examples**:
1. Single ticker backtest
2. Multi-ticker comparison
3. HMM regime analysis

**Usage**: `python example.py`

---

### Configuration Files

#### `requirements.txt`
**Purpose**: Python package dependencies
**Packages**:
- streamlit (UI)
- plotly (Charts)
- pandas (Data)
- numpy (Math)
- yfinance (Data source)
- hmmlearn (ML)
- scikit-learn (ML)
- [Optional] ta-lib (Indicators)

**Usage**: `pip install -r requirements.txt`

---

#### `.gitignore`
**Purpose**: Specify files to ignore in Git
**Ignores**:
- Python cache (`__pycache__`, `.pyc`)
- Virtual environments (`venv/`)
- IDE files (`.vscode/`, `.idea/`)
- Data files (`.csv`, `.pkl`)
- OS files (`Thumbs.db`, `.DS_Store`)

---

---

## 🚀 Quick Reference

### Installation
```bash
# Windows
setup_windows.bat

# macOS/Linux
chmod +x setup_linux_mac.sh
./setup_linux_mac.sh
```

### Running the App
```bash
streamlit run myPortfolioapp.py
```

### Verification
```bash
python setup_check.py
python test_suite.py
```

### Examples
```bash
python example.py
```

### Configuration
```bash
python config.py
```

---

## 📊 Architecture Diagram

```
User Interface
    ↓
    └─→ myPortfolioapp.py (Streamlit Dashboard)
        ├─→ Sidebar: Configuration
        ├─→ Main: Results Display
        └─→ Charts: Plotly Visualizations
            ↓
Trading Engine
    └─→ myPortfoliobacktester.py (Backtesting)
        ├─→ Entry Logic (8 conditions)
        ├─→ Exit Logic (Regime flip)
        ├─→ Position Management
        └─→ Trade Logging
            ↓
Market Regime Detector
    └─→ hmm_engine.py (HMM Model)
        ├─→ Train on 3 features
        ├─→ Predict regimes
        └─→ Identify Bull/Bear states
            ↓
Technical Analysis
    ├─→ indicators.py (8+ Indicators)
    │   ├─→ RSI, MACD, ADX
    │   ├─→ EMA50/200, Momentum
    │   └─→ Volatility, Volume
    └─→ data_loader.py (Feature Engineering)
        └─→ Returns, Range, Vol Volatility
            ↓
Data Pipeline
    └─→ yfinance (OHLCV Data)
        └─→ 28+ Stocks, 730-day history
```

---

## 📈 Data Flow

```
1. DATA FETCHING
   Stock Symbol → yfinance → OHLCV Data (8,760 bars)

2. FEATURE ENGINEERING
   OHLCV → Calculate Features → [Returns, Range, VolVolatility]

3. HMM TRAINING
   Features → Standardize → Train 7-component HMM → Model

4. TECHNICAL INDICATORS
   OHLCV → Calculate 8+ Indicators → Indicator DataFrame

5. REGIME PREDICTION
   Features → HMM Model → Regime Timeseries

6. BACKTESTING
   Regimes, Indicators, Historical Prices → Trading Logic → Trades

7. METRICS CALCULATION
   Trades → Calculate Returns, Win Rate, Drawdown, etc.

8. VISUALIZATION
   Results → Plotly Charts → Streamlit Dashboard
```

---

## 🔄 Trading Loop (Per Hour)

```
For each hourly bar:

1. Get current prices & indicators
2. Predict current regime
3. Count conditions met (0-8)
4. If position open:
   - Check if regime changed to Bear
   - If yes: Close position, start cooldown
5. If position closed and outside cooldown:
   - If regime == Bull AND conditions >= 7:
     - Open position, calculate size
6. Update equity and log metrics
```

---

## 📖 Learning Path

**Beginner** (0-1 hour)
1. Read QUICKSTART.md
2. Run setup script
3. Try first backtest
4. Review results

**Intermediate** (1-2 hours)
1. Read README.md fully
2. Run example.py
3. Try different parameters
4. Review trade logs

**Advanced** (2+ hours)
1. Study PROJECT_SUMMARY.md
2. Review hmm_engine.py code
3. Modify entry conditions
4. Understand HMM logic

**Expert** (Research-level)
1. Study academic HMM papers
2. Modify HMM components
3. Add new indicators
4. Implement machine learning

---

## ✅ Validation Checklist

After installation:
- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] setup_check.py passes
- [ ] test_suite.py passes 80%+
- [ ] App starts with `streamlit run myPortfolioapp.py`
- [ ] Dashboard loads in browser
- [ ] First backtest completes successfully

---

## 📞 Support Resources

| Issue | Solution |
|-------|----------|
| Installation | INSTALLATION.md |
| First run | QUICKSTART.md |
| Understanding | README.md |
| Technical details | PROJECT_SUMMARY.md |
| Code examples | example.py |
| Troubleshooting | INSTALLATION.md troubleshooting section |
| Verification | setup_check.py, test_suite.py |

---

## 📝 Version Information

- **Version**: 1.0.0
- **Release Date**: February 2024
- **Python**: 3.8+
- **Status**: Production Ready
- **Maintenance**: Active

---

**Last Updated**: February 2024
**Total LOC**: ~3,500 (Python) + ~1,500 (Documentation)
**Project Size**: ~43 KB core + dependencies
**Documentation**: Comprehensive (8+ guides)
