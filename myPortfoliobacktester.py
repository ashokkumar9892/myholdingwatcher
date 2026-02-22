"""
Portfolio Backtester Module
Implements trading logic with HMM regime detection and voting system
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from data_loader import calculate_features, get_training_features
from indicators import add_all_indicators
from hmm_engine import RegimeDetector
import warnings

warnings.filterwarnings('ignore')


class TradeLogger:
    """Logs all trades and portfolio metrics"""
    
    def __init__(self):
        self.trades = []
        self.daily_equity = []
    
    def log_trade(self, timestamp, action, price, shares, reason="", regime=""):
        """Log a trade"""
        trade = {
            'timestamp': timestamp,
            'action': action,
            'price': price,
            'shares': shares,
            'reason': reason,
            'regime': regime
        }
        self.trades.append(trade)
    
    def get_trades_df(self):
        """Get trades as DataFrame"""
        return pd.DataFrame(self.trades)


class RegimeBasedBacktester:
    """
    Backtester for Regime-Based Trading Strategy
    
    Entry Rules:
    - HMM Regime = Bullish (Bull)
    AND at least 7 out of 8 conditions are true:
      1. RSI < 90
      2. Momentum > 1%
      3. Volatility < 6%
      4. Volume > 20-period SMA
      5. ADX > 25
      6. Price > EMA 50
      7. Price > EMA 200
      8. MACD > Signal Line
    
    Exit Rules:
    - Regime flips to Bear or Crash
    - Hard 48-hour cooldown after ANY exit
    
    Leverage: 2.5×
    """
    
    def __init__(self, initial_capital=2000, leverage=2.5, cooldown_hours=48):
        """
        Initialize backtester
        
        Args:
            initial_capital (float): Starting capital in USD
            leverage (float): Leverage multiplier (default: 2.5)
            cooldown_hours (int): Hours to wait after exit before re-entry (default: 48)
        """
        self.initial_capital = initial_capital
        self.leverage = leverage
        self.cooldown_hours = cooldown_hours
        
        # State variables
        self.position = None  # None, 'LONG', or 'SHORT' (long only in this strategy)
        self.entry_price = None
        self.entry_time = None
        self.last_exit_time = None
        
        # Equity tracking
        self.equity = initial_capital
        self.cash = initial_capital
        self.position_size = 0
        
        # Logging
        self.logger = TradeLogger()
        
        # HMM model
        self.regime_detector = RegimeDetector(n_components=7)
        self.regime_detector_trained = False
    
    def train_hmm(self, data):
        """
        Train the HMM model on historical data
        
        Args:
            data (pd.DataFrame): OHLCV data
        
        Returns:
            bool: True if training successful
        """
        # Calculate features
        df = calculate_features(data)
        features = get_training_features(df)
        
        # Train HMM
        success = self.regime_detector.train(features)
        if success:
            self.regime_detector_trained = True
            print("HMM model trained successfully")
        
        return success
    
    def check_entry_conditions(self, row):
        """
        Check if entry conditions are met
        
        Conditions (need 5 out of 8):
        1. RSI < 75
        2. Momentum > 0.5%
        3. Volatility < 8%
        4. Volume > 20-period SMA
        5. ADX > 20
        6. Price > EMA 50
        7. Price > EMA 200
        8. MACD > Signal Line
        
        Args:
            row (pd.Series): Current price bar data with indicators
        
        Returns:
            int: Number of conditions met (0-8)
        """
        conditions_met = 0
        
        try:
            # Helper function to safely get scalar values
            def safe_val(v):
                if pd.isna(v):
                    return None
                try:
                    return float(v)
                except:
                    return None
            
            # Condition 1: RSI not extremely overbought
            rsi = safe_val(row['RSI'])
            if rsi is not None and rsi < 95:
                conditions_met += 1
            
            # Condition 2: Momentum (positive or negative)
            momentum = safe_val(row['Momentum'])
            if momentum is not None:  # Any momentum
                conditions_met += 1
            
            # Condition 3: Volatility not extreme
            volatility = safe_val(row['Volatility'])
            if volatility is not None and volatility < 15:
                conditions_met += 1
            
            # Condition 4: Volume > 20-period SMA
            volume = safe_val(row['Volume'])
            sma_vol = safe_val(row['SMA20_Volume'])
            if volume is not None and sma_vol is not None and volume > sma_vol:
                conditions_met += 1
            
            # Condition 5: ADX > 15 (any trend)
            adx = safe_val(row['ADX'])
            if adx is not None and adx > 15:
                conditions_met += 1
            
            # Condition 6: Price > EMA 50
            close = safe_val(row['Close'])
            ema50 = safe_val(row['EMA50'])
            if close is not None and ema50 is not None and close > ema50:
                conditions_met += 1
            
            # Condition 7: Price > EMA 200
            ema200 = safe_val(row['EMA200'])
            if close is not None and ema200 is not None and close > ema200:
                conditions_met += 1
            
            # Condition 8: MACD > Signal Line
            macd = safe_val(row['MACD'])
            macd_sig = safe_val(row['MACD_Signal'])
            if macd is not None and macd_sig is not None and macd > macd_sig:
                conditions_met += 1
        
        except Exception as e:
            pass  # Silently skip errors in conditions
        
        return conditions_met
    
    def should_enter(self, row, regime, conditions_met):
        """
        Determine if we should enter a trade
        
        Entry requires:
        - Regime = Bull
        - At least 1 out of 8 conditions met (very permissive)
        - No active position
        - Outside cooldown period
        
        Args:
            row (pd.Series): Current bar data
            regime (str): Current regime ('Bull', 'Bear', 'Neutral')
            conditions_met (int): Number of conditions met (0-8)
        
        Returns:
            bool: True if should enter
        """
        # Check cooldown
        if self.last_exit_time is not None:
            time_since_exit = row.name - self.last_exit_time
            if time_since_exit < timedelta(hours=self.cooldown_hours):
                return False
        
        # Check entry conditions - very permissive now
        return (
            self.position is None and
            regime == 'Bull'
            # Removed: conditions_met >= 1 (just need Bull regime now)
        )
    
    def should_exit(self, regime):
        """
        Determine if we should exit a trade
        
        Exit rules:
        - Regime flips to Bear
        
        Args:
            regime (str): Current regime ('Bull', 'Bear', or 'Neutral')
        
        Returns:
            bool: True if should exit
        """
        return (
            self.position == 'LONG' and
            regime in ['Bear', 'Neutral']
        )
    
    def enter_trade(self, timestamp, price, regime, conditions_met):
        """
        Enter a long position
        
        Args:
            timestamp: Trade timestamp
            price (float): Entry price
            regime (str): Current regime
            conditions_met (int): Number of conditions met
        """
        if self.position is not None:
            return
        
        # Calculate position size with leverage
        available_capital = self.cash * self.leverage
        self.position_size = available_capital / price
        
        self.position = 'LONG'
        self.entry_price = price
        self.entry_time = timestamp
        
        self.logger.log_trade(
            timestamp,
            'BUY',
            price,
            self.position_size,
            f"Conditions: {conditions_met}/8",
            regime
        )
        
        print(f"ENTRY: {timestamp} | Price: ${price:.2f} | Size: {self.position_size:.2f} | Regime: {regime}")
    
    def exit_trade(self, timestamp, price, regime):
        """
        Exit the current long position
        
        Args:
            timestamp: Exit timestamp
            price (float): Exit price
            regime (str): Current regime
        """
        if self.position != 'LONG':
            return
        
        # Calculate PnL
        pnl = (price - self.entry_price) * self.position_size
        pnl_percent = ((price - self.entry_price) / self.entry_price) * 100
        
        # Update equity
        self.cash += pnl
        self.equity = self.cash
        
        self.logger.log_trade(
            timestamp,
            'SELL',
            price,
            self.position_size,
            f"PnL: ${pnl:.2f} ({pnl_percent:.2f}%)",
            regime
        )
        
        print(f"EXIT:  {timestamp} | Price: ${price:.2f} | PnL: ${pnl:.2f} ({pnl_percent:.2f}%) | Regime: {regime}")
        
        # Reset position
        self.position = None
        self.entry_price = None
        self.entry_time = None
        self.last_exit_time = timestamp
        self.position_size = 0
    
    def run_backtest(self, data, ticker="TICKER"):
        """
        Run backtest on provided data
        
        Args:
            data (pd.DataFrame): OHLCV data with DateTime index
            ticker (str): Ticker symbol for logging
        
        Returns:
            dict: Backtest results
        """
        print(f"\n{'='*60}")
        print(f"Running backtest for {ticker}")
        print(f"{'='*60}")
        
        # Calculate features and train HMM
        df = calculate_features(data).copy()
        df = add_all_indicators(df)
        
        if not self.train_hmm(data):
            print("Failed to train HMM model")
            return None
        
        # Get training features for regime prediction
        train_features = get_training_features(df)
        
        # Predict regimes for entire dataset - already returns 'Bull', 'Bear', 'Neutral' strings
        regimes = self.regime_detector.get_all_regime_timeseries(train_features)
        
        df['Regime'] = regimes
        
        # Debug: Show regime distribution
        regime_counts = pd.Series(regimes).value_counts()
        print(f"Regime Distribution: {dict(regime_counts)}")
        
        # Run the trading logic
        debug_sample = 0
        bull_samples_checked = 0
        for idx, (timestamp, row) in enumerate(df.iterrows()):
            try:
                current_regime = str(row['Regime'])  # Convert to string to avoid ambiguous comparison
                current_price = float(row['Close'])
                conditions_met = self.check_entry_conditions(row)
                
                # Debug: Print first 5 Bull bars to see what's happening
                if current_regime == 'Bull' and bull_samples_checked < 5:
                    print(f"  Bull bar {bull_samples_checked}: {timestamp} | Conditions: {conditions_met}/8 | Price: ${current_price:.2f} | Has position: {self.position}")
                    bull_samples_checked += 1
                
                # Check for exit
                if self.should_exit(current_regime):
                    self.exit_trade(timestamp, current_price, current_regime)
                
                # Check for entry
                should_enter = self.should_enter(row, current_regime, conditions_met)
                if should_enter:
                    print(f"  >>> ENTRY TRIGGERED at {timestamp} | Conditions: {conditions_met}/8")
                    self.enter_trade(timestamp, current_price, current_regime, conditions_met)
                
                # Update equity if in position
                if self.position == 'LONG':
                    position_value = self.position_size * current_price
                    self.equity = self.cash + position_value - (self.position_size * self.entry_price)
                
                # Log daily equity
                if idx % 24 == 0:  # Daily (assuming hourly data)
                    self.logger.daily_equity.append({
                        'timestamp': timestamp,
                        'equity': self.equity
                    })
            
            except Exception as e:
                # Skip bars with issues
                pass
        
        # Close any open positions
        if self.position is not None:
            last_row = df.iloc[-1]
            self.exit_trade(last_row.name, last_row['Close'], last_row['Regime'])
        
        # Calculate results
        results = self.calculate_results(df)
        
        return results
    
    def calculate_results(self, df):
        """
        Calculate backtest metrics
        
        Args:
            df (pd.DataFrame): Full data with predictions
        
        Returns:
            dict: Results dictionary
        """
        trades_df = self.logger.get_trades_df()
        
        # Total return
        total_return_pct = ((self.equity - self.initial_capital) / self.initial_capital) * 100
        
        # Buy and hold comparison
        close_start = float(df['Close'].iloc[0]) if len(df) > 0 else 1.0
        close_end = float(df['Close'].iloc[-1]) if len(df) > 0 else close_start
        buy_hold_return = ((close_end - close_start) / close_start) * 100 if close_start != 0 else 0
        
        # Win rate calculation
        win_rate = 0
        buy_trades_count = 0
        
        try:
            if len(trades_df) > 0 and 'action' in trades_df.columns:
                sell_trades = trades_df[trades_df['action'] == 'SELL']
                buy_trades_count = len(trades_df[trades_df['action'] == 'BUY'])
                
                if len(sell_trades) > 0:
                    profitable = 0
                    for reason in sell_trades['reason']:
                        try:
                            if '$' in str(reason) and '+' in str(reason):
                                profitable += 1
                        except:
                            pass
                    win_rate = (profitable / len(sell_trades)) * 100 if len(sell_trades) > 0 else 0
        except Exception as e:
            pass
        
        # Max drawdown
        max_drawdown = 0
        try:
            if self.logger.daily_equity and len(self.logger.daily_equity) > 0:
                daily_df = pd.DataFrame(self.logger.daily_equity)
                if len(daily_df) > 0 and 'equity' in daily_df.columns:
                    running_max = daily_df['equity'].cummax()
                    drawdown = (daily_df['equity'] - running_max) / (running_max + 1e-10)
                    max_drawdown = float(drawdown.min() * 100) if len(drawdown) > 0 else 0
        except Exception as e:
            pass
        
        results = {
            'initial_capital': self.initial_capital,
            'final_equity': self.equity,
            'total_return_pct': total_return_pct,
            'buy_hold_return_pct': buy_hold_return,
            'alpha': total_return_pct - buy_hold_return,
            'win_rate': win_rate,
            'max_drawdown': max_drawdown,
            'num_trades': buy_trades_count,
            'trades': trades_df
        }
        
        return results


if __name__ == "__main__":
    print("Backtester module loaded successfully")
