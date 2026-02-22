"""
Technical Indicators Module
Implements various technical indicators used in the trading strategy
Includes fallback implementations for indicators without TA-Lib
"""

import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# Try to import TA-Lib, fall back to manual implementations if not available
try:
    from talib import RSI as TA_RSI, MACD as TA_MADC, ADX as TA_ADX
    HAS_TALIB = True
except ImportError:
    HAS_TALIB = False
    print("Warning: TA-Lib not installed. Using manual indicator calculations.")


def calculate_rsi(data, period=14):
    """Calculate Relative Strength Index"""
    if HAS_TALIB:
        close_vals = np.asarray(data['Close']).flatten()
        return TA_RSI(close_vals, timeperiod=period)
    else:
        # Manual RSI calculation using pandas
        close = np.asarray(data['Close']).flatten()
        delta = np.diff(close)
        gain = np.zeros_like(close)
        loss = np.zeros_like(close)
        
        for i in range(period, len(close)):
            gains = delta[i-period:i]
            losses = -delta[i-period:i]
            
            gain[i] = np.mean(gains[gains > 0]) if np.any(gains > 0) else 0
            loss[i] = np.mean(losses[losses > 0]) if np.any(losses > 0) else 0
        
        rs = gain / (loss + 1e-10)
        rsi = 100 - (100 / (1 + rs))
        return rsi


def calculate_macd(data, fast=12, slow=26, signal=9):
    """Calculate MACD and Signal Line"""
    if HAS_TALIB:
        close = np.asarray(data['Close']).flatten()
        return TA_MADC(close, fastperiod=fast, slowperiod=slow, signalperiod=signal)
    else:
        # Manual MACD calculation
        close = np.asarray(data['Close']).flatten()
        ema_fast = pd.Series(close).ewm(span=fast, adjust=False).mean().values
        ema_slow = pd.Series(close).ewm(span=slow, adjust=False).mean().values
        macd_line = ema_fast - ema_slow
        signal_line = pd.Series(macd_line).ewm(span=signal, adjust=False).mean().values
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram


def calculate_adx(data, period=14):
    """Calculate Average Directional Index"""
    if HAS_TALIB:
        high = np.asarray(data['High']).flatten()
        low = np.asarray(data['Low']).flatten()
        close = np.asarray(data['Close']).flatten()
        return TA_ADX(high, low, close, timeperiod=period)
    else:
        # Manual ADX calculation - simplified version
        high = np.asarray(data['High']).flatten()
        low = np.asarray(data['Low']).flatten()
        close = np.asarray(data['Close']).flatten()
        
        # Calculate True Range
        tr = np.zeros(len(close))
        for i in range(len(close)):
            if i == 0:
                tr[i] = high[i] - low[i]
            else:
                tr[i] = max(
                    high[i] - low[i],
                    abs(high[i] - close[i-1]),
                    abs(low[i] - close[i-1])
                )
        
        # Calculate ATR
        atr = pd.Series(tr).rolling(window=period).mean().values
        
        # Directional Movement
        plus_dm = np.zeros(len(close))
        minus_dm = np.zeros(len(close))
        
        for i in range(1, len(close)):
            up = high[i] - high[i-1]
            down = low[i-1] - low[i]
            
            if up > down and up > 0:
                plus_dm[i] = up
            else:
                plus_dm[i] = 0
                
            if down > up and down > 0:
                minus_dm[i] = down
            else:
                minus_dm[i] = 0
        
        # Calculate DI+, DI-
        plus_di = 100 * pd.Series(plus_dm).rolling(window=period).mean() / (pd.Series(atr) + 0.0001)
        minus_di = 100 * pd.Series(minus_dm).rolling(window=period).mean() / (pd.Series(atr) + 0.0001)
        
        # Calculate ADX
        di_diff = np.abs(plus_di.values - minus_di.values)
        di_sum = plus_di.values + minus_di.values + 0.0001
        dx = 100 * di_diff / di_sum
        adx = pd.Series(dx).rolling(window=period).mean().values
        
        return adx


def calculate_ema(data, period=50):
    """Calculate Exponential Moving Average"""
    return data['Close'].ewm(span=period, adjust=False).mean().values


def calculate_sma(data, period=20):
    """Calculate Simple Moving Average"""
    return data['Close'].rolling(window=period).mean().values


def calculate_volatility(data, period=20):
    """Calculate rolling volatility (standard deviation of returns)"""
    returns = np.log(data['Close'] / data['Close'].shift(1))
    volatility = returns.rolling(window=period).std() * 100  # Convert to percentage
    return volatility.values


def calculate_momentum(data, period=14):
    """Calculate Momentum indicator"""
    momentum = ((data['Close'] - data['Close'].shift(period)) / data['Close'].shift(period)) * 100
    return momentum.values


def calculate_volume_sma(data, period=20):
    """Calculate Simple Moving Average of Volume"""
    return data['Volume'].rolling(window=period).mean().values


def add_all_indicators(data):
    """
    Add all technical indicators to the dataframe
    
    Args:
        data (pd.DataFrame): OHLCV data
    
    Returns:
        pd.DataFrame: Data with all indicators added
    """
    df = data.copy()
    
    # RSI
    df['RSI'] = calculate_rsi(df, period=14)
    
    # MACD
    df['MACD'], df['MACD_Signal'], df['MACD_Histogram'] = calculate_macd(df)
    
    # ADX
    df['ADX'] = calculate_adx(df, period=14)
    
    # EMAs
    df['EMA50'] = calculate_ema(df, period=50)
    df['EMA200'] = calculate_ema(df, period=200)
    
    # SMAs
    df['SMA20_Volume'] = calculate_volume_sma(df, period=20)
    
    # Volatility
    df['Volatility'] = calculate_volatility(df, period=20)
    
    # Momentum
    df['Momentum'] = calculate_momentum(df, period=14)
    
    # Remove NaN values
    df = df.dropna()
    
    return df


if __name__ == "__main__":
    print("Indicators module loaded successfully")
