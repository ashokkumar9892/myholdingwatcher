"""
Example Usage Script
Demonstrates how to use the Regime-Based Trading App programmatically
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from data_loader import fetch_hourly_data, calculate_features, get_training_features
from indicators import add_all_indicators
from hmm_engine import RegimeDetector
from myPortfoliobacktester import RegimeBasedBacktester
from config import print_config


def example_single_backtest():
    """
    Example 1: Run backtest for a single ticker
    """
    print("\n" + "="*60)
    print("EXAMPLE 1: Single Ticker Backtest")
    print("="*60)
    
    ticker = 'AAPL'
    print(f"\nBacTesting {ticker}...")
    
    # Fetch data
    print(f"  1. Fetching {ticker} data...")
    data = fetch_hourly_data(ticker, days=180)
    
    if data is None:
        print(f"   ❌ Failed to fetch data for {ticker}")
        return
    
    print(f"   ✅ Fetched {len(data)} hourly bars")
    
    # Calculate features and add indicators
    print("  2. Calculating features and indicators...")
    df = calculate_features(data).copy()
    df = add_all_indicators(df)
    print(f"   ✅ Added {len(df.columns)} columns with features and indicators")
    
    # Run backtest
    print("  3. Running backtest...")
    backtester = RegimeBasedBacktester(
        initial_capital=2000,
        leverage=2.5,
        cooldown_hours=48
    )
    
    results = backtester.run_backtest(data, ticker=ticker)
    
    if results:
        print("\n  Results:")
        print(f"    Total Return: {results['total_return_pct']:.2f}%")
        print(f"    Buy & Hold: {results['buy_hold_return_pct']:.2f}%")
        print(f"    Alpha: {results['alpha']:.2f}%")
        print(f"    Max Drawdown: {results['max_drawdown']:.2f}%")
        print(f"    Number of Trades: {results['num_trades']}")
        print(f"    Win Rate: {results['win_rate']:.1f}%")


def example_multi_backtest():
    """
    Example 2: Backtest multiple tickers and compare results
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: Multi-Ticker Comparison")
    print("="*60)
    
    tickers = ['MSFT', 'GOOGL', 'TSLA']
    results_dict = {}
    
    for ticker in tickers:
        print(f"\nTesting {ticker}...")
        
        try:
            # Fetch data
            data = fetch_hourly_data(ticker, days=90)
            if data is None:
                print(f"  ⚠️ No data for {ticker}")
                continue
            
            # Calculate features
            df = calculate_features(data).copy()
            df = add_all_indicators(df)
            
            # Run backtest
            backtester = RegimeBasedBacktester(initial_capital=2000, leverage=2.5)
            results = backtester.run_backtest(data, ticker=ticker)
            
            if results:
                results_dict[ticker] = results
                print(f"  ✅ Return: {results['total_return_pct']:.2f}% | Trades: {results['num_trades']}")
        
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
    
    # Compare results
    if results_dict:
        print("\n" + "-"*60)
        print("Comparison Results:")
        print("-"*60)
        print(f"{'Ticker':<10} {'Return %':<12} {'Alpha %':<12} {'Trades':<10}")
        print("-"*60)
        
        for ticker, results in results_dict.items():
            print(f"{ticker:<10} {results['total_return_pct']:>10.2f}% {results['alpha']:>10.2f}% {results['num_trades']:>8}")


def example_hmm_analysis():
    """
    Example 3: HMM Regime Analysis
    """
    print("\n" + "="*60)
    print("EXAMPLE 3: HMM Regime Analysis")
    print("="*60)
    
    ticker = 'NASDAQ'
    print(f"\nAnalyzing regimes for {ticker}...")
    
    try:
        # Fetch data
        data = fetch_hourly_data(ticker, days=180)
        if data is None:
            print(f"  ❌ Failed to fetch data")
            return
        
        # Calculate features
        df = calculate_features(data).copy()
        features = get_training_features(df)
        
        # Train HMM
        print("  Training HMM model...")
        regime_detector = RegimeDetector(n_components=7)
        
        if not regime_detector.train(features):
            print("  ❌ Training failed")
            return
        
        print("  ✅ Model trained successfully")
        print(f"    Bull State: {regime_detector.bull_state}")
        print(f"    Bear State: {regime_detector.bear_state}")
        
        # Analyze regimes
        regimes = regime_detector.get_all_regime_timeseries(features)
        unique, counts = np.unique(regimes, return_counts=True)
        
        print("\n  Regime Distribution:")
        for regime, count in zip(unique, counts):
            pct = (count / len(regimes)) * 100
            print(f"    {regime}: {count} bars ({pct:.1f}%)")
        
        # Current regime
        current_regime = regime_detector.get_current_regime(features[-1:])
        print(f"\n  Current Regime: {current_regime}")
    
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")


if __name__ == "__main__":
    import numpy as np
    
    print("\n")
    print("╔" + "═"*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  REGIME-BASED TRADING APP - EXAMPLES".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "═"*58 + "╝")
    
    # Print configuration
    print_config()
    
    # Run examples
    try:
        example_single_backtest()
        example_hmm_analysis()
        # example_multi_backtest()  # Commented to avoid too many API calls
        
        print("\n" + "="*60)
        print("✅ Examples completed!")
        print("="*60)
        print("\nTo run the interactive dashboard:")
        print("  streamlit run myPortfolioapp.py")
        print()
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Examples interrupted by user")
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
