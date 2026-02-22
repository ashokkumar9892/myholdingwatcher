"""
Data Loader Module
Fetches hourly OHLCV data for specified stocks using yfinance
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')

# List of stocks to trade
STOCK_LIST = [
    'ABVX', 'AAP', 'ADMA', 'AGEN', 'CELC', 'CNC', 'CONI', 'DAVE', 'FIVN', 'GLUE',
    'LUMN', 'LWAY', 'MGPI', 'NNNN', 'NVCR', 'NVDL', 'ODD', 'PEGA', 'QURE', 'RXO',
    'SBUX', 'SERV', 'SOGP', 'TIL', 'TREE', 'UPST', 'WLDN', 'ZEPP'
]

def fetch_hourly_data(ticker, days=730):
    """
    Fetch hourly OHLCV data for a given ticker
    
    Args:
        ticker (str): Stock ticker symbol
        days (int): Number of days of historical data to fetch (default: 730 days)
    
    Returns:
        pd.DataFrame: OHLCV data with Open, High, Low, Close, Volume columns
    """
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        data = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            interval='1h',
            progress=False,
            threads=True
        )
        
        if data.empty:
            print(f"Warning: No data found for {ticker}")
            return None
        
        # Ensure required columns exist
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in data.columns for col in required_cols):
            print(f"Warning: Missing required columns for {ticker}")
            return None
        
        # Remove any NaN values
        data = data.dropna()
        
        if len(data) < 100:
            print(f"Warning: Insufficient data for {ticker} ({len(data)} bars)")
            return None
        
        return data
    
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return None


def fetch_multisymbol_data(ticker_list=None, days=730):
    """
    Fetch hourly data for multiple stocks
    
    Args:
        ticker_list (list): List of stock tickers (default: STOCK_LIST)
        days (int): Number of days of historical data (default: 730)
    
    Returns:
        dict: Dictionary with ticker as key and DataFrame as value
    """
    if ticker_list is None:
        ticker_list = STOCK_LIST
    
    data_dict = {}
    
    for ticker in ticker_list:
        print(f"Fetching data for {ticker}...")
        data = fetch_hourly_data(ticker, days)
        if data is not None:
            data_dict[ticker] = data
    
    return data_dict


def calculate_features(data):
    """
    Calculate HMM training features from OHLCV data
    
    Features:
    1. Returns: log returns
    2. Range: (High - Low) / Close
    3. Volume Volatility: rolling standard deviation of returns
    
    Args:
        data (pd.DataFrame): OHLCV data
    
    Returns:
        pd.DataFrame: DataFrame with calculated features
    """
    df = data.copy()
    
    # Calculate log returns
    df['Returns'] = np.log(df['Close'] / df['Close'].shift(1))
    
    # Calculate range
    df['Range'] = (df['High'] - df['Low']) / df['Close']
    
    # Calculate volume volatility (rolling std of returns)
    df['Volume_Volatility'] = df['Returns'].rolling(window=20).std()
    
    # Remove NaN values
    df = df.dropna()
    
    return df


def get_training_features(data):
    """
    Extract training features for HMM model
    
    Args:
        data (pd.DataFrame): Data with calculated features
    
    Returns:
        np.ndarray: Array of shape (n_samples, 3) with [Returns, Range, Volume_Volatility]
    """
    features = data[['Returns', 'Range', 'Volume_Volatility']].values
    return features


if __name__ == "__main__":
    # Test data loading
    print("Testing data loader...")
    data = fetch_hourly_data('AAPL', days=30)
    if data is not None:
        print(f"Fetched {len(data)} bars for AAPL")
        print(data.head())
        
        # Test feature calculation
        features_df = calculate_features(data)
        print("\nFeatures sample:")
        print(features_df[['Returns', 'Range', 'Volume_Volatility']].head())
