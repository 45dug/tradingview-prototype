import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ===== TRADINGVIEW STYLE CSS =====
st.markdown("""
<style>
    /* TradingView Dark Theme */
    .main {
        background-color: #131722;
        color: #d1d4dc;
    }
    .sidebar .sidebar-content {
        background-color: #1e222d;
        color: #d1d4dc;
    }
    /* Chart Container */
    .chart-container {
        background-color: #131722;
        border-radius: 4px;
        padding: 10px;
        margin-bottom: 10px;
    }
    /* Watchlist Items */
    .watchlist-item {
        padding: 8px;
        margin: 4px 0;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    .watchlist-item:hover {
        background-color: #2a2e39;
    }
    /* Buttons */
    .stButton>button {
        background-color: #2962ff;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: 500;
    }
    .stButton>button:hover {
        background-color: #1e53e5;
    }
    /* Green/Red colors */
    .green { color: #26a69a; }
    .red { color: #ef5350; }
    
    /* Make charts dark */
    .stChart {
        background-color: #131722;
        border-radius: 8px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="TradingView Clone",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== SAMPLE DATA =====
def generate_price_data(symbol, periods=100):
    np.random.seed(hash(symbol) % 100)
    
    base_prices = {"AAPL": 180, "MSFT": 420, "TSLA": 250, "BTCUSD": 65000}
    base_price = base_prices.get(symbol, 100)
    
    dates = [datetime.now() - timedelta(minutes=x) for x in range(periods, 0, -1)]
    prices = base_price + np.cumsum(np.random.randn(periods) * 0.8)
    
    return pd.DataFrame({
        'Time': dates,
        'Price': prices
    })

# ===== WATCHLIST DATA =====
WATCHLIST = {
    "AAPL": {"name": "Apple Inc.", "price": 180.25, "change": +1.25},
    "MSFT": {"name": "Microsoft", "price": 421.80, "change": -2.30},
    "TSLA": {"name": "Tesla Inc.", "price": 248.90, "change": +5.60},
    "BTCUSD": {"name": "Bitcoin", "price": 65123.45, "change": +1234.56}
}

# ===== SESSION STATE =====
if 'current_symbol' not in st.session_state:
    st.session_state.current_symbol = "AAPL"
if 'price_data' not in st.session_state:
    st.session_state.price_data = generate_price_data("AAPL")

# ===== SIDEBAR - TRADINGVIEW STYLE =====
with st.sidebar:
    st.markdown("<h1 style='color: #2962ff; margin-bottom: 30px;'>TradingView</h1>", unsafe_allow_html=True)
    
    # Watchlist Section
    st.markdown("### 📈 Watchlist")
    for symbol, data in WATCHLIST.items():
        change_color = "green" if data["change"] >= 0 else "red"
        change_icon = "▲" if data["change"] >= 0 else "▼"
        
        if st.button(f"{symbol} - ${data['price']:.2f} {change_icon} {abs(data['change']):.2f}", 
                    key=f"btn_{symbol}", use_container_width=True):
            st.session_state.current_symbol = symbol
            st.session_state.price_data = generate_price_data(symbol)
            st.rerun()
    
    st.markdown("---")
    
    # Technical Indicators
    st.markdown("### 📊 Indicators")
    st.checkbox("RSI (14)", value=True)
    st.checkbox("MACD (12,26,9)")
    st.checkbox("Moving Average (50)")
    st.checkbox("Bollinger Bands (20)")
    
    st.markdown("---")
    
    # Time Frames
    st.markdown("### ⏰ Time Frame")
    time_frames = ["1m", "5m", "15m", "30m", "1h", "4h", "1D", "1W"]
    for tf in time_frames:
        st.button(f"• {tf}")

# ===== MAIN CHART AREA =====
st.markdown(f"## {st.session_state.current_symbol} - {WATCHLIST[st.session_state.current_symbol]['name']}")

# Display price chart
current_price = st.session_state.price_data['Price'].iloc[-1]
prev_price = st.session_state.price_data['Price'].iloc[-2]
price_change = current_price - prev_price
price_change_pct = (price_change / prev_price) * 100

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Price", f"${current_price:.2f}", f"{price_change:+.2f} ({price_change_pct:+.2f}%)")
with col2:
    st.metric("High", f"${st.session_state.price_data['Price'].max():.2f}")
with col3:
    st.metric("Low", f"${st.session_state.price_data['Price'].min():.2f}")

# Price chart
st.line_chart(st.session_state.price_data.set_index('Time'), height=400)

# ===== BOTTOM PANEL =====
st.markdown("---")

# Order entry panel
st.markdown("#### 🎯 Order Entry")
col1, col2, col3, col4 = st.columns(4)

with col1:
    order_type = st.selectbox("Order Type", ["Market", "Limit", "Stop"])
with col2:
    quantity = st.number_input("Quantity", min_value=1, value=100)
with col3:
    price = st.number_input("Price", value=float(current_price))
with col4:
    st.write("")
    st.write("")
    if st.button("🟢 BUY", type="primary", use_container_width=True):
        st.success(f"Buy order: {quantity} {st.session_state.current_symbol} @ ${current_price:.2f}")
    if st.button("🔴 SELL", type="secondary", use_container_width=True):
        st.error(f"Sell order: {quantity} {st.session_state.current_symbol} @ ${current_price:.2f}")

# ===== FOOTER =====
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6a737d; font-size: 12px;'>
    TradingView Clone • Real-time charts • Technical analysis • 
    <span style='color: #26a69a;'>Live Demo</span> • 
    Not financial advice
</div>
""", unsafe_allow_html=True)
