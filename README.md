# Regime-Based Trading App

A professional trading platform built with Python, leveraging Hidden Markov Models for market regime detection and a sophisticated 8-factor confirmation system.

## Features

### 🤖 Core Engine
- **HMM (Hidden Markov Model)**: 7-component GaussianHMM for automatic market regime detection
- **Smart State Identification**: Auto-identifies Bull Run and Bear/Crash states based on returns
- **Training Features**:
  - Log Returns
  - Range (High - Low / Close)
  - Volume Volatility

### 📊 Strategy Logic
- **Voting System**: 8 confirmations required for trade entry
- **Entry Conditions** (need 7 out of 8):
  1. RSI < 90
  2. Momentum > 1%
  3. Volatility < 6%
  4. Volume > 20-period SMA
  5. ADX > 25
  6. Price > EMA 50
  7. Price > EMA 200
  8. MACD > Signal Line

### 🛡️ Risk Management
- **Regime-Based Entry**: Trade ONLY when HMM detects Bull regime
- **Automatic Exit**: Closes positions immediately on regime flip to Bear/Crash
- **48-Hour Cooldown**: Prevents re-entry after any exit to avoid chop
- **2.5× Leverage**: Simulated in PnL calculations

### 📈 Dashboard Features
- Interactive Plotly candlestick charts with regime color coding
- Real-time signals (LONG/CASH)
- Comprehensive performance metrics:
  - Total Return & Alpha vs Buy & Hold
  - Win Rate
  - Max Drawdown
  - Trade history log
- Regime distribution analysis

## Architecture

### Modules

1. **data_loader.py**
   - Fetches hourly OHLCV data via yfinance
   - Loads 730 days of historical data
   - Supports 28 pre-configured stocks
   - Calculates HMM training features

2. **hmm_engine.py**
   - RegimeDetector class with GaussianHMM
   - 7-component regime detection
   - Automatic Bull/Bear state identification
   - Regime probability calculations

3. **indicators.py**
   - Technical indicators: RSI, MACD, ADX, EMA, SMA
   - Volume metrics
   - Momentum and volatility calculations
   - Uses TA-Lib for performance

4. **myPortfoliobacktester.py**
   - TradeLogger for comprehensive trade logging
   - RegimeBasedBacktester class
   - Entry/exit logic implementation
   - Performance metrics calculation
   - Risk management (cooldown, leverage)

5. **myPortfolioapp.py**
   - Streamlit dashboard
   - Interactive UI controls
   - Real-time chart visualization
   - Performance metrics display
   - Trade analysis tools

## Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Quick Setup (Recommended for Windows Users)

**Option 1: Automated Setup Script (Windows)**
1. Extract the project folder
2. Right-click `setup_windows.bat` → "Run as administrator"
3. Follow the prompts
4. Choose to run the dashboard or examples

**Option 2: Automated Setup Script (macOS/Linux)**
1. Extract the project folder
2. Open Terminal and navigate to the folder:
   ```bash
   cd path/to/EtradeMyPortfolioClaudeAI
   ```
3. Make the script executable and run it:
   ```bash
   chmod +x setup_linux_mac.sh
   ./setup_linux_mac.sh
   ```
4. Follow the prompts

### Manual Setup

1. **Navigate to project folder**
   ```bash
   cd d:\Ashok\ETrade\EtradeMyPortfolioClaudeAI
   # or on macOS/Linux:
   cd path/to/EtradeMyPortfolioClaudeAI
   ```

2. **Create virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **(Optional) Install TA-Lib for better performance**
   
   **Windows:**
   ```bash
   pip install TA-Lib
   ```
   If this fails, download pre-compiled wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib)
   
   **macOS:**
   ```bash
   brew install ta-lib
   pip install TA-Lib
   ```
   
   **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt-get install build-essential wget
   wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
   tar -xzf ta-lib-0.4.0-src.tar.gz
   cd ta-lib
   ./configure --prefix=/usr
   make
   sudo make install
   cd ..
   pip install TA-Lib
   ```
   
   **Note:** If TA-Lib installation fails, the app will work fine using built-in manual calculations.

5. **Verify installation**
   ```bash
   # Windows
   python setup_check.py
   
   # macOS/Linux
   python3 setup_check.py
   ```

## Usage

### Run the Streamlit Dashboard

**After setup, run the app with:**

```bash
streamlit run myPortfolioapp.py
```

The app will automatically open in your browser at `http://localhost:8501`

**Or use the setup script to run it:**
- **Windows:** Double-click `setup_windows.bat` and select option 1
- **macOS/Linux:** Run `./setup_linux_mac.sh` and select option 1

### Using the Dashboard

1. **Select Configuration**:
   - Choose a ticker from the dropdown (supports 28+ stocks)
   - Set historical data period (30-730 days)
   - Adjust initial capital ($100-$100,000)
   - Configure leverage multiplier (1.0-10.0)

2. **Run Backtest**:
   - Click "🚀 Run Backtest" button
   - Wait for model training and simulation (typically 2-5 minutes)

3. **View Results**:
   - See current regime and signal
   - Analyze interactive candlestick chart with regime coloring
   - Review comprehensive performance metrics
   - Examine detailed trade log with entry/exit prices and reasons

### Running Examples Programmatically

To see example usage of the API:

```bash
# Windows
python example.py

# macOS/Linux
python3 example.py
```

This will run backtests on sample tickers and show regime analysis.

## Configuration

### Default Parameters

- **Initial Capital**: $2,000
- **Leverage**: 2.5×
- **Historical Data**: Last 730 days
- **Timeframe**: Hourly (1H)
- **HMM Components**: 7 states
- **Cooldown**: 48 hours

### Stock List

**28 Supported Tickers**:
ABVX, AAP, ADMA, AGEN, CELC, CNC, CONI, DAVE, FIVN, GLUE, LUMN, LWAY, MGPI, NNNN, NVCR, NVDL, ODD, PEGA, QURE, RXO, SBUX, SERV, SOGP, TIL, TREE, UPST, WLDN, ZEPP

Plus popular stocks: AAPL, MSFT, GOOGL, TSLA, NVDA, META, AMD, etc.

## Backtest Metrics Explained

### Performance Metrics
- **Total Return %**: Overall profit/loss as percentage of initial capital
- **Alpha**: Excess return vs Buy & Hold strategy
- **Win Rate %**: Percentage of profitable trades

### Risk Metrics
- **Max Drawdown %**: Largest peak-to-trough decline
- **Number of Trades**: Total round-trip trades executed

### Regime Colors
- 🟢 **Green (Bull)**: Positive return regime, favorable for trades
- 🔴 **Red (Bear)**: Low/negative return regime, positions auto-exit
- 🟠 **Orange (Neutral)**: Intermediate market regime

## Backtesting Logic

```
For Each Hour:
  1. Calculate all 8 conditions
  2. Predict current regime using HMM
  
  IF Position Open:
    - Monitor regime flip to Bear
    - Close position if regime changes
    - Start 48-hour cooldown
  
  IF Position Closed AND Outside Cooldown:
    - Check if Regime = BULL
    - Count conditions met (need 7/8)
    - Enter on confirmation
    - Calculate position size with leverage
  
  Update equity and metrics
```

## Technical Details

### HMM Training
- Features: [Returns, Range, Volume_Volatility]
- Normalizes features using StandardScaler
- Auto-identifies Bull state (max return mean)
- Auto-identifies Bear state (min return mean)

### Entry Rules (Logic AND)
```python
if (regime == 'Bull' AND 
    conditions_met >= 7 AND 
    no_active_position AND 
    outside_cooldown):
    entry_trade()
```

### Exit Rules
```python
if regime in ['Bear', 'Crash']:
    exit_trade()
    start_48h_cooldown()
```

## Troubleshooting

### Common Issues

**"No data found for ticker"**
- Ticker may be invalid or delisted
- Try a different ticker from the supported list
- Use only market hours (US market)

**"TA-Lib installation failed"**
- Use conda: `conda install -c conda-forge ta-lib`
- Or install pre-compiled wheel for your Python version

**"Insufficient data"**
- Increase historical data days in sidebar
- Use tickers with sufficient trading history

**"Module not found" errors**
- Ensure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt --force-reinstall`

## Performance Notes

- **Data Loading**: 1-2 minutes for 730 days hourly data
- **HMM Training**: 30-60 seconds depending on data size
- **Backtest Simulation**: 2-5 minutes for full year of hourly data
- **Dashboard**: Real-time updates after calculation

## Customization

### Modify Entry Conditions

Edit `check_entry_conditions()` in `myPortfoliobacktester.py`:

```python
def check_entry_conditions(self, row):
    conditions_met = 0
    
    # Add/modify conditions here
    if row['RSI'] < 80:  # Changed from 90
        conditions_met += 1
    
    return conditions_met
```

### Change HMM Parameters

Edit `RegimeDetector` in `hmm_engine.py`:

```python
regime_detector = RegimeDetector(
    n_components=8,  # Change components
    covariance_type='full',  # Change type
    n_iter=2000  # More iterations
)
```

### Adjust Risk Management

Edit `RegimeBasedBacktester.__init__()`:

```python
self.leverage = 3.0  # Increase leverage
self.cooldown_hours = 24  # Reduce cooldown
```

## File Structure

```
EtradeMyPortfolioClaudeAI/
├── data_loader.py              # Data fetching and feature engineering
├── hmm_engine.py               # HMM regime detection engine
├── indicators.py               # Technical indicators calculations
├── myPortfoliobacktester.py    # Backtesting engine and logic
├── myPortfolioapp.py           # Streamlit dashboard
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Disclaimer

This is an educational/research tool. Past performance does not guarantee future results. Use at your own risk. Not financial advice.

## License

Proprietary - Etrade Portfolio Analysis

## Support

For issues, questions, or feature requests, please review the code documentation or refer to the module docstrings.

---

**Built with** 🐍 Python, 🤖 HMM, 📊 Streamlit, 📈 Plotly
