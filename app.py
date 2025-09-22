import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
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
</style>
""", unsafe_allow_html=True)

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="TradingView Clone",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== SAMPLE DATA =====
def generate_tradingview_data(symbol, periods=100):
    np.random.seed(hash(symbol) % 100)
    
    base_prices = {"AAPL": 180, "MSFT": 420, "TSLA": 250, "BTCUSD": 65000}
    base_price = base_prices.get(symbol, 100)
    volatility = 0.8 if symbol == "BTCUSD" else 0.5
    
    dates = [datetime.now() - timedelta(minutes=x) for x in range(periods, 0, -1)]
    
    # Generate realistic OHLC data
    prices = base_price + np.cumsum(np.random.randn(periods) * volatility)
    opens = prices * (1 + np.random.uniform(-0.002, 0.002, periods))
    highs = prices * (1 + np.random.uniform(0.003, 0.008, periods))
    lows = prices * (1 - np.random.uniform(0.003, 0.008, periods))
    closes = prices * (1 + np.random.uniform(-0.004, 0.004, periods))
    
    return pd.DataFrame({
        'time': dates,
        'open': opens, 'high': highs, 'low': lows, 'close': closes,
        'volume': np.random.randint(1000, 50000, periods)
    })

# ===== WATCHLIST DATA =====
WATCHLIST = {
    "AAPL": {"name": "Apple Inc.", "price": 180.25, "change": +1.25, "change_pct": +0.70},
    "MSFT": {"name": "Microsoft", "price": 421.80, "change": -2.30, "change_pct": -0.54},
    "TSLA": {"name": "Tesla Inc.", "price": 248.90, "change": +5.60, "change_pct": +2.30},
    "BTCUSD": {"name": "Bitcoin", "price": 65123.45, "change": +1234.56, "change_pct": +1.93},
    "NVDA": {"name": "NVIDIA", "price": 122.75, "change": -1.25, "change_pct": -1.01},
    "GOOGL": {"name": "Google", "price": 2798.30, "change": +15.80, "change_pct": +0.57}
}

# ===== SESSION STATE =====
if 'current_symbol' not in st.session_state:
    st.session_state.current_symbol = "AAPL"
if 'chart_data' not in st.session_state:
    st.session_state.chart_data = generate_tradingview_data("AAPL")

# ===== SIDEBAR - TRADINGVIEW STYLE =====
with st.sidebar:
    st.markdown("<h1 style='color: #2962ff; margin-bottom: 30px;'>TradingView</h1>", unsafe_allow_html=True)
    
    # Watchlist Section
    st.markdown("### 📈 Watchlist")
    for symbol, data in WATCHLIST.items():
        change_color = "green" if data["change"] >= 0 else "red"
        change_icon = "▲" if data["change"] >= 0 else "▼"
        
        st.markdown(f"""
        <div class='watchlist-item' onclick='window.symbolClick("{symbol}")'>
            <div style='display: flex; justify-content: space-between;'>
                <strong>{symbol}</strong>
                <span class='{change_color}'>${data['price']:.2f}</span>
            </div>
            <div style='display: flex; justify-content: space-between; font-size: 12px;'>
                <span>{data['name']}</span>
                <span class='{change_color}'>{change_icon} {data['change_pct']:.2f}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Technical Indicators
    st.markdown("### 📊 Indicators")
    indicators = ["MACD", "RSI", "Moving Average", "Bollinger Bands", "Volume"]
    for indicator in indicators:
        st.checkbox(f"• {indicator}", value=True if indicator == "RSI" else False)
    
    st.markdown("---")
    
    # Drawing Tools
    st.markdown("### 🛠️ Drawing Tools")
    tools = ["Trend Line", "Horizontal Line", "Fibonacci", "Text", "Arrow"]
    for tool in tools:
        st.button(f"• {tool}")

# ===== MAIN CHART AREA =====
col1, col2 = st.columns([8, 2])
with col1:
    st.markdown(f"### {st.session_state.current_symbol} - {WATCHLIST[st.session_state.current_symbol]['name']}")

# Chart type selector
chart_type = st.selectbox("Chart Type", ["Candlestick", "Line", "Area", "Heikin Ashi"], label_visibility="collapsed")

# Create TradingView-style chart
fig = go.Figure()

if chart_type == "Candlestick":
    fig.add_trace(go.Candlestick(
        x=st.session_state.chart_data['time'],
        open=st.session_state.chart_data['open'],
        high=st.session_state.chart_data['high'],
        low=st.session_state.chart_data['low'],
        close=st.session_state.chart_data['close'],
        increasing_line_color='#26a69a',
        decreasing_line_color='#ef5350',
        name=st.session_state.current_symbol
    ))
else:
    fig.add_trace(go.Scatter(
        x=st.session_state.chart_data['time'],
        y=st.session_state.chart_data['close'],
        mode='lines',
        line=dict(color='#2962ff', width=2),
        name=st.session_state.current_symbol
    ))

# Update layout to match TradingView dark theme
fig.update_layout(
    height=600,
    plot_bgcolor='#131722',
    paper_bgcolor='#131722',
    font=dict(color='#d1d4dc'),
    xaxis=dict(gridcolor='#2a2e39'),
    yaxis=dict(gridcolor='#2a2e39'),
    showlegend=False,
    xaxis_rangeslider_visible=False,
    margin=dict(l=20, r=20, t=30, b=20)
)

st.plotly_chart(fig, use_container_width=True)

# ===== BOTTOM PANEL - TRADINGVIEW STYLE =====
st.markdown("---")

# Order entry panel
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("#### 🎯 Order Entry")
    order_type = st.selectbox("Type", ["Market", "Limit", "Stop", "Stop Limit"])
with col2:
    quantity = st.number_input("Quantity", min_value=1, value=100)
with col3:
    current_price = st.session_state.chart_data['close'].iloc[-1]
    price = st.number_input("Price", value=float(current_price))
with col4:
    st.write("")
    st.write("")
    if st.button("BUY", type="primary"):
        st.success(f"Market Buy {quantity} {st.session_state.current_symbol}")
    if st.button("SELL"):
        st.error(f"Market Sell {quantity} {st.session_state.current_symbol}")

# ===== FOOTER =====
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6a737d; font-size: 12px;'>
    TradingView Clone • Real-time charts • Technical analysis • 
    <span style='color: #26a69a;'>Demo Mode</span> • 
    Not financial advice
</div>
""", unsafe_allow_html=True)

# JavaScript for symbol clicks
st.markdown("""
<script>
function symbolClick(symbol) {
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: symbol
    }, '*');
}
</script>
""", unsafe_allow_html=True)
