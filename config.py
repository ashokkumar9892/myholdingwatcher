"""
Configuration Module
Centralized configuration for the Regime-Based Trading App
"""

import json
from pathlib import Path

# ============================================================================
# STRATEGY CONFIGURATION
# ============================================================================

# HMM Model Parameters
HMM_COMPONENTS = 7  # Number of hidden states
HMM_COVARIANCE_TYPE = 'diag'  # 'diag' or 'full'
HMM_N_ITER = 1000  # Training iterations

# Feature Configuration
FEATURES = ['Returns', 'Range', 'Volume_Volatility']
MIN_SAMPLES_FOR_TRAINING = 100

# ============================================================================
# STRATEGY LOGIC CONFIGURATION
# ============================================================================

# Entry Confirmation Conditions
ENTRY_CONDITIONS = {
    'rsi_max': 90,  # RSI < 90
    'momentum_min': 1.0,  # Momentum > 1%
    'volatility_max': 6.0,  # Volatility < 6%
    'volume_multiplier': 1.0,  # Volume > SMA
    'adx_min': 25,  # ADX > 25
    'ema50': True,  # Price > EMA50
    'ema200': True,  # Price > EMA200
    'macd': True,  # MACD > Signal
}

# Required confirmations (out of 8)
MIN_CONDITIONS_FOR_ENTRY = 7

# ============================================================================
# RISK MANAGEMENT CONFIGURATION
# ============================================================================

# Default backtesting parameters
DEFAULT_INITIAL_CAPITAL = 2000  # USD
DEFAULT_LEVERAGE = 2.5  # Leverage multiplier
COOLDOWN_HOURS = 48  # Hours before re-entry after exit

# ============================================================================
# DATA CONFIGURATION
# ============================================================================

# Stock list (28 micro-cap and small-cap stocks)
STOCK_LIST = [
    'ABVX', 'AAP', 'ADMA', 'AGEN', 'CELC', 'CNC', 'CONI', 'DAVE', 'FIVN', 'GLUE',
    'LUMN', 'LWAY', 'MGPI', 'NNNN', 'NVCR', 'NVDL', 'ODD', 'PEGA', 'QURE', 'RXO',
    'SBUX', 'SERV', 'SOGP', 'TIL', 'TREE', 'UPST', 'WLDN', 'ZEPP'
]

# Additional popular stocks for testing
POPULAR_STOCKS = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA', 'META', 'AMD', 'AZURE']

# All available stocks
ALL_STOCKS = sorted(STOCK_LIST + POPULAR_STOCKS)

# Data fetching parameters
DATA_INTERVALS = ['1h', '1d', '15m', '5m']  # Available intervals
DEFAULT_INTERVAL = '1h'  # Hourly
DEFAULT_HISTORY_DAYS = 730  # 2 years
MAX_HISTORY_DAYS = 730  # Maximum allowed

# ============================================================================
# TECHNICAL INDICATORS CONFIGURATION
# ============================================================================

# RSI
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# MACD
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# ADX
ADX_PERIOD = 14
ADX_TREND_THRESHOLD = 25

# Moving Averages
EMA_FAST = 50
EMA_SLOW = 200
SMA_VOLUME = 20

# Momentum
MOMENTUM_PERIOD = 14

# Volatility
VOLATILITY_PERIOD = 20

# ============================================================================
# DASHBOARD CONFIGURATION
# ============================================================================

# Color scheme for regimes
REGIME_COLORS = {
    'Bull': '#09ab3b',  # Green
    'Bear': '#ff2b6e',  # Red
    'Neutral': '#ffa500',  # Orange
    'Crash': '#8B0000'  # Dark red
}

# Chart configuration
CHART_BARS_DISPLAY = 100  # Number of bars to show in chart
CHART_HEIGHT = 700  # Chart height in pixels

# Dashboard refresh
AUTO_REFRESH_ENABLED = False
REFRESH_INTERVAL_SECONDS = 300

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Trade logging
LOG_TRADES = True
LOG_FILE = 'trade_log.csv'

# Debug mode
DEBUG_MODE = False

# ============================================================================
# PERFORMANCE METRICS
# ============================================================================

# Metrics to display
DISPLAY_METRICS = [
    'total_return',
    'alpha',
    'win_rate',
    'max_drawdown',
    'num_trades',
    'avg_trade_duration'
]


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_stock_list():
    """Get the full list of stocks"""
    return ALL_STOCKS


def get_entry_conditions_count():
    """Get the number of entry conditions"""
    return len(ENTRY_CONDITIONS)


def validate_config():
    """Validate configuration parameters"""
    errors = []
    
    if HMM_COMPONENTS < 2:
        errors.append("HMM_COMPONENTS must be at least 2")
    
    if MIN_CONDITIONS_FOR_ENTRY > get_entry_conditions_count():
        errors.append(f"MIN_CONDITIONS_FOR_ENTRY cannot exceed {get_entry_conditions_count()}")
    
    if DEFAULT_LEVERAGE < 1.0:
        errors.append("DEFAULT_LEVERAGE must be at least 1.0")
    
    if COOLDOWN_HOURS < 0:
        errors.append("COOLDOWN_HOURS cannot be negative")
    
    if DEFAULT_INITIAL_CAPITAL <= 0:
        errors.append("DEFAULT_INITIAL_CAPITAL must be positive")
    
    return errors


def print_config():
    """Print current configuration"""
    print("\n" + "="*60)
    print("REGIME-BASED TRADING APP - CONFIGURATION")
    print("="*60)
    
    print("\n[HMM Configuration]")
    print(f"  Components: {HMM_COMPONENTS}")
    print(f"  Covariance Type: {HMM_COVARIANCE_TYPE}")
    print(f"  Training Iterations: {HMM_N_ITER}")
    
    print("\n[Strategy Configuration]")
    print(f"  Entry Conditions: {get_entry_conditions_count()}")
    print(f"  Minimum for Entry: {MIN_CONDITIONS_FOR_ENTRY}")
    print(f"  Initial Capital: ${DEFAULT_INITIAL_CAPITAL}")
    print(f"  Leverage: {DEFAULT_LEVERAGE}×")
    print(f"  Cooldown Period: {COOLDOWN_HOURS}h")
    
    print("\n[Data Configuration]")
    print(f"  Default Interval: {DEFAULT_INTERVAL}")
    print(f"  Default History: {DEFAULT_HISTORY_DAYS} days")
    print(f"  Available Stocks: {len(ALL_STOCKS)}")
    
    print("\n[Technical Indicators]")
    print(f"  RSI Period: {RSI_PERIOD}")
    print(f"  MACD: ({MACD_FAST}, {MACD_SLOW}, {MACD_SIGNAL})")
    print(f"  ADX Period: {ADX_PERIOD}")
    print(f"  EMA: {EMA_FAST}/{EMA_SLOW}")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    # Validate configuration on load
    errors = validate_config()
    if errors:
        print("Configuration errors found:")
        for error in errors:
            print(f"  ⚠️ {error}")
    else:
        print("✅ Configuration is valid")
    
    # Print configuration
    print_config()
