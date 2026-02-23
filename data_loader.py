"""
Data Loader Module
Fetches hourly OHLCV data for specified stocks using Polygon.io API
"""

from polygon import RESTClient
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
from config import POLYGON_API_KEY

warnings.filterwarnings('ignore')

# List of stocks to trade
STOCK_LIST = [
    'ABVX', 'AAP', 'ADMA', 'AGEN', 'CELC', 'CNC', 'CONI', 'DAVE', 'FIVN', 'GLUE',
    'LUMN', 'LWAY', 'MGPI', 'NNNN', 'NVCR', 'NVDL', 'ODD', 'PEGA', 'QURE', 'RXO',
    'SBUX', 'SERV', 'SOGP', 'TIL', 'TREE', 'UPST', 'WLDN', 'ZEPP'
]

def fetch_hourly_data(ticker, days=730):
    """
    Fetch hourly OHLCV data for a given ticker using Polygon.io
    
    Args:
        ticker (str): Stock ticker symbol
        days (int): Number of days of historical data to fetch (default: 730 days)
    
    Returns:
        pd.DataFrame: OHLCV data with Open, High, Low, Close, Volume columns
    """
    try:
        if not POLYGON_API_KEY:
            raise ValueError(
                "Polygon.io API key not found. Please set POLYGON_API_KEY in your .env file. "
                "Get your free API key at: https://polygon.io/"
            )
        
        # Initialize Polygon client
        client = RESTClient(api_key=POLYGON_API_KEY)
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Format dates for Polygon API (YYYY-MM-DD)
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')
        
        # Fetch hourly aggregates
        # timespan='hour', multiplier=1
        aggs = []
        for agg in client.list_aggs(
            ticker=ticker,
            multiplier=1,
            timespan='hour',
            from_=start_str,
            to=end_str,
            limit=50000  # Max limit
        ):
            aggs.append(agg)
        
        if not aggs:
            print(f"Warning: No data found for {ticker}")
            return None
        
        # Convert to DataFrame
        data_list = []
        for agg in aggs:
            data_list.append({
                'timestamp': pd.to_datetime(agg.timestamp, unit='ms'),
                'Open': agg.open,
                'High': agg.high,
                'Low': agg.low,
                'Close': agg.close,
                'Volume': agg.volume
            })
        
        df = pd.DataFrame(data_list)
        df.set_index('timestamp', inplace=True)
        df.sort_index(inplace=True)
        
        # Ensure required columns exist
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in df.columns for col in required_cols):
            print(f"Warning: Missing required columns for {ticker}")
            return None
        
        # Remove any NaN values
        df = df.dropna()
        
        if len(df) < 100:
            print(f"Warning: Insufficient data for {ticker} ({len(df)} bars)")
            return None
        
        return df
    
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
