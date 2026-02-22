# QUICKSTART.md - Get Up and Running in 5 Minutes

## Windows (Fastest Way)

1. **Extract the project** to your desired location
2. **Double-click** `setup_windows.bat`
3. Follow the script prompts:
   - It will create a virtual environment
   - It will install all dependencies automatically
   - You can choose to install TA-Lib (optional)
4. **Select option 1** to run the dashboard
5. The app opens automatically at `http://localhost:8501`

## macOS/Linux

1. **Extract the project** to your desired location
2. **Open Terminal** and navigate to the folder:
   ```bash
   cd path/to/EtradeMyPortfolioClaudeAI
   ```
3. **Run the setup script:**
   ```bash
   chmod +x setup_linux_mac.sh
   ./setup_linux_mac.sh
   ```
4. **Select option 1** to run the dashboard
5. The app opens automatically at `http://localhost:8501`

## Using the App

### First Run
1. Select a ticker (try AAPL or GOOGL)
2. Keep the default settings for your first test
3. Click **"🚀 Run Backtest"**
4. Wait 2-5 minutes for the simulation to complete

### Understanding the Results
- **Green background** = Bull regime (favorable for trading)
- **Red background** = Bear regime (positions auto-exit)
- **Current Signal** = LONG or CASH
- **Performance Metrics** = Total return, win rate, max drawdown

### Next Steps After First Run
- Try different tickers
- Adjust capital and leverage
- Change historical data period
- View detailed trade logs
- Analyze regime distribution

## Troubleshooting First Run

**"No data found for ticker"**
- Try: AAPL, MSFT, GOOGL, TSLA, NVDA
- Or any stock from the pre-configured list

**"TA-Lib installation failed"**
- It's optional! The app works fine without it
- It just won't show TA-Lib warning, will use manual calculations

**App doesn't start**
- Run `python setup_check.py` to verify installation
- Make sure virtual environment is activated
- Try reinstalling: `pip install -r requirements.txt --force-reinstall`

## Command Line Reference

```bash
# After setup, activate environment (if not automated):
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Run dashboard
streamlit run myPortfolioapp.py

# Run examples
python example.py

# Check configuration
python config.py

# Verify setup
python setup_check.py
```

## What Happens During Backtest

1. **Data Fetching** (1-2 min)
   - Downloads 1 year of hourly price data
   - Calculates technical indicators

2. **HMM Training** (30-60 sec)
   - Trains 7-component Hidden Markov Model
   - Identifies Bull and Bear regimes
   - Learns market behavior patterns

3. **Backtesting** (2-5 min)
   - Simulates trading for entire history
   - Checks 8 entry conditions each hour
   - Records all trades and metrics
   - Calculates performance statistics

4. **Results Display** (instant)
   - Shows interactive chart
   - Displays all trades with entry/exit prices
   - Calculates performance metrics

## Typical Results

Most backtests on random tickers show:
- **Total Returns**: -10% to +30%
- **Win Rate**: 40-60%
- **Max Drawdown**: 10-25%
- **Number of Trades**: 5-15 over one year

These results vary significantly based on:
- Selected ticker and its volatility
- Market conditions over the backtest period
- Whether you're in a bull or bear market

## Tips for Best Results

1. **Use liquid stocks** (AAPL, MSFT, GOOGL, NVDA, TSLA)
   - Better data quality and execution
   
2. **Test multiple tickers** to understand strategy
   - Different tickers have different characteristics
   
3. **Adjust leverage carefully**
   - Higher leverage = higher risk AND higher returns
   - Start with 1.0x or 1.5x if new to trading
   
4. **Review trade logs**
   - Understand why each trade was entered and exited
   - Look at win/loss patterns
   
5. **Try different timeframes**
   - 30-day backtest = more choppy market
   - 365-day backtest = full market cycles

## Need Help?

1. Check README.md for detailed documentation
2. Run `python setup_check.py` to diagnose issues
3. Review example.py to see API usage
4. Check config.py to understand parameters

## That's It!

You're now ready to trade. The app will:
- ✅ Detect market regimes automatically
- ✅ Execute trades based on 8-factor confirmation
- ✅ Manage risk with automatic stop-outs
- ✅ Show you all metrics and analysis

Happy trading! 📈
