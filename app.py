import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="TradingView - Advanced Charts & Trading Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== GENERATE REALISTIC TRADING DATA =====
def generate_live_data(symbol, periods=200):
    np.random.seed(hash(symbol) % 100)
    
    base_prices = {
        "AAPL": 180, "TSLA": 250, "MSFT": 420, 
        "BTCUSD": 65000, "SPX": 5200, "GOOGL": 2800
    }
    base_price = base_prices.get(symbol, 100)
    
    # Generate realistic price movement
    dates = [datetime.now() - timedelta(minutes=x) for x in range(periods, 0, -1)]
    returns = np.random.normal(0, 0.002, periods)  # 0.2% daily volatility
    prices = base_price * np.exp(np.cumsum(returns))
    
    # Create OHLC data
    opens = prices * (1 + np.random.uniform(-0.001, 0.001, periods))
    highs = prices * (1 + np.abs(np.random.normal(0, 0.0015, periods)))
    lows = prices * (1 - np.abs(np.random.normal(0, 0.0015, periods)))
    closes = prices * (1 + np.random.normal(0, 0.001, periods))
    
    df = pd.DataFrame({
        'time': dates,
        'open': opens, 'high': highs, 'low': lows, 'close': closes,
        'volume': np.random.randint(1000000, 5000000, periods)
    })
    
    return df

# ===== INITIALIZE SESSION STATE =====
if 'current_symbol' not in st.session_state:
    st.session_state.current_symbol = "AAPL"
if 'chart_data' not in st.session_state:
    st.session_state.chart_data = generate_live_data("AAPL")
if 'live_mode' not in st.session_state:
    st.session_state.live_mode = False

# ===== SIDEBAR - TRADINGVIEW STYLE =====
with st.sidebar:
    st.title("📊 TradingView")
    st.markdown("---")
    
    # Watchlist
    st.subheader("📍 Watchlist")
    symbols = {
        "AAPL": "Apple Inc.", "TSLA": "Tesla Inc.", "MSFT": "Microsoft",
        "BTCUSD": "Bitcoin/USD", "SPX": "S&P 500", "GOOGL": "Google"
    }
    
    for symbol, name in symbols.items():
        if st.button(f"{symbol} - {name}", key=f"btn_{symbol}", use_container_width=True):
            st.session_state.current_symbol = symbol
            st.session_state.chart_data = generate_live_data(symbol)
            st.rerun()
    
    st.markdown("---")
    
    # Chart Controls
    st.subheader("⚙️ Chart Settings")
    chart_type = st.selectbox("Chart Type", ["Candlestick", "Line", "Area"])
    timeframe = st.selectbox("Timeframe", ["1m", "5m", "15m", "1H", "4H", "1D"])
    
    st.markdown("---")
    
    # Indicators
    st.subheader("📈 Indicators")
    st.checkbox("Moving Average (50)")
    st.checkbox("RSI (14)")
    st.checkbox("MACD")
    st.checkbox("Bollinger Bands")
    
    st.markdown("---")
    
    # Account Summary
    st.subheader("💼 Portfolio")
    st.metric("Account Value", "$125,430.25", "+2.3%")
    st.write("**AAPL:** 15 shares")
    st.write("**Cash:** $12,500.00")

# ===== MAIN TRADING INTERFACE =====
st.header(f"📈 {st.session_state.current_symbol} - Live Chart")

# Current price info
current_data = st.session_state.chart_data.iloc[-1]
prev_data = st.session_state.chart_data.iloc[-2]
price_change = current_data['close'] - prev_data['close']
price_change_pct = (price_change / prev_data['close']) * 100

# Price metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        "Current Price", 
        f"${current_data['close']:.2f}", 
        f"{price_change_pct:+.2f}%"
    )
with col2:
    st.metric("Today's High", f"${current_data['high']:.2f}")
with col3:
    st.metric("Today's Low", f"${current_data['low']:.2f}")
with col4:
    st.metric("Volume", f"{current_data['volume']:,}")

# Interactive Chart
fig = go.Figure()

if chart_type == "Candlestick":
    fig.add_trace(go.Candlestick(
        x=st.session_state.chart_data['time'],
        open=st.session_state.chart_data['open'],
        high=st.session_state.chart_data['high'],
        low=st.session_state.chart_data['low'],
        close=st.session_state.chart_data['close'],
        name=st.session_state.current_symbol
    ))
else:
    fig.add_trace(go.Scatter(
        x=st.session_state.chart_data['time'],
        y=st.session_state.chart_data['close'],
        mode='lines',
        name=st.session_state.current_symbol,
        fill='tozeroy' if chart_type == "Area" else None
    ))

fig.update_layout(
    height=500,
    xaxis_rangeslider_visible=False,
    template="plotly_white",
    margin=dict(l=20, r=20, t=30, b=20)
)

st.plotly_chart(fig, use_container_width=True)

# Live Trading Controls
st.subheader("🎯 Trading Panel")

col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("▶️ Start Live Data" if not st.session_state.live_mode else "⏸️ Pause Live"):
        st.session_state.live_mode = not st.session_state.live_mode

with col2:
    if st.button("🔄 Refresh Data"):
        st.session_state.chart_data = generate_live_data(st.session_state.current_symbol)
        st.rerun()

with col3:
    # Order Entry
    order_col1, order_col2, order_col3, order_col4 = st.columns(4)
    with order_col1:
        order_type = st.selectbox("Type", ["Market", "Limit"])
    with order_col2:
        quantity = st.number_input("Qty", min_value=1, value=100)
    with order_col3:
        if st.button("🟢 BUY", type="primary", use_container_width=True):
            st.success(f"BUY order: {quantity} {st.session_state.current_symbol} @ ${current_data['close']:.2f}")
    with order_col4:
        if st.button("🔴 SELL", type="secondary", use_container_width=True):
            st.error(f"SELL order: {quantity} {st.session_state.current_symbol} @ ${current_data['close']:.2f}")

# Live data simulation
if st.session_state.live_mode:
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(20):
        if not st.session_state.live_mode:
            break
            
        # Generate new price
        last_close = st.session_state.chart_data['close'].iloc[-1]
        new_return = np.random.normal(0, 0.001)  # 0.1% change
        new_close = last_close * (1 + new_return)
        
        new_row = pd.DataFrame({
            'time': [datetime.now()],
            'open': [last_close],
            'high': [max(last_close, new_close) * 1.001],
            'low': [min(last_close, new_close) * 0.999],
            'close': [new_close],
            'volume': [np.random.randint(1000000, 3000000)]
        })
        
        st.session_state.chart_data = pd.concat([
            st.session_state.chart_data.iloc[1:],
            new_row
        ], ignore_index=True)
        
        progress_bar.progress((i + 1) / 20)
        status_text.text(f"🔄 Live updating... {i + 1}/20")
        time.sleep(0.5)
    
    progress_bar.empty()
    status_text.empty()
    st.session_state.live_mode = False
    st.rerun()

# Market News
st.subheader("📰 Market News")
news_items = [
    ("Apple announces breakthrough in AI technology", "2 min ago", "AAPL"),
    ("Federal Reserve maintains interest rates", "15 min ago", "SPX"),
    ("Bitcoin ETF volumes hit record high", "30 min ago", "BTCUSD")
]

for headline, timestamp, symbol in news_items:
    st.write(f"**{headline}** · `{timestamp}` · #{symbol}")

st.markdown("---")
st.caption("TradingView Prototype · Real-time trading platform · Data simulated for demonstration")

