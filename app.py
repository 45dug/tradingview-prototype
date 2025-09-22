
  import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# ========== PAGE SETUP ==========
st.set_page_config(
    page_title="TradeVision Pro", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== SAMPLE DATA GENERATION ==========
@st.cache_data
def generate_sample_data(symbol, periods=200):
    np.random.seed(hash(symbol) % 100)
    
    # Different base prices for different symbols
    base_prices = {
        "AAPL": 180, "MSFT": 420, "TSLA": 250, 
        "GOOGL": 2800, "NVDA": 120, "BTCUSD": 65000
    }
    
    base_price = base_prices.get(symbol, 100)
    volatility = 0.7 if symbol == "BTCUSD" else 0.4
    
    # Generate timestamps
    end_time = datetime.now()
    timestamps = [end_time - timedelta(minutes=x) for x in range(periods, 0, -1)]
    
    # Generate realistic price movement
    changes = np.random.randn(periods) * volatility
    prices = base_price + np.cumsum(changes)
    
    # Create OHLC data
    opens = prices * (1 + np.random.uniform(-0.001, 0.001, periods))
    highs = prices * (1 + np.random.uniform(0.001, 0.003, periods))
    lows = prices * (1 - np.random.uniform(0.001, 0.003, periods))
    closes = prices * (1 + np.random.uniform(-0.002, 0.002, periods))
    
    volume = np.random.randint(1000, 100000, periods)
    
    df = pd.DataFrame({
        'timestamp': timestamps,
        'open': opens,
        'high': highs,
        'low': lows,
        'close': closes,
        'volume': volume
    })
    
    return df

# ========== WATCHLIST & SYMBOLS ==========
WATCHLIST = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corp.",
    "TSLA": "Tesla Inc.",
    "GOOGL": "Google LLC",
    "NVDA": "NVIDIA Corp.",
    "BTCUSD": "Bitcoin / USD"
}

# ========== INITIALIZE SESSION STATE ==========
if 'current_symbol' not in st.session_state:
    st.session_state.current_symbol = "AAPL"
if 'chart_data' not in st.session_state:
    st.session_state.chart_data = generate_sample_data("AAPL")
if 'live_mode' not in st.session_state:
    st.session_state.live_mode = False
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {"AAPL": 10, "CASH": 10000}

# ========== SIDEBAR - WATCHLIST & CONTROLS ==========
with st.sidebar:
    st.title("📊 TradeVision Pro")
    st.divider()
    
    st.header("📍 Watchlist")
    for symbol, name in WATCHLIST.items():
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("📈", key=f"btn_{symbol}"):
                st.session_state.current_symbol = symbol
                st.session_state.chart_data = generate_sample_data(symbol)
        with col2:
            current_price = st.session_state.chart_data['close'].iloc[-1]
            price_change = current_price - st.session_state.chart_data['close'].iloc[-2]
            pct_change = (price_change / st.session_state.chart_data['close'].iloc[-2]) * 100
            
            color = "green" if price_change >= 0 else "red"
            emoji = "🟢" if price_change >= 0 else "🔴"
            
            st.markdown(f"""
                **{symbol}**  
                ${current_price:.2f}  
                <span style="color:{color}">{emoji} {pct_change:+.2f}%</span>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    st.header("⚙️ Chart Settings")
    chart_type = st.selectbox("Chart Type", ["Candlestick", "Line", "Area"])
    timeframe = st.selectbox("Timeframe", ["1m", "5m", "15m", "1H", "4H", "1D"])
    
    st.divider()
    
    st.header("🔔 Alerts")
    if st.button("+ Create Alert", use_container_width=True):
        st.success("Alert created for current price level!")
    
    st.divider()
    
    st.header("💼 Portfolio")
    for asset, amount in st.session_state.portfolio.items():
        if asset != "CASH":
            price = st.session_state.chart_data['close'].iloc[-1] if asset == st.session_state.current_symbol else np.random.uniform(50, 500)
            value = amount * price
            st.write(f"{asset}: {amount} shares (${value:,.2f})")
        else:
            st.write(f"CASH: ${amount:,.2f}")

# ========== MAIN CHART AREA ==========
st.header(f"📈 {st.session_state.current_symbol} - {WATCHLIST[st.session_state.current_symbol]}")

# Create interactive chart with Plotly
fig = go.Figure()

if chart_type == "Candlestick":
    fig.add_trace(go.Candlestick(
        x=st.session_state.chart_data['timestamp'],
        open=st.session_state.chart_data['open'],
        high=st.session_state.chart_data['high'],
        low=st.session_state.chart_data['low'],
        close=st.session_state.chart_data['close'],
        name=st.session_state.current_symbol
    ))
else:
    fig.add_trace(go.Scatter(
        x=st.session_state.chart_data['timestamp'],
        y=st.session_state.chart_data['close'],
        mode='lines',
        fill='tozeroy' if chart_type == "Area" else None,
        name=st.session_state.current_symbol
    ))

fig.update_layout(
    height=500,
    showlegend=False,
    xaxis_rangeslider_visible=False,
    template="plotly_white",
    margin=dict(l=20, r=20, t=30, b=20)
)

st.plotly_chart(fig, use_container_width=True)

# ========== LIVE SIMULATION CONTROLS ==========
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    if st.button("▶️ Start Live Simulation" if not st.session_state.live_mode else "⏸️ Pause Live Simulation"):
        st.session_state.live_mode = not st.session_state.live_mode

with col2:
    if st.button("🔁 Reset Chart"):
        st.session_state.chart_data = generate_sample_data(st.session_state.current_symbol)
        st.session_state.live_mode = False

# Live simulation update
if st.session_state.live_mode:
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(50):
        if not st.session_state.live_mode:
            break
            
        # Generate new data point
        last_close = st.session_state.chart_data['close'].iloc[-1]
        new_close = last_close * (1 + np.random.uniform(-0.005, 0.005))
        new_high = new_close * (1 + np.random.uniform(0.001, 0.003))
        new_low = new_close * (1 - np.random.uniform(0.001, 0.003))
        new_open = new_close * (1 + np.random.uniform(-0.002, 0.002))
        
        new_row = pd.DataFrame({
            'timestamp': [datetime.now()],
            'open': [new_open],
            'high': [new_high],
            'low': [new_low],
            'close': [new_close],
            'volume': [np.random.randint(1000, 50000)]
        })
        
        st.session_state.chart_data = pd.concat([
            st.session_state.chart_data.iloc[1:],  # Remove oldest point
            new_row
        ], ignore_index=True)
        
        progress_bar.progress((i + 1) / 50)
        status_text.text(f"🔄 Live updating... {i + 1}/50")
        time.sleep(0.3)
    
    progress_bar.empty()
    status_text.empty()
    st.session_state.live_mode = False
    st.rerun()

# ========== ORDER ENTRY PANEL ==========
st.divider()
st.subheader("🎯 Order Entry")

col1, col2, col3, col4 = st.columns(4)

with col1:
    order_type = st.selectbox("Order Type", ["Market", "Limit", "Stop"])

with col2:
    quantity = st.number_input("Quantity", min_value=1, value=10, step=1)

with col3:
    current_price = st.session_state.chart_data['close'].iloc[-1]
    price = st.number_input("Price", value=float(current_price), 
                           disabled=(order_type == "Market"))

with col4:
    st.write("")  # Spacer
    st.write("")
    if st.button("🟢 BUY", type="primary", use_container_width=True):
        st.success(f"✅ Buy order for {quantity} {st.session_state.current_symbol} at ${current_price:.2f}!")
    if st.button("🔴 SELL", type="secondary", use_container_width=True):
        st.error(f"✅ Sell order for {quantity} {st.session_state.current_symbol} at ${current_price:.2f}!")

# ========== MARKET DATA SUMMARY ==========
st.divider()
st.subheader("📊 Market Summary")

col1, col2, col3, col4 = st.columns(4)

current_data = st.session_state.chart_data.iloc[-1]
prev_data = st.session_state.chart_data.iloc[-2]

price_change = current_data['close'] - prev_data['close']
pct_change = (price_change / prev_data['close']) * 100

with col1:
    st.metric(
        label="Current Price",
        value=f"${current_data['close']:.2f}",
        delta=f"{pct_change:+.2f}%"
    )

with col2:
    st.metric("Today's High", f"${current_data['high']:.2f}")

with col3:
    st.metric("Today's Low", f"${current_data['low']:.2f}")

with col4:
    st.metric("Volume", f"{current_data['volume']:,.0f}")

# ========== FOOTER ==========
st.divider()
st.caption("""
    **TradeVision Pro** • Real-time trading prototype • 
    Data is simulated for demonstration purposes • 
    Not financial advice
""")
