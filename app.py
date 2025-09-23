import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# Page setup
st.set_page_config(
    page_title="TradingView Pro - Advanced Trading Platform",
    layout="wide"
)

# Advanced CSS for TradingView-like interface
st.markdown("""
<style>
    /* Main TradingView Theme */
    .main { 
        background-color: #131722; 
        color: #d1d4dc;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background-color: #1e222d;
        color: #d1d4dc;
    }
    
    /* Professional Cards */
    .card {
        background: #1e222d;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #2962ff;
    }
    
    /* Watchlist Items */
    .watchlist-item {
        background: #2a2e39;
        padding: 12px;
        margin: 8px 0;
        border-radius: 6px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .watchlist-item:hover {
        background: #3a3e49;
        transform: translateX(5px);
    }
    
    /* Chart Container */
    .chart-container {
        background: #131722;
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
    }
    
    /* Trading Panel */
    .trading-panel {
        background: #1e222d;
        padding: 20px;
        border-radius: 8px;
        margin: 20px 0;
    }
    
    /* Colors */
    .green { color: #26a69a; font-weight: 600; }
    .red { color: #ef5350; font-weight: 600; }
    .blue { color: #2962ff; }
    
    /* Buttons */
    .stButton>button {
        background-color: #2962ff;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: 500;
    }
    
    .timeframe-btn {
        background: #2a2e39;
        color: #d1d4dc;
        border: 1px solid #3a3e49;
        border-radius: 4px;
        padding: 8px 12px;
        margin: 2px;
        cursor: pointer;
    }
    
    .timeframe-btn.active {
        background: #2962ff;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Generate advanced trading data with OHLC
def generate_advanced_data(symbol, points=200):
    np.random.seed(hash(symbol) % 100)
    
    base_prices = {
        "AAPL": 180, "TSLA": 250, "MSFT": 420, "GOOGL": 2800,
        "BTCUSD": 65000, "SPX": 5200, "NVDA": 120, "AMZN": 3500
    }
    base_price = base_prices.get(symbol, 100)
    
    dates = [datetime.now() - timedelta(minutes=x) for x in range(points, 0, -1)]
    
    # Generate realistic price movement with volatility
    returns = np.random.normal(0, 0.002, points)  # More realistic returns
    prices = base_price * np.exp(np.cumsum(returns))
    
    # Create OHLC data
    opens = []
    highs = []
    lows = []
    closes = []
    
    for i in range(points):
        if i == 0:
            open_price = base_price
        else:
            open_price = closes[i-1] if closes else base_price
            
        close_price = prices[i]
        high_price = max(open_price, close_price) * (1 + abs(np.random.normal(0, 0.005)))
        low_price = min(open_price, close_price) * (1 - abs(np.random.normal(0, 0.005)))
        
        opens.append(open_price)
        highs.append(high_price)
        lows.append(low_price)
        closes.append(close_price)
    
    df = pd.DataFrame({
        'timestamp': dates,
        'open': opens, 'high': highs, 'low': lows, 'close': closes,
        'volume': np.random.randint(1000000, 5000000, points)
    })
    
    return df

# Calculate technical indicators
def calculate_indicators(df):
    # Simple Moving Average
    df['sma_20'] = df['close'].rolling(window=20).mean()
    df['sma_50'] = df['close'].rolling(window=50).mean()
    
    # RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    return df

# Initialize session state
if 'current_symbol' not in st.session_state:
    st.session_state.current_symbol = "AAPL"
if 'chart_data' not in st.session_state:
    st.session_state.chart_data = generate_advanced_data("AAPL")
if 'is_live' not in st.session_state:
    st.session_state.is_live = False
if 'timeframe' not in st.session_state:
    st.session_state.timeframe = "1H"
if 'chart_type' not in st.session_state:
    st.session_state.chart_type = "Line"
if 'indicators' not in st.session_state:
    st.session_state.indicators = {"SMA": True, "RSI": False}

# Calculate indicators
st.session_state.chart_data = calculate_indicators(st.session_state.chart_data)

# Sidebar - Advanced TradingView Interface
with st.sidebar:
    st.markdown("<h1 style='color: #2962ff;'>TradingView Pro</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Advanced Watchlist
    st.markdown("### 📈 Advanced Watchlist")
    
    watchlist_data = {
        "AAPL": {"name": "Apple Inc.", "price": 182.35, "change": +1.25, "change_pct": +0.69, "volume": "25.3M"},
        "TSLA": {"name": "Tesla Inc.", "price": 248.90, "change": +5.60, "change_pct": +2.30, "volume": "18.7M"},
        "MSFT": {"name": "Microsoft", "price": 421.80, "change": -2.30, "change_pct": -0.54, "volume": "12.1M"},
        "GOOGL": {"name": "Google", "price": 2798.30, "change": +15.80, "change_pct": +0.57, "volume": "8.9M"},
        "BTCUSD": {"name": "Bitcoin", "price": 65123.45, "change": +1234.56, "change_pct": +1.93, "volume": "32.5B"}
    }
    
    for symbol, data in watchlist_data.items():
        change_color = "green" if data["change"] >= 0 else "red"
        change_icon = "▲" if data["change"] >= 0 else "▼"
        
        if st.button(
            f"""**{symbol}** - ${data['price']:.2f}  
            <span style='color: {change_color}'>{change_icon} {data['change_pct']:.2f}%</span>""",
            key=f"watch_{symbol}", 
            use_container_width=True
        ):
            st.session_state.current_symbol = symbol
            st.session_state.chart_data = generate_advanced_data(symbol)
            st.session_state.chart_data = calculate_indicators(st.session_state.chart_data)
            st.rerun()
    
    st.markdown("---")
    
    # Advanced Chart Controls
    st.markdown("### ⚙️ Chart Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        chart_type = st.selectbox("Chart Type", ["Line", "Candlestick", "Area", "Heikin Ashi"])
    with col2:
        timeframe = st.selectbox("Timeframe", ["1m", "5m", "15m", "30m", "1H", "4H", "1D", "1W"])
    
    st.markdown("---")
    
    # Technical Indicators Panel
    st.markdown("### 📊 Technical Indicators")
    
    indicators = {
        "Moving Average (20)": "sma_20",
        "Moving Average (50)": "sma_50", 
        "RSI (14)": "rsi",
        "Bollinger Bands": "bb",
        "MACD": "macd",
        "Volume Profile": "volume"
    }
    
    for name, key in indicators.items():
        if st.checkbox(name, value=(name in ["Moving Average (20)"])):
            if name == "RSI (14)":
                st.slider("RSI Levels", 20, 80, (30, 70), key="rsi_levels")
    
    st.markdown("---")
    
    # Drawing Tools
    st.markdown("### 🛠️ Drawing Tools")
    drawing_tools = ["Trend Line", "Horizontal Line", "Fibonacci", "Text", "Arrow"]
    for tool in drawing_tools:
        st.button(f"• {tool}", key=f"draw_{tool}", use_container_width=True)
    
    st.markdown("---")
    
    # Market Overview
    st.markdown("### 🌍 Market Overview")
    markets = [
        ("Crypto Cap", "3.91T", "-1.26%", "red"),
        ("DXY", "97.789", "+0.15%", "green"),
        ("Oil", "62.77", "+0.59%", "green"),
        ("Gold", "2345.60", "-0.45%", "red")
    ]
    
    for name, value, change, color in markets:
        st.markdown(f"**{name}**: {value} <span class='{color}'>{change}</span>", unsafe_allow_html=True)

# Main Trading Interface
st.markdown(f"## 📈 {st.session_state.current_symbol} - {watchlist_data[st.session_state.current_symbol]['name']}")

# Advanced Price Header
current_data = st.session_state.chart_data.iloc[-1]
prev_data = st.session_state.chart_data.iloc[-2]
price_change = current_data['close'] - prev_data['close']
price_change_pct = (price_change / prev_data['close']) * 100

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.metric("Price", f"${current_data['close']:.2f}", f"{price_change_pct:+.2f}%")
with col2:
    st.metric("Open", f"${current_data['open']:.2f}")
with col3:
    st.metric("High", f"${current_data['high']:.2f}")
with col4:
    st.metric("Low", f"${current_data['low']:.2f}")
with col5:
    st.metric("Volume", f"{current_data['volume']:,}")
with col6:
    st.metric("Change", f"${price_change:+.2f}", f"{price_change_pct:+.2f}%")

# Timeframe Selection Buttons
st.markdown("### Timeframe")
timeframes = ["1m", "5m", "15m", "30m", "1H", "4H", "1D", "1W"]
cols = st.columns(8)
for i, tf in enumerate(timeframes):
    with cols[i]:
        if st.button(tf, key=f"tf_{tf}", use_container_width=True):
            st.session_state.timeframe = tf
            st.info(f"Switched to {tf} timeframe")

# Advanced Chart Display
st.markdown("### Advanced Chart")
chart_container = st.container()

with chart_container:
    # Display main price chart
    if chart_type == "Candlestick":
        # For candlestick, we'll use a line chart as fallback
        chart_data = st.session_state.chart_data[['timestamp', 'open', 'high', 'low', 'close']].set_index('timestamp')
        st.line_chart(chart_data, height=500)
    else:
        chart_data = st.session_state.chart_data.set_index('timestamp')[['close']]
        if chart_type == "Area":
            st.area_chart(chart_data, height=500)
        else:
            st.line_chart(chart_data, height=500)
    
    # Display SMA indicators if enabled
    if st.session_state.indicators.get("SMA", True):
        sma_data = st.session_state.chart_data.set_index('timestamp')[['sma_20', 'sma_50']]
        st.line_chart(sma_data, height=200)

# Advanced Trading Panel
st.markdown("### 🎯 Advanced Trading Panel")

tcol1, tcol2, tcol3, tcol4, tcol5, tcol6, tcol7 = st.columns(7)

with tcol1:
    live_icon = "⏸️" if st.session_state.is_live else "▶️"
    if st.button(live_icon, help="Live Trading Mode", use_container_width=True):
        st.session_state.is_live = not st.session_state.is_live

with tcol2:
    if st.button("🔄", help="Refresh Data", use_container_width=True):
        st.session_state.chart_data = generate_advanced_data(st.session_state.current_symbol)
        st.session_state.chart_data = calculate_indicators(st.session_state.chart_data)
        st.rerun()

with tcol3:
    order_type = st.selectbox("Type", ["Market", "Limit", "Stop", "Stop Limit"], label_visibility="collapsed")

with tcol4:
    quantity = st.number_input("Quantity", min_value=1, value=100, label_visibility="collapsed")

with tcol5:
    price = st.number_input("Price", value=float(current_data['close']), label_visibility="collapsed")

with tcol6:
    if st.button("🟢 BUY", type="primary", use_container_width=True):
        order_value = quantity * current_data['close']
        st.success(f"✅ BUY {quantity} {st.session_state.current_symbol} @ ${current_data['close']:.2f} | Total: ${order_value:,.2f}")

with tcol7:
    if st.button("🔴 SELL", type="secondary", use_container_width=True):
        order_value = quantity * current_data['close']
        st.error(f"✅ SELL {quantity} {st.session_state.current_symbol} @ ${current_data['close']:.2f} | Total: ${order_value:,.2f}")

# Order Book Simulation
st.markdown("### 📊 Order Book")
ob_col1, ob_col2 = st.columns(2)

with ob_col1:
    st.markdown("**Bids (Buy Orders)**")
    for i in range(5):
        price_level = current_data['close'] * (1 - (i+1)*0.001)
        size = np.random.randint(100, 1000)
        st.write(f"${price_level:.2f} | {size} shares")

with ob_col2:
    st.markdown("**Asks (Sell Orders)**")
    for i in range(5):
        price_level = current_data['close'] * (1 + (i+1)*0.001)
        size = np.random.randint(100, 1000)
        st.write(f"${price_level:.2f} | {size} shares")

# Advanced Live Data Simulation
if st.session_state.is_live:
    progress_bar = st.progress(0)
    status_text = st.empty()
    live_data = st.empty()
    
    for i in range(15):
        if not st.session_state.is_live:
            break
            
        # Generate new realistic data point
        last_close = st.session_state.chart_data['close'].iloc[-1]
        new_return = np.random.normal(0, 0.0015)  # Realistic volatility
        new_close = last_close * (1 + new_return)
        
        new_row = pd.DataFrame({
            'timestamp': [datetime.now()],
            'open': [last_close],
            'high': [max(last_close, new_close) * (1 + abs(np.random.normal(0, 0.002)))],
            'low': [min(last_close, new_close) * (1 - abs(np.random.normal(0, 0.002)))],
            'close': [new_close],
            'volume': [np.random.randint(1000000, 3000000)]
        })
        
        st.session_state.chart_data = pd.concat([
            st.session_state.chart_data.iloc[1:],
            new_row
        ], ignore_index=True)
        
        # Recalculate indicators
        st.session_state.chart_data = calculate_indicators(st.session_state.chart_data)
        
        progress_bar.progress((i + 1) / 15)
        current_change = (new_close - last_close) / last_close * 100
        status_text.text(f"📡 Live Trading: {st.session_state.current_symbol} | Price: ${new_close:.2f} | Change: {current_change:+.2f}%")
        time.sleep(0.8)
    
    progress_bar.empty()
    status_text.empty()
    st.session_state.is_live = False
    st.rerun()

# Market Depth & Analytics
st.markdown("### 📈 Market Analytics")

ana_col1, ana_col2, ana_col3 = st.columns(3)

with ana_col1:
    st.metric("RSI (14)", f"{st.session_state.chart_data['rsi'].iloc[-1]:.1f}")
    st.metric("Volatility", "2.3%")
    st.metric("Market Sentiment", "Bullish")

with ana_col2:
    st.metric("24h Volume", "25.3M")
    st.metric("Avg. Spread", "0.02%")
    st.metric("Liquidity", "High")

with ana_col3:
    st.metric("Support Level", f"${current_data['close']*0.98:.2f}")
    st.metric("Resistance Level", f"${current_data['close']*1.02:.2f}")
    st.metric("Trend", "Upward")

# News & Alerts
st.markdown("### 📰 Real-time News & Alerts")

news_items = [
    {"symbol": "AAPL", "headline": "Apple announces breakthrough AI chip", "impact": "High", "sentiment": "Bullish"},
    {"symbol": "TSLA", "headline": "Tesla Model 3 deliveries beat estimates", "impact": "Medium", "sentiment": "Bullish"},
    {"symbol": "BTCUSD", "headline": "Bitcoin ETF volumes hit record high", "impact": "High", "sentiment": "Bullish"}
]

for news in news_items:
    with st.expander(f"🚨 {news['symbol']}: {news['headline']}"):
        st.write(f"**Impact:** {news['impact']} | **Sentiment:** {news['sentiment']}")
        st.write("Market analysts expect positive price movement following this news.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6a737d;'>
    <p>TradingView Pro • Advanced Trading Platform • Real-time Data • Professional Charts</p>
    <p>© 2025 TradingView Pro. All rights reserved. Not financial advice.</p>
</div>
""", unsafe_allow_html=True)
