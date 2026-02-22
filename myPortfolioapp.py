"""
Regime-Based Trading App - Streamlit Dashboard
Interactive dashboard for visualizing and analyzing trading signals and performance
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from datetime import datetime, timedelta
import warnings
import time

from data_loader import fetch_hourly_data, calculate_features, get_training_features
from indicators import add_all_indicators
from hmm_engine import RegimeDetector
from myPortfoliobacktester import RegimeBasedBacktester

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Regime-Based Trading App",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .positive {
        color: #09ab3b;
        font-weight: bold;
    }
    .negative {
        color: #ff2b6e;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_ticker_data(ticker, days=730):
    """Load ticker data with caching"""
    return fetch_hourly_data(ticker, days=days)


def get_regime_color(regime):
    """Get color for regime display"""
    regime_str = str(regime).strip()
    if regime_str == 'Bull':
        return '#09ab3b'  # Green
    elif regime_str == 'Bear':
        return '#ff2b6e'  # Red
    else:
        return '#ffa500'  # Orange


def create_candlestick_chart(data_with_regimes, ticker, trades_df=None):
    """
    Create interactive candlestick chart with regime colors and buy/sell markers
    
    Args:
        data_with_regimes (pd.DataFrame): Data with Regime column
        ticker (str): Ticker symbol
        trades_df (pd.DataFrame): DataFrame with trades (optional)
    
    Returns:
        plotly.graph_objects.Figure: Candlestick chart
    """
    df = data_with_regimes.tail(100).copy()  # Last 100 bars
    
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        row_heights=[0.7, 0.3],
        specs=[[{"secondary_y": False}], [{"secondary_y": False}]]
    )
    
    # Create candlestick chart with regime colors
    for i in range(len(df)):
        regime = str(df['Regime'].iloc[i])
        color = get_regime_color(regime)
        
        open_price = float(df['Open'].iloc[i])
        close_price = float(df['Close'].iloc[i])
        high_price = float(df['High'].iloc[i])
        low_price = float(df['Low'].iloc[i])
        volume = float(df['Volume'].iloc[i])
        
        # Candlestick
        fig.add_trace(
            go.Scatter(
                x=[df.index[i], df.index[i]],
                y=[low_price, high_price],
                mode='lines',
                line=dict(color=color, width=1),
                hoverinfo='skip',
                showlegend=False
            ),
            row=1, col=1
        )
        
        # Body
        fig.add_trace(
            go.Bar(
                x=[df.index[i]],
                y=[abs(close_price - open_price)],
                base=min(open_price, close_price),
                marker=dict(color=color, line=dict(color=color, width=0)),
                hovertext=[f"O: ${open_price:.2f}<br>H: ${high_price:.2f}<br>L: ${low_price:.2f}<br>C: ${close_price:.2f}<br>Regime: {regime}"],
                hoverinfo='text',
                showlegend=False
            ),
            row=1, col=1
        )
    
    # Add buy/sell markers if trades available
    last_trade_info = None
    if trades_df is not None and len(trades_df) > 0:
        try:
            buy_times = []
            buy_prices = []
            sell_times = []
            sell_prices = []
            
            # Get last trade for annotation
            try:
                last_trade = trades_df.iloc[-1]
                last_action = str(last_trade['action']).upper()
                last_price = float(last_trade['price'])
                last_timestamp = pd.to_datetime(last_trade['timestamp'])
                last_trade_info = {
                    'action': last_action,
                    'price': last_price,
                    'timestamp': last_timestamp,
                    'time_str': last_timestamp.strftime('%Y-%m-%d %H:%M')
                }
            except:
                pass
            
            for _, trade in trades_df.iterrows():
                try:
                    price = float(trade['price'])
                    timestamp = pd.to_datetime(trade['timestamp'])
                    action = str(trade['action']).upper()
                    
                    if action == 'BUY':
                        buy_times.append(timestamp)
                        buy_prices.append(price)
                    elif action == 'SELL':
                        sell_times.append(timestamp)
                        sell_prices.append(price)
                except:
                    pass
            
            # Add buy markers (green triangles)
            if buy_times:
                fig.add_trace(
                    go.Scatter(
                        x=buy_times,
                        y=buy_prices,
                        mode='markers+text',
                        name='Buy',
                        text=['<b>📈 BUY</b>'] * len(buy_times),
                        textposition='top center',
                        textfont=dict(size=13, color='darkgreen', family='Arial Black'),
                        marker=dict(symbol='triangle-up', size=16, color='lime', line=dict(color='darkgreen', width=3)),
                        hovertemplate='<b>BUY</b><br>Price: $%{y:.2f}<br>Time: %{x}<extra></extra>',
                        showlegend=True
                    ),
                    row=1, col=1
                )
            
            # Add sell markers (red triangles)
            if sell_times:
                fig.add_trace(
                    go.Scatter(
                        x=sell_times,
                        y=sell_prices,
                        mode='markers+text',
                        name='Sell',
                        text=['<b>📉 SELL</b>'] * len(sell_times),
                        textposition='bottom center',
                        textfont=dict(size=13, color='darkred', family='Arial Black'),
                        marker=dict(symbol='triangle-down', size=16, color='red', line=dict(color='darkred', width=3)),
                        hovertemplate='<b>SELL</b><br>Price: $%{y:.2f}<br>Time: %{x}<extra></extra>',
                        showlegend=True
                    ),
                    row=1, col=1
                )
        except Exception as e:
            pass  # Skip if trade markers fail
    
    # Add annotation for last trade as a box
    if last_trade_info:
        try:
            max_price = df['High'].max()
            min_price = df['Low'].min()
            price_range = max_price - min_price
            annotation_y = max_price - (price_range * 0.1)
            
            action_color = 'green' if last_trade_info['action'] == 'BUY' else 'red'
            annotation_text = f"<b>Last: {last_trade_info['action']}</b><br>${last_trade_info['price']:.2f}<br>{last_trade_info['time_str']}"
            
            fig.add_annotation(
                text=annotation_text,
                x=df.index[-1],
                y=annotation_y,
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor=action_color,
                ax=50,
                ay=-40,
                bgcolor=action_color,
                opacity=0.8,
                font=dict(color='white', size=11),
                bordercolor=action_color,
                borderwidth=2,
                row=1, col=1
            )
        except:
            pass
    
    # Add volume bars
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df['Volume'],
            marker=dict(color='rgba(0,0,0,0.1)'),
            showlegend=False,
            hovertemplate='Volume: %{y}<extra></extra>'
        ),
        row=2, col=1
    )
    
    # Add EMAs
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['EMA50'],
            mode='lines',
            name='EMA 50',
            line=dict(color='blue', width=1, dash='dash'),
            hovertemplate='EMA50: %{y:.2f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['EMA200'],
            mode='lines',
            name='EMA 200',
            line=dict(color='purple', width=1, dash='dash'),
            hovertemplate='EMA200: %{y:.2f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Update layout
    fig.update_layout(
        title=f"{ticker} - Hourly Chart with Regimes",
        yaxis_title="Price (USD)",
        yaxis2_title="Volume",
        hovermode='x unified',
        height=700,
        template='plotly_white'
    )
    
    fig.update_xaxes(title_text="Date", row=2, col=1)
    
    return fig


def create_metrics_chart(results):
    """Create performance metrics summary"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Return",
            value=f"{results['total_return_pct']:.2f}%",
            delta=f"{results['alpha']:.2f}% vs B&H"
        )
    
    with col2:
        st.metric(
            label="Win Rate",
            value=f"{results['win_rate']:.1f}%"
        )
    
    with col3:
        st.metric(
            label="Max Drawdown",
            value=f"{results['max_drawdown']:.2f}%"
        )
    
    with col4:
        st.metric(
            label="Number of Trades",
            value=f"{results['num_trades']}"
        )


def get_quick_analysis(ticker, days=730):
    """
    Quick analysis for a single ticker (for portfolio view)
    Returns: dict with analysis results or None if failed
    """
    try:
        # Load data
        data = fetch_hourly_data(ticker, days=days)
        if data is None or len(data) < 100:
            return None
        
        # Calculate features and indicators
        df = calculate_features(data).copy()
        df = add_all_indicators(df)
        
        # Train HMM
        regime_detector = RegimeDetector(n_components=7)
        train_features = get_training_features(df)
        
        if not regime_detector.train(train_features):
            return None
        
        # Predict regimes
        regimes = regime_detector.get_all_regime_timeseries(train_features)
        df['Regime'] = regimes
        
        # Run backtest
        backtester = RegimeBasedBacktester(initial_capital=2000, leverage=2.5)
        results = backtester.run_backtest(data, ticker=ticker)
        
        if results is None:
            return None
        
        # Get current status
        current_regime = str(df['Regime'].iloc[-1]).strip()
        current_price = float(df['Close'].iloc[-1])
        num_trades = results['num_trades']
        
        # Determine signal
        signal = "CASH"
        recommendation = "HOLD"
        
        if current_regime == 'Bull':
            signal = "LONG"
            recommendation = "BUY"
        elif current_regime == 'Bear':
            signal = "SHORT"
            recommendation = "SELL"
        
        return {
            'ticker': ticker,
            'regime': current_regime,
            'signal': signal,
            'price': current_price,
            'num_trades': num_trades,
            'recommendation': recommendation,
            'total_return': results['total_return_pct']
        }
    except Exception as e:
        return None


def portfolio_page():
    """Portfolio watchlist page showing multiple tickers"""
    st.title("📊 Portfolio Watchlist")
    st.markdown("Track multiple stocks with regime analysis")
    
    # Initialize portfolio in session state
    if 'portfolio_tickers' not in st.session_state:
        st.session_state.portfolio_tickers = ['AAPL', 'TSLA', 'NVDA', 'MSFT', 'AMD']
    
    # Sidebar for managing portfolio
    st.sidebar.header("Manage Portfolio")
    
    # Add ticker to portfolio
    new_ticker = st.sidebar.text_input(
        "Add Ticker",
        placeholder="Enter ticker symbol",
        max_chars=10
    ).upper().strip()
    
    if st.sidebar.button("➕ Add to Portfolio"):
        if new_ticker and new_ticker not in st.session_state.portfolio_tickers:
            st.session_state.portfolio_tickers.append(new_ticker)
            st.sidebar.success(f"Added {new_ticker}!")
        elif new_ticker in st.session_state.portfolio_tickers:
            st.sidebar.warning(f"{new_ticker} already in portfolio")
    
    # Remove ticker
    if st.session_state.portfolio_tickers:
        ticker_to_remove = st.sidebar.selectbox(
            "Remove Ticker",
            st.session_state.portfolio_tickers
        )
        if st.sidebar.button("➖ Remove"):
            st.session_state.portfolio_tickers.remove(ticker_to_remove)
            st.sidebar.success(f"Removed {ticker_to_remove}!")
    
    # Refresh button
    refresh_portfolio = st.sidebar.button("🔄 Refresh All")
    
    # Display current portfolio
    st.sidebar.markdown(f"**Portfolio ({len(st.session_state.portfolio_tickers)} stocks)**")
    st.sidebar.write(", ".join(st.session_state.portfolio_tickers))
    
    # Main content
    if not st.session_state.portfolio_tickers:
        st.info("👆 Add tickers to your portfolio using the sidebar")
        return
    
    if refresh_portfolio or 'portfolio_data' not in st.session_state:
        portfolio_results = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, ticker in enumerate(st.session_state.portfolio_tickers):
            status_text.text(f"Analyzing {ticker}... ({idx+1}/{len(st.session_state.portfolio_tickers)})")
            
            result = get_quick_analysis(ticker)
            if result:
                portfolio_results.append(result)
            
            progress_bar.progress((idx + 1) / len(st.session_state.portfolio_tickers))
        
        status_text.empty()
        progress_bar.empty()
        
        st.session_state.portfolio_data = portfolio_results
    
    # Display results table
    if 'portfolio_data' in st.session_state and st.session_state.portfolio_data:
        df_portfolio = pd.DataFrame(st.session_state.portfolio_data)
        
        # Format the dataframe for display
        df_display = df_portfolio.copy()
        df_display.columns = ['Ticker', 'Regime', 'Signal', 'Price', 'Trades', 'Action', 'Return %']
        df_display['Price'] = df_display['Price'].apply(lambda x: f"${x:.2f}")
        df_display['Return %'] = df_display['Return %'].apply(lambda x: f"{x:.2f}%")
        
        # Color code the action column
        def highlight_action(row):
            if row['Action'] == 'BUY':
                return ['background-color: #d4edda'] * len(row)
            elif row['Action'] == 'SELL':
                return ['background-color: #f8d7da'] * len(row)
            else:
                return ['background-color: #fff3cd'] * len(row)
        
        st.dataframe(
            df_display.style.apply(highlight_action, axis=1),
            use_container_width=True,
            hide_index=True
        )
        
        # Summary stats
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        buy_signals = len([r for r in st.session_state.portfolio_data if r['recommendation'] == 'BUY'])
        sell_signals = len([r for r in st.session_state.portfolio_data if r['recommendation'] == 'SELL'])
        hold_signals = len([r for r in st.session_state.portfolio_data if r['recommendation'] == 'HOLD'])
        avg_return = np.mean([r['total_return'] for r in st.session_state.portfolio_data])
        
        with col1:
            st.metric("🟢 BUY Signals", buy_signals)
        with col2:
            st.metric("🔴 SELL Signals", sell_signals)
        with col3:
            st.metric("⚪ HOLD Signals", hold_signals)
        with col4:
            st.metric("📊 Avg Return", f"{avg_return:.2f}%")
    else:
        st.warning("No data available. Click 'Refresh All' to analyze your portfolio.")


def main():
    """Main Streamlit app"""
    
    st.title("📈 Regime-Based Trading App")
    st.markdown("Professional HMM-based trading system with multi-factor confirmation")
    
    # Page selection
    page = st.sidebar.radio(
        "Navigation",
        ["📊 Portfolio Watchlist", "🔍 Single Stock Analysis"],
        index=0
    )
    
    st.sidebar.markdown("---")
    
    # Route to appropriate page
    if page == "📊 Portfolio Watchlist":
        portfolio_page()
        return
    
    # Continue with single stock analysis page
    # Initialize session state for auto-refresh
    if 'last_run_time' not in st.session_state:
        st.session_state.last_run_time = None
    if 'auto_refresh' not in st.session_state:
        st.session_state.auto_refresh = False
    
    # Sidebar for controls
    st.sidebar.header("Configuration")
    
    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox(
        "🔄 Auto-refresh every 1 hour",
        value=st.session_state.auto_refresh,
        help="Automatically run backtest every hour"
    )
    st.session_state.auto_refresh = auto_refresh
    
    # Show last update time and countdown
    if st.session_state.last_run_time:
        time_since_last = datetime.now() - st.session_state.last_run_time
        minutes_since = int(time_since_last.total_seconds() / 60)
        next_refresh_in = 60 - minutes_since
        
        if next_refresh_in > 0:
            st.sidebar.info(f"⏱️ Next refresh in: {next_refresh_in} minutes")
        else:
            st.sidebar.info(f"⏱️ Refreshing now...")
    
    # Ticker selection with custom input option
    ticker_input_method = st.sidebar.radio(
        "Ticker Selection",
        ["📋 Select from list", "✍️ Enter custom"],
        horizontal=True
    )
    
    if ticker_input_method == "📋 Select from list":
        selected_ticker = st.sidebar.selectbox(
            "Select Ticker",
            [
                'AAPL', 'AFJK',
                'ABVX', 'AAP', 'ADMA', 'AGEN', 'CELC', 'CNC', 'CONI', 'DAVE', 'FIVN', 'GLUE',
                'LUMN', 'LWAY', 'MGPI', 'NNNN', 'NVCR', 'NVDL','OIS', 'ODD', 'PEGA', 'QURE', 'RXO',
                'SBUX', 'SERV', 'SOGP', 'TIL', 'TREE','TSLA', 'UPST','VNDA', 'WLDN', 'ZEPP',
                'MSFT', 'GOOGL', 'META', 'AMZN', 'NVDA', 'AMD', 'INTC'
            ]
        )
    else:
        selected_ticker = st.sidebar.text_input(
            "Enter Ticker Symbol",
            value="AAPL",
            help="Enter any valid stock ticker symbol (e.g., AAPL, TSLA, MSFT)",
            max_chars=10
        ).upper().strip()
        
        if not selected_ticker:
            st.sidebar.warning("⚠️ Please enter a ticker symbol")
            return
    
    days_history = st.sidebar.slider(
        "Historical Data (days)",
        min_value=30,
        max_value=730,
        value=180,
        step=30
    )
    
    initial_capital = st.sidebar.number_input(
        "Initial Capital ($)",
        min_value=100,
        max_value=100000,
        value=2000,
        step=100
    )
    
    leverage = st.sidebar.number_input(
        "Leverage",
        min_value=1.0,
        max_value=10.0,
        value=2.5,
        step=0.5
    )
    
    run_backtest = st.sidebar.button(
        "🚀 Run Backtest",
        key="backtest_button"
    )
    
    # Auto-refresh logic: trigger backtest if enabled and 1 hour has passed
    should_run = run_backtest
    if auto_refresh and st.session_state.last_run_time:
        time_since_last = datetime.now() - st.session_state.last_run_time
        if time_since_last >= timedelta(hours=1):
            should_run = True
            st.sidebar.success("🔄 Auto-refreshing...")
    elif auto_refresh and not st.session_state.last_run_time:
        # First time with auto-refresh enabled
        should_run = True
    
    if should_run:
        # Update last run time
        st.session_state.last_run_time = datetime.now()
        
        with st.spinner(f"Loading data for {selected_ticker}..."):
            # Load data
            data = load_ticker_data(selected_ticker, days=days_history)
            
            if data is None or len(data) < 100:
                st.error(f"Unable to load sufficient data for {selected_ticker}")
                return
            
            # Calculate features and indicators
            with st.spinner("Calculating features and indicators..."):
                df = calculate_features(data).copy()
                df = add_all_indicators(df)
            
            # Train HMM
            with st.spinner("Training HMM model..."):
                regime_detector = RegimeDetector(n_components=7)
                train_features = get_training_features(df)
                
                if not regime_detector.train(train_features):
                    st.error("Failed to train HMM model")
                    return
                
                # Predict regimes
                regimes = regime_detector.get_all_regime_timeseries(train_features)
                df['Regime'] = regimes
            
            # Run backtest
            with st.spinner("Running backtest simulation..."):
                backtester = RegimeBasedBacktester(
                    initial_capital=initial_capital,
                    leverage=leverage
                )
                results = backtester.run_backtest(data, ticker=selected_ticker)
            
            if results is None:
                st.error("Backtest failed. Please try again.")
                return
            
            # Display results
            st.success("✅ Backtest completed successfully!")
            
            # Top section with current signal and regime
            col1, col2, col3 = st.columns(3)
            
            with col1:
                current_regime = str(df['Regime'].iloc[-1]).strip()
                regime_color = get_regime_color(current_regime)
                st.markdown(
                    f"<h3 style='color: {regime_color}'>Current Regime: {current_regime}</h3>",
                    unsafe_allow_html=True
                )
            
            with col2:
                current_signal = "🟢 LONG" if results['num_trades'] > 0 else "⚪ CASH"
                st.markdown(f"<h3>Signal: {current_signal}</h3>", unsafe_allow_html=True)
            
            with col3:
                current_price = float(df['Close'].iloc[-1])
                st.markdown(f"<h3>Current Price: ${current_price:.2f}</h3>", unsafe_allow_html=True)
            
            # Last trade action section
            if 'trades' in results and len(results['trades']) > 0:
                try:
                    last_trade = results['trades'].iloc[-1]
                    last_action = str(last_trade['action']).upper()
                    last_price = float(last_trade['price'])
                    last_time = pd.to_datetime(last_trade['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                    
                    action_color = '#09ab3b' if last_action == 'BUY' else '#ff2b6e'
                    action_emoji = '📈' if last_action == 'BUY' else '📉'
                    
                    st.markdown(
                        f"<div style='background-color: {action_color}; padding: 15px; border-radius: 8px; text-align: center; margin-top: 10px;'>"
                        f"<h3 style='color: white; margin: 0;'>{action_emoji} Last Action: <b>{last_action}</b></h3>"
                        f"<h4 style='color: white; margin: 5px 0;'>Price: ${last_price:.2f}</h4>"
                        f"<p style='color: white; margin: 0;'>{last_time}</p>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                except:
                    pass
            
            st.divider()
            
            # Chart
            st.subheader("📊 Interactive Candlestick Chart")
            trades_df = results['trades'] if 'trades' in results and len(results['trades']) > 0 else None
            fig = create_candlestick_chart(df, selected_ticker, trades_df=trades_df)
            st.plotly_chart(fig, use_container_width=True)
            
            # Trade History Grid
            if trades_df is not None and len(trades_df) > 0:
                st.subheader("📋 Trade History")
                
                # Create a more readable trade history display
                trade_history = []
                for _, trade in trades_df.iterrows():
                    try:
                        trade_history.append({
                            'Time': pd.to_datetime(trade['timestamp']),
                            'Action': str(trade['action']).upper(),
                            'Price': f"${float(trade['price']):.2f}",
                            'Shares': f"{abs(float(trade.get('shares', 0))):.2f}",
                            'Regime': str(trade.get('regime', 'N/A')).strip(),
                            'Reason': str(trade.get('reason', 'N/A'))[:50]
                        })
                    except:
                        pass
                
                if trade_history:
                    trade_df_display = pd.DataFrame(trade_history)
                    st.dataframe(trade_df_display, use_container_width=True)
            
            st.divider()
            
            # Metrics
            st.subheader("📈 Performance Metrics")
            create_metrics_chart(results)
            
            st.divider()
            
            # Detailed metrics
            st.subheader("📋 Detailed Results")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Capital & Returns**")
                st.write(f"Initial Capital: ${results['initial_capital']:.2f}")
                st.write(f"Final Equity: ${results['final_equity']:.2f}")
                st.write(f"Total Return: {results['total_return_pct']:.2f}%")
                st.write(f"Buy & Hold Return: {results['buy_hold_return_pct']:.2f}%")
                st.write(f"Alpha: {results['alpha']:.2f}%")
            
            with col2:
                st.write("**Risk Metrics**")
                st.write(f"Max Drawdown: {results['max_drawdown']:.2f}%")
                st.write(f"Win Rate: {results['win_rate']:.1f}%")
                st.write(f"Number of Trades: {results['num_trades']}")
            
            # Trade log
            if len(results['trades']) > 0:
                st.subheader("📜 Trade Log")
                trades_display = results['trades'].copy()
                trades_display['timestamp'] = trades_display['timestamp'].astype(str)
                st.dataframe(trades_display, use_container_width=True)
            
            # Regime distribution
            st.subheader("📊 Regime Distribution")
            regime_counts = df['Regime'].value_counts()
            
            fig_regime = go.Figure(
                data=[go.Pie(
                    labels=regime_counts.index,
                    values=regime_counts.values,
                    marker=dict(colors=['#09ab3b', '#ff2b6e', '#ffa500'])
                )]
            )
            fig_regime.update_layout(title="Regime Distribution")
            st.plotly_chart(fig_regime, use_container_width=True)
    
    else:
        # Display welcome message
        st.info("""
        ### Welcome to the Regime-Based Trading App! 👋
        
        **How to use:**
        1. Select a ticker from the sidebar
        2. Configure your parameters
        3. Click "Run Backtest" to analyze the strategy
        
        **Features:**
        - 🤖 Hidden Markov Model (HMM) for regime detection
        - 📊 8-condition voting system for trade confirmation
        - 💰 2.5× leverage simulation
        - 📈 Comprehensive performance metrics
        - 🛡️ Risk management with 48-hour cooldown
        
        **Supported Tickers:**
        - Blue chips: AAPL, MSFT, GOOGL, TSLA, NVDA
        - Micro-caps: ABVX, AAP, ADMA, AGEN, CELC, and many more...
        """)
    
    # Auto-refresh mechanism: continuously poll to check if refresh is needed
    if auto_refresh:
        time.sleep(5)  # Check every 5 seconds
        st.rerun()


if __name__ == "__main__":
    main()
